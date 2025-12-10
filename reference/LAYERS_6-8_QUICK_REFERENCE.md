# Layers 6-8 Quick Reference Guide

**Comprehensive Formula Database:** See `LAYERS_6-8_NEURAL_COMPUTATION_FORMULAS.md` for full details

---

## LAYER 6: NEURON/DENDRITE LAYER

### Core Models

| Model | Key Equation | Parameters | Use Case |
|-------|--------------|------------|----------|
| **Cable Theory** | $\frac{\partial V}{\partial t} = \frac{1}{c_m}\left[\frac{d}{4R_i}\frac{\partial^2 V}{\partial x^2} - \frac{V-V_{rest}}{r_m}\right]$ | $\lambda = \sqrt{\frac{d \cdot r_m}{4R_i}}$ | Dendritic signal propagation |
| **LIF** | $C_m \frac{dV}{dt} = -g_L(V - E_L) + I(t)$ | $V_{th}=-50$ mV, $\tau_m=20$ ms | Fast, simple spiking |
| **AdEx** | $C_m \frac{dV}{dt} = -g_L(V-E_L) + g_L\Delta_T e^{(V-V_T)/\Delta_T} - w + I$ | $\Delta_T=2$ mV, $\tau_w=100$ ms | Adaptive neurons |
| **Izhikevich** | $\frac{dv}{dt} = 0.04v^2 + 5v + 140 - u + I$ | RS: $(0.02, 0.2, -65, 8)$ | Diverse dynamics |
| **Hodgkin-Huxley** | $C_m\frac{dV}{dt} = -I_{Na} - I_K - I_L + I_{ext}$ | $\bar{g}_{Na}=120$, $\bar{g}_K=36$ mS/cm² | Biophysically detailed |

### Dendritic Computation

| Mechanism | Formula | Implementation |
|-----------|---------|----------------|
| **NMDA Spike** | $I_{NMDA} = \bar{g}_{NMDA} s_{NMDA} \frac{1}{1+\frac{[Mg^{2+}]}{3.57}e^{-0.062V}}(V-E_{NMDA})$ | Coincidence detector |
| **Ca Spike** | $I_{Ca} = \bar{g}_{Ca} m_{Ca}^2 (V - E_{Ca})$ | Regenerative amplification |
| **Backprop AP** | Soma spike → dendritic depolarization | Learning signal distribution |

### Typical Parameters

- **Membrane capacitance:** $C_m = 1$ μF/cm² (0.8-1.2)
- **Membrane resistance:** $R_m = 20$ kΩ·cm² (10-50)
- **Intracellular resistance:** $R_i = 100$ Ω·cm (70-150)
- **Resting potential:** $V_{rest} = -70$ mV
- **Threshold:** $V_{th} = -50$ mV (LIF)
- **Reset:** $V_{reset} = -70$ mV
- **Refractory period:** $t_{refr} = 2$ ms

---

## LAYER 7: SYNAPSE/PLASTICITY LAYER

### Plasticity Rules

| Rule | Equation | Timescale | Use Case |
|------|----------|-----------|----------|
| **Classical STDP** | $\Delta w = A_+ e^{-\Delta t/\tau_+}$ (LTP)<br>$\Delta w = -A_- e^{\Delta t/\tau_-}$ (LTD) | $\tau_{\pm} \sim 20$ ms | Temporal correlation learning |
| **Triplet STDP** | $\Delta w = A_2^+ r_1 + A_3^+ r_2 o_1$ | $\tau_x=101$ ms, $\tau_y=125$ ms | Frequency-dependent |
| **Hebbian** | $\Delta w = \eta \cdot r_i \cdot r_j$ | Instantaneous | Rate-based correlation |
| **Oja's Rule** | $\Delta w = \eta(r_i r_j - \alpha r_j^2 w)$ | Slow | Normalized Hebbian |
| **BCM** | $\Delta w = \eta r_i r_j (r_j - \theta_j)$ | $\tau_\theta \sim$ hours | Sliding threshold |
| **Synaptic Scaling** | $\tau_{scale}\frac{dw}{dt} = w \cdot \alpha(\langle r_{target}\rangle - \langle r\rangle)$ | Days | Homeostasis |
| **STP (Tsodyks-Markram)** | $I_{syn} = A \cdot u \cdot x$ | $\tau_f \sim 750$ ms, $\tau_d \sim 1$ s | Short-term dynamics |
| **Neuromodulated** | $\Delta w = \eta \cdot \delta_{DA} \cdot e(t)$ | $\tau_e \sim 1$ s | Reward-based learning |

### STDP Parameters

**Standard values:**
- $A_+ = 0.005 - 0.01$ (LTP amplitude)
- $A_- = 0.00525 - 0.0105$ (LTD amplitude, slightly larger)
- $\tau_+ = 16.8$ ms (LTP window)
- $\tau_- = 33.7$ ms (LTD window)

**Triplet parameters:**
- $A_2^+ = 0.005$, $A_2^- = 0.007$
- $A_3^+ = 0.0062$, $A_3^- = 0.0023$

### Short-Term Plasticity

**Facilitating synapse:** $U=0.15$, $\tau_f=750$ ms, $\tau_d=50$ ms
**Depressing synapse:** $U=0.5$, $\tau_f=50$ ms, $\tau_d=750$ ms

---

## LAYER 8: MICROCIRCUIT/MOTIF LAYER

### Circuit Motifs

| Motif | Dynamics | Key Parameters | Function |
|-------|----------|----------------|----------|
| **Winner-Take-All** | $\tau\frac{dx_i}{dt} = -x_i + f(I_i - \sum_{j\neq i}w_{ij}x_j)$ | $w_{inh}=2.0$, $\tau=10$ ms | Sparse selection |
| **Hopfield Network** | $E = -\frac{1}{2}\sum_{ij}w_{ij}s_is_j$ | Capacity: $0.138N$ | Pattern storage |
| **Ring Attractor** | $w_{ij} = A\cos(\theta_i - \theta_j)$ | $A=1.0$ | Continuous representation |
| **Wilson-Cowan** | $\tau_E\frac{dE}{dt} = -E + f(w_{EE}E - w_{EI}I)$ | $w_{EI}w_{IE} > 1$ for osc | E-I dynamics |
| **PING Gamma** | E→I→E feedback loop | $\tau_I < \tau_E$ | 40-100 Hz oscillations |

### Attractor Networks

**Hopfield capacity:** Maximum stored patterns = $0.138 \times N$ neurons

**Ring attractor:**
- Weight: $w_{ij} = A \cos(\theta_i - \theta_j)$
- Decoding: $\theta = \arctan2\left(\sum_i x_i \sin\theta_i, \sum_i x_i \cos\theta_i\right)$

### Wilson-Cowan Parameters

**Oscillatory regime:**
- $w_{EE} = 1.2$ (recurrent excitation)
- $w_{EI} = 2.0$ (feedback inhibition)
- $w_{IE} = 1.5$ (feedforward excitation)
- $w_{II} = 0.5$ (recurrent inhibition)
- $\tau_E = 10$ ms, $\tau_I = 5$ ms

**Oscillation frequency:** $f \approx \frac{1}{2\pi\sqrt{\tau_E \tau_I}}$ when $w_{EI}w_{IE}$ large

### Gamma Oscillations

**PING mechanism:**
1. E cells fire → activate I cells
2. I cells suppress E cells
3. Inhibition decays → E cells rebound
4. **Period ≈ GABA decay constant (10-25 ms)**

**Frequency range:** 40-100 Hz (typically 60-80 Hz)

---

## STABILITY ANALYSIS

### Linear Stability

**System:** $\frac{dx}{dt} = F(x)$

**Fixed point:** $x^*$ where $F(x^*) = 0$

**Jacobian:** $J = \frac{\partial F}{\partial x}\bigg|_{x^*}$

**Stability:** All eigenvalues $\lambda$ must satisfy $\text{Re}(\lambda) < 0$

**Oscillations:** $\text{Im}(\lambda) \neq 0$ (complex eigenvalues)

**Frequency:** $f = \frac{|\text{Im}(\lambda)|}{2\pi}$

### E-I Network Stability

Oscillations occur when:
$$\text{det}(J - \lambda I) = 0 \text{ has complex roots}$$

Typically requires: $w_{EI} \cdot w_{IE} > (1 + \frac{\tau_E}{\tau_I})(1 + \frac{\tau_I}{\tau_E})$

---

## CODE IMPLEMENTATION CHECKLIST

### Layer 6: Neurons ✓
- [x] LIF neuron
- [x] AdEx neuron
- [x] Izhikevich neuron
- [x] Hodgkin-Huxley neuron
- [x] Compartmental cable model
- [x] Dendritic branch with NMDA/Ca spikes
- [x] Coincidence detector

### Layer 7: Synapses ✓
- [x] STDP synapse (classical)
- [x] Triplet STDP
- [x] Hebbian synapse
- [x] Oja's rule
- [x] BCM synapse
- [x] Homeostatic scaling
- [x] Short-term plasticity (Tsodyks-Markram)
- [x] Neuromodulated learning

### Layer 8: Circuits ✓
- [x] Winner-take-all network
- [x] Soft WTA (softmax)
- [x] K-winners-take-all
- [x] Hopfield network
- [x] Ring attractor
- [x] Auto-associative memory
- [x] Wilson-Cowan E-I network
- [x] PING gamma oscillator

---

## PERFORMANCE BENCHMARKS

### Computational Complexity

| Model | Per-step cost | Memory | Typical size |
|-------|---------------|--------|--------------|
| LIF neuron | O(1) | 4 floats | 1K-1M neurons |
| AdEx neuron | O(1) | 6 floats | 1K-100K neurons |
| HH neuron | O(1) | 8 floats | 100-10K neurons |
| Compartmental | O(N) | 3N floats | N=10-100 compartments |
| STDP synapse | O(1) | 5 floats | 1M-100M synapses |
| WTA network | O(N²) | N² weights | N=10-1000 |
| Hopfield | O(N²) | N² weights | N=100-10K |
| Wilson-Cowan | O(1) | 4 floats | 2 populations |

### Timescales

| Process | Timescale | dt required |
|---------|-----------|-------------|
| Spike | 1 ms | 0.01-0.1 ms |
| NMDA | 50-100 ms | 0.1-1 ms |
| STDP | 20 ms window | 0.1-1 ms |
| STP facilitation | 100-1000 ms | 1-10 ms |
| Homeostatic scaling | Hours-days | Minutes |
| Oscillations (gamma) | 10-25 ms period | 0.1 ms |

---

## BIOLOGICAL VS ARTIFICIAL COMPARISON

### Expressiveness

| Metric | Biological (Layers 6-8) | Artificial (Standard NN) | Advantage |
|--------|------------------------|--------------------------|-----------|
| **Neuron complexity** | 10-50 dendritic branches | 1 scalar | 100-1000× |
| **Learning rules** | 10+ local rules | 1 global (backprop) | Diversity |
| **Timescales** | 5+ (ms to days) | 1 (training phase) | Continual learning |
| **Memory capacity** | Distributed attractors | Separate weights | Integrated |
| **Dynamics** | Rich (oscillations, chaos) | Feedforward | Temporal computation |

### Computational Cost

**Training:**
- Biological: O(N) local updates (parallel)
- Artificial: O(N²) backprop (sequential)

**Inference:**
- Biological: O(N·T) recurrent dynamics
- Artificial: O(N) feedforward pass

**Memory:**
- Biological: O(N²) for full connectivity
- Artificial: O(N²) same, but fixed

---

## INTEGRATION ROADMAP

### Phase 1: Standalone Components (Weeks 1-2)
- Implement all neuron models
- Test individual plasticity rules
- Validate circuit motifs

### Phase 2: Combined Systems (Weeks 3-4)
- Integrate Layer 6 + Layer 7
- Build Layer 6 + Layer 7 + Layer 8 microcircuits
- Test on simple tasks (XOR, pattern recognition)

### Phase 3: Brain Regions (Weeks 5-8)
- Assemble microcircuits into regions (V1, Hippocampus, PFC)
- Implement inter-region communication
- Test on complex tasks (memory, reasoning)

### Phase 4: Full BioAI System (Weeks 9-12)
- Integrate all 88 layers
- Add global neuromodulation (dopamine, serotonin)
- Deploy on realistic benchmarks

---

## KEY REFERENCES

### Foundational Papers
1. **Rall (1959)** - Cable theory
2. **Hodgkin & Huxley (1952)** - Action potential
3. **Bi & Poo (1998)** - STDP discovery
4. **Hopfield (1982)** - Attractor networks
5. **Wilson & Cowan (1972)** - E-I dynamics

### Modern Reviews
6. **Pfister & Gerstner (2006)** - Triplet STDP
7. **Tsodyks & Markram (1997)** - Short-term plasticity
8. **Földiák (1990)** - Sparse coding via WTA

### Implementation Guides
9. **Dayan & Abbott (2001)** - *Theoretical Neuroscience*
10. **Gerstner et al. (2014)** - *Neuronal Dynamics*

---

## RESOURCES

**Full Documentation:** `/home/user/MAINFRAME/LAYERS_6-8_NEURAL_COMPUTATION_FORMULAS.md`

**Code Examples:** All implementations included in main document

**Database Schema:** `/home/user/MAINFRAME/bioformulas/schema.sql`

**Related Files:**
- `/home/user/MAINFRAME/DENDRITIC_NEURON_MODULE.md`
- `/home/user/MAINFRAME/bioai_os/layer_5_proto_neuron.py`
- `/home/user/MAINFRAME/BIOAI_590_MECHANISMS_DATABASE.md`

---

**Status:** Complete ✓
**Coverage:** 15+ neuron models, 10+ plasticity rules, 8+ circuit motifs
**Code:** All models implemented with working examples
**Validation:** Parameter ranges verified against neuroscience literature
