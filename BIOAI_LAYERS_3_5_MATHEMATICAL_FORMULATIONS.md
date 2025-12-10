# BioAI Layers 3-5: Complete Mathematical Formulations
## Proto-Components through Cells: From Molecular Kinetics to Self-Regulating Agents

**Author:** BioAI Research Team
**Date:** 2025-12-10
**Status:** Comprehensive Reference Implementation
**Scope:** Molecular through Cellular Layer Mathematical Models

---

# Table of Contents

1. [LAYER 3: Proto-Component Layer (Molecular)](#layer-3-proto-component-layer-molecular)
2. [LAYER 4: Organelle Layer (Functional Subsystems)](#layer-4-organelle-layer-functional-subsystems)
3. [LAYER 5: Cell Layer (Self-Regulating Agents)](#layer-5-cell-layer-self-regulating-agents)
4. [Integration & Composition to Layer 6](#integration--composition-to-layer-6)
5. [Computational Implementation Guide](#computational-implementation-guide)
6. [Complete Code Examples](#complete-code-examples)

---

# LAYER 3: Proto-Component Layer (Molecular)

## Overview

Layer 3 models the fundamental biochemical processes that underpin all cellular computation. These are the atomic units of biological information processing.

**Core Principle:** Molecular interactions follow thermodynamic laws and kinetic rate equations that can be modeled as differential equations.

---

## 3.1 Molecular Binding Kinetics

### 3.1.1 Basic Binding Equilibrium

**Biological Context:** Ligand-receptor binding, protein-protein interactions, DNA-protein binding

**Reaction:**
```
A + B ⇌ AB
    k₊
    k₋
```

**Mathematical Formulation:**

Dissociation constant:
$$K_d = \frac{k_-}{k_+} = \frac{[A][B]}{[AB]}$$

Rate equations:
$$\frac{d[AB]}{dt} = k_+ [A][B] - k_- [AB]$$

$$\frac{d[A]}{dt} = -k_+ [A][B] + k_- [AB]$$

$$\frac{d[B]}{dt} = -k_+ [A][B] + k_- [AB]$$

**Equilibrium Solution:**

At equilibrium ($\frac{d}{dt} = 0$):

$$[AB]_{eq} = \frac{[A]_0 [B]_0}{K_d + [A]_0}$$

**Parameter Ranges:**

| Parameter | Typical Range | Units | Example (Neurotransmitter) |
|-----------|--------------|-------|---------------------------|
| $k_+$ | $10^6 - 10^9$ | M⁻¹s⁻¹ | $10^7$ M⁻¹s⁻¹ (Glutamate-AMPAR) |
| $k_-$ | $10^{-3} - 10^3$ | s⁻¹ | $10^2$ s⁻¹ |
| $K_d$ | $10^{-12} - 10^{-3}$ | M | $10^{-6}$ M (μM range) |
| $[A]_0, [B]_0$ | $10^{-9} - 10^{-3}$ | M | $10^{-6}$ M |

### 3.1.2 Cooperative Binding (Hill Equation)

**Biological Context:** Hemoglobin-oxygen binding, allosteric enzymes, transcription factors

**Mathematical Formulation:**

$$\theta = \frac{[L]^n}{K_d^n + [L]^n}$$

Where:
- $\theta$ = fraction of binding sites occupied
- $[L]$ = ligand concentration
- $n$ = Hill coefficient (cooperativity)
- $K_d$ = dissociation constant

**Differential Form:**

$$\frac{d\theta}{dt} = k_+ [L]^n (1-\theta) - k_- \theta$$

**Parameter Ranges:**

| Parameter | Range | Interpretation |
|-----------|-------|----------------|
| $n = 1$ | Non-cooperative | Independent binding |
| $n > 1$ | Positive cooperativity | Binding facilitates more binding |
| $n < 1$ | Negative cooperativity | Binding inhibits more binding |
| $n = 2-4$ | Typical biological range | |

**Computational Implementation:**

```python
import numpy as np
from scipy.integrate import odeint

class CooperativeBinding:
    """Hill equation model for cooperative binding"""

    def __init__(self, kd, hill_coef, k_plus, k_minus):
        self.kd = kd              # Dissociation constant (M)
        self.n = hill_coef        # Hill coefficient
        self.k_plus = k_plus      # On-rate (M⁻¹s⁻¹)
        self.k_minus = k_minus    # Off-rate (s⁻¹)

    def equilibrium_occupancy(self, ligand_conc):
        """Steady-state fraction bound"""
        return (ligand_conc**self.n) / (self.kd**self.n + ligand_conc**self.n)

    def dynamics(self, state, t, ligand_conc):
        """ODE for binding dynamics"""
        theta = state[0]  # Fraction bound

        # Rate equation
        dtheta_dt = (self.k_plus * ligand_conc**self.n * (1 - theta) -
                     self.k_minus * theta)

        return [dtheta_dt]

    def simulate(self, ligand_conc, t_span, theta_0=0.0):
        """Simulate binding dynamics"""
        t = np.linspace(t_span[0], t_span[1], 1000)
        solution = odeint(self.dynamics, [theta_0], t, args=(ligand_conc,))
        return t, solution[:, 0]

# Example: NMDA receptor binding (n=2, cooperative)
nmda_binding = CooperativeBinding(
    kd=1e-6,         # 1 μM
    hill_coef=2,     # Positive cooperativity
    k_plus=1e7,      # Fast on-rate
    k_minus=10       # Moderate off-rate
)

# Simulate response to 10 μM glutamate
t, theta = nmda_binding.simulate(
    ligand_conc=10e-6,  # 10 μM
    t_span=[0, 1.0],    # 1 second
    theta_0=0.0
)
```

---

## 3.2 Enzyme Kinetics (Michaelis-Menten)

### 3.2.1 Standard Michaelis-Menten

**Biological Context:** Enzymatic reactions, metabolic pathways, signal transduction

**Reaction Scheme:**
```
E + S ⇌ ES → E + P
    k₁   k₂
    k₋₁
```

**Mathematical Formulation:**

Rate equation (Michaelis-Menten):
$$v = \frac{V_{max} [S]}{K_m + [S]}$$

Where:
- $v$ = reaction velocity
- $V_{max} = k_{cat} [E]_0$ = maximum velocity
- $K_m = \frac{k_{-1} + k_2}{k_1}$ = Michaelis constant
- $k_{cat}$ = turnover number

**Full ODE System:**

$$\frac{d[S]}{dt} = -k_1 [E][S] + k_{-1}[ES]$$

$$\frac{d[E]}{dt} = -k_1 [E][S] + (k_{-1} + k_2)[ES]$$

$$\frac{d[ES]}{dt} = k_1 [E][S] - (k_{-1} + k_2)[ES]$$

$$\frac{d[P]}{dt} = k_2 [ES]$$

**Conservation Law:**
$$[E]_0 = [E] + [ES]$$

**Parameter Ranges:**

| Parameter | Range | Units | Example Enzyme |
|-----------|-------|-------|----------------|
| $K_m$ | $10^{-7} - 10^{-2}$ | M | $10^{-5}$ M (Hexokinase) |
| $k_{cat}$ | $10^{-1} - 10^7$ | s⁻¹ | $10^3$ s⁻¹ (Carbonic anhydrase) |
| $k_{cat}/K_m$ | $10^3 - 10^9$ | M⁻¹s⁻¹ | $10^8$ (diffusion-limited) |
| $[E]_0$ | $10^{-9} - 10^{-6}$ | M | $10^{-8}$ M (nM range) |

### 3.2.2 Enzyme Inhibition

**Competitive Inhibition:**

$$v = \frac{V_{max} [S]}{K_m (1 + [I]/K_i) + [S]}$$

**Non-competitive Inhibition:**

$$v = \frac{V_{max} [S]}{(K_m + [S])(1 + [I]/K_i)}$$

**Uncompetitive Inhibition:**

$$v = \frac{V_{max} [S]}{K_m + [S](1 + [I]/K_i)}$$

**Computational Implementation:**

```python
class MichaelisMenten:
    """Complete Michaelis-Menten enzyme kinetics"""

    def __init__(self, km, vmax, k1, k_minus1, k2):
        self.km = km              # Michaelis constant (M)
        self.vmax = vmax          # Maximum velocity (M/s)
        self.k1 = k1              # Forward binding (M⁻¹s⁻¹)
        self.k_minus1 = k_minus1  # Reverse binding (s⁻¹)
        self.k2 = k2              # Catalytic rate (s⁻¹)

        # Calculate derived parameters
        self.kcat = k2
        self.enzyme_0 = vmax / k2  # Total enzyme concentration

    def velocity(self, substrate_conc):
        """Steady-state reaction velocity (simplified MM equation)"""
        return (self.vmax * substrate_conc) / (self.km + substrate_conc)

    def velocity_with_inhibition(self, substrate_conc, inhibitor_conc=0,
                                 ki=1e-6, mode='competitive'):
        """MM velocity with inhibition"""
        if mode == 'competitive':
            km_apparent = self.km * (1 + inhibitor_conc / ki)
            return (self.vmax * substrate_conc) / (km_apparent + substrate_conc)

        elif mode == 'noncompetitive':
            vmax_apparent = self.vmax / (1 + inhibitor_conc / ki)
            return (vmax_apparent * substrate_conc) / (self.km + substrate_conc)

        elif mode == 'uncompetitive':
            km_apparent = self.km / (1 + inhibitor_conc / ki)
            vmax_apparent = self.vmax / (1 + inhibitor_conc / ki)
            return (vmax_apparent * substrate_conc) / (km_apparent + substrate_conc)

    def full_dynamics(self, state, t, substrate_influx=0):
        """Full ODE system for enzyme kinetics"""
        S, E, ES, P = state

        # Rate equations
        dS_dt = substrate_influx - self.k1*E*S + self.k_minus1*ES
        dE_dt = -self.k1*E*S + (self.k_minus1 + self.k2)*ES
        dES_dt = self.k1*E*S - (self.k_minus1 + self.k2)*ES
        dP_dt = self.k2 * ES

        return [dS_dt, dE_dt, dES_dt, dP_dt]

    def simulate(self, initial_state, t_span, substrate_influx=0):
        """Simulate full enzyme kinetics"""
        t = np.linspace(t_span[0], t_span[1], 1000)
        solution = odeint(self.full_dynamics, initial_state, t,
                         args=(substrate_influx,))
        return t, solution

# Example: Glucose phosphorylation by hexokinase
hexokinase = MichaelisMenten(
    km=1e-4,       # 0.1 mM
    vmax=1e-7,     # 0.1 μM/s (depends on enzyme conc)
    k1=1e6,        # Fast binding
    k_minus1=10,   # Slow unbinding
    k2=100         # Moderate catalysis
)

# Simulate enzyme reaction
initial_state = [1e-3, 1e-8, 0, 0]  # [S, E, ES, P]
t, solution = hexokinase.simulate(initial_state, [0, 10])
```

---

## 3.3 Reaction Networks

### 3.3.1 Mass Action Kinetics

**Biological Context:** Metabolic pathways, signaling cascades, gene regulatory networks

**General Form:**

For reaction: $\sum_i \nu_i^- X_i \rightarrow \sum_i \nu_i^+ X_i$

Rate equation:
$$v = k \prod_i [X_i]^{\nu_i^-}$$

**Example: Glycolysis Fragment**

```
Glucose → G6P → F6P → FBP
   k₁      k₂     k₃
```

ODEs:
$$\frac{d[Glc]}{dt} = -k_1 [Glc]$$
$$\frac{d[G6P]}{dt} = k_1 [Glc] - k_2 [G6P]$$
$$\frac{d[F6P]}{dt} = k_2 [G6P] - k_3 [F6P]$$
$$\frac{d[FBP]}{dt} = k_3 [F6P]$$

### 3.3.2 Feedback and Feed-forward Loops

**Negative Feedback (Homeostasis):**

```
     ┌─────┐
     │     ↓
A → B → C → D
     ↑     │
     └─────┘
```

ODEs with feedback:
$$\frac{d[A]}{dt} = k_0 - k_1 [A]$$
$$\frac{d[B]}{dt} = k_1 [A] - k_2 \frac{[B]}{1 + ([D]/K_i)^n}$$
$$\frac{d[D]}{dt} = k_3 [C] - k_4 [D]$$

**Parameter Ranges:**

| Parameter | Typical Range | Units |
|-----------|--------------|-------|
| Rate constants ($k_i$) | $10^{-3} - 10^3$ | s⁻¹ or M⁻¹s⁻¹ |
| Inhibition constant ($K_i$) | $10^{-9} - 10^{-6}$ | M |
| Hill coefficient ($n$) | 1-4 | dimensionless |

**Computational Implementation:**

```python
class ReactionNetwork:
    """General reaction network simulator"""

    def __init__(self, species_names):
        self.species = species_names
        self.reactions = []
        self.n_species = len(species_names)

    def add_reaction(self, reactants, products, rate_constant,
                     rate_law='mass_action'):
        """
        Add a reaction to the network

        Parameters:
        -----------
        reactants : dict
            {species_name: stoichiometry}
        products : dict
            {species_name: stoichiometry}
        rate_constant : float
            Reaction rate constant
        rate_law : str
            'mass_action', 'michaelis_menten', or 'hill'
        """
        self.reactions.append({
            'reactants': reactants,
            'products': products,
            'k': rate_constant,
            'law': rate_law
        })

    def compute_rate(self, reaction, concentrations):
        """Compute reaction rate given current concentrations"""
        if reaction['law'] == 'mass_action':
            rate = reaction['k']
            for species, stoich in reaction['reactants'].items():
                idx = self.species.index(species)
                rate *= concentrations[idx]**stoich
            return rate

        # Add other rate laws as needed
        return 0.0

    def derivatives(self, state, t):
        """Compute d[X]/dt for all species"""
        d_state = np.zeros(self.n_species)

        for reaction in self.reactions:
            rate = self.compute_rate(reaction, state)

            # Subtract reactants
            for species, stoich in reaction['reactants'].items():
                idx = self.species.index(species)
                d_state[idx] -= stoich * rate

            # Add products
            for species, stoich in reaction['products'].items():
                idx = self.species.index(species)
                d_state[idx] += stoich * rate

        return d_state

    def simulate(self, initial_concentrations, t_span):
        """Simulate the reaction network"""
        t = np.linspace(t_span[0], t_span[1], 1000)
        solution = odeint(self.derivatives, initial_concentrations, t)
        return t, solution

# Example: Simple cascade with feedback
network = ReactionNetwork(['A', 'B', 'C', 'D'])

# A → B → C → D
network.add_reaction({'A': 1}, {'B': 1}, k=1.0)
network.add_reaction({'B': 1}, {'C': 1}, k=2.0)
network.add_reaction({'C': 1}, {'D': 1}, k=1.5)

# D inhibits B production (requires custom rate law in full implementation)
# This is simplified; real implementation would modify compute_rate

initial = [1.0, 0.0, 0.0, 0.0]  # Start with only A
t, solution = network.simulate(initial, [0, 10])
```

---

## 3.4 State Transition Models (Markov Models)

### 3.4.1 Discrete State Markov Chains

**Biological Context:** Ion channel gating, protein conformational changes, enzyme states

**Mathematical Formulation:**

State probability vector: $\mathbf{p}(t) = [p_1(t), p_2(t), ..., p_n(t)]^T$

Master equation:
$$\frac{d\mathbf{p}}{dt} = \mathbf{Q} \mathbf{p}$$

Where $\mathbf{Q}$ is the rate matrix:
$$Q_{ij} = \begin{cases}
k_{ij} & i \neq j \\
-\sum_{k \neq i} k_{ik} & i = j
\end{cases}$$

**Example: Two-State Channel (Closed ⇌ Open)**

```
Closed ⇌ Open
   α  β
```

Rate matrix:
$$\mathbf{Q} = \begin{bmatrix} -\alpha & \alpha \\ \beta & -\beta \end{bmatrix}$$

ODEs:
$$\frac{dp_C}{dt} = -\alpha p_C + \beta p_O$$
$$\frac{dp_O}{dt} = \alpha p_C - \beta p_O$$

Steady-state:
$$p_O^{ss} = \frac{\alpha}{\alpha + \beta}$$

### 3.4.2 Multi-State Ion Channel Models

**Three-State Model (C ⇌ O ⇌ I):**

```
Closed ⇌ Open ⇌ Inactivated
   α₁  β₁   α₂  β₂
```

Rate matrix:
$$\mathbf{Q} = \begin{bmatrix}
-\alpha_1 & \alpha_1 & 0 \\
\beta_1 & -(\beta_1+\alpha_2) & \alpha_2 \\
0 & \beta_2 & -\beta_2
\end{bmatrix}$$

**Voltage-Dependent Rates:**

$$\alpha(V) = \alpha_0 \exp\left(\frac{z \delta F V}{RT}\right)$$

$$\beta(V) = \beta_0 \exp\left(\frac{-z (1-\delta) F V}{RT}\right)$$

Where:
- $V$ = membrane voltage
- $z$ = gating charge (typically 2-6)
- $\delta$ = fraction of voltage drop
- $F$ = Faraday constant
- $R$ = gas constant
- $T$ = temperature

**Parameter Ranges:**

| Parameter | Range | Units |
|-----------|-------|-------|
| $\alpha_0, \beta_0$ | $10^{-1} - 10^4$ | s⁻¹ |
| $z$ | 1-6 | elementary charges |
| $\delta$ | 0-1 | dimensionless |
| $V$ | -100 to +50 | mV |

**Computational Implementation:**

```python
class MarkovChannel:
    """Markov state model for ion channels"""

    def __init__(self, n_states, state_names=None):
        self.n_states = n_states
        self.state_names = state_names or [f"S{i}" for i in range(n_states)]
        self.Q = np.zeros((n_states, n_states))
        self.voltage_dependent = {}

    def add_transition(self, from_state, to_state, rate,
                      voltage_dependent=False, z=0, delta=0.5):
        """Add a transition between states"""
        i = self.state_names.index(from_state)
        j = self.state_names.index(to_state)

        if voltage_dependent:
            self.voltage_dependent[(i, j)] = {
                'rate0': rate,
                'z': z,
                'delta': delta
            }
        else:
            self.Q[i, j] = rate
            self.Q[i, i] -= rate

    def update_rates(self, voltage):
        """Update voltage-dependent transition rates"""
        F = 96485  # Faraday constant (C/mol)
        R = 8.314  # Gas constant (J/(mol·K))
        T = 310    # Temperature (K) - physiological

        for (i, j), params in self.voltage_dependent.items():
            rate = params['rate0'] * np.exp(
                params['z'] * params['delta'] * F * voltage / (R * T)
            )
            self.Q[i, j] = rate
            self.Q[i, i] -= rate

    def derivatives(self, state, t, voltage_func):
        """Compute dp/dt for all states"""
        voltage = voltage_func(t) if callable(voltage_func) else voltage_func
        self.update_rates(voltage)
        return self.Q @ state

    def steady_state(self, voltage):
        """Compute steady-state probabilities at given voltage"""
        self.update_rates(voltage)

        # Solve Q·p = 0 with constraint Σp = 1
        A = np.vstack([self.Q.T, np.ones(self.n_states)])
        b = np.zeros(self.n_states + 1)
        b[-1] = 1

        p_ss = np.linalg.lstsq(A, b, rcond=None)[0]
        return p_ss

    def simulate(self, initial_state, t_span, voltage):
        """Simulate channel state evolution"""
        t = np.linspace(t_span[0], t_span[1], 1000)
        solution = odeint(self.derivatives, initial_state, t, args=(voltage,))
        return t, solution

# Example: Sodium channel (3-state model)
na_channel = MarkovChannel(3, ['Closed', 'Open', 'Inactivated'])

# Transitions
na_channel.add_transition('Closed', 'Open', rate=1.0,
                         voltage_dependent=True, z=3, delta=0.5)
na_channel.add_transition('Open', 'Closed', rate=4.0,
                         voltage_dependent=True, z=-3, delta=0.5)
na_channel.add_transition('Open', 'Inactivated', rate=0.5)
na_channel.add_transition('Inactivated', 'Closed', rate=0.1)

# Simulate at -65 mV (resting) then step to 0 mV
def voltage_step(t):
    return -65 if t < 5 else 0

initial = [1.0, 0.0, 0.0]  # Start in closed state
t, solution = na_channel.simulate(initial, [0, 20], voltage_step)
```

---

# LAYER 4: Organelle Layer (Functional Subsystems)

## Overview

Layer 4 models the compartmentalized functional units within cells, particularly focusing on energy metabolism, material transport, and compartmental organization.

---

## 4.1 Metabolic Network Models

### 4.1.1 Glycolysis (Complete Pathway)

**Biological Context:** Primary glucose metabolism pathway, produces ATP and NADH

**Simplified Reaction Network:**

```
Glucose → G6P → F6P → FBP → DHAP/G3P → 1,3-BPG → 3-PG → 2-PG → PEP → Pyruvate
  HK      PGI    PFK     ALD      TPI        GAPDH    PGK    PGM    ENO    PK
```

**Key Regulatory Steps:**

1. **Hexokinase (HK):** Glucose → G6P
$$v_{HK} = \frac{V_{max}^{HK} [Glc]}{K_m^{Glc} + [Glc]} \cdot \frac{K_i^{G6P}}{K_i^{G6P} + [G6P]}$$

2. **Phosphofructokinase (PFK):** F6P → FBP (rate-limiting step)
$$v_{PFK} = \frac{V_{max}^{PFK} [F6P]}{K_m^{F6P} + [F6P]} \cdot \frac{1 + ([AMP]/K_a)^n}{1 + ([ATP]/K_i)^n}$$

3. **Pyruvate Kinase (PK):** PEP → Pyruvate
$$v_{PK} = \frac{V_{max}^{PK} [PEP]}{K_m^{PEP} + [PEP]} \cdot \frac{1 + ([FBP]/K_a)^2}{1}$$

**Parameter Ranges (Glycolysis):**

| Enzyme | $K_m$ (mM) | $V_{max}$ (mM/min) | Regulation |
|--------|------------|-------------------|------------|
| HK | 0.1 | 0.5 | Inhibited by G6P |
| PFK | 0.5 | 2.0 | Activated by AMP, inhibited by ATP |
| PK | 0.3 | 5.0 | Activated by FBP |

### 4.1.2 ATP/ADP Cycle (Energy Currency)

**Energy Balance Equation:**

$$\frac{d[ATP]}{dt} = v_{synthesis} - v_{consumption}$$

$$v_{synthesis} = v_{glycolysis} + v_{oxidative\_phosphorylation}$$

$$v_{consumption} = v_{biosynthesis} + v_{transport} + v_{signaling}$$

**Detailed ATP Synthesis (Oxidative Phosphorylation):**

$$v_{ox\_phos} = \frac{V_{max} [ADP][P_i]}{(K_m^{ADP} + [ADP])(K_m^{Pi} + [P_i])} \cdot \frac{NADH}{K_m^{NADH} + NADH}$$

**ATP Hydrolysis (Generic Consumer):**

$$v_{ATPase} = \frac{V_{max}^{ATPase} [ATP]}{K_m^{ATP} + [ATP]}$$

**Adenylate Energy Charge:**

$$EC = \frac{[ATP] + 0.5[ADP]}{[ATP] + [ADP] + [AMP]}$$

Typical cellular range: $EC = 0.8 - 0.95$

**Parameter Ranges:**

| Parameter | Resting | Active | Units |
|-----------|---------|--------|-------|
| $[ATP]$ | 3-5 | 2-4 | mM |
| $[ADP]$ | 0.5-1 | 1-2 | mM |
| $[AMP]$ | 0.05-0.1 | 0.1-0.3 | mM |
| $ATP/ADP$ ratio | 5-10 | 2-4 | dimensionless |

**Computational Implementation:**

```python
class Glycolysis:
    """Complete glycolysis pathway model"""

    def __init__(self):
        # Enzyme parameters (all in mM and min⁻¹)
        self.params = {
            # Hexokinase
            'V_HK': 0.5,
            'Km_Glc': 0.1,
            'Ki_G6P': 1.0,

            # Phosphofructokinase (rate-limiting)
            'V_PFK': 2.0,
            'Km_F6P': 0.5,
            'Ka_AMP': 0.05,
            'Ki_ATP': 2.0,
            'n_PFK': 2,

            # Pyruvate kinase
            'V_PK': 5.0,
            'Km_PEP': 0.3,
            'Ka_FBP': 0.1,

            # ATP synthesis/consumption
            'V_ox_phos': 3.0,
            'Km_ADP': 0.3,
            'Km_Pi': 1.0,
            'V_ATPase': 2.0,
            'Km_ATP_use': 1.0
        }

        # Species indices
        self.species_names = ['Glc', 'G6P', 'F6P', 'FBP', 'PEP',
                             'Pyr', 'ATP', 'ADP', 'AMP', 'Pi']

    def reaction_rates(self, conc):
        """Compute all reaction rates"""
        Glc, G6P, F6P, FBP, PEP, Pyr, ATP, ADP, AMP, Pi = conc
        p = self.params

        # Hexokinase (with product inhibition)
        v_HK = (p['V_HK'] * Glc / (p['Km_Glc'] + Glc) *
                p['Ki_G6P'] / (p['Ki_G6P'] + G6P))

        # Phosphofructokinase (allosteric regulation)
        amp_activation = (1 + (AMP / p['Ka_AMP'])**p['n_PFK'])
        atp_inhibition = (1 + (ATP / p['Ki_ATP'])**p['n_PFK'])
        v_PFK = (p['V_PFK'] * F6P / (p['Km_F6P'] + F6P) *
                 amp_activation / atp_inhibition)

        # Pyruvate kinase (activated by FBP)
        fbp_activation = 1 + (FBP / p['Ka_FBP'])**2
        v_PK = (p['V_PK'] * PEP / (p['Km_PEP'] + PEP) *
                fbp_activation)

        # Simplified intermediate steps (first-order)
        v_PGI = 5.0 * G6P  # G6P → F6P
        v_ALD = 3.0 * FBP  # FBP → PEP (lumped)

        # ATP synthesis (oxidative phosphorylation)
        v_ox_phos = (p['V_ox_phos'] * ADP * Pi /
                     ((p['Km_ADP'] + ADP) * (p['Km_Pi'] + Pi)))

        # ATP consumption
        v_ATPase = p['V_ATPase'] * ATP / (p['Km_ATP_use'] + ATP)

        return {
            'v_HK': v_HK, 'v_PGI': v_PGI, 'v_PFK': v_PFK,
            'v_ALD': v_ALD, 'v_PK': v_PK,
            'v_ox_phos': v_ox_phos, 'v_ATPase': v_ATPase
        }

    def derivatives(self, state, t, glucose_supply=0.1):
        """ODE system for glycolysis"""
        v = self.reaction_rates(state)

        Glc, G6P, F6P, FBP, PEP, Pyr, ATP, ADP, AMP, Pi = state

        # Mass balance ODEs
        d_Glc = glucose_supply - v['v_HK']
        d_G6P = v['v_HK'] - v['v_PGI']
        d_F6P = v['v_PGI'] - v['v_PFK']
        d_FBP = v['v_PFK'] - v['v_ALD']
        d_PEP = v['v_ALD'] - v['v_PK']
        d_Pyr = v['v_PK']

        # ATP/ADP/AMP dynamics
        # Glycolysis: net +2 ATP per glucose
        # HK, PFK consume ATP; later steps produce ATP
        d_ATP = (2*v['v_PK'] + v['v_ox_phos'] - v['v_HK'] -
                 v['v_PFK'] - v['v_ATPase'])
        d_ADP = -d_ATP  # Simplified
        d_AMP = 0.0     # Simplified (adenylate kinase ignored)
        d_Pi = -v['v_ox_phos'] + v['v_ATPase']

        return [d_Glc, d_G6P, d_F6P, d_FBP, d_PEP, d_Pyr,
                d_ATP, d_ADP, d_AMP, d_Pi]

    def energy_charge(self, ATP, ADP, AMP):
        """Compute adenylate energy charge"""
        return (ATP + 0.5*ADP) / (ATP + ADP + AMP + 1e-10)

    def simulate(self, initial_state, t_span, glucose_supply=0.1):
        """Simulate glycolysis pathway"""
        t = np.linspace(t_span[0], t_span[1], 1000)
        solution = odeint(self.derivatives, initial_state, t,
                         args=(glucose_supply,))

        # Calculate energy charge over time
        ec = np.array([self.energy_charge(s[6], s[7], s[8])
                      for s in solution])

        return t, solution, ec

# Example simulation
glycolysis = Glycolysis()

# Initial conditions: [Glc, G6P, F6P, FBP, PEP, Pyr, ATP, ADP, AMP, Pi]
initial = [5.0, 0.1, 0.1, 0.05, 0.05, 0.0, 3.0, 0.5, 0.05, 1.0]

t, solution, energy_charge = glycolysis.simulate(
    initial,
    t_span=[0, 60],  # 60 minutes
    glucose_supply=0.1  # mM/min
)
```

---

## 4.2 Compartmentalization Models

### 4.2.1 Multi-Compartment Systems

**Biological Context:** Cytoplasm, nucleus, mitochondria, ER - each with different concentrations

**General Framework:**

For species $X$ in compartments $i=1..N$:

$$\frac{d[X]_i}{dt} = R_i([X]_i) + \sum_{j \neq i} J_{ji}$$

Where:
- $R_i$ = reactions in compartment $i$
- $J_{ji}$ = flux from compartment $j$ to $i$

**Transport Flux Models:**

**Passive Diffusion:**
$$J_{diff} = P \cdot A \cdot ([X]_1 - [X]_2)$$

**Active Transport (Pump):**
$$J_{pump} = \frac{V_{max} [X]_1}{K_m + [X]_1} \cdot \frac{[ATP]}{K_{ATP} + [ATP]}$$

**Facilitated Diffusion:**
$$J_{fac} = \frac{V_{max} ([X]_1 - [X]_2)}{K_m + [X]_1 + [X]_2}$$

### 4.2.2 Calcium Compartments (Example)

**Cytoplasm ⇌ ER ⇌ Mitochondria**

$$\frac{d[Ca^{2+}]_{cyt}}{dt} = J_{in} - J_{SERCA} + J_{RyR} - J_{mito}$$

$$\frac{d[Ca^{2+}]_{ER}}{dt} = \frac{V_{cyt}}{V_{ER}}(J_{SERCA} - J_{RyR})$$

$$\frac{d[Ca^{2+}]_{mito}}{dt} = \frac{V_{cyt}}{V_{mito}} J_{mito}$$

**Fluxes:**

SERCA pump (cytoplasm → ER):
$$J_{SERCA} = \frac{V_{SERCA} [Ca^{2+}]_{cyt}^2}{K_{SERCA}^2 + [Ca^{2+}]_{cyt}^2}$$

RyR channel (ER → cytoplasm):
$$J_{RyR} = k_{RyR} \frac{[Ca^{2+}]_{cyt}^4}{K_{act}^4 + [Ca^{2+}]_{cyt}^4} \cdot ([Ca^{2+}]_{ER} - [Ca^{2+}]_{cyt})$$

Mitochondrial uniporter:
$$J_{mito} = \frac{V_{uni} [Ca^{2+}]_{cyt}^2}{K_{uni}^2 + [Ca^{2+}]_{cyt}^2}$$

**Parameter Ranges:**

| Parameter | Value | Units | Description |
|-----------|-------|-------|-------------|
| $[Ca^{2+}]_{cyt}$ (rest) | 0.1 | μM | Cytoplasmic calcium |
| $[Ca^{2+}]_{ER}$ | 400 | μM | ER calcium store |
| $V_{SERCA}$ | 1.0 | μM/s | SERCA max rate |
| $K_{SERCA}$ | 0.2 | μM | SERCA affinity |
| $k_{RyR}$ | 10 | s⁻¹ | RyR opening rate |

**Computational Implementation:**

```python
class CalciumCompartments:
    """Multi-compartment calcium dynamics"""

    def __init__(self):
        # Compartment volumes (relative)
        self.V_cyt = 1.0
        self.V_ER = 0.1
        self.V_mito = 0.05

        # SERCA parameters
        self.V_SERCA = 1.0    # μM/s
        self.K_SERCA = 0.2    # μM

        # RyR parameters
        self.k_RyR = 10.0     # s⁻¹
        self.K_act = 0.3      # μM

        # Mitochondrial uniporter
        self.V_uni = 0.5      # μM/s
        self.K_uni = 1.0      # μM

        # Leak rates
        self.k_leak_ER = 0.01  # s⁻¹
        self.k_leak_mito = 0.001

    def serca_flux(self, ca_cyt):
        """SERCA pump flux (cyt → ER)"""
        return self.V_SERCA * ca_cyt**2 / (self.K_SERCA**2 + ca_cyt**2)

    def ryr_flux(self, ca_cyt, ca_er):
        """RyR channel flux (ER → cyt)"""
        activation = ca_cyt**4 / (self.K_act**4 + ca_cyt**4)
        driving_force = ca_er - ca_cyt
        return self.k_RyR * activation * max(0, driving_force)

    def mito_flux(self, ca_cyt):
        """Mitochondrial uniporter flux (cyt → mito)"""
        return self.V_uni * ca_cyt**2 / (self.K_uni**2 + ca_cyt**2)

    def derivatives(self, state, t, influx=0):
        """
        State: [ca_cyt, ca_er, ca_mito]
        """
        ca_cyt, ca_er, ca_mito = state

        # Compute fluxes
        j_serca = self.serca_flux(ca_cyt)
        j_ryr = self.ryr_flux(ca_cyt, ca_er)
        j_mito = self.mito_flux(ca_cyt)
        j_leak_er = self.k_leak_ER * (ca_er - ca_cyt)

        # ODEs
        d_ca_cyt = influx - j_serca + j_ryr + j_leak_er - j_mito
        d_ca_er = (self.V_cyt / self.V_ER) * (j_serca - j_ryr - j_leak_er)
        d_ca_mito = (self.V_cyt / self.V_mito) * j_mito

        return [d_ca_cyt, d_ca_er, d_ca_mito]

    def simulate_pulse(self, initial_state, t_span,
                      pulse_time=1.0, pulse_strength=5.0):
        """Simulate with a calcium pulse"""
        t = np.linspace(t_span[0], t_span[1], 1000)

        # Create influx function
        def influx_func(time):
            if pulse_time <= time < pulse_time + 0.1:
                return pulse_strength
            return 0

        # Integrate with time-varying influx
        solution = []
        current_state = initial_state

        for i in range(len(t)-1):
            dt = t[i+1] - t[i]
            influx = influx_func(t[i])
            d_state = self.derivatives(current_state, t[i], influx)
            current_state = current_state + np.array(d_state) * dt
            solution.append(current_state)

        return t[:-1], np.array(solution)

# Example simulation
ca_system = CalciumCompartments()

# Initial: [cyt, ER, mito] in μM
initial = [0.1, 400.0, 0.1]

t, solution = ca_system.simulate_pulse(
    initial,
    t_span=[0, 10],  # 10 seconds
    pulse_time=1.0,
    pulse_strength=10.0  # μM/s
)
```

---

## 4.3 Vesicle Transport & Exocytosis

### 4.3.1 Vesicle Pool Models

**Biological Context:** Synaptic vesicle release, neurotransmitter dynamics

**Three-Pool Model:**

```
Reserve Pool → Recycling Pool → Readily Releasable Pool → Released
    k₁              k₂                k₃(Ca²⁺)
```

**ODEs:**

$$\frac{dN_R}{dt} = -k_1 N_R + k_{rec} N_{ext}$$

$$\frac{dN_C}{dt} = k_1 N_R - k_2 N_C$$

$$\frac{dN_{RRP}}{dt} = k_2 N_C - k_3([Ca^{2+}]) N_{RRP}$$

$$\frac{dN_{released}}{dt} = k_3([Ca^{2+}]) N_{RRP}$$

**Calcium-Dependent Release:**

$$k_3([Ca^{2+}]) = k_{max} \frac{[Ca^{2+}]^n}{K_d^n + [Ca^{2+}]^n}$$

**Parameter Ranges:**

| Parameter | Value | Units | Description |
|-----------|-------|-------|-------------|
| $N_{total}$ | 1000-10000 | vesicles | Total vesicles |
| $N_{RRP}$ (rest) | 10-100 | vesicles | Readily releasable |
| $k_1$ | 0.1 | s⁻¹ | Reserve mobilization |
| $k_2$ | 1.0 | s⁻¹ | Priming rate |
| $k_{max}$ | 1000 | s⁻¹ | Max release rate |
| $K_d$ | 10 | μM | Ca²⁺ sensitivity |
| $n$ | 3-5 | - | Hill coefficient |

---

# LAYER 5: Cell Layer (Self-Regulating Agents)

## Overview

Layer 5 models complete cellular systems with homeostatic regulation, ion channel dynamics, and membrane excitability - the foundation for neuronal computation.

---

## 5.1 Hodgkin-Huxley Model (Complete Formulation)

### 5.1.1 Original HH Equations

**Biological Context:** Action potential generation in squid giant axon (Nobel Prize 1963)

**Membrane Voltage Equation:**

$$C_m \frac{dV}{dt} = -I_{Na} - I_K - I_L + I_{ext}$$

**Ionic Currents:**

Sodium current:
$$I_{Na} = \bar{g}_{Na} m^3 h (V - E_{Na})$$

Potassium current:
$$I_K = \bar{g}_K n^4 (V - E_K)$$

Leak current:
$$I_L = \bar{g}_L (V - E_L)$$

**Gating Variable Dynamics:**

General form:
$$\frac{dx}{dt} = \alpha_x(V)(1-x) - \beta_x(V) x$$

Equivalent form:
$$\frac{dx}{dt} = \frac{x_\infty(V) - x}{\tau_x(V)}$$

Where:
$$x_\infty(V) = \frac{\alpha_x(V)}{\alpha_x(V) + \beta_x(V)}$$

$$\tau_x(V) = \frac{1}{\alpha_x(V) + \beta_x(V)}$$

**Voltage-Dependent Rate Constants:**

Sodium activation ($m$):
$$\alpha_m(V) = \frac{0.1(V+40)}{1 - \exp(-(V+40)/10)}$$
$$\beta_m(V) = 4 \exp(-(V+65)/18)$$

Sodium inactivation ($h$):
$$\alpha_h(V) = 0.07 \exp(-(V+65)/20)$$
$$\beta_h(V) = \frac{1}{1 + \exp(-(V+35)/10)}$$

Potassium activation ($n$):
$$\alpha_n(V) = \frac{0.01(V+55)}{1 - \exp(-(V+55)/10)}$$
$$\beta_n(V) = 0.125 \exp(-(V+65)/80)$$

**Parameter Values (Original HH, Squid Axon, 6.3°C):**

| Parameter | Value | Units |
|-----------|-------|-------|
| $C_m$ | 1.0 | μF/cm² |
| $\bar{g}_{Na}$ | 120 | mS/cm² |
| $\bar{g}_K$ | 36 | mS/cm² |
| $\bar{g}_L$ | 0.3 | mS/cm² |
| $E_{Na}$ | +50 | mV |
| $E_K$ | -77 | mV |
| $E_L$ | -54.4 | mV |
| $V_{rest}$ | -65 | mV |

### 5.1.2 Temperature Dependence (Q₁₀)

**Temperature Scaling:**

$$\tau_x(V, T) = \frac{\tau_x(V, T_0)}{Q_{10}^{(T-T_0)/10}}$$

Typical $Q_{10}$ values:
- Ionic currents: 2-3
- Gates: 2.5-3.5

**Computational Implementation:**

```python
class HodgkinHuxley:
    """Complete Hodgkin-Huxley neuron model"""

    def __init__(self, temperature=6.3):
        # Membrane capacitance
        self.C_m = 1.0  # μF/cm²

        # Maximum conductances
        self.g_Na = 120.0  # mS/cm²
        self.g_K = 36.0    # mS/cm²
        self.g_L = 0.3     # mS/cm²

        # Reversal potentials
        self.E_Na = 50.0   # mV
        self.E_K = -77.0   # mV
        self.E_L = -54.4   # mV

        # Temperature
        self.T = temperature
        self.T_ref = 6.3   # Reference temperature (°C)
        self.Q10 = 3.0     # Temperature coefficient

        # Compute temperature factor
        self.phi = self.Q10**((self.T - self.T_ref) / 10.0)

    def alpha_m(self, V):
        """Sodium activation rate"""
        return 0.1 * (V + 40.0) / (1.0 - np.exp(-(V + 40.0) / 10.0))

    def beta_m(self, V):
        """Sodium activation rate"""
        return 4.0 * np.exp(-(V + 65.0) / 18.0)

    def alpha_h(self, V):
        """Sodium inactivation rate"""
        return 0.07 * np.exp(-(V + 65.0) / 20.0)

    def beta_h(self, V):
        """Sodium inactivation rate"""
        return 1.0 / (1.0 + np.exp(-(V + 35.0) / 10.0))

    def alpha_n(self, V):
        """Potassium activation rate"""
        return 0.01 * (V + 55.0) / (1.0 - np.exp(-(V + 55.0) / 10.0))

    def beta_n(self, V):
        """Potassium activation rate"""
        return 0.125 * np.exp(-(V + 65.0) / 80.0)

    def m_inf(self, V):
        """Steady-state sodium activation"""
        return self.alpha_m(V) / (self.alpha_m(V) + self.beta_m(V))

    def h_inf(self, V):
        """Steady-state sodium inactivation"""
        return self.alpha_h(V) / (self.alpha_h(V) + self.beta_h(V))

    def n_inf(self, V):
        """Steady-state potassium activation"""
        return self.alpha_n(V) / (self.alpha_n(V) + self.beta_n(V))

    def I_Na(self, V, m, h):
        """Sodium current"""
        return self.g_Na * m**3 * h * (V - self.E_Na)

    def I_K(self, V, n):
        """Potassium current"""
        return self.g_K * n**4 * (V - self.E_K)

    def I_L(self, V):
        """Leak current"""
        return self.g_L * (V - self.E_L)

    def derivatives(self, state, t, I_ext):
        """
        State vector: [V, m, h, n]
        """
        V, m, h, n = state

        # Gating variable derivatives (with temperature scaling)
        dm_dt = self.phi * (self.alpha_m(V)*(1-m) - self.beta_m(V)*m)
        dh_dt = self.phi * (self.alpha_h(V)*(1-h) - self.beta_h(V)*h)
        dn_dt = self.phi * (self.alpha_n(V)*(1-n) - self.beta_n(V)*n)

        # Membrane voltage derivative
        dV_dt = (I_ext(t) - self.I_Na(V, m, h) -
                 self.I_K(V, n) - self.I_L(V)) / self.C_m

        return [dV_dt, dm_dt, dh_dt, dn_dt]

    def steady_state(self, V_hold=-65):
        """Compute steady-state gating at holding potential"""
        return [V_hold,
                self.m_inf(V_hold),
                self.h_inf(V_hold),
                self.n_inf(V_hold)]

    def simulate(self, t_span, I_ext, initial_state=None):
        """
        Simulate HH neuron

        Parameters:
        -----------
        t_span : tuple
            (t_start, t_end) in ms
        I_ext : callable or float
            External current (μA/cm²)
        initial_state : list, optional
            [V, m, h, n] initial conditions
        """
        if initial_state is None:
            initial_state = self.steady_state()

        # Make I_ext callable if it's a constant
        if not callable(I_ext):
            I_ext_const = I_ext
            I_ext = lambda t: I_ext_const

        t = np.linspace(t_span[0], t_span[1], int((t_span[1]-t_span[0])*10))
        solution = odeint(self.derivatives, initial_state, t, args=(I_ext,))

        return t, solution

    def spike_detection(self, t, V, threshold=-20):
        """Detect action potential times"""
        spikes = []
        above_threshold = V > threshold

        for i in range(1, len(above_threshold)):
            if above_threshold[i] and not above_threshold[i-1]:
                spikes.append(t[i])

        return np.array(spikes)

# Example: Generate action potential
hh = HodgkinHuxley(temperature=20)  # Room temperature

# Current pulse: 10 μA/cm² for 1 ms at t=10 ms
def current_pulse(t):
    if 10 <= t < 11:
        return 10.0
    return 0.0

# Simulate
t, solution = hh.simulate([0, 50], current_pulse)
V, m, h, n = solution.T

# Detect spikes
spike_times = hh.spike_detection(t, V)
print(f"Action potential at: {spike_times} ms")
```

---

## 5.2 Extended Neuron Models

### 5.2.1 Morris-Lecar Model (2D Reduction)

**Biological Context:** Simplified model capturing basic excitability with 2 variables

**Equations:**

$$C \frac{dV}{dt} = I_{ext} - g_{Ca} m_\infty(V)(V - E_{Ca}) - g_K w(V - E_K) - g_L(V - E_L)$$

$$\frac{dw}{dt} = \frac{w_\infty(V) - w}{\tau_w(V)}$$

**Steady-State Functions:**

$$m_\infty(V) = 0.5(1 + \tanh((V - V_1)/V_2))$$

$$w_\infty(V) = 0.5(1 + \tanh((V - V_3)/V_4))$$

$$\tau_w(V) = 1 / \cosh((V - V_3)/(2V_4))$$

**Parameter Sets:**

Class I excitability:
- $V_1 = -1.2$ mV, $V_2 = 18$ mV
- $V_3 = 2$ mV, $V_4 = 30$ mV
- $g_{Ca} = 4.4$ mS/cm², $g_K = 8$ mS/cm²

Class II excitability:
- $V_1 = -1.2$ mV, $V_2 = 18$ mV
- $V_3 = 12$ mV, $V_4 = 17.4$ mV
- $g_{Ca} = 4$ mS/cm², $g_K = 8$ mS/cm²

### 5.2.2 Izhikevich Model (Computationally Efficient)

**Biological Context:** Captures diverse spiking patterns with computational efficiency

**Equations:**

$$\frac{dv}{dt} = 0.04v^2 + 5v + 140 - u + I$$

$$\frac{du}{dt} = a(bv - u)$$

**Reset Conditions:**
```
if v ≥ 30 mV:
    v ← c
    u ← u + d
```

**Parameters for Different Cell Types:**

| Type | $a$ | $b$ | $c$ | $d$ | Behavior |
|------|-----|-----|-----|-----|----------|
| Regular spiking | 0.02 | 0.2 | -65 | 8 | Cortical pyramidal |
| Intrinsically bursting | 0.02 | 0.2 | -55 | 4 | Cortical chattering |
| Chattering | 0.02 | 0.2 | -50 | 2 | Burst firing |
| Fast spiking | 0.1 | 0.2 | -65 | 2 | Cortical interneurons |
| Low-threshold spiking | 0.02 | 0.25 | -65 | 2 | Thalamic |
| Resonator | 0.1 | 0.26 | -65 | 2 | Subthreshold oscillations |

**Computational Implementation:**

```python
class IzhikevichNeuron:
    """Efficient spiking neuron model with diverse behaviors"""

    def __init__(self, a=0.02, b=0.2, c=-65, d=8):
        self.a = a  # Time scale of recovery variable
        self.b = b  # Sensitivity of recovery to V
        self.c = c  # After-spike reset value of V
        self.d = d  # After-spike increment of u

        self.v_threshold = 30  # mV

    def derivatives(self, state, t, I_ext):
        """State: [v, u]"""
        v, u = state

        dv_dt = 0.04*v**2 + 5*v + 140 - u + I_ext(t)
        du_dt = self.a * (self.b*v - u)

        return [dv_dt, du_dt]

    def simulate(self, t_span, I_ext, dt=0.1):
        """
        Simulate with spike reset

        Uses Euler method with reset to handle discontinuity
        """
        t = np.arange(t_span[0], t_span[1], dt)
        v = np.zeros(len(t))
        u = np.zeros(len(t))
        spikes = []

        # Initial conditions
        v[0] = self.c
        u[0] = self.b * v[0]

        # Make I_ext callable
        if not callable(I_ext):
            I_const = I_ext
            I_ext = lambda t: I_const

        for i in range(len(t) - 1):
            # Check for spike
            if v[i] >= self.v_threshold:
                v[i] = self.v_threshold  # For plotting
                spikes.append(t[i])
                v[i+1] = self.c
                u[i+1] = u[i] + self.d
            else:
                # Euler integration
                dv, du = self.derivatives([v[i], u[i]], t[i], I_ext)
                v[i+1] = v[i] + dv * dt
                u[i+1] = u[i] + du * dt

        return t, v, u, np.array(spikes)

    @staticmethod
    def preset_params(neuron_type):
        """Get preset parameters for common neuron types"""
        presets = {
            'RS': (0.02, 0.2, -65, 8),      # Regular spiking
            'IB': (0.02, 0.2, -55, 4),      # Intrinsically bursting
            'CH': (0.02, 0.2, -50, 2),      # Chattering
            'FS': (0.1, 0.2, -65, 2),       # Fast spiking
            'LTS': (0.02, 0.25, -65, 2),    # Low threshold spiking
            'RZ': (0.1, 0.26, -65, 2)       # Resonator
        }
        return presets.get(neuron_type, (0.02, 0.2, -65, 8))

# Example: Compare different neuron types
import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 2, figsize=(12, 10))
neuron_types = ['RS', 'IB', 'CH', 'FS', 'LTS', 'RZ']

for idx, ntype in enumerate(neuron_types):
    ax = axes[idx // 2, idx % 2]

    # Create neuron
    params = IzhikevichNeuron.preset_params(ntype)
    neuron = IzhikevichNeuron(*params)

    # Step current
    I_ext = lambda t: 10 if t > 100 else 0

    # Simulate
    t, v, u, spikes = neuron.simulate([0, 300], I_ext, dt=0.25)

    # Plot
    ax.plot(t, v, 'b-', linewidth=1)
    ax.axhline(-70, color='k', linestyle='--', alpha=0.3)
    ax.set_title(f'{ntype} Neuron')
    ax.set_ylabel('V (mV)')
    if idx >= 4:
        ax.set_xlabel('Time (ms)')

    ax.text(250, 20, f'{len(spikes)} spikes',
            bbox=dict(boxstyle='round', facecolor='wheat'))

plt.tight_layout()
# plt.savefig('izhikevich_neuron_types.png', dpi=150)
```

---

## 5.3 Homeostatic Regulation

### 5.3.1 Calcium Homeostasis

**Biological Context:** Cells maintain tight Ca²⁺ control (~100 nM resting)

**Comprehensive Model:**

$$\frac{d[Ca^{2+}]}{dt} = J_{in} - J_{pump} + J_{release} - J_{buffer}$$

**Components:**

Influx (voltage-gated channels):
$$J_{in} = g_{Ca} m^2 h (V - E_{Ca})$$

PMCA pump (plasma membrane):
$$J_{pump} = \frac{V_{pump} [Ca^{2+}]^2}{K_p^2 + [Ca^{2+}]^2}$$

Internal release (IP₃ receptor):
$$J_{release} = k_{rel} \frac{[IP_3]^3}{K_{IP3}^3 + [IP_3]^3} \cdot \frac{[Ca^{2+}]^2}{K_{act}^2 + [Ca^{2+}]^2} \cdot ([Ca_{ER}] - [Ca])$$

Buffering:
$$\frac{d[CaB]}{dt} = k_{on}[Ca][B_{free}] - k_{off}[CaB]$$

### 5.3.2 pH Regulation

**Biological Context:** Maintain pH ~7.2 intracellularly

**Buffering Equation:**

$$\frac{d[H^+]}{dt} = J_{production} - J_{transport} - J_{buffer}$$

**Transporters:**

Na⁺/H⁺ exchanger (NHE):
$$J_{NHE} = V_{max} \frac{[H^+]_{in} - [H^+]_{out}}{K_m + [H^+]_{in}}$$

H⁺-ATPase:
$$J_{ATPase} = V_{max} \frac{[H^+][ATP]}{(K_{H} + [H^+])(K_{ATP} + [ATP])}$$

---

## 5.4 Cell Cycle & Growth Control

### 5.4.1 Simplified Cell Cycle Model

**Biological Context:** G1 → S → G2 → M phases

**Tyson Model (Minimal):**

$$\frac{d[Cyclin]}{dt} = k_{syn} - k_{deg}[Cyclin][CDK_{active}]$$

$$[CDK_{active}] = \frac{[Cyclin]^n}{K_m^n + [Cyclin]^n}$$

**Oscillatory Regime:**

When $k_{syn} > k_{deg} K_m$, system shows limit cycle oscillations representing cell cycle.

**Period:**
$$T_{cycle} \approx 2\pi \sqrt{\frac{1}{k_{syn} k_{deg}}}$$

**Computational Implementation:**

```python
class CellCycle:
    """Minimal cell cycle oscillator (Tyson model)"""

    def __init__(self, k_syn=0.015, k_deg=1.0, Km=0.5, n=4):
        self.k_syn = k_syn    # Cyclin synthesis rate
        self.k_deg = k_deg    # Degradation rate
        self.Km = Km          # Michaelis constant
        self.n = n            # Hill coefficient

    def cdk_active(self, cyclin):
        """Active CDK fraction"""
        return cyclin**self.n / (self.Km**self.n + cyclin**self.n)

    def derivatives(self, state, t):
        """State: [cyclin]"""
        cyclin = state[0]
        cdk_act = self.cdk_active(cyclin)

        d_cyclin = self.k_syn - self.k_deg * cyclin * cdk_act

        return [d_cyclin]

    def simulate(self, t_span, initial_cyclin=0.1):
        """Simulate cell cycle"""
        t = np.linspace(t_span[0], t_span[1], 5000)
        solution = odeint(self.derivatives, [initial_cyclin], t)

        return t, solution[:, 0]

    def period(self):
        """Estimate oscillation period"""
        return 2 * np.pi * np.sqrt(1 / (self.k_syn * self.k_deg))

# Example
cell_cycle = CellCycle(k_syn=0.02, k_deg=1.0)
t, cyclin = cell_cycle.simulate([0, 200])

print(f"Theoretical period: {cell_cycle.period():.1f} time units")
```

---

# Integration & Composition to Layer 6

## How Layers 3-5 Compose into Layer 6 (Neuron Types)

**Layer 6** combines the molecular (Layer 3), organelle (Layer 4), and cellular (Layer 5) mechanisms into complete, functional neuron types.

### Integration Hierarchy:

```
Layer 6: Complete Neuron Types
    ↑
    ├─ Layer 5: Cell-Level Regulation
    │   ├─ Hodgkin-Huxley dynamics (membrane excitability)
    │   ├─ Homeostatic control (Ca²⁺, pH, energy)
    │   └─ Feedback control systems
    │
    ├─ Layer 4: Organelle Function
    │   ├─ ATP generation (mitochondria)
    │   ├─ Ca²⁺ stores (ER)
    │   ├─ Vesicle pools (synaptic transmission)
    │   └─ Protein synthesis (ribosomes)
    │
    └─ Layer 3: Molecular Components
        ├─ Ion channel gating (Markov models)
        ├─ Enzyme kinetics (metabolic flux)
        ├─ Binding kinetics (receptor activation)
        └─ Reaction networks (signaling cascades)
```

### Complete Pyramidal Neuron Model (Layer 6)

```python
class PyramidalNeuron:
    """
    Complete pyramidal neuron integrating Layers 3-5

    Components:
    - Layer 3: Channel gating, enzyme kinetics
    - Layer 4: Energy metabolism, Ca²⁺ stores
    - Layer 5: Membrane excitability, homeostasis
    """

    def __init__(self):
        # Layer 5: Hodgkin-Huxley membrane
        self.hh = HodgkinHuxley(temperature=37)

        # Layer 4: Metabolic system
        self.metabolism = Glycolysis()
        self.calcium_stores = CalciumCompartments()

        # Layer 3: Ion channels
        self.na_channel = MarkovChannel(3, ['C', 'O', 'I'])
        self.k_channel = MarkovChannel(2, ['C', 'O'])

        # State variables
        self.state = {
            'V': -65,           # Membrane voltage (mV)
            'm': 0.05, 'h': 0.6, 'n': 0.32,  # HH gates
            'ATP': 3.0,         # ATP concentration (mM)
            'ADP': 0.5,         # ADP concentration (mM)
            'Ca_cyt': 0.1,      # Cytoplasmic Ca²⁺ (μM)
            'Ca_ER': 400,       # ER Ca²⁺ (μM)
            'glucose': 5.0,     # Glucose (mM)
        }

    def energy_dependent_pumps(self):
        """Layer 4: ATP-dependent ion pumps"""
        atp_factor = self.state['ATP'] / (self.state['ATP'] + 0.5)

        # Na⁺/K⁺-ATPase
        na_k_pump = 20 * atp_factor  # Current density (μA/cm²)

        # Ca²⁺-ATPase (PMCA)
        ca_pump = 5 * atp_factor

        # ATP consumption
        atp_consumption = (na_k_pump + ca_pump) / 100

        return na_k_pump, ca_pump, atp_consumption

    def metabolic_coupling(self, firing_rate):
        """Layer 4: Energy production matches demand"""
        # Increased firing → increased ATP demand
        base_consumption = 0.1  # mM/s
        activity_consumption = 0.5 * firing_rate

        total_consumption = base_consumption + activity_consumption

        # Glucose metabolism responds to ATP/ADP ratio
        energy_charge = (self.state['ATP'] + 0.5*self.state['ADP']) / 4.5

        if energy_charge < 0.8:
            # Low energy: increase glycolysis
            glucose_flux = 0.2
        else:
            # High energy: reduce glycolysis
            glucose_flux = 0.05

        return glucose_flux, total_consumption

    def update(self, dt, I_ext, synaptic_input=0):
        """
        Complete neuron update integrating all layers

        Parameters:
        -----------
        dt : float
            Time step (ms)
        I_ext : float
            External current (μA/cm²)
        synaptic_input : float
            Synaptic conductance changes
        """
        # Layer 5: Membrane dynamics
        hh_state = [self.state['V'], self.state['m'],
                    self.state['h'], self.state['n']]

        # Compute pump currents (Layer 4)
        na_k_pump, ca_pump, atp_used_pumps = self.energy_dependent_pumps()

        # Total current
        I_total = I_ext + synaptic_input - na_k_pump

        # Update HH dynamics
        derivatives = self.hh.derivatives(hh_state, 0, lambda t: I_total)

        self.state['V'] += derivatives[0] * dt
        self.state['m'] += derivatives[1] * dt
        self.state['h'] += derivatives[2] * dt
        self.state['n'] += derivatives[3] * dt

        # Detect spike
        spike = self.state['V'] > 0

        # Layer 4: Calcium dynamics
        if spike:
            ca_influx = 10.0  # μM (calcium entry during spike)
        else:
            ca_influx = 0.0

        # Update calcium
        ca_derivatives = self.calcium_stores.derivatives(
            [self.state['Ca_cyt'], self.state['Ca_ER'], 0],
            0, ca_influx
        )
        self.state['Ca_cyt'] += ca_derivatives[0] * dt / 1000  # ms→s
        self.state['Ca_ER'] += ca_derivatives[1] * dt / 1000

        # Layer 4: Energy metabolism
        firing_rate = 100 if spike else 0  # Hz
        glucose_flux, atp_consumption = self.metabolic_coupling(firing_rate)

        # Simplified ATP dynamics
        atp_production = glucose_flux * 2  # 2 ATP per glucose
        total_atp_use = atp_consumption + atp_used_pumps

        self.state['ATP'] += (atp_production - total_atp_use) * dt / 1000
        self.state['ADP'] += (total_atp_use - atp_production) * dt / 1000

        # Homeostatic constraints (Layer 5)
        self.state['ATP'] = np.clip(self.state['ATP'], 0.1, 5.0)
        self.state['ADP'] = np.clip(self.state['ADP'], 0.1, 2.0)
        self.state['Ca_cyt'] = np.clip(self.state['Ca_cyt'], 0.05, 10.0)

        return spike

    def simulate(self, t_span, I_ext, dt=0.01):
        """Full simulation of integrated neuron"""
        t = np.arange(t_span[0], t_span[1], dt)

        # Make I_ext callable
        if not callable(I_ext):
            I_const = I_ext
            I_ext = lambda t: I_const

        # Storage
        voltage = np.zeros(len(t))
        atp = np.zeros(len(t))
        calcium = np.zeros(len(t))
        spikes = []

        for i, time in enumerate(t):
            spike = self.update(dt, I_ext(time))

            voltage[i] = self.state['V']
            atp[i] = self.state['ATP']
            calcium[i] = self.state['Ca_cyt']

            if spike:
                spikes.append(time)

        return {
            't': t,
            'V': voltage,
            'ATP': atp,
            'Ca': calcium,
            'spikes': np.array(spikes)
        }

# Example: Integrated neuron simulation
neuron = PyramidalNeuron()

# Pulse current
def current_pulse(t):
    if 50 <= t < 100:
        return 15
    return 0

# Simulate
result = neuron.simulate([0, 200], current_pulse, dt=0.01)

print(f"Generated {len(result['spikes'])} spikes")
print(f"Final ATP: {result['ATP'][-1]:.2f} mM")
print(f"Final Ca²⁺: {result['Ca'][-1]:.3f} μM")
```

---

# Computational Implementation Guide

## Performance Optimization Strategies

### 1. Stiff ODE Solvers

Many biological systems have multiple timescales (stiff systems):

```python
from scipy.integrate import solve_ivp

def solve_stiff_ode(derivatives, initial_state, t_span, params):
    """
    Use for systems with widely separated timescales
    (e.g., fast channel gating + slow metabolism)
    """
    solution = solve_ivp(
        derivatives,
        t_span,
        initial_state,
        method='LSODA',  # Switches between stiff/non-stiff automatically
        args=params,
        dense_output=True,
        rtol=1e-6,
        atol=1e-9
    )
    return solution
```

### 2. Vectorization for Networks

```python
class NeuronPopulation:
    """Vectorized simulation of neuron population"""

    def __init__(self, n_neurons, neuron_params):
        self.n = n_neurons

        # Vectorized state: shape (n_neurons, n_state_vars)
        self.state = np.zeros((n_neurons, 4))  # [V, m, h, n]

        # Initialize at resting state
        for i in range(n_neurons):
            self.state[i, :] = [-65, 0.05, 0.6, 0.32]

    def update_vectorized(self, dt, I_ext):
        """
        Update all neurons simultaneously
        Exploits SIMD and cache locality
        """
        V = self.state[:, 0]
        m = self.state[:, 1]
        h = self.state[:, 2]
        n = self.state[:, 3]

        # Vectorized rate functions (using numpy broadcasting)
        alpha_m = 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))
        beta_m = 4 * np.exp(-(V + 65) / 18)
        # ... (other rates)

        # Vectorized updates
        dm = dt * (alpha_m * (1 - m) - beta_m * m)
        # ... (other gate updates)

        self.state[:, 1] += dm
        # ... (other state updates)
```

### 3. GPU Acceleration

```python
try:
    import cupy as cp  # CUDA arrays

    class GPUNeuronPopulation:
        """GPU-accelerated neuron simulation"""

        def __init__(self, n_neurons):
            # Allocate on GPU
            self.state = cp.zeros((n_neurons, 4))
            self.state[:, 0] = -65  # V
            self.state[:, 1] = 0.05  # m
            # ...

        def update_gpu(self, dt, I_ext):
            """All operations on GPU"""
            V = self.state[:, 0]

            # GPU kernel operations
            alpha_m = 0.1 * (V + 40) / (1 - cp.exp(-(V + 40) / 10))
            # ...

            # Update in place on GPU
            self.state[:, 1] += dt * (alpha_m * (1 - self.state[:, 1]) -
                                     beta_m * self.state[:, 1])

except ImportError:
    print("CuPy not available, using CPU")
```

### 4. Adaptive Time Stepping

```python
class AdaptiveSimulator:
    """Adaptive time step for efficiency"""

    def __init__(self, model, tol=1e-4):
        self.model = model
        self.tol = tol
        self.dt_min = 0.001
        self.dt_max = 1.0

    def estimate_error(self, state, dt):
        """Estimate local truncation error"""
        # Full step
        state_full = self.model.step(state, dt)

        # Two half steps
        state_half = self.model.step(state, dt/2)
        state_double = self.model.step(state_half, dt/2)

        # Error estimate
        error = np.max(np.abs(state_full - state_double))

        return error

    def adapt_step(self, state, dt):
        """Adjust time step based on error"""
        error = self.estimate_error(state, dt)

        if error < self.tol / 10:
            # Error very small, increase dt
            dt_new = min(dt * 1.5, self.dt_max)
        elif error > self.tol:
            # Error too large, decrease dt
            dt_new = max(dt * 0.5, self.dt_min)
        else:
            dt_new = dt

        return dt_new
```

---

# Complete Code Examples

## Example 1: Multi-Scale Integration

```python
class MultiScaleCell:
    """
    Complete example: molecular → organelle → cell
    Demonstrates Layer 3 → 4 → 5 integration
    """

    def __init__(self):
        # Layer 3: Receptor binding
        self.receptor_binding = CooperativeBinding(
            kd=1e-6, hill_coef=2, k_plus=1e7, k_minus=10
        )

        # Layer 3: Enzyme (signal amplification)
        self.enzyme = MichaelisMenten(
            km=1e-4, vmax=1e-7, k1=1e6, k_minus1=10, k2=100
        )

        # Layer 4: Metabolism
        self.metabolism = Glycolysis()

        # Layer 5: Excitability
        self.excitability = HodgkinHuxley()

        # State
        self.state = {
            # Layer 3
            'ligand': 0,
            'receptor_occupied': 0,
            'second_messenger': 0,

            # Layer 4
            'ATP': 3.0,
            'glucose': 5.0,

            # Layer 5
            'V': -65,
            'm': 0.05, 'h': 0.6, 'n': 0.32
        }

    def update(self, dt, ligand_input):
        """Integrate across all layers"""

        # LAYER 3: Receptor activation
        # Ligand binds to receptor
        _, theta = self.receptor_binding.simulate(
            ligand_conc=ligand_input,
            t_span=[0, dt],
            theta_0=self.state['receptor_occupied']
        )
        self.state['receptor_occupied'] = theta[-1]

        # Receptor activates enzyme (second messenger production)
        enzyme_activation = 10 * self.state['receptor_occupied']
        second_messenger_production = self.enzyme.velocity(enzyme_activation)
        self.state['second_messenger'] += second_messenger_production * dt

        # LAYER 4: Metabolism responds to signaling
        # Second messenger increases glucose uptake
        glucose_supply = 0.1 * (1 + self.state['second_messenger'])

        # Simulate metabolism
        metab_state = [self.state['glucose'], 0.1, 0.1, 0.05, 0.05, 0,
                      self.state['ATP'], 0.5, 0.05, 1.0]
        _, metab_solution, _ = self.metabolism.simulate(
            metab_state, [0, dt], glucose_supply
        )
        self.state['ATP'] = metab_solution[-1, 6]

        # LAYER 5: ATP-dependent excitability
        # ATP level modulates ion pumps
        atp_factor = self.state['ATP'] / (self.state['ATP'] + 0.5)
        pump_current = -20 * atp_factor  # Na/K pump

        # Membrane excitability
        hh_state = [self.state['V'], self.state['m'],
                   self.state['h'], self.state['n']]

        I_total = pump_current + self.state['second_messenger'] * 5

        derivatives = self.excitability.derivatives(
            hh_state, 0, lambda t: I_total
        )

        self.state['V'] += derivatives[0] * dt
        self.state['m'] += derivatives[1] * dt
        self.state['h'] += derivatives[2] * dt
        self.state['n'] += derivatives[3] * dt

        # Decay second messenger
        self.state['second_messenger'] *= np.exp(-dt / 10)

        return self.state['V'] > 0  # Return spike

# Run multi-scale simulation
cell = MultiScaleCell()

t_total = 100  # ms
dt = 0.01
n_steps = int(t_total / dt)

# Apply ligand pulse at t=20 ms
for i in range(n_steps):
    t = i * dt
    ligand = 10e-6 if 20 <= t < 25 else 0

    spike = cell.update(dt, ligand)

    if spike:
        print(f"Spike at t={t:.1f} ms")
```

## Example 2: Network Simulation

```python
class NeuronNetwork:
    """
    Network of integrated neurons with synaptic connections
    """

    def __init__(self, n_neurons, connectivity=0.1):
        self.n = n_neurons

        # Create neurons
        self.neurons = [PyramidalNeuron() for _ in range(n_neurons)]

        # Create connectivity matrix
        self.W = np.random.rand(n_neurons, n_neurons) < connectivity
        np.fill_diagonal(self.W, 0)  # No self-connections

        # Synaptic weights
        self.weights = np.random.randn(n_neurons, n_neurons) * 0.5
        self.weights[~self.W] = 0

    def synaptic_input(self, neuron_idx, spike_history):
        """Compute synaptic input from network"""
        # Simple model: sum of weighted recent spikes
        synaptic_current = 0

        for pre in range(self.n):
            if self.W[pre, neuron_idx] and spike_history[pre]:
                synaptic_current += self.weights[pre, neuron_idx] * 10

        return synaptic_current

    def simulate(self, t_span, I_ext_func, dt=0.01):
        """Simulate network dynamics"""
        t = np.arange(t_span[0], t_span[1], dt)

        # Storage
        voltage = np.zeros((len(t), self.n))
        spike_history = np.zeros(self.n, dtype=bool)
        spike_times = [[] for _ in range(self.n)]

        for i, time in enumerate(t):
            # Update each neuron
            for j, neuron in enumerate(self.neurons):
                # External + synaptic input
                I_ext = I_ext_func(time, j)
                I_syn = self.synaptic_input(j, spike_history)

                spike = neuron.update(dt, I_ext, I_syn)

                voltage[i, j] = neuron.state['V']
                spike_history[j] = spike

                if spike:
                    spike_times[j].append(time)

        return {
            't': t,
            'V': voltage,
            'spikes': spike_times
        }

# Example: Create small network
network = NeuronNetwork(n_neurons=10, connectivity=0.2)

# External input to first neuron only
def ext_input(t, neuron_idx):
    if neuron_idx == 0 and 50 <= t < 60:
        return 15
    return 0

# Simulate
result = network.simulate([0, 200], ext_input)

# Analyze
for i in range(10):
    print(f"Neuron {i}: {len(result['spikes'][i])} spikes")
```

---

# References & Further Reading

## Mathematical Biology

1. **Murray, J.D.** (2002). *Mathematical Biology I: An Introduction*. Springer.
2. **Keener, J. & Sneyd, J.** (2009). *Mathematical Physiology*. Springer.
3. **Fall, C.P., et al.** (2002). *Computational Cell Biology*. Springer.

## Neuroscience

4. **Dayan, P. & Abbott, L.F.** (2001). *Theoretical Neuroscience*. MIT Press.
5. **Izhikevich, E.M.** (2007). *Dynamical Systems in Neuroscience*. MIT Press.
6. **Gerstner, W., et al.** (2014). *Neuronal Dynamics*. Cambridge University Press.

## Biochemistry & Metabolism

7. **Alon, U.** (2007). *An Introduction to Systems Biology*. Chapman & Hall.
8. **Voit, E.O.** (2013). *Biochemical Systems Theory*. Cambridge University Press.

## Computational Methods

9. **Hairer, E. & Wanner, G.** (1996). *Solving Ordinary Differential Equations II: Stiff Problems*. Springer.
10. **Ermentrout, B. & Terman, D.H.** (2010). *Mathematical Foundations of Neuroscience*. Springer.

---

# Appendix: Parameter Tables

## Complete HH Parameters (Mammalian, 37°C)

| Parameter | Value | Units | Source |
|-----------|-------|-------|--------|
| $C_m$ | 1.0 | μF/cm² | Standard |
| $\bar{g}_{Na}$ | 120 | mS/cm² | Hodgkin & Huxley 1952 |
| $\bar{g}_K$ | 36 | mS/cm² | Hodgkin & Huxley 1952 |
| $\bar{g}_L$ | 0.3 | mS/cm² | Hodgkin & Huxley 1952 |
| $E_{Na}$ | +55 | mV | Nernst equation |
| $E_K$ | -77 | mV | Nernst equation |
| $E_L$ | -54.4 | mV | Measured |

## Metabolic Parameters (Typical Neuron)

| Parameter | Resting | Active | Units |
|-----------|---------|--------|-------|
| ATP consumption | 0.1 | 0.5 | mM/s |
| Glucose uptake | 0.05 | 0.2 | mM/s |
| O₂ consumption | 0.1 | 0.4 | mM/s |
| Lactate production | 0.02 | 0.1 | mM/s |

---

**End of Document**

This comprehensive reference provides complete mathematical formulations, parameter ranges, computational implementations, and integration strategies for BioAI Layers 3-5, enabling construction of Layer 6 neuron types and beyond.
