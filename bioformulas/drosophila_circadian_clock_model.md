# Drosophila Circadian Clock Mathematical Model

**Source:** Cell (2009) - "Mathematical Model of the Drosophila Circadian Clock: Loop Regulation and Transcriptional Integration"
**DOI:** https://pmc.ncbi.nlm.nih.gov/articles/PMC2770617/
**Model Type:** Nonlinear ordinary differential equations (ODEs)
**Period:** ~24 hours (23.97-24.05 hours)

---

## Novel ODE Framework

### General Regulatory Equation

**Equation 1** - Core dynamics for molecular concentration:

```
dx_i(t)/dt = ρ_i * g(Σ(λ_ji * x_j(t))) - δ_i * x_i(t) * x_i(t) * (s_i - x_i(t))
```

#### Variables:
- **x_i(t)** = concentration of molecule i at time t (mRNA, protein, dimer, or phosphorylated form)
- **t** = time (hours)

#### Parameters:
- **ρ_i** > 0 = maximum formation rate constant (concentration/hour)
- **δ_i** > 0 = decay/degradation rate constant (1/hour)
- **s_i** ≥ 0 = saturation level (maximum concentration)
- **λ_ji** = regulatory weight from molecule j to molecule i
  - **λ_ji > 0** → activation/enhancement
  - **λ_ji < 0** → repression/inhibition
  - **λ_ji = 0** → no regulation

---

## Sigmoid Modulation Function

**Equation 2** - Transforms regulatory signals:

```
g(u) = u / (1 + u²)
```

**Alternative formulation:**
```
g(u) = tanh(ln(u + √(1 + u²)))
```

### Properties:
- **Odd function:** g(-u) = -g(u)
- **Range:** (-1, 1)
- **Smooth:** continuously differentiable
- **Biological interpretation:** integrates opposing regulatory signals nonlinearly

---

## Transcriptional Signal Integration

**Equation 3** - How genes integrate positive (CLK-CYC) and negative (CWO) signals:

```
sign(ΔY_g) = sign[ΔxC/C(t_g) * λC/C,g - xCWO(t_g) * |λCWO,g|]
```

Where:
- **ΔY_g** = change in gene g transcript level
- **xC/C(t_g)** = CLK-CYC concentration at time t_g
- **ΔxC/C(t_g)** = change in CLK-CYC concentration
- **xCWO(t_g)** = CWO (Clockwork Orange) concentration
- **λC/C,g** = activation weight from CLK-CYC to gene g
- **λCWO,g** = repression weight from CWO to gene g

**Biological meaning:** Gene expression increases when CLK-CYC activation exceeds CWO repression.

---

## Gene Regulatory Network

### Positive Feedback Loop
```
clk mRNA → CLK protein ↘
                          → CLK-CYC dimer → transcription activation
cyc mRNA → CYC protein ↗
```

### Negative Feedback Loops

**Loop 1: PER/TIM**
```
CLK-CYC → per mRNA → PER protein ↘
                                   → PER-TIM dimer → (represses CLK-CYC)
CLK-CYC → tim mRNA → TIM protein ↗
```

**Loop 2: VRI/PDP1**
```
CLK-CYC → vri mRNA → VRI protein → (represses clk)
CLK-CYC → Pdp1 mRNA → PDP1 protein → (activates clk)
```

**Additional repression:**
```
CLK-CYC → cwo mRNA → CWO protein → (represses CLK-CYC targets)
```

---

## Molecular Species Tracked

### Transcripts (mRNA):
1. **clk** - clock
2. **cyc** - cycle
3. **per** - period
4. **tim** - timeless
5. **vri** - vrille
6. **Pdp1** - PAR domain protein 1
7. **cwo** - clockwork orange
8. **cry** - cryptochrome

### Proteins (single):
1. **CLK** - CLOCK protein
2. **CYC** - CYCLE protein
3. **PER** - PERIOD protein
4. **TIM** - TIMELESS protein
5. **VRI** - VRILLE protein
6. **PDP1** - PDP1 protein
7. **CWO** - Clockwork Orange protein
8. **CRY** - CRYPTOCHROME protein

### Protein Complexes:
1. **CLK-CYC** - heterodimer (active transcription factor)
2. **PER-TIM** - heterodimer (enters nucleus to repress CLK-CYC)
3. **PER-p** - phosphorylated PER (degradation target)
4. **TIM-p** - phosphorylated TIM (degradation target)

---

## Example ODE for *per* mRNA

```
d[per_mRNA]/dt = ρ_per * g(λ_CLK-CYC,per * [CLK-CYC] - λ_CWO,per * [CWO])
                 - δ_per * [per_mRNA] * [per_mRNA] * (s_per - [per_mRNA])
```

**Interpretation:**
- CLK-CYC activates *per* transcription (positive term)
- CWO represses *per* transcription (negative term)
- g() function integrates both signals nonlinearly
- mRNA degrades proportionally to concentration

---

## Key Regulatory Weights (Example Values)

These are illustrative - full parametrization in supplementary MATLAB code:

| Interaction | λ value | Type |
|-------------|---------|------|
| CLK-CYC → per | +2.5 | Activation |
| CLK-CYC → tim | +2.3 | Activation |
| CLK-CYC → vri | +2.8 | Activation |
| CLK-CYC → Pdp1 | +2.1 | Activation |
| CLK-CYC → cwo | +1.9 | Activation |
| CWO → per | -1.5 | Repression |
| CWO → tim | -1.4 | Repression |
| VRI → clk | -2.0 | Repression |
| PDP1 → clk | +1.8 | Activation |
| PER-TIM → CLK-CYC | -3.0 | Repression |

---

## Numerical Implementation

### Solver
- **MATLAB ode45** (Dormand-Prince method)
- **Time step:** Adaptive (stiff ODE solver)
- **Duration:** 240+ hours (10 days) to ensure stable oscillations
- **Initial conditions:** Randomized, converges to limit cycle

### Optimization
- Parameters (ρ, δ, s, λ) fitted to match experimental data:
  - mRNA/protein peak times
  - Amplitude ratios
  - Phase relationships
  - Mutant phenotypes (per^0, tim^0, clk^jrk, etc.)

---

## Model Predictions

### Wild-Type Behavior
- **Period:** 24.0 ± 0.05 hours
- **Phase order:** CLK-CYC peaks → per/tim transcription → PER/TIM protein accumulation → nuclear entry → repression → cycle repeats
- **Amplitude:** Self-sustaining oscillations (stable limit cycle)

### Mutant Simulations
- **per^0** (no PER): Arrhythmic (no negative feedback)
- **tim^0** (no TIM): Arrhythmic (PER unstable alone)
- **clk^jrk** (no CLK): Flat-lined (no positive drive)
- **cwo^0** (no CWO): Increased amplitude (less repression)

---

## Python Implementation

```python
import numpy as np
from scipy.integrate import odeint

def g(u):
    """Sigmoid modulation function"""
    return u / (1 + u**2)

def circadian_odes(state, t, params):
    """
    Drosophila circadian clock ODEs
    state = [clk_mRNA, cyc_mRNA, per_mRNA, tim_mRNA, vri_mRNA, Pdp1_mRNA, cwo_mRNA,
             CLK, CYC, PER, TIM, VRI, PDP1, CWO, CLK_CYC, PER_TIM]
    """
    # Unpack state variables
    clk_m, cyc_m, per_m, tim_m, vri_m, Pdp1_m, cwo_m = state[0:7]
    CLK, CYC, PER, TIM, VRI, PDP1, CWO = state[7:14]
    CLK_CYC, PER_TIM = state[14:16]

    # Unpack parameters (example values)
    rho = params['rho']  # formation rates
    delta = params['delta']  # decay rates
    s = params['s']  # saturation levels
    lam = params['lambda']  # regulatory weights

    # Transcription rates with regulatory integration
    d_clk_m = rho['clk'] * g(lam['PDP1_clk']*PDP1 - lam['VRI_clk']*VRI) \
              - delta['clk_m'] * clk_m * clk_m * (s['clk_m'] - clk_m)

    d_per_m = rho['per'] * g(lam['CLKCYC_per']*CLK_CYC - lam['CWO_per']*CWO) \
              - delta['per_m'] * per_m * per_m * (s['per_m'] - per_m)

    d_tim_m = rho['tim'] * g(lam['CLKCYC_tim']*CLK_CYC - lam['CWO_tim']*CWO) \
              - delta['tim_m'] * tim_m * tim_m * (s['tim_m'] - tim_m)

    d_vri_m = rho['vri'] * g(lam['CLKCYC_vri']*CLK_CYC) \
              - delta['vri_m'] * vri_m * vri_m * (s['vri_m'] - vri_m)

    d_Pdp1_m = rho['Pdp1'] * g(lam['CLKCYC_Pdp1']*CLK_CYC) \
               - delta['Pdp1_m'] * Pdp1_m * Pdp1_m * (s['Pdp1_m'] - Pdp1_m)

    d_cwo_m = rho['cwo'] * g(lam['CLKCYC_cwo']*CLK_CYC) \
              - delta['cwo_m'] * cwo_m * cwo_m * (s['cwo_m'] - cwo_m)

    # Protein translation and degradation
    d_CLK = rho['CLK'] * clk_m - delta['CLK'] * CLK - params['k_dimer'] * CLK * CYC
    d_CYC = rho['CYC'] * cyc_m - delta['CYC'] * CYC - params['k_dimer'] * CLK * CYC
    d_PER = rho['PER'] * per_m - delta['PER'] * PER - params['k_dimer'] * PER * TIM
    d_TIM = rho['TIM'] * tim_m - delta['TIM'] * TIM - params['k_dimer'] * PER * TIM
    d_VRI = rho['VRI'] * vri_m - delta['VRI'] * VRI
    d_PDP1 = rho['PDP1'] * Pdp1_m - delta['PDP1'] * PDP1
    d_CWO = rho['CWO'] * cwo_m - delta['CWO'] * CWO

    # Dimer formation and degradation
    d_CLK_CYC = params['k_dimer'] * CLK * CYC \
                - delta['CLK_CYC'] * CLK_CYC \
                - lam['PERTIM_CLKCYC'] * PER_TIM * CLK_CYC

    d_PER_TIM = params['k_dimer'] * PER * TIM - delta['PER_TIM'] * PER_TIM

    return [d_clk_m, 0, d_per_m, d_tim_m, d_vri_m, d_Pdp1_m, d_cwo_m,
            d_CLK, d_CYC, d_PER, d_TIM, d_VRI, d_PDP1, d_CWO,
            d_CLK_CYC, d_PER_TIM]

# Simulation
t = np.linspace(0, 240, 10000)  # 10 days
state0 = np.random.rand(16)  # Random initial conditions
params = {...}  # Define full parameter set
solution = odeint(circadian_odes, state0, t, args=(params,))
```

---

## AI Architecture Implications

### Architecture #37: Circadian Oscillator Network

```python
class CircadianOscillatorLayer(nn.Module):
    """
    Neural layer with built-in 24-step oscillations
    Uses circadian-inspired regulatory feedback
    """
    def __init__(self, features):
        super().__init__()
        # Positive elements (CLK-CYC analog)
        self.W_pos = nn.Parameter(torch.randn(features, features))

        # Negative elements (PER-TIM analog)
        self.W_neg = nn.Parameter(torch.randn(features, features))

        # Regulatory weights
        self.lambda_act = nn.Parameter(torch.ones(features) * 2.0)
        self.lambda_rep = nn.Parameter(torch.ones(features) * -1.5)

        # Decay rates
        self.delta = nn.Parameter(torch.ones(features) * 0.1)

    def g(self, u):
        """Odd sigmoid modulation"""
        return u / (1 + u**2)

    def forward(self, x, state_pos, state_neg):
        """
        x: input features
        state_pos: positive regulator state (CLK-CYC analog)
        state_neg: negative regulator state (PER-TIM analog)
        """
        # Regulatory integration
        reg_signal = self.lambda_act * state_pos + self.lambda_rep * state_neg
        modulated = self.g(reg_signal)

        # Update positive regulator
        d_pos = F.relu(x @ self.W_pos) * modulated - self.delta * state_pos
        new_pos = state_pos + d_pos

        # Update negative regulator (delayed activation)
        d_neg = F.relu(new_pos @ self.W_neg) - self.delta * state_neg
        new_neg = state_neg + d_neg

        return new_pos, new_neg
```

### Architecture #38: Odd-Sigmoid Activation

```python
class OddSigmoidActivation(nn.Module):
    """
    Activation function from circadian model: g(u) = u/(1 + u²)
    Properties: odd function, bounded, smooth
    """
    def forward(self, x):
        return x / (1 + x**2)
```

### Architecture #39: Regulatory Weight Network

```python
class RegulatoryWeightNetwork(nn.Module):
    """
    Network where edges have signed weights representing activation/repression
    Single parameter per regulation (like biological λ_ji)
    """
    def __init__(self, n_nodes):
        super().__init__()
        # Lambda matrix: positive = activation, negative = repression
        self.Lambda = nn.Parameter(torch.randn(n_nodes, n_nodes))

    def forward(self, x):
        # Sign-preserving transformation
        signed_weights = torch.tanh(self.Lambda)  # Keep in [-1, 1]
        return x @ signed_weights
```

---

## References

- **Paper:** https://pmc.ncbi.nlm.nih.gov/articles/PMC2770617/
- **Supplementary MATLAB:** Referenced in paper (full parameter sets)
- **Experimental data:** Multiple sources cited for validation
