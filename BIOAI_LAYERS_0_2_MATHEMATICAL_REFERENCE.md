# BioAI Layers 0-2: Mathematical Reference
## Physical Substrate through Morphogenesis

**Document Version:** 1.0
**Date:** December 10, 2025
**Status:** Comprehensive Mathematical Reference

---

## Table of Contents

1. [LAYER 0: Physical Substrate](#layer-0-physical-substrate)
   - Energy Gradients and Potential Fields
   - Stochastic Differential Equations
   - Langevin Equations
   - Brownian Motion Models
   - Potential Energy Landscapes

2. [LAYER 1: Physical Description / Capability Graph](#layer-1-physical-description--capability-graph)
   - Graph Representation Models
   - Capability Encoding
   - Topology Metrics
   - Graph Neural Networks

3. [LAYER 2: Dynamic Field / Morphogenesis](#layer-2-dynamic-field--morphogenesis)
   - Reaction-Diffusion Equations
   - Turing Patterns
   - Morphogen Gradients
   - Local Interaction Rules
   - Cellular Automata

---

# LAYER 0: Physical Substrate

**Biological Basis:** At the most fundamental level, biological computation emerges from the stochastic dynamics of molecules in thermal environments. Proteins fold, molecules diffuse, and reactions occur driven by thermal fluctuations and energy gradients.

**Computing Principle:** Computation at the physical layer is probabilistic, continuous, and governed by the laws of statistical mechanics. Unlike digital bits, biological states exist in energy landscapes with probabilistic transitions.

---

## 1. Langevin Equation (Stochastic Dynamics)

### Mathematical Formulation

The Langevin equation describes the motion of a particle in a fluid subject to random thermal forces:

```
Langevin Equation (overdamped):
dx/dt = -(1/γ) ∇U(x) + √(2D) η(t)

where:
  x(t)      = position/state vector at time t
  γ         = friction coefficient (damping)
  U(x)      = potential energy function
  ∇U(x)     = gradient of potential (deterministic force)
  D         = diffusion coefficient = kB·T/γ
  kB        = Boltzmann constant (1.38 × 10⁻²³ J/K)
  T         = absolute temperature (K)
  η(t)      = white noise: ⟨η(t)⟩ = 0, ⟨η(t)η(t')⟩ = δ(t-t')
```

**Physical Interpretation:**
- First term: Deterministic drift toward energy minima
- Second term: Random thermal fluctuations (Brownian motion)
- Balance determines exploration vs. exploitation in state space

### General Form (with inertia)

```
Langevin Equation (underdamped):
m(d²x/dt²) = -γ(dx/dt) - ∇U(x) + √(2γkB·T) η(t)

where:
  m = particle mass
```

### Fokker-Planck Equation (Probability Distribution Evolution)

The probability density ρ(x,t) evolves according to:

```
∂ρ/∂t = (1/γ) ∇·[∇U(x)ρ] + D∇²ρ

Stationary distribution (t → ∞):
ρ_eq(x) ∝ exp(-U(x)/(kB·T))    [Boltzmann distribution]
```

### Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

class LangevinDynamics:
    """
    Simulate Langevin dynamics in a potential energy landscape.

    References:
        Risken, H. (1996). The Fokker-Planck Equation. Springer.
        Gardiner, C. (2009). Stochastic Methods. Springer.
    """

    def __init__(self, potential_fn, gradient_fn, gamma=1.0, temperature=300.0):
        """
        Args:
            potential_fn: U(x) - potential energy function
            gradient_fn: ∇U(x) - gradient of potential
            gamma: friction coefficient
            temperature: temperature in Kelvin
        """
        self.U = potential_fn
        self.grad_U = gradient_fn
        self.gamma = gamma
        self.kB = 1.38e-23  # Boltzmann constant (J/K)
        self.T = temperature
        self.D = (self.kB * self.T) / gamma  # Diffusion coefficient

    def step(self, x, dt):
        """
        Euler-Maruyama integration step.

        Args:
            x: current state
            dt: timestep

        Returns:
            x_new: state at t + dt
        """
        # Deterministic drift
        drift = -(1.0 / self.gamma) * self.grad_U(x)

        # Stochastic diffusion
        noise = np.sqrt(2 * self.D * dt) * np.random.randn(*x.shape)

        # Euler-Maruyama update
        x_new = x + drift * dt + noise

        return x_new

    def simulate(self, x0, T_total, dt=0.001):
        """
        Run full simulation.

        Args:
            x0: initial state
            T_total: total simulation time
            dt: timestep

        Returns:
            trajectory: array of states over time
            times: time points
        """
        n_steps = int(T_total / dt)
        trajectory = np.zeros((n_steps, *x0.shape))
        trajectory[0] = x0

        for i in range(1, n_steps):
            trajectory[i] = self.step(trajectory[i-1], dt)

        times = np.arange(n_steps) * dt
        return trajectory, times


# Example: Double-well potential (bistable system)
def double_well_potential(x):
    """U(x) = (x² - 1)²"""
    return (x**2 - 1)**2

def double_well_gradient(x):
    """∇U(x) = 4x(x² - 1)"""
    return 4 * x * (x**2 - 1)

# Simulation
langevin = LangevinDynamics(
    potential_fn=double_well_potential,
    gradient_fn=double_well_gradient,
    gamma=1.0,
    temperature=300.0
)

x0 = np.array([0.5])  # Start near unstable equilibrium
trajectory, times = langevin.simulate(x0, T_total=10.0, dt=0.001)

# Visualization
plt.figure(figsize=(12, 4))
plt.subplot(121)
plt.plot(times, trajectory)
plt.xlabel('Time')
plt.ylabel('State x(t)')
plt.title('Langevin Dynamics in Double-Well Potential')

plt.subplot(122)
x_range = np.linspace(-2, 2, 200)
plt.plot(x_range, double_well_potential(x_range))
plt.xlabel('State x')
plt.ylabel('Potential U(x)')
plt.title('Energy Landscape')
plt.tight_layout()
```

### Key References

1. **Risken, H.** (1996). *The Fokker-Planck Equation: Methods of Solution and Applications*. Springer.
   - DOI: 10.1007/978-3-642-61544-3
   - Classic reference on stochastic differential equations

2. **Gardiner, C.W.** (2009). *Stochastic Methods: A Handbook for the Natural and Social Sciences*. Springer.
   - Comprehensive treatment of Langevin dynamics

3. **Zwanzig, R.** (2001). *Nonequilibrium Statistical Mechanics*. Oxford University Press.
   - Applications to biological systems

---

## 2. Brownian Motion and Diffusion

### Mathematical Formulation

Standard Brownian motion (Wiener process):

```
Brownian Motion:
dW(t) = √dt · N(0,1)

Properties:
  1. W(0) = 0
  2. W(t) is continuous but nowhere differentiable
  3. Increments are independent: W(t₂)-W(t₁) ⊥ W(t₄)-W(t₃) for t₁<t₂≤t₃<t₄
  4. Increments are Gaussian: W(t) - W(s) ~ N(0, |t-s|)

Einstein Relation:
⟨x²(t)⟩ = 2Dt    (mean-squared displacement)

where:
  D = diffusion coefficient
  For spherical particle: D = kB·T/(6πηr)
    η = fluid viscosity
    r = particle radius
```

### Diffusion Equation (Fick's Laws)

```
Fick's First Law (flux):
J = -D ∇c

Fick's Second Law (concentration evolution):
∂c/∂t = D ∇²c

where:
  c(x,t) = concentration at position x, time t
  J      = diffusion flux
  D      = diffusion coefficient
```

### Solution in 1D (free diffusion)

```
c(x,t) = (N/√(4πDt)) exp(-x²/(4Dt))

where:
  N = total number of particles (conserved)

Spreading:
σ(t) = √(2Dt)    (standard deviation grows as √t)
```

### Python Implementation

```python
import numpy as np
from scipy.ndimage import convolve

class DiffusionSystem:
    """
    Simulate diffusion using finite difference methods.

    References:
        Berg, H.C. (1993). Random Walks in Biology. Princeton.
        Einstein, A. (1905). On the movement of small particles...
    """

    def __init__(self, grid_size, dx, D=1.0):
        """
        Args:
            grid_size: number of grid points (1D, 2D, or 3D)
            dx: spatial step size
            D: diffusion coefficient
        """
        self.grid_size = grid_size
        self.dx = dx
        self.D = D

        # Initialize concentration field
        if isinstance(grid_size, int):
            self.c = np.zeros(grid_size)
            self.dim = 1
        elif isinstance(grid_size, tuple):
            self.c = np.zeros(grid_size)
            self.dim = len(grid_size)

    def set_initial_condition(self, c0):
        """Set initial concentration distribution."""
        self.c = c0.copy()

    def step_explicit(self, dt):
        """
        Explicit Euler step (Forward Time Centered Space).

        Stability requirement: dt ≤ dx²/(2D·dim)
        """
        if self.dim == 1:
            # 1D diffusion: c_new[i] = c[i] + D·dt/dx² · (c[i+1] - 2c[i] + c[i-1])
            laplacian = (np.roll(self.c, 1) - 2*self.c + np.roll(self.c, -1)) / self.dx**2
        elif self.dim == 2:
            # 2D diffusion using convolution
            kernel = np.array([[0, 1, 0],
                             [1, -4, 1],
                             [0, 1, 0]]) / self.dx**2
            laplacian = convolve(self.c, kernel, mode='wrap')
        elif self.dim == 3:
            # 3D diffusion kernel
            kernel = np.array([
                [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
                [[0, 1, 0], [1, -6, 1], [0, 1, 0]],
                [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
            ]) / self.dx**2
            laplacian = convolve(self.c, kernel, mode='wrap')

        self.c += self.D * dt * laplacian

    def simulate(self, T_total, dt):
        """
        Simulate diffusion over time.

        Args:
            T_total: total simulation time
            dt: timestep

        Returns:
            history: concentration field at each timestep
        """
        n_steps = int(T_total / dt)
        history = [self.c.copy()]

        for _ in range(n_steps):
            self.step_explicit(dt)
            history.append(self.c.copy())

        return np.array(history)


# Example: 2D diffusion from point source
grid_size = (100, 100)
dx = 0.1
D = 1.0

system = DiffusionSystem(grid_size, dx, D)

# Point source at center
c0 = np.zeros(grid_size)
c0[50, 50] = 1000.0
system.set_initial_condition(c0)

# Simulate
dt = 0.001  # Must satisfy stability: dt < dx²/(2D·dim) = 0.005
history = system.simulate(T_total=1.0, dt=dt)

# Visualize
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for i, t_idx in enumerate([0, len(history)//2, -1]):
    axes[i].imshow(history[t_idx], cmap='hot')
    axes[i].set_title(f't = {t_idx * dt:.3f}')
    axes[i].axis('off')
plt.suptitle('2D Diffusion from Point Source')
```

### Key References

1. **Einstein, A.** (1905). "On the movement of small particles suspended in stationary liquids required by the molecular-kinetic theory of heat." *Annalen der Physik*.
   - Original paper deriving Brownian motion

2. **Berg, H.C.** (1993). *Random Walks in Biology*. Princeton University Press.
   - Excellent introduction to diffusion in biological contexts

3. **Crank, J.** (1975). *The Mathematics of Diffusion*. Oxford University Press.
   - Comprehensive treatment of diffusion equations

---

## 3. Energy Landscapes and Potential Fields

### Mathematical Formulation

For a system with state vector **x**, the potential energy landscape U(**x**) determines dynamics:

```
Energy Landscape:
U(x) = potential energy at state x

Critical points:
  Minima:  ∇U(x*) = 0, Hessian H positive definite
  Maxima:  ∇U(x*) = 0, Hessian H negative definite
  Saddles: ∇U(x*) = 0, Hessian H indefinite

Barrier crossing (Kramers rate):
k = (ω₀ωb)/(2πγ) exp(-ΔU/(kB·T))

where:
  ω₀  = frequency at minimum
  ωb  = frequency at barrier top
  ΔU  = barrier height
  γ   = friction
  kB·T = thermal energy
```

### Protein Folding Energy Landscape (Funnel Theory)

```
Funnel Energy Landscape:
U(Q, E) = E_0 + α·Q² - β·Q·E + γ·E²

where:
  Q = fraction of native contacts (0 to 1)
  E = conformational energy
  α, β, γ = landscape parameters

Native state: Q → 1, E → E_min
Unfolded state: Q → 0, E → high
```

### Hopfield Network Energy Function

```
Hopfield Energy (associative memory):
E = -(1/2) Σᵢⱼ wᵢⱼ sᵢ sⱼ - Σᵢ θᵢ sᵢ

where:
  sᵢ ∈ {-1, +1} = neuron states
  wᵢⱼ = connection weights (symmetric: wᵢⱼ = wⱼᵢ)
  θᵢ = thresholds

Energy always decreases or stays constant:
ΔE ≤ 0  for any state update

Stable states = energy minima = stored memories
```

### Python Implementation

```python
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import eigh

class EnergyLandscape:
    """
    Analyze and visualize energy landscapes.

    References:
        Onuchic et al. (1997). Theory of protein folding: the energy
        landscape perspective. Annu. Rev. Phys. Chem.
    """

    def __init__(self, potential_fn, gradient_fn=None, hessian_fn=None):
        """
        Args:
            potential_fn: U(x) - energy function
            gradient_fn: ∇U(x) - gradient (optional, will use numerical if None)
            hessian_fn: H(x) - Hessian matrix (optional)
        """
        self.U = potential_fn
        self.grad_U = gradient_fn
        self.hess_U = hessian_fn

    def find_minima(self, x0_list, method='BFGS'):
        """
        Find local minima starting from multiple initial points.

        Args:
            x0_list: list of initial guesses
            method: optimization method

        Returns:
            minima: list of local minima
            energies: energies at minima
        """
        minima = []
        energies = []

        for x0 in x0_list:
            result = minimize(
                self.U,
                x0,
                method=method,
                jac=self.grad_U
            )
            if result.success:
                # Check if this is a new minimum (not already found)
                is_new = True
                for m in minima:
                    if np.linalg.norm(result.x - m) < 1e-6:
                        is_new = False
                        break

                if is_new:
                    minima.append(result.x)
                    energies.append(result.fun)

        return minima, energies

    def classify_critical_point(self, x):
        """
        Classify critical point using Hessian eigenvalues.

        Returns:
            'minimum', 'maximum', 'saddle', or 'not_critical'
        """
        grad = self.grad_U(x) if self.grad_U else self._numerical_gradient(x)

        if np.linalg.norm(grad) > 1e-4:
            return 'not_critical'

        hess = self.hess_U(x) if self.hess_U else self._numerical_hessian(x)
        eigenvalues = eigh(hess, eigvals_only=True)

        if np.all(eigenvalues > 0):
            return 'minimum'
        elif np.all(eigenvalues < 0):
            return 'maximum'
        else:
            return 'saddle'

    def compute_barrier(self, x_min1, x_min2, n_points=100):
        """
        Estimate energy barrier between two minima.

        Args:
            x_min1, x_min2: two local minima
            n_points: number of points along path

        Returns:
            barrier_height: ΔU = U_max - max(U_min1, U_min2)
        """
        # Linear interpolation path
        path = np.linspace(x_min1, x_min2, n_points)
        energies = np.array([self.U(x) for x in path])

        U_max = np.max(energies)
        U_base = max(self.U(x_min1), self.U(x_min2))
        barrier = U_max - U_base

        return barrier, path, energies

    def _numerical_gradient(self, x, eps=1e-6):
        """Numerical gradient via finite differences."""
        grad = np.zeros_like(x)
        for i in range(len(x)):
            x_plus = x.copy()
            x_plus[i] += eps
            x_minus = x.copy()
            x_minus[i] -= eps
            grad[i] = (self.U(x_plus) - self.U(x_minus)) / (2 * eps)
        return grad

    def _numerical_hessian(self, x, eps=1e-5):
        """Numerical Hessian via finite differences."""
        n = len(x)
        hess = np.zeros((n, n))

        for i in range(n):
            for j in range(n):
                x_pp = x.copy(); x_pp[i] += eps; x_pp[j] += eps
                x_pm = x.copy(); x_pm[i] += eps; x_pm[j] -= eps
                x_mp = x.copy(); x_mp[i] -= eps; x_mp[j] += eps
                x_mm = x.copy(); x_mm[i] -= eps; x_mm[j] -= eps

                hess[i,j] = (self.U(x_pp) - self.U(x_pm) -
                           self.U(x_mp) + self.U(x_mm)) / (4 * eps**2)

        return hess


# Example: Muller-Brown potential (has 3 minima, 2 saddles)
def muller_brown_potential(x):
    """
    Classic test potential for energy landscape analysis.

    Reference:
        Muller, K. & Brown, L.D. (1979). Theor. Chim. Acta 53, 75-93.
    """
    A = np.array([-200, -100, -170, 15])
    a = np.array([-1, -1, -6.5, 0.7])
    b = np.array([0, 0, 11, 0.6])
    c = np.array([-10, -10, -6.5, 0.7])
    x0 = np.array([1, 0, -0.5, -1])
    y0 = np.array([0, 0.5, 1.5, 1])

    x_coord, y_coord = x[0], x[1]

    V = 0
    for i in range(4):
        V += A[i] * np.exp(
            a[i] * (x_coord - x0[i])**2 +
            b[i] * (x_coord - x0[i]) * (y_coord - y0[i]) +
            c[i] * (y_coord - y0[i])**2
        )

    return V

landscape = EnergyLandscape(muller_brown_potential)

# Find minima from random starting points
x0_list = [np.random.randn(2) for _ in range(50)]
minima, energies = landscape.find_minima(x0_list)

print(f"Found {len(minima)} local minima:")
for i, (m, E) in enumerate(zip(minima, energies)):
    print(f"  Minimum {i+1}: x = {m}, E = {E:.2f}")
```

### Key References

1. **Onuchic, J.N., Luthey-Schulten, Z. & Wolynes, P.G.** (1997). "Theory of protein folding: the energy landscape perspective." *Annu. Rev. Phys. Chem.* 48, 545-600.
   - DOI: 10.1146/annurev.physchem.48.1.545

2. **Frauenfelder, H., Sligar, S.G. & Wolynes, P.G.** (1991). "The energy landscapes and motions of proteins." *Science* 254, 1598-1603.
   - Foundational paper on energy landscapes in biology

3. **Wales, D.J.** (2003). *Energy Landscapes*. Cambridge University Press.
   - Comprehensive treatment of energy landscape theory

---

## 4. Thermal Noise and Fluctuations

### Fluctuation-Dissipation Theorem

```
Fluctuation-Dissipation Theorem:
⟨x(0)·x(t)⟩ = (kB·T/γ) exp(-γt/m)

Relates:
  - Fluctuations: ⟨x²⟩ (mean-squared displacement)
  - Dissipation: γ (friction coefficient)

Power spectral density:
S(ω) = (4kB·T·γ)/(m²ω² + γ²)    (thermal noise spectrum)
```

### Johnson-Nyquist Noise (Electrical Analog)

```
Thermal voltage noise in resistor:
⟨V²⟩ = 4kB·T·R·Δf

where:
  R  = resistance
  Δf = frequency bandwidth

Applies to ion channels (membrane resistance)
```

### Python Implementation

```python
class ThermalNoise:
    """
    Generate thermal noise for stochastic simulations.

    References:
        Kubo, R. (1966). The fluctuation-dissipation theorem.
        Rep. Prog. Phys. 29, 255.
    """

    def __init__(self, temperature=300.0, friction=1.0, mass=1.0):
        self.kB = 1.38e-23  # J/K
        self.T = temperature
        self.gamma = friction
        self.m = mass

    def generate_white_noise(self, n_samples, dt):
        """
        Generate white noise samples.

        Returns:
            noise: array of Gaussian random numbers with correct variance
        """
        # Variance from fluctuation-dissipation theorem
        variance = 2 * self.kB * self.T * self.gamma * dt / self.m
        return np.random.normal(0, np.sqrt(variance), n_samples)

    def generate_colored_noise(self, n_samples, dt, tau_correlation):
        """
        Generate colored (Ornstein-Uhlenbeck) noise.

        Args:
            tau_correlation: correlation time

        Returns:
            noise: temporally correlated noise
        """
        noise = np.zeros(n_samples)
        noise[0] = np.random.normal(0, np.sqrt(self.kB * self.T / self.gamma))

        for i in range(1, n_samples):
            decay = np.exp(-dt / tau_correlation)
            noise[i] = decay * noise[i-1] + \
                      np.sqrt(1 - decay**2) * \
                      np.random.normal(0, np.sqrt(self.kB * self.T / self.gamma))

        return noise

    def power_spectrum(self, frequencies):
        """
        Thermal noise power spectrum.

        Returns:
            S(ω): power spectral density
        """
        omega = 2 * np.pi * frequencies
        S = (4 * self.kB * self.T * self.gamma) / \
            (self.m**2 * omega**2 + self.gamma**2)
        return S
```

### Key References

1. **Kubo, R.** (1966). "The fluctuation-dissipation theorem." *Rep. Prog. Phys.* 29, 255.
   - Classic exposition of FDT

2. **Nyquist, H.** (1928). "Thermal agitation of electric charge in conductors." *Phys. Rev.* 32, 110-113.
   - Original derivation of thermal noise

---

# LAYER 1: Physical Description / Capability Graph

**Biological Basis:** Biological systems can be represented as graphs where nodes are molecular components (proteins, genes) and edges are interactions (binding, regulation). The topology of these graphs encodes the system's capabilities.

**Computing Principle:** Represent the physical substrate as a directed graph where nodes have states and edges have transformation rules. The graph structure determines what computations are possible.

---

## 1. Graph Representation Models

### Mathematical Formulation

```
Capability Graph G = (V, E, S, T)

Components:
  V = {v₁, v₂, ..., vₙ}        Vertices (computational units)
  E ⊆ V × V                     Edges (connections)
  S: V → ℝᵈ                     State function (assigns state to each vertex)
  T: V × E → ℝᵈ                 Transformation function

Adjacency Matrix:
A[i,j] = { 1  if (vᵢ, vⱼ) ∈ E
         { 0  otherwise

Weighted Adjacency:
W[i,j] = weight of edge (vᵢ, vⱼ)

State Update:
s(t+1) = f(A·s(t), T)

where f is a nonlinear activation function
```

### Graph Laplacian

```
Graph Laplacian:
L = D - A

where:
  D = diagonal degree matrix: D[i,i] = Σⱼ A[i,j]
  A = adjacency matrix

Properties:
  - L is positive semi-definite
  - Smallest eigenvalue λ₁ = 0
  - Number of zero eigenvalues = number of connected components
  - Second eigenvalue λ₂ (Fiedler value) measures connectivity

Normalized Laplacian:
ℒ = I - D⁻¹/² A D⁻¹/²

Eigenvalues: 0 ≤ λᵢ ≤ 2
```

### Signaling on Graphs (Diffusion)

```
Heat Equation on Graph:
∂s/∂t = -L·s

Solution:
s(t) = exp(-Lt)·s(0)

Steady state (t → ∞):
s(∞) = (D⁻¹·1)·(1ᵀ·s(0))    (uniform distribution)
```

### Python Implementation

```python
import numpy as np
import networkx as nx
from scipy.linalg import expm
from scipy.sparse.linalg import eigsh

class CapabilityGraph:
    """
    Represent biological system as capability graph.

    References:
        Barabási, A.L. & Oltvai, Z.N. (2004). Network biology:
        understanding the cell's functional organization. Nat. Rev. Genet.
    """

    def __init__(self, n_nodes):
        """
        Args:
            n_nodes: number of computational units
        """
        self.n = n_nodes
        self.adjacency = np.zeros((n_nodes, n_nodes))
        self.states = np.zeros(n_nodes)
        self.capabilities = {}  # Node -> list of operations

    def add_edge(self, i, j, weight=1.0):
        """Add directed edge from node i to j."""
        self.adjacency[i, j] = weight

    def add_capability(self, node_id, operation):
        """Assign computational capability to node."""
        if node_id not in self.capabilities:
            self.capabilities[node_id] = []
        self.capabilities[node_id].append(operation)

    def compute_laplacian(self, normalized=False):
        """
        Compute graph Laplacian.

        Args:
            normalized: if True, return normalized Laplacian

        Returns:
            L: Laplacian matrix
        """
        A = self.adjacency
        D = np.diag(np.sum(A, axis=1))
        L = D - A

        if normalized:
            D_inv_sqrt = np.diag(1.0 / np.sqrt(np.diag(D) + 1e-10))
            L = np.eye(self.n) - D_inv_sqrt @ A @ D_inv_sqrt

        return L

    def spectral_analysis(self, k=10):
        """
        Compute spectral properties of graph.

        Args:
            k: number of eigenvalues/eigenvectors to compute

        Returns:
            eigenvalues, eigenvectors of Laplacian
        """
        L = self.compute_laplacian(normalized=True)
        eigenvalues, eigenvectors = eigsh(L, k=min(k, self.n-1), which='SM')
        return eigenvalues, eigenvectors

    def diffusion_propagate(self, initial_state, t, dt=0.01):
        """
        Propagate state via diffusion on graph.

        Args:
            initial_state: initial node states
            t: simulation time
            dt: timestep

        Returns:
            final_state: states after time t
        """
        L = self.compute_laplacian()

        # Matrix exponential method (exact)
        self.states = expm(-L * t) @ initial_state

        return self.states

    def message_passing(self, node_states, n_iterations=10):
        """
        Graph neural network style message passing.

        Args:
            node_states: initial node feature vectors
            n_iterations: number of message passing rounds

        Returns:
            updated_states: node states after message passing
        """
        states = node_states.copy()

        for _ in range(n_iterations):
            messages = np.zeros_like(states)

            # Aggregate messages from neighbors
            for i in range(self.n):
                for j in range(self.n):
                    if self.adjacency[j, i] > 0:  # Edge from j to i
                        # Simple aggregation (can be replaced with learned function)
                        messages[i] += self.adjacency[j, i] * states[j]

            # Update states
            states = self.activation(states + messages)

        return states

    def activation(self, x):
        """Nonlinear activation function."""
        return np.tanh(x)

    def compute_topology_metrics(self):
        """
        Compute graph topology metrics.

        Returns:
            metrics: dict of topology measures
        """
        # Convert to NetworkX for advanced metrics
        G = nx.from_numpy_array(self.adjacency, create_using=nx.DiGraph)

        metrics = {
            'clustering_coefficient': nx.average_clustering(G.to_undirected()),
            'average_path_length': nx.average_shortest_path_length(G) if nx.is_connected(G.to_undirected()) else float('inf'),
            'degree_distribution': dict(G.degree()),
            'in_degree': dict(G.in_degree()),
            'out_degree': dict(G.out_degree()),
            'betweenness_centrality': nx.betweenness_centrality(G),
            'eigenvector_centrality': nx.eigenvector_centrality(G, max_iter=1000),
            'pagerank': nx.pagerank(G),
        }

        return metrics


# Example: Protein interaction network
n_proteins = 50
graph = CapabilityGraph(n_proteins)

# Create scale-free network (Barabási-Albert model)
for i in range(n_proteins):
    # New node connects to existing nodes preferentially
    if i > 0:
        degrees = np.sum(graph.adjacency[:i, :i], axis=1) + 1
        probs = degrees / np.sum(degrees)
        n_connections = min(3, i)
        targets = np.random.choice(i, size=n_connections, replace=False, p=probs)
        for j in targets:
            graph.add_edge(i, j, weight=1.0)
            graph.add_edge(j, i, weight=1.0)  # Undirected

# Add capabilities
capabilities_list = ['kinase', 'phosphatase', 'transcription_factor', 'receptor']
for i in range(n_proteins):
    cap = np.random.choice(capabilities_list)
    graph.add_capability(i, cap)

# Analyze topology
metrics = graph.compute_topology_metrics()
print(f"Clustering coefficient: {metrics['clustering_coefficient']:.3f}")
print(f"Average path length: {metrics['average_path_length']:.3f}")

# Spectral analysis
eigenvalues, eigenvectors = graph.spectral_analysis(k=10)
print(f"Fiedler value (λ₂): {eigenvalues[1]:.3f}")
```

### Key References

1. **Barabási, A.L. & Oltvai, Z.N.** (2004). "Network biology: understanding the cell's functional organization." *Nature Reviews Genetics* 5, 101-113.
   - DOI: 10.1038/nrg1272

2. **Chung, F.R.K.** (1997). *Spectral Graph Theory*. American Mathematical Society.
   - Comprehensive treatment of graph Laplacians

3. **Newman, M.E.J.** (2010). *Networks: An Introduction*. Oxford University Press.
   - Modern treatment of network science

---

## 2. Graph Neural Networks (GNNs)

### Mathematical Formulation

```
Graph Convolutional Network (GCN):

Layer update:
H^(l+1) = σ(D̃^(-1/2) Ã D̃^(-1/2) H^(l) W^(l))

where:
  H^(l)     = node features at layer l (n × d^(l) matrix)
  Ã         = A + I (adjacency with self-loops)
  D̃         = degree matrix of Ã
  W^(l)     = learnable weight matrix (d^(l) × d^(l+1))
  σ         = activation function (ReLU, tanh, etc.)

Message Passing Neural Network (MPNN):

m_v^(t) = Σ_{u∈N(v)} M_t(h_v^(t-1), h_u^(t-1), e_{uv})    (message)
h_v^(t) = U_t(h_v^(t-1), m_v^(t))                         (update)

where:
  m_v^(t)   = aggregated message to node v at step t
  h_v^(t)   = hidden state of node v at step t
  M_t       = message function
  U_t       = update function
  e_{uv}    = edge features
  N(v)      = neighbors of v
```

### Python Implementation (PyTorch)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class GraphConvLayer(nn.Module):
    """
    Graph convolutional layer (Kipf & Welling, 2017).

    References:
        Kipf, T.N. & Welling, M. (2017). Semi-supervised classification
        with graph convolutional networks. ICLR.
    """

    def __init__(self, in_features, out_features):
        super().__init__()
        self.weight = nn.Parameter(torch.FloatTensor(in_features, out_features))
        self.bias = nn.Parameter(torch.FloatTensor(out_features))
        self.reset_parameters()

    def reset_parameters(self):
        nn.init.xavier_uniform_(self.weight)
        nn.init.zeros_(self.bias)

    def forward(self, x, adj):
        """
        Args:
            x: node features (n_nodes × in_features)
            adj: adjacency matrix (n_nodes × n_nodes)

        Returns:
            out: updated node features (n_nodes × out_features)
        """
        # Add self-loops
        adj_hat = adj + torch.eye(adj.size(0), device=adj.device)

        # Compute degree matrix
        deg = torch.sum(adj_hat, dim=1)
        deg_inv_sqrt = torch.pow(deg, -0.5)
        deg_inv_sqrt[torch.isinf(deg_inv_sqrt)] = 0.0

        # Normalized adjacency: D^(-1/2) A D^(-1/2)
        norm_adj = deg_inv_sqrt.view(-1, 1) * adj_hat * deg_inv_sqrt.view(1, -1)

        # Propagate: X' = norm_adj @ X @ W
        support = torch.mm(x, self.weight)
        output = torch.mm(norm_adj, support) + self.bias

        return output


class GCN(nn.Module):
    """
    Graph Convolutional Network for node classification.
    """

    def __init__(self, n_features, n_hidden, n_classes, dropout=0.5):
        super().__init__()
        self.gc1 = GraphConvLayer(n_features, n_hidden)
        self.gc2 = GraphConvLayer(n_hidden, n_classes)
        self.dropout = dropout

    def forward(self, x, adj):
        x = F.relu(self.gc1(x, adj))
        x = F.dropout(x, self.dropout, training=self.training)
        x = self.gc2(x, adj)
        return F.log_softmax(x, dim=1)


# Example usage
n_nodes = 100
n_features = 32
n_hidden = 64
n_classes = 5

# Random graph
adj = torch.rand(n_nodes, n_nodes)
adj = (adj > 0.9).float()  # Sparse graph
adj = (adj + adj.T) / 2  # Make symmetric

# Random features
features = torch.randn(n_nodes, n_features)

# Initialize model
model = GCN(n_features, n_hidden, n_classes)

# Forward pass
output = model(features, adj)
print(f"Output shape: {output.shape}")  # (n_nodes, n_classes)
```

### Key References

1. **Kipf, T.N. & Welling, M.** (2017). "Semi-Supervised Classification with Graph Convolutional Networks." *ICLR*.
   - Influential GCN paper

2. **Gilmer, J. et al.** (2017). "Neural Message Passing for Quantum Chemistry." *ICML*.
   - MPNN framework

3. **Hamilton, W.L., Ying, R. & Leskovec, J.** (2017). "Inductive Representation Learning on Large Graphs." *NIPS*.
   - GraphSAGE method

---

# LAYER 2: Dynamic Field / Morphogenesis

**Biological Basis:** During development, simple chemical gradients (morphogens) create complex spatial patterns through reaction-diffusion processes. These same mechanisms can generate computational structures.

**Computing Principle:** Local interaction rules + diffusion → global spatial patterns. Self-organizing computation emerges from simple local dynamics.

---

## 1. Reaction-Diffusion Equations

### Mathematical Formulation

```
General Reaction-Diffusion System:

∂u/∂t = D_u ∇²u + f(u, v)
∂v/∂t = D_v ∇²v + g(u, v)

where:
  u, v      = concentrations of two species
  D_u, D_v  = diffusion coefficients
  ∇²        = Laplacian operator
  f, g      = reaction kinetics (nonlinear)

Components:
  1. Diffusion: D∇²u spreads concentration
  2. Reaction: f(u,v) creates/destroys locally
```

### Gray-Scott Model

```
Gray-Scott Reaction-Diffusion:

∂u/∂t = D_u ∇²u - uv² + F(1-u)
∂v/∂t = D_v ∇²v + uv² - (F+k)v

where:
  u = substrate concentration
  v = catalyst concentration
  D_u, D_v = diffusion rates (typically D_u > D_v)
  F = feed rate
  k = kill rate

Chemical interpretation:
  U + 2V → 3V    (autocatalytic reaction)
  V → P          (decay)
  ∅ → U          (feed)

Parameter regimes produce different patterns:
  - Spots
  - Stripes
  - Spirals
  - Chaos
```

### Python Implementation

```python
import numpy as np
from scipy.ndimage import convolve

class GrayScottSystem:
    """
    Simulate Gray-Scott reaction-diffusion system.

    References:
        Pearson, J.E. (1993). Complex patterns in a simple system.
        Science 261, 189-192.
    """

    def __init__(self, size, dx=1.0, Du=0.16, Dv=0.08, F=0.060, k=0.062):
        """
        Args:
            size: grid size (N×N)
            dx: spatial step
            Du: diffusion coefficient for u
            Dv: diffusion coefficient for v
            F: feed rate
            k: kill rate
        """
        self.size = size
        self.dx = dx
        self.Du = Du
        self.Dv = Dv
        self.F = F
        self.k = k

        # Initialize fields
        self.u = np.ones((size, size))
        self.v = np.zeros((size, size))

        # Laplacian kernel for discrete diffusion
        self.laplacian_kernel = np.array([[0.05, 0.2, 0.05],
                                         [0.2,  -1.0, 0.2],
                                         [0.05, 0.2, 0.05]])

    def set_initial_condition(self, perturbation='central'):
        """
        Set initial condition.

        Args:
            perturbation: 'central', 'random', or 'stripe'
        """
        self.u = np.ones((self.size, self.size))
        self.v = np.zeros((self.size, self.size))

        if perturbation == 'central':
            # Central square of v
            center = self.size // 2
            r = self.size // 10
            self.v[center-r:center+r, center-r:center+r] = 1.0
        elif perturbation == 'random':
            # Random noise
            self.v = np.random.rand(self.size, self.size) * 0.1
        elif perturbation == 'stripe':
            # Vertical stripe
            self.v[:, self.size//2-5:self.size//2+5] = 1.0

    def step(self, dt):
        """
        Euler step for reaction-diffusion.

        Args:
            dt: timestep
        """
        # Compute Laplacians (discrete diffusion)
        laplacian_u = convolve(self.u, self.laplacian_kernel, mode='wrap')
        laplacian_v = convolve(self.v, self.laplacian_kernel, mode='wrap')

        # Reaction terms
        uvv = self.u * self.v * self.v

        # Update equations
        du_dt = self.Du * laplacian_u - uvv + self.F * (1 - self.u)
        dv_dt = self.Dv * laplacian_v + uvv - (self.F + self.k) * self.v

        self.u += du_dt * dt
        self.v += dv_dt * dt

        # Clamp to valid range
        self.u = np.clip(self.u, 0, 1)
        self.v = np.clip(self.v, 0, 1)

    def simulate(self, n_steps, dt=1.0):
        """
        Run simulation.

        Args:
            n_steps: number of timesteps
            dt: timestep size

        Returns:
            history_v: v field at each timestep
        """
        history = [self.v.copy()]

        for _ in range(n_steps):
            self.step(dt)
            history.append(self.v.copy())

        return np.array(history)


# Example: Generate Turing patterns
system = GrayScottSystem(size=200, Du=0.16, Dv=0.08, F=0.035, k=0.065)
system.set_initial_condition('random')

history = system.simulate(n_steps=10000, dt=1.0)

# Visualize
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
timesteps = [0, 2000, 4000, 6000, 8000, 10000]

for ax, t in zip(axes.flat, timesteps):
    ax.imshow(history[t], cmap='viridis', vmin=0, vmax=0.5)
    ax.set_title(f't = {t}')
    ax.axis('off')

plt.suptitle('Gray-Scott Reaction-Diffusion: Spot Pattern Formation')
plt.tight_layout()
```

### Parameter Exploration

```python
# Famous parameter sets for different patterns

PATTERNS = {
    'spots': {'F': 0.035, 'k': 0.065},
    'stripes': {'F': 0.035, 'k': 0.060},
    'worms': {'F': 0.058, 'k': 0.065},
    'waves': {'F': 0.014, 'k': 0.054},
    'chaos': {'F': 0.026, 'k': 0.051},
    'mitosis': {'F': 0.0367, 'k': 0.0649}
}

# Generate all patterns
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

for ax, (name, params) in zip(axes.flat, PATTERNS.items()):
    system = GrayScottSystem(size=200, Du=0.16, Dv=0.08, **params)
    system.set_initial_condition('random')

    # Run to steady state
    for _ in range(10000):
        system.step(dt=1.0)

    ax.imshow(system.v, cmap='viridis')
    ax.set_title(f'{name}: F={params["F"]}, k={params["k"]}')
    ax.axis('off')

plt.tight_layout()
```

### Key References

1. **Turing, A.M.** (1952). "The chemical basis of morphogenesis." *Phil. Trans. R. Soc. Lond. B* 237, 37-72.
   - Original paper proposing reaction-diffusion patterns

2. **Pearson, J.E.** (1993). "Complex patterns in a simple system." *Science* 261, 189-192.
   - Gray-Scott model and pattern catalog

3. **Murray, J.D.** (2003). *Mathematical Biology II: Spatial Models and Biomedical Applications*. Springer.
   - Comprehensive textbook on reaction-diffusion

---

## 2. Gierer-Meinhardt Model (Activator-Inhibitor)

### Mathematical Formulation

```
Gierer-Meinhardt Equations:

∂a/∂t = c_a (a²/h - μ_a a + ρ_a) + D_a ∇²a
∂h/∂t = c_h (a² - μ_h h + ρ_h) + D_h ∇²h

where:
  a = activator concentration
  h = inhibitor concentration
  c_a, c_h = production rates
  μ_a, μ_h = degradation rates
  ρ_a, ρ_h = basal production
  D_a << D_h (short-range activation, long-range inhibition)

Key feature:
  - Activator activates itself: ∂a/∂t ∝ a²
  - Activator activates inhibitor: ∂h/∂t ∝ a²
  - Inhibitor inhibits activator: ∂a/∂t ∝ -a/h
  - Inhibitor diffuses faster: D_h >> D_a

Produces:
  - Periodic patterns (segments in embryos)
  - Spot patterns (animal coat markings)
  - Regeneration dynamics
```

### Python Implementation

```python
class GiererMeinhardtSystem:
    """
    Activator-inhibitor model for pattern formation.

    References:
        Gierer, A. & Meinhardt, H. (1972). A theory of biological
        pattern formation. Kybernetik 12, 30-39.
    """

    def __init__(self, size, dx=1.0, Da=0.01, Dh=1.0,
                 ca=0.01, ch=0.01, mu_a=0.01, mu_h=0.02,
                 rho_a=0.001, rho_h=0.0):
        self.size = size
        self.dx = dx
        self.Da = Da  # Activator diffusion (small)
        self.Dh = Dh  # Inhibitor diffusion (large)
        self.ca = ca
        self.ch = ch
        self.mu_a = mu_a
        self.mu_h = mu_h
        self.rho_a = rho_a
        self.rho_h = rho_h

        # Initialize
        self.a = np.ones((size, size)) * 0.1 + np.random.rand(size, size) * 0.01
        self.h = np.ones((size, size)) * 0.1 + np.random.rand(size, size) * 0.01

        # Laplacian kernel
        self.laplacian = np.array([[0, 1, 0],
                                   [1, -4, 1],
                                   [0, 1, 0]]) / (self.dx**2)

    def step(self, dt):
        """Integrate one timestep."""
        # Diffusion terms
        lap_a = convolve(self.a, self.laplacian, mode='wrap')
        lap_h = convolve(self.h, self.laplacian, mode='wrap')

        # Reaction terms
        da_dt = self.ca * (self.a**2 / (self.h + 1e-10) - self.mu_a * self.a + self.rho_a) + \
                self.Da * lap_a
        dh_dt = self.ch * (self.a**2 - self.mu_h * self.h + self.rho_h) + \
                self.Dh * lap_h

        # Update
        self.a += da_dt * dt
        self.h += dh_dt * dt

        # Prevent negative concentrations
        self.a = np.maximum(self.a, 0)
        self.h = np.maximum(self.h, 0.01)

    def simulate(self, n_steps, dt=0.1):
        """Run simulation."""
        history_a = [self.a.copy()]
        history_h = [self.h.copy()]

        for _ in range(n_steps):
            self.step(dt)
            history_a.append(self.a.copy())
            history_h.append(self.h.copy())

        return np.array(history_a), np.array(history_h)


# Example
system = GiererMeinhardtSystem(size=100)
history_a, history_h = system.simulate(n_steps=5000, dt=0.1)

# Visualize final state
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(history_a[-1], cmap='hot')
axes[0].set_title('Activator (a)')
axes[0].axis('off')

axes[1].imshow(history_h[-1], cmap='cool')
axes[1].set_title('Inhibitor (h)')
axes[1].axis('off')
plt.suptitle('Gierer-Meinhardt Pattern Formation')
```

### Key References

1. **Gierer, A. & Meinhardt, H.** (1972). "A theory of biological pattern formation." *Kybernetik* 12, 30-39.
   - Original activator-inhibitor model

2. **Meinhardt, H.** (1982). *Models of Biological Pattern Formation*. Academic Press.
   - Comprehensive book on morphogenesis models

---

## 3. Morphogen Gradients

### Mathematical Formulation

```
Morphogen Gradient (French Flag Model):

c(x) = c_source · exp(-x/λ)

where:
  c(x)     = morphogen concentration at position x
  c_source = concentration at source
  λ        = length constant = √(D/k)
  D        = diffusion coefficient
  k        = degradation rate

Steady-state from:
D(d²c/dx²) - kc = 0    with boundary c(0) = c_source

Cell fate specification:
  if c(x) > θ_1: cell type A
  elif c(x) > θ_2: cell type B
  else: cell type C
```

### Bicoid Gradient in Drosophila

```
Bicoid protein gradient:

∂c/∂t = D∇²c - kc + S(x)

where:
  S(x) = { S_0  if x = 0 (anterior)
         { 0    otherwise

Steady state:
c(x) = (S_0/k) exp(-x/λ)

λ ≈ 100 μm in Drosophila embryo

Threshold readout:
  hunchback expression: c(x) > c_threshold
```

### Python Implementation

```python
class MorphogenGradient:
    """
    Simulate morphogen gradient formation and readout.

    References:
        Wolpert, L. (1969). Positional information and the spatial
        pattern of cellular differentiation. J. Theor. Biol. 25, 1-47.
    """

    def __init__(self, length, dx=1.0, D=1.0, k=0.1, source_strength=1.0):
        """
        Args:
            length: spatial domain length
            dx: spatial discretization
            D: diffusion coefficient
            k: degradation rate
            source_strength: production at source
        """
        self.L = length
        self.dx = dx
        self.D = D
        self.k = k
        self.S0 = source_strength

        # Spatial grid
        self.n = int(length / dx)
        self.x = np.linspace(0, length, self.n)
        self.c = np.zeros(self.n)

        # Length constant
        self.lambda_ = np.sqrt(D / k)

    def analytical_steady_state(self):
        """
        Compute analytical steady-state gradient.

        Returns:
            c(x): concentration profile
        """
        return (self.S0 / self.k) * np.exp(-self.x / self.lambda_)

    def simulate_to_steady_state(self, dt=0.01, max_steps=10000, tol=1e-6):
        """
        Numerically integrate to steady state.

        Args:
            dt: timestep
            max_steps: maximum iterations
            tol: convergence tolerance

        Returns:
            c: final concentration profile
        """
        # Initialize
        self.c = np.zeros(self.n)

        for step in range(max_steps):
            c_old = self.c.copy()

            # Compute Laplacian (second derivative)
            laplacian = np.zeros(self.n)
            laplacian[1:-1] = (self.c[2:] - 2*self.c[1:-1] + self.c[:-2]) / self.dx**2

            # Boundary conditions
            laplacian[0] = 0  # No flux at x=0 (source maintained)
            laplacian[-1] = 0  # No flux at x=L

            # Source term (only at x=0)
            source = np.zeros(self.n)
            source[0] = self.S0

            # Update
            dc_dt = self.D * laplacian - self.k * self.c + source
            self.c += dc_dt * dt

            # Enforce non-negativity
            self.c = np.maximum(self.c, 0)

            # Check convergence
            if np.max(np.abs(self.c - c_old)) < tol:
                print(f"Converged at step {step}")
                break

        return self.c

    def cell_fate_determination(self, thresholds):
        """
        Determine cell fates based on concentration thresholds.

        Args:
            thresholds: list of threshold concentrations [θ₁, θ₂, ...]

        Returns:
            fates: array of cell fate indices
        """
        fates = np.zeros(self.n, dtype=int)

        thresholds = sorted(thresholds, reverse=True)

        for i, x in enumerate(self.x):
            for fate_id, threshold in enumerate(thresholds):
                if self.c[i] > threshold:
                    fates[i] = fate_id
                    break
            else:
                fates[i] = len(thresholds)  # Lowest fate

        return fates


# Example: Bicoid-like gradient
gradient = MorphogenGradient(length=500, dx=1.0, D=10.0, k=0.1, source_strength=100)

# Analytical solution
c_analytical = gradient.analytical_steady_state()

# Numerical solution
c_numerical = gradient.simulate_to_steady_state()

# Cell fate determination
thresholds = [20, 10, 5]  # Three thresholds → 4 cell types
fates = gradient.cell_fate_determination(thresholds)

# Visualize
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

axes[0].plot(gradient.x, c_analytical, 'k-', label='Analytical', linewidth=2)
axes[0].plot(gradient.x, c_numerical, 'r--', label='Numerical', linewidth=2)
axes[0].set_xlabel('Position (μm)')
axes[0].set_ylabel('Morphogen concentration')
axes[0].set_title('Morphogen Gradient Formation')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Add threshold lines
for i, t in enumerate(thresholds):
    axes[0].axhline(t, color='gray', linestyle=':', alpha=0.5)
    axes[0].text(gradient.L * 0.9, t, f'θ{i+1}', va='bottom')

axes[1].plot(gradient.x, fates, 'o-', markersize=2)
axes[1].set_xlabel('Position (μm)')
axes[1].set_ylabel('Cell fate')
axes[1].set_title('Cell Fate Specification (French Flag Model)')
axes[1].set_yticks(range(len(thresholds) + 1))
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
```

### Key References

1. **Wolpert, L.** (1969). "Positional information and the spatial pattern of cellular differentiation." *J. Theor. Biol.* 25, 1-47.
   - Original positional information theory

2. **Gregor, T. et al.** (2007). "Probing the limits to positional information." *Cell* 130, 153-164.
   - Experimental measurement of Bicoid gradient

3. **Lander, A.D.** (2007). "Morpheus unbound: reimagining the morphogen gradient." *Cell* 128, 245-256.
   - Modern perspective on morphogen gradients

---

## 4. Cellular Automata (Local Interaction Rules)

### Mathematical Formulation

```
Cellular Automaton:

s_i(t+1) = f(s_i(t), {s_j(t) | j ∈ N(i)})

where:
  s_i(t)   = state of cell i at time t
  N(i)     = neighborhood of cell i
  f        = local update rule

Examples of neighborhoods (2D grid):
  - Von Neumann: {(i±1,j), (i,j±1)} (4 neighbors)
  - Moore: {(i±1,j±1), (i±1,j), (i,j±1)} (8 neighbors)
  - Extended: radius-r neighborhood
```

### Conway's Game of Life

```
Rules (Moore neighborhood):
  1. Birth: dead cell with exactly 3 live neighbors → alive
  2. Survival: live cell with 2-3 live neighbors → alive
  3. Death: otherwise → dead

Mathematically:
s(t+1) = { 1  if N(t) = 3 or (s(t) = 1 and N(t) = 2)
         { 0  otherwise

where N(t) = number of live neighbors
```

### Python Implementation

```python
class CellularAutomaton:
    """
    General cellular automaton simulator.

    References:
        Wolfram, S. (2002). A New Kind of Science. Wolfram Media.
    """

    def __init__(self, size, rule='life'):
        """
        Args:
            size: grid size (N × N)
            rule: update rule ('life', 'brian', custom function)
        """
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)

        if rule == 'life':
            self.update_fn = self.game_of_life_rule
        elif rule == 'brian':
            self.update_fn = self.brians_brain_rule
        else:
            self.update_fn = rule

    def set_initial_state(self, pattern='random', density=0.3):
        """
        Set initial configuration.

        Args:
            pattern: 'random', 'glider', 'blinker', etc.
            density: fraction of live cells (for random)
        """
        if pattern == 'random':
            self.grid = (np.random.rand(self.size, self.size) < density).astype(int)

        elif pattern == 'glider':
            self.grid = np.zeros((self.size, self.size), dtype=int)
            glider = np.array([[0, 1, 0],
                              [0, 0, 1],
                              [1, 1, 1]])
            self.grid[1:4, 1:4] = glider

        elif pattern == 'blinker':
            self.grid = np.zeros((self.size, self.size), dtype=int)
            mid = self.size // 2
            self.grid[mid, mid-1:mid+2] = 1

    def count_neighbors(self, i, j):
        """Count live neighbors (Moore neighborhood)."""
        count = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni = (i + di) % self.size  # Periodic boundary
                nj = (j + dj) % self.size
                count += self.grid[ni, nj]
        return count

    def game_of_life_rule(self, state, neighbors):
        """Conway's Game of Life rule."""
        if state == 1:
            # Live cell
            return 1 if neighbors in [2, 3] else 0
        else:
            # Dead cell
            return 1 if neighbors == 3 else 0

    def brians_brain_rule(self, state, neighbors):
        """
        Brian's Brain (3-state CA):
          0 = off, 1 = on, 2 = dying
        """
        if state == 0:
            # Off → on if exactly 2 neighbors are on
            return 1 if neighbors == 2 else 0
        elif state == 1:
            # On → dying
            return 2
        else:  # state == 2
            # Dying → off
            return 0

    def step(self):
        """Execute one timestep."""
        new_grid = np.zeros_like(self.grid)

        for i in range(self.size):
            for j in range(self.size):
                neighbors = self.count_neighbors(i, j)
                new_grid[i, j] = self.update_fn(self.grid[i, j], neighbors)

        self.grid = new_grid

    def simulate(self, n_steps):
        """
        Run simulation.

        Args:
            n_steps: number of timesteps

        Returns:
            history: list of grid states
        """
        history = [self.grid.copy()]

        for _ in range(n_steps):
            self.step()
            history.append(self.grid.copy())

        return history


# Example: Game of Life
ca = CellularAutomaton(size=100, rule='life')
ca.set_initial_state('random', density=0.3)

history = ca.simulate(n_steps=100)

# Animate (display selected frames)
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
timesteps = [0, 20, 40, 60, 80, 100]

for ax, t in zip(axes.flat, timesteps):
    ax.imshow(history[t], cmap='binary')
    ax.set_title(f't = {t}')
    ax.axis('off')

plt.suptitle("Conway's Game of Life")
plt.tight_layout()
```

### Elementary Cellular Automata (1D)

```python
class ElementaryCA:
    """
    1D cellular automaton (Wolfram's elementary CAs).

    256 possible rules (2^8).
    """

    def __init__(self, size, rule_number):
        """
        Args:
            size: number of cells
            rule_number: 0-255 (Wolfram rule number)
        """
        self.size = size
        self.state = np.zeros(size, dtype=int)

        # Convert rule number to lookup table
        self.rule = self.number_to_rule(rule_number)

    def number_to_rule(self, n):
        """Convert rule number to lookup table."""
        binary = format(n, '08b')  # 8-bit binary
        rule_dict = {}

        for i, config in enumerate(['111', '110', '101', '100',
                                   '011', '010', '001', '000']):
            rule_dict[config] = int(binary[i])

        return rule_dict

    def step(self):
        """Update one timestep."""
        new_state = np.zeros(self.size, dtype=int)

        for i in range(self.size):
            left = self.state[(i - 1) % self.size]
            center = self.state[i]
            right = self.state[(i + 1) % self.size]

            config = f'{left}{center}{right}'
            new_state[i] = self.rule[config]

        self.state = new_state

    def simulate(self, n_steps):
        """Simulate and return spacetime diagram."""
        history = np.zeros((n_steps + 1, self.size), dtype=int)
        history[0] = self.state.copy()

        for t in range(n_steps):
            self.step()
            history[t + 1] = self.state.copy()

        return history


# Example: Rule 30 (chaotic), Rule 110 (Turing-complete)
for rule_num in [30, 110]:
    ca = ElementaryCA(size=200, rule_number=rule_num)
    ca.state[100] = 1  # Single seed in middle

    spacetime = ca.simulate(n_steps=100)

    plt.figure(figsize=(12, 6))
    plt.imshow(spacetime, cmap='binary', interpolation='nearest')
    plt.title(f'Elementary CA: Rule {rule_num}')
    plt.xlabel('Cell index')
    plt.ylabel('Time')
    plt.tight_layout()
```

### Key References

1. **Wolfram, S.** (2002). *A New Kind of Science*. Wolfram Media.
   - Comprehensive exploration of cellular automata

2. **Gardner, M.** (1970). "Mathematical Games: The fantastic combinations of John Conway's new solitaire game 'life'." *Scientific American*.
   - Introduced Game of Life to popular audience

3. **Cook, M.** (2004). "Universality in Elementary Cellular Automata." *Complex Systems* 15, 1-40.
   - Proof that Rule 110 is Turing-complete

---

# Summary Tables

## Layer 0: Physical Substrate - Key Equations

| Model | Equation | Application |
|-------|----------|-------------|
| Langevin | dx/dt = -(1/γ)∇U + √(2D)η(t) | Protein dynamics, molecular motors |
| Diffusion | ∂c/∂t = D∇²c | Signaling molecules, neurotransmitters |
| Energy Landscape | U(x), ΔU_barrier, k ∝ exp(-ΔU/kT) | Protein folding, state transitions |

## Layer 1: Capability Graph - Key Metrics

| Metric | Formula | Meaning |
|--------|---------|---------|
| Laplacian | L = D - A | Governs diffusion on graph |
| Fiedler value | λ₂(L) | Connectivity strength |
| Clustering | C = ⟨triangles/triples⟩ | Local clustering |
| Betweenness | g(v) = Σ σ_st(v)/σ_st | Information flow centrality |

## Layer 2: Morphogenesis - Pattern Types

| System | Parameters | Pattern |
|--------|-----------|---------|
| Gray-Scott | F=0.035, k=0.065 | Spots |
| Gray-Scott | F=0.035, k=0.060 | Stripes |
| Gierer-Meinhardt | D_h >> D_a | Periodic segments |
| Morphogen gradient | λ = √(D/k) | Exponential decay |
| Game of Life | B3/S23 | Complex emergent |

---

# Implementation Checklist

For implementing Layers 0-2 in BioAI system:

## Layer 0: Physical Substrate
- [ ] Implement Langevin dynamics engine
- [ ] Define potential energy functions for state transitions
- [ ] Add thermal noise generators with correct statistics
- [ ] Implement Kramers rate calculations for barrier crossing
- [ ] Validate against known analytical solutions

## Layer 1: Capability Graph
- [ ] Design graph representation (adjacency matrix vs. edge list)
- [ ] Implement graph Laplacian computation
- [ ] Add spectral analysis routines
- [ ] Implement message passing framework
- [ ] Add topology metric calculations
- [ ] Validate graph algorithms against NetworkX

## Layer 2: Morphogenesis
- [ ] Implement reaction-diffusion solver (explicit/implicit)
- [ ] Add Gray-Scott parameter sets for different patterns
- [ ] Implement Gierer-Meinhardt solver
- [ ] Add morphogen gradient generator
- [ ] Implement cellular automaton engine
- [ ] Validate pattern formation against literature
- [ ] Add visualization tools for spatiotemporal dynamics

---

# Further Reading

## Books

1. **Risken, H.** (1996). *The Fokker-Planck Equation*. Springer.
2. **Murray, J.D.** (2003). *Mathematical Biology II: Spatial Models*. Springer.
3. **Newman, M.E.J.** (2010). *Networks: An Introduction*. Oxford.
4. **Wolfram, S.** (2002). *A New Kind of Science*. Wolfram Media.

## Review Articles

1. **Onuchic et al.** (1997). "Energy landscape perspective on protein folding." *Ann. Rev. Phys. Chem.*
2. **Barabási & Oltvai** (2004). "Network biology." *Nat. Rev. Genet.*
3. **Kondo & Miura** (2010). "Reaction-diffusion model as a framework for understanding biological pattern formation." *Science*.

## Databases

1. **BioModels**: https://www.ebi.ac.uk/biomodels/
2. **ModelDB**: https://senselab.med.yale.edu/ModelDB/
3. **NeuroML**: https://neuroml.org/

---

**Document Status:** Complete
**Next Steps:** Implement computational kernels and validate against biological data
**Related Documents:**
- `/home/user/MAINFRAME/BIOAI_88_LAYER_HIERARCHY.md`
- `/home/user/MAINFRAME/BIOAI_COMPLETE_ARCHITECTURE_CASCADE.md`
