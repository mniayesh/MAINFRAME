"""
Biologically-Inspired AI Architecture Components
Based on 595 formulas from bioformulas.db

This module provides PyTorch implementations of neural network components
derived from biological formulas including:
- Hill activation functions (cooperative nonlinearity)
- Ion channel gating mechanisms (m^n * h dynamics)
- Synaptic temporal kernels (dual-exponential)
- Plasticity rules (STDP, BCM, Oja)
- Population dynamics (Wilson-Cowan E-I balance)
- Oscillatory coupling (Kuramoto)

Author: Generated from bioformulas database analysis
Date: 2025-12-10
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Optional, Tuple, List


# =============================================================================
# 1. ACTIVATION FUNCTIONS
# =============================================================================

class HillActivation(nn.Module):
    """
    Hill equation-based activation with learnable cooperativity.

    From database: "Hill Equation" (rate_equation)
    LaTeX: v = V_max * [S]^n / (K_0.5^n + [S]^n)

    Provides tunable steepness via Hill coefficient n, unlike fixed sigmoid/ReLU.
    """

    def __init__(self, dim: int, init_n: float = 2.0, init_k: float = 1.0):
        """
        Args:
            dim: Number of features
            init_n: Initial Hill coefficient (cooperativity), typically 1-4
            init_k: Initial half-maximal activation point
        """
        super().__init__()
        self.n = nn.Parameter(torch.full((dim,), init_n))
        self.k = nn.Parameter(torch.full((dim,), init_k))
        self.vmax = nn.Parameter(torch.ones(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Apply Hill activation element-wise with sign preservation.

        Args:
            x: Input tensor [..., dim]

        Returns:
            Activated tensor with same shape as input
        """
        sign = torch.sign(x)
        abs_x = torch.abs(x)
        n = F.softplus(self.n)  # Ensure n > 0
        k = F.softplus(self.k)  # Ensure k > 0

        numerator = self.vmax * torch.pow(abs_x + 1e-8, n)
        denominator = torch.pow(k, n) + torch.pow(abs_x + 1e-8, n)

        return sign * (numerator / (denominator + 1e-8))


class BoltzmannActivation(nn.Module):
    """
    Voltage-gated channel-inspired activation with learnable threshold and slope.

    From database: "Nav1.1 Activation" (algebraic, ion-channels)
    LaTeX: m_∞ = 1 / (1 + exp((V_1/2,m - V)/k_m))

    Provides learnable activation threshold, unlike fixed sigmoid.
    """

    def __init__(self, dim: int):
        """
        Args:
            dim: Number of features
        """
        super().__init__()
        self.v_half = nn.Parameter(torch.zeros(dim))  # Activation threshold
        self.k = nn.Parameter(torch.ones(dim))        # Slope factor

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Apply Boltzmann sigmoid with learnable midpoint and slope.

        Args:
            x: Input tensor [..., dim]

        Returns:
            Activated tensor in range (0, 1)
        """
        return torch.sigmoid((x - self.v_half) / (torch.abs(self.k) + 1e-8))


class HHAlphaActivation(nn.Module):
    """
    Hodgkin-Huxley alpha-function activation (rational exponential).

    From database: "Generic HH Alpha Rate" (ion-channels)
    LaTeX: α(V) = A(V - V_0) / (1 - exp(-(V - V_0)/k))

    Combines linear and exponential terms for richer dynamics.
    """

    def __init__(self, dim: int):
        super().__init__()
        self.A = nn.Parameter(torch.ones(dim) * 0.1)
        self.V0 = nn.Parameter(torch.zeros(dim))
        self.k = nn.Parameter(torch.ones(dim) * 10.0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        v_shifted = x - self.V0
        exp_term = torch.exp(-v_shifted / (self.k + 1e-8))
        return self.A * v_shifted / (1 - exp_term + 1e-8)


# =============================================================================
# 2. GATING MECHANISMS
# =============================================================================

class ChannelGate(nn.Module):
    """
    Ion channel-inspired gating with m^n * h * (V - E_rev) dynamics.

    From database: "Nav1.1 Sodium Current (SCN1A)" (current_equation)
    LaTeX: I = g_max * m^3 * h * (V - E_Na)

    Features:
    - Power-law activation (m^n) for sharp switching
    - Separate inactivation gate (h)
    - Driving force (V - E_rev) for context-dependent saturation
    - Dual timescales (fast m, slow h)
    """

    def __init__(self, dim: int, power: int = 3):
        """
        Args:
            dim: Number of features
            power: Exponent for activation gate (typically 3-4)
        """
        super().__init__()
        self.power = power

        # Activation gate (m) - fast dynamics
        self.W_m = nn.Linear(dim, dim)
        self.tau_m = nn.Parameter(torch.ones(dim) * 5.0)

        # Inactivation gate (h) - slow dynamics
        self.W_h = nn.Linear(dim, dim)
        self.tau_h = nn.Parameter(torch.ones(dim) * 50.0)

        # Reversal potential
        self.E_rev = nn.Parameter(torch.zeros(dim))

        # State variables
        self.register_buffer('m_state', torch.zeros(1, dim))
        self.register_buffer('h_state', torch.ones(1, dim))

    def forward(self, x: torch.Tensor, dt: float = 1.0) -> torch.Tensor:
        """
        Apply channel gating dynamics.

        Args:
            x: Input tensor [batch, dim]
            dt: Time step for integration (default 1.0)

        Returns:
            Gated output [batch, dim]
        """
        batch_size = x.size(0)

        # Steady-state gating values
        m_inf = torch.sigmoid(self.W_m(x))
        h_inf = torch.sigmoid(-self.W_h(x))  # Inverted for inactivation

        if self.training:
            # Temporal integration: dx/dt = (x_inf - x)/tau
            m = self.m_state.expand(batch_size, -1)
            h = self.h_state.expand(batch_size, -1)

            m = m + dt * (m_inf - m) / (F.softplus(self.tau_m) + 1e-8)
            h = h + dt * (h_inf - h) / (F.softplus(self.tau_h) + 1e-8)

            # Update running state
            self.m_state = m.mean(0, keepdim=True).detach()
            self.h_state = h.mean(0, keepdim=True).detach()
        else:
            m, h = m_inf, h_inf

        # Channel current: I = m^n * h * (V - E_rev)
        conductance = torch.pow(m, self.power) * h
        driving_force = x - self.E_rev

        return conductance * driving_force

    def reset_state(self):
        """Reset state variables (call between sequences)"""
        self.m_state.zero_()
        self.h_state.fill_(1.0)


class MultiTimescaleGate(nn.Module):
    """
    Multiple gating variables with hierarchical time constants.

    From database: Multiple synaptic timescales
    - AMPA: τ_rise=0.5ms, τ_decay=3ms (fast)
    - NMDA: τ_rise=2ms, τ_decay=100ms (slow)

    Enables multi-timescale memory without explicit recurrence.
    """

    def __init__(self, dim: int, n_timescales: int = 3):
        """
        Args:
            dim: Number of features
            n_timescales: Number of parallel timescales (default 3)
        """
        super().__init__()
        self.n_timescales = n_timescales

        # Geometric spacing of time constants: 5ms, 50ms, 500ms
        tau_init = torch.logspace(np.log10(5), np.log10(500), n_timescales)
        self.tau = nn.Parameter(tau_init.unsqueeze(-1).expand(-1, dim))

        # Separate projection for each timescale
        self.W = nn.ModuleList([nn.Linear(dim, dim) for _ in range(n_timescales)])

        # Learnable mixing weights
        self.alpha = nn.Parameter(torch.ones(n_timescales, dim) / n_timescales)

        # State for each timescale
        self.register_buffer('states', torch.zeros(n_timescales, 1, dim))

    def forward(self, x: torch.Tensor, dt: float = 1.0) -> torch.Tensor:
        """
        Apply multi-timescale gating.

        Args:
            x: Input [batch, dim]
            dt: Time step

        Returns:
            Mixed output [batch, dim]
        """
        batch_size = x.size(0)
        outputs = []

        for i in range(self.n_timescales):
            # Steady-state value
            x_inf = torch.sigmoid(self.W[i](x))

            # Leaky integration
            state = self.states[i].expand(-1, batch_size, -1)
            tau_safe = F.softplus(self.tau[i]) + 1e-8
            state = state + dt * (x_inf - state) / tau_safe

            if self.training:
                self.states[i] = state.mean(1, keepdim=True).detach()

            outputs.append(state.squeeze(0))

        # Weighted combination
        outputs = torch.stack(outputs, dim=0)  # [n_timescales, batch, dim]
        alpha_norm = F.softmax(self.alpha, dim=0).unsqueeze(1)

        return (outputs * alpha_norm).sum(0)

    def reset_state(self):
        """Reset all state variables"""
        self.states.zero_()


# =============================================================================
# 3. TEMPORAL DYNAMICS
# =============================================================================

class LeakyResidualBlock(nn.Module):
    """
    Leaky integrate-and-fire inspired residual connection.

    From database: "Leaky Integrate-and-Fire" (ODE)
    LaTeX: τ_m * dV/dt = -(V - V_rest) + R_m * I_ext

    Provides learnable residual mixing ratio (adaptive skip connections).
    """

    def __init__(self, dim: int, init_tau: float = 10.0, mlp_ratio: int = 4):
        """
        Args:
            dim: Feature dimension
            init_tau: Initial time constant (higher = slower adaptation)
            mlp_ratio: MLP expansion ratio (default 4)
        """
        super().__init__()
        self.tau = nn.Parameter(torch.full((dim,), init_tau))
        self.V_rest = nn.Parameter(torch.zeros(dim))

        self.transform = nn.Sequential(
            nn.Linear(dim, dim * mlp_ratio),
            nn.GELU(),
            nn.Linear(dim * mlp_ratio, dim)
        )

    def forward(self, x: torch.Tensor, dt: float = 1.0) -> torch.Tensor:
        """
        Apply leaky residual update.

        Args:
            x: Input [batch, dim]
            dt: Time step

        Returns:
            Updated state [batch, dim]
        """
        F_x = self.transform(x)
        tau_safe = F.softplus(self.tau) + 1e-8

        # Leaky integration: dV/dt = -(V - V_rest)/tau + F(V)
        decay = dt / tau_safe
        x_new = x + decay * (-(x - self.V_rest) + F_x)

        return x_new


class SynapticConv1D(nn.Module):
    """
    1D convolution with dual-exponential synaptic kernels.

    From database: Synaptic dynamics
    - AMPA: τ_rise=0.5ms, τ_decay=3ms
    - NMDA: τ_rise=2ms, τ_decay=100ms

    Kernel shape: A * (exp(-t/τ_decay) - exp(-t/τ_rise))
    """

    def __init__(self, in_channels: int, out_channels: int, kernel_size: int = 20):
        """
        Args:
            in_channels: Number of input channels
            out_channels: Number of output channels
            kernel_size: Temporal kernel size
        """
        super().__init__()
        self.kernel_size = kernel_size

        # Learnable time constants (per output-input pair)
        self.tau_rise = nn.Parameter(torch.ones(out_channels, in_channels) * 2.0)
        self.tau_decay = nn.Parameter(torch.ones(out_channels, in_channels) * 10.0)

        # Amplitude
        self.weight = nn.Parameter(torch.randn(out_channels, in_channels))

    def get_kernel(self) -> torch.Tensor:
        """
        Generate dual-exponential kernel.

        Returns:
            Kernel [out_channels, in_channels, kernel_size]
        """
        t = torch.arange(self.kernel_size, dtype=torch.float32,
                        device=self.weight.device)
        t = t.view(1, 1, -1)

        tau_r = F.softplus(self.tau_rise).unsqueeze(-1) + 1e-8
        tau_d = F.softplus(self.tau_decay).unsqueeze(-1) + tau_r  # Ensure τ_d > τ_r

        # Dual exponential
        kernel = torch.exp(-t / tau_d) - torch.exp(-t / tau_r)

        # Normalize
        kernel = kernel / (kernel.sum(-1, keepdim=True) + 1e-8)

        return self.weight.unsqueeze(-1) * kernel

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Apply synaptic convolution.

        Args:
            x: Input [batch, in_channels, time]

        Returns:
            Output [batch, out_channels, time]
        """
        kernel = self.get_kernel()
        return F.conv1d(x, kernel, padding=self.kernel_size // 2)


# =============================================================================
# 4. PLASTICITY RULES
# =============================================================================

class STDPLayer(nn.Module):
    """
    Spike-timing-dependent plasticity for unsupervised learning.

    From database: "Pair-Based STDP" (synaptic-plasticity)
    LaTeX: Δw = A_+ * exp(-Δt/τ_+) if Δt > 0 (LTP)
                -A_- * exp(Δt/τ_-) if Δt < 0 (LTD)

    Implements local, Hebbian learning without backpropagation.
    """

    def __init__(self, in_features: int, out_features: int,
                 tau_plus: float = 20.0, tau_minus: float = 20.0,
                 A_plus: float = 0.01, A_minus: float = 0.01):
        """
        Args:
            in_features: Input dimension
            out_features: Output dimension
            tau_plus: LTP time constant (ms)
            tau_minus: LTD time constant (ms)
            A_plus: LTP amplitude
            A_minus: LTD amplitude
        """
        super().__init__()

        self.weight = nn.Parameter(torch.randn(out_features, in_features) * 0.01)

        self.tau_plus = tau_plus
        self.tau_minus = tau_minus
        self.A_plus = A_plus
        self.A_minus = A_minus

        # Eligibility traces
        self.register_buffer('pre_trace', torch.zeros(1, in_features))
        self.register_buffer('post_trace', torch.zeros(1, out_features))

    def forward(self, x_spikes: torch.Tensor) -> torch.Tensor:
        """
        Forward pass (converts spikes to membrane potential to output spikes).

        Args:
            x_spikes: Input spikes [batch, in_features] (binary or rates)

        Returns:
            Output spikes [batch, out_features]
        """
        v = F.linear(x_spikes, torch.clamp(self.weight, 0, 1))  # Only excitatory
        spike_prob = torch.sigmoid(v)
        out_spikes = (torch.rand_like(spike_prob) < spike_prob).float()
        return out_spikes

    def stdp_update(self, pre_spikes: torch.Tensor, post_spikes: torch.Tensor,
                   dt: float = 1.0, lr: float = 1e-4):
        """
        Apply STDP weight update rule.

        Args:
            pre_spikes: Pre-synaptic spikes [batch, in_features]
            post_spikes: Post-synaptic spikes [batch, out_features]
            dt: Time step
            lr: Learning rate
        """
        # Update traces
        decay_pre = torch.exp(torch.tensor(-dt / self.tau_minus))
        decay_post = torch.exp(torch.tensor(-dt / self.tau_plus))

        pre_trace = self.pre_trace * decay_pre + pre_spikes.mean(0, keepdim=True)
        post_trace = self.post_trace * decay_post + post_spikes.mean(0, keepdim=True)

        # STDP updates
        # LTP: post spike strengthens weights from recent pre-spikes
        dw_ltp = self.A_plus * torch.outer(post_spikes.mean(0), pre_trace.squeeze(0))

        # LTD: pre spike weakens weights to recent post-spikes
        dw_ltd = self.A_minus * torch.outer(post_trace.squeeze(0), pre_spikes.mean(0))

        with torch.no_grad():
            self.weight += lr * (dw_ltp - dw_ltd)
            self.weight.clamp_(0, 1)

        self.pre_trace = pre_trace.detach()
        self.post_trace = post_trace.detach()

    def reset_traces(self):
        """Reset eligibility traces"""
        self.pre_trace.zero_()
        self.post_trace.zero_()


class BCMLayer(nn.Module):
    """
    Bienenstock-Cooper-Munro learning rule with sliding threshold.

    From database: "BCM Sliding Threshold" (metaplasticity)
    LaTeX: dθ/dt = (c̄² - θ)/τ_θ
    Learning: Δw = η * y * (y - θ) * x

    Provides stable unsupervised learning with activity-dependent threshold.
    """

    def __init__(self, in_features: int, out_features: int, tau_theta: float = 1000.0):
        super().__init__()

        self.weight = nn.Parameter(torch.randn(out_features, in_features) * 0.01)
        self.tau_theta = tau_theta

        self.register_buffer('theta', torch.ones(out_features) * 0.5)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return F.linear(x, self.weight)

    def bcm_update(self, x: torch.Tensor, y: torch.Tensor,
                  dt: float = 1.0, lr: float = 1e-3):
        """
        Apply BCM learning update.

        Args:
            x: Input [batch, in_features]
            y: Output [batch, out_features]
            dt: Time step
            lr: Learning rate
        """
        y_mean = y.mean(0)
        x_mean = x.mean(0)

        # BCM term: y * (y - θ)
        bcm_term = y_mean * (y_mean - self.theta)

        # Weight update
        dw = torch.outer(bcm_term, x_mean)

        with torch.no_grad():
            self.weight += lr * dw

            # Update sliding threshold
            self.theta += dt * ((y_mean ** 2) - self.theta) / self.tau_theta


class OjaLayer(nn.Module):
    """
    Oja's learning rule for principal component analysis.

    From database: "Oja's Learning Rule" (synaptic-plasticity)
    LaTeX: Δw_i = η * y * (x_i - y * w_i)

    Converges to principal component with built-in weight normalization.
    """

    def __init__(self, in_features: int, out_features: int):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(out_features, in_features) * 0.01)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return F.linear(x, self.weight)

    def oja_update(self, x: torch.Tensor, y: torch.Tensor, lr: float = 1e-3):
        """
        Apply Oja's rule update.

        Args:
            x: Input [batch, in_features]
            y: Output [batch, out_features]
            lr: Learning rate
        """
        # Oja: Δw = η * y * (x - y * w)
        # Equivalent to: Δw = η * (y ⊗ x - y ⊗ y * w)
        hebbian = torch.outer(y.mean(0), x.mean(0))
        decay = torch.outer(y.mean(0), y.mean(0)) @ self.weight

        with torch.no_grad():
            self.weight += lr * (hebbian - decay)


# =============================================================================
# 5. POPULATION DYNAMICS
# =============================================================================

class WilsonCowanLayer(nn.Module):
    """
    Excitatory-Inhibitory balanced population dynamics.

    From database: "Wilson-Cowan Excitatory/Inhibitory" (neural-networks)
    LaTeX:
        τ_E * dE/dt = -E + S_E(w_EE*E - w_EI*I + I_ext)
        τ_I * dI/dt = -I + S_I(w_IE*E - w_II*I)

    Provides self-stabilizing dynamics through lateral inhibition.
    """

    def __init__(self, dim: int, ratio_ei: float = 0.8):
        """
        Args:
            dim: Total dimension
            ratio_ei: Fraction of excitatory units (default 0.8 = 80% E, 20% I)
        """
        super().__init__()

        self.dim_e = int(dim * ratio_ei)
        self.dim_i = dim - self.dim_e

        # Connection weights
        self.W_ee = nn.Linear(self.dim_e, self.dim_e)
        self.W_ei = nn.Linear(self.dim_i, self.dim_e)
        self.W_ie = nn.Linear(self.dim_e, self.dim_i)
        self.W_ii = nn.Linear(self.dim_i, self.dim_i)

        # Time constants (inhibition typically faster)
        self.tau_e = nn.Parameter(torch.tensor(10.0))
        self.tau_i = nn.Parameter(torch.tensor(5.0))

        # State
        self.register_buffer('E_state', torch.zeros(1, self.dim_e))
        self.register_buffer('I_state', torch.zeros(1, self.dim_i))

    def forward(self, x: torch.Tensor, dt: float = 1.0, n_steps: int = 3) -> torch.Tensor:
        """
        Apply Wilson-Cowan dynamics.

        Args:
            x: Input [batch, dim]
            dt: Time step
            n_steps: Number of iterative refinement steps

        Returns:
            Output [batch, dim] (concatenated E and I)
        """
        batch_size = x.size(0)

        # Split input
        x_e = x[:, :self.dim_e]
        x_i = x[:, self.dim_e:]

        # Initialize state
        E = self.E_state.expand(batch_size, -1).clone()
        I = self.I_state.expand(batch_size, -1).clone()

        # Iterate dynamics
        for _ in range(n_steps):
            # E dynamics
            E_input = self.W_ee(E) - self.W_ei(I) + x_e
            dE = (-E + torch.tanh(E_input)) / (F.softplus(self.tau_e) + 1e-8)

            # I dynamics
            I_input = self.W_ie(E) - self.W_ii(I) + x_i
            dI = (-I + torch.tanh(I_input)) / (F.softplus(self.tau_i) + 1e-8)

            E = E + dt * dE
            I = I + dt * dI

        if self.training:
            self.E_state = E.mean(0, keepdim=True).detach()
            self.I_state = I.mean(0, keepdim=True).detach()

        return torch.cat([E, I], dim=-1)

    def reset_state(self):
        """Reset state variables"""
        self.E_state.zero_()
        self.I_state.zero_()


class KuramotoLayer(nn.Module):
    """
    Kuramoto phase oscillators for synchronization.

    From database: "Coupled Oscillators (Kuramoto)" (oscillations)
    LaTeX: dθ_i/dt = ω_i + (K/N) * Σ_j sin(θ_j - θ_i)

    Enables emergent synchronization and phase coding.
    """

    def __init__(self, n_oscillators: int, coupling_strength: float = 1.0):
        super().__init__()

        self.n = n_oscillators

        # Natural frequencies (learnable)
        self.omega = nn.Parameter(torch.randn(n_oscillators) * 0.1)

        # Coupling strength
        self.K = nn.Parameter(torch.tensor(coupling_strength))

        # Phase state
        self.register_buffer('theta', torch.rand(1, n_oscillators) * 2 * np.pi)

    def forward(self, x: torch.Tensor, dt: float = 0.1) -> torch.Tensor:
        """
        Apply Kuramoto dynamics.

        Args:
            x: Input driving forces [batch, n_oscillators]
            dt: Time step

        Returns:
            Phase-encoded output [batch, n_oscillators * 2] (cos, sin)
        """
        batch_size = x.size(0)
        theta = self.theta.expand(batch_size, -1).clone()

        # Phase differences
        theta_diff = theta.unsqueeze(1) - theta.unsqueeze(2)  # [batch, n, n]
        coupling = torch.sin(theta_diff).mean(1)  # [batch, n]

        # Kuramoto equation
        dtheta = self.omega + self.K * coupling + x

        # Update
        theta = (theta + dt * dtheta) % (2 * np.pi)

        if self.training:
            self.theta = theta.mean(0, keepdim=True).detach()

        # Output as cos/sin pairs
        return torch.stack([torch.cos(theta), torch.sin(theta)], dim=-1).flatten(-2)

    def reset_state(self):
        """Reset phase states"""
        self.theta.uniform_(0, 2 * np.pi)


# =============================================================================
# 6. COMPOSITE ARCHITECTURES
# =============================================================================

class BioTransformerBlock(nn.Module):
    """
    Biologically-inspired transformer block combining multiple bio-components.

    Integrates:
    - Hill activation
    - Channel gating (m^3 * h)
    - Leaky residual connections
    - Multi-timescale integration
    """

    def __init__(self, dim: int, n_heads: int = 8, n_timescales: int = 3,
                 mlp_ratio: int = 4):
        super().__init__()

        # Standard multi-head attention
        self.attn = nn.MultiheadAttention(dim, n_heads, batch_first=True)

        # Normalization
        self.norm1 = nn.LayerNorm(dim)
        self.norm2 = nn.LayerNorm(dim)

        # Bio-inspired MLP
        self.mlp = nn.Sequential(
            nn.Linear(dim, dim * mlp_ratio),
            HillActivation(dim * mlp_ratio, init_n=2.0),
            ChannelGate(dim * mlp_ratio, power=3),
            nn.Linear(dim * mlp_ratio, dim)
        )

        # Leaky residual time constants
        self.tau1 = nn.Parameter(torch.tensor(10.0))
        self.tau2 = nn.Parameter(torch.tensor(10.0))

        # Multi-timescale integration
        self.multi_time = MultiTimescaleGate(dim, n_timescales)

    def forward(self, x: torch.Tensor, dt: float = 1.0) -> torch.Tensor:
        """
        Forward pass through bio-transformer block.

        Args:
            x: Input [batch, seq_len, dim]
            dt: Time step for dynamics

        Returns:
            Output [batch, seq_len, dim]
        """
        # Attention with leaky residual
        attn_out, _ = self.attn(x, x, x)
        decay1 = dt / (F.softplus(self.tau1) + 1e-8)
        x = x + decay1 * (attn_out - x)
        x = self.norm1(x)

        # Process sequence position-wise
        batch, seq_len, dim = x.shape
        x_flat = x.reshape(-1, dim)

        # MLP with bio-components
        mlp_out = self.mlp(x_flat)

        # Multi-timescale integration
        mlp_out = self.multi_time(mlp_out, dt)

        mlp_out = mlp_out.reshape(batch, seq_len, dim)

        # Leaky residual
        decay2 = dt / (F.softplus(self.tau2) + 1e-8)
        x = x + decay2 * (mlp_out - x)
        x = self.norm2(x)

        return x


class SynapticTCN(nn.Module):
    """
    Temporal Convolutional Network with synaptic kernels.

    Uses dual-exponential kernels matching AMPA/NMDA dynamics.
    """

    def __init__(self, in_channels: int, channels: List[int] = [64, 128, 256],
                 kernel_size: int = 20):
        super().__init__()

        layers = []
        prev_channels = in_channels

        for i, out_channels in enumerate(channels):
            # Alternate between fast (AMPA-like) and slow (NMDA-like) kernels
            is_fast = (i < len(channels) // 2)
            tau_rise = 0.5 if is_fast else 2.0
            tau_decay = 3.0 if is_fast else 100.0

            conv = SynapticConv1D(prev_channels, out_channels, kernel_size)
            conv.tau_rise.data.fill_(tau_rise)
            conv.tau_decay.data.fill_(tau_decay)

            layers.append(conv)
            layers.append(HillActivation(out_channels))

            prev_channels = out_channels

        self.network = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: Input [batch, in_channels, time]

        Returns:
            Output [batch, out_channels, time]
        """
        return self.network(x)


# =============================================================================
# 7. UTILITY FUNCTIONS
# =============================================================================

def reset_all_states(module: nn.Module):
    """
    Recursively reset all stateful components in a module.

    Args:
        module: PyTorch module containing bio-components
    """
    for child in module.modules():
        if hasattr(child, 'reset_state'):
            child.reset_state()
        elif hasattr(child, 'reset_traces'):
            child.reset_traces()


def count_learnable_timescales(module: nn.Module) -> int:
    """
    Count learnable time constant parameters in a module.

    Args:
        module: PyTorch module

    Returns:
        Total number of learnable τ parameters
    """
    count = 0
    for name, param in module.named_parameters():
        if 'tau' in name.lower():
            count += param.numel()
    return count


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("Biologically-Inspired AI Components")
    print("=" * 80)

    # Example 1: Hill Activation
    print("\n1. Hill Activation")
    x = torch.randn(32, 128)
    hill = HillActivation(128, init_n=2.0)
    y = hill(x)
    print(f"   Input shape: {x.shape}, Output shape: {y.shape}")
    print(f"   Learned Hill coefficients (n): min={hill.n.min():.2f}, max={hill.n.max():.2f}")

    # Example 2: Channel Gate
    print("\n2. Channel Gate (m^3 * h dynamics)")
    gate = ChannelGate(128, power=3)
    y = gate(x, dt=1.0)
    print(f"   Output shape: {y.shape}")
    print(f"   Activation τ: {gate.tau_m.mean():.2f}, Inactivation τ: {gate.tau_h.mean():.2f}")

    # Example 3: Multi-timescale Gate
    print("\n3. Multi-Timescale Gate")
    mtg = MultiTimescaleGate(128, n_timescales=3)
    y = mtg(x)
    print(f"   Output shape: {y.shape}")
    print(f"   Time constants: {mtg.tau[:, 0].detach().numpy()}")

    # Example 4: Synaptic Conv
    print("\n4. Synaptic Temporal Convolution")
    x_seq = torch.randn(8, 16, 100)  # [batch, channels, time]
    conv = SynapticConv1D(16, 32, kernel_size=20)
    y = conv(x_seq)
    print(f"   Input: {x_seq.shape}, Output: {y.shape}")

    # Example 5: STDP Layer
    print("\n5. STDP Unsupervised Learning")
    stdp = STDPLayer(784, 128)
    spikes_in = (torch.rand(32, 784) > 0.9).float()
    spikes_out = stdp(spikes_in)
    stdp.stdp_update(spikes_in, spikes_out, lr=1e-3)
    print(f"   Input spikes: {spikes_in.sum().item():.0f}, Output spikes: {spikes_out.sum().item():.0f}")

    # Example 6: Wilson-Cowan E-I Balance
    print("\n6. Wilson-Cowan E-I Layer")
    wc = WilsonCowanLayer(128, ratio_ei=0.8)
    y = wc(x, dt=1.0, n_steps=3)
    print(f"   E units: {wc.dim_e}, I units: {wc.dim_i}")
    print(f"   Output shape: {y.shape}")

    # Example 7: Bio-Transformer Block
    print("\n7. Bio-Transformer Block")
    x_seq = torch.randn(8, 50, 256)  # [batch, seq_len, dim]
    bio_block = BioTransformerBlock(256, n_heads=8, n_timescales=3)
    y = bio_block(x_seq)
    print(f"   Input: {x_seq.shape}, Output: {y.shape}")
    print(f"   Learnable timescales: {count_learnable_timescales(bio_block)}")

    # Example 8: Kuramoto Oscillators
    print("\n8. Kuramoto Phase Coupling")
    kuramoto = KuramotoLayer(n_oscillators=64, coupling_strength=1.0)
    drive = torch.randn(8, 64) * 0.1
    y = kuramoto(drive, dt=0.1)
    print(f"   Input: {drive.shape}, Output (cos/sin): {y.shape}")

    print("\n" + "=" * 80)
    print("All components initialized successfully!")
    print(f"Total components: 8 demonstrated")
