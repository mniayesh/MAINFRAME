"""
Metabolic Neural Networks: Applying Biological Optimization Principles to AI

This module implements neural network components inspired by metabolic efficiency
and resource allocation strategies found in biological systems.

Based on analysis of 90,313 bioformulas from the bioformulas database.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Tuple, Optional
import numpy as np


# =============================================================================
# 1. MICHAELIS-MENTEN ACTIVATION FUNCTIONS
# =============================================================================

class MichaelisMentenActivation(nn.Module):
    """
    Activation function based on Michaelis-Menten enzyme kinetics.

    Formula: v = (V_max * [S]) / (K_m + [S])

    At low [S]: Linear response (first-order kinetics)
    At high [S]: Saturates at V_max (zero-order kinetics)

    Benefits:
    - Smooth saturation (like enzyme kinetics)
    - Prevents explosive activations
    - Learnable saturation point (K_m)
    """

    def __init__(self, v_max=1.0, k_m=1.0, learnable=True):
        super().__init__()
        if learnable:
            self.v_max = nn.Parameter(torch.tensor(v_max))
            self.k_m = nn.Parameter(torch.tensor(k_m))
        else:
            self.register_buffer('v_max', torch.tensor(v_max))
            self.register_buffer('k_m', torch.tensor(k_m))

    def forward(self, x):
        # Ensure positive input (substrate concentration)
        x_abs = torch.abs(x)
        # Michaelis-Menten kinetics
        return torch.sign(x) * (self.v_max * x_abs) / (self.k_m + x_abs)


class SubstrateInhibitionActivation(nn.Module):
    """
    Activation with substrate inhibition (excess input reduces output).

    Formula: v = (V_max * [S]) / (K_m + [S] + [S]^2 / K_si)

    Models biological phenomenon where too much substrate inhibits enzyme.
    Useful for preventing overconfident predictions.
    """

    def __init__(self, v_max=1.0, k_m=1.0, k_si=10.0):
        super().__init__()
        self.v_max = nn.Parameter(torch.tensor(v_max))
        self.k_m = nn.Parameter(torch.tensor(k_m))
        self.k_si = nn.Parameter(torch.tensor(k_si))

    def forward(self, x):
        x_abs = torch.abs(x)
        denominator = self.k_m + x_abs + (x_abs ** 2) / self.k_si
        return torch.sign(x) * (self.v_max * x_abs) / denominator


class HillActivation(nn.Module):
    """
    Hill equation activation (cooperative binding).

    Formula: v = (V_max * [S]^n) / (K_0.5^n + [S]^n)

    n > 1: Positive cooperativity (sharp threshold)
    n = 1: Michaelis-Menten
    n < 1: Negative cooperativity

    Useful for creating sharp decision boundaries.
    """

    def __init__(self, v_max=1.0, k_half=1.0, n=2.0):
        super().__init__()
        self.v_max = nn.Parameter(torch.tensor(v_max))
        self.k_half = nn.Parameter(torch.tensor(k_half))
        self.n = nn.Parameter(torch.tensor(n))

    def forward(self, x):
        x_abs = torch.abs(x)
        x_n = x_abs ** self.n
        k_n = self.k_half ** self.n
        return torch.sign(x) * (self.v_max * x_n) / (k_n + x_n)


# =============================================================================
# 2. METABOLIC COMPUTE BUDGET
# =============================================================================

class MetabolicComputeBudget:
    """
    Manages compute budget like ATP in metabolic pathways.

    - Start with fixed budget (ATP pool)
    - Layers consume budget (ATP consumption)
    - Regenerate budget based on confidence (ATP production)
    """

    def __init__(self, initial_budget: float = 1.0):
        self.initial_budget = initial_budget
        self.reset()

    def reset(self):
        """Reset budget to initial value."""
        self.available = self.initial_budget
        self.consumed = 0.0
        self.regenerated = 0.0

    def consume(self, amount: float) -> bool:
        """
        Consume budget (ATP consumption).
        Returns True if consumption successful, False if insufficient budget.
        """
        if self.available >= amount:
            self.available -= amount
            self.consumed += amount
            return True
        return False

    def regenerate(self, confidence: float, max_regen: float = 0.2):
        """
        Regenerate budget based on confidence (ATP production).

        High confidence → model is efficient → regenerate budget
        Low confidence → model struggling → no regeneration
        """
        if confidence > 0.7:
            regen_amount = max_regen * (confidence - 0.7) / 0.3
            self.available = min(self.initial_budget, self.available + regen_amount)
            self.regenerated += regen_amount

    def get_efficiency(self) -> float:
        """Calculate efficiency (like ATP yield)."""
        if self.consumed == 0:
            return 1.0
        return self.regenerated / self.consumed


# =============================================================================
# 3. ALLOSTERIC REGULATION LAYER
# =============================================================================

class AllostericLayer(nn.Module):
    """
    Layer with allosteric regulation (like PFK1 in glycolysis).

    Integrates multiple signals:
    - Main substrate (input)
    - Inhibitor (e.g., high loss → slow down)
    - Activator (e.g., high uncertainty → speed up)
    """

    def __init__(self, d_model: int, dropout: float = 0.1):
        super().__init__()
        self.main_transform = nn.Linear(d_model, d_model)
        self.inhibitor_gate = nn.Linear(d_model, d_model)
        self.activator_gate = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)
        self.norm = nn.LayerNorm(d_model)

    def forward(self, x: torch.Tensor,
                inhibition_signal: Optional[float] = None,
                activation_signal: Optional[float] = None) -> torch.Tensor:
        """
        Forward pass with allosteric regulation.

        Args:
            x: Input tensor
            inhibition_signal: 0-1, strength of inhibition (like ATP)
            activation_signal: 0-1, strength of activation (like AMP)
        """
        # Main transformation
        y = self.main_transform(x)

        # Allosteric inhibition (product inhibition)
        if inhibition_signal is not None and inhibition_signal > 0:
            inhibition = torch.sigmoid(self.inhibitor_gate(x))
            y = y * (1 - inhibition_signal * inhibition)

        # Allosteric activation (substrate activation)
        if activation_signal is not None and activation_signal > 0:
            activation = torch.sigmoid(self.activator_gate(x))
            y = y * (1 + activation_signal * activation)

        y = self.dropout(y)
        return self.norm(x + y)


# =============================================================================
# 4. ENZYME-INSPIRED ROUTING (MIXTURE OF EXPERTS)
# =============================================================================

class EnzymeRouter(nn.Module):
    """
    Routes inputs to specialized 'enzyme' networks based on substrate affinity.

    Like different enzyme isoforms with different Km values for substrates.
    """

    def __init__(self, d_model: int, num_experts: int = 8, k: int = 2):
        super().__init__()
        self.num_experts = num_experts
        self.k = k  # Top-k routing

        # Router (determines substrate-enzyme affinity)
        self.router = nn.Linear(d_model, num_experts)

        # Experts (enzyme isoforms)
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(d_model, d_model * 4),
                nn.GELU(),
                nn.Linear(d_model * 4, d_model)
            ) for _ in range(num_experts)
        ])

        # Km values for each expert (learnable affinity)
        self.km_values = nn.Parameter(torch.ones(num_experts))

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, Dict]:
        """
        Route input to top-k experts based on affinity.

        Returns:
            output: Processed tensor
            aux_info: Routing statistics
        """
        batch_size, seq_len, d_model = x.shape

        # Compute routing affinities (substrate-enzyme binding)
        router_logits = self.router(x)  # (batch, seq, num_experts)
        routing_weights = F.softmax(router_logits, dim=-1)

        # Select top-k experts (competitive binding)
        top_k_weights, top_k_indices = routing_weights.topk(self.k, dim=-1)

        # Normalize top-k weights
        top_k_weights = top_k_weights / top_k_weights.sum(dim=-1, keepdim=True)

        # Route to experts with Michaelis-Menten kinetics
        output = torch.zeros_like(x)
        expert_usage = torch.zeros(self.num_experts)

        for i in range(self.k):
            expert_idx = top_k_indices[..., i]
            weight = top_k_weights[..., i].unsqueeze(-1)

            for expert_id in range(self.num_experts):
                mask = (expert_idx == expert_id)
                if mask.any():
                    # Apply Michaelis-Menten kinetics
                    km = self.km_values[expert_id]
                    activity = weight / (km + weight)

                    # Process with expert
                    expert_input = x[mask]
                    expert_output = self.experts[expert_id](expert_input)
                    output[mask] += (activity * expert_output)[mask]

                    expert_usage[expert_id] += mask.float().sum()

        aux_info = {
            'routing_weights': routing_weights,
            'expert_usage': expert_usage,
            'load_balance': expert_usage.std() / (expert_usage.mean() + 1e-8)
        }

        return output, aux_info


# =============================================================================
# 5. ADAPTIVE PRECISION LAYER
# =============================================================================

class AdaptivePrecisionLayer(nn.Module):
    """
    Adjusts computational precision based on activation magnitude.

    Like substrate inhibition: excessive activation → lower precision.
    Mimics biological systems that adjust enzyme expression based on demand.
    """

    def __init__(self, d_model: int):
        super().__init__()
        self.high_precision = nn.Linear(d_model, d_model)
        self.medium_precision = nn.Linear(d_model, d_model)
        self.low_precision = nn.Linear(d_model, d_model)

        # Thresholds for precision switching
        self.register_buffer('low_threshold', torch.tensor(0.1))
        self.register_buffer('high_threshold', torch.tensor(1.0))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Dynamically select precision based on activation magnitude.
        """
        activation_mag = torch.abs(x).mean(dim=-1, keepdim=True)

        # Compute all precisions (in practice, would use different dtypes)
        out_high = self.high_precision(x)  # FP32
        out_medium = self.medium_precision(x)  # FP16
        out_low = self.low_precision(x)  # INT8

        # Soft routing based on magnitude
        weight_high = torch.sigmoid(10 * (self.low_threshold - activation_mag))
        weight_low = torch.sigmoid(10 * (activation_mag - self.high_threshold))
        weight_medium = 1 - weight_high - weight_low

        output = (weight_high * out_high +
                 weight_medium * out_medium +
                 weight_low * out_low)

        return output


# =============================================================================
# 6. METABOLIC CASCADE NETWORK
# =============================================================================

class MetabolicCascadeNetwork(nn.Module):
    """
    Complete network organized like a metabolic pathway.

    Structure:
    1. Glycolysis pathway (fast, initial processing)
    2. TCA cycle (iterative refinement)
    3. Oxidative phosphorylation (final high-efficiency extraction)
    """

    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int,
                 num_tca_cycles: int = 8):
        super().__init__()

        # Glycolysis (fast initial processing, 2 ATP net)
        self.glycolysis = nn.Sequential(
            nn.Linear(input_dim, hidden_dim * 2),
            MichaelisMentenActivation(),
            nn.Linear(hidden_dim * 2, hidden_dim),
            AllostericLayer(hidden_dim),  # PFK1-like regulation
            nn.Linear(hidden_dim, hidden_dim // 2),
        )

        # TCA Cycle (iterative refinement, cyclic processing)
        self.tca_cycles = nn.ModuleList([
            nn.Sequential(
                nn.Linear(hidden_dim // 2, hidden_dim // 2),
                nn.GELU(),
                nn.Linear(hidden_dim // 2, hidden_dim // 2),
            ) for _ in range(num_tca_cycles)
        ])
        self.tca_norm = nn.LayerNorm(hidden_dim // 2)

        # Oxidative Phosphorylation (high-yield final processing, ~30 ATP)
        self.oxidative_phos = nn.Sequential(
            nn.Linear(hidden_dim // 2, hidden_dim // 4),
            nn.GELU(),
            nn.Linear(hidden_dim // 4, output_dim),
        )

        # Fast glycolytic pathway (low yield, emergency mode)
        self.fast_pathway = nn.Linear(hidden_dim // 2, output_dim)

    def forward(self, x: torch.Tensor,
                energy_demand: str = 'high',
                compute_budget: Optional[MetabolicComputeBudget] = None) -> torch.Tensor:
        """
        Forward pass with adaptive pathway selection.

        Args:
            x: Input tensor
            energy_demand: 'low', 'medium', or 'high'
            compute_budget: Optional compute budget manager

        Returns:
            Output predictions
        """
        # Stage 1: Glycolysis (always runs, fast)
        x = self.glycolysis(x)

        if compute_budget is not None:
            compute_budget.consume(0.2)

        # Stage 2: TCA Cycle (optional, medium energy)
        if energy_demand in ['medium', 'high']:
            for cycle in self.tca_cycles:
                residual = x
                x = cycle(x)
                x = self.tca_norm(x + residual)  # Residual connection

            if compute_budget is not None:
                compute_budget.consume(0.5)

        # Stage 3: Oxidative Phosphorylation or Fast Pathway
        if energy_demand == 'high':
            x = self.oxidative_phos(x)
            if compute_budget is not None:
                compute_budget.consume(0.3)
        else:
            # Emergency glycolytic pathway (fast but inefficient)
            x = self.fast_pathway(x)
            if compute_budget is not None:
                compute_budget.consume(0.05)

        return x


# =============================================================================
# 7. DYNAMIC INFERENCE CONTROLLER
# =============================================================================

class MetabolicInferenceController:
    """
    Controls inference strategy based on resource availability.

    Like cell switching between aerobic and anaerobic metabolism.
    """

    def __init__(self, model: nn.Module):
        self.model = model
        self.budget = MetabolicComputeBudget(initial_budget=1.0)

    def infer(self, x: torch.Tensor, time_budget: float = None) -> Dict:
        """
        Perform inference with adaptive resource allocation.

        Args:
            x: Input tensor
            time_budget: Available compute time (seconds)

        Returns:
            Dictionary with predictions and statistics
        """
        self.budget.reset()

        # Determine energy demand based on time budget
        if time_budget is None or time_budget > 1.0:
            energy_demand = 'high'  # Aerobic (OXPHOS)
        elif time_budget > 0.1:
            energy_demand = 'medium'  # TCA cycle
        else:
            energy_demand = 'low'  # Anaerobic (glycolysis only)

        # Forward pass
        output = self.model(x, energy_demand=energy_demand,
                          compute_budget=self.budget)

        # Calculate confidence
        probs = F.softmax(output, dim=-1)
        confidence = probs.max(dim=-1).values.mean().item()

        # Regenerate budget based on confidence
        self.budget.regenerate(confidence)

        return {
            'output': output,
            'predictions': output.argmax(dim=-1),
            'confidence': confidence,
            'energy_demand': energy_demand,
            'efficiency': self.budget.get_efficiency(),
            'budget_remaining': self.budget.available,
        }


# =============================================================================
# 8. EXAMPLE USAGE
# =============================================================================

def example_usage():
    """Demonstrate metabolic neural network components."""

    print("="*80)
    print("METABOLIC NEURAL NETWORKS - EXAMPLE USAGE")
    print("="*80)

    # 1. Michaelis-Menten Activation
    print("\n1. Michaelis-Menten Activation Function")
    mm_activation = MichaelisMentenActivation(v_max=1.0, k_m=1.0)
    x = torch.linspace(-5, 5, 100)
    y = mm_activation(x)
    print(f"Input range: [{x.min():.2f}, {x.max():.2f}]")
    print(f"Output range: [{y.min():.2f}, {y.max():.2f}]")
    print(f"Saturates at V_max = {mm_activation.v_max.item():.2f}")

    # 2. Metabolic Compute Budget
    print("\n2. Metabolic Compute Budget")
    budget = MetabolicComputeBudget(initial_budget=1.0)
    print(f"Initial budget: {budget.available:.3f}")
    budget.consume(0.3)
    print(f"After consuming 0.3: {budget.available:.3f}")
    budget.regenerate(confidence=0.85)
    print(f"After regeneration (conf=0.85): {budget.available:.3f}")
    print(f"Efficiency: {budget.get_efficiency():.3f}")

    # 3. Enzyme Router
    print("\n3. Enzyme Router (Mixture of Experts)")
    d_model = 64
    batch_size = 4
    seq_len = 10
    router = EnzymeRouter(d_model=d_model, num_experts=8, k=2)
    x = torch.randn(batch_size, seq_len, d_model)
    output, aux_info = router(x)
    print(f"Input shape: {x.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Expert usage: {aux_info['expert_usage']}")
    print(f"Load balance (lower is better): {aux_info['load_balance']:.3f}")

    # 4. Complete Metabolic Network
    print("\n4. Metabolic Cascade Network")
    network = MetabolicCascadeNetwork(
        input_dim=784,
        hidden_dim=256,
        output_dim=10,
        num_tca_cycles=8
    )

    controller = MetabolicInferenceController(network)

    # Test different energy demands
    x = torch.randn(4, 784)

    for demand, budget in [('high', 2.0), ('medium', 0.5), ('low', 0.05)]:
        result = controller.infer(x, time_budget=budget)
        print(f"\nEnergy demand: {demand}")
        print(f"  Confidence: {result['confidence']:.3f}")
        print(f"  Efficiency: {result['efficiency']:.3f}")
        print(f"  Budget remaining: {result['budget_remaining']:.3f}")

    print("\n" + "="*80)
    print("Analysis complete. See metabolic_efficiency_analysis.md for details.")
    print("="*80)


if __name__ == '__main__':
    example_usage()
