# Computational Value Mapping: The Rosetta Stone of Bio-Architecture

**Version:** 1.0.0
**Last Updated:** 2025-12-10
**Purpose:** Translation guide from biological mechanisms to computational/architectural primitives

---

## Table of Contents

1. [Master Mapping Table](#1-master-mapping-table)
2. [Category-by-Category Deep Dives](#2-category-by-category-deep-dives)
3. [Computational Primitives Library](#3-computational-primitives-library)
4. [Architecture Patterns Catalog](#4-architecture-patterns-catalog)
5. [Fidelity Scores](#5-fidelity-scores)
6. [Implementation Roadmap](#6-implementation-roadmap)
7. [Cross-Reference Index](#7-cross-reference-index)

---

## 1. Master Mapping Table

This table provides a high-level overview of how each biological entity type maps to computational primitives.

### 1.1 Mechanisms (~300) → Update Rules

| Biological Entity | Source DB | Computational Primitive | Architectural Pattern | Math Formalization | Difficulty | Dependencies |
|-------------------|-----------|------------------------|----------------------|-------------------|------------|--------------|
| **Lateral Inhibition** | NeuroML, ModelDB | Competitive suppression | Winner-Take-All network | `dy_i/dt = -y_i + f(x_i - Σ w_ij·y_j)` | Moderate | None |
| **Hebbian Learning** | ModelDB, Neuroscience | Correlation-based weight update | Associative memory | `dw_ij/dt = η·x_i·y_j` | Trivial | None |
| **STDP** | ModelDB | Temporal causality learning | Sequence learning network | `dw/dt = A₊e^(-Δt/τ₊) - A₋e^(Δt/τ₋)` | Moderate | Timing mechanism |
| **Homeostatic Plasticity** | Neuroscience | Stability constraint | Self-normalizing network | `dw/dt = ε(ρ₀ - ρ)` | Moderate | Activity monitoring |
| **Feedback Inhibition** | Systems Biology | Negative feedback control | PID controller | `dx/dt = k_prod - k_deg·x - k_fb·x^n` | Trivial | None |
| **Feedforward Activation** | Systems Biology | Anticipatory control | Predictive gating | `dy/dt = k₁x - k₂y - k₃zy` | Moderate | Multi-component |
| **Competitive Learning** | Neural Networks | Sparse coding | Self-organizing map | `w_winner += η(x - w_winner)` | Trivial | Distance metric |
| **BCM Plasticity** | Neuroscience | Sliding threshold learning | Adaptive threshold network | `dw/dt = φ(y)(y - θ_m)x` | Complex | Threshold tracking |
| **Spike Frequency Adaptation** | Neuroscience | Rate limiting | Adaptive filter | `dw/dt = a(V - E_L) - bw` | Moderate | State variable |
| **Presynaptic Facilitation** | Neuroscience | Input amplification | Gain modulation | `dR/dt = (1-R)/τ + U·R` | Moderate | Resource tracking |

### 1.2 Processes (~2500) → Runtime Dynamics

| Biological Entity | Source DB | Computational Primitive | Architectural Pattern | Math Formalization | Difficulty | Dependencies |
|-------------------|-----------|------------------------|----------------------|-------------------|------------|--------------|
| **Action Potential** | ModelDB | Signal propagation | Wave propagation | Hodgkin-Huxley equations | Complex | Ion channels |
| **Synaptic Transmission** | NeuroML | Message passing | Event-driven communication | `I_syn = g·(V - E_rev)` | Moderate | Receptors |
| **Calcium Oscillations** | BioModels | Clock/timing mechanism | Oscillator circuit | `d[Ca]/dt = J_in - J_out + J_leak` | Moderate | Calcium stores |
| **Vesicle Release** | Neuroscience | Probabilistic dispatch | Stochastic event generator | `P_r = 1 - exp(-[Ca]^4/K_d^4)` | Moderate | Calcium signal |
| **Neurotransmitter Diffusion** | BioModels | Spatial message broadcast | Diffusion network | `∂c/∂t = D∇²c - k·c` | Complex | Geometry |
| **Receptor Desensitization** | KEGG | Adaptive attenuation | Auto-scaling | `dD/dt = k_d(1-D) - k_r·D` | Moderate | Receptor state |
| **Ion Pump Operation** | BioModels | Resource management | Active transport | `J = J_max[Na]^3/([Na]^3 + K_m^3)` | Moderate | Energy (ATP) |
| **Glycolysis** | KEGG, Reactome | Sequential processing | Pipeline architecture | Michaelis-Menten cascade | Complex | Enzymes, substrates |
| **Oxidative Phosphorylation** | BioModels | Energy generation | Power supply circuit | Chemiosmotic coupling | Complex | Mitochondria |
| **Signal Transduction Cascade** | KEGG | Amplification pipeline | Signal amplifier | MAPK cascade equations | Complex | Kinases |

### 1.3 Circuit Motifs (~100) → Network Patterns

| Biological Entity | Source DB | Computational Primitive | Architectural Pattern | Math Formalization | Difficulty | Dependencies |
|-------------------|-----------|------------------------|----------------------|-------------------|------------|--------------|
| **Feedforward Inhibition** | Neuroscience | Temporal precision gate | Coincidence detector | Two-path delay + summation | Moderate | Delay elements |
| **Recurrent Excitation** | Neuroscience | Working memory buffer | Attractor network | `dy/dt = -y + f(Wx + Uy)` | Complex | Recurrent connectivity |
| **Mutual Inhibition** | Neuroscience | Bistable switch | Flip-flop circuit | `dx/dt = f(-ax - by + I)` | Moderate | Cross-inhibition |
| **Feedback Loop** | Systems Biology | State maintenance | Memory cell | `dx/dt = f(x) + input` | Trivial | Self-connection |
| **Lateral Excitation** | Neuroscience | Pattern completion | Content-addressable memory | Hebbian attractor | Complex | Associative weights |
| **Disinhibition** | Neuroscience | Gated activation | Enable signal | `y = input if not(inhibited)` | Trivial | Inhibitory interneuron |
| **Winner-Take-All** | Neural Networks | Competitive selection | Argmax operation | Global inhibition | Moderate | All-to-all inhibition |
| **Central Pattern Generator** | Neuroscience | Rhythmic output | Oscillator network | Coupled oscillators | Complex | Reciprocal inhibition |
| **Hierarchical Processing** | Neuroscience | Feature abstraction | Deep network | Layer-wise computation | Complex | Multi-layer structure |
| **Divisive Normalization** | Neuroscience | Dynamic range adjustment | Automatic gain control | `y_i = x_i/(σ + Σx_j)` | Moderate | Population activity |

### 1.4 Network Structures (~250) → Architectural Templates

| Biological Entity | Source DB | Computational Primitive | Architectural Pattern | Math Formalization | Difficulty | Dependencies |
|-------------------|-----------|------------------------|----------------------|-------------------|------------|--------------|
| **Cortical Column** | Allen Brain | Hierarchical processing unit | Microarchitecture module | Laminar connectivity matrix | Complex | Cell types |
| **Basal Ganglia** | Neuroscience | Action selection | Reinforcement learning system | Actor-critic architecture | Complex | Dopamine signals |
| **Hippocampus** | Allen Brain | Sequence memory | Recurrent autoencoder | CA3-CA1 network | Complex | Place cells |
| **Cerebellum** | Neuroscience | Error correction | Supervised learning system | Perceptron-like learning | Complex | Climbing fibers |
| **Thalamic Relay** | Allen Brain | Gated information flow | Multiplexer | Context-dependent routing | Moderate | Cortical feedback |
| **Default Mode Network** | Neuroscience | Background processing | Idle state processor | Anticorrelated activity | Complex | Resting state |
| **Visual Cortex Hierarchy** | Allen Brain | Progressive abstraction | Convolutional network | V1→V2→V4→IT pathway | Complex | Receptive fields |
| **Small-World Network** | Network Science | Efficient routing | Graph topology | High clustering + short path | Moderate | Graph metrics |
| **Scale-Free Network** | Network Science | Hub-based routing | Hierarchical network | Power-law degree distribution | Moderate | Preferential attachment |
| **Modular Network** | Network Science | Functional segregation | Microservices architecture | Community structure | Moderate | Modularity metric |

### 1.5 Representations (~50) → Encoding Formats

| Biological Entity | Source DB | Computational Primitive | Architectural Pattern | Math Formalization | Difficulty | Dependencies |
|-------------------|-----------|------------------------|----------------------|-------------------|------------|--------------|
| **Rate Coding** | Neuroscience | Frequency modulation | Analog encoding | `r = f(I)` | Trivial | Firing rate |
| **Temporal Coding** | Neuroscience | Phase modulation | Time-based encoding | Spike timing | Moderate | Precise timing |
| **Population Coding** | Neuroscience | Distributed representation | Vector encoding | Tuning curve ensemble | Moderate | Multiple neurons |
| **Sparse Coding** | Neural Networks | Compressed representation | Sparse vector | `min ||x - Ws||² + λ||s||₁` | Complex | Optimization |
| **Place Fields** | Neuroscience | Spatial encoding | Spatial hash map | Gaussian bumps in space | Moderate | Spatial coordinates |
| **Grid Cells** | Neuroscience | Metric encoding | Hexagonal tiling | Periodic firing pattern | Complex | Path integration |
| **Phase Coding** | Neuroscience | Temporal ordering | Phase-locked encoding | Theta phase precession | Complex | Oscillations |
| **Rank-Order Coding** | Neuroscience | Ordinal encoding | Priority encoding | First-to-spike wins | Moderate | Timing comparison |
| **Predictive Coding** | Neuroscience | Error-based encoding | Residual encoding | `y = x - prediction` | Complex | Prediction model |
| **Grandmother Cell** | Neuroscience | Dedicated encoding | Symbolic representation | One-hot encoding | Trivial | Specificity |

### 1.6 Computations (~100) → Universal Operators

| Biological Entity | Source DB | Computational Primitive | Architectural Pattern | Math Formalization | Difficulty | Dependencies |
|-------------------|-----------|------------------------|----------------------|-------------------|------------|--------------|
| **Dendritic Integration** | Neuroscience | Weighted summation | Linear combiner | `y = Σ w_i·x_i` | Trivial | Synaptic weights |
| **Nonlinear Summation** | Neuroscience | Threshold function | Activation function | `y = f(Σ w_i·x_i)` | Trivial | Nonlinearity |
| **Temporal Integration** | Neuroscience | Leaky accumulator | Low-pass filter | `τdy/dt = -y + x` | Trivial | Time constant |
| **Coincidence Detection** | Neuroscience | AND gate | Logical conjunction | `y = x₁ AND x₂` | Trivial | Temporal precision |
| **Motion Detection** | Neuroscience | Spatiotemporal correlation | Correlation filter | Reichardt detector | Moderate | Delay + multiply |
| **Gain Modulation** | Neuroscience | Multiplicative scaling | Variable gain amplifier | `y = g(context)·f(input)` | Moderate | Context signal |
| **Normalization** | Neuroscience | Divisive scaling | Dynamic range compression | `y_i = x_i / (σ + Σx_j)` | Moderate | Population sum |
| **Differentiation** | Neuroscience | Rate-of-change detection | High-pass filter | `y = dx/dt` | Moderate | Temporal derivative |
| **Pattern Completion** | Neuroscience | Associative recall | Content-addressable memory | Hopfield network | Complex | Associative weights |
| **Predictive Inference** | Neuroscience | Bayesian inference | Probabilistic computation | `P(x|y) ∝ P(y|x)P(x)` | Complex | Prior distribution |

### 1.7 Constraints (~100) → Optimization Limits

| Biological Entity | Source DB | Computational Primitive | Architectural Pattern | Math Formalization | Difficulty | Dependencies |
|-------------------|-----------|------------------------|----------------------|-------------------|------------|--------------|
| **Metabolic Cost** | Biophysics | Energy budget constraint | Power consumption limit | `E = Σ ATP_i` | Moderate | ATP accounting |
| **Wiring Length** | Neuroscience | Communication cost | Spatial routing constraint | `C = Σ d_ij` | Moderate | Physical layout |
| **Spike Rate Limit** | Biophysics | Bandwidth constraint | Maximum throughput | `r < r_max` | Trivial | Refractory period |
| **Axonal Delay** | Neuroscience | Latency constraint | Propagation delay | `Δt = d/v` | Trivial | Conduction velocity |
| **Dendritic Attenuation** | Biophysics | Signal degradation | Cable loss | `V(x) = V₀e^(-x/λ)` | Moderate | Cable properties |
| **Synaptic Saturation** | Neuroscience | Dynamic range limit | Clipping constraint | `w ∈ [w_min, w_max]` | Trivial | Bounds |
| **Receptor Availability** | Biophysics | Resource constraint | Buffer capacity | `R_total = R_free + R_bound` | Moderate | Conservation |
| **Calcium Buffering** | Biophysics | Temporal smoothing | Low-pass filtering | Fast buffers limit rate | Moderate | Buffer kinetics |
| **Membrane Capacitance** | Biophysics | Temporal filtering | RC time constant | `τ = R_m·C_m` | Trivial | Passive properties |
| **Sparse Connectivity** | Neuroscience | Structural constraint | Graph sparsity | `density = edges/max_edges` | Trivial | Connectivity matrix |

### 1.8 Enzymes (~6000) → Computational Operators

| Biological Entity | Source DB | Computational Primitive | Architectural Pattern | Math Formalization | Difficulty | Dependencies |
|-------------------|-----------|------------------------|----------------------|-------------------|------------|--------------|
| **Kinase** | UniProt, BRENDA | State flag setting | Phosphorylation = SET bit | `E + S ⇌ ES → E + P` | Moderate | ATP, target protein |
| **Phosphatase** | UniProt, BRENDA | State flag clearing | Dephosphorylation = CLEAR bit | `E + P-S → E + S + Pi` | Moderate | Target protein |
| **Ligase** | UniProt, BRENDA | Pointer creation | Linking operation | `A + B → A-B` | Moderate | ATP, substrates |
| **Protease** | UniProt, BRENDA | Pointer breaking | Unlinking operation | `A-B → A + B` | Moderate | Target bond |
| **Dehydrogenase** | BRENDA | Oxidation operation | Electron transfer | `AH₂ → A + 2H⁺ + 2e⁻` | Moderate | NAD/FAD |
| **Reductase** | BRENDA | Reduction operation | Electron acceptance | `A + 2H⁺ + 2e⁻ → AH₂` | Moderate | NADH/FADH₂ |
| **Transferase** | UniProt, BRENDA | Group transfer | Data movement | `A-X + B → A + B-X` | Moderate | Donor, acceptor |
| **Isomerase** | BRENDA | Structural transformation | Bit rearrangement | `A ⇌ B` (isomers) | Moderate | Conformational change |
| **Hydrolase** | UniProt, BRENDA | Bond cleavage | Destruction operation | `A-B + H₂O → A-OH + B-H` | Moderate | Water |
| **Synthase** | BRENDA | Bond formation | Construction operation | `A + B → A-B` (no ATP) | Moderate | Substrates |

### 1.9 Receptors/Channels (~3000) → Gating Mechanisms

| Biological Entity | Source DB | Computational Primitive | Architectural Pattern | Math Formalization | Difficulty | Dependencies |
|-------------------|-----------|------------------------|----------------------|-------------------|------------|--------------|
| **Voltage-Gated Na Channel** | NeuroML | Voltage-triggered gate | Threshold detector | HH gating variables | Complex | Membrane voltage |
| **Voltage-Gated K Channel** | NeuroML | Voltage-triggered gate | Delayed rectifier | HH n⁴ gating | Complex | Membrane voltage |
| **Ca-Gated K Channel** | NeuroML | Ligand-triggered gate | Concentration sensor | `P_open = [Ca]^n/(K_d^n + [Ca]^n)` | Moderate | Calcium concentration |
| **NMDA Receptor** | NeuroML | Coincidence detector | AND gate (V + ligand) | Mg²⁺ block + glutamate | Complex | Voltage + glutamate |
| **AMPA Receptor** | NeuroML | Fast ligand gate | Signal receiver | `I = g·(V - E_rev)` | Moderate | Glutamate |
| **GABA_A Receptor** | NeuroML | Inhibitory ligand gate | Inhibitory switch | Cl⁻ conductance | Moderate | GABA |
| **GPCR** | UniProt | Signal transduction gate | Second messenger generator | G-protein activation | Complex | Ligand, G-protein |
| **Nicotinic ACh Receptor** | NeuroML | Fast excitatory gate | Non-selective cation channel | Pentameric structure | Moderate | Acetylcholine |
| **Inward Rectifier K Channel** | NeuroML | Directional gate | One-way valve | Inward > outward | Moderate | Voltage, polyamines |
| **Leak Channel** | NeuroML | Constant conductance | Passive resistor | Ohmic conductance | Trivial | None |

### 1.10 Cell Types (~3000) → Architectural Templates

| Biological Entity | Source DB | Computational Primitive | Architectural Pattern | Math Formalization | Difficulty | Dependencies |
|-------------------|-----------|------------------------|----------------------|-------------------|------------|--------------|
| **Pyramidal Neuron** | NeuroMorpho | Integrator + transmitter | Computing + broadcasting | Dendritic integration | Complex | Synapses, dendrites |
| **Interneuron (PV)** | Allen Brain | Fast inhibitory unit | Temporal sharpening gate | Fast-spiking dynamics | Moderate | High firing rate |
| **Interneuron (SST)** | Allen Brain | Dendritic inhibitor | Gain control | Dendritic targeting | Moderate | Dendritic location |
| **Granule Cell** | NeuroMorpho | Sparse encoder | Sparse coding unit | High threshold | Moderate | Mossy fibers |
| **Purkinje Cell** | NeuroMorpho | Pattern classifier | Perceptron unit | Massive input integration | Complex | Parallel fibers |
| **Dopamine Neuron** | Allen Brain | Reward signal broadcaster | TD-error transmitter | Phasic firing | Moderate | Reward prediction |
| **Motor Neuron** | NeuroMorpho | Output executor | Actuator driver | Large cell body | Moderate | Muscle interface |
| **Sensory Receptor** | Neuroscience | Input transducer | Sensor | Stimulus → spike encoding | Moderate | Specific modality |
| **Astrocyte** | Neuroscience | Support/modulation | Homeostatic regulator | Slow timescale | Moderate | Neurotransmitter uptake |
| **Microglia** | Neuroscience | Maintenance/repair | Garbage collector | Immune response | Moderate | Debris detection |

### 1.11 Pathways (~500) → Control Flow

| Biological Entity | Source DB | Computational Primitive | Architectural Pattern | Math Formalization | Difficulty | Dependencies |
|-------------------|-----------|------------------------|----------------------|-------------------|------------|--------------|
| **MAPK Cascade** | KEGG, Reactome | Multi-stage amplification | Signal amplifier pipeline | 3-tier kinase cascade | Complex | Kinases, phosphatases |
| **PI3K-AKT Pathway** | KEGG | Growth signal processor | Resource allocation | Phosphorylation cascade | Complex | Growth factors |
| **cAMP Pathway** | KEGG | Second messenger system | Event broadcasting | GPCR → AC → PKA | Moderate | GPCR, AC, PKA |
| **Calcium Signaling** | Reactome | Universal second messenger | Global broadcast channel | IP3 → Ca²⁺ release | Moderate | IP3, ER stores |
| **NF-κB Pathway** | KEGG | Transcription activator | Gene expression controller | IκB degradation → nuclear translocation | Complex | Kinases, degradation |
| **Wnt Pathway** | KEGG | Development controller | State transition controller | β-catenin stabilization | Complex | Destruction complex |
| **Notch Pathway** | KEGG | Cell fate determinant | Lateral inhibition | Membrane cleavage | Moderate | Ligand, γ-secretase |
| **JAK-STAT Pathway** | KEGG | Cytokine signal transducer | Fast transcription pathway | Receptor → JAK → STAT | Moderate | Cytokine receptors |
| **mTOR Pathway** | KEGG | Nutrient sensor | Resource availability sensor | Growth/autophagy switch | Complex | Nutrients, energy |
| **TGF-β Pathway** | KEGG | Growth regulator | Development controller | SMAD phosphorylation | Moderate | Ligand, receptors |

---

## 2. Category-by-Category Deep Dives

### 2.1 Mechanisms (~300) → Update Rules

Mechanisms are the computational primitives that define how state changes over time. They are the "instruction set" of biological computation.

#### 2.1.1 Hebbian Learning → Local Correlation-Based Weight Update

**Biological Description:**
"Neurons that fire together, wire together." When pre-synaptic neuron A repeatedly participates in firing post-synaptic neuron B, the synaptic strength from A to B increases.

**Computational Primitive:**
Correlation-based weight update rule

**Mathematical Formalization:**
```
dw_ij/dt = η · x_i · y_j

where:
  w_ij = synaptic weight from neuron i to neuron j
  x_i = pre-synaptic activity (firing rate or spike)
  y_j = post-synaptic activity
  η = learning rate
```

**Pseudocode:**
```python
def hebbian_update(pre_activity, post_activity, learning_rate):
    """Hebbian weight update rule."""
    delta_w = learning_rate * pre_activity * post_activity
    return delta_w

# Usage:
weight += hebbian_update(pre_spike, post_spike, eta)
```

**OS/Architecture Analogue:**
Similar to cache locality optimization - frequently co-accessed memory locations are kept closer together. Also similar to database indexing based on query patterns.

**Implementation Difficulty:** Trivial
**Dependencies:** None
**Database References:**
- ModelDB: Multiple STDP models
- Formula DB: "Hebbian Learning Rule" (ID: varies by model)

**Computational Properties:**
- Unsupervised learning
- Local computation (only needs pre/post activity)
- Unstable without normalization (weights grow unbounded)
- Forms associative memories

**Biological Substrate:**
- NMDA receptors act as coincidence detectors
- Calcium influx triggers molecular cascades
- CaMKII phosphorylation stabilizes changes

#### 2.1.2 Spike-Timing Dependent Plasticity (STDP) → Temporal Causality Learning Rule

**Biological Description:**
Refinement of Hebbian learning that considers the precise timing of spikes. If pre fires before post (within ~20ms), strengthen synapse. If post fires before pre, weaken synapse.

**Computational Primitive:**
Temporal causality detector + asymmetric weight update

**Mathematical Formalization:**
```
         { A₊ · exp(-Δt/τ₊)    if Δt > 0 (pre before post)
dw/dt = {
         { -A₋ · exp(Δt/τ₋)    if Δt < 0 (post before pre)

where:
  Δt = t_post - t_pre (spike time difference)
  A₊, A₋ = potentiation/depression amplitudes
  τ₊, τ₋ = time constants (~20ms)
```

**Pseudocode:**
```python
def stdp_update(t_pre, t_post, A_plus=0.01, A_minus=0.01, tau_plus=20, tau_minus=20):
    """STDP weight update based on spike timing."""
    delta_t = t_post - t_pre

    if delta_t > 0:  # Pre before post → potentiation
        delta_w = A_plus * np.exp(-delta_t / tau_plus)
    else:  # Post before pre → depression
        delta_w = -A_minus * np.exp(delta_t / tau_minus)

    return delta_w

# Usage in event-driven simulation:
if pre_spike_event:
    for post_spike_time in recent_post_spikes:
        weight += stdp_update(current_time, post_spike_time)
```

**OS/Architecture Analogue:**
Similar to branch prediction in CPUs - reinforcing pathways that successfully predicted future activity. Also similar to temporal difference learning in RL.

**Implementation Difficulty:** Moderate (requires spike timing tracking)
**Dependencies:**
- Precise timing mechanism
- Spike event detection
- Short-term memory of recent spikes

**Database References:**
- ModelDB: 64261, 83319, 114242
- GO: GO:0048169 (regulation of synaptic plasticity)

**Computational Properties:**
- Learns temporal sequences
- Causal relationships
- Sensitive to precise timing (sub-millisecond)
- Self-stabilizing with appropriate parameters

**Biological Substrate:**
- Backpropagating action potentials
- NMDA receptor timing window
- Calcium transient dynamics

#### 2.1.3 Homeostatic Plasticity → Stability Constraint

**Biological Description:**
Neurons maintain target firing rate by scaling all synaptic weights up or down. Prevents runaway excitation or silence.

**Computational Primitive:**
Global normalization + target maintenance

**Mathematical Formalization:**
```
dw_i/dt = ε · w_i · (ρ₀ - ρ)

where:
  w_i = synaptic weight
  ρ = actual firing rate
  ρ₀ = target firing rate
  ε = homeostatic learning rate (slow, ~hours-days)
```

**Pseudocode:**
```python
def homeostatic_scaling(weights, actual_rate, target_rate, epsilon=1e-5, dt=1.0):
    """Scale all weights to maintain target firing rate."""
    rate_error = target_rate - actual_rate
    delta_weights = epsilon * weights * rate_error * dt
    return weights + delta_weights

# Usage (typically on slow timescale):
if time % homeostatic_update_interval == 0:
    avg_rate = compute_average_firing_rate(spike_history)
    weights = homeostatic_scaling(weights, avg_rate, target_rate)
```

**OS/Architecture Analogue:**
Similar to load balancing in distributed systems, or automatic gain control in audio systems.

**Implementation Difficulty:** Moderate
**Dependencies:**
- Firing rate monitoring
- All synaptic weights
- Slow timescale mechanism

**Database References:**
- GO: GO:0060291 (long-term synaptic potentiation)
- Literature: Turrigiano & Nelson (2004)

**Computational Properties:**
- Stabilizes learning
- Prevents saturation
- Maintains sensitivity
- Works on slow timescale (hours-days)

#### 2.1.4 Predictive Coding → Hierarchical Error Minimization

**Biological Description:**
Each cortical layer predicts activity in the layer below. Only prediction errors are propagated, reducing redundancy.

**Computational Primitive:**
Residual computation + error backpropagation

**Mathematical Formalization:**
```
Prediction: x̂_l = f(x_{l+1})    (top-down)
Error:      e_l = x_l - x̂_l     (bottom-up)
Update:     dx_{l+1}/dt = -∂E/∂x_{l+1} where E = ||e_l||²
```

**Pseudocode:**
```python
def predictive_coding_layer(input_bottom_up, prediction_top_down, learning_rate):
    """Predictive coding: compute error and update representation."""
    # Compute prediction error
    error = input_bottom_up - prediction_top_down

    # Update higher-level representation to minimize error
    delta_representation = -learning_rate * gradient_of_error(error)

    return error, delta_representation

# Hierarchical application:
for layer in reversed(hierarchy):
    prediction = layer.predict_lower_level()
    error, update = predictive_coding_layer(
        layer.input, prediction, learning_rate
    )
    layer.update_weights(update)
    layer.send_error_to_next(error)
```

**OS/Architecture Analogue:**
Similar to differential/incremental encoding in compression, or delta updates in version control systems.

**Implementation Difficulty:** Complex
**Dependencies:**
- Hierarchical architecture
- Bidirectional connections
- Prediction model

**Computational Properties:**
- Efficient coding (sparse errors)
- Hierarchical processing
- Explains away redundancy
- Bayesian interpretation

### 2.2 Processes (~2500) → Runtime Dynamics

Processes are the active behaviors that unfold over time in biological systems.

#### 2.2.1 Action Potential Propagation → Signal Routing

**Biological Description:**
Electrical spike travels along axon via sequential opening of voltage-gated ion channels. Regenerative process that doesn't degrade over distance.

**Computational Primitive:**
Wave propagation + signal regeneration

**Mathematical Formalization:**
Hodgkin-Huxley model:
```
C_m dV/dt = I_ext - g_Na·m³·h·(V - E_Na) - g_K·n⁴·(V - E_K) - g_L·(V - E_L)

dm/dt = α_m(V)·(1-m) - β_m(V)·m
dh/dt = α_h(V)·(1-h) - β_h(V)·h
dn/dt = α_n(V)·(1-n) - β_n(V)·n
```

**Pseudocode:**
```python
def action_potential_propagation(V, m, h, n, I_ext, dt):
    """Hodgkin-Huxley action potential."""
    # Voltage-dependent rate constants
    alpha_m = 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))
    beta_m = 4 * np.exp(-(V + 65) / 18)
    # ... (similar for h, n)

    # Ionic currents
    I_Na = g_Na * m**3 * h * (V - E_Na)
    I_K = g_K * n**4 * (V - E_K)
    I_L = g_L * (V - E_L)

    # Update voltage
    dV = (I_ext - I_Na - I_K - I_L) / C_m * dt

    # Update gating variables
    dm = (alpha_m * (1 - m) - beta_m * m) * dt
    dh = (alpha_h * (1 - h) - beta_h * h) * dt
    dn = (alpha_n * (1 - n) - beta_n * n) * dt

    return V + dV, m + dm, h + dh, n + dn
```

**OS/Architecture Analogue:**
Similar to signal regeneration in network repeaters, or clock signal propagation in synchronous circuits.

**Implementation Difficulty:** Complex
**Dependencies:**
- Ion channel models
- Membrane capacitance
- Spatial discretization (for cable equation)

**Database References:**
- ModelDB: 2488 (Original HH model)
- Formula DB: "Hodgkin-Huxley Membrane Equation"

#### 2.2.2 Synaptic Transmission → Message Passing

**Biological Description:**
Pre-synaptic spike triggers vesicle release, neurotransmitter diffuses across cleft, binds to post-synaptic receptors, opens ion channels, generates post-synaptic current.

**Computational Primitive:**
Event-triggered message passing with temporal dynamics

**Mathematical Formalization:**
```
Vesicle release (stochastic):
  P_release = 1 - exp(-[Ca]^n / K_d^n)

Post-synaptic current (AMPA):
  I_syn = g_syn(t) · (V - E_rev)
  dg/dt = -g/τ_decay
  g → g + Δg  (on each pre-synaptic spike)
```

**Pseudocode:**
```python
class Synapse:
    def __init__(self, tau_decay=5.0, g_max=1.0, E_rev=0.0):
        self.g = 0.0  # conductance
        self.tau_decay = tau_decay
        self.g_max = g_max
        self.E_rev = E_rev

    def on_presynaptic_spike(self):
        """Handle pre-synaptic spike arrival."""
        self.g += self.g_max  # Instantaneous jump

    def update(self, dt):
        """Exponential decay."""
        self.g *= np.exp(-dt / self.tau_decay)

    def current(self, V_post):
        """Compute post-synaptic current."""
        return self.g * (V_post - self.E_rev)
```

**OS/Architecture Analogue:**
Similar to asynchronous message passing in distributed systems, or interrupt handling in OS.

**Implementation Difficulty:** Moderate
**Dependencies:**
- Spike detection
- Receptor models
- Event queue

#### 2.2.3 Calcium Oscillations → Clock/Timing Mechanism

**Biological Description:**
Rhythmic variations in intracellular calcium concentration driven by interplay between ER calcium stores and cytoplasmic calcium.

**Computational Primitive:**
Oscillator / clock generator

**Mathematical Formalization:**
```
d[Ca]/dt = J_in - J_out + J_leak

where:
  J_in = IP3-mediated release from ER
  J_out = SERCA pump (ATP-driven)
  J_leak = passive leak from ER

Typical result: limit cycle oscillation
```

**Pseudocode:**
```python
def calcium_oscillator(Ca_cyt, Ca_ER, IP3, dt):
    """Simple calcium oscillation model."""
    # IP3-mediated release (autocatalytic)
    J_in = k_in * IP3 * (Ca_cyt / (Ca_cyt + K_act))**3 * (Ca_ER - Ca_cyt)

    # SERCA pump (active transport)
    J_out = V_max * Ca_cyt**2 / (K_pump**2 + Ca_cyt**2)

    # Leak
    J_leak = k_leak * (Ca_ER - Ca_cyt)

    # Update
    dCa_cyt = (J_in - J_out + J_leak) * dt
    dCa_ER = -dCa_cyt * (V_cyt / V_ER)  # conservation

    return Ca_cyt + dCa_cyt, Ca_ER + dCa_ER
```

**OS/Architecture Analogue:**
Similar to system clock/timer in OS, or crystal oscillator in hardware.

**Implementation Difficulty:** Moderate
**Dependencies:**
- Calcium stores model
- Pump and channel kinetics

### 2.3 Circuit Motifs (~100) → Network Patterns

Circuit motifs are recurring connectivity patterns that implement specific computational functions.

#### 2.3.1 Feedforward Inhibition → Temporal Precision Gate

**Biological Description:**
Excitatory input simultaneously activates target neuron AND inhibitory interneuron. The interneuron then inhibits the target with a slight delay, creating a narrow time window for excitation.

**Computational Primitive:**
Coincidence detection + temporal gating

**Network Topology:**
```
Input → [Excitatory] → Target
   ↓
   [Inhibitory Interneuron] → Target (delayed)
```

**Mathematical Formalization:**
```
Target receives:
  I_exc(t) = w_exc · input(t)
  I_inh(t) = w_inh · input(t - Δt)

Effective window: Target fires only if input during Δt window
```

**Pseudocode:**
```python
class FeedforwardInhibition:
    def __init__(self, w_exc=1.0, w_inh=0.8, delay=5.0):
        self.w_exc = w_exc
        self.w_inh = w_inh
        self.delay_buffer = []  # Stores (time, value) tuples
        self.delay = delay

    def process(self, input_signal, current_time):
        """Process input through FFI circuit."""
        # Excitatory path (immediate)
        excitation = self.w_exc * input_signal

        # Inhibitory path (delayed)
        self.delay_buffer.append((current_time, input_signal))

        # Remove old entries and compute delayed inhibition
        inhibition = 0
        for t, val in self.delay_buffer:
            if current_time - t >= self.delay:
                inhibition += self.w_inh * val
                self.delay_buffer.remove((t, val))

        return excitation - inhibition
```

**OS/Architecture Analogue:**
Similar to pulse shaping in digital circuits, or time-window authentication in security systems.

**Implementation Difficulty:** Moderate
**Dependencies:**
- Delay mechanism
- Inhibitory neurons

**Computational Properties:**
- Temporal precision
- Coincidence detection
- Noise rejection
- Spike timing control

#### 2.3.2 Recurrent Excitation → Working Memory Buffer

**Biological Description:**
Neurons excite each other in a loop, maintaining activity even after input is removed. Enables short-term memory.

**Computational Primitive:**
Attractor state / persistent activity

**Network Topology:**
```
    ┌───────┐
    │   A   │──┐
    └───────┘  │
        ↑      ↓
    ┌───────────┐
    │           │
    └───────────┘
  (recurrent connections)
```

**Mathematical Formalization:**
```
dy/dt = -y + f(W_rec · y + W_in · x)

where:
  y = neural activity (state)
  W_rec = recurrent weight matrix
  W_in = input weights
  f = nonlinear activation

Stable states occur where dy/dt = 0
```

**Pseudocode:**
```python
class RecurrentNetwork:
    def __init__(self, n_units, W_rec, W_in, tau=10.0):
        self.y = np.zeros(n_units)  # Neural state
        self.W_rec = W_rec  # Recurrent weights
        self.W_in = W_in    # Input weights
        self.tau = tau

    def update(self, input_signal, dt):
        """Update recurrent network state."""
        # Recurrent + input drive
        drive = np.dot(self.W_rec, self.y) + np.dot(self.W_in, input_signal)

        # Nonlinear activation
        activated = np.tanh(drive)

        # Leaky integration
        dy = (-self.y + activated) / self.tau * dt
        self.y += dy

        return self.y

    def reset(self):
        """Clear working memory."""
        self.y = np.zeros_like(self.y)
```

**OS/Architecture Analogue:**
Similar to SRAM cells (cross-coupled inverters), or register files in CPU.

**Implementation Difficulty:** Complex
**Dependencies:**
- Recurrent connectivity
- Nonlinear dynamics
- Stable attractor states

**Computational Properties:**
- Persistent activity
- Multiple stable states
- Content-addressable memory
- Sensitive to initial conditions

#### 2.3.3 Lateral Inhibition → Winner-Take-All Selection

**Biological Description:**
Neurons inhibit their neighbors. The most active neuron suppresses all others, implementing competitive selection.

**Computational Primitive:**
Competitive dynamics / argmax operation

**Mathematical Formalization:**
```
dy_i/dt = -y_i + f(x_i - Σ_{j≠i} w_ij · y_j)

Strong lateral inhibition → winner-take-all
Weak lateral inhibition → sparse coding
```

**Pseudocode:**
```python
def winner_take_all(inputs, inhibition_strength=1.0, dt=0.1, steps=100):
    """Simulate WTA network via lateral inhibition."""
    y = np.zeros_like(inputs)

    for _ in range(steps):
        # Each neuron receives its input minus inhibition from all others
        total_inhibition = inhibition_strength * np.sum(y)
        dy = -y + np.maximum(0, inputs - total_inhibition + y)
        y += dy * dt

    return y

# Result: highest input dominates, others suppressed
```

**OS/Architecture Analogue:**
Similar to priority-based scheduling, or competitive resource allocation.

**Implementation Difficulty:** Moderate
**Dependencies:**
- All-to-all inhibition or global inhibition pool

**Computational Properties:**
- Selection/decision making
- Sparse coding
- Normalization
- Competition

---

## 3. Computational Primitives Library

This section catalogs ~75 universal computational primitives that biology implements, organized by function.

### 3.1 Signal Processing Primitives

#### 3.1.1 Gating (Conditional Execution)

**Biological Implementation:**
Voltage-gated ion channels, NMDA receptors (voltage + ligand), neuromodulation

**Mathematical Form:**
```
output = input if condition else 0
# Smooth version:
output = input · σ(gate_signal)
```

**Pseudocode:**
```python
def gating(signal, gate, threshold=0.5):
    """Conditional signal transmission."""
    return signal if gate > threshold else 0

# Smooth gating:
def smooth_gating(signal, gate):
    return signal * sigmoid(gate)
```

**OS/Architecture Analogue:**
Multiplexer, conditional execution (if statements), interrupt masking

**Use Cases:**
- Attention mechanisms
- Conditional routing
- Modulation
- State-dependent processing

#### 3.1.2 Amplification (Signal Boosting)

**Biological Implementation:**
Synaptic transmission (1 vesicle → 1000s of ions), signaling cascades (MAPK: 1:100:10000 amplification), dendritic spikes

**Mathematical Form:**
```
output = gain · input
# Nonlinear amplification:
output = input^n (cooperativity/ultrasensitivity)
```

**Pseudocode:**
```python
def linear_amplification(signal, gain):
    return gain * signal

def nonlinear_amplification(signal, n=4, K=1.0):
    """Hill equation amplification."""
    return signal**n / (K**n + signal**n)
```

**OS/Architecture Analogue:**
Operational amplifier, signal repeater, cascade multiplication

**Use Cases:**
- Signal transduction
- Threshold detection
- Noise suppression (via threshold)

#### 3.1.3 Integration (Summation)

**Biological Implementation:**
Dendritic summation of synaptic inputs, temporal integration by membrane capacitance

**Mathematical Form:**
```
# Spatial:
y = Σ w_i · x_i

# Temporal:
τ dy/dt = -y + x
```

**Pseudocode:**
```python
def spatial_integration(inputs, weights):
    """Weighted sum."""
    return np.dot(weights, inputs)

def temporal_integration(y, input, tau, dt):
    """Leaky integrator."""
    dy = (-y + input) / tau * dt
    return y + dy
```

**OS/Architecture Analogue:**
Accumulator register, summation in CPU, running average

**Use Cases:**
- Evidence accumulation
- Decision making
- Filtering
- Averaging

#### 3.1.4 Differentiation (Rate of Change Detection)

**Biological Implementation:**
Adaptation currents, high-pass filtering in sensory systems, velocity detection

**Mathematical Form:**
```
y = dx/dt

# Discrete:
y[t] = (x[t] - x[t-1]) / dt
```

**Pseudocode:**
```python
def differentiation(signal_history, dt):
    """Temporal derivative."""
    if len(signal_history) < 2:
        return 0
    return (signal_history[-1] - signal_history[-2]) / dt

# Smooth differentiation:
def adaptive_differentiation(x, x_prev, y_prev, tau, dt):
    """High-pass filter."""
    alpha = tau / (tau + dt)
    return alpha * (y_prev + x - x_prev)
```

**OS/Architecture Analogue:**
Edge detection in image processing, change detection in databases

**Use Cases:**
- Motion detection
- Edge detection
- Change detection
- Velocity encoding

#### 3.1.5 Normalization

**Biological Implementation:**
Divisive normalization in cortex, synaptic scaling, gain control

**Mathematical Form:**
```
y_i = x_i / (σ + Σ x_j)

# Alternatives:
# L2 norm: y = x / ||x||
# Softmax: y_i = exp(x_i) / Σ exp(x_j)
```

**Pseudocode:**
```python
def divisive_normalization(inputs, sigma=1.0):
    """Divisive normalization."""
    total = np.sum(inputs) + sigma
    return inputs / total

def softmax_normalization(inputs, temperature=1.0):
    """Softmax (temperature-controlled)."""
    exp_inputs = np.exp(inputs / temperature)
    return exp_inputs / np.sum(exp_inputs)
```

**OS/Architecture Analogue:**
Automatic gain control, normalization in machine learning

**Use Cases:**
- Dynamic range compression
- Probability distributions
- Attention weights
- Invariance

### 3.2 Memory Primitives

#### 3.2.1 Short-Term Memory (Working Memory)

**Biological Implementation:**
Recurrent excitation, persistent activity in PFC

**Mathematical Form:**
```
dy/dt = -y + f(W_rec·y + input)
# Bistable if W_rec eigenvalues > 1
```

**Pseudocode:**
```python
class WorkingMemory:
    def __init__(self, size, W_rec):
        self.state = np.zeros(size)
        self.W_rec = W_rec

    def update(self, input, dt):
        drive = np.dot(self.W_rec, self.state) + input
        dy = (-self.state + np.tanh(drive)) * dt
        self.state += dy

    def read(self):
        return self.state

    def clear(self):
        self.state = np.zeros_like(self.state)
```

**OS/Architecture Analogue:**
CPU registers, cache memory, RAM

#### 3.2.2 Long-Term Memory (Associative)

**Biological Implementation:**
Synaptic weights modified by plasticity (Hebbian, STDP)

**Mathematical Form:**
```
# Hebbian storage:
W = Σ x_i ⊗ x_i  (outer product)

# Retrieval:
y = sign(W · x_query)
```

**Pseudocode:**
```python
class HopfieldNetwork:
    def __init__(self, size):
        self.W = np.zeros((size, size))
        np.fill_diagonal(self.W, 0)  # No self-connections

    def store(self, pattern):
        """Store pattern (Hebbian rule)."""
        pattern = np.sign(pattern)
        self.W += np.outer(pattern, pattern)
        np.fill_diagonal(self.W, 0)

    def recall(self, query, steps=10):
        """Retrieve pattern from partial cue."""
        state = np.sign(query)
        for _ in range(steps):
            state = np.sign(np.dot(self.W, state))
        return state
```

**OS/Architecture Analogue:**
Content-addressable memory (CAM), hash tables

#### 3.2.3 Sequence Memory

**Biological Implementation:**
STDP, time cells in hippocampus, phase precession

**Mathematical Form:**
```
# Asymmetric Hebbian:
dW_ij/dt = x_i(t) · x_j(t + τ)
# Strengthens i→j if j follows i
```

**Pseudocode:**
```python
class SequenceMemory:
    def __init__(self, size):
        self.W = np.zeros((size, size))
        self.history = []

    def learn_sequence(self, sequence, learning_rate=0.01):
        """Learn temporal sequence."""
        for i in range(len(sequence) - 1):
            current = sequence[i]
            next_item = sequence[i + 1]
            self.W[current, next_item] += learning_rate

    def recall_next(self, current_state):
        """Predict next state."""
        activation = np.dot(self.W.T, current_state)
        return np.argmax(activation)
```

**OS/Architecture Analogue:**
Markov chain, n-gram models, state machines

### 3.3 Pattern Matching Primitives

#### 3.3.1 Template Matching

**Biological Implementation:**
Receptive fields in sensory cortex, grandmother cells

**Mathematical Form:**
```
similarity = <template, input> / (||template|| · ||input||)
# Cosine similarity
```

**Pseudocode:**
```python
def template_matching(input_pattern, templates):
    """Find best matching template."""
    similarities = []
    for template in templates:
        # Cosine similarity
        sim = np.dot(input_pattern, template)
        sim /= (np.linalg.norm(input_pattern) * np.linalg.norm(template))
        similarities.append(sim)

    best_match = np.argmax(similarities)
    return best_match, similarities[best_match]
```

**OS/Architecture Analogue:**
Pattern matching in compilers, template engines

#### 3.3.2 Feature Detection

**Biological Implementation:**
Simple and complex cells in V1 (edge, orientation detection)

**Mathematical Form:**
```
response = Σ w_i · x_i
# With spatial receptive field w_i
```

**Pseudocode:**
```python
def gabor_filter(image, theta, frequency, sigma):
    """Orientation-selective feature detector (V1 simple cell)."""
    # Create Gabor filter
    x, y = np.meshgrid(range(-size, size), range(-size, size))
    x_theta = x * np.cos(theta) + y * np.sin(theta)
    y_theta = -x * np.sin(theta) + y * np.cos(theta)

    gabor = np.exp(-(x_theta**2 + y_theta**2) / (2*sigma**2))
    gabor *= np.cos(2 * np.pi * frequency * x_theta)

    # Convolve with image
    response = convolve(image, gabor)
    return response
```

### 3.4 Decision Making Primitives

#### 3.4.1 Threshold Detection

**Biological Implementation:**
Spike generation threshold, all-or-none responses

**Mathematical Form:**
```
output = 1 if input > threshold else 0
# Smooth: output = σ((input - threshold)/sharpness)
```

**Pseudocode:**
```python
def threshold_detection(signal, threshold, sharpness=1.0):
    """Binary or smooth threshold."""
    if sharpness == float('inf'):
        return 1.0 if signal > threshold else 0.0
    else:
        return 1.0 / (1.0 + np.exp(-(signal - threshold) / sharpness))
```

#### 3.4.2 Winner-Take-All

**Biological Implementation:**
Lateral inhibition, competitive dynamics

**Pseudocode:**
```python
def winner_take_all(inputs):
    """Select strongest input."""
    output = np.zeros_like(inputs)
    winner = np.argmax(inputs)
    output[winner] = inputs[winner]
    return output

# Soft WTA:
def soft_winner_take_all(inputs, temperature=1.0):
    """Softmax-based WTA."""
    return np.exp(inputs/temperature) / np.sum(np.exp(inputs/temperature))
```

#### 3.4.3 Evidence Accumulation

**Biological Implementation:**
Drift-diffusion in decision making (LIP neurons)

**Mathematical Form:**
```
dy/dt = evidence + noise
Decision when y > threshold
```

**Pseudocode:**
```python
class DriftDiffusion:
    def __init__(self, threshold=1.0, noise_std=0.1):
        self.evidence = 0.0
        self.threshold = threshold
        self.noise_std = noise_std

    def update(self, input_evidence, dt):
        """Accumulate evidence."""
        noise = np.random.normal(0, self.noise_std * np.sqrt(dt))
        self.evidence += (input_evidence + noise) * dt

        # Check decision
        if abs(self.evidence) > self.threshold:
            decision = np.sign(self.evidence)
            self.evidence = 0  # Reset
            return decision
        return None  # No decision yet
```

### 3.5 Temporal Primitives

#### 3.5.1 Delay

**Biological Implementation:**
Axonal propagation delay, synaptic delay

**Pseudocode:**
```python
class DelayLine:
    def __init__(self, delay_steps):
        self.buffer = [0] * delay_steps

    def process(self, input_signal):
        """Delay signal by fixed amount."""
        self.buffer.append(input_signal)
        output = self.buffer.pop(0)
        return output
```

#### 3.5.2 Oscillation

**Biological Implementation:**
Central pattern generators, gamma/theta oscillations

**Mathematical Form:**
```
dx/dt = ω·y
dy/dt = -ω·x
# Generates sinusoidal oscillation at frequency ω
```

**Pseudocode:**
```python
class NeuralOscillator:
    def __init__(self, frequency):
        self.x = 1.0
        self.y = 0.0
        self.omega = 2 * np.pi * frequency

    def update(self, dt):
        """Generate oscillation."""
        dx = self.omega * self.y * dt
        dy = -self.omega * self.x * dt
        self.x += dx
        self.y += dy
        return self.x  # Output
```

#### 3.5.3 Coincidence Detection

**Biological Implementation:**
MSO neurons (sound localization), NMDA receptors

**Pseudocode:**
```python
def coincidence_detection(input_A, input_B, time_window=5.0):
    """Detect simultaneous events."""
    return input_A * input_B  # Simple multiplicative
    # Or check if both above threshold within time window
```

### 3.6 Transform Primitives

#### 3.6.1 Fourier Analysis

**Biological Implementation:**
Cochlear filtering (tonotopic organization)

**Mathematical Form:**
```
F(ω) = ∫ f(t) · e^(-iωt) dt
```

**Biological Analogue:**
Bank of bandpass filters (hair cells in cochlea)

#### 3.6.2 Dimensionality Reduction

**Biological Implementation:**
Retinal ganglion cells (100M photoreceptors → 1M RGCs)

**Mathematical Form:**
```
y = W^T · x  where W captures principal components
```

**Pseudocode:**
```python
def pca_projection(data, n_components):
    """Biological dimensionality reduction."""
    # Compute covariance matrix
    cov = np.cov(data.T)
    # Get top eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(cov)
    idx = eigenvalues.argsort()[::-1]
    W = eigenvectors[:, idx[:n_components]]
    # Project
    return np.dot(data, W)
```

#### 3.6.3 Coordinate Transform

**Biological Implementation:**
Head-centered → world-centered (parietal cortex), retinotopic → spatiotopic

**Pseudocode:**
```python
def coordinate_transform(input_coords, transform_matrix):
    """Transform between reference frames."""
    return np.dot(transform_matrix, input_coords)
```

### 3.7 Learning Primitives

#### 3.7.1 Supervised Learning

**Biological Implementation:**
Cerebellum (climbing fiber = error signal)

**Mathematical Form:**
```
dw/dt = η · error · input
# Perceptron/delta rule
```

**Pseudocode:**
```python
def supervised_learning(weights, inputs, target, actual, learning_rate):
    """Error-driven learning."""
    error = target - actual
    delta_w = learning_rate * error * inputs
    return weights + delta_w
```

#### 3.7.2 Reinforcement Learning

**Biological Implementation:**
Dopamine = reward prediction error, basal ganglia

**Mathematical Form:**
```
δ = r + γV(s') - V(s)  # TD error
dw/dt = η · δ · x
```

**Pseudocode:**
```python
def td_learning(V, state, next_state, reward, gamma=0.9, learning_rate=0.1):
    """Temporal difference learning."""
    td_error = reward + gamma * V[next_state] - V[state]
    V[state] += learning_rate * td_error
    return td_error
```

#### 3.7.3 Unsupervised Learning

**Biological Implementation:**
Hebbian plasticity, self-organization

**Mathematical Form:**
```
dw/dt = η · (x - w) · y
# Competitive learning
```

**Pseudocode:**
```python
def competitive_learning(weights, input, learning_rate):
    """Self-organizing learning."""
    # Find best matching unit
    similarities = np.dot(weights, input)
    winner = np.argmax(similarities)

    # Update winner
    weights[winner] += learning_rate * (input - weights[winner])
    return weights
```

### 3.8 Summary Table of Primitives

| Primitive | Biological Implementation | Computational Class | Math Form | Difficulty |
|-----------|--------------------------|---------------------|-----------|------------|
| **Gating** | Voltage-gated channels | Conditional execution | `y = x if c else 0` | Trivial |
| **Amplification** | Signaling cascades | Signal multiplication | `y = g·x` or `y = x^n` | Trivial |
| **Integration** | Dendritic summation | Accumulation | `y = Σw·x` | Trivial |
| **Differentiation** | Adaptation currents | Change detection | `y = dx/dt` | Moderate |
| **Normalization** | Divisive normalization | Scaling | `y = x/Σx` | Trivial |
| **Threshold** | Spike generation | Binary decision | `y = H(x-θ)` | Trivial |
| **Winner-Take-All** | Lateral inhibition | Selection | Competitive dynamics | Moderate |
| **Evidence Accumulation** | Drift-diffusion | Sequential integration | `dy = evidence·dt` | Moderate |
| **Oscillation** | Central pattern generators | Periodic signal | Limit cycle | Moderate |
| **Coincidence Detection** | NMDA, MSO neurons | AND gate | `y = x₁·x₂` | Trivial |
| **Template Matching** | Receptive fields | Pattern recognition | Cosine similarity | Moderate |
| **Feature Detection** | V1 simple cells | Filtering | Convolution | Moderate |
| **Delay** | Axonal propagation | Time shifting | Buffer | Trivial |
| **Working Memory** | Recurrent excitation | State maintenance | Attractor dynamics | Complex |
| **Associative Memory** | Hebbian plasticity | Content retrieval | Outer product | Complex |
| **Sequence Memory** | STDP | Temporal patterns | Asymmetric Hebbian | Complex |
| **PCA** | Retinal compression | Dimensionality reduction | Eigenvectors | Complex |
| **Coordinate Transform** | Parietal cortex | Reference frame change | Matrix multiplication | Moderate |

---

## 4. Architecture Patterns Catalog

This section documents ~50 architectural patterns inspired by biological systems.

### 4.1 Memory Architectures

#### 4.1.1 Sparse Distributed Memory (SDM)

**Biological Inspiration:**
Hippocampus, cortical encoding (sparse activation ~2-5%)

**Key Mechanisms:**
- Sparse coding (few active neurons)
- Distributed representation (information across population)
- Content-addressable retrieval

**Computational Properties:**
- Fault tolerance (graceful degradation)
- Large capacity (exponential in sparsity)
- Pattern completion
- Noise resistance

**Mathematical Description:**
```
Encoding: Select k out of N neurons (k << N)
Storage: W += x ⊗ y  (Hebbian)
Retrieval: y' = f(W · x')  where x' is partial cue
```

**Implementation Sketch:**
```python
class SparseDistributedMemory:
    def __init__(self, n_neurons=10000, sparsity=0.02):
        self.n_neurons = n_neurons
        self.k_active = int(n_neurons * sparsity)
        self.W = np.zeros((n_neurons, n_neurons))

    def encode(self, pattern):
        """Convert dense input to sparse representation."""
        # Select top-k activations
        indices = np.argpartition(pattern, -self.k_active)[-self.k_active:]
        sparse = np.zeros(self.n_neurons)
        sparse[indices] = 1
        return sparse

    def store(self, key, value):
        """Store association."""
        key_sparse = self.encode(key)
        value_sparse = self.encode(value)
        self.W += np.outer(key_sparse, value_sparse)

    def retrieve(self, key_partial):
        """Retrieve from partial key."""
        key_sparse = self.encode(key_partial)
        activation = np.dot(self.W.T, key_sparse)
        return self.encode(activation)  # Re-sparsify
```

**Use Cases:**
- Long-term memory systems
- Pattern recognition databases
- Fault-tolerant storage
- Associative retrieval

**Database References:**
- Related to hippocampal CA3 models (ModelDB)
- Sparse coding in V1 (Olshausen & Field, 1996)

#### 4.1.2 Attractor Networks

**Biological Inspiration:**
Persistent activity in prefrontal cortex, grid cells, head direction cells

**Key Mechanisms:**
- Recurrent excitation
- Feedback stabilization
- Multiple stable states

**Computational Properties:**
- Working memory
- Continuous attractors (smooth manifolds)
- Discrete attractors (point attractors)
- Error correction

**Mathematical Description:**
```
dy/dt = -y + f(W_rec·y + input)

Stable states: dy/dt = 0
Continuous attractor: 1D ring of stable states
```

**Implementation Sketch:**
```python
class AttractorNetwork:
    def __init__(self, n_units, W_rec):
        self.y = np.zeros(n_units)
        self.W_rec = W_rec  # Design for desired attractor structure
        self.tau = 10.0

    def update(self, input, dt):
        """Evolve network dynamics."""
        recurrent = np.dot(self.W_rec, self.y)
        dy = (-self.y + np.tanh(recurrent + input)) / self.tau * dt
        self.y += dy
        return self.y

    @staticmethod
    def create_ring_attractor(n_units, connection_width):
        """Create continuous ring attractor connectivity."""
        W = np.zeros((n_units, n_units))
        for i in range(n_units):
            for j in range(n_units):
                # Distance on ring
                dist = min(abs(i-j), n_units - abs(i-j))
                W[i,j] = np.exp(-dist**2 / (2*connection_width**2))
        return W
```

**Use Cases:**
- Working memory
- Spatial navigation
- Motor planning
- Decision making

#### 4.1.3 Hierarchical Temporal Memory (HTM)

**Biological Inspiration:**
Cortical columns, hierarchical processing in neocortex

**Key Mechanisms:**
- Spatial pooling (column formation)
- Temporal pooling (sequence learning)
- Hierarchical structure
- Sparse distributed representations

**Computational Properties:**
- Online learning
- Temporal pattern recognition
- Hierarchical abstraction
- Invariance learning

**Implementation Sketch:**
```python
class HTMRegion:
    def __init__(self, n_columns, cells_per_column):
        self.columns = [HTMColumn(cells_per_column) for _ in range(n_columns)]
        self.active_columns = set()

    def spatial_pooling(self, input_sdr):
        """Find active columns based on input overlap."""
        overlaps = [col.compute_overlap(input_sdr) for col in self.columns]
        # Inhibition: select top-k
        k = int(len(self.columns) * 0.02)  # 2% active
        winners = np.argpartition(overlaps, -k)[-k:]
        self.active_columns = set(winners)
        return self.active_columns

    def temporal_pooling(self, prev_active_cells):
        """Predict next active cells based on sequences."""
        predicted_cells = set()
        for col_idx in self.active_columns:
            predicted = self.columns[col_idx].get_predicted_cells(prev_active_cells)
            predicted_cells.update(predicted)
        return predicted_cells
```

**Use Cases:**
- Anomaly detection
- Sequence prediction
- Streaming data analysis
- Hierarchical classification

### 4.2 Processing Architectures

#### 4.2.1 Liquid State Machines (LSM)

**Biological Inspiration:**
Cortical microcircuits, recurrent connectivity in cortex

**Key Mechanisms:**
- Recurrent reservoir of neurons
- High-dimensional temporal dynamics
- Linear readout layer

**Computational Properties:**
- Universal function approximation
- Temporal pattern recognition
- Fading memory
- Real-time processing

**Mathematical Description:**
```
Reservoir: dx/dt = -x + tanh(W_res·x + W_in·u)
Readout:   y = W_out · x
```

**Implementation Sketch:**
```python
class LiquidStateMachine:
    def __init__(self, n_reservoir=1000, n_inputs=10, n_outputs=5):
        # Random recurrent reservoir
        self.W_res = np.random.randn(n_reservoir, n_reservoir) * 0.5
        self.W_res /= np.max(np.abs(np.linalg.eigvals(self.W_res)))  # Stability

        # Input and output weights
        self.W_in = np.random.randn(n_reservoir, n_inputs) * 0.1
        self.W_out = np.random.randn(n_outputs, n_reservoir) * 0.1

        self.x = np.zeros(n_reservoir)
        self.tau = 10.0

    def update(self, input, dt):
        """Update reservoir state."""
        activation = np.dot(self.W_res, self.x) + np.dot(self.W_in, input)
        dx = (-self.x + np.tanh(activation)) / self.tau * dt
        self.x += dx

        # Compute output
        output = np.dot(self.W_out, self.x)
        return output

    def train_readout(self, input_sequence, target_sequence):
        """Train output weights (linear regression)."""
        states = []
        for inp in input_sequence:
            self.update(inp, dt=0.1)
            states.append(self.x.copy())

        X = np.array(states)
        Y = np.array(target_sequence)
        self.W_out = np.linalg.lstsq(X, Y, rcond=None)[0].T
```

**Use Cases:**
- Speech recognition
- Time series prediction
- Robot control
- Real-time classification

#### 4.2.2 Predictive Coding Networks

**Biological Inspiration:**
Cortical hierarchy (feedback predicts, feedforward carries error)

**Key Mechanisms:**
- Top-down prediction
- Bottom-up error
- Hierarchical error minimization

**Computational Properties:**
- Efficient coding
- Invariance learning
- Attention (precision weighting)
- Bayesian inference

**Mathematical Description:**
```
Level l:
  Prediction: x̂_l = f(x_{l+1})     (top-down)
  Error:      e_l = x_l - x̂_l      (bottom-up)
  Update:     dx_{l+1}/dt = -∂E/∂x_{l+1}
```

**Implementation Sketch:**
```python
class PredictiveCodingNetwork:
    def __init__(self, layer_sizes):
        self.n_layers = len(layer_sizes)
        self.representations = [np.zeros(size) for size in layer_sizes]
        self.errors = [np.zeros(size) for size in layer_sizes[:-1]]
        self.weights = [np.random.randn(layer_sizes[i+1], layer_sizes[i]) * 0.1
                       for i in range(len(layer_sizes)-1)]

    def forward_pass(self, input_data):
        """Compute predictions and errors."""
        self.representations[0] = input_data

        # Top-down predictions
        for l in range(self.n_layers - 1, 0, -1):
            prediction = np.dot(self.weights[l-1].T, self.representations[l])
            self.errors[l-1] = self.representations[l-1] - prediction

    def update_representations(self, learning_rate):
        """Minimize prediction error."""
        for l in range(1, self.n_layers):
            # Error from below
            error_below = self.errors[l-1] if l > 0 else 0
            # Error from above
            error_above = (np.dot(self.weights[l], self.errors[l])
                          if l < self.n_layers-1 else 0)

            # Update to minimize error
            delta = learning_rate * (error_below - error_above)
            self.representations[l] += delta
```

**Use Cases:**
- Vision (invariance, object recognition)
- Sensory prediction
- Attention mechanisms
- Compression

#### 4.2.3 Spiking Neural Networks (SNN)

**Biological Inspiration:**
Actual neuron spiking dynamics

**Key Mechanisms:**
- Discrete spike events
- Temporal coding
- Asynchronous processing
- Energy efficiency

**Computational Properties:**
- Event-driven computation
- Low power consumption
- Temporal precision
- Neuromorphic hardware compatible

**Implementation Sketch:**
```python
class SpikingNeuralNetwork:
    def __init__(self, n_neurons, connectivity):
        self.V = np.random.rand(n_neurons) * -70  # Membrane potential
        self.threshold = -55  # mV
        self.reset = -70
        self.W = connectivity
        self.spike_times = [[] for _ in range(n_neurons)]

    def update(self, I_ext, t, dt=0.1):
        """LIF neuron dynamics."""
        tau = 20.0  # ms

        # Synaptic input from spikes
        I_syn = np.zeros(len(self.V))
        # (Would process recent spikes here with synaptic kernels)

        # Membrane dynamics
        dV = (-(self.V - self.reset) + I_ext + I_syn) / tau * dt
        self.V += dV

        # Check for spikes
        spiked = self.V > self.threshold
        self.V[spiked] = self.reset

        # Record spike times
        for idx in np.where(spiked)[0]:
            self.spike_times[idx].append(t)

        return spiked
```

**Use Cases:**
- Neuromorphic computing
- Real-time processing
- Low-power AI
- Temporal pattern recognition

### 4.3 Control Architectures

#### 4.3.1 Actor-Critic (Basal Ganglia)

**Biological Inspiration:**
Basal ganglia: striatum (actor) + dopamine (critic)

**Key Mechanisms:**
- Policy (actor): selects actions
- Value function (critic): evaluates states
- TD error: dopamine signal

**Computational Properties:**
- Reinforcement learning
- Credit assignment
- Exploration vs exploitation
- Online learning

**Implementation Sketch:**
```python
class ActorCritic:
    def __init__(self, n_states, n_actions):
        self.actor_weights = np.random.randn(n_actions, n_states) * 0.1
        self.critic_weights = np.random.randn(n_states) * 0.1

    def select_action(self, state):
        """Actor: policy."""
        logits = np.dot(self.actor_weights, state)
        probs = np.exp(logits) / np.sum(np.exp(logits))
        return np.random.choice(len(probs), p=probs)

    def td_error(self, state, next_state, reward, gamma=0.9):
        """Critic: temporal difference error (dopamine)."""
        V_current = np.dot(self.critic_weights, state)
        V_next = np.dot(self.critic_weights, next_state)
        return reward + gamma * V_next - V_current

    def update(self, state, action, next_state, reward, alpha=0.01):
        """Update both actor and critic."""
        td_err = self.td_error(state, next_state, reward)

        # Update critic (value function)
        self.critic_weights += alpha * td_err * state

        # Update actor (policy)
        self.actor_weights[action] += alpha * td_err * state
```

**Use Cases:**
- Reinforcement learning
- Robot control
- Game playing
- Decision making

#### 4.3.2 Cerebellum-like Controller

**Biological Inspiration:**
Cerebellum: supervised learning of motor control

**Key Mechanisms:**
- Parallel fibers (context)
- Purkinje cells (output)
- Climbing fibers (error signal)
- Perceptron-like learning

**Computational Properties:**
- Supervised learning
- Motor control
- Timing and coordination
- Error correction

**Implementation Sketch:**
```python
class CerebellumController:
    def __init__(self, n_parallel_fibers, n_purkinje_cells):
        # Parallel fiber → Purkinje cell weights
        self.W = np.random.randn(n_purkinje_cells, n_parallel_fibers) * 0.01

    def predict(self, context):
        """Purkinje cell output."""
        return np.dot(self.W, context)

    def learn_from_error(self, context, error, learning_rate=0.01):
        """Climbing fiber teaches Purkinje cells."""
        # Simple perceptron-like rule
        self.W -= learning_rate * np.outer(error, context)

    def control_loop(self, context, desired_output):
        """Execute and learn."""
        actual_output = self.predict(context)
        error = actual_output - desired_output
        self.learn_from_error(context, error)
        return actual_output
```

**Use Cases:**
- Motor control
- Adaptive filtering
- Predictive control
- Timing tasks

### 4.4 Sensory Processing Architectures

#### 4.4.1 Retinal Preprocessing

**Biological Inspiration:**
Retina: center-surround, edge detection, adaptation

**Key Mechanisms:**
- Center-surround receptive fields
- Temporal filtering
- Automatic gain control
- Dimensionality reduction (100M → 1M)

**Computational Properties:**
- Edge enhancement
- Compression
- Adaptation to mean luminance
- Motion detection

**Implementation Sketch:**
```python
class RetinaPreprocessing:
    def __init__(self, image_size):
        self.center_surround_filter = self.create_dog_filter()
        self.adaptation_state = 0.5

    def create_dog_filter(self):
        """Difference of Gaussians (center-surround)."""
        # Approximates retinal ganglion cell RF
        center = gaussian_filter(sigma=1.0)
        surround = gaussian_filter(sigma=3.0)
        return center - 0.5 * surround

    def process(self, image):
        """Retinal processing pipeline."""
        # 1. Adaptation (automatic gain control)
        adapted = image / (self.adaptation_state + 0.1)
        self.adaptation_state = 0.9 * self.adaptation_state + 0.1 * np.mean(image)

        # 2. Center-surround filtering
        edges = convolve(adapted, self.center_surround_filter)

        # 3. Temporal filtering (difference)
        # (would store previous frame)

        return edges
```

**Use Cases:**
- Image preprocessing
- Edge detection
- Compression
- Feature extraction

#### 4.4.2 Cochlear Processing

**Biological Inspiration:**
Cochlea: tonotopic organization, bandpass filtering

**Key Mechanisms:**
- Bank of bandpass filters
- Logarithmic frequency spacing
- Hair cell transduction
- Temporal encoding

**Implementation Sketch:**
```python
class CochlearModel:
    def __init__(self, n_channels=128, sr=44100):
        self.n_channels = n_channels
        self.filters = self.create_gammatone_filterbank(sr)

    def create_gammatone_filterbank(self, sr):
        """Cochlear-like filterbank."""
        # Logarithmically spaced center frequencies
        f_min, f_max = 100, sr/2
        center_freqs = np.logspace(np.log10(f_min), np.log10(f_max), self.n_channels)

        filters = []
        for fc in center_freqs:
            # Gammatone filter (models basilar membrane)
            filters.append(GammatoneFilter(fc, sr))
        return filters

    def process(self, audio_signal):
        """Cochlear filtering."""
        outputs = []
        for filt in self.filters:
            filtered = filt.apply(audio_signal)
            # Hair cell transduction (rectification + compression)
            transduced = np.maximum(0, filtered) ** 0.3
            outputs.append(transduced)
        return np.array(outputs)
```

**Use Cases:**
- Audio preprocessing
- Speech recognition
- Sound localization
- Auditory scene analysis

### 4.5 Summary of Patterns

| Pattern | Brain Region | Computational Function | Key Property | Difficulty |
|---------|--------------|------------------------|--------------|------------|
| **Sparse Distributed Memory** | Hippocampus | Associative memory | Fault tolerance | Complex |
| **Attractor Networks** | PFC, entorhinal cortex | Working memory | Stable states | Complex |
| **Hierarchical Temporal Memory** | Neocortex | Sequence learning | Online learning | Complex |
| **Liquid State Machines** | Cortical microcircuits | Temporal processing | Reservoir computing | Moderate |
| **Predictive Coding** | Cortical hierarchy | Efficient coding | Error minimization | Complex |
| **Spiking Neural Networks** | All of brain | Event-driven processing | Energy efficiency | Complex |
| **Actor-Critic** | Basal ganglia | Reinforcement learning | Policy optimization | Complex |
| **Cerebellum Controller** | Cerebellum | Motor control | Supervised learning | Moderate |
| **Retinal Preprocessing** | Retina | Edge detection | Center-surround | Moderate |
| **Cochlear Processing** | Cochlea | Frequency analysis | Tonotopic filtering | Moderate |
| **Convolutional Hierarchy** | Visual cortex | Feature abstraction | Spatial invariance | Moderate |
| **Recurrent Neural Networks** | Cortex (general) | Temporal patterns | Memory | Moderate |
| **Hopfield Networks** | Cortex (memory) | Pattern completion | Energy minimization | Moderate |
| **Self-Organizing Maps** | Somatosensory/visual maps | Topographic mapping | Competitive learning | Moderate |
| **Adaptive Resonance Theory** | Cortex (learning) | Stable-plastic learning | No catastrophic forgetting | Complex |

---

## 5. Fidelity Scores

For each biological → computational mapping, we assess four dimensions:

### 5.1 Scoring Methodology

**Completeness (0-1):** How much of the biological mechanism is captured?
- 1.0: Complete mathematical equivalence
- 0.7-0.9: Core mechanism captured, minor details omitted
- 0.4-0.6: Key principles captured, significant simplification
- 0-0.3: Only conceptual analogy

**Accuracy (0-1):** How faithful is the mapping to biology?
- 1.0: Quantitatively matches experimental data
- 0.7-0.9: Qualitatively matches, parameters approximate
- 0.4-0.6: Matches general behavior, not specific dynamics
- 0-0.3: Conceptual similarity only

**Practicality (0-1):** How implementable is it?
- 1.0: Trivial implementation (few lines of code)
- 0.7-0.9: Standard implementation (well-understood algorithms)
- 0.4-0.6: Requires specialized knowledge/tools
- 0-0.3: Research-level difficulty

**Value (0-1):** How useful is the primitive?
- 1.0: Universal, solves many problems, no alternatives
- 0.7-0.9: Broadly useful, some alternatives exist
- 0.4-0.6: Niche applications
- 0-0.3: Theoretical interest only

### 5.2 Scored Mappings

#### Mechanisms

| Mechanism | Computational Mapping | Completeness | Accuracy | Practicality | Value | Overall |
|-----------|----------------------|--------------|----------|--------------|-------|---------|
| Hebbian Learning | Correlation weight update | 0.85 | 0.80 | 0.95 | 0.90 | 0.88 |
| STDP | Temporal causality learning | 0.90 | 0.85 | 0.80 | 0.85 | 0.85 |
| Lateral Inhibition | Winner-take-all | 0.80 | 0.75 | 0.90 | 0.85 | 0.83 |
| Homeostatic Plasticity | Batch normalization | 0.60 | 0.50 | 0.95 | 0.80 | 0.71 |
| Feedback Inhibition | PID controller | 0.90 | 0.85 | 0.95 | 0.90 | 0.90 |
| Predictive Coding | Residual networks | 0.70 | 0.65 | 0.85 | 0.85 | 0.76 |
| Spike Frequency Adaptation | Rate limiting | 0.75 | 0.70 | 0.90 | 0.70 | 0.76 |
| Neuromodulation | Attention/gating | 0.65 | 0.60 | 0.85 | 0.90 | 0.75 |

#### Processes

| Process | Computational Mapping | Completeness | Accuracy | Practicality | Value | Overall |
|---------|----------------------|--------------|----------|--------------|-------|---------|
| Action Potential | Signal propagation | 0.95 | 0.95 | 0.70 | 0.75 | 0.84 |
| Synaptic Transmission | Message passing | 0.80 | 0.75 | 0.90 | 0.95 | 0.85 |
| Calcium Oscillations | Clock generator | 0.70 | 0.70 | 0.85 | 0.80 | 0.76 |
| Vesicle Release | Stochastic events | 0.85 | 0.80 | 0.85 | 0.75 | 0.81 |
| Diffusion | Spatial broadcast | 0.90 | 0.90 | 0.60 | 0.70 | 0.78 |
| Glycolysis | Pipeline processing | 0.75 | 0.70 | 0.80 | 0.85 | 0.78 |
| MAPK Cascade | Amplification pipeline | 0.85 | 0.80 | 0.75 | 0.80 | 0.80 |
| Receptor Desensitization | Adaptive attenuation | 0.80 | 0.75 | 0.90 | 0.85 | 0.83 |

#### Circuit Motifs

| Motif | Computational Mapping | Completeness | Accuracy | Practicality | Value | Overall |
|-------|----------------------|--------------|----------|--------------|-------|---------|
| Feedforward Inhibition | Coincidence detector | 0.85 | 0.80 | 0.85 | 0.90 | 0.85 |
| Recurrent Excitation | Working memory | 0.75 | 0.70 | 0.75 | 0.95 | 0.79 |
| Mutual Inhibition | Bistable flip-flop | 0.90 | 0.85 | 0.95 | 0.85 | 0.89 |
| Winner-Take-All | Argmax operation | 0.80 | 0.75 | 0.90 | 0.90 | 0.84 |
| Central Pattern Generator | Oscillator network | 0.85 | 0.80 | 0.70 | 0.80 | 0.79 |
| Divisive Normalization | Softmax/normalization | 0.75 | 0.70 | 0.95 | 0.90 | 0.83 |
| Hierarchical Processing | Deep networks | 0.65 | 0.60 | 0.90 | 0.95 | 0.78 |

#### Architectural Patterns

| Pattern | Biological Basis | Completeness | Accuracy | Practicality | Value | Overall |
|---------|-----------------|--------------|----------|--------------|-------|---------|
| Sparse Distributed Memory | Hippocampus | 0.70 | 0.65 | 0.70 | 0.90 | 0.74 |
| Attractor Networks | PFC working memory | 0.80 | 0.75 | 0.65 | 0.85 | 0.76 |
| Liquid State Machines | Cortical microcircuits | 0.60 | 0.55 | 0.80 | 0.85 | 0.70 |
| Predictive Coding Networks | Cortical hierarchy | 0.65 | 0.60 | 0.70 | 0.85 | 0.70 |
| Convolutional Networks | Visual cortex | 0.60 | 0.50 | 0.95 | 0.95 | 0.75 |
| Reservoir Computing | Cortical dynamics | 0.65 | 0.60 | 0.85 | 0.80 | 0.73 |
| Actor-Critic | Basal ganglia | 0.75 | 0.70 | 0.80 | 0.90 | 0.79 |
| Spiking Neural Networks | Actual neurons | 0.85 | 0.80 | 0.60 | 0.75 | 0.75 |

### 5.3 High-Value, High-Fidelity Mappings

These mappings score >0.80 overall and should be prioritized for implementation:

1. **Feedback Inhibition → PID Controller** (0.90)
   - Near-perfect mapping
   - Extremely practical
   - Universal applicability

2. **Hebbian Learning → Correlation Update** (0.88)
   - Well-understood
   - Easy to implement
   - Foundational for learning

3. **Mutual Inhibition → Bistable Switch** (0.89)
   - Direct correspondence
   - Simple implementation
   - Useful for decisions

4. **Synaptic Transmission → Message Passing** (0.85)
   - Core communication primitive
   - Event-driven architecture
   - High value

5. **Feedforward Inhibition → Coincidence Detection** (0.85)
   - Temporal precision
   - Well-characterized
   - Multiple applications

6. **STDP → Temporal Causality Learning** (0.85)
   - Sequence learning
   - Causal relationships
   - Moderate complexity

7. **Action Potential → Signal Propagation** (0.84)
   - Faithful model exists (HH)
   - Complex but valuable

8. **Winner-Take-All → Argmax** (0.84)
   - Simple and effective
   - Decision making
   - Very practical

### 5.4 Research-Needed Mappings

These mappings have potential but need more work (score 0.60-0.75):

1. **Homeostatic Plasticity → Batch Normalization** (0.71)
   - Conceptual similarity
   - Timescale mismatch
   - Mechanisms differ

2. **Liquid State Machines** (0.70)
   - Promising architecture
   - Parameter sensitivity
   - Training challenges

3. **Predictive Coding Networks** (0.70)
   - Theoretical appeal
   - Implementation complexity
   - Still being refined

4. **Sparse Distributed Memory** (0.74)
   - Great properties
   - Implementation subtleties
   - Scaling challenges

---

## 6. Implementation Roadmap

Priority ranking based on value, difficulty, and dependencies.

### 6.1 Phase 1: Foundational Primitives (Weeks 1-4)

**Priority: CRITICAL**
**Goal:** Establish basic computational building blocks

#### Week 1-2: Core Signal Processing
1. **Weighted Summation** (Dendritic integration)
   - Difficulty: Trivial
   - Value: Critical (used everywhere)
   - Implementation: `output = np.dot(weights, inputs)`
   - Tests: Linearity, dimensionality

2. **Nonlinear Activation** (Threshold/sigmoid)
   - Difficulty: Trivial
   - Value: Critical
   - Implementation: Standard activation functions
   - Tests: Range, monotonicity, derivatives

3. **Temporal Integration** (Leaky integrator)
   - Difficulty: Trivial
   - Value: High
   - Implementation: First-order ODE solver
   - Tests: Time constant, stability

4. **Gating** (Conditional execution)
   - Difficulty: Trivial
   - Value: High
   - Implementation: Multiplicative modulation
   - Tests: Binary/smooth gating, gradients

#### Week 3-4: Learning Rules
5. **Hebbian Learning**
   - Difficulty: Trivial
   - Value: High
   - Implementation: `dw = eta * pre * post`
   - Tests: Convergence, associativity
   - Dependencies: None

6. **Feedback Inhibition**
   - Difficulty: Trivial
   - Value: High
   - Implementation: Negative feedback ODE
   - Tests: Stability, setpoint tracking

7. **Winner-Take-All**
   - Difficulty: Moderate
   - Value: High
   - Implementation: Lateral inhibition or softmax
   - Tests: Selection, competition

### 6.2 Phase 2: Memory Systems (Weeks 5-8)

**Priority: HIGH**
**Goal:** Implement various memory architectures

#### Week 5-6: Short-Term Memory
8. **Attractor Networks**
   - Difficulty: Complex
   - Value: High
   - Implementation: Recurrent dynamics with attractors
   - Tests: Stable states, basins of attraction
   - Dependencies: Recurrent connectivity, nonlinear dynamics

9. **Working Memory Buffer**
   - Difficulty: Moderate
   - Value: High
   - Implementation: Persistent activity via recurrence
   - Tests: Retention time, capacity
   - Dependencies: Attractor networks

#### Week 7-8: Long-Term Memory
10. **Hopfield Network** (Associative memory)
    - Difficulty: Moderate
    - Value: High
    - Implementation: Symmetric weights, energy function
    - Tests: Pattern completion, capacity
    - Dependencies: Hebbian learning

11. **Sparse Distributed Memory**
    - Difficulty: Complex
    - Value: High
    - Implementation: Sparse coding + distributed storage
    - Tests: Fault tolerance, capacity
    - Dependencies: Winner-take-all

### 6.3 Phase 3: Temporal Processing (Weeks 9-12)

**Priority: HIGH**
**Goal:** Sequence and temporal pattern recognition

#### Week 9-10: Timing Mechanisms
12. **Delay Lines**
    - Difficulty: Trivial
    - Value: Moderate
    - Implementation: Circular buffer
    - Tests: Delay accuracy

13. **Oscillators**
    - Difficulty: Moderate
    - Value: Moderate
    - Implementation: Coupled ODEs (limit cycle)
    - Tests: Frequency, phase, stability

14. **Coincidence Detection**
    - Difficulty: Trivial
    - Value: High
    - Implementation: Temporal window + AND
    - Tests: Window size, precision

#### Week 11-12: Sequence Learning
15. **STDP** (Spike-timing dependent plasticity)
    - Difficulty: Moderate
    - Value: High
    - Implementation: Asymmetric Hebbian rule
    - Tests: Timing window, causality
    - Dependencies: Spike timing, delay tracking

16. **Sequence Memory**
    - Difficulty: Complex
    - Value: High
    - Implementation: Asymmetric weights + temporal context
    - Tests: Sequence recall, prediction
    - Dependencies: STDP

### 6.4 Phase 4: Advanced Architectures (Weeks 13-20)

**Priority: MEDIUM**
**Goal:** Implement complex bio-inspired architectures

#### Week 13-15: Reservoir Computing
17. **Liquid State Machines**
    - Difficulty: Complex
    - Value: High
    - Implementation: Random recurrent network + linear readout
    - Tests: Separation property, echo state property
    - Dependencies: Recurrent dynamics

18. **Echo State Networks** (variant of LSM)
    - Difficulty: Moderate
    - Value: High
    - Implementation: Sparse random reservoir
    - Tests: Memory capacity, temporal XOR

#### Week 16-18: Hierarchical Processing
19. **Convolutional Architecture** (Visual cortex)
    - Difficulty: Moderate
    - Value: Very High
    - Implementation: Standard CNNs with biological constraints
    - Tests: Receptive fields, translation invariance
    - Dependencies: Convolution operation

20. **Hierarchical Temporal Memory**
    - Difficulty: Complex
    - Value: Moderate
    - Implementation: Spatial/temporal pooling
    - Tests: Sequence learning, prediction
    - Dependencies: Sparse coding

#### Week 19-20: Predictive Processing
21. **Predictive Coding Networks**
    - Difficulty: Complex
    - Value: High (research)
    - Implementation: Hierarchical error minimization
    - Tests: Prediction error, invariance
    - Dependencies: Hierarchical architecture

### 6.5 Phase 5: Control Systems (Weeks 21-24)

**Priority: MEDIUM**
**Goal:** Implement biological control architectures

#### Week 21-22: Reinforcement Learning
22. **Actor-Critic** (Basal ganglia)
    - Difficulty: Complex
    - Value: Very High
    - Implementation: Policy + value function + TD learning
    - Tests: Learning convergence, exploration
    - Dependencies: TD learning, policy gradients

23. **TD Learning** (Dopamine signals)
    - Difficulty: Moderate
    - Value: Very High
    - Implementation: Temporal difference algorithm
    - Tests: Value approximation, credit assignment

#### Week 23-24: Motor Control
24. **Cerebellum-like Controller**
    - Difficulty: Moderate
    - Value: High
    - Implementation: Supervised learning of forward model
    - Tests: Error correction, adaptation
    - Dependencies: Supervised learning

25. **Central Pattern Generator**
    - Difficulty: Complex
    - Value: Moderate
    - Implementation: Coupled oscillators with mutual inhibition
    - Tests: Rhythmic output, frequency control
    - Dependencies: Oscillators

### 6.6 Phase 6: Sensory Processing (Weeks 25-28)

**Priority: LOW-MEDIUM**
**Goal:** Implement sensory preprocessing architectures

#### Week 25-26: Vision
26. **Retinal Preprocessing**
    - Difficulty: Moderate
    - Value: Moderate
    - Implementation: Center-surround filters + adaptation
    - Tests: Edge enhancement, gain control
    - Dependencies: Convolution

27. **V1 Feature Detectors**
    - Difficulty: Moderate
    - Value: High
    - Implementation: Gabor filters / oriented edges
    - Tests: Orientation selectivity, spatial frequency
    - Dependencies: Convolution

#### Week 27-28: Audition
28. **Cochlear Model**
    - Difficulty: Moderate
    - Value: Moderate
    - Implementation: Gammatone filterbank
    - Tests: Frequency decomposition, tonotopic organization
    - Dependencies: Bandpass filters

### 6.7 Implementation Dependencies Graph

```
Level 0 (No dependencies):
├── Weighted Summation
├── Nonlinear Activation
├── Gating
├── Hebbian Learning
└── Delay Lines

Level 1:
├── Temporal Integration
├── Feedback Inhibition
├── Threshold Detection
├── Coincidence Detection
└── Oscillators

Level 2:
├── Winner-Take-All (needs: lateral inhibition)
├── STDP (needs: delay tracking)
├── Hopfield Network (needs: Hebbian)
└── Differentiation

Level 3:
├── Attractor Networks (needs: recurrent dynamics)
├── Working Memory (needs: attractors)
├── Sequence Memory (needs: STDP)
└── Normalization

Level 4:
├── Sparse Distributed Memory (needs: WTA)
├── Liquid State Machines (needs: recurrent)
├── TD Learning
└── Reservoir Computing

Level 5:
├── Actor-Critic (needs: TD)
├── Hierarchical Temporal Memory (needs: sparse coding)
└── Predictive Coding (needs: hierarchical structure)
```

### 6.8 Resource Estimates

| Phase | Duration | Complexity | Team Size | Key Deliverables |
|-------|----------|------------|-----------|------------------|
| Phase 1 | 4 weeks | Low | 1-2 | Core primitives library |
| Phase 2 | 4 weeks | Medium | 2-3 | Memory systems |
| Phase 3 | 4 weeks | Medium | 2-3 | Temporal processing |
| Phase 4 | 8 weeks | High | 3-4 | Advanced architectures |
| Phase 5 | 4 weeks | Medium-High | 2-3 | Control systems |
| Phase 6 | 4 weeks | Medium | 2 | Sensory processing |

**Total:** 28 weeks (~7 months) with 2-4 person team

### 6.9 Success Criteria

Each implementation must pass:

1. **Unit Tests**
   - Correct mathematical behavior
   - Edge cases handled
   - Numerical stability

2. **Integration Tests**
   - Works with other primitives
   - Composability verified
   - No unexpected interactions

3. **Biological Validation**
   - Matches known biological data (where available)
   - Reproduces published computational results
   - Qualitative behavior correct

4. **Performance Benchmarks**
   - Computational efficiency
   - Memory usage
   - Scalability

5. **Documentation**
   - API documentation
   - Example usage
   - Biological background
   - Mathematical derivation

---

## 7. Cross-Reference Index

### 7.1 Database Entity Cross-References

#### Mechanisms

| Mechanism | GO Term | ModelDB | NeuroML | Formula DB | Literature |
|-----------|---------|---------|---------|------------|------------|
| Lateral Inhibition | GO:0060080 | 12345 | - | Formula #23 | Douglas & Martin (2004) |
| Hebbian Learning | GO:0048169 | Multiple | - | Formula #567 | Hebb (1949) |
| STDP | GO:0048169 | 64261, 83319 | STDP.xml | Formula #568-570 | Bi & Poo (1998) |
| Homeostatic Plasticity | GO:0060291 | - | - | - | Turrigiano (2004) |
| Predictive Coding | - | - | - | - | Rao & Ballard (1999) |
| Feedback Inhibition | GO:0051101 | - | - | - | Systems Biology |
| Neuromodulation | GO:0050804 | Multiple | - | - | Marder (2012) |

#### Processes

| Process | GO Term | KEGG | Reactome | Formula DB | Literature |
|---------|---------|------|----------|------------|------------|
| Action Potential | GO:0001508 | - | R-HSA-1296071 | Formulas #1-7 | Hodgkin & Huxley (1952) |
| Synaptic Transmission | GO:0007268 | - | R-HSA-112315 | Formulas #17-22 | Katz (1969) |
| Glycolysis | GO:0006096 | map00010 | R-HSA-70171 | Formulas #200-212 | Berg et al. (2002) |
| Calcium Signaling | GO:0019722 | map04020 | R-HSA-1257604 | Formulas #138-145 | Berridge et al. (2003) |
| MAPK Cascade | GO:0000165 | map04010 | R-HSA-5683057 | Formulas #380-390 | Huang & Ferrell (1996) |

#### Circuit Motifs

| Motif | Brain Region | ModelDB | Literature | Formula DB |
|-------|--------------|---------|------------|------------|
| Feedforward Inhibition | Hippocampus, Cortex | 144054 | Pouille & Scanziani (2001) | - |
| Recurrent Excitation | PFC, CA3 | 87284 | Wang (2001) | Formulas #45-48 |
| Mutual Inhibition | Many | 3815 | Wilson & Cowan (1972) | Formula #40 |
| Winner-Take-All | Cortex | - | Douglas & Martin (2004) | Formula #23 |
| Central Pattern Generator | Spinal cord, brainstem | 3665 | Marder & Calabrese (1996) | - |

#### Enzymes

| Enzyme | EC Number | UniProt | BRENDA | KEGG | Formula DB |
|--------|-----------|---------|--------|------|------------|
| Hexokinase | EC 2.7.1.1 | P19367 | 2.7.1.1 | K00844 | Formula #200 |
| Phosphofructokinase | EC 2.7.1.11 | P08237 | 2.7.1.11 | K00850 | Formula #202 |
| Pyruvate Kinase | EC 2.7.1.40 | P14618 | 2.7.1.40 | K00873 | Formula #211 |
| CaMKII | EC 2.7.11.17 | Q9UQM7 | 2.7.11.17 | K04515 | - |
| Protein Phosphatase 1 | EC 3.1.3.16 | P62136 | 3.1.3.16 | K06275 | - |

#### Receptors/Channels

| Receptor/Channel | UniProt | NeuroML | Ion | Formula DB | Literature |
|------------------|---------|---------|-----|------------|------------|
| Nav1.6 | Q9Y5Y9 | Nav1p6.channel.nml | Na+ | Formulas #3, 4 | HH (1952) |
| Kv1.1 | Q09470 | Kv1.channel.nml | K+ | Formulas #6-8 | HH (1952) |
| NMDA Receptor | Q12879 | NMDA.channel.nml | Ca2+, Na+, K+ | Formula #19 | Jahr & Stevens (1990) |
| AMPA Receptor | P42261 | AMPA.channel.nml | Na+, K+ | Formula #17 | - |
| GABA_A Receptor | P14867 | GABA_A.channel.nml | Cl- | - | - |

#### Cell Types

| Cell Type | Brain Region | NeuroMorpho | Allen Brain | Markers | Properties |
|-----------|--------------|-------------|-------------|---------|------------|
| Pyramidal Neuron | Cortex, Hippocampus | NMO_00001-10000 | Exc neurons | CaMKII, Glutamate | Excitatory, apical dendrite |
| PV+ Interneuron | Cortex, Hippocampus | NMO_50001-51000 | Pvalb+ | Parvalbumin | Fast-spiking, basket cells |
| SST+ Interneuron | Cortex | NMO_52001-53000 | Sst+ | Somatostatin | Dendritic targeting |
| Granule Cell | Cerebellum, Dentate Gyrus | NMO_30001-35000 | Granule cells | - | Small, high threshold |
| Purkinje Cell | Cerebellum | NMO_25001-26000 | Purkinje | Calbindin | Large dendritic tree |

#### Pathways

| Pathway | KEGG ID | Reactome ID | Key Components | Formula DB |
|---------|---------|-------------|----------------|------------|
| MAPK/ERK | hsa04010 | R-HSA-5683057 | Ras, Raf, MEK, ERK | Formulas #380-390 |
| PI3K-AKT | hsa04151 | R-HSA-1257604 | PI3K, AKT, mTOR | Formulas #400-410 |
| cAMP | hsa04024 | R-HSA-111932 | GPCR, AC, PKA | Formulas #330-335 |
| Calcium | hsa04020 | R-HSA-1296071 | IP3, Ca2+ stores | Formulas #138-145 |
| Wnt | hsa04310 | R-HSA-195721 | Wnt, β-catenin | Formulas #420-425 |
| Notch | hsa04330 | R-HSA-157118 | Notch, γ-secretase | - |

### 7.2 Formula Database Cross-Reference

Link to specific formulas in bioformulas.db:

| Category | Formula Count | Key Formulas | Notes |
|----------|---------------|--------------|-------|
| **Ion Channels** | 121 | HH equations (#1-8), Ca channels (#101-110) | ODEs, current equations |
| **Synaptic Transmission** | 14 | AMPA (#17-18), NMDA (#19-20), GABA (#21-22) | Current equations |
| **Plasticity** | 32 | STDP (#568-570), BCM (#571-573), Homeostatic (#574-576) | Plasticity rules |
| **Metabolism** | 54 | Glycolysis (#200-212), TCA (#220-228), OXPHOS (#230-236) | Michaelis-Menten |
| **Signaling** | 67 | MAPK (#380-390), PI3K (#400-410), cAMP (#330-335) | Cascade dynamics |
| **Networks** | 33 | Attractor (#45-48), WTA (#23), Oscillator (#60-65) | Population dynamics |
| **Receptors** | 126 | GPCRs (#37 types), Nuclear receptors (#32), RTKs (#31) | Binding kinetics |

### 7.3 Literature References

Key papers by topic:

#### Mechanisms
- Hebb, D.O. (1949). *The Organization of Behavior*
- Bi, G.Q. & Poo, M.M. (1998). Synaptic modifications in cultured hippocampal neurons. *J Neurosci* 18(24):10464-72
- Turrigiano, G.G. (2004). Homeostatic plasticity in neuronal networks. *Curr Opin Neurobiol* 14(3):283-8
- Rao, R.P. & Ballard, D.H. (1999). Predictive coding in the visual cortex. *Nature Neurosci* 2(1):79-87

#### Processes
- Hodgkin, A.L. & Huxley, A.F. (1952). A quantitative description of membrane current. *J Physiol* 117(4):500-544
- Katz, B. (1969). *The Release of Neural Transmitter Substances*
- Berridge, M.J. et al. (2003). Calcium signalling: dynamics, homeostasis and remodelling. *Nature Rev Mol Cell Biol* 4(7):517-29

#### Circuit Motifs
- Pouille, F. & Scanziani, M. (2001). Enforcement of temporal fidelity. *Science* 293(5532):1159-63
- Wilson, H.R. & Cowan, J.D. (1972). Excitatory and inhibitory interactions. *Biophys J* 12(1):1-24
- Marder, E. & Calabrese, R.L. (1996). Principles of rhythmic motor pattern generation. *Physiol Rev* 76(3):687-717

#### Architectures
- Hopfield, J.J. (1982). Neural networks and physical systems. *PNAS* 79(8):2554-8
- Kohonen, T. (1982). Self-organized formation of topologically correct feature maps. *Biol Cybern* 43(1):59-69
- Maass, W. et al. (2002). Real-time computing without stable states. *Neural Comput* 14(11):2531-60

### 7.4 External Database URLs

Quick links to external resources:

| Database | URL | Coverage | Access |
|----------|-----|----------|--------|
| **Gene Ontology** | http://geneontology.org | All processes/functions | Free |
| **KEGG Pathways** | https://www.kegg.jp | Metabolic/signaling pathways | Free (limited) |
| **Reactome** | https://reactome.org | Biological pathways | Free |
| **UniProt** | https://www.uniprot.org | Protein sequences/functions | Free |
| **BRENDA** | https://www.brenda-enzymes.org | Enzyme kinetics | Free |
| **ModelDB** | https://modeldb.science | Computational models | Free |
| **NeuroML** | https://neuroml.org | Neuron/network models | Free |
| **Allen Brain Atlas** | https://brain-map.org | Brain anatomy/expression | Free |
| **NeuroMorpho** | http://neuromorpho.org | Neuron morphology | Free |
| **PDB** | https://www.rcsb.org | Protein structures | Free |

### 7.5 Code Repository Structure

Suggested organization for implementation:

```
bio_architecture/
├── primitives/
│   ├── signal_processing/
│   │   ├── integration.py
│   │   ├── gating.py
│   │   ├── normalization.py
│   │   └── differentiation.py
│   ├── memory/
│   │   ├── hopfield.py
│   │   ├── attractor.py
│   │   └── sparse_distributed.py
│   ├── learning/
│   │   ├── hebbian.py
│   │   ├── stdp.py
│   │   └── td_learning.py
│   └── temporal/
│       ├── delay.py
│       ├── oscillator.py
│       └── coincidence.py
├── architectures/
│   ├── liquid_state_machine.py
│   ├── predictive_coding.py
│   ├── actor_critic.py
│   └── hierarchical_temporal_memory.py
├── models/
│   ├── neurons/
│   │   ├── hodgkin_huxley.py
│   │   ├── lif.py
│   │   └── izhikevich.py
│   ├── synapses/
│   │   ├── ampa.py
│   │   ├── nmda.py
│   │   └── gaba.py
│   └── networks/
│       ├── feedforward_inhibition.py
│       └── winner_take_all.py
├── data/
│   ├── formulas.db → bioformulas.db
│   ├── bio_architecture.db
│   └── computational_mappings.json
├── docs/
│   ├── COMPUTATIONAL_VALUE_MAPPING.md (this file)
│   ├── api/
│   └── examples/
└── tests/
    ├── test_primitives/
    ├── test_architectures/
    └── test_models/
```

---

## Conclusion

This document provides a comprehensive mapping from biological mechanisms to computational primitives. It serves as:

1. **Translation Guide**: Understand what computational value each biological entity provides
2. **Implementation Reference**: Prioritized roadmap with dependencies
3. **Validation Framework**: Fidelity scores to assess mapping quality
4. **Research Index**: Cross-references to databases and literature

**Next Steps:**
1. Review and validate mappings with domain experts
2. Begin Phase 1 implementation (foundational primitives)
3. Populate bio_architecture.db with detailed entity information
4. Expand formula database with additional mechanisms
5. Develop comprehensive test suites for each primitive

**Maintenance:**
- Update fidelity scores as implementations improve
- Add new biological discoveries as they emerge
- Refine mathematical formalizations based on experimental data
- Expand cross-references to new databases and papers

---

**Document Version:** 1.0.0
**Generated:** 2025-12-10
**Database Version:** bio_architecture.db v1.0, bioformulas.db v1.0
**Formula Count:** 595
**Entity Count:** ~13,000 (estimated across all types)
**Mappings Documented:** ~100 (high-priority subset)

