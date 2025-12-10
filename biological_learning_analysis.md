# Deep Dive: Biological Learning and Plasticity Rules

## Executive Summary
This analysis examines **33 unique biological learning formulas** from the BioFormulas database, spanning:
- 12 STDP variants
- 7 Hebbian & rate-based rules
- 5 homeostatic mechanisms
- 3 calcium-based models
- 2 metaplasticity rules
- 4 learning algorithms
- 2 reward learning formulas

---

## I. DETAILED ANALYSIS OF KEY LEARNING RULES

### A. SPIKE-TIMING DEPENDENT PLASTICITY (STDP)

#### 1. **Pair-Based STDP** [ID: 25]
**Formula:**
```
Δw = { A₊ exp(-Δt/τ₊)    if Δt > 0  (LTP)
     {-A₋ exp(Δt/τ₋)     if Δt < 0  (LTD)
```

**Biological Mechanism:**
- **LTP (Long-Term Potentiation)**: Pre-synaptic spike BEFORE post-synaptic spike (Δt > 0) → strengthen synapse
- **LTD (Long-Term Depression)**: Pre AFTER post (Δt < 0) → weaken synapse
- Implements causality detection: "neurons that fire together, wire together"
- Window: typically τ₊ ≈ 20ms, τ₋ ≈ 20ms

**Key Variables:**
- **Δt**: Spike timing difference (tpost - tpre)
- **A₊, A₋**: LTP/LTD amplitudes
- **τ₊, τ₋**: Time constants (asymmetric allows different temporal windows)

**Mathematical Properties:**
- **Stability**: Unbounded - requires weight constraints or homeostatic mechanisms
- **Fixed Points**: None inherently - weights drift to bounds
- **Locality**: Fully local (only pre/post spike times needed)
- **Causality**: Enforces temporal causality
- **Non-linearity**: Exponential decay creates critical temporal windows

---

#### 2. **Triplet STDP** [ID: 26]
**Formula:**
```
Δw = r₁(t)[A₂⁺ + A₃⁺r₂(t-ε)] - o₁(t)[A₂⁻ + A₃⁻o₂(t-ε)]
```

**Biological Mechanism:**
- Captures **frequency dependence** - triplet of spikes matters
- r₁, r₂: presynaptic traces (fast and slow)
- o₁, o₂: postsynaptic traces (fast and slow)
- Explains experimental data better than pair-based STDP

**Key Variables:**
- **Triggers**: Individual spikes update traces
- **Modulation**: Previous activity history (r₂, o₂ traces)
- **Frequency**: High-frequency bursts → stronger plasticity

**Mathematical Properties:**
- **Stability**: Better than pair-based (nonlinear suppression at high rates)
- **Fixed Points**: Activity-dependent equilibrium
- **Memory**: Maintains history via traces (differential equations)
- **Bounded**: A₃ terms provide frequency-dependent saturation

---

#### 3. **Voltage-Dependent STDP (Clopath)** [ID: 502]
**Formula:**
```
dw/dt = A_LTD x̄(V - θ_LTD)₋ + A_LTP x(V̄ - θ_LTP)₊(V - θ_LTD)₊
```

**Biological Mechanism:**
- Uses **dendritic voltage** instead of spikes
- More biologically realistic (dendrites compute with voltage)
- (·)₊ = max(·, 0), (·)₋ = min(·, 0)
- x: presynaptic trace, x̄: low-pass filtered
- V̄: low-pass filtered voltage

**Key Variables:**
- **Triggers**: Voltage crossing thresholds (θ_LTD, θ_LTP)
- **Modulation**: Presynaptic activity trace
- **Thresholds**: θ_LTD ≈ -70mV, θ_LTP ≈ -50mV (depolarization)

**Mathematical Properties:**
- **Stability**: Voltage-dependent bounds prevent runaway
- **Thresholding**: Requires sufficient depolarization
- **Local**: Voltage is local variable
- **Continuous**: ODE formulation (not discrete spikes)

---

#### 4. **Multiplicative STDP (Soft Bounds)** [ID: 499]
**Formula:**
```
Δw = { (wₘₐₓ - w)·f₊(Δt)    LTP
     { w·f₋(Δt)             LTD
```

**Biological Mechanism:**
- **Weight-dependent plasticity** prevents saturation
- Strong weights: harder to strengthen, easier to weaken
- Weak weights: easier to strengthen, harder to weaken completely
- Maintains weights in (0, wₘₐₓ)

**Mathematical Properties:**
- **Stability**: STABLE - self-limiting
- **Fixed Points**: Competition-dependent equilibrium
- **Bounds**: Naturally constrained to [0, wₘₐₓ]
- **Multiplicative**: Preserves relative weight distributions

---

### B. HEBBIAN & RATE-BASED RULES

#### 5. **BCM (Bienenstock-Cooper-Munro) Rule** [ID: 27]
**Formula:**
```
dw/dt = η φ(c) c_pre
φ(c) = c(c - θₘ)
```

**Biological Mechanism:**
- **Sliding threshold** θₘ adjusts based on postsynaptic activity
- Below threshold → LTD, above threshold → LTP
- Enables **selectivity** - neurons become tuned to specific inputs
- Stabilizes Hebbian learning

**Key Variables:**
- **c**: Postsynaptic activity (firing rate)
- **c_pre**: Presynaptic activity
- **θₘ**: Modification threshold (slides with activity)

**Mathematical Properties:**
- **Stability**: STABLE via sliding threshold
- **Fixed Points**: θₘ = E[c²] (BCM theorem)
- **Selectivity**: Quadratic function creates competition
- **Metaplasticity**: Threshold changes on slower timescale

---

#### 6. **Oja's Rule** [ID: 29]
**Formula:**
```
Δwᵢ = η y(xᵢ - y wᵢ)
```

**Biological Mechanism:**
- Hebbian term (y·xᵢ) + normalization term (-y²wᵢ)
- Implements **Principal Component Analysis (PCA)**
- Weights converge to eigenvector of input covariance matrix
- Maintains ||w|| ≈ constant

**Key Variables:**
- **x**: Input vector
- **y**: Output (y = w·x)
- **η**: Learning rate

**Mathematical Properties:**
- **Stability**: STABLE - weight normalization term
- **Fixed Points**: w ∝ principal eigenvector
- **Bounded**: ||w|| → 1/√η
- **Convergence**: Proven to extract first principal component
- **Unsupervised**: No external teaching signal

---

#### 7. **Covariance Learning** [ID: 583]
**Formula:**
```
Δwᵢⱼ = η(xᵢ - x̄ᵢ)(yⱼ - ȳⱼ)
```

**Biological Mechanism:**
- Learns **correlations** (not just co-activation)
- Subtracts mean → detects deviations from baseline
- More stable than pure Hebbian (w = xy)
- Implements decorrelation / whitening

**Mathematical Properties:**
- **Stability**: More stable than Hebbian (zero mean)
- **Fixed Points**: w ∝ covariance matrix
- **Bounded**: Mean subtraction prevents runaway
- **Statistical**: Learns second-order statistics

---

### C. CALCIUM-BASED PLASTICITY

#### 8. **Shouval Calcium Model** [ID: 493]
**Formula:**
```
dw/dt = η([Ca])·(Ω([Ca]) - w)
Ω([Ca]) = sig([Ca] - θ_LTP) - 0.5·sig([Ca] - θ_LTD)
```

**Biological Mechanism:**
- **Calcium concentration** determines plasticity direction
- Low [Ca] → LTD
- Medium [Ca] → no change
- High [Ca] → LTP
- Unifies NMDA receptor dynamics with plasticity

**Key Variables:**
- **[Ca]**: Postsynaptic calcium concentration
- **θ_LTD, θ_LTP**: Calcium thresholds
- **Ω**: Direction function (positive → LTP, negative → LTD)

**Mathematical Properties:**
- **Stability**: Bounded by (Ω([Ca]) - w) term
- **Fixed Points**: w = Ω([Ca]) (activity-dependent)
- **Thresholds**: Biphasic response (LTD/LTP regions)
- **Continuous**: Smooth transition between LTD/LTP
- **Biological**: Directly models Ca²⁺ signaling cascades

---

### D. HOMEOSTATIC PLASTICITY

#### 9. **Synaptic Scaling** [ID: 508]
**Formula:**
```
dw/dt = α(r_target - r)
```

**Biological Mechanism:**
- **Global homeostasis** - maintains target firing rate
- Prevents runaway excitation/depression
- Multiplicative scaling preserves relative weight structure
- Operates on slower timescale than Hebbian plasticity

**Key Variables:**
- **r**: Current firing rate
- **r_target**: Target firing rate (e.g., 5 Hz)
- **α**: Homeostatic gain

**Mathematical Properties:**
- **Stability**: STABLE - negative feedback
- **Fixed Points**: r = r_target
- **Timescale**: Hours to days (vs. ms for STDP)
- **Global**: All weights scaled similarly
- **Preserves structure**: Multiplicative → maintains weight ratios

---

#### 10. **Heterosynaptic Plasticity** [ID: 511]
**Formula:**
```
Δwᵢ = -γ Σⱼ≠ᵢ Δwⱼ
```

**Biological Mechanism:**
- **Local competition** between synapses
- If other synapses strengthen, this one weakens
- Maintains total synaptic strength
- More local than global scaling

**Mathematical Properties:**
- **Stability**: Zero-sum constraint
- **Conservation**: Σᵢ wᵢ = constant
- **Competition**: Winner-take-all dynamics
- **Local**: Operates at single dendritic branch

---

### E. REWARD-MODULATED LEARNING

#### 11. **Reward-Modulated STDP** [ID: 504]
**Formula:**
```
dw/dt = c·STDP(Δt)·(R - R̄)
```

**Biological Mechanism:**
- **Three-factor learning rule**:
  1. Pre-post correlation (STDP)
  2. Eligibility trace (c)
  3. Reward signal (R - R̄)
- Implements **reinforcement learning**
- Dopamine provides reward signal
- Explains basal ganglia learning

**Key Variables:**
- **STDP(Δt)**: Spike-timing signal
- **c**: Eligibility trace (memory of recent activity)
- **R - R̄**: Reward prediction error

**Mathematical Properties:**
- **Stability**: Depends on reward structure
- **Credit Assignment**: Eligibility trace bridges temporal gap
- **Exploration**: Noise in eligibility trace
- **Delayed reward**: Can learn from delayed reinforcement

---

## II. COMMON PRINCIPLES ACROSS BIOLOGICAL LEARNING RULES

### 1. **Locality**
- All rules use **only local variables** (pre/post activity, voltage, Ca²⁺)
- No global error signals
- No backpropagation of errors
- Physically implementable in synaptic machinery

### 2. **Multiple Timescales**
- Fast: Spike timing (ms) - STDP
- Medium: Firing rates (100ms-1s) - Hebbian, BCM
- Slow: Homeostatic (hours-days) - Synaptic scaling
- Very slow: Metaplasticity (days-weeks) - Threshold changes

### 3. **Stability Mechanisms**
- **Weight dependence**: Multiplicative STDP
- **Sliding thresholds**: BCM
- **Normalization**: Oja's rule
- **Homeostatic**: Synaptic scaling
- **Competition**: Heterosynaptic plasticity

### 4. **Correlation-Based**
- Detect correlations between pre/post activity
- Not gradient descent
- Unsupervised (except reward-modulated)

### 5. **Threshold Nonlinearities**
- Calcium thresholds (LTD/LTP)
- Voltage thresholds (Clopath)
- Activity thresholds (BCM)
- Implement decision boundaries

### 6. **Temporal Sensitivity**
- STDP: Causality detection (order matters)
- Triplet STDP: Frequency matters
- Reward-modulated: Temporal credit assignment

---

## III. COMPARISON WITH BACKPROPAGATION

| Property | Biological Learning | Backpropagation |
|----------|-------------------|-----------------|
| **Locality** | Fully local | Non-local (error propagation) |
| **Error Signal** | No explicit error | Requires target/error |
| **Symmetry** | No weight symmetry needed | Requires symmetric weights |
| **Online Learning** | Continuous, online | Typically batch-based |
| **Supervision** | Unsupervised (mostly) | Supervised |
| **Stability** | Built-in mechanisms | Requires regularization |
| **Credit Assignment** | Local correlation | Global gradient |
| **Energy Efficiency** | Low (local computation) | High (global computation) |
| **Biological Plausibility** | High | Low |
| **Learning Speed** | Slow (but online) | Fast (with large batches) |
| **Convergence Guarantees** | Limited | Strong (for convex) |

### Key Differences:

1. **No Backward Pass**: Biological rules don't propagate errors backward
2. **No Separate Phases**: No forward/backward distinction
3. **No Weight Transport**: Don't need symmetric weights
4. **Spontaneous Activity**: Learn from intrinsic dynamics, not just external input
5. **Multi-Objective**: Simultaneously optimize multiple objectives (selectivity, stability, efficiency)

---

## IV. ADVANTAGES OF BIOLOGICAL LEARNING

### 1. **Local Computation**
- Each synapse computes independently
- Massively parallelizable
- No communication overhead
- Scales to billions of synapses

### 2. **Online Learning**
- Learn continuously from data stream
- No batch requirements
- Adapt to non-stationary environments
- No separate train/test phases

### 3. **Energy Efficiency**
- No backward pass (50% savings)
- Sparse updates (only active synapses)
- Event-driven (spike-based)
- Brain: ~20W vs. GPU: ~300W

### 4. **Robustness**
- Homeostatic mechanisms prevent instability
- Graceful degradation with damage
- No catastrophic forgetting (with consolidation)
- Noise tolerance

### 5. **Unsupervised/Self-Supervised**
- Most rules don't require labels
- Learn structure from data
- Temporal prediction (next-step prediction)
- Anomaly detection

### 6. **Composability**
- Multiple learning rules coexist
- Different timescales don't interfere
- Hebbian + homeostatic + neuromodulation
- Hierarchical learning

---

## V. PYTORCH IMPLEMENTATIONS

### Implementation 1: STDP Layer

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class STDPLayer(nn.Module):
    """
    Spike-Timing Dependent Plasticity Layer

    Implements pair-based STDP with exponential kernels.
    Differentiable approximation using soft spike rates.
    """

    def __init__(self, in_features, out_features,
                 A_plus=0.01, A_minus=0.01,
                 tau_plus=20.0, tau_minus=20.0,
                 w_max=1.0, dt=1.0):
        super().__init__()

        # Initialize weights
        self.weight = nn.Parameter(torch.randn(out_features, in_features) * 0.1)

        # STDP parameters
        self.A_plus = A_plus
        self.A_minus = A_minus
        self.tau_plus = tau_plus
        self.tau_minus = tau_minus
        self.w_max = w_max
        self.dt = dt

        # Traces for temporal integration
        self.register_buffer('pre_trace', torch.zeros(in_features))
        self.register_buffer('post_trace', torch.zeros(out_features))

    def forward(self, x):
        """
        x: input spike rates [batch, in_features]
        returns: output spike rates [batch, out_features]
        """
        # Linear transformation
        y = F.linear(x, self.weight.clamp(0, self.w_max))

        # Apply nonlinearity (soft spike rate)
        y = torch.sigmoid(y)

        return y

    def stdp_update(self, x, y):
        """
        Update weights based on STDP rule

        x: pre-synaptic activity [batch, in_features]
        y: post-synaptic activity [batch, out_features]
        """
        # Average over batch
        x_mean = x.mean(dim=0)
        y_mean = y.mean(dim=0)

        # Update traces (exponential decay)
        alpha_pre = torch.exp(-self.dt / self.tau_plus)
        alpha_post = torch.exp(-self.dt / self.tau_minus)

        self.pre_trace = alpha_pre * self.pre_trace + x_mean
        self.post_trace = alpha_post * self.post_trace + y_mean

        # STDP weight update
        # LTP: post spike occurs, pre_trace indicates recent pre activity
        ltp = self.A_plus * torch.outer(y_mean, self.pre_trace)

        # LTD: pre spike occurs, post_trace indicates recent post activity
        ltd = self.A_minus * torch.outer(self.post_trace, x_mean)

        # Combined update
        dw = ltp - ltd

        # Multiplicative normalization (soft bounds)
        dw_ltp = (self.w_max - self.weight) * (dw > 0).float() * dw
        dw_ltd = self.weight * (dw < 0).float() * dw

        # Apply update
        with torch.no_grad():
            self.weight.add_(dw_ltp + dw_ltd)
            self.weight.clamp_(0, self.w_max)

# Example usage
stdp_layer = STDPLayer(784, 100)
x = torch.rand(32, 784)  # batch of inputs

# Forward pass
y = stdp_layer(x)

# STDP learning (call after each forward pass)
stdp_layer.stdp_update(x, y)
```

---

### Implementation 2: BCM Layer with Sliding Threshold

```python
class BCMLayer(nn.Module):
    """
    Bienenstock-Cooper-Munro learning rule

    Implements BCM with sliding threshold for selectivity.
    Stabilizes Hebbian learning.
    """

    def __init__(self, in_features, out_features,
                 eta=0.01, tau_theta=1000.0, theta_0=1.0):
        super().__init__()

        # Initialize weights
        self.weight = nn.Parameter(torch.randn(out_features, in_features) * 0.1)
        self.bias = nn.Parameter(torch.zeros(out_features))

        # BCM parameters
        self.eta = eta
        self.tau_theta = tau_theta

        # Sliding threshold (one per output neuron)
        self.register_buffer('theta', torch.ones(out_features) * theta_0)

        # Running average of activity squared
        self.register_buffer('activity_sq_avg', torch.ones(out_features) * theta_0)

    def forward(self, x):
        """
        x: input [batch, in_features]
        returns: output activity [batch, out_features]
        """
        # Linear transformation
        c = F.linear(x, self.weight, self.bias)

        # Nonlinearity (ReLU or sigmoid)
        c = F.relu(c)

        return c

    def phi(self, c):
        """BCM selectivity function"""
        # phi(c) = c(c - theta)
        return c * (c - self.theta.unsqueeze(0))

    def bcm_update(self, x, c):
        """
        Update weights using BCM rule

        x: pre-synaptic activity [batch, in_features]
        c: post-synaptic activity [batch, out_features]
        """
        # Average over batch
        x_mean = x.mean(dim=0)
        c_mean = c.mean(dim=0)

        # Update sliding threshold
        # theta <- theta + (c^2 - theta)/tau_theta
        c_sq = c_mean ** 2
        self.activity_sq_avg = (
            (1 - 1/self.tau_theta) * self.activity_sq_avg +
            (1/self.tau_theta) * c_sq
        )
        self.theta = self.activity_sq_avg

        # BCM weight update
        # dw = eta * phi(c) * x_pre
        phi_c = self.phi(c_mean)
        dw = self.eta * torch.outer(phi_c, x_mean)

        # Apply update
        with torch.no_grad():
            self.weight.add_(dw)

            # Optional: weight normalization to prevent unbounded growth
            weight_norm = self.weight.norm(dim=1, keepdim=True)
            self.weight.div_(weight_norm + 1e-8)

# Example usage
bcm_layer = BCMLayer(784, 100)
x = torch.rand(32, 784)

# Forward pass
c = bcm_layer(x)

# BCM learning
bcm_layer.bcm_update(x, c)

# Check threshold adaptation
print(f"Thresholds: {bcm_layer.theta[:5]}")  # First 5 neurons
```

---

### Implementation 3: Reward-Modulated STDP (3-Factor Learning)

```python
class RewardModulatedSTDPLayer(nn.Module):
    """
    Reward-Modulated STDP (3-factor learning rule)

    Combines:
    1. Pre-post correlation (STDP)
    2. Eligibility trace
    3. Reward signal (dopamine)

    Implements reinforcement learning with biologically plausible rules.
    """

    def __init__(self, in_features, out_features,
                 A_plus=0.01, A_minus=0.01,
                 tau_plus=20.0, tau_minus=20.0,
                 tau_eligibility=1000.0,
                 w_max=1.0, dt=1.0):
        super().__init__()

        # Weights
        self.weight = nn.Parameter(torch.randn(out_features, in_features) * 0.1)

        # STDP parameters
        self.A_plus = A_plus
        self.A_minus = A_minus
        self.tau_plus = tau_plus
        self.tau_minus = tau_minus
        self.tau_e = tau_eligibility
        self.w_max = w_max
        self.dt = dt

        # Traces
        self.register_buffer('pre_trace', torch.zeros(in_features))
        self.register_buffer('post_trace', torch.zeros(out_features))

        # Eligibility trace (memory of recent STDP events)
        self.register_buffer('eligibility',
                           torch.zeros(out_features, in_features))

        # Reward baseline (running average)
        self.register_buffer('reward_baseline', torch.tensor(0.0))
        self.reward_alpha = 0.01

    def forward(self, x):
        """Forward pass"""
        y = F.linear(x, self.weight.clamp(0, self.w_max))
        y = torch.sigmoid(y)
        return y

    def update_traces(self, x, y):
        """Update activity traces"""
        x_mean = x.mean(dim=0)
        y_mean = y.mean(dim=0)

        # Exponential decay
        alpha_pre = torch.exp(-self.dt / self.tau_plus)
        alpha_post = torch.exp(-self.dt / self.tau_minus)

        self.pre_trace = alpha_pre * self.pre_trace + x_mean
        self.post_trace = alpha_post * self.post_trace + y_mean

        # Compute STDP signal
        ltp = self.A_plus * torch.outer(y_mean, self.pre_trace)
        ltd = self.A_minus * torch.outer(self.post_trace, x_mean)
        stdp_signal = ltp - ltd

        # Update eligibility trace (decaying memory of STDP)
        alpha_e = torch.exp(-self.dt / self.tau_e)
        self.eligibility = alpha_e * self.eligibility + stdp_signal

    def reward_update(self, reward):
        """
        Apply reward-modulated weight update

        reward: scalar reward signal
        """
        # Update reward baseline
        self.reward_baseline = (
            (1 - self.reward_alpha) * self.reward_baseline +
            self.reward_alpha * reward
        )

        # Reward prediction error
        reward_error = reward - self.reward_baseline

        # Weight update: eligibility trace * reward error
        dw = self.eligibility * reward_error

        with torch.no_grad():
            self.weight.add_(dw)
            self.weight.clamp_(0, self.w_max)

    def train_step(self, x, reward):
        """
        Complete training step

        x: input
        reward: scalar reward (e.g., 1 for correct, 0 for incorrect)
        """
        # Forward pass
        y = self.forward(x)

        # Update traces and eligibility
        self.update_traces(x, y)

        # Apply reward-modulated update
        self.reward_update(reward)

        return y

# Example usage in reinforcement learning task
reward_layer = RewardModulatedSTDPLayer(10, 3)

# Simulate learning episode
for step in range(100):
    # Get state
    state = torch.rand(1, 10)

    # Forward pass (select action based on output)
    action_probs = reward_layer(state)
    action = torch.multinomial(action_probs.squeeze(), 1).item()

    # Get reward from environment
    reward = 1.0 if action == 2 else 0.0  # Example: action 2 is correct

    # Learning update
    reward_layer.train_step(state, reward)

    if step % 10 == 0:
        print(f"Step {step}: Reward baseline = {reward_layer.reward_baseline:.3f}")
```

---

### Implementation 4: Homeostatic Plasticity (Bonus)

```python
class HomeostaticLayer(nn.Module):
    """
    Neural layer with homeostatic synaptic scaling

    Maintains target firing rate through global weight scaling.
    Prevents runaway dynamics from Hebbian learning.
    """

    def __init__(self, in_features, out_features,
                 target_rate=0.1, alpha_homeostatic=0.001):
        super().__init__()

        self.weight = nn.Parameter(torch.randn(out_features, in_features) * 0.1)
        self.bias = nn.Parameter(torch.zeros(out_features))

        self.target_rate = target_rate
        self.alpha_h = alpha_homeostatic

        # Running average of firing rates
        self.register_buffer('avg_rate',
                           torch.ones(out_features) * target_rate)

    def forward(self, x):
        y = F.linear(x, self.weight, self.bias)
        y = torch.sigmoid(y)
        return y

    def homeostatic_update(self, y):
        """
        Synaptic scaling to maintain target rate
        """
        # Update running average of activity
        y_mean = y.mean(dim=0)
        self.avg_rate = 0.99 * self.avg_rate + 0.01 * y_mean

        # Scaling factor
        scale = self.target_rate / (self.avg_rate + 1e-8)

        with torch.no_grad():
            # Multiplicative scaling (preserves weight structure)
            self.weight.mul_(1 + self.alpha_h * (scale.unsqueeze(1) - 1))
            self.bias.add_(self.alpha_h * (self.target_rate - self.avg_rate))

# Combined STDP + Homeostatic layer
class BiologicalPlasticityLayer(nn.Module):
    """
    Combines fast Hebbian learning with slow homeostatic regulation
    """

    def __init__(self, in_features, out_features):
        super().__init__()

        # Use STDP for fast plasticity
        self.stdp = STDPLayer(in_features, out_features)

        # Homeostatic parameters
        self.target_rate = 0.1
        self.alpha_h = 0.0001  # Slow timescale

        self.register_buffer('avg_rate',
                           torch.ones(out_features) * self.target_rate)

    def forward(self, x):
        return self.stdp(x)

    def plasticity_update(self, x, y):
        """Apply both fast and slow plasticity"""
        # Fast: STDP
        self.stdp.stdp_update(x, y)

        # Slow: Homeostatic scaling
        y_mean = y.mean(dim=0)
        self.avg_rate = 0.999 * self.avg_rate + 0.001 * y_mean

        scale = self.target_rate / (self.avg_rate + 1e-8)

        with torch.no_grad():
            self.stdp.weight.mul_(1 + self.alpha_h * (scale.unsqueeze(1) - 1))
```

---

## VI. SYNTHESIS AND INSIGHTS

### Key Insights:

1. **Biological learning is fundamentally different from backprop**
   - Local vs. global
   - Online vs. batch
   - Multi-timescale vs. single-timescale
   - Correlation-based vs. gradient-based

2. **Stability emerges from multiple mechanisms**
   - No single mechanism ensures stability
   - Combination of weight-dependence, homeostasis, competition, thresholds
   - Multiple timescales provide separation of concerns

3. **Learning rules are composable**
   - STDP + homeostasis
   - Hebbian + metaplasticity
   - Unsupervised + reward-modulated
   - Each addresses different aspect of learning

4. **Trade-offs exist**
   - Speed vs. stability
   - Locality vs. global optimization
   - Biological plausibility vs. performance
   - Energy efficiency vs. learning speed

5. **Emerging research directions**
   - Hybrid systems (biological rules + backprop)
   - Neuromorphic hardware (event-driven, low power)
   - Continual learning (no catastrophic forgetting)
   - Energy-efficient AI

---

## VII. FUTURE DIRECTIONS

### For Neural Networks:
1. **Local learning rules** for edge devices (no GPU backprop)
2. **Online continual learning** without catastrophic forgetting
3. **Energy-efficient training** for sustainable AI
4. **Neuromorphic chips** implementing STDP in hardware

### For Neuroscience:
1. **Unifying theory** of biological learning
2. **Role of astrocytes** and glia in plasticity
3. **Interaction** between learning rules
4. **Developmental plasticity** vs. adult learning

### Hybrid Approaches:
1. **Equilibrium propagation** (local gradient approximation)
2. **Target propagation** (local targets, no backward pass)
3. **Predictive coding** (hierarchical prediction errors)
4. **Forward-forward algorithm** (Hinton 2022) - two forward passes

---

## CONCLUSION

The BioFormulas database contains a rich collection of **33+ biological learning rules** spanning multiple timescales, mechanisms, and computational principles. These rules reveal that biological learning:

1. **Prioritizes locality and energy efficiency** over global optimization
2. **Achieves stability through multiple complementary mechanisms**
3. **Operates continuously online** without separate training phases
4. **Combines multiple learning signals** (correlation, reward, homeostasis)
5. **Scales to billions of synapses** through parallelism

While backpropagation remains superior for supervised learning with large labeled datasets, biological learning rules offer compelling advantages for:
- **Edge AI** (local, low-power)
- **Continual learning** (no catastrophic forgetting)
- **Unsupervised learning** (structure discovery)
- **Neuromorphic computing** (brain-inspired hardware)

The PyTorch implementations above demonstrate that these rules can be implemented in modern deep learning frameworks, opening pathways for hybrid approaches that combine the best of biological and artificial intelligence.
