# Drosophila Compartmental Neuron Model (Gouwens & Wilson 2009)

**Source:** J Neurosci (2009) - "Signal propagation in Drosophila central neurons"
**DOI:** https://pmc.ncbi.nlm.nih.gov/articles/PMC2709801/
**Model Type:** Multi-compartment cable theory
**Implementation:** NEURON simulator
**Code:** https://github.com/ModelDBRepository/118662

---

## Cable Theory Equations

### Core Geometry-Independent Parameters

**Intracellular resistance:**
```
r_i = R_i · l / A
```

**Membrane resistance:**
```
r_m = R_m / a
```

**Membrane capacitance:**
```
c_m = C_m · a
```

Where:
- **l** = segment length (µm)
- **A** = cross-sectional area (µm²)
- **a** = surface area (µm²)
- **R_i** = specific intracellular resistivity (Ω·cm)
- **R_m** = specific membrane resistance (kΩ·cm²)
- **C_m** = specific membrane capacitance (µF·cm⁻²)

---

## Fitted Membrane Parameters

Measurements from 3 antennal lobe projection neurons (PNs) innervating glomerulus DM1:

| Cell | R_m (kΩ·cm²) | C_m (µF·cm⁻²) | R_i (Ω·cm) |
|------|--------------|----------------|-----------|
| **1** | 8.3 | 2.6 | 163.9 |
| **2** | 20.4 | 1.5 | 102.5 |
| **3** | 20.8 | 0.8 | 266.1 |

**Mean values:**
- **R_m:** 16.5 ± 7.1 kΩ·cm²
- **C_m:** 1.6 ± 0.9 µF·cm⁻²
- **R_i:** 177.5 ± 84.3 Ω·cm

---

## Electrophysiological Measurements

### Input Properties
- **Input resistance (Rin):** 598.0 ± 69.3 MΩ
- **Seal resistance (Rseal):** 10.1 ± 1.6 GΩ
- **Resting potential (corrected):** -55 to -60 mV
- **Depolarization artifact:** ~10 mV upon whole-cell configuration

### Voltage Attenuation
- Neurons are **electrotonically extensive**
- Somatic recording electrode **imperfectly controls voltage** in dendrites and axon
- Action potentials initiate in **proximal axon**, not soma

---

## Cable Equation (Passive Membrane)

For a cylindrical cable segment:

```
C_m · ∂V/∂t = (1/(r_i + r_e)) · ∂²V/∂x² - (V - V_rest) / r_m + I_ext
```

**Simplified (r_e ≈ 0):**
```
C_m · ∂V/∂t = (1/r_i) · ∂²V/∂x² - (V - V_rest) / r_m + I_ext
```

Where:
- **V(x,t)** = membrane potential at position x and time t
- **V_rest** = resting potential
- **C_m** = membrane capacitance per unit length
- **r_i** = intracellular resistance per unit length
- **r_m** = membrane resistance per unit length
- **r_e** = extracellular resistance (typically negligible)
- **I_ext** = external current injection

---

## Compartmental Discretization

The continuous cable is divided into **N discrete compartments**, each governed by:

```
C_m · dV_i/dt = (V_{i-1} - V_i) / R_{i-1,i} + (V_{i+1} - V_i) / R_{i,i+1}
                - (V_i - V_rest) / R_m,i + I_ext,i
```

Where:
- **V_i** = voltage of compartment i
- **R_{i-1,i}** = axial resistance between compartments i-1 and i
- **R_{i,i+1}** = axial resistance between compartments i and i+1
- **R_m,i** = membrane resistance of compartment i

---

## Steady-State Voltage Attenuation

At steady state (dV/dt = 0), the cable equation reduces to:

```
λ² · d²V/dx² = V - V_rest
```

Where **λ** (space constant) is:

```
λ = √(r_m / r_i)
```

**Solution for semi-infinite cable:**
```
V(x) = V_rest + (V_0 - V_rest) · exp(-x/λ)
```

**Biological interpretation:** Voltage decays exponentially with distance, characterized by space constant λ.

---

## NEURON Implementation Structure

### Morphology Files (`.hoc`)
- `dm1_morph_1.hoc` — Cell 1 reconstruction
- `dm1_morph_2.hoc` — Cell 2 reconstruction
- `dm1_morph_3.hoc` — Cell 3 reconstruction

Each file specifies:
- Number of compartments
- Geometry (length, diameter)
- Topology (parent-child connections)
- 3D coordinates

### Mechanism Files (`.mod`)

**LeakConductance.mod** — Passive membrane properties:
```c
NEURON {
    SUFFIX leak
    NONSPECIFIC_CURRENT i
    RANGE g, e
}

PARAMETER {
    g = 0.001 (siemens/cm2)
    e = -55 (millivolt)
}

ASSIGNED {
    v (millivolt)
    i (milliamp/cm2)
}

BREAKPOINT {
    i = g * (v - e)
}
```

**v_atten.mod** — Voltage attenuation recording at multiple sites

### Simulation Scripts

**mosinit.hoc** — Main initialization:
```hoc
load_file("nrngui.hoc")
load_file("dm1_morph_1.hoc")  // Load morphology

// Set passive properties
forall {
    insert leak
    g_leak = 1e-4  // S/cm²
    e_leak = -60   // mV
    Ra = 163.9     // Ω·cm
    cm = 2.6       // µF/cm²
}

// Current injection at soma
access soma
objref stim
stim = new IClamp(0.5)
stim.del = 100   // ms
stim.dur = 500   // ms
stim.amp = 0.1   // nA
```

---

## Key Findings from Model

### 1. Electrotonic Extent
- Projection neurons are **NOT electrotonically compact**
- Space constant λ ≈ 100-300 µm (neuron spans ~500+ µm)
- Voltage control from soma is **incomplete** in distal dendrites

### 2. Action Potential Initiation
- Spikes originate in **proximal axon** (not soma)
- Axon initial segment has highest excitability
- Similar to mammalian cortical neurons

### 3. Dendritic Integration
- Distal synaptic inputs are **attenuated** by ~50-70% at soma
- Provides **location-dependent weighting** of inputs
- Proximal inputs have stronger somatic influence

### 4. Seal Conductance Artifact
- Whole-cell recording introduces ~10 mV **depolarization artifact**
- Due to seal conductance in equivalent circuit
- Must be corrected when interpreting resting potential

---

## Python Implementation (Simplified)

```python
import numpy as np
from scipy.integrate import odeint

class CompartmentalNeuron:
    """
    Simple multi-compartment neuron model with passive cable properties
    """
    def __init__(self, n_compartments, Rm, Cm, Ri, lengths, diameters):
        """
        n_compartments: number of segments
        Rm: specific membrane resistance (kΩ·cm²)
        Cm: specific membrane capacitance (µF·cm⁻²)
        Ri: specific intracellular resistivity (Ω·cm)
        lengths: array of compartment lengths (µm)
        diameters: array of compartment diameters (µm)
        """
        self.n = n_compartments
        self.Rm = Rm
        self.Cm = Cm
        self.Ri = Ri
        self.lengths = lengths
        self.diameters = diameters

        # Calculate compartmental parameters
        self.surface_areas = np.pi * diameters * lengths  # µm²
        self.cross_sections = np.pi * (diameters/2)**2    # µm²

        # Convert to SI units and calculate r_m, c_m, r_i
        self.r_m = Rm * 1e3 / (self.surface_areas * 1e-8)  # Ω
        self.c_m = Cm * 1e-6 * (self.surface_areas * 1e-8)  # F
        self.r_i = Ri * lengths * 1e-4 / (self.cross_sections * 1e-8)  # Ω

    def derivatives(self, V, t, I_inj):
        """
        Compute dV/dt for each compartment
        V: voltage array (mV)
        t: time (ms)
        I_inj: injected current array (nA)
        """
        dVdt = np.zeros(self.n)
        V_rest = -60  # mV

        for i in range(self.n):
            # Leak current
            I_leak = -(V[i] - V_rest) / self.r_m[i] * 1e9  # nA

            # Axial currents from neighbors
            I_axial = 0
            if i > 0:  # current from left neighbor
                I_axial += (V[i-1] - V[i]) / self.r_i[i] * 1e9
            if i < self.n - 1:  # current from right neighbor
                I_axial += (V[i+1] - V[i]) / self.r_i[i+1] * 1e9

            # External injection
            I_ext = I_inj[i]

            # dV/dt = (I_total) / C_m
            dVdt[i] = (I_leak + I_axial + I_ext) / (self.c_m[i] * 1e9)  # mV/ms

        return dVdt

    def simulate(self, T, dt, I_inj_func):
        """
        Run simulation
        T: total time (ms)
        dt: time step (ms)
        I_inj_func: function(t, compartment_idx) -> current (nA)
        """
        t = np.arange(0, T, dt)
        V0 = np.ones(self.n) * -60  # initial voltages (mV)

        V_history = [V0]
        for i in range(1, len(t)):
            I_inj = np.array([I_inj_func(t[i], j) for j in range(self.n)])
            V_new = V_history[-1] + self.derivatives(V_history[-1], t[i], I_inj) * dt
            V_history.append(V_new)

        return t, np.array(V_history)

# Example usage
neuron = CompartmentalNeuron(
    n_compartments=10,
    Rm=16.5,      # kΩ·cm²
    Cm=1.6,       # µF·cm⁻²
    Ri=177.5,     # Ω·cm
    lengths=np.ones(10) * 50,      # µm
    diameters=np.ones(10) * 2      # µm
)

# Current injection at soma (compartment 0)
def I_inject(t, comp):
    if comp == 0 and 100 < t < 600:
        return 0.1  # nA
    return 0

t, V = neuron.simulate(T=1000, dt=0.1, I_inj_func=I_inject)
```

---

## AI Architecture Implications

### Architecture #40: Spatially-Extended Neuron Layer

```python
class CompartmentalLayer(nn.Module):
    """
    Neurons with spatial extent - each neuron has multiple compartments
    Information propagates via cable equations within neurons
    """
    def __init__(self, n_neurons, n_compartments_per_neuron):
        super().__init__()
        self.n_neurons = n_neurons
        self.n_comp = n_compartments_per_neuron

        # Membrane parameters
        self.Rm = nn.Parameter(torch.tensor(16.5))
        self.Cm = nn.Parameter(torch.tensor(1.6))
        self.Ri = nn.Parameter(torch.tensor(177.5))

        # Inter-compartment coupling
        self.axial_weights = nn.Parameter(torch.randn(n_neurons, n_compartments_per_neuron-1))

    def forward(self, x, V_state):
        """
        x: input to first compartment [batch, n_neurons]
        V_state: voltage state [batch, n_neurons, n_compartments]
        """
        batch_size = x.size(0)

        # Update first compartment with input
        V_new = V_state.clone()
        V_new[:, :, 0] = V_new[:, :, 0] + x

        # Propagate voltage via cable equations
        for i in range(1, self.n_comp):
            # Axial current from previous compartment
            axial = self.axial_weights[:, i-1] * (V_new[:, :, i-1] - V_new[:, :, i])

            # Leak current
            leak = -V_new[:, :, i] / F.softplus(self.Rm)

            # Update voltage
            dV = (axial + leak) / F.softplus(self.Cm)
            V_new[:, :, i] = V_new[:, :, i] + dV

        # Output from last compartment (axon terminal)
        return V_new[:, :, -1], V_new
```

### Architecture #41: Location-Dependent Input Weighting

```python
class DendriticWeighting(nn.Module):
    """
    Synaptic inputs are automatically weighted by location
    Distal inputs attenuated by cable properties
    """
    def __init__(self, n_inputs, space_constant=2.0):
        super().__init__()
        self.W = nn.Parameter(torch.randn(n_inputs))
        self.positions = nn.Parameter(torch.linspace(0, 5, n_inputs))  # distance from soma
        self.lambda_space = nn.Parameter(torch.tensor(space_constant))

    def forward(self, x):
        # Exponential attenuation based on distance
        attenuation = torch.exp(-self.positions / F.softplus(self.lambda_space))
        weighted_inputs = self.W * attenuation * x
        return weighted_inputs.sum()
```

### Architecture #42: Electrotonic Distance Normalization

```python
class ElectrotonicNorm(nn.Module):
    """
    Normalize activations based on electrotonic distance (not physical depth)
    Mimics how neurons compensate for cable attenuation
    """
    def __init__(self, num_features):
        super().__init__()
        self.gamma = nn.Parameter(torch.ones(num_features))
        self.beta = nn.Parameter(torch.zeros(num_features))
        # Learnable "space constant" per feature
        self.lambda_e = nn.Parameter(torch.ones(num_features))

    def forward(self, x, depth):
        """
        x: features [batch, features]
        depth: layer depth (0 = input, increases with depth)
        """
        # Compute electrotonic distance
        e_distance = depth / F.softplus(self.lambda_e)

        # Amplify based on distance (compensate for attenuation)
        amplification = torch.exp(e_distance)

        # Normalize and scale
        x_norm = F.layer_norm(x, x.shape[1:])
        return self.gamma * x_norm * amplification + self.beta
```

---

## References

- **Paper:** https://pmc.ncbi.nlm.nih.gov/articles/PMC2709801/
- **ModelDB:** https://modeldb.science/118662
- **GitHub:** https://github.com/ModelDBRepository/118662
- **NEURON Simulator:** https://neuron.yale.edu/
- **Cable Theory:** https://neuronaldynamics.epfl.ch/online/Ch3.S4.html
