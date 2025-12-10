# Biological Learning Formulas - Quick Reference Guide

## Database Summary
- **Total Learning Formulas**: 33
- **Database**: `/home/user/MAINFRAME/bioformulas/bioformulas.db`
- **Categories**: STDP (12), Hebbian (7), Homeostatic (5), Learning Algorithms (4), Calcium-Based (3), Metaplasticity (2), Reward Learning (2)

---

## Category Breakdown

| Category | Count | Key Principles |
|----------|-------|----------------|
| **STDP Variants** | 12 | Spike timing causality, exponential windows, temporal credit |
| **Hebbian & Rate-Based** | 7 | Correlation learning, PCA, sliding thresholds |
| **Homeostatic** | 5 | Stability, target firing rates, synaptic scaling |
| **Learning Algorithms** | 4 | Contrastive learning, ICA, predictive coding, sparse coding |
| **Calcium-Based** | 3 | Calcium thresholds, LTP/LTD direction, biochemical signals |
| **Metaplasticity** | 2 | Threshold adaptation, learning to learn |
| **Reward Learning** | 2 | Eligibility traces, dopamine modulation, RL |

---

## Top 10 Most Important Learning Rules

### 1. Pair-Based STDP [ID: 25]
```latex
Δw = { A₊ exp(-Δt/τ₊)  if Δt > 0
     {-A₋ exp(Δt/τ₋)   if Δt < 0
```
- **Principle**: Causality detection - pre before post → LTP, post before pre → LTD
- **Timescale**: Milliseconds (τ ≈ 20ms)
- **Stability**: Unbounded (needs regulation)
- **Biology**: Found in hippocampus, cortex, cerebellum
- **Application**: Temporal sequence learning, causality detection

### 2. BCM Plasticity Rule [ID: 27]
```latex
dw/dt = η φ(c) c_pre
φ(c) = c(c - θₘ)
```
- **Principle**: Sliding threshold creates selectivity (below θ → LTD, above θ → LTP)
- **Timescale**: 100ms - 1s (firing rates)
- **Stability**: Stable via threshold adaptation
- **Biology**: Visual cortex orientation tuning
- **Application**: Feature selectivity, receptive field development

### 3. Oja's Learning Rule [ID: 29]
```latex
Δwᵢ = η y(xᵢ - y wᵢ)
```
- **Principle**: Hebbian + normalization → extracts principal components
- **Timescale**: Medium (seconds to minutes)
- **Stability**: Stable (self-normalizing)
- **Biology**: Cortical feature extraction
- **Application**: Unsupervised PCA, dimensionality reduction

### 4. Triplet STDP [ID: 26]
```latex
Δw = r₁(t)[A₂⁺ + A₃⁺r₂(t-ε)] - o₁(t)[A₂⁻ + A₃⁻o₂(t-ε)]
```
- **Principle**: Frequency-dependent STDP (triplets of spikes matter)
- **Timescale**: Fast (ms) with slow traces
- **Stability**: Better than pair-based STDP
- **Biology**: Explains experimental data better than pair-based
- **Application**: Burst detection, frequency coding

### 5. Voltage-Dependent STDP (Clopath) [ID: 502]
```latex
dw/dt = A_LTD x̄(V - θ_LTD)₋ + A_LTP x(V̄ - θ_LTP)₊(V - θ_LTD)₊
```
- **Principle**: Dendritic voltage (not spikes) drives plasticity
- **Timescale**: Milliseconds (voltage dynamics)
- **Stability**: Voltage-dependent bounds
- **Biology**: More biologically accurate (dendrites compute)
- **Application**: Dendritic computation, nonlinear integration

### 6. Multiplicative STDP [ID: 499]
```latex
Δw = { (wₘₐₓ - w)·f₊(Δt)  LTP
     { w·f₋(Δt)           LTD
```
- **Principle**: Weight-dependent plasticity prevents saturation
- **Timescale**: Fast (ms)
- **Stability**: **STABLE** - naturally bounded
- **Biology**: Observed in many synapses
- **Application**: Self-limiting learning, competition

### 7. Shouval Calcium Model [ID: 493]
```latex
dw/dt = η([Ca])·(Ω([Ca]) - w)
Ω([Ca]) = sig([Ca] - θ_LTP) - 0.5·sig([Ca] - θ_LTD)
```
- **Principle**: Calcium level determines plasticity direction
- **Timescale**: Medium (100ms - 1s)
- **Stability**: Activity-dependent equilibrium
- **Biology**: Unifies NMDA receptor dynamics with plasticity
- **Application**: Calcium-based learning rules in simulations

### 8. Synaptic Scaling [ID: 508]
```latex
dw/dt = α(r_target - r)
```
- **Principle**: Homeostatic regulation maintains target firing rate
- **Timescale**: **Slow** (hours to days)
- **Stability**: **STABLE** - negative feedback
- **Biology**: Prevents runaway excitation
- **Application**: Stabilizing Hebbian learning, catastrophic forgetting prevention

### 9. Reward-Modulated STDP [ID: 504]
```latex
dw/dt = c·STDP(Δt)·(R - R̄)
```
- **Principle**: Three-factor rule: correlation + eligibility + reward
- **Timescale**: Fast (ms) + slow (reward)
- **Stability**: Depends on reward structure
- **Biology**: Dopaminergic modulation in basal ganglia
- **Application**: Reinforcement learning, reward-based learning

### 10. Covariance Learning [ID: 583]
```latex
Δwᵢⱼ = η(xᵢ - x̄ᵢ)(yⱼ - ȳⱼ)
```
- **Principle**: Learns correlations (not just co-activation)
- **Timescale**: Medium
- **Stability**: More stable than pure Hebbian
- **Biology**: Decorrelation, whitening
- **Application**: Statistical learning, ICA preprocessing

---

## Common Mathematical Patterns

### Exponential Kernels (STDP windows)
```
f(Δt) = A exp(-|Δt|/τ)
```
- **Count**: 10 formulas (30%)
- **Purpose**: Temporal windows for spike coincidence
- **Biology**: Matches NMDA receptor kinetics

### Thresholds (Decision boundaries)
```
(V - θ)₊ = max(V - θ, 0)
```
- **Count**: 8 formulas (24%)
- **Purpose**: Nonlinear gating, bifurcations
- **Biology**: Voltage thresholds, calcium thresholds

### Sliding Thresholds (Metaplasticity)
```
dθ/dt = f(activity)
```
- **Count**: 5 formulas (15%)
- **Purpose**: Adaptation, history-dependence
- **Biology**: BCM threshold, homeostasis

### Weight Dependence (Soft bounds)
```
dw ∝ (wₘₐₓ - w)  or  w^μ
```
- **Count**: 2 formulas (6%)
- **Purpose**: Natural stability
- **Biology**: Receptor saturation

### Calcium Signaling
```
Plasticity = f([Ca²⁺])
```
- **Count**: 4 formulas (12%)
- **Purpose**: Biochemical signaling
- **Biology**: NMDA receptors, CaMKII, calcineurin

---

## Stability Analysis Summary

| Mechanism | Formula IDs | Count | How It Works |
|-----------|-------------|-------|--------------|
| **Soft Bounds** | 499, 500 | 2 | Weight-dependent plasticity (wₘₐₓ - w) |
| **Normalization** | 29 | 1 | Oja's rule: -y²w term |
| **Sliding Threshold** | 27, 506, 512 | 3 | BCM, metaplasticity |
| **Negative Feedback** | 508, 509, 510 | 3 | Homeostatic (r_target - r) |
| **None (Unstable)** | 25, 495 | 2 | Unbounded STDP |

---

## Learning Type Distribution

| Type | Count | Percentage |
|------|-------|------------|
| **Unsupervised** | 31 | 94% |
| **Reinforcement** | 1 | 3% |
| **Supervised** | 1 | 3% |

**Key Insight**: Biology overwhelmingly uses **unsupervised** learning rules that discover structure from data statistics.

---

## Timescale Distribution

| Timescale | Count | Example |
|-----------|-------|---------|
| **Fast (ms)** | 12 | STDP, spike timing |
| **Medium (100ms-1s)** | 19 | Firing rates, BCM, Oja |
| **Slow (hours-days)** | 2 | Synaptic scaling, homeostasis |
| **Very slow (weeks)** | 0 | Metaplasticity adaptation |

---

## Biological Learning vs Backpropagation

| Feature | Biological | Backprop | Winner |
|---------|-----------|----------|--------|
| **Locality** | ✓ Local | ✗ Non-local | Bio |
| **Online Learning** | ✓ Continuous | △ Batch-based | Bio |
| **Energy** | ✓ 20W | ✗ 300W | Bio |
| **Stability** | ✓ Built-in | △ Regularization | Bio |
| **Supervision** | ✓ Unsupervised | ✗ Requires labels | Bio |
| **Speed** | ✗ Slow | ✓ Fast | Backprop |
| **Convergence** | △ Limited | ✓ Strong | Backprop |
| **Performance** | △ Good | ✓ Excellent | Backprop |

**Summary**: Biological learning wins on efficiency, locality, and unsupervised learning. Backprop wins on speed and performance with labeled data.

---

## Biological Advantages

### 1. Locality
- **All 33 formulas are local**
- No backward pass needed
- Massively parallelizable
- Scales to billions of synapses

### 2. Energy Efficiency
- Brain: ~20W for 86 billion neurons
- GPU: ~300W for 1 billion parameters
- **~15x more energy efficient per parameter**

### 3. Online Learning
- Continuous adaptation to data stream
- No batch requirements
- No separate train/test phases
- Immediate learning from single examples

### 4. Stability
- Multiple complementary mechanisms
- Self-organizing dynamics
- No gradient explosion/vanishing
- Robust to noise and damage

### 5. Multi-Timescale
- Fast: STDP (ms)
- Medium: Hebbian (100ms-1s)
- Slow: Homeostatic (hours-days)
- Very slow: Metaplasticity (weeks)

### 6. Unsupervised
- 94% of rules don't need labels
- Learn structure from statistics
- Self-organized feature extraction
- Anomaly detection

---

## Applications & Future Directions

### Neuromorphic Computing
- **Intel Loihi**: STDP in hardware
- **IBM TrueNorth**: Event-driven spikes
- **BrainScaleS**: Accelerated analog neurons
- **SpiNNaker**: Million-core spiking neural networks

### Edge AI
- Local learning (no cloud)
- Low power consumption
- Real-time adaptation
- Privacy-preserving

### Continual Learning
- No catastrophic forgetting
- Consolidation mechanisms
- Synaptic scaling prevents runaway
- Meta-learning via metaplasticity

### Hybrid Approaches
1. **Equilibrium Propagation**: Local gradient approximation
2. **Target Propagation**: Local targets, no backward pass
3. **Predictive Coding**: Hierarchical prediction errors
4. **Forward-Forward** (Hinton 2022): Two forward passes

---

## PyTorch Implementation Summary

### Available Implementations
See `/home/user/MAINFRAME/biological_learning_analysis.md` for full code.

1. **STDPLayer**: Pair-based STDP with soft bounds
   - Exponential traces for pre/post activity
   - Multiplicative normalization
   - Differentiable approximation

2. **BCMLayer**: BCM with sliding threshold
   - Quadratic selectivity function
   - Automatic threshold adaptation
   - Weight normalization

3. **RewardModulatedSTDPLayer**: 3-factor learning
   - STDP eligibility traces
   - Reward prediction error
   - Temporal credit assignment

4. **HomeostaticLayer**: Synaptic scaling
   - Target rate maintenance
   - Multiplicative scaling
   - Slow timescale regulation

---

## Key Formulas by Function

### Temporal Learning
- **Pair-Based STDP** [25]: Classic causality detection
- **Triplet STDP** [26]: Frequency-dependent
- **Voltage-Dependent STDP** [502]: Dendritic computation

### Feature Extraction
- **Oja's Rule** [29]: PCA, eigenvector extraction
- **BCM Rule** [27]: Selectivity, orientation tuning
- **Covariance Learning** [583]: Decorrelation

### Stability
- **Synaptic Scaling** [508]: Homeostatic regulation
- **Multiplicative STDP** [499]: Soft bounds
- **Heterosynaptic Plasticity** [511]: Local competition

### Reward Learning
- **Reward-Modulated STDP** [504]: RL with STDP
- **Eligibility Trace** [505]: Temporal credit

### Calcium Dynamics
- **Shouval Model** [493]: Calcium-dependent plasticity
- **Omega Function** [494]: LTP/LTD direction
- **Clopath Model** [502]: Voltage-based

---

## Research Frontiers

### Open Questions
1. How do multiple plasticity rules interact?
2. What role do astrocytes play in learning?
3. How does metaplasticity enable transfer learning?
4. Can biological rules match backprop performance?

### Promising Directions
1. **Hybrid Models**: Biological local rules + global coordination
2. **Neuromorphic Hardware**: STDP in silicon
3. **Energy-Efficient AI**: Brain-inspired algorithms for edge devices
4. **Continual Learning**: No catastrophic forgetting

### Recent Breakthroughs
- **Forward-Forward Algorithm** (Hinton, 2022): Two forward passes, no backprop
- **Equilibrium Propagation**: Energy-based local learning
- **Dendritic Computation**: Multi-compartment learning
- **Predictive Coding**: Hierarchical prediction errors

---

## Quick Reference: Formula Selection Guide

**Need to detect temporal sequences?**
→ Use Pair-Based STDP [25] or Triplet STDP [26]

**Need feature selectivity?**
→ Use BCM [27] or Oja's Rule [29]

**Need stability?**
→ Add Synaptic Scaling [508] or use Multiplicative STDP [499]

**Need reward learning?**
→ Use Reward-Modulated STDP [504]

**Need unsupervised feature extraction?**
→ Use Oja [29], Covariance Learning [583], or ICA [585]

**Need calcium-based model?**
→ Use Shouval Model [493] or Clopath [502]

**Need homeostasis?**
→ Use Synaptic Scaling [508] or Intrinsic Excitability [510]

---

## Conclusion

The BioFormulas database contains **33 biological learning and plasticity formulas** representing decades of neuroscience research. Key insights:

1. **100% are local** (no backpropagation)
2. **94% are unsupervised** (no labels needed)
3. **Multiple timescales** (ms to weeks)
4. **Composable** (multiple rules coexist)
5. **Energy efficient** (~15x more than GPUs)
6. **Biologically plausible** (implementable in neurons)

These formulas provide a rich toolkit for:
- Neuromorphic computing
- Edge AI
- Continual learning
- Energy-efficient algorithms
- Brain-inspired architectures

**Next Steps**: Implement these in PyTorch, test on benchmarks, compare to backprop, explore hybrid approaches.

---

## Files Generated

1. **biological_learning_analysis.md**: Comprehensive analysis with detailed explanations and PyTorch implementations
2. **analyze_learning_formulas.py**: Python script for database analysis
3. **learning_formulas_quick_ref.md** (this file): Quick reference guide

**Database**: `/home/user/MAINFRAME/bioformulas/bioformulas.db`
