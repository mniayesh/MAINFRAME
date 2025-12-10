# BioAI Layers 0-2: Quick Reference Guide

**Version:** 1.0
**Date:** December 10, 2025

---

## Overview

This guide provides quick access to the mathematical foundations of BioAI Layers 0-2:
- **Layer 0:** Physical Substrate (stochastic dynamics, energy landscapes)
- **Layer 1:** Capability Graph (graph theory, GNNs)
- **Layer 2:** Morphogenesis (reaction-diffusion, pattern formation)

**Full Documentation:** `/home/user/MAINFRAME/BIOAI_LAYERS_0_2_MATHEMATICAL_REFERENCE.md`
**Database:** `/home/user/MAINFRAME/bioformulas/bioformulas.db`
**Query Script:** `/home/user/MAINFRAME/bioformulas/query_layers_0_2.py`

---

## Layer 0: Physical Substrate - Essential Equations

### 1. Langevin Equation (Stochastic Dynamics)

```latex
dx/dt = -(1/γ)∇U(x) + √(2D)η(t)
```

**Use:** Molecular dynamics, protein folding, thermal fluctuations
**Code:** `langevin_step(x, dt, U_grad, gamma, D)`

**Key Parameters:**
- `γ` = friction coefficient
- `D` = diffusion coefficient = kB·T/γ
- `U(x)` = potential energy landscape
- `η(t)` = white noise

---

### 2. Diffusion Equation (Fick's 2nd Law)

```latex
∂c/∂t = D∇²c
```

**Use:** Molecular transport, neurotransmitter spreading
**Solution:** Gaussian spreading with σ(t) = √(2Dt)

---

### 3. Energy Landscapes

```latex
Barrier crossing rate: k = (ω₀ωb/2πγ) exp(-ΔU/kBT)
Equilibrium: ρ(x) ∝ exp(-U(x)/kBT)
```

**Use:** State transitions, protein folding, reaction kinetics

---

## Layer 1: Capability Graph - Essential Equations

### 1. Graph Laplacian

```latex
L = D - A
(where D = degree matrix, A = adjacency)
```

**Use:** Diffusion on networks, community detection, spectral clustering
**Code:** `L = np.diag(A.sum(axis=1)) - A`

**Properties:**
- Smallest eigenvalue λ₁ = 0
- Fiedler value λ₂ measures connectivity
- Number of zero eigenvalues = number of components

---

### 2. Graph Convolutional Network (GCN)

```latex
H^(l+1) = σ(D̃^(-1/2)ÃD̃^(-1/2)H^(l)W^(l))
```

**Use:** Learning on graph-structured data, protein interaction networks
**Code:** See `gcn_layer()` in reference doc

---

### 3. Heat Diffusion on Graph

```latex
∂s/∂t = -Ls
Solution: s(t) = exp(-Lt)·s(0)
```

**Use:** Signal propagation, information flow on networks

---

## Layer 2: Morphogenesis - Essential Equations

### 1. Gray-Scott Model (Reaction-Diffusion)

```latex
∂u/∂t = Du∇²u - uv² + F(1-u)
∂v/∂t = Dv∇²v + uv² - (F+k)v
```

**Famous Parameter Sets:**
- Spots: F=0.035, k=0.065
- Stripes: F=0.035, k=0.060
- Worms: F=0.058, k=0.065
- Chaos: F=0.026, k=0.051

**Code:** `gray_scott_step(u, v, dx, dt, Du, Dv, F, k)`

---

### 2. Gierer-Meinhardt (Activator-Inhibitor)

```latex
∂a/∂t = ca(a²/h - μa·a + ρa) + Da∇²a
∂h/∂t = ch(a² - μh·h + ρh) + Dh∇²h
```

**Key Feature:** Short-range activation (Da << Dh) + long-range inhibition

**Use:** Segmentation, periodic patterns, regeneration

---

### 3. Morphogen Gradients

```latex
Steady state: c(x) = c₀ exp(-x/λ)
Length scale: λ = √(D/k)
```

**Use:** Positional information, cell fate specification (French flag model)

**Cell fate rule:**
```
if c(x) > θ₁: Type A
elif c(x) > θ₂: Type B
else: Type C
```

---

### 4. Cellular Automata

**Conway's Game of Life:**
- Birth: dead cell + 3 neighbors → alive
- Survival: live cell + 2-3 neighbors → alive
- Death: otherwise → dead

**Elementary CA:** 256 rules (Rule 30 = chaotic, Rule 110 = Turing-complete)

---

## Implementation Checklist

### Quick Start (Python)

```python
import numpy as np
from scipy.ndimage import convolve

# Layer 0: Langevin dynamics
def simulate_langevin(x0, U_grad, T_total, dt, gamma=1.0, kB=1.38e-23, T=300):
    D = kB * T / gamma
    trajectory = [x0]
    x = x0
    for _ in range(int(T_total/dt)):
        drift = -(1/gamma) * U_grad(x)
        noise = np.sqrt(2*D*dt) * np.random.randn(*x.shape)
        x = x + drift*dt + noise
        trajectory.append(x)
    return np.array(trajectory)

# Layer 1: Graph diffusion
def graph_diffusion(s0, adjacency, t, dt):
    D = np.diag(adjacency.sum(axis=1))
    L = D - adjacency
    s = s0
    for _ in range(int(t/dt)):
        s = s - L @ s * dt
    return s

# Layer 2: Gray-Scott
def simulate_gray_scott(size, n_steps, F=0.035, k=0.065):
    u = np.ones((size, size))
    v = np.zeros((size, size))
    v[size//2-10:size//2+10, size//2-10:size//2+10] = 1.0

    kernel = np.array([[0.05, 0.2, 0.05],
                      [0.2, -1.0, 0.2],
                      [0.05, 0.2, 0.05]])

    for _ in range(n_steps):
        laplacian_u = convolve(u, kernel, mode='wrap')
        laplacian_v = convolve(v, kernel, mode='wrap')
        uvv = u * v * v
        u += (0.16*laplacian_u - uvv + F*(1-u))
        v += (0.08*laplacian_v + uvv - (F+k)*v)
        u = np.clip(u, 0, 1)
        v = np.clip(v, 0, 1)

    return u, v
```

---

## Database Queries

### Query formulas by layer

```python
import sqlite3

conn = sqlite3.connect('bioformulas/bioformulas.db')
conn.row_factory = sqlite3.Row

# Get all Layer 0 formulas
formulas = conn.execute("""
    SELECT f.name, f.latex, f.python_code
    FROM formulas f
    JOIN categories c ON f.category_id = c.category_id
    WHERE c.name LIKE 'Layer 0%'
""").fetchall()

for f in formulas:
    print(f"{f['name']}: {f['latex']}")
```

### Search formulas

```python
# Full-text search
results = conn.execute("""
    SELECT name, description
    FROM formulas
    WHERE name LIKE '%diffusion%' OR description LIKE '%diffusion%'
""").fetchall()
```

---

## Key References by Layer

### Layer 0: Physical Substrate

1. **Risken, H.** (1996). *The Fokker-Planck Equation*. Springer.
   - DOI: 10.1007/978-3-642-61544-3
2. **Gardiner, C.W.** (2009). *Stochastic Methods*. Springer.
3. **Berg, H.C.** (1993). *Random Walks in Biology*. Princeton.
4. **Onuchic et al.** (1997). "Energy landscape perspective." *Annu. Rev. Phys. Chem.* 48, 545.

### Layer 1: Capability Graph

1. **Chung, F.R.K.** (1997). *Spectral Graph Theory*. AMS.
2. **Newman, M.E.J.** (2010). *Networks: An Introduction*. Oxford.
3. **Barabási & Oltvai** (2004). "Network biology." *Nat. Rev. Genet.* 5, 101.
4. **Kipf & Welling** (2017). "GCN." *ICLR*. arXiv:1609.02907

### Layer 2: Morphogenesis

1. **Turing, A.M.** (1952). "Chemical basis of morphogenesis." *Phil. Trans. R. Soc.* 237, 37.
2. **Pearson, J.E.** (1993). "Complex patterns." *Science* 261, 189.
3. **Murray, J.D.** (2003). *Mathematical Biology II*. Springer.
4. **Wolpert, L.** (1969). "Positional information." *J. Theor. Biol.* 25, 1.
5. **Gierer & Meinhardt** (1972). "Pattern formation." *Kybernetik* 12, 30.

---

## Computational Resources

### Available Tools

1. **Database:** 295 total formulas (21 for Layers 0-2)
   - Location: `/home/user/MAINFRAME/bioformulas/bioformulas.db`
   - Schema: SQL with full-text search
   - Query tool: `query_layers_0_2.py`

2. **Documentation:**
   - Full reference: `BIOAI_LAYERS_0_2_MATHEMATICAL_REFERENCE.md`
   - Architecture: `BIOAI_COMPLETE_ARCHITECTURE_CASCADE.md`
   - 88 layers: `BIOAI_88_LAYER_HIERARCHY.md`

3. **Python Libraries:**
   - NumPy: numerical arrays
   - SciPy: scientific computing (diffusion, ODEs)
   - NetworkX: graph algorithms
   - PyTorch/JAX: differentiable implementations

---

## Common Patterns

### Pattern 1: Energy Minimization

```python
# Gradient descent on energy landscape
def minimize_energy(x0, U_grad, n_steps=1000, lr=0.01):
    x = x0
    for _ in range(n_steps):
        x = x - lr * U_grad(x)
    return x
```

### Pattern 2: Stochastic Exploration

```python
# Langevin dynamics with annealing
def simulated_annealing(x0, U_grad, T_schedule, dt=0.01):
    x = x0
    for T in T_schedule:
        D = kB * T / gamma
        drift = -(1/gamma) * U_grad(x)
        noise = np.sqrt(2*D*dt) * np.random.randn(*x.shape)
        x = x + drift*dt + noise
    return x
```

### Pattern 3: Diffusive Communication

```python
# Graph-based message passing
def message_passing(states, adjacency, n_rounds=10):
    for _ in range(n_rounds):
        messages = adjacency @ states
        states = activation(states + messages)
    return states
```

### Pattern 4: Self-Organization

```python
# Reaction-diffusion pattern formation
def self_organize(grid_size, n_steps, reaction_fn, D=1.0):
    field = np.random.rand(grid_size, grid_size)
    for _ in range(n_steps):
        laplacian = compute_laplacian(field)
        field += (D * laplacian + reaction_fn(field))
    return field
```

---

## Next Steps

### For Implementation:

1. **Layer 0:** Implement Langevin engine for physical substrate
2. **Layer 1:** Build graph representation of hardware capabilities
3. **Layer 2:** Add morphogenesis for self-organizing structure

### For Research:

1. **Validate:** Compare simulations against biological data
2. **Optimize:** Profile computational kernels for performance
3. **Extend:** Add Layers 3-88 formulations

### For Integration:

1. **Connect layers:** Layer N output → Layer N+1 input
2. **Add feedback:** Higher layers modulate lower layer parameters
3. **Emerge cognition:** Layer 2 patterns → Layer 3 macromolecules

---

## File Organization

```
/home/user/MAINFRAME/
├── BIOAI_LAYERS_0_2_MATHEMATICAL_REFERENCE.md  (Full documentation)
├── BIOAI_LAYERS_0_2_QUICK_REFERENCE.md         (This file)
├── BIOAI_COMPLETE_ARCHITECTURE_CASCADE.md      (14-layer cascade)
├── BIOAI_88_LAYER_HIERARCHY.md                 (Complete hierarchy)
└── bioformulas/
    ├── bioformulas.db                          (Formula database)
    ├── schema.sql                              (Database schema)
    ├── populate_layers_0_2.py                  (Population script)
    └── query_layers_0_2.py                     (Query examples)
```

---

## Summary Statistics

- **Total formulas documented:** 21 (8 Layer 0, 6 Layer 1, 7 Layer 2)
- **Total in database:** 295 formulas across all categories
- **Code examples:** 15+ complete Python implementations
- **References:** 20+ seminal papers and textbooks
- **Computational domains:** Statistical mechanics, graph theory, morphogenesis

**Status:** Complete mathematical foundation for Layers 0-2
**Next:** Implement computational kernels and validate against biology
