"""
QUANTUM.SCHRODINGER_TIMEDEPENDENT: Time-Dependent Schrödinger Equation

Fundamental equation: i*ℏ*dψ/dt = H*ψ

This module propagates a quantum wavefunction forward in time under
a Hamiltonian operator. Core quantum dynamics for all molecular processes.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class SchrodingerTimedependent(nn.Module):
    """
    Time-dependent Schrödinger equation propagator.

    Propagates quantum wavefunction ψ(r,t) forward in time:
    i*ℏ*dψ/dt = H*ψ

    Args:
        grid_size: Spatial discretization (number of grid points)
        hbar: Reduced Planck constant (default: 1.054e-34 J·s)
        dtype: Data type for computations (default: complex64)
    """

    def __init__(self, grid_size=100, hbar=1.054e-34, dtype=torch.complex64):
        super().__init__()
        self.grid_size = grid_size
        self.hbar = hbar
        self.dtype = dtype

        # Hamiltonian operator as learnable parameter
        # Can represent kinetic + potential energy
        H_real = torch.randn(grid_size, grid_size, dtype=torch.float32) * 0.1
        H_imag = torch.randn(grid_size, grid_size, dtype=torch.float32) * 0.1

        # Make Hermitian: H = H†
        H_real = (H_real + H_real.T) / 2

        H_complex = torch.complex(H_real, H_imag)
        H_complex = (H_complex + H_complex.mH) / 2  # Hermitian

        self.register_buffer('H', H_complex)

    def forward(self, psi, t, dt=0.001, steps=1):
        """
        Propagate wavefunction forward in time.

        Args:
            psi: Input wavefunction (batch_size, grid_size) - complex tensor
            t: Current time (scalar or tensor)
            dt: Time step for integration (default: 0.001)
            steps: Number of time steps to take (default: 1)

        Returns:
            psi_new: Propagated wavefunction (batch_size, grid_size)
            energies: Expected energies <ψ|H|ψ> (batch_size,)
        """

        # Ensure complex dtype
        if psi.dtype != torch.complex64:
            psi = psi.to(torch.complex64)

        psi_current = psi

        # Time evolution: ψ(t+dt) ≈ ψ(t) + (dt) * dψ/dt
        # where dψ/dt = -i*H*ψ / ℏ
        for _ in range(steps):
            # Compute Hamiltonian action
            H_psi = torch.matmul(self.H, psi_current.T).T  # (batch, grid)

            # Time derivative: dψ/dt = -i*H*ψ / ℏ
            dpsi_dt = -1j * H_psi / self.hbar

            # Simple Euler step
            psi_current = psi_current + dt * dpsi_dt

            # Renormalize to preserve probability (optional)
            norm = torch.norm(psi_current, dim=1, keepdim=True)
            psi_current = psi_current / (norm + 1e-8)

        # Compute expected energy: <ψ|H|ψ>
        H_psi = torch.matmul(self.H, psi_current.T).T
        energies = torch.sum(
            torch.conj(psi_current) * H_psi,
            dim=1
        ).real

        return psi_current, energies

    def kinetic_energy(self, psi):
        """Estimate kinetic energy from wavefunction."""
        # Kinetic energy ~ ∫ |∇ψ|² dr
        dpsi = torch.diff(psi, dim=1)
        kinetic = torch.sum(torch.abs(dpsi) ** 2, dim=1)
        return kinetic

    def potential_energy(self, psi, V=None):
        """
        Compute potential energy <ψ|V|ψ>.

        Args:
            psi: Wavefunction
            V: Potential energy matrix (grid_size, grid_size)

        Returns:
            Potential energies (batch_size,)
        """
        if V is None:
            # Default: harmonic oscillator potential
            x = torch.linspace(-5, 5, self.grid_size, device=psi.device)
            V = 0.5 * x**2  # V(x) = 0.5 * x²
            V = torch.diag(V)

        V_psi = torch.matmul(V, psi.T).T
        potential = torch.sum(
            torch.conj(psi) * V_psi,
            dim=1
        ).real

        return potential


class TimeEvolutionOperator(nn.Module):
    """
    Explicit time evolution operator: U(t) = exp(-i*H*t/ℏ)

    For small time steps, implements:
    ψ(t+dt) = U(dt)*ψ(t) = exp(-i*H*dt/ℏ)*ψ(t)
    """

    def __init__(self, hamiltonian, hbar=1.054e-34):
        """
        Args:
            hamiltonian: Hermitian matrix (grid_size, grid_size)
            hbar: Reduced Planck constant
        """
        super().__init__()
        self.hbar = hbar
        self.register_buffer('H', hamiltonian)

    def forward(self, psi, dt):
        """
        Apply time evolution operator: U(dt) = exp(-i*H*dt/ℏ)

        Uses matrix exponential (expensive but accurate).
        For large systems, use simple Euler or RK4 instead.
        """
        # Eigendecomposition for accurate exponentiation
        # H = Q * Λ * Q†
        eigenvalues, eigenvectors = torch.linalg.eigh(self.H)

        # U(dt) = Q * exp(-i*Λ*dt/ℏ) * Q†
        exp_eigenvalues = torch.exp(-1j * eigenvalues * dt / self.hbar)
        exp_H = torch.matmul(
            eigenvectors,
            torch.matmul(
                torch.diag(exp_eigenvalues),
                eigenvectors.mH
            )
        )

        # Apply to wavefunction: ψ' = U(dt) * ψ
        psi_new = torch.matmul(exp_H, psi.T).T

        return psi_new


class RK4TimeEvolution(nn.Module):
    """
    4th-order Runge-Kutta time evolution.

    More accurate than simple Euler stepping.
    """

    def __init__(self, hamiltonian, hbar=1.054e-34):
        super().__init__()
        self.hbar = hbar
        self.register_buffer('H', hamiltonian)

    def forward(self, psi, dt):
        """
        RK4 step for: dψ/dt = -i*H*ψ / ℏ
        """
        def f(psi_t):
            H_psi = torch.matmul(self.H, psi_t.T).T
            return -1j * H_psi / self.hbar

        k1 = f(psi)
        k2 = f(psi + dt * k1 / 2)
        k3 = f(psi + dt * k2 / 2)
        k4 = f(psi + dt * k3)

        psi_new = psi + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)

        return psi_new


if __name__ == "__main__":
    # Example usage
    batch_size = 4
    grid_size = 50

    # Initialize module
    model = SchrodingerTimedependent(grid_size=grid_size)

    # Random initial wavefunction
    psi0 = torch.randn(batch_size, grid_size, dtype=torch.complex64)
    psi0 = psi0 / torch.norm(psi0, dim=1, keepdim=True)  # Normalize

    # Propagate for 5 time steps
    psi_evolved, energies = model(psi0, t=0, dt=0.001, steps=5)

    print(f"Initial shape: {psi0.shape}")
    print(f"Evolved shape: {psi_evolved.shape}")
    print(f"Energies shape: {energies.shape}")
    print(f"Energy range: [{energies.min():.4f}, {energies.max():.4f}]")
