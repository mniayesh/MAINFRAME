"""
QUANTUM.KOHN_SHAM_DFT: Kohn-Sham Density Functional Theory

One of the most widely used methods in quantum chemistry.
Maps many-electron problem to single-electron problem with effective potential.

[-ℏ²/2m ∇² + V_eff[ρ]] φ_i = ε_i φ_i
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class KohnShamDFT(nn.Module):
    """
    Kohn-Sham Density Functional Theory solver.

    Solves self-consistent field equations:
    [-ℏ²/2m ∇² + V_eff[ρ]] φ_i = ε_i φ_i

    Args:
        grid_size: Number of spatial grid points
        num_electrons: Number of electrons to compute
        hbar: Reduced Planck constant
        m: Electron mass
    """

    def __init__(self, grid_size=100, num_electrons=10, hbar=1.054e-34, m=9.109e-31):
        super().__init__()
        self.grid_size = grid_size
        self.num_electrons = num_electrons
        self.hbar = hbar
        self.m = m

        # Initial kinetic energy operator (Laplacian)
        self.register_buffer(
            'kinetic_energy_matrix',
            self._construct_kinetic_matrix(grid_size)
        )

        # Exchange-correlation approximation weight
        self.xc_weight = nn.Parameter(torch.tensor(0.7))

        # Self-consistency iteration counter
        self.num_iterations = 30
        self.convergence_threshold = 1e-5

    def _construct_kinetic_matrix(self, grid_size):
        """Construct kinetic energy operator (discrete Laplacian)."""
        # Second derivative in 1D: [1, -2, 1] / dx²
        # For simplicity, use finite differences
        dx = 1.0 / (grid_size - 1)
        T = torch.zeros(grid_size, grid_size)

        for i in range(grid_size):
            T[i, i] = -2.0 / (dx ** 2)
            if i > 0:
                T[i, i - 1] = 1.0 / (dx ** 2)
            if i < grid_size - 1:
                T[i, i + 1] = 1.0 / (dx ** 2)

        T = T * (self.hbar ** 2) / (2 * self.m)
        return T

    def electron_density(self, orbitals):
        """
        Compute electron density from occupied orbitals.

        ρ(r) = Σ_i |φ_i(r)|²

        Args:
            orbitals: (batch, num_electrons, grid_size)

        Returns:
            density: (batch, grid_size)
        """
        # Sum over occupied orbitals
        density = torch.sum(torch.abs(orbitals) ** 2, dim=1)
        return density

    def hartree_potential(self, density):
        """
        Compute Hartree (Coulomb) potential from electron density.

        V_H(r) = ∫ ρ(r') / |r - r'| dr'

        For 1D, approximate as convolution.
        """
        # Coulomb kernel in 1D: K(r) = 1/|r|
        # Approximate as Gaussian for numerical stability
        grid_size = density.shape[-1]
        x = torch.linspace(-5, 5, grid_size, device=density.device)
        xx, xx_prime = torch.meshgrid(x, x, indexing='ij')
        r = torch.abs(xx - xx_prime) + 0.1  # Avoid singularity

        # Coulomb kernel
        K = 1.0 / r

        # V_H(r) = ∫ K(r,r') ρ(r') dr'
        V_H = torch.matmul(K, density.unsqueeze(-1)).squeeze(-1)

        # Normalize by grid spacing
        dx = x[1] - x[0]
        V_H = V_H * dx

        return V_H

    def exchange_correlation_potential(self, density):
        """
        Exchange-correlation potential (LDA approximation).

        V_xc(r) ≈ -C_x * ρ(r)^(1/3)

        where C_x is the LDA exchange constant.
        """
        C_x = 0.7386  # LDA exchange constant

        # Avoid singularities
        rho_safe = torch.clamp(density, min=1e-8)

        V_xc = -C_x * (rho_safe ** (1.0 / 3.0))

        return V_xc

    def effective_potential(self, density, external_potential=None):
        """
        Construct effective potential: V_eff = V_ext + V_H + V_xc

        Args:
            density: Electron density (batch, grid_size)
            external_potential: Optional external potential (batch, grid_size)

        Returns:
            V_eff: Effective potential (batch, grid_size)
        """
        # Hartree potential from density
        V_H = self.hartree_potential(density)

        # Exchange-correlation potential
        V_xc = self.exchange_correlation_potential(density)

        # External potential (default: harmonic)
        if external_potential is None:
            grid_size = density.shape[-1]
            x = torch.linspace(-5, 5, grid_size, device=density.device)
            external_potential = 0.5 * (x ** 2)  # Harmonic potential
            external_potential = external_potential.unsqueeze(0).expand(density.shape[0], -1)

        # Total effective potential
        V_eff = external_potential + V_H + self.xc_weight * V_xc

        return V_eff

    def solve_kohn_sham(self, external_potential=None):
        """
        Self-consistent field iteration to solve Kohn-Sham equations.

        Returns:
            orbitals: Lowest num_electrons orbitals (batch=1, num_electrons, grid_size)
            density: Final electron density (1, grid_size)
            energies: Orbital energies (num_electrons,)
        """
        batch_size = 1
        grid_size = self.grid_size

        # Initialize density from hydrogen-like initial guess
        x = torch.linspace(-5, 5, grid_size, device=self.kinetic_energy_matrix.device)
        rho_init = torch.exp(-x ** 2).unsqueeze(0)
        rho_init = rho_init / torch.sum(rho_init) * self.num_electrons

        density = rho_init

        # SCF iterations
        for iteration in range(self.num_iterations):
            # Construct Fock matrix: F = T + V_eff
            V_eff = self.effective_potential(density, external_potential)

            # Create potential diagonal matrix
            V_eff_matrix = torch.diag(V_eff[0])

            # Fock matrix: F = T + V
            F = self.kinetic_energy_matrix + V_eff_matrix

            # Solve eigenvalue problem: F * φ = ε * φ
            eigenvalues, eigenvectors = torch.linalg.eigh(F)

            # Take lowest num_electrons eigenstates
            orbitals = eigenvectors[:, :self.num_electrons].T  # (num_electrons, grid_size)

            # Compute new density
            density_new = self.electron_density(orbitals.unsqueeze(0))

            # Check convergence
            density_diff = torch.norm(density_new - density)
            if density_diff < self.convergence_threshold:
                break

            # Mix old and new density (damping for stability)
            alpha = 0.5
            density = alpha * density_new + (1 - alpha) * density

        # Return results
        return orbitals.unsqueeze(0), density, eigenvalues[:self.num_electrons]

    def forward(self, external_potential=None):
        """
        Solve Kohn-Sham DFT equations.

        Args:
            external_potential: Optional external potential

        Returns:
            results: dict with orbitals, density, energies, kinetic_energy, hartree_energy, xc_energy, total_energy
        """
        orbitals, density, orbital_energies = self.solve_kohn_sham(external_potential)

        # Compute energy components
        kinetic = self._compute_kinetic_energy(orbitals)
        hartree = self._compute_hartree_energy(density)
        xc = self._compute_xc_energy(density)
        extern = self._compute_external_energy(density, external_potential)

        total_energy = kinetic + hartree + xc + extern

        results = {
            'orbitals': orbitals,
            'density': density,
            'orbital_energies': orbital_energies,
            'kinetic_energy': kinetic,
            'hartree_energy': hartree,
            'xc_energy': xc,
            'external_energy': extern,
            'total_energy': total_energy,
        }

        return results

    def _compute_kinetic_energy(self, orbitals):
        """Compute kinetic energy: T = Σ_i <φ_i|T|φ_i>"""
        T_phi = torch.matmul(self.kinetic_energy_matrix, orbitals[0].T).T
        kinetic = torch.sum(
            torch.conj(orbitals[0]) * T_phi,
            dim=1
        ).real.sum()
        return kinetic

    def _compute_hartree_energy(self, density):
        """Hartree energy: E_H = 0.5 * ∫∫ ρ(r)ρ(r') / |r-r'| dr dr'"""
        V_H = self.hartree_potential(density)
        hartree = 0.5 * torch.sum(density * V_H)
        return hartree

    def _compute_xc_energy(self, density):
        """Exchange-correlation energy (LDA)."""
        # LDA energy: E_xc ≈ C_xc * ∫ ρ(r)^(4/3) dr
        C_xc = -0.916  # LDA XC constant
        rho_safe = torch.clamp(density, min=1e-8)
        xc = C_xc * torch.sum(rho_safe ** (4.0 / 3.0))
        return xc

    def _compute_external_energy(self, density, external_potential=None):
        """External potential energy: E_ext = ∫ V_ext(r) ρ(r) dr"""
        if external_potential is None:
            return torch.tensor(0.0, device=density.device)
        return torch.sum(density * external_potential)


class SimpleDFTLayer(nn.Module):
    """
    Simplified DFT layer for use in larger networks.

    Performs one SCF iteration given current density.
    """

    def __init__(self, grid_size=100):
        super().__init__()
        self.grid_size = grid_size
        self.kinetic = self._construct_kinetic_matrix(grid_size)
        self.xc_strength = nn.Parameter(torch.tensor(1.0))

    def _construct_kinetic_matrix(self, grid_size):
        dx = 1.0 / (grid_size - 1)
        T = torch.zeros(grid_size, grid_size)
        for i in range(grid_size):
            T[i, i] = -2.0 / (dx ** 2)
            if i > 0:
                T[i, i - 1] = 1.0 / (dx ** 2)
            if i < grid_size - 1:
                T[i, i + 1] = 1.0 / (dx ** 2)
        return T

    def forward(self, density):
        """
        Single DFT step: given density, return improved density.

        Args:
            density: (batch, grid_size)

        Returns:
            density_new: (batch, grid_size)
        """
        # Hartree potential (simplified)
        V_H = torch.zeros_like(density)
        for i in range(self.grid_size):
            V_H[:, i] = torch.sum(density, dim=1) / (abs(i - torch.arange(self.grid_size)) + 1)

        # XC potential (LDA)
        V_xc = -self.xc_strength * (torch.clamp(density, min=1e-8) ** (1.0 / 3.0))

        # Effective potential
        V_eff = V_H + V_xc

        # Solve single-particle equation (eigenvalue problem)
        F = torch.diag_embed(torch.diagonal(V_eff, dim1=1, dim2=2)) + self.kinetic.unsqueeze(0)

        # Eigendecomposition
        eigenvalues, eigenvectors = torch.linalg.eigh(F)

        # Reconstruct density from lowest eigenstates
        # (simplified: just use first eigenvector)
        density_new = (torch.abs(eigenvectors[:, :, 0]) ** 2).real

        return density_new


if __name__ == "__main__":
    # Example: Solve for simple potential well
    dft = KohnShamDFT(grid_size=100, num_electrons=5)
    results = dft()

    print("DFT Results:")
    print(f"  Total Energy: {results['total_energy']:.6f}")
    print(f"  Kinetic Energy: {results['kinetic_energy']:.6f}")
    print(f"  Hartree Energy: {results['hartree_energy']:.6f}")
    print(f"  XC Energy: {results['xc_energy']:.6f}")
    print(f"  Orbital Energies: {results['orbital_energies'][:3]}")
    print(f"  Density shape: {results['density'].shape}")
