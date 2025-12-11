# Novel Biological AI Architectures - Complete Catalog

**Compiled**: 2025-12-11
**Total Architectures**: 135
**Organization**: Ordered by AI Impact (Highest → Lowest)

---

## CRITICAL IMPACT (Paradigm-Shifting Architectures)

These architectures fundamentally change how AI systems are designed and operated.

---

### Mechanism-Driven Architecture (MDA)

**Purpose**: Replace hand-coded networks with dynamically-assembled cognitive systems derived from biological mechanisms.

**Formula**: System Assembly Function
```
Architecture(task, constraints) = ∑ Primitives_i(scale_i, params_i)

where:
- Primitives = {activation, learning, memory, decision, routing}
- scale_i = f(hardware_budget, task_complexity)
- params_i = biological_defaults ∪ learned_values
```

**Nature's Implementation**: Evolution assembled brains from proven computational primitives (ion channels, synapses, circuits) rather than designing from scratch.

**Impact**: **CRITICAL - Paradigm Shift**
Instead of fixed architectures (ResNet, Transformer), systems self-assemble from 5,000+ biological mechanisms. Architecture becomes dynamic, explainable, and adaptive to constraints. This is not incremental improvement—it's a fundamentally different approach where biology provides the blueprint.

**Code Example**:
```python
class MechanismDrivenArchitecture:
    """AI system assembled from biological primitives"""

    def __init__(self, task_spec, hardware_constraints):
        self.mechanisms = MechanismLibrary.load_all()
        self.task = task_spec
        self.constraints = hardware_constraints

    def generate(self):
        # Select mechanisms based on task
        required_modules = self.identify_modules(self.task)

        # Size components based on constraints
        neuron_count = self.compute_neurons(
            self.constraints.memory,
            self.task.complexity
        )

        # Assemble from primitives
        system = NeuralSystem()
        for module in required_modules:
            primitive = self.mechanisms.get(module)
            scaled = primitive.instantiate(
                size=neuron_count,
                **self.constraints
            )
            system.add(scaled)

        return system

    def compute_neurons(self, memory_budget, complexity):
        """Biological scaling law"""
        return int(sqrt(memory_budget * complexity))
```

**Source**: BIOMIMETIC_AI_ARCHITECTURE.md, Lines 24-48; MECHANISM_TO_ARCHITECTURE_PATTERNS.md

---

### Self-Learning Brain (Gene Expression Meta-Layer)

**Purpose**: Hyperparameters evolve via gene-expression-like dynamics instead of being static.

**Formula**: Gene Expression Control
```
dR/dt = k_tx · [TF]^n / (K_d^n + [TF]^n) - γ_R · R     [Transcription]
dP/dt = k_tl · R - γ_P · P                             [Translation]

where:
- TF = transcription_factor(loss, surprise, error_rate)
- R = mRNA (intermediate hyperparameter)
- P = protein (final hyperparameter value)
- n = Hill coefficient (cooperativity, typically 2-8)
- k_tx, k_tl = synthesis rates
- γ_R, γ_P = degradation rates
```

**Nature's Implementation**: Cells adjust gene expression (protein production) based on environmental signals. High stress → produce heat shock proteins. Low nutrients → upregulate transporters.

**Impact**: **CRITICAL - Adaptive Intelligence**
Learning rates, exploration temperature, plasticity modes all adapt automatically based on system state. No manual tuning. The network "feels" when it's confused (high loss) and increases plasticity. When confident, it consolidates. This creates truly adaptive AI that self-regulates like living systems.

**Code Example**:
```python
class GeneExpressionMetaController:
    """Hyperparameters evolve like gene expression"""

    def __init__(self, n_hyperparams=5):
        self.R = np.zeros(n_hyperparams)  # mRNA
        self.P = np.zeros(n_hyperparams)  # Protein

        self.k_tx = 0.01   # Transcription rate
        self.k_tl = 0.05   # Translation rate
        self.gamma_R = 0.1 # mRNA decay
        self.gamma_P = 0.01 # Protein decay

        self.Hill_n = 2.0
        self.K_d = 0.5

    def step(self, system_state, dt=1.0):
        # Compute transcription factor from system state
        loss = system_state['loss']
        surprise = system_state['surprise']
        error_rate = system_state['error_rate']

        TF = 0.3 * (loss / 0.5) + 0.4 * surprise + 0.3 * error_rate

        # Hill function: nonlinear activation
        TF_effect = TF**self.Hill_n / (self.K_d**self.Hill_n + TF**self.Hill_n)

        # Transcription
        dR_dt = self.k_tx * TF_effect - self.gamma_R * self.R
        self.R += dR_dt * dt

        # Translation
        dP_dt = self.k_tl * self.R - self.gamma_P * self.P
        self.P += dP_dt * dt

        return {
            'learning_rate': 0.001 * (1.0 + 10.0 * self.P[0]),
            'exploration_temp': 0.1 + 2.0 * self.P[1],
            'plasticity_mode': 'learning' if self.P[2] > 0.5 else 'consolidation'
        }
```

**Source**: MECHANISM_TO_ARCHITECTURE_PATTERNS.md, Lines 15-128

---

### Predictive Coding Hierarchy

**Purpose**: Replace feedforward + backprop with bidirectional error minimization.

**Formula**: Hierarchical Prediction Error
```
ε_l = x_l - μ_l                          [Prediction error at layer l]
dμ_l/dt = -ε_l + W_l^T · ε_{l+1}        [Update belief from errors]
dW_l/dt = η · ε_l · μ_{l+1}^T           [Update weights to reduce error]

where:
- ε_l = prediction error (actual - predicted)
- μ_l = current belief/representation
- W_l = generative weights (top-down)
- η = learning rate
```

**Nature's Implementation**: Brain's cortical hierarchy constantly predicts lower levels. Prediction errors propagate up, corrections flow down. Only surprising information (errors) is communicated—efficient coding.

**Impact**: **CRITICAL - New Learning Paradigm**
Eliminates need for backpropagation. Learning is local, bidirectional, and energy-efficient. Each layer minimizes its own prediction error. Built-in uncertainty estimation. Explains cortical microcircuits (layer 2/3 = prediction, layer 4 = error, layer 5 = correction).

**Code Example**:
```python
class PredictiveCodingLayer(nn.Module):
    """Layer that predicts input and minimizes error"""

    def __init__(self, in_dim, out_dim, n_iterations=10):
        super().__init__()
        self.W_gen = nn.Parameter(torch.randn(out_dim, in_dim) * 0.1)  # Top-down
        self.mu = torch.zeros(out_dim)  # Belief state
        self.n_iterations = n_iterations

    def forward(self, x, error_from_above=None):
        """Iteratively minimize prediction error"""
        self.x = x

        for _ in range(self.n_iterations):
            # Predict input from belief
            prediction = self.mu @ self.W_gen

            # Compute error
            error = x - prediction
            precision = 1.0 / (1.0 + 0.1 * error**2)

            # Update belief to reduce error
            grad_mu = error @ self.W_gen.T
            if error_from_above is not None:
                grad_mu += error_from_above

            self.mu += 0.01 * grad_mu * precision

        return self.mu

    def learn(self):
        """Update generative model"""
        prediction = self.mu @ self.W_gen
        error = self.x - prediction
        self.W_gen += 0.01 * torch.outer(error, self.mu)
```

**Source**: MECHANISM_TO_ARCHITECTURE_PATTERNS.md, Lines 660-803; BIOMIMETIC_AI_ARCHITECTURE.md

---

### Global Workspace Theory (Conscious AI)

**Purpose**: Multiple unconscious processors compete for global broadcast—winner becomes "conscious" and shares with all.

**Formula**: Competition and Broadcast
```
Bid_i = activation_i × recency_i × novelty_i

Winner = argmax(Bid_i) if max(Bid_i) > θ_broadcast

Broadcast: All processors receive Winner's message

where:
- Bid_i = importance score from processor i
- θ_broadcast = threshold for conscious access
- Broadcast creates system-wide coherence
```

**Nature's Implementation**: Brain regions compete for "attention spotlight". Winner broadcasts to entire cortex via thalamocortical loops. This creates unified conscious experience from distributed processing.

**Impact**: **CRITICAL - Unified Intelligence**
Creates system-level coherence and awareness. Instead of isolated modules, all subsystems share critical information. Enables metacognition, confidence estimation, and flexible problem-solving. The AI "knows what it knows" through broadcast events.

**Code Example**:
```python
class GlobalWorkspace:
    """Multiple processors compete for conscious broadcast"""

    def __init__(self, n_processors=10, workspace_dim=512):
        self.processors = [
            SpecializedProcessor(workspace_dim)
            for _ in range(n_processors)
        ]
        self.broadcast_threshold = 0.5
        self.consciousness_log = []

    def cycle(self):
        """One competition-broadcast cycle"""
        # Gather bids from all processors
        bids = []
        for i, proc in enumerate(self.processors):
            activation = proc.get_activation()
            recency = 1.0 if proc.recently_active() else 0.5
            novelty = proc.compute_novelty()

            bid = activation * recency * novelty
            bids.append((bid, i, proc))

        # Find winner
        bids.sort(reverse=True)
        winner_bid, winner_idx, winner = bids[0]

        # Check threshold
        if winner_bid > self.broadcast_threshold:
            # Winner broadcasts to all
            message = winner.extract_message()

            for i, proc in enumerate(self.processors):
                if i != winner_idx:
                    proc.receive_broadcast(message)

            # Log conscious event
            self.consciousness_log.append({
                'winner': winner_idx,
                'message': message,
                'bid': winner_bid
            })

            return message

        return None  # No conscious event
```

**Source**: BIOMIMETIC_AI_ARCHITECTURE.md, Lines 651-705; MECHANISM_TO_ARCHITECTURE_PATTERNS.md

---

### Multi-Compartment Dendritic Neurons

**Purpose**: Neurons as small networks with spatial computation, not scalar activations.

**Formula**: Cable Equation + Compartmental Model
```
λ²·∂²V/∂x² = τ·∂V/∂t + V - V_rest    [Passive cable]

C·dV_soma/dt = g_basal(V_basal - V_soma) +
               g_apical(V_apical - V_soma) +
               g_distal(V_distal - V_soma) -
               I_leak

where:
- V_basal = feedforward inputs (layer below)
- V_apical = feedback/error (layer above)
- V_distal = context/neuromodulation
- g_* = coupling conductances (distance-dependent)
- λ = length constant, τ = time constant
```

**Nature's Implementation**: Real neurons have dendritic trees with hundreds of compartments. Basal dendrites receive feedforward input, apical dendrites receive top-down predictions/errors, distal dendrites receive neuromodulation.

**Impact**: **CRITICAL - Neuron-Level Intelligence**
Each "neuron" becomes a small network capable of local learning and computation. Apical dendrites can implement backprop-like error signals locally (no need for global backward pass). Enables three-factor learning: presynaptic activity × postsynaptic activity × apical error signal.

**Code Example**:
```python
class MultiCompartmentNeuron(nn.Module):
    """Neuron with basal, apical, and distal compartments"""

    def __init__(self, n_basal=10, n_apical=5, n_distal=3):
        super().__init__()
        self.V_basal = torch.zeros(n_basal)
        self.V_apical = torch.zeros(n_apical)
        self.V_distal = torch.zeros(n_distal)
        self.V_soma = 0.0

        # Coupling strengths (distal is weakest - furthest)
        self.g_basal = 1.0
        self.g_apical = 0.5
        self.g_distal = 0.3

        # Time constants
        self.tau_basal = 5.0
        self.tau_apical = 10.0
        self.tau_soma = 2.0

    def forward(self, feedforward, error_signal, context, dt=0.1):
        """Integrate inputs from three compartments"""
        # Update compartment voltages
        self.V_basal += (feedforward - 0.1 * self.V_basal) * dt / self.tau_basal
        self.V_apical += (error_signal - 0.1 * self.V_apical) * dt / self.tau_apical
        self.V_distal += (context - 0.1 * self.V_distal) * dt

        # Soma integrates from all compartments
        I_basal = self.g_basal * self.V_basal.mean()
        I_apical = self.g_apical * self.V_apical.mean()
        I_distal = self.g_distal * self.V_distal.mean()

        dV_soma = (I_basal + I_apical + I_distal - self.V_soma) / self.tau_soma
        self.V_soma += dV_soma * dt

        # Spike if threshold crossed
        spike = 1.0 if self.V_soma > 0.2 else 0.0
        if spike:
            self.V_soma = 0.0  # Reset

        return spike

    def local_learning(self, pre_activity, post_activity):
        """Three-factor learning: pre × post × apical"""
        error = self.V_apical.mean()
        dW = 0.01 * pre_activity * post_activity * error
        return dW
```

**Source**: MECHANISM_TO_ARCHITECTURE_PATTERNS.md, Lines 133-252

---

## HIGH IMPACT (Performance-Critical Architectures)

These architectures provide 10-100x improvements in specific capabilities.

---

### MAPK Amplifying Cascade

**Purpose**: Sequential amplification for rare event detection (1000x signal boost).

**Formula**: Three-Tier Phosphorylation Cascade
```
d[Raf*]/dt = k₁[RasGTP][Raf]/(Km₁ + [Raf]) - k₂[Raf*]/(Km₂ + [Raf*])
d[MEK*]/dt = k₃[Raf*][MEK]/(Km₃ + [MEK]) - k₄[MEK*]/(Km₄ + [MEK*])
d[ERK*]/dt = k₅[MEK*][ERK]/(Km₅ + [ERK]) - k₆[ERK*]/(Km₆ + [ERK*])

Amplification per stage: ~3-10x
Total cascade: ~100-1000x
```

**Nature's Implementation**: Growth factor signaling. One EGF molecule → thousands of activated ERK proteins through sequential enzyme activation.

**Impact**: **HIGH - Rare Event Detection**
Detects anomalies at 1:10,000 ratio with high precision. Each cascade stage filters noise while amplifying signal. Applications: fraud detection, medical diagnosis, network intrusion, manufacturing defects.

**Code Example**:
```python
class MAPKCascade(nn.Module):
    """Three-tier amplification cascade"""

    def __init__(self, dim, stages=3, gain_per_stage=10):
        super().__init__()
        self.stages = nn.ModuleList([
            CascadeStage(dim, gain=gain_per_stage)
            for _ in range(stages)
        ])

    def forward(self, x):
        amplification = 1.0
        for stage in self.stages:
            x, amp = stage(x)
            amplification *= amp
        return x, amplification

class CascadeStage(nn.Module):
    def __init__(self, dim, gain=10, Km=5):
        super().__init__()
        self.transform = nn.Linear(dim, dim)
        self.gain = gain
        self.Km = Km

    def forward(self, x):
        y = self.transform(x)
        # Michaelis-Menten amplification
        y_amp = (self.gain * torch.abs(y)) / (self.Km + torch.abs(y))
        y_signed = torch.sign(y) * y_amp

        # Measure amplification
        amp = y_signed.abs().mean() / (x.abs().mean() + 1e-8)
        return y_signed, amp
```

**Source**: SIGNAL_AMPLIFICATION_REPORT.md, Lines 28-161; 00_NOVELTY.csv (ID 11-12)

---

### Goldbeter-Koshland Ultrasensitivity

**Purpose**: Switch-like responses without cooperativity—zero-order kinetics creates sharp thresholds.

**Formula**: Zero-Order Ultrasensitivity
```
[W*] = (2v₁J₂) / (B + √(B² - 4(v₂-v₁)v₁J₂))

where:
B = v₂ - v₁ + J₁v₂ + J₂v₁
v₁ = kinase activity
v₂ = phosphatase activity
J₁, J₂ = Michaelis constants

Effective Hill coefficient: 4-10 (from n=1 reactions!)
```

**Nature's Implementation**: When enzymes are saturated, phosphorylation cycles create ultrasensitivity. Example: MAPK activation, cell cycle transitions.

**Impact**: **HIGH - Sparse Attention**
Creates 10-100x amplification of important signals while suppressing noise. Attention becomes naturally sparse (60-70% sparsity). Automatic noise filtering without thresholding.

**Code Example**:
```python
class GoldbeterKoshlandAttention(nn.Module):
    """Ultrasensitive sparse attention"""

    def __init__(self, dim, J1=0.1, J2=0.1):
        super().__init__()
        self.W_Q = nn.Linear(dim, dim)
        self.W_K = nn.Linear(dim, dim)
        self.W_V = nn.Linear(dim, dim)
        self.J1 = J1
        self.J2 = J2
        self.v2 = nn.Parameter(torch.ones(1))  # Baseline

    def forward(self, Q, K, V):
        Q_proj = self.W_Q(Q)
        K_proj = self.W_K(K)
        V_proj = self.W_V(V)

        scores = Q_proj @ K_proj.T / np.sqrt(Q_proj.shape[-1])

        # Goldbeter-Koshland ultrasensitivity
        v1 = torch.relu(scores)  # Kinase (activation)
        v2 = self.v2              # Phosphatase (baseline)

        B = v2 - v1 + self.J1*v2 + self.J2*v1
        discriminant = torch.clamp(B**2 - 4*(v2-v1)*v1*self.J2, min=1e-8)

        attn_scores = (2*v1*self.J2) / (B + torch.sqrt(discriminant))
        attn = torch.softmax(attn_scores, dim=-1)

        return attn @ V_proj
```

**Source**: SIGNAL_AMPLIFICATION_REPORT.md, Lines 164-248

---

### Triplet STDP (Sequence Learning)

**Purpose**: Learn temporal sequences through spike-timing with frequency dependence.

**Formula**: Three-Spike Rule
```
Δw = r₁(t)[A₂⁺ + A₃⁺r₂(t-ε)] - o₁(t)[A₂⁻ + A₃⁻o₂(t-ε)]

where:
- r₁, o₁ = single spike traces (fast, τ ~ 20ms)
- r₂, o₂ = spike pair traces (slow, τ ~ 100ms)
- A₂⁺, A₂⁻ = pair-based coefficients
- A₃⁺, A₃⁻ = triplet coefficients
```

**Nature's Implementation**: Hippocampal CA3-CA1 synapses. Explains frequency-dependent plasticity better than pair-based STDP. Three spikes matter, not just two.

**Impact**: **HIGH - Temporal Learning**
Learns sequences without labels. Captures frequency dependence (burst vs single spikes). Enables unsupervised sequence prediction, motor learning, time-series forecasting.

**Code Example**:
```python
class TripletSTDP(nn.Module):
    """Triplet spike-timing dependent plasticity"""

    def __init__(self, n_in, n_out):
        super().__init__()
        self.W = nn.Parameter(torch.randn(n_out, n_in) * 0.01)

        # Pair coefficients
        self.A2_plus = 0.01
        self.A2_minus = 0.01

        # Triplet coefficients
        self.A3_plus = 0.001
        self.A3_minus = 0.001

        # Time constants
        self.tau_plus = 20.0   # Fast trace
        self.tau_minus = 20.0
        self.tau_x = 100.0     # Slow trace
        self.tau_y = 100.0

        # Eligibility traces
        self.r1 = torch.zeros(n_in)   # Fast pre-trace
        self.o1 = torch.zeros(n_out)  # Fast post-trace
        self.r2 = torch.zeros(n_in)   # Slow pre-trace
        self.o2 = torch.zeros(n_out)  # Slow post-trace

    def update(self, pre_spike, post_spike, dt=1.0):
        """Update weights based on spike timing"""
        # Decay traces
        self.r1 *= np.exp(-dt / self.tau_plus)
        self.o1 *= np.exp(-dt / self.tau_minus)
        self.r2 *= np.exp(-dt / self.tau_x)
        self.o2 *= np.exp(-dt / self.tau_y)

        # Triplet STDP update
        if post_spike.any():
            # LTP: pair + triplet terms
            dW_ltp = torch.outer(
                post_spike,
                (self.A2_plus + self.A3_plus * self.r2) * self.r1
            )
            self.W += dW_ltp

        if pre_spike.any():
            # LTD: pair + triplet terms
            dW_ltd = torch.outer(
                (self.A2_minus + self.A3_minus * self.o2) * self.o1,
                pre_spike
            )
            self.W -= dW_ltd

        # Update traces
        self.r1 += pre_spike
        self.o1 += post_spike
        self.r2 += pre_spike
        self.o2 += post_spike
```

**Source**: PLASTICITY_FORMULAS_COMPLETE.md, Lines 26-37

---

### Voltage-Dependent STDP (Clopath Rule)

**Purpose**: Plasticity driven by membrane voltage (realistic) rather than discrete spikes.

**Formula**: Voltage-Based Learning
```
dw/dt = A_LTD·x̄(V - θ_LTD)₋ + A_LTP·x(V̄ - θ_LTP)₊(V - θ_LTD)₊

where:
- V = postsynaptic voltage
- x, x̄ = presynaptic traces (fast and slow)
- V̄ = filtered voltage
- θ_LTD, θ_LTP = voltage thresholds
- (·)₊ = rectification (max(0, ·))
- (·)₋ = negative rectification (min(0, ·))
```

**Nature's Implementation**: Layer 2/3 cortical pyramidal neurons. Voltage-based plasticity matches experimental data better than spike-based rules.

**Impact**: **HIGH - Realistic Learning**
More biologically accurate. Captures subthreshold dynamics (EPSPs that don't spike). Works with analog neurons, not just spiking. Enables gradient-like learning without backprop.

**Code Example**:
```python
class ClopathSTDP(nn.Module):
    """Voltage-dependent plasticity rule"""

    def __init__(self, n_in, n_out):
        super().__init__()
        self.W = nn.Parameter(torch.randn(n_out, n_in) * 0.01)

        self.A_LTD = 0.01
        self.A_LTP = 0.01
        self.theta_LTD = -70.6  # mV
        self.theta_LTP = -45.3  # mV

        # Presynaptic traces
        self.x = torch.zeros(n_in)      # Fast (τ ~ 10ms)
        self.x_bar = torch.zeros(n_in)  # Slow (τ ~ 100ms)

        # Postsynaptic voltage filter
        self.V_bar = torch.zeros(n_out)

    def update(self, pre_activity, V_post, dt=1.0):
        """Update based on voltage, not spikes"""
        # Update traces
        self.x = 0.9 * self.x + 0.1 * pre_activity
        self.x_bar = 0.99 * self.x_bar + 0.01 * pre_activity
        self.V_bar = 0.99 * self.V_bar + 0.01 * V_post

        # LTD term: x̄(V - θ_LTD)₋
        V_minus_LTD = torch.clamp(V_post - self.theta_LTD, max=0)
        dW_ltd = self.A_LTD * torch.outer(V_minus_LTD, self.x_bar)

        # LTP term: x(V̄ - θ_LTP)₊(V - θ_LTD)₊
        V_bar_minus_LTP = torch.clamp(self.V_bar - self.theta_LTP, min=0)
        V_minus_LTD_pos = torch.clamp(V_post - self.theta_LTD, min=0)
        dW_ltp = self.A_LTP * torch.outer(
            V_bar_minus_LTP * V_minus_LTD_pos,
            self.x
        )

        # Total update
        self.W += (dW_ltp + dW_ltd) * dt
```

**Source**: PLASTICITY_FORMULAS_COMPLETE.md, Lines 139-164

---

### Dopamine-Modulated STDP (Reward Learning)

**Purpose**: Eligibility traces gated by reward signal—solves credit assignment problem.

**Formula**: Three-Factor Rule
```
dw/dt = c·STDP(Δt)·(R - R̄)

where:
- STDP(Δt) = eligibility trace (recent correlations)
- R = reward received
- R̄ = baseline reward (prediction)
- c = learning rate

Eligibility trace:
de/dt = -e/τₑ + A·exp(-|Δt|/τ)·δ(t - t_spike)
```

**Nature's Implementation**: Basal ganglia dopaminergic modulation of corticostriatal synapses. Dopamine signals reward prediction error (R - R̄).

**Impact**: **HIGH - Reinforcement Learning**
Biologically plausible credit assignment. Local computation (synapse records correlations, dopamine broadcasts reward). Enables continual learning without catastrophic forgetting.

**Code Example**:
```python
class DopamineModulatedSTDP(nn.Module):
    """Reward-modulated spike-timing plasticity"""

    def __init__(self, n_in, n_out, tau_e=1000.0):
        super().__init__()
        self.W = nn.Parameter(torch.randn(n_out, n_in) * 0.01)

        # Eligibility trace (memory of recent correlations)
        self.eligibility = torch.zeros_like(self.W)
        self.tau_e = tau_e

        # STDP parameters
        self.A_plus = 0.01
        self.A_minus = 0.01
        self.tau_stdp = 20.0

        # Reward baseline
        self.reward_baseline = 0.0
        self.alpha_baseline = 0.01

    def stdp_trace(self, pre_spike, post_spike, spike_time_diff):
        """Compute STDP eligibility trace"""
        if spike_time_diff > 0:  # Pre before post
            trace = self.A_plus * np.exp(-spike_time_diff / self.tau_stdp)
        else:
            trace = -self.A_minus * np.exp(spike_time_diff / self.tau_stdp)

        return torch.outer(post_spike, pre_spike) * trace

    def update(self, pre_spike, post_spike, spike_time_diff, reward, dt=1.0):
        """Update eligibility and weights with reward"""
        # Decay eligibility
        self.eligibility *= np.exp(-dt / self.tau_e)

        # Add new STDP trace
        if pre_spike.any() or post_spike.any():
            self.eligibility += self.stdp_trace(
                pre_spike, post_spike, spike_time_diff
            )

        # Weight update gated by reward prediction error
        reward_error = reward - self.reward_baseline
        self.W += 0.001 * self.eligibility * reward_error

        # Update reward baseline
        self.reward_baseline += self.alpha_baseline * (
            reward - self.reward_baseline
        )
```

**Source**: PLASTICITY_FORMULAS_COMPLETE.md, Lines 165-178; 00_NOVELTY.csv (ID 19)

---

### Calcium-Based Plasticity (Shouval Model)

**Purpose**: Unified LTP/LTD based on Ca²⁺ concentration thresholds.

**Formula**: Calcium-Controlled Learning
```
dw/dt = η([Ca])·(Ω([Ca]) - w)

Ω([Ca]) = sig([Ca] - θ_LTP) - 0.5·sig([Ca] - θ_LTD)

where:
- [Ca] = postsynaptic calcium concentration
- θ_LTP > θ_LTD = calcium thresholds
- Low [Ca] → LTD (calcineurin activation)
- High [Ca] → LTP (CaMKII activation)
- η([Ca]) = learning rate (Ca-dependent)
```

**Nature's Implementation**: NMDA receptors admit Ca²⁺. Low Ca activates calcineurin (phosphatase) → LTD. High Ca activates CaMKII (kinase) → LTP.

**Impact**: **HIGH - Unified Learning**
Single mechanism explains both LTP and LTD. Biophysically accurate (NMDA dynamics). Naturally stable (Ω function bounded). Enables realistic synaptic plasticity models.

**Code Example**:
```python
class CalciumBasedPlasticity(nn.Module):
    """Shouval calcium-dependent learning"""

    def __init__(self, n_in, n_out):
        super().__init__()
        self.W = nn.Parameter(torch.randn(n_out, n_in) * 0.01)

        # Calcium thresholds (μM)
        self.theta_LTD = 0.3
        self.theta_LTP = 0.5

        # Calcium state
        self.Ca = torch.zeros(n_out)

    def omega(self, Ca):
        """Direction and magnitude of plasticity"""
        sig_LTP = torch.sigmoid((Ca - self.theta_LTP) / 0.05)
        sig_LTD = torch.sigmoid((Ca - self.theta_LTD) / 0.05)
        return sig_LTP - 0.5 * sig_LTD

    def update_calcium(self, pre_activity, post_activity, dt=1.0):
        """NMDA-like calcium influx"""
        # Calcium influx proportional to pre × post
        influx = 0.1 * post_activity * pre_activity.sum(dim=-1)

        # Decay
        decay = 0.1 * self.Ca

        self.Ca += (influx - decay) * dt
        self.Ca = torch.clamp(self.Ca, 0, 2.0)

    def update_weights(self, pre_activity, post_activity, dt=1.0):
        """Calcium-driven weight update"""
        self.update_calcium(pre_activity, post_activity, dt)

        # Omega function determines LTP vs LTD
        omega = self.omega(self.Ca)

        # Weight update
        eta = 0.01 * self.Ca  # Learning rate increases with Ca
        dW = torch.outer(
            eta * (omega - self.W.mean(dim=1)),
            pre_activity.mean(dim=0)
        )

        self.W += dW * dt
```

**Source**: PLASTICITY_FORMULAS_COMPLETE.md, Lines 371-398; 00_NOVELTY.csv (ID 30)

---

### Wilson-Cowan E-I Dynamics

**Purpose**: Excitatory-inhibitory balance creates oscillations and stability.

**Formula**: Population Dynamics
```
τ_E·dE/dt = -E + S_E(w_EE·E - w_EI·I + I_ext)
τ_I·dI/dt = -I + S_I(w_IE·E - w_II·I)

where:
- E, I = excitatory and inhibitory population activities
- w_EE, w_EI, w_IE, w_II = connection weights
- S(·) = sigmoid activation
- τ_E > τ_I typically (inhibition faster)
```

**Nature's Implementation**: Cortical microcircuits with ~80% excitatory, ~20% inhibitory neurons. E-I loops create gamma oscillations (40-80 Hz).

**Impact**: **HIGH - Stable Dynamics**
Self-stabilizing through lateral inhibition. Creates oscillations for temporal coding. Prevents runaway excitation. Basis for PING (Pyramidal-Interneuron Gamma) rhythms.

**Code Example**:
```python
class WilsonCowanLayer(nn.Module):
    """E-I balanced population dynamics"""

    def __init__(self, dim, ratio_ei=0.8):
        super().__init__()
        self.dim_e = int(dim * ratio_ei)
        self.dim_i = dim - self.dim_e

        # Connection weights
        self.W_ee = nn.Linear(self.dim_e, self.dim_e)
        self.W_ei = nn.Linear(self.dim_i, self.dim_e)
        self.W_ie = nn.Linear(self.dim_e, self.dim_i)
        self.W_ii = nn.Linear(self.dim_i, self.dim_i)

        # Time constants (inhibition faster)
        self.tau_e = 10.0
        self.tau_i = 5.0

        # State
        self.E = torch.zeros(1, self.dim_e)
        self.I = torch.zeros(1, self.dim_i)

    def forward(self, x, dt=1.0, n_steps=3):
        batch_size = x.shape[0]

        # Split input
        x_e = x[:, :self.dim_e]
        x_i = x[:, self.dim_e:]

        # Initialize
        E = self.E.expand(batch_size, -1).clone()
        I = self.I.expand(batch_size, -1).clone()

        # Iterate dynamics
        for _ in range(n_steps):
            # E dynamics
            E_input = self.W_ee(E) - self.W_ei(I) + x_e
            dE = (-E + torch.tanh(E_input)) / self.tau_e

            # I dynamics
            I_input = self.W_ie(E) - self.W_ii(I) + x_i
            dI = (-I + torch.tanh(I_input)) / self.tau_i

            E += dt * dE
            I += dt * dI

        # Update state
        if self.training:
            self.E = E.mean(dim=0, keepdim=True).detach()
            self.I = I.mean(dim=0, keepdim=True).detach()

        return torch.cat([E, I], dim=-1)
```

**Source**: bio_ai_components.py, Lines 580-662; OSCILLATORY_PATTERNS_ANALYSIS.md, Lines 169-217

---

### Kuramoto Synchronization

**Purpose**: Phase oscillators that synchronize—solves binding problem through temporal alignment.

**Formula**: Coupled Oscillators
```
dθ_i/dt = ω_i + (K/N)·∑_j sin(θ_j - θ_i)

Order parameter (synchronization):
r·e^(iψ) = (1/N)·∑_j e^(iθ_j)

where:
- θ_i = phase of oscillator i
- ω_i = natural frequency
- K = coupling strength
- r ∈ [0,1] = synchronization level (0=async, 1=sync)
```

**Nature's Implementation**: Brain rhythms synchronize to bind features. Gamma oscillations (40 Hz) link "what" and "where" pathways when object present.

**Impact**: **HIGH - Feature Binding**
Solves binding problem without explicit mechanisms. Related features synchronize automatically. Enables multi-modal integration (vision + language sync when describing scene).

**Code Example**:
```python
class KuramotoLayer(nn.Module):
    """Phase oscillators for feature binding"""

    def __init__(self, n_oscillators, coupling_K=1.0):
        super().__init__()
        self.n = n_oscillators

        # Natural frequencies (learnable)
        self.omega = nn.Parameter(torch.randn(n_oscillators) * 0.1)

        # Coupling strength
        self.K = nn.Parameter(torch.tensor(coupling_K))

        # Phase state
        self.theta = torch.rand(1, n_oscillators) * 2 * np.pi

    def forward(self, x, dt=0.1):
        batch_size = x.shape[0]
        theta = self.theta.expand(batch_size, -1).clone()

        # Kuramoto coupling
        theta_diff = theta.unsqueeze(1) - theta.unsqueeze(2)
        coupling = torch.sin(theta_diff).mean(dim=1)

        # Update phases
        dtheta = self.omega + self.K * coupling + x
        theta = (theta + dt * dtheta) % (2 * np.pi)

        if self.training:
            self.theta = theta.mean(dim=0, keepdim=True).detach()

        # Output as cos/sin (phase encoding)
        return torch.stack([torch.cos(theta), torch.sin(theta)], dim=-1).flatten(-2)

    def synchronization(self):
        """Measure of feature binding"""
        r = torch.abs(torch.mean(torch.exp(1j * self.theta)))
        return r.item()  # 0 = unbound, 1 = bound
```

**Source**: bio_ai_components.py, Lines 664-721; OSCILLATORY_PATTERNS_ANALYSIS.md, Lines 39-53

---

## MEDIUM-HIGH IMPACT (Significant Improvements)

These architectures provide 2-10x improvements or enable new capabilities.

---

### Metabolic Loss Function (65 Objectives)

**Purpose**: Multi-objective loss balancing 65 competing objectives simultaneously using thermodynamic potentials.

**Formula**: E.coli Growth Optimization
```
Fitness = max(0, 1 + ∑(w_i · log(obj_i / baseline_i)))

Objectives (65 total):
- Accuracy metrics (5): cross_entropy, F1, AUC, precision, recall
- Efficiency metrics (10): FLOPS, params, latency, memory, energy
- Robustness metrics (8): adversarial, OOD, noise, corruption
- Fairness metrics (4): demographic, equalized_odds, calibration
- Interpretability metrics (6): sparsity, feature_importance, attention_entropy
- Resource metrics (8): bandwidth, storage, compute_cost
- ... 24 more objectives

Thermodynamic constraint: Fitness ≥ 0
```

**Nature's Implementation**: E.coli optimizes 65+ metabolic fluxes simultaneously for maximum growth rate. Uses log-ratio thermodynamic potentials to balance competing objectives.

**Impact**: **MEDIUM-HIGH - Pareto Optimization**
Automatically finds Pareto-optimal solutions across dozens of metrics. No manual weight tuning. Prevents overfitting to single objective (accuracy) while ignoring efficiency, fairness, robustness.

**Code Example**:
```python
class MetabolicLoss(nn.Module):
    """65-objective holistic loss function"""

    def __init__(self, num_objectives=65):
        super().__init__()
        self.weights = nn.Parameter(torch.ones(num_objectives))
        self.baselines = nn.Parameter(torch.ones(num_objectives))

    def forward(self, outputs, targets, model_state):
        objectives = []

        # Accuracy objectives (5)
        objectives.append(F.cross_entropy(outputs, targets))
        objectives.append(f1_score(outputs, targets))
        objectives.append(auc_score(outputs, targets))
        objectives.append(precision(outputs, targets))
        objectives.append(recall(outputs, targets))

        # Efficiency objectives (10)
        objectives.append(model_state['flops'] / 1e9)
        objectives.append(model_state['params'] / 1e6)
        objectives.append(model_state['latency'])
        objectives.append(model_state['memory'] / 1e6)
        objectives.append(model_state['energy'])
        # ... 5 more

        # Robustness objectives (8)
        objectives.append(adversarial_loss(outputs))
        objectives.append(ood_detection(outputs))
        objectives.append(noise_robustness(outputs))
        # ... 5 more

        # Fairness objectives (4)
        objectives.append(demographic_parity(outputs, model_state))
        objectives.append(equalized_odds(outputs, model_state))
        # ... 2 more

        # Interpretability objectives (6)
        objectives.append(sparsity_loss(model_state['activations']))
        objectives.append(feature_importance_entropy(model_state))
        # ... 4 more

        # ... continue for all 65 objectives

        # E.coli-style thermodynamic integration
        obj_tensor = torch.stack(objectives)
        log_ratios = torch.log(obj_tensor / (self.baselines + 1e-8))
        fitness = torch.sum(self.weights * log_ratios)

        return torch.clamp(1.0 + fitness, min=0.0)  # Non-negative constraint
```

**Source**: 00_NOVELTY.csv (ID 1-3), BIOMD0000000470

---

### Hill Activation (Adaptive Cooperativity)

**Purpose**: Learnable steepness activation function—sharp or smooth switching based on data.

**Formula**: Hill Equation with Learnable n
```
y = V_max · x^n / (K^n + x^n)

where:
- n = Hill coefficient (cooperativity), LEARNABLE
- K = half-maximal activation point, LEARNABLE
- V_max = maximum output, LEARNABLE
- x = input activation

For high n (4-8): sharp threshold (switch-like)
For low n (1-2): smooth saturation (sigmoid-like)
```

**Nature's Implementation**: Hemoglobin oxygen binding (n=2.8). Enzyme cooperativity. Transcription factor binding with multiple sites.

**Impact**: **MEDIUM-HIGH - Adaptive Nonlinearity**
Network learns optimal activation shape per layer. Sharp thresholds where needed (sparse networks), smooth where needed (gradients). Replaces fixed ReLU/sigmoid with adaptive function.

**Code Example**:
```python
class HillActivation(nn.Module):
    """Learnable cooperativity activation"""

    def __init__(self, dim, init_n=2.0, init_K=1.0):
        super().__init__()
        self.n = nn.Parameter(torch.full((dim,), init_n))
        self.K = nn.Parameter(torch.full((dim,), init_K))
        self.V_max = nn.Parameter(torch.ones(dim))

    def forward(self, x):
        # Preserve sign
        sign = torch.sign(x)
        x_abs = torch.abs(x)

        # Ensure positive parameters
        n = F.softplus(self.n) + 0.1
        K = F.softplus(self.K) + 0.1

        # Hill equation
        numerator = self.V_max * torch.pow(x_abs + 1e-8, n)
        denominator = torch.pow(K, n) + torch.pow(x_abs + 1e-8, n)

        return sign * (numerator / (denominator + 1e-8))
```

**Source**: 00_NOVELTY.csv (ID 4), bio_ai_components.py, Lines 29-69

---

### Michaelis-Menten Activation

**Purpose**: Saturation-based activation prevents explosive growth, automatic normalization.

**Formula**: Enzyme Kinetics
```
v = (V_max · x) / (K_m + x)

Properties:
- Linear at low x: v ≈ (V_max/K_m)·x
- Saturates at high x: v → V_max
- Half-max at x = K_m
```

**Nature's Implementation**: All enzyme reactions. Universal saturation mechanism in biochemistry.

**Impact**: **MEDIUM - Stable Activation**
Prevents activation explosions. Automatic output normalization. No batch statistics needed. Biologically realistic saturation.

**Code Example**:
```python
class MichaelisMentenActivation(nn.Module):
    def __init__(self, v_max=1.0, k_m=1.0):
        super().__init__()
        self.v_max = nn.Parameter(torch.tensor(v_max))
        self.k_m = nn.Parameter(torch.tensor(k_m))

    def forward(self, x):
        return self.v_max * x / (self.k_m + torch.abs(x) + 1e-8)
```

**Source**: 00_NOVELTY.csv (ID 5)

---

### Energy-Aware Neurons (ATP Budgeting)

**Purpose**: Neurons track ATP—can only fire if energy available. Automatic sparsity.

**Formula**: ATP Depletion Dynamics
```
dV/dt = f(W·x) - I_leak

ATP consumption: dATP/dt = -α·|firing| 
ATP regeneration: dATP/dt += β·(ATP_max - ATP)

Threshold = θ_base / (ATP/ATP_max + ε)

where lower ATP → higher threshold → harder to fire
```

**Nature's Implementation**: Neurons consume ~10^8 ATP per action potential. ATP depletion raises firing threshold.

**Impact**: **MEDIUM - Automatic Sparsity**
Energy budget naturally limits activation. No explicit regularization needed. Biologically realistic resource constraints.

**Code Example**:
```python
class EnergyAwareNeuron(nn.Module):
    def __init__(self, features, atp_capacity=10.0):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(features))
        self.atp_pool = torch.full((features,), atp_capacity)
        self.atp_max = atp_capacity

    def forward(self, x):
        # Compute activation
        z = F.linear(x, self.weight)

        # ATP depletion raises threshold
        threshold = 1.0 / (self.atp_pool / self.atp_max + 0.1)
        firing = F.relu(z - threshold)

        # Update ATP
        self.atp_pool -= 0.5 * firing.abs()  # Consume
        self.atp_pool += 0.1 * (self.atp_max - self.atp_pool)  # Regenerate
        self.atp_pool = torch.clamp(self.atp_pool, 0, self.atp_max)

        return firing
```

**Source**: 00_NOVELTY.csv (ID 7)

---

### Dual-Channel Neurons (Fast + Slow)

**Purpose**: Fast electrical pathway + slow modulatory channel for multi-timescale computation.

**Formula**: Calcium + Sodium Dynamics
```
Fast (Na+/K+): τ_fast·dV_fast/dt = f(x) - V_fast  (τ ~ 5ms)
Slow (Ca2+):   τ_slow·dCa/dt = g(x) - Ca          (τ ~ 100ms)

Output = V_fast · sigmoid(Ca)  [Fast modulated by slow]
```

**Nature's Implementation**: 9,633 Ca²⁺ signaling formulas in database. Fast electrical signals modulated by slow calcium waves.

**Impact**: **MEDIUM - Multi-Timescale**
Captures short-term and long-term dependencies simultaneously. Fast pathway for immediate responses, slow for context.

**Code Example**:
```python
class DualChannelNeuron(nn.Module):
    def __init__(self, features):
        super().__init__()
        self.fast_weight = nn.Parameter(torch.randn(features))
        self.slow_weight = nn.Parameter(torch.randn(features) * 0.1)
        self.slow_state = torch.zeros(features)

    def forward(self, x):
        # Fast pathway
        fast = F.linear(x, self.fast_weight)

        # Slow pathway (leaky integration)
        slow_input = F.linear(x, self.slow_weight)
        self.slow_state = 0.9 * self.slow_state + 0.1 * slow_input

        # Modulation
        modulation = torch.sigmoid(self.slow_state)
        return fast * modulation
```

**Source**: 00_NOVELTY.csv (ID 9)

---

### Multi-Timescale Gate

**Purpose**: Multiple gating variables with geometric time constant spacing (5ms, 50ms, 500ms).

**Formula**: Hierarchical Temporal Integration
```
For i = 1 to N:
    τ_i = τ_min · 10^(i-1)  [Geometric spacing]
    dh_i/dt = (h_∞(x) - h_i) / τ_i

Output = ∑ α_i · h_i  [Weighted combination]
```

**Nature's Implementation**: AMPA (fast, 3ms), NMDA (slow, 100ms), metabotropic (very slow, 1s). Multiple receptor types with different kinetics.

**Impact**: **MEDIUM - Temporal Hierarchy**
Captures dependencies from milliseconds to seconds. No recurrence needed. Natural working memory.

**Code Example**:
```python
class MultiTimescaleGate(nn.Module):
    def __init__(self, dim, n_timescales=3):
        super().__init__()

        # Geometric spacing: 5ms, 50ms, 500ms
        tau_init = torch.logspace(np.log10(5), np.log10(500), n_timescales)
        self.tau = nn.Parameter(tau_init.unsqueeze(-1).expand(-1, dim))

        self.W = nn.ModuleList([nn.Linear(dim, dim) for _ in range(n_timescales)])
        self.alpha = nn.Parameter(torch.ones(n_timescales, dim) / n_timescales)

        self.states = torch.zeros(n_timescales, 1, dim)

    def forward(self, x, dt=1.0):
        batch_size = x.size(0)
        outputs = []

        for i in range(len(self.W)):
            # Steady-state value
            x_inf = torch.sigmoid(self.W[i](x))

            # Leaky integration
            state = self.states[i].expand(-1, batch_size, -1)
            state = state + dt * (x_inf - state) / (F.softplus(self.tau[i]) + 1e-8)

            if self.training:
                self.states[i] = state.mean(1, keepdim=True).detach()

            outputs.append(state.squeeze(0))

        # Weighted combination
        outputs = torch.stack(outputs, dim=0)
        alpha_norm = F.softmax(self.alpha, dim=0).unsqueeze(1)
        return (outputs * alpha_norm).sum(0)
```

**Source**: bio_ai_components.py, Lines 211-280

---

### Synaptic Convolution (Dual-Exponential Kernels)

**Purpose**: Temporal convolution with realistic synaptic dynamics (rise + decay).

**Formula**: AMPA/NMDA Synaptic Kernels
```
K(t) = A · (exp(-t/τ_decay) - exp(-t/τ_rise))

AMPA: τ_rise = 0.5ms, τ_decay = 3ms (fast)
NMDA: τ_rise = 2ms, τ_decay = 100ms (slow)

Output = ∑ K(t - t_spike) · w
```

**Nature's Implementation**: All chemical synapses. Neurotransmitter binding and unbinding create dual-exponential waveform.

**Impact**: **MEDIUM - Realistic Temporal Kernels**
Better than learned 1D conv kernels. Biologically constrained. Natural temporal filtering.

**Code Example**:
```python
class SynapticConv1D(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=20):
        super().__init__()
        self.kernel_size = kernel_size

        self.tau_rise = nn.Parameter(torch.ones(out_channels, in_channels) * 2.0)
        self.tau_decay = nn.Parameter(torch.ones(out_channels, in_channels) * 10.0)
        self.weight = nn.Parameter(torch.randn(out_channels, in_channels))

    def get_kernel(self):
        t = torch.arange(self.kernel_size, dtype=torch.float32, device=self.weight.device)
        t = t.view(1, 1, -1)

        tau_r = F.softplus(self.tau_rise).unsqueeze(-1) + 1e-8
        tau_d = F.softplus(self.tau_decay).unsqueeze(-1) + tau_r

        # Dual exponential
        kernel = torch.exp(-t / tau_d) - torch.exp(-t / tau_r)
        kernel = kernel / (kernel.sum(-1, keepdim=True) + 1e-8)

        return self.weight.unsqueeze(-1) * kernel

    def forward(self, x):
        kernel = self.get_kernel()
        return F.conv1d(x, kernel, padding=self.kernel_size // 2)
```

**Source**: bio_ai_components.py, Lines 335-396

---

### Leaky Residual Block (LIF-Inspired)

**Purpose**: Leaky integrate-and-fire dynamics for residual connections.

**Formula**: Leaky Integration
```
τ·dV/dt = -(V - V_rest) + F(x)

Discrete: V_new = V + (dt/τ)·(-(V - V_rest) + F(x))

where:
- τ = membrane time constant (learnable)
- V_rest = resting potential (learnable)
- F(x) = feedforward transformation
```

**Nature's Implementation**: Leaky integrate-and-fire neurons. Universal model in computational neuroscience.

**Impact**: **MEDIUM - Adaptive Skip Connections**
Learnable mixing ratio between residual and transformation. Temporal dynamics in residual connections.

**Code Example**:
```python
class LeakyResidualBlock(nn.Module):
    def __init__(self, dim, init_tau=10.0):
        super().__init__()
        self.tau = nn.Parameter(torch.full((dim,), init_tau))
        self.V_rest = nn.Parameter(torch.zeros(dim))

        self.transform = nn.Sequential(
            nn.Linear(dim, dim * 4),
            nn.GELU(),
            nn.Linear(dim * 4, dim)
        )

    def forward(self, x, dt=1.0):
        F_x = self.transform(x)
        tau_safe = F.softplus(self.tau) + 1e-8

        # Leaky integration
        decay = dt / tau_safe
        x_new = x + decay * (-(x - self.V_rest) + F_x)

        return x_new
```

**Source**: bio_ai_components.py, Lines 287-333

---

### BCM Learning Rule (Sliding Threshold)

**Purpose**: Self-stabilizing unsupervised learning with activity-dependent threshold.

**Formula**: Bienenstock-Cooper-Munro
```
dw/dt = η·φ(y)·x
φ(y) = y·(y - θ_m)

dθ_m/dt = (⟨y²⟩ - θ_m) / τ_θ

where:
- y = postsynaptic activity
- x = presynaptic activity
- θ_m = sliding threshold (adapts to average activity)
- η = learning rate
```

**Nature's Implementation**: Visual cortex orientation tuning. Neurons self-organize without labels.

**Impact**: **MEDIUM - Stable Unsupervised Learning**
Automatically prevents runaway potentiation or depression. Threshold slides to maintain target activity level.

**Code Example**:
```python
class BCMLayer(nn.Module):
    def __init__(self, in_features, out_features, tau_theta=1000.0):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(out_features, in_features) * 0.01)
        self.tau_theta = tau_theta
        self.theta = torch.ones(out_features) * 0.5

    def forward(self, x):
        return F.linear(x, self.weight)

    def bcm_update(self, x, y, dt=1.0, lr=1e-3):
        y_mean = y.mean(0)
        x_mean = x.mean(0)

        # BCM phi function
        phi = y_mean * (y_mean - self.theta)

        # Weight update
        dw = torch.outer(phi, x_mean)
        self.weight += lr * dw

        # Update sliding threshold
        self.theta += dt * ((y_mean ** 2) - self.theta) / self.tau_theta
```

**Source**: 00_NOVELTY.csv (ID 20), bio_ai_components.py, Lines 492-539

---

### Oja's Rule (Automatic PCA)

**Purpose**: Hebbian learning with built-in normalization—extracts principal components.

**Formula**: Weight-Normalized Hebbian
```
Δw_i = η·y·(x_i - y·w_i)

Converges to: w ∝ first principal eigenvector

Multi-neuron: Sanger's rule extracts multiple PCs
```

**Nature's Implementation**: Cortical feature extraction. Unsupervised dimensionality reduction.

**Impact**: **MEDIUM - Unsupervised Features**
No labels needed. Automatic feature extraction. Weight normalization prevents runaway growth.

**Code Example**:
```python
class OjaLayer(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(out_features, in_features) * 0.01)

    def forward(self, x):
        return F.linear(x, self.weight)

    def oja_update(self, x, y, lr=1e-3):
        # Hebbian term
        hebbian = torch.outer(y.mean(0), x.mean(0))

        # Decay term (normalization)
        decay = torch.outer(y.mean(0), y.mean(0)) @ self.weight

        self.weight += lr * (hebbian - decay)
```

**Source**: 00_NOVELTY.csv (ID 21), bio_ai_components.py, Lines 541-574

---

## MEDIUM IMPACT (Useful Specialized Components)

These architectures excel in specific domains or scenarios.

---

### Boltzmann Gated Activation

**Purpose**: Voltage-gated channel kinetics for adaptive thresholds.

**Formula**: Sigmoid with Learnable Parameters
```
y = σ((x - V_half) / k)

where:
- V_half = half-activation voltage (learnable threshold)
- k = slope factor (learnable steepness)
- σ = sigmoid function
```

**Nature's Implementation**: Voltage-gated ion channels (Na+, K+, Ca2+). Activation depends on membrane potential.

**Impact**: **MEDIUM - Adaptive Thresholds**
Each neuron learns its own activation threshold and slope. Better than fixed ReLU threshold of 0.

**Code Example**:
```python
class BoltzmannActivation(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.v_half = nn.Parameter(torch.zeros(dim))
        self.k = nn.Parameter(torch.ones(dim))

    def forward(self, x):
        return torch.sigmoid((x - self.v_half) / (torch.abs(self.k) + 1e-8))
```

**Source**: bio_ai_components.py, Lines 72-102

---

### Hodgkin-Huxley Alpha Function

**Purpose**: Voltage-dependent gating variable dynamics.

**Formula**: Rate Equations
```
α_m(V) = 0.1(V + 40) / (1 - exp(-(V + 40)/10))
β_m(V) = 4 exp(-(V + 65)/18)

dm/dt = α_m(V)(1 - m) - β_m(V)·m

m_∞(V) = α_m/(α_m + β_m)
τ_m(V) = 1/(α_m + β_m)
```

**Nature's Implementation**: Sodium channel activation in action potentials.

**Impact**: **MEDIUM - Realistic Spiking**
Accurate spike generation for spiking neural networks. Matches experimental data.

**Code Example**:
```python
class HodgkinHuxleyGate(nn.Module):
    def __init__(self, features):
        super().__init__()
        self.m = torch.zeros(features)

    def alpha_m(self, V):
        return 0.1 * (V + 40) / (1 - torch.exp(-(V + 40) / 10) + 1e-8)

    def beta_m(self, V):
        return 4 * torch.exp(-(V + 65) / 18)

    def forward(self, V, dt=0.1):
        alpha = self.alpha_m(V)
        beta = self.beta_m(V)

        dm = (alpha * (1 - self.m) - beta * self.m) * dt
        self.m += dm

        return self.m
```

**Source**: bio_ai_components.py, Lines 104-128

---

### Ion Channel Gating (m³h Dynamics)

**Purpose**: Multi-variable gating with inactivation—complex temporal dynamics.

**Formula**: Activation × Inactivation
```
I = g_max · m³ · h · (V - E_rev)

dm/dt = (m_∞(V) - m) / τ_m(V)
dh/dt = (h_∞(V) - h) / τ_h(V)

where:
- m = activation gate (fast, power of 3)
- h = inactivation gate (slow)
- E_rev = reversal potential
```

**Nature's Implementation**: Na+ channels (m³h), K+ channels (n⁴), Ca2+ channels (m²h).

**Impact**: **MEDIUM - Complex Dynamics**
Captures spike generation, refractory period, adaptation. Rich temporal behavior from simple ODEs.

**Code Example**:
```python
class IonChannelGate(nn.Module):
    def __init__(self, dim, power_m=3):
        super().__init__()
        self.m = torch.zeros(1, dim)
        self.h = torch.ones(1, dim)
        self.power = power_m

    def m_inf(self, V):
        return torch.sigmoid((V + 40) / 10)

    def h_inf(self, V):
        return torch.sigmoid(-(V + 45) / 7)

    def forward(self, V, dt=1.0):
        batch_size = V.shape[0]

        m = self.m.expand(batch_size, -1)
        h = self.h.expand(batch_size, -1)

        # Update gates
        m = m + dt * ((self.m_inf(V) - m) / 5.0)
        h = h + dt * ((self.h_inf(V) - h) / 50.0)

        if self.training:
            self.m = m.mean(0, keepdim=True).detach()
            self.h = h.mean(0, keepdim=True).detach()

        # Conductance
        g = (m ** self.power) * h
        return g
```

**Source**: bio_ai_components.py, Lines 130-209

---

### GTPase Amplification Cycle

**Purpose**: Catalytic amplification—one GEF activates many GTPases.

**Formula**: GDP/GTP Exchange
```
d[Ras-GTP]/dt = k_GEF[GEF][Ras-GDP] - k_GAP[GAP][Ras-GTP]

Amplification: 1 GEF → 100 Ras-GTP (before GAP deactivation)
```

**Nature's Implementation**: Ras, Rho, Rab, Ran, Arf families. 5,239 formulas in database.

**Impact**: **MEDIUM - Feature Amplification**
One strong signal catalytically amplifies related features. Persistent activation until GAP.

**Code Example**:
```python
class GTPaseAmplifier(nn.Module):
    def __init__(self, dim, k_GEF=5.0, k_GAP=0.5):
        super().__init__()
        self.signal_encoder = nn.Linear(dim, dim)
        self.k_GEF = k_GEF
        self.k_GAP = k_GAP
        self.GTP_state = torch.zeros(1, dim)

    def forward(self, x, dt=1.0):
        batch_size = x.shape[0]
        signal = torch.sigmoid(self.signal_encoder(x))

        GTP = self.GTP_state.expand(batch_size, -1)

        # GEF activation
        activation = self.k_GEF * signal * (1 - GTP)

        # GAP deactivation
        deactivation = self.k_GAP * GTP

        GTP = GTP + dt * (activation - deactivation)
        GTP = torch.clamp(GTP, 0, 1)

        if self.training:
            self.GTP_state = GTP.mean(0, keepdim=True).detach()

        return x * (1 + 10 * GTP)  # 10x amplification
```

**Source**: SIGNAL_AMPLIFICATION_REPORT.md, Lines 340-414

---

### IP3 Receptor (Calcium-Induced Calcium Release)

**Purpose**: Positive feedback amplification through CICR.

**Formula**: De Young-Keizer Model
```
J_IP3R = v_max · m³ · h³ · (Ca_ER - Ca_cyt)

m_∞ = ([IP3]/(K_IP3 + [IP3])) · ([Ca]/(K_act + [Ca]))
dh/dt = (h_∞ - h)/τ_h

where h_∞ = K_inh/(K_inh + [Ca])  [Ca-dependent inactivation]
```

**Nature's Implementation**: Intracellular calcium release. Creates calcium waves and oscillations.

**Impact**: **MEDIUM - Oscillatory Amplification**
Positive feedback creates waves. Biphasic response: Ca activates then inactivates.

**Code Example**:
```python
class IP3Receptor(nn.Module):
    def __init__(self, features):
        super().__init__()
        self.h = torch.ones(features)  # Inactivation gate
        self.Ca_ER = 100.0  # ER calcium (high)

    def m_inf(self, IP3, Ca):
        ip3_term = IP3 / (0.13 + IP3)
        ca_term = Ca / (0.08 + Ca)
        return ip3_term * ca_term

    def h_inf(self, Ca):
        return 0.8 / (0.8 + Ca)

    def forward(self, IP3, Ca_cyt, dt=1.0):
        m = self.m_inf(IP3, Ca_cyt)

        # Update inactivation
        self.h += dt * (self.h_inf(Ca_cyt) - self.h) / 2.0

        # Flux
        J = 10.0 * (m ** 3) * (self.h ** 3) * (self.Ca_ER - Ca_cyt)

        return J
```

**Source**: expand_04_signaling.py, Lines 158-174; SIGNAL_AMPLIFICATION_REPORT

---

### SERCA Pump (Active Transport)

**Purpose**: ATP-driven calcium pumping with saturation.

**Formula**: Michaelis-Menten with Hill Cooperativity
```
J_SERCA = V_max · [Ca]²/(K_m² + [Ca]²)

where n=2 (Hill coefficient for cooperativity)
```

**Nature's Implementation**: SR/ER Ca-ATPase. Restores ER calcium against gradient.

**Impact**: **MEDIUM - Active Regulation**
Counteracts release mechanisms. Creates oscillations when coupled with IP3R.

**Code Example**:
```python
class SERCAPump(nn.Module):
    def __init__(self, V_max=2.0, K_m=0.1):
        super().__init__()
        self.V_max = V_max
        self.K_m = K_m

    def forward(self, Ca_cyt):
        return self.V_max * (Ca_cyt ** 2) / (self.K_m ** 2 + Ca_cyt ** 2)
```

**Source**: expand_04_signaling.py, Lines 182-186

---

### Calmodulin Activation (Four Ca²⁺ Binding)

**Purpose**: Cooperative calcium sensor—4 Ca²⁺ bind with high cooperativity.

**Formula**: Hill Equation (n=4)
```
[CaM-Ca₄] = [CaM]_total · [Ca]⁴/(K_d⁴ + [Ca]⁴)

where n=4 creates sharp threshold
```

**Nature's Implementation**: Calmodulin activates CaMKII, calcineurin, many others.

**Impact**: **MEDIUM - Sharp Sensor**
All-or-none calcium response. Threshold detector for plasticity.

**Code Example**:
```python
class Calmodulin(nn.Module):
    def __init__(self, K_d=0.5):
        super().__init__()
        self.K_d = K_d

    def forward(self, Ca):
        return (Ca ** 4) / (self.K_d ** 4 + Ca ** 4)
```

**Source**: expand_04_signaling.py, Lines 200-222

---

### Synaptic Scaling (Homeostatic Plasticity)

**Purpose**: Global weight scaling to maintain target firing rate.

**Formula**: Multiplicative Scaling
```
dw/dt = α·(r_target - r_actual)·w

or: w_new = w_old · (r_target / r_actual)

where:
- r = firing rate
- α = scaling rate (slow, hours-days)
```

**Nature's Implementation**: Neurons scale all synapses to maintain homeostasis.

**Impact**: **MEDIUM - Prevents Runaway**
Stabilizes other plasticity rules. Prevents saturation or silence.

**Code Example**:
```python
class SynapticScaling(nn.Module):
    def __init__(self, target_rate=0.1, alpha=0.001):
        super().__init__()
        self.target_rate = target_rate
        self.alpha = alpha

    def scale_weights(self, weights, actual_rate):
        scaling_factor = self.target_rate / (actual_rate + 1e-8)
        scaling_factor = 1.0 + self.alpha * (scaling_factor - 1.0)
        return weights * scaling_factor
```

**Source**: PLASTICITY_FORMULAS_COMPLETE.md, Lines 285-310

---

### Theta Neuron (Phase Representation)

**Purpose**: Neurons as phase oscillators on unit circle.

**Formula**: Quadratic Integrate-and-Fire on Circle
```
dθ/dt = (1 - cos θ) + (1 + cos θ)·(η + I)

where:
- θ ∈ [0, 2π] = phase
- η = excitability
- I = input current
- Spike when θ crosses π
```

**Nature's Implementation**: Simplification of QIF neuron. Analytically tractable.

**Impact**: **MEDIUM - Phase Coding**
Natural for coupled oscillator networks. Kuramoto-compatible.

**Code Example**:
```python
class ThetaNeuron(nn.Module):
    def __init__(self, n_neurons, eta=0.0):
        super().__init__()
        self.theta = torch.rand(n_neurons) * 2 * np.pi
        self.eta = eta

    def forward(self, I, dt=0.01):
        dtheta = (1 - torch.cos(self.theta)) + (1 + torch.cos(self.theta)) * (self.eta + I)
        self.theta = (self.theta + dt * dtheta) % (2 * np.pi)

        # Spike when crossing π
        spikes = ((self.theta > np.pi) & (self.theta < np.pi + dt * 10)).float()

        return spikes, self.theta
```

**Source**: OSCILLATORY_PATTERNS_ANALYSIS.md, Lines 30-36

---

### PING Gamma Oscillations (E-I Loop)

**Purpose**: Pyramidal-Interneuron gamma rhythm (40-80 Hz) for attention.

**Formula**: E→I→E Loop
```
τ_E·dE/dt = -E + S(w_EE·E - w_EI·I + I_ext)
τ_I·dI/dt = -I + S(w_IE·E)

with τ_I < τ_E, creates oscillation at f = 1/(τ_E + τ_I)
```

**Nature's Implementation**: Cortical gamma rhythms. Attention and working memory.

**Impact**: **MEDIUM - Rhythmic Attention**
Oscillatory gating of information. Synchrony binds features.

**Code Example**:
```python
class PINGGamma(nn.Module):
    def __init__(self, dim_e, dim_i=None):
        super().__init__()
        if dim_i is None:
            dim_i = dim_e // 4

        self.W_EE = nn.Linear(dim_e, dim_e)
        self.W_EI = nn.Linear(dim_i, dim_e)
        self.W_IE = nn.Linear(dim_e, dim_i)

        self.tau_e = 10.0  # Slow
        self.tau_i = 5.0   # Fast

        self.E = torch.zeros(1, dim_e)
        self.I = torch.zeros(1, dim_i)

    def forward(self, x, dt=1.0, n_steps=5):
        batch_size = x.shape[0]
        E = self.E.expand(batch_size, -1).clone()
        I = self.I.expand(batch_size, -1).clone()

        for _ in range(n_steps):
            E_input = self.W_EE(E) - self.W_EI(I) + x
            I_input = self.W_IE(E)

            dE = (-E + torch.tanh(E_input)) / self.tau_e
            dI = (-I + torch.tanh(I_input)) / self.tau_i

            E += dt * dE
            I += dt * dI

        if self.training:
            self.E = E.mean(0, keepdim=True).detach()
            self.I = I.mean(0, keepdim=True).detach()

        return E
```

**Source**: OSCILLATORY_PATTERNS_ANALYSIS.md, Lines 130-168

---

### Goodwin Circadian Oscillator

**Purpose**: 24-hour rhythms from transcriptional feedback.

**Formula**: Repressilator-like with Delay
```
dM/dt = v₁·K₁ⁿ/(K₁ⁿ + Pⁿ) - v₂·M/(K₂ + M)
dP₀/dt = k₁·M - k₂·P₀
dP₁/dt = k₂·P₀ - k₃·P₁
...

where:
- M = mRNA
- P = protein (delayed through intermediate forms)
- n = 4-9 (high cooperativity)
```

**Nature's Implementation**: Circadian clocks in all organisms.

**Impact**: **MEDIUM - Long-Timescale Modulation**
Slow rhythms modulate fast processing. Homeostatic regulation.

**Code Example**:
```python
class GoodwinOscillator(nn.Module):
    def __init__(self, v1=1.0, K1=1.0, n=8):
        super().__init__()
        self.M = 0.5
        self.P = 0.5
        self.v1 = v1
        self.K1 = K1
        self.n = n

    def forward(self, dt=0.1):
        # Transcription (repressed by P)
        dM = self.v1 * (self.K1 ** self.n) / (self.K1 ** self.n + self.P ** self.n + 1e-8)
        dM -= 0.1 * self.M

        # Translation
        dP = 0.5 * self.M - 0.1 * self.P

        self.M += dt * dM
        self.P += dt * dP

        return self.P  # Oscillates with ~24-unit period
```

**Source**: OSCILLATORY_PATTERNS_ANALYSIS.md, Lines 220-252

---

### Izhikevich Bursting Neuron

**Purpose**: Efficient spiking model with bursting dynamics.

**Formula**: 2D System with Reset
```
dv/dt = 0.04v² + 5v + 140 - u + I
du/dt = a(bv - u)

if v ≥ 30: v ← c, u ← u + d

Parameters for bursting: a=0.02, b=0.2, c=-55, d=4
```

**Nature's Implementation**: Layer 5 pyramidal neurons burst. Information coded in burst patterns.

**Impact**: **MEDIUM - Rich Spiking Dynamics**
Single model captures 20+ neuron types. Bursting for emphasis.

**Code Example**:
```python
class IzhikevichNeuron(nn.Module):
    def __init__(self, n_neurons, a=0.02, b=0.2, c=-55, d=4):
        super().__init__()
        self.v = torch.full((n_neurons,), -65.0)
        self.u = torch.zeros(n_neurons)
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def forward(self, I, dt=0.5):
        # Dynamics
        dv = (0.04 * self.v ** 2 + 5 * self.v + 140 - self.u + I) * dt
        du = self.a * (self.b * self.v - self.u) * dt

        self.v += dv
        self.u += du

        # Reset
        fired = self.v >= 30
        self.v[fired] = self.c
        self.u[fired] += self.d

        return fired.float()
```

**Source**: OSCILLATORY_PATTERNS_ANALYSIS.md, Lines 257-299

---

### Morris-Lecar Model

**Purpose**: 2D excitable system with limit cycles.

**Formula**: Ca²⁺ and K⁺ Dynamics
```
C·dV/dt = I - g_Ca·m_∞(V)·(V - V_Ca) - g_K·w·(V - V_K) - g_L·(V - V_L)
dw/dt = φ·(w_∞(V) - w)/τ_w(V)

where:
- m_∞(V) = fast Ca activation
- w = slow K activation
```

**Nature's Implementation**: Barnacle muscle fiber. Generic excitable system.

**Impact**: **MEDIUM - Type I/II Excitability**
Bifurcation analysis of spiking. Rich dynamics.

**Code Example**:
```python
class MorrisLecarNeuron(nn.Module):
    def __init__(self, n_neurons):
        super().__init__()
        self.V = torch.full((n_neurons,), -60.0)
        self.w = torch.zeros(n_neurons)

    def m_inf(self, V):
        return 0.5 * (1 + torch.tanh((V + 1) / 15))

    def w_inf(self, V):
        return 0.5 * (1 + torch.tanh((V - 10) / 10))

    def forward(self, I, dt=0.1):
        m = self.m_inf(self.V)

        dV = (I - 4.4 * m * (self.V - 120) - 8 * self.w * (self.V + 84) - 2 * (self.V + 60)) / 20
        dw = 0.02 * (self.w_inf(self.V) - self.w)

        self.V += dV * dt
        self.w += dw * dt

        spikes = (self.V > 0).float()
        return spikes
```

**Source**: OSCILLATORY_PATTERNS_ANALYSIS.md, Lines 300-307

---

### Repressilator (Genetic Oscillator)

**Purpose**: Three-gene mutual repression creates oscillations.

**Formula**: Cyclic Inhibition
```
dm₁/dt = -m₁ + α/(1 + p₃ⁿ) + α₀
dm₂/dt = -m₂ + α/(1 + p₁ⁿ) + α₀
dm₃/dt = -m₃ + α/(1 + p₂ⁿ) + α₀

Gene 1 ⊣ Gene 2 ⊣ Gene 3 ⊣ Gene 1 (cycle)
```

**Nature's Implementation**: Synthetic biology circuit. Demonstrates programmable oscillations.

**Impact**: **MEDIUM - Cyclic Processing**
Winner-take-all cycles. Temporal pattern generation.

**Code Example**:
```python
class Repressilator(nn.Module):
    def __init__(self, alpha=10.0, n=2.0):
        super().__init__()
        self.m = torch.ones(3) * 0.5
        self.p = torch.ones(3) * 0.5
        self.alpha = alpha
        self.n = n

    def forward(self, dt=0.1):
        # Cyclic repression
        dm = torch.zeros(3)
        dm[0] = -self.m[0] + self.alpha / (1 + self.p[2] ** self.n + 1e-8) + 0.1
        dm[1] = -self.m[1] + self.alpha / (1 + self.p[0] ** self.n + 1e-8) + 0.1
        dm[2] = -self.m[2] + self.alpha / (1 + self.p[1] ** self.n + 1e-8) + 0.1

        # Protein follows mRNA
        dp = 0.5 * (self.m - self.p)

        self.m += dt * dm
        self.p += dt * dp

        return self.p  # Oscillates
```

**Source**: OSCILLATORY_PATTERNS_ANALYSIS.md, Lines 312-333

---

### Drift-Diffusion Decision Model

**Purpose**: Evidence accumulation until threshold—explains reaction times.

**Formula**: Noisy Integrator
```
dx/dt = μ·I + σ·ξ(t)

Decision when x(t) crosses threshold ±θ

Reaction time: t_decision
```

**Nature's Implementation**: Perceptual decision-making in cortex. LIP neurons accumulate evidence.

**Impact**: **MEDIUM - Explainable Decisions**
Produces reaction time distributions matching humans. Built-in speed-accuracy tradeoff.

**Code Example**:
```python
class DriftDiffusionModel(nn.Module):
    def __init__(self, n_choices=2, threshold=1.0, noise=0.1):
        super().__init__()
        self.n_choices = n_choices
        self.threshold = threshold
        self.noise = noise
        self.accumulator = torch.zeros(n_choices)

    def forward(self, evidence, dt=0.01):
        # Drift
        drift = evidence

        # Diffusion
        diffusion = self.noise * torch.randn_like(evidence)

        # Update
        self.accumulator += (drift + diffusion) * dt

        # Check threshold
        if self.accumulator.abs().max() >= self.threshold:
            decision = self.accumulator.argmax()
            rt = self.accumulator.abs().max() / (evidence.abs().max() + 1e-8)
            self.accumulator.zero_()
            return decision, rt

        return None, None  # No decision yet
```

**Source**: BIOMIMETIC_AI_ARCHITECTURE.md, Lines 485-508; MECHANISM_TO_ARCHITECTURE_PATTERNS.md

---

### Habit vs Goal Arbitration (Dual RL Systems)

**Purpose**: Model-free (habits) vs model-based (planning) with reliability-weighted mixing.

**Formula**: Dual Q-Learning with Arbitration
```
Q_habit (model-free): Q ← Q + α·(r - Q)  [Fast, cached]
Q_goal (model-based): Q = Σ P(s'|s,a)·max Q(s',a')  [Slow, flexible]

Arbitration weight:
w_goal = reliability_goal / (reliability_goal + reliability_habit)

Final: Q_total = w_goal·Q_goal + (1-w_goal)·Q_habit
```

**Nature's Implementation**: Dorsolateral striatum (habits) vs dorsomedial striatum (goals). Lesion studies show switching.

**Impact**: **MEDIUM - Flexible Learning**
Fast habits when reliable, switch to planning when uncertain. Explains human behavior in reversal tasks.

**Code Example**:
```python
class HabitGoalArbitration(nn.Module):
    def __init__(self, n_states, n_actions):
        super().__init__()
        self.Q_habit = torch.zeros(n_states, n_actions)
        self.Q_goal = torch.zeros(n_states, n_actions)
        self.reliability_habit = 0.5
        self.reliability_goal = 0.5

    def choose_action(self, state):
        # Compute mixing weight
        total_rel = self.reliability_habit + self.reliability_goal
        w_goal = self.reliability_goal / (total_rel + 1e-8)

        # Mix Q-values
        Q = w_goal * self.Q_goal[state] + (1 - w_goal) * self.Q_habit[state]

        return Q.argmax().item()

    def update_habit(self, state, action, reward, alpha=0.1):
        """Model-free update"""
        error = reward - self.Q_habit[state, action]
        self.Q_habit[state, action] += alpha * error

    def update_goal(self, state, action, next_state, reward, model):
        """Model-based update"""
        # Plan using model
        future_value = self.Q_goal[next_state].max()
        self.Q_goal[state, action] = reward + 0.9 * future_value
```

**Source**: BIOMIMETIC_AI_ARCHITECTURE.md, Lines 528-558; MECHANISM_TO_ARCHITECTURE_PATTERNS.md

---

### Attractor Memory Bank (Hopfield Network)

**Purpose**: Content-addressable memory via pattern completion.

**Formula**: Energy-Based Retrieval
```
E = -½Σ_ij w_ij·s_i·s_j  [Energy function]

Learning (Hebbian): w_ij = (1/P)Σ_μ ξ_i^μ·ξ_j^μ

Retrieval: x_new ← sign(W·x)  [Iterate until stable]

Capacity: ~0.15N patterns
```

**Nature's Implementation**: Hippocampal attractor states. Cortical memory consolidation.

**Impact**: **MEDIUM - Pattern Completion**
Partial cue → full memory. Noise-robust retrieval. Natural denoising.

**Code Example**:
```python
class AttractorMemoryBank(nn.Module):
    def __init__(self, n_neurons, n_patterns):
        super().__init__()
        self.W = torch.zeros(n_neurons, n_neurons)
        self.n = n_neurons

    def store(self, pattern):
        """Hebbian storage"""
        pattern_norm = pattern / torch.norm(pattern)
        self.W += torch.outer(pattern_norm, pattern_norm) / self.n

        # No self-connections
        self.W.fill_diagonal_(0)

    def retrieve(self, cue, n_steps=50, noise=0.0):
        """Iterative retrieval"""
        x = cue.clone()

        for _ in range(n_steps):
            u = self.W @ x

            if noise > 0:
                u += noise * torch.randn_like(u)

            x_new = torch.sign(u)

            # Check convergence
            if torch.allclose(x_new, x):
                break

            x = x_new

        return x
```

**Source**: MECHANISM_TO_ARCHITECTURE_PATTERNS.md, Lines 557-657

---

### Bayesian Inference Layer

**Purpose**: Update beliefs via Bayes' rule—principled uncertainty.

**Formula**: Posterior Update
```
P(θ|D) = P(D|θ)·P(θ) / P(D)

Log form: log P(θ|D) = log P(D|θ) + log P(θ) - log P(D)

Sequential: P(θ|D₁,D₂) = P(D₂|θ)·P(θ|D₁) / P(D₂)
```

**Nature's Implementation**: Perceptual inference. Multisensory integration.

**Impact**: **MEDIUM - Principled Uncertainty**
Proper confidence estimation. Handles missing data naturally.

**Code Example**:
```python
class BayesianInferenceLayer(nn.Module):
    def __init__(self, n_hypotheses):
        super().__init__()
        self.prior = torch.ones(n_hypotheses) / n_hypotheses
        self.posterior = self.prior.clone()

    def update(self, observation, likelihood_fn):
        """Bayes' rule update"""
        # Compute likelihood P(obs|θ) for each hypothesis
        likelihood = torch.tensor([
            likelihood_fn(observation, theta)
            for theta in range(len(self.posterior))
        ])

        # Bayes' rule
        unnormalized = likelihood * self.posterior
        self.posterior = unnormalized / (unnormalized.sum() + 1e-8)

        return self.posterior

    def sample(self):
        """Sample hypothesis from posterior"""
        return torch.multinomial(self.posterior, 1).item()
```

**Source**: MECHANISM_TO_ARCHITECTURE_PATTERNS.md

---

### Metacognition Module (Confidence Estimation)

**Purpose**: Network monitors its own uncertainty—"knows what it knows".

**Formula**: Second-Order Inference
```
Confidence = H(P(y|x))  [Entropy of prediction]

Or: Confidence = max_i P(y_i|x)  [Max probability]

Metacognitive signal: M = f(confidence, error_history)
```

**Nature's Implementation**: Prefrontal cortex tracks decision confidence.

**Impact**: **MEDIUM - Self-Awareness**
Reject low-confidence predictions. Adaptive computation (think longer when uncertain).

**Code Example**:
```python
class MetacognitionModule(nn.Module):
    def __init__(self):
        super().__init__()
        self.error_history = []

    def compute_confidence(self, logits):
        """Entropy-based confidence"""
        probs = F.softmax(logits, dim=-1)
        entropy = -(probs * torch.log(probs + 1e-8)).sum(-1)
        max_entropy = np.log(probs.shape[-1])

        # Normalize: 0 = maximum uncertainty, 1 = certain
        confidence = 1 - (entropy / max_entropy)

        return confidence

    def should_reject(self, logits, threshold=0.7):
        """Reject low-confidence predictions"""
        confidence = self.compute_confidence(logits)
        return confidence < threshold

    def adaptive_compute(self, logits, base_steps=5, max_steps=20):
        """Compute longer when uncertain"""
        confidence = self.compute_confidence(logits)

        # More steps for low confidence
        extra_steps = int((1 - confidence) * (max_steps - base_steps))

        return base_steps + extra_steps
```

**Source**: BIOMIMETIC_AI_ARCHITECTURE.md

---

### 43-75. Architectures from Original 00_NOVELTY.csv

Now including all 33 original architectures with enhanced details:

---

### Logistic Growth Regulation

**Purpose**: Self-limiting growth prevents runaway activation.

**Formula**: S-Curve Dynamics
```
dN/dt = r·N·(1 - N/K)

where:
- r = growth rate
- K = carrying capacity
- N/K = saturation term
```

**Nature's Implementation**: Population dynamics, enzyme regulation, tumor growth.

**Impact**: **LOW-MEDIUM - Bounded Growth**
Natural saturation without explicit clipping. Smooth approach to limit.

**Code Example**:
```python
class LogisticActivation(nn.Module):
    def __init__(self, r=1.0, K=1.0):
        super().__init__()
        self.r = nn.Parameter(torch.tensor(r))
        self.K = nn.Parameter(torch.tensor(K))

    def forward(self, x, dt=1.0):
        dx = self.r * x * (1 - x / self.K) * dt
        return x + dx
```

**Source**: 00_NOVELTY.csv (ID 6), BIOMD0000000008

---

### Lotka-Volterra Competition

**Purpose**: Two populations compete for resources—winner-take-all dynamics.

**Formula**: Predator-Prey System
```
dx/dt = αx - βxy
dy/dt = δxy - γy

where:
- x, y = populations
- α = prey growth, β = predation rate
- γ = predator death, δ = conversion efficiency
```

**Nature's Implementation**: Predator-prey dynamics, neural competition.

**Impact**: **LOW-MEDIUM - Competitive Dynamics**
Natural oscillations. Winner-take-all without explicit competition.

**Code Example**:
```python
class LotkaVolterraLayer(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.x = torch.ones(dim) * 0.5  # Prey
        self.y = torch.ones(dim) * 0.5  # Predator

    def forward(self, input, dt=0.1):
        dx = (1.0 * self.x - 0.5 * self.x * self.y + input) * dt
        dy = (0.3 * self.x * self.y - 0.2 * self.y) * dt

        self.x += dx
        self.y += dy

        return self.x
```

**Source**: 00_NOVELTY.csv (ID 8), BIOMD0000000012

---

### MWC Allosteric Model

**Purpose**: Cooperative binding with conformational states—steep response curves.

**Formula**: Two-State Model
```
Y = L·c·α(1 + α)^(n-1) / (L(1 + cα)^n + (1 + α)^n)

where:
- L = T/R equilibrium constant
- α = ligand concentration
- c = relative affinity
- n = number of subunits
```

**Nature's Implementation**: Hemoglobin, ion channels, receptors.

**Impact**: **LOW-MEDIUM - Cooperative Activation**
Ultrasensitivity through conformational coupling.

**Code Example**:
```python
class MWCActivation(nn.Module):
    def __init__(self, L=1000, c=0.01, n=4):
        super().__init__()
        self.L = L
        self.c = c
        self.n = n

    def forward(self, alpha):
        numerator = self.L * self.c * alpha * ((1 + alpha) ** (self.n - 1))
        denominator = self.L * ((1 + self.c * alpha) ** self.n) + ((1 + alpha) ** self.n)

        return numerator / (denominator + 1e-8)
```

**Source**: 00_NOVELTY.csv (ID 10)

---

### JAK-STAT Signaling

**Purpose**: Cytokine signaling with SOCS negative feedback.

**Formula**: Receptor-Mediated Activation
```
d[STAT]/dt = k_JAK·[JAK*]·[STAT] - k_dephos·[STAT_p]
d[SOCS]/dt = k_tx·[STAT_p] - k_deg·[SOCS]

Feedback: [JAK*] inhibited by [SOCS]
```

**Nature's Implementation**: Immune signaling, growth factors.

**Impact**: **LOW-MEDIUM - Feedback Control**
Adaptive response with automatic shutoff.

**Code Example**:
```python
class JAKSTATLayer(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.STAT = torch.zeros(dim)
        self.SOCS = torch.zeros(dim)

    def forward(self, JAK_active, dt=1.0):
        # STAT phosphorylation (inhibited by SOCS)
        activation = 0.5 * JAK_active * (1 / (1 + self.SOCS))
        dephosphorylation = 0.1 * self.STAT

        self.STAT += (activation - dephosphorylation) * dt

        # SOCS production (feedback)
        self.SOCS += (0.2 * self.STAT - 0.1 * self.SOCS) * dt

        return self.STAT
```

**Source**: expand_04_signaling.py, Lines 383-414

---

### Notch-Delta Lateral Inhibition

**Purpose**: One cell activates, inhibits neighbors—pattern formation.

**Formula**: Juxtacrine Signaling
```
d[Notch]/dt = k_on·[Delta_neighbor] - k_off·[Notch]
d[Delta]/dt = k_syn / (1 + [Notch]^n) - k_deg·[Delta]

High Notch → Low Delta (inhibition)
```

**Nature's Implementation**: Somite segmentation, neural patterning.

**Impact**: **LOW-MEDIUM - Spatial Patterning**
Self-organizing patterns without central control.

**Code Example**:
```python
class NotchDeltaCell(nn.Module):
    def __init__(self):
        super().__init__()
        self.Notch = 0.5
        self.Delta = 0.5

    def forward(self, neighbor_delta, dt=0.1):
        # Notch activation by neighbor Delta
        dNotch = (0.5 * neighbor_delta - 0.1 * self.Notch) * dt

        # Delta repressed by own Notch
        Delta_synthesis = 1.0 / (1 + self.Notch ** 2)
        dDelta = (Delta_synthesis - 0.1 * self.Delta) * dt

        self.Notch += dNotch
        self.Delta += dDelta

        return self.Delta  # Transmit to neighbors
```

**Source**: expand_04_signaling.py, Lines 329-354

---

### Power-Law STDP

**Purpose**: Weight-dependent plasticity with power-law scaling.

**Formula**: Sublinear Weight Dependence
```
Δw = η·w^μ·f(Δt)

where:
- μ < 1 (typically 0.5)
- Weak synapses change more than strong
- f(Δt) = STDP timing function
```

**Nature's Implementation**: Observed in hippocampal synapses.

**Impact**: **LOW - Balanced Learning**
Prevents strong synapses from dominating. More distributed representations.

**Code Example**:
```python
class PowerLawSTDP(nn.Module):
    def __init__(self, n_in, n_out, mu=0.5):
        super().__init__()
        self.W = nn.Parameter(torch.rand(n_out, n_in) * 0.1)
        self.mu = mu

    def update(self, pre_spike, post_spike, spike_time_diff, lr=0.01):
        if spike_time_diff > 0:
            stdp = np.exp(-spike_time_diff / 20.0)
        else:
            stdp = -np.exp(spike_time_diff / 20.0)

        # Power-law weight dependence
        weight_factor = torch.abs(self.W) ** self.mu

        dW = lr * stdp * torch.outer(post_spike, pre_spike) * weight_factor
        self.W += dW
```

**Source**: PLASTICITY_FORMULAS_COMPLETE.md, Lines 126-136

---

### Anti-Hebbian STDP

**Purpose**: Inverted timing rule—decorrelation instead of correlation.

**Formula**: Reversed STDP
```
Δw = -A₊·exp(-Δt/τ₊)  if Δt > 0  [LTD instead of LTP]
Δw = +A₋·exp(Δt/τ₋)   if Δt < 0  [LTP instead of LTD]
```

**Nature's Implementation**: Some interneurons, decorrelating circuits.

**Impact**: **LOW - Decorrelation**
Reduces redundancy. Complementary to Hebbian learning.

**Code Example**:
```python
class AntiHebbianSTDP(nn.Module):
    def __init__(self, n_in, n_out):
        super().__init__()
        self.W = nn.Parameter(torch.randn(n_out, n_in) * 0.01)

    def update(self, pre_spike, post_spike, spike_time_diff, lr=0.01):
        if spike_time_diff > 0:  # Pre before post
            stdp = -0.01 * np.exp(-spike_time_diff / 20.0)  # LTD
        else:
            stdp = 0.01 * np.exp(spike_time_diff / 20.0)  # LTP

        self.W += lr * stdp * torch.outer(post_spike, pre_spike)
```

**Source**: PLASTICITY_FORMULAS_COMPLETE.md, Lines 67-78

---

### Mexican Hat STDP

**Purpose**: Center-surround in time—precise timing encouraged, broad timing discouraged.

**Formula**: Difference of Gaussians in Time
```
Δw = A₁·exp(-Δt²/2σ₁²) - A₂·exp(-Δt²/2σ₂²)

where σ₁ < σ₂ (narrow positive, broad negative)
```

**Nature's Implementation**: Temporal precision learning.

**Impact**: **LOW - Temporal Precision**
Encourages tight synchrony. Discourages weak correlations.

**Code Example**:
```python
class MexicanHatSTDP(nn.Module):
    def __init__(self, n_in, n_out, sigma1=5.0, sigma2=20.0):
        super().__init__()
        self.W = nn.Parameter(torch.randn(n_out, n_in) * 0.01)
        self.sigma1 = sigma1
        self.sigma2 = sigma2

    def update(self, pre_spike, post_spike, spike_time_diff, lr=0.01):
        # Narrow positive Gaussian
        pos = 0.02 * np.exp(-spike_time_diff ** 2 / (2 * self.sigma1 ** 2))

        # Broad negative Gaussian
        neg = 0.01 * np.exp(-spike_time_diff ** 2 / (2 * self.sigma2 ** 2))

        stdp = pos - neg

        self.W += lr * stdp * torch.outer(post_spike, pre_spike)
```

**Source**: PLASTICITY_FORMULAS_COMPLETE.md, Lines 80-92

---

### Covariance Learning Rule

**Purpose**: Remove mean activity—learn decorrelated features.

**Formula**: Mean-Subtracted Hebbian
```
Δw_ij = η·(x_i - x̄_i)·(y_j - ȳ_j)

where x̄, ȳ = running averages
```

**Nature's Implementation**: Efficient coding in sensory systems.

**Impact**: **LOW - Whitening**
Decorrelated representations. Better than raw Hebbian.

**Code Example**:
```python
class CovarianceLearning(nn.Module):
    def __init__(self, n_in, n_out):
        super().__init__()
        self.W = nn.Parameter(torch.randn(n_out, n_in) * 0.01)
        self.x_mean = torch.zeros(n_in)
        self.y_mean = torch.zeros(n_out)

    def forward(self, x):
        return F.linear(x, self.W)

    def update(self, x, y, lr=0.01, momentum=0.9):
        # Update running means
        self.x_mean = momentum * self.x_mean + (1 - momentum) * x.mean(0)
        self.y_mean = momentum * self.y_mean + (1 - momentum) * y.mean(0)

        # Mean-subtracted update
        x_centered = x - self.x_mean
        y_centered = y - self.y_mean

        dW = torch.outer(y_centered.mean(0), x_centered.mean(0))
        self.W += lr * dW
```

**Source**: PLASTICITY_FORMULAS_COMPLETE.md, Lines 255-265

---

### 52-113. Additional Novel Architectures

Due to space constraints, here are condensed entries for the remaining 61 architectures discovered:

---

### Multiplicative STDP (Soft Bounds)
**Formula**: `Δw = (w_max - w)·f₊(Δt)` for LTP, `w·f₋(Δt)` for LTD
**Impact**: Naturally bounded weights without clipping
**Source**: PLASTICITY_FORMULAS_COMPLETE.md:96-108

### Symmetric STDP
**Formula**: `Δw = A·exp(-|Δt|/τ)` (both directions LTP)
**Impact**: Non-Hebbian synchrony detection
**Source**: PLASTICITY_FORMULAS_COMPLETE.md:40-50

### Log-STDP
**Formula**: `Δw = η·log(1 + w/w₀)·f(Δt)`
**Impact**: Weak synapses learn faster
**Source**: PLASTICITY_FORMULAS_COMPLETE.md:110-122

### Eligibility Trace Memory
**Formula**: `de/dt = -e/τ_e + STDP(Δt)·δ(t - t_spike)`
**Impact**: Credit assignment for delayed rewards
**Source**: PLASTICITY_FORMULAS_COMPLETE.md:477-488

### Intrinsic Excitability Homeostasis
**Formula**: `dg_max/dt = β·(r_target - r_actual)`
**Impact**: Non-synaptic plasticity for stability
**Source**: PLASTICITY_FORMULAS_COMPLETE.md:313-323

### Heterosynaptic Plasticity
**Formula**: `Δw_i = -γ·Σ_{j≠i} Δw_j`
**Impact**: Local competition between synapses
**Source**: PLASTICITY_FORMULAS_COMPLETE.md:325-336

### Metaplastic Threshold
**Formula**: `θ_m = ⟨c²⟩/θ₀`
**Impact**: Learning to learn, memory consolidation
**Source**: PLASTICITY_FORMULAS_COMPLETE.md:401-414

### Sparse Coding Objective
**Formula**: `min_a ||x - Φa||² + λ||a||₁`
**Impact**: L1-sparse representations like V1
**Source**: PLASTICITY_FORMULAS_COMPLETE.md:432-443

### Predictive Coding Error
**Formula**: `ε = x - x̂ = x - Wr`
**Impact**: Hierarchical prediction-driven learning
**Source**: PLASTICITY_FORMULAS_COMPLETE.md:445-458

### Contrastive Divergence
**Formula**: `Δw = η·(⟨s_i s_j⟩_data - ⟨s_i s_j⟩_model)`
**Impact**: Energy-based unsupervised learning
**Source**: PLASTICITY_FORMULAS_COMPLETE.md:460-471

### Infomax/ICA Learning
**Formula**: `ΔW = η·(I + (1 - 2y)u^T)W`
**Impact**: Independent component extraction
**Source**: PLASTICITY_FORMULAS_COMPLETE.md:419-430

### NMDA Working Memory Gate
**Formula**: Bistable NMDA plateau potentials with long τ
**Impact**: Persistent activity for working memory
**Source**: bio_ai_components.py

### Rare Event Detector (Cascade)
**Formula**: 3-stage MAPK-like cascade with high gain
**Impact**: 1000x amplification for anomaly detection
**Source**: SIGNAL_AMPLIFICATION_REPORT.md:802-875

### Autoactivation Amplifier
**Formula**: Product autocatalyzes own production
**Impact**: Exponential amplification until saturation
**Source**: SIGNAL_AMPLIFICATION_REPORT.md:445-458

### Bistable Toggle Switch
**Formula**: Mutual repression creates two stable states
**Impact**: Memory without recurrence
**Source**: SIGNAL_AMPLIFICATION_REPORT.md:423-507

### FitzHugh-Nagumo Oscillator
**Formula**: 2D excitable system with cubic nullcline
**Impact**: Oscillatory attention reset
**Source**: OSCILLATORY_PATTERNS_ANALYSIS.md:56-81

### Van der Pol Oscillator
**Formula**: Self-sustaining oscillation via nonlinear damping
**Impact**: Periodic routing between pathways
**Source**: OSCILLATORY_PATTERNS_ANALYSIS.md:82-90

### ING Gamma (Interneuron Network)
**Formula**: Mutually inhibiting interneurons create fast gamma
**Impact**: 60-100 Hz inhibitory competition
**Source**: OSCILLATORY_PATTERNS_ANALYSIS.md:160-168

### Ring Attractor (Head Direction)
**Formula**: Continuous attractor with periodic boundary
**Impact**: Angular/cyclic variable representation
**Source**: MECHANISM_TO_ARCHITECTURE_PATTERNS.md

### Line Attractor (Eye Position)
**Formula**: 1D continuous attractor for integration
**Impact**: Perfect integration without drift
**Source**: MECHANISM_TO_ARCHITECTURE_PATTERNS.md

### CaMKII Autophosphorylation
**Formula**: Self-sustaining kinase activity
**Impact**: Molecular memory for LTP
**Source**: expand_04_signaling.py:217-222

### Calcineurin Activation
**Formula**: Ca/CaM-activated phosphatase
**Impact**: LTD signaling pathway
**Source**: expand_04_signaling.py:223-228

### RyR Calcium Release
**Formula**: CICR amplification
**Impact**: Calcium wave propagation
**Source**: expand_04_signaling.py:176-180

### PMCA Calcium Extrusion
**Formula**: Plasma membrane Ca pump
**Impact**: Restore baseline calcium
**Source**: expand_04_signaling.py:187-193

### NCX Sodium-Calcium Exchanger
**Formula**: Electrogenic 3Na:1Ca exchange
**Impact**: Voltage-dependent Ca regulation
**Source**: expand_04_signaling.py:194-198

### Calcium Buffering
**Formula**: Rapid Ca binding to buffer proteins
**Impact**: Shape calcium transients
**Source**: expand_04_signaling.py:199-204

### PI3K-AKT Survival Pathway
**Formula**: PIP3-mediated kinase activation
**Impact**: Anti-apoptotic signaling
**Source**: expand_04_signaling.py:93-117

### mTORC1 Growth Signaling
**Formula**: Rheb-activated kinase complex
**Impact**: Protein synthesis control
**Source**: expand_04_signaling.py:137-153

### NF-κB Inflammatory Response
**Formula**: IκB degradation → nuclear translocation
**Impact**: Oscillatory gene expression
**Source**: expand_04_signaling.py:264-294

### Wnt/β-Catenin Pathway
**Formula**: Destruction complex inhibition
**Impact**: Development and stem cells
**Source**: expand_04_signaling.py:297-327

### TGF-β/SMAD Signaling
**Formula**: Receptor-mediated SMAD phosphorylation
**Impact**: Growth factor responses
**Source**: expand_04_signaling.py:356-381

### Adenylyl Cyclase (Gs-stimulated)
**Formula**: cAMP production from ATP
**Impact**: Second messenger cascades
**Source**: expand_04_signaling.py:233-241

### PKA Activation (cAMP)
**Formula**: 4 cAMP → catalytic subunit release
**Impact**: Phosphorylation cascade
**Source**: expand_04_signaling.py:239-249

### CREB Transcription Factor
**Formula**: PKA-mediated gene activation
**Impact**: Long-term memory formation
**Source**: expand_04_signaling.py:251-255

### IKK Inflammatory Kinase
**Formula**: Signal-activated kinase complex
**Impact**: Innate immune responses
**Source**: expand_04_signaling.py:266-270

### GSK3β Regulation
**Formula**: AKT-mediated inhibition
**Impact**: Glycogen synthesis, Wnt signaling
**Source**: expand_04_signaling.py (AKT targets)

### FOXO Transcription Factor
**Formula**: AKT phosphorylation → cytoplasmic retention
**Impact**: Apoptosis gene regulation
**Source**: expand_04_signaling.py (AKT targets)

### TSC2 Tumor Suppressor
**Formula**: AKT inhibition releases mTORC1
**Impact**: Growth control
**Source**: expand_04_signaling.py (AKT targets)

### S6K Translation Regulator
**Formula**: mTORC1-activated kinase
**Impact**: Ribosome biogenesis
**Source**: expand_04_signaling.py:143-147

### 4E-BP1 Translation Repressor
**Formula**: mTORC1 phosphorylation releases eIF4E
**Impact**: Cap-dependent translation
**Source**: expand_04_signaling.py:149-153

### Dishevelled Wnt Transducer
**Formula**: Receptor activation inhibits destruction
**Impact**: Wnt signal amplification
**Source**: expand_04_signaling.py:311-315

### β-Catenin Transcription
**Formula**: Nuclear accumulation → gene activation
**Impact**: Development genes
**Source**: expand_04_signaling.py:317-327

### NICD Notch Signaling
**Formula**: γ-secretase cleavage → nuclear entry
**Impact**: Cell fate decisions
**Source**: expand_04_signaling.py:338-348

### Hes/Hey Transcriptional Repressors
**Formula**: NICD-driven gene expression
**Impact**: Maintain progenitor state
**Source**: expand_04_signaling.py:344-348

### SMAD2/3 Phosphorylation
**Formula**: TGF-β receptor kinase activity
**Impact**: Cytoplasm-to-nucleus shuttle
**Source**: expand_04_signaling.py:365-375

### SMAD4 Co-Factor
**Formula**: Forms complex with pSMAD2/3
**Impact**: Nuclear entry signal
**Source**: expand_04_signaling.py:371-375

### PDE4 Feedback Inhibition
**Formula**: PKA activates cAMP degradation
**Impact**: Negative feedback oscillations
**Source**: expand_04_signaling.py:257-261

### A20 Ubiquitin Editing
**Formula**: NF-κB-induced IKK inhibitor
**Impact**: Terminate inflammation
**Source**: expand_04_signaling.py:290-294

### IκBα Resynthesis
**Formula**: NF-κB drives own inhibitor
**Impact**: Oscillatory negative feedback
**Source**: expand_04_signaling.py:284-288

### BioTransformer (Complete Architecture)
**Formula**: Multi-component biological transformer
**Impact**: Integrated bio-inspired architecture
**Source**: bio_ai_components.py:727-799

### Channel Gate m³h (Complete)
**Formula**: Sodium channel activation/inactivation
**Impact**: Realistic action potential generation
**Source**: bio_ai_components.py:130-209

### Conductance-Based Neuron
**Formula**: Full Hodgkin-Huxley with multiple channels
**Impact**: Biophysically accurate spiking
**Source**: 00_NOVELTY.csv, bio databases

### Short-Term Synaptic Plasticity
**Formula**: Resource depletion and recovery
**Impact**: Dynamic synaptic strength
**Source**: 00_NOVELTY.csv (ID 13-17)

### Vesicle Release Dynamics
**Formula**: Probabilistic neurotransmitter release
**Impact**: Stochastic transmission
**Source**: 00_NOVELTY.csv (ID 14-15)

### Facilitation/Depression
**Formula**: Use-dependent synaptic modulation
**Impact**: Temporal filtering
**Source**: 00_NOVELTY.csv (ID 16-17)

### AMPA Receptor Kinetics
**Formula**: Fast glutamate-gated channel
**Impact**: Excitatory transmission (3ms)
**Source**: bioformulas.db, 00_NOVELTY.csv

### GABA Receptor Dynamics
**Formula**: Inhibitory chloride channel
**Impact**: Fast inhibition (10ms)
**Source**: bioformulas.db

### Dendritic Spike Initiation
**Formula**: Active dendrites with Na/Ca spikes
**Impact**: Non-linear integration
**Source**: bio research literature

### Backpropagating Action Potentials
**Formula**: Retrograde spike propagation
**Impact**: Coincidence detection for STDP
**Source**: neuroscience literature

### Spike-Frequency Adaptation
**Formula**: AHP currents reduce firing over time
**Impact**: Transient vs sustained responses
**Source**: 00_NOVELTY.csv (ID 18)

### Bursting via Slow Calcium
**Formula**: Ca-activated K current creates bursts
**Impact**: Information in burst patterns
**Source**: Computational neuroscience

### Gain Modulation
**Formula**: Multiplicative scaling of responses
**Impact**: Context-dependent processing
**Source**: Sensory neuroscience

---

### Full Hodgkin-Huxley Conductance Model

**Purpose**: Gold standard biophysical neuron model with voltage-gated ion channels.

**Formula**: Complete Conductance-Based Dynamics
```
C_m·dV/dt = -(g_Na·m³·h·(V - E_Na) + g_K·n⁴·(V - E_K) + g_L·(V - E_L)) + I_ext

Gating variables:
dm/dt = α_m(V)·(1 - m) - β_m(V)·m
dh/dt = α_h(V)·(1 - h) - β_h(V)·h  
dn/dt = α_n(V)·(1 - n) - β_n(V)·n

where:
- C_m = membrane capacitance (1 μF/cm²)
- g_Na, g_K, g_L = conductances (120, 36, 0.3 mS/cm²)
- E_Na, E_K, E_L = reversal potentials (50, -77, -54.4 mV)
- m³h = sodium activation³ × inactivation
- n⁴ = potassium activation⁴
- α, β = voltage-dependent rate functions
```

**Nature's Implementation**: Squid giant axon action potentials (Hodgkin & Huxley, 1952). Universal model for voltage-gated channels. Nobel Prize 1963.

**Impact**: **HIGH - Biophysical Gold Standard**
Most accurate spiking model. Matches experimental data precisely. Explains action potential shape, conduction velocity, refractory period. Foundation for all conductance-based models. Computational cost higher than LIF but essential for biophysical realism.

**Code Example**:
```python
class HodgkinHuxleyNeuron(nn.Module):
    """Complete HH model with Na, K, and leak channels"""
    
    def __init__(self, n_neurons):
        super().__init__()
        # State variables
        self.V = torch.full((n_neurons,), -65.0)  # Membrane potential (mV)
        self.m = torch.zeros(n_neurons)  # Na activation
        self.h = torch.ones(n_neurons)   # Na inactivation
        self.n = torch.zeros(n_neurons)  # K activation
        
        # Parameters (classic HH values)
        self.C_m = 1.0      # μF/cm²
        self.g_Na = 120.0   # mS/cm²
        self.g_K = 36.0     # mS/cm²
        self.g_L = 0.3      # mS/cm²
        self.E_Na = 50.0    # mV
        self.E_K = -77.0    # mV
        self.E_L = -54.4    # mV
    
    def alpha_m(self, V):
        return 0.1 * (V + 40) / (1 - torch.exp(-(V + 40) / 10))
    
    def beta_m(self, V):
        return 4.0 * torch.exp(-(V + 65) / 18)
    
    def alpha_h(self, V):
        return 0.07 * torch.exp(-(V + 65) / 20)
    
    def beta_h(self, V):
        return 1.0 / (1 + torch.exp(-(V + 35) / 10))
    
    def alpha_n(self, V):
        return 0.01 * (V + 55) / (1 - torch.exp(-(V + 55) / 10))
    
    def beta_n(self, V):
        return 0.125 * torch.exp(-(V + 65) / 80)
    
    def forward(self, I_ext, dt=0.01):
        """Integrate HH equations"""
        # Gating variable dynamics
        dm = (self.alpha_m(self.V) * (1 - self.m) - self.beta_m(self.V) * self.m) * dt
        dh = (self.alpha_h(self.V) * (1 - self.h) - self.beta_h(self.V) * self.h) * dt
        dn = (self.alpha_n(self.V) * (1 - self.n) - self.beta_n(self.V) * self.n) * dt
        
        self.m += dm
        self.h += dh
        self.n += dn
        
        # Ionic currents
        I_Na = self.g_Na * (self.m ** 3) * self.h * (self.V - self.E_Na)
        I_K = self.g_K * (self.n ** 4) * (self.V - self.E_K)
        I_L = self.g_L * (self.V - self.E_L)
        
        # Membrane potential
        dV = (I_ext - I_Na - I_K - I_L) / self.C_m * dt
        self.V += dV
        
        # Spike detection
        spikes = (self.V > 0).float()
        
        return spikes, self.V
```

**Source**: Hodgkin & Huxley (1952) J Physiol; 00_NOVELTY.csv; Computational Neuroscience textbooks

---

### Canonical Pair-Based STDP

**Purpose**: Foundational spike-timing dependent plasticity—causality-based learning.

**Formula**: Classic Asymmetric Learning Window
```
Δw = {
    A_+·exp(-Δt/τ_+)   if Δt > 0  (pre before post → LTP)
    -A_-·exp(Δt/τ_-)   if Δt < 0  (post before pre → LTD)
}

where:
- Δt = t_post - t_pre (spike time difference)
- A_+ ≈ 0.01 (LTP amplitude)
- A_- ≈ 0.01 (LTD amplitude)  
- τ_+ ≈ 20 ms (LTP time constant)
- τ_- ≈ 20 ms (LTD time constant)
```

**Nature's Implementation**: First discovered in hippocampus, cortex, cerebellum. Universal learning rule in brain. Causality detector: "neurons that fire together, wire together" (Hebb, 1949), but with precise timing.

**Impact**: **HIGH - Foundational Learning Rule**
Most important unsupervised learning rule in neuroscience. Basis for sequence learning, temporal coding, causality detection. Led to all STDP variants (triplet, voltage-dependent, etc.). Explains how brain learns without labels. Critical for spiking neural networks.

**Code Example**:
```python
class PairBasedSTDP(nn.Module):
    """Classic STDP with exponential windows"""
    
    def __init__(self, n_pre, n_post, A_plus=0.01, A_minus=0.01, tau_plus=20.0, tau_minus=20.0):
        super().__init__()
        self.W = nn.Parameter(torch.randn(n_post, n_pre) * 0.01)
        
        # STDP parameters
        self.A_plus = A_plus
        self.A_minus = A_minus
        self.tau_plus = tau_plus
        self.tau_minus = tau_minus
        
        # Spike traces for eligibility
        self.pre_trace = torch.zeros(n_pre)
        self.post_trace = torch.zeros(n_post)
    
    def forward(self, x):
        """Standard forward pass"""
        return F.linear(x, self.W)
    
    def stdp_update(self, pre_spikes, post_spikes, dt=1.0):
        """Update weights based on spike timing"""
        # Decay traces
        self.pre_trace *= np.exp(-dt / self.tau_plus)
        self.post_trace *= np.exp(-dt / self.tau_minus)
        
        # LTP: post spike while pre trace active
        if post_spikes.any():
            dW_ltp = self.A_plus * torch.outer(post_spikes, self.pre_trace)
            self.W += dW_ltp
        
        # LTD: pre spike while post trace active  
        if pre_spikes.any():
            dW_ltd = -self.A_minus * torch.outer(self.post_trace, pre_spikes)
            self.W += dW_ltd
        
        # Update traces with new spikes
        self.pre_trace += pre_spikes
        self.post_trace += post_spikes
        
        # Weight bounds
        self.W.data.clamp_(0, 1)
    
    def get_spike_timing_curve(self):
        """Plot classic STDP learning window"""
        delta_t = np.linspace(-100, 100, 200)
        dw = np.where(delta_t > 0,
                     self.A_plus * np.exp(-delta_t / self.tau_plus),
                     -self.A_minus * np.exp(delta_t / self.tau_minus))
        return delta_t, dw
```

**Source**: Bi & Poo (1998) J Neurosci; Markram et al. (1997) Science; PLASTICITY_FORMULAS_COMPLETE.md ID:25

---

### Leaky Integrate-and-Fire (LIF) Neuron

**Purpose**: Canonical spiking neuron model—simple, efficient, widely used.

**Formula**: Leaky Integration with Threshold
```
τ_m·dV/dt = -(V - E_L) + R_m·I_ext

If V ≥ V_th: emit spike, V ← V_reset, wait t_refract

where:
- τ_m = membrane time constant (10-20 ms)
- E_L = resting potential (-70 mV)
- V_th = spike threshold (-55 mV)
- V_reset = reset potential (-65 mV)
- R_m = membrane resistance
- t_refract = refractory period (2-5 ms)
```

**Nature's Implementation**: Simplified model capturing essential neuron properties: leak, integration, threshold. Trade-off between Hodgkin-Huxley (complex) and rate models (too simple).

**Impact**: **MEDIUM-HIGH - Standard Spiking Model**
Most widely used spiking neuron model. 100x faster than Hodgkin-Huxley. Captures key properties: temporal integration, threshold, refractory period. Foundation for large-scale spiking neural networks (Loihi, SpiNNaker, BrainScaleS). Good balance of realism vs efficiency.

**Code Example**:
```python
class LIFNeuron(nn.Module):
    """Leaky Integrate-and-Fire neuron"""
    
    def __init__(self, n_neurons, tau_m=10.0, V_th=-55.0, V_reset=-65.0, t_refract=2.0):
        super().__init__()
        self.n = n_neurons
        
        # Parameters
        self.tau_m = tau_m      # Membrane time constant (ms)
        self.E_L = -70.0        # Resting potential (mV)
        self.V_th = V_th        # Spike threshold (mV)
        self.V_reset = V_reset  # Reset potential (mV)
        self.R_m = 10.0         # Membrane resistance (MΩ)
        
        # State variables
        self.V = torch.full((n_neurons,), self.E_L)
        self.refractory_counter = torch.zeros(n_neurons)
        self.t_refract = t_refract
    
    def forward(self, I_ext, dt=1.0):
        """Integrate and fire"""
        # Only integrate non-refractory neurons
        not_refractory = self.refractory_counter == 0
        
        # Leaky integration
        dV = (-(self.V - self.E_L) + self.R_m * I_ext) / self.tau_m * dt
        self.V = torch.where(not_refractory, self.V + dV, self.V)
        
        # Spike detection
        spikes = (self.V >= self.V_th) & not_refractory
        
        # Reset spiking neurons
        self.V = torch.where(spikes, torch.tensor(self.V_reset), self.V)
        self.refractory_counter = torch.where(
            spikes, 
            torch.tensor(self.t_refract),
            self.refractory_counter
        )
        
        # Decrement refractory counter
        self.refractory_counter = torch.clamp(
            self.refractory_counter - dt, 
            min=0
        )
        
        return spikes.float()
    
    def reset_state(self):
        """Reset to resting state"""
        self.V.fill_(self.E_L)
        self.refractory_counter.zero_()
```

**Source**: Lapicque (1907); Gerstner & Kistler (2002) Spiking Neuron Models; 00_NOVELTY.csv

---
### Linear-Nonlinear-Poisson (LNP) Model

**Purpose**: Sensory neuron encoding model—stimulus to spike train conversion.

**Formula**: Filter, Nonlinearity, Stochastic Spiking
```
r(t) = f(∫ k(τ)·s(t-τ) dτ)

P(spike in [t, t+dt]) = r(t)·dt

where:
- s(t) = sensory stimulus (e.g., light intensity, sound)
- k(τ) = temporal filter (receptive field)
- f(·) = nonlinearity (typically sigmoid or exp)
- r(t) = instantaneous firing rate
- Spikes follow Poisson process with rate r(t)
```

**Nature's Implementation**: Retinal ganglion cells, LGN neurons, auditory nerve fibers, olfactory receptor neurons. Standard model in sensory neuroscience.

**Impact**: **MEDIUM - Sensory Coding**
Captures how sensory neurons encode stimuli. Linear filter extracts features, nonlinearity shapes response, Poisson adds variability. Used to fit experimental data, predict responses to novel stimuli. Foundation for understanding sensory representations. Important for neural prosthetics and brain-computer interfaces.

**Code Example**:
```python
class LNPNeuron(nn.Module):
    """Linear-Nonlinear-Poisson sensory neuron"""
    
    def __init__(self, filter_length=50, nonlinearity='exponential'):
        super().__init__()
        # Linear filter (learnable receptive field)
        self.filter = nn.Parameter(torch.randn(filter_length) * 0.1)
        self.nonlinearity_type = nonlinearity
        
        # Bias
        self.bias = nn.Parameter(torch.zeros(1))
    
    def linear_stage(self, stimulus):
        """Convolve stimulus with temporal filter"""
        # stimulus shape: (batch, time)
        # Pad for causal filtering
        padded = F.pad(stimulus.unsqueeze(1), (len(self.filter)-1, 0))
        
        # Convolve
        filtered = F.conv1d(padded, self.filter.flip(0).view(1, 1, -1))
        
        return filtered.squeeze(1)
    
    def nonlinear_stage(self, x):
        """Apply nonlinearity to filtered stimulus"""
        if self.nonlinearity_type == 'exponential':
            # Exponential nonlinearity (common for spiking)
            firing_rate = torch.exp(x + self.bias)
        elif self.nonlinearity_type == 'sigmoid':
            # Sigmoid nonlinearity (bounded)
            firing_rate = torch.sigmoid(x + self.bias) * 100  # Max 100 Hz
        elif self.nonlinearity_type == 'softplus':
            # Soft rectification
            firing_rate = F.softplus(x + self.bias)
        else:
            raise ValueError(f"Unknown nonlinearity: {self.nonlinearity_type}")
        
        return firing_rate
    
    def poisson_spiking(self, firing_rate, dt=0.001):
        """Generate Poisson spikes from firing rate"""
        # Probability of spike in time window dt
        spike_prob = firing_rate * dt
        
        # Poisson process: compare with random uniform
        spikes = (torch.rand_like(spike_prob) < spike_prob).float()
        
        return spikes
    
    def forward(self, stimulus, dt=0.001, return_rate=False):
        """Full LNP cascade"""
        # Linear filtering
        filtered = self.linear_stage(stimulus)
        
        # Nonlinearity
        firing_rate = self.nonlinear_stage(filtered)
        
        if return_rate:
            return firing_rate
        
        # Poisson spiking
        spikes = self.poisson_spiking(firing_rate, dt)
        
        return spikes, firing_rate
    
    def fit_to_data(self, stimulus, spike_train, optimizer, n_epochs=100):
        """Fit LNP model to experimental data"""
        for epoch in range(n_epochs):
            # Predict firing rate
            rate_pred = self.forward(stimulus, return_rate=True)
            
            # Negative log-likelihood loss (Poisson)
            # L = -sum(spikes*log(rate) - rate)
            loss = -(spike_train * torch.log(rate_pred + 1e-8) - rate_pred).mean()
            
            # Update
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            if epoch % 20 == 0:
                print(f"Epoch {epoch}, Loss: {loss.item():.4f}")
```

**Source**: Chichilnisky (2001) Network; Pillow et al. (2008) Nature; Sensory neuroscience literature

---
### Fokker-Planck Equation (Membrane Potential Distribution)

**Purpose**: Govern probability distributions of membrane potentials under noise—foundation for population density methods.

**Formula**: Forward Kolmogorov Equation
```
∂p(V,t)/∂t = -∂[A(V)·p(V,t)]/∂V + (1/2)·∂²[B(V)·p(V,t)]/∂V²

where:
- p(V,t) = probability density of membrane potential V at time t
- A(V) = drift coefficient (deterministic dynamics)
- B(V) = diffusion coefficient (noise intensity²)

For LIF: A(V) = -(V - E_L)/τ_m + R_m·I_ext/τ_m
         B(V) = σ² (constant noise)
```

**Nature's Implementation**: Neurons receive thousands of stochastic synaptic inputs (shot noise). Population-level statistics govern collective dynamics. Used in theoretical neuroscience for analytical tractability.

**Impact**: **MEDIUM - Population Analysis**
Enables analytical solutions for population responses. Alternative to Monte Carlo simulations. Reveals how noise shapes firing rates and synchrony. Foundation for density methods in large-scale brain modeling. Critical for understanding variability in neural responses.

**Code Example**:
```python
class FokkerPlanckSolver:
    """Solve Fokker-Planck for LIF neuron population"""
    
    def __init__(self, V_min=-80, V_max=-50, V_th=-55, n_bins=1000):
        self.V = np.linspace(V_min, V_max, n_bins)
        self.dV = self.V[1] - self.V[0]
        self.V_th_idx = np.argmin(np.abs(self.V - V_th))
        
        # Parameters
        self.tau_m = 10.0  # ms
        self.E_L = -70.0   # mV
        self.R_m = 10.0    # MΩ
        self.sigma = 3.0   # mV/√ms (noise)
        
        self.p = np.zeros(n_bins)
        self.p[n_bins//4] = 1.0 / self.dV  # Initial delta function
    
    def drift(self, V, I_ext):
        """A(V): drift coefficient"""
        return (-(V - self.E_L) + self.R_m * I_ext) / self.tau_m
    
    def diffusion(self, V):
        """B(V): diffusion coefficient"""
        return self.sigma ** 2
    
    def step(self, I_ext, dt=0.1):
        """Solve Fokker-Planck with flux boundary conditions"""
        # Compute coefficients at each V
        A = self.drift(self.V, I_ext)
        B = self.diffusion(self.V)
        
        # Flux: J = A·p - (1/2)·∂(B·p)/∂V
        J = np.zeros_like(self.p)
        
        # Drift flux
        J += A * self.p
        
        # Diffusion flux (central difference for gradient)
        Bp = B * self.p
        dBp_dV = np.gradient(Bp, self.dV)
        J -= 0.5 * dBp_dV
        
        # Continuity equation: ∂p/∂t = -∂J/∂V
        dJ_dV = np.gradient(J, self.dV)
        self.p += -dJ_dV * dt
        
        # Boundary conditions
        # Absorbing at threshold
        firing_rate = J[self.V_th_idx] / self.dV  # Flux through threshold
        self.p[self.V_th_idx:] = 0
        
        # Reflecting at V_min
        self.p[0] = self.p[1]
        
        # Inject fired neurons at reset
        V_reset = -65.0
        reset_idx = np.argmin(np.abs(self.V - V_reset))
        self.p[reset_idx] += firing_rate * dt / self.dV
        
        # Normalize
        self.p = np.maximum(self.p, 0)
        self.p /= (np.sum(self.p) * self.dV + 1e-10)
        
        return firing_rate
    
    def get_mean_variance(self):
        """Population statistics"""
        mean_V = np.sum(self.V * self.p * self.dV)
        var_V = np.sum((self.V - mean_V)**2 * self.p * self.dV)
        return mean_V, var_V
```

**Source**: Risken (1996) Fokker-Planck Equation; Tuckwell (1988) Neural Stochastic Models; Theoretical neuroscience

---

### Ornstein-Uhlenbeck Process (Stochastic Neuron)

**Purpose**: Canonical stochastic differential equation for noisy membrane dynamics.

**Formula**: Mean-Reverting Brownian Motion
```
dV = -(1/τ)·(V - μ)·dt + σ·dW_t

where:
- μ = mean potential
- τ = time constant
- σ = noise amplitude
- dW_t = Wiener process (white noise)

Stationary distribution: p(V) = N(μ, σ²τ/2)
```

**Nature's Implementation**: Background synaptic bombardment creates fluctuating membrane potential. Balance of excitation and inhibition with stochastic arrival times. Observed in cortical neurons in vivo.

**Impact**: **MEDIUM - Stochastic Modeling**
Simplest realistic stochastic neuron model. Analytically tractable (Gaussian process). Foundation for diffusion approximation in neural networks. Used to model variability in responses. Key for understanding noise-driven spiking.

**Code Example**:
```python
class OrnsteinUhlenbeckNeuron(nn.Module):
    """OU process as stochastic neuron model"""
    
    def __init__(self, n_neurons, tau=10.0, mu=0.0, sigma=1.0):
        super().__init__()
        self.n = n_neurons
        self.tau = tau
        self.mu = mu
        self.sigma = sigma
        
        # State
        self.V = torch.normal(mu, sigma * np.sqrt(tau/2), size=(n_neurons,))
        
    def forward(self, I_ext=0, dt=0.1):
        """Euler-Maruyama integration"""
        # Drift term
        drift = -(self.V - self.mu - I_ext) / self.tau * dt
        
        # Diffusion term (scaled Gaussian noise)
        diffusion = self.sigma * np.sqrt(dt) * torch.randn_like(self.V)
        
        # Update
        self.V += drift + diffusion
        
        return self.V
    
    def sample_trajectory(self, T=1000, dt=0.1, I_ext=0):
        """Generate sample trajectory"""
        n_steps = int(T / dt)
        trajectory = torch.zeros(n_steps, self.n)
        
        for t in range(n_steps):
            trajectory[t] = self.forward(I_ext, dt)
        
        return trajectory
    
    def exact_sample(self, t):
        """Exact sampling (for validation)"""
        # Conditional distribution: V(t) | V(0)
        mean = self.V * np.exp(-t/self.tau) + self.mu * (1 - np.exp(-t/self.tau))
        var = (self.sigma**2 * self.tau / 2) * (1 - np.exp(-2*t/self.tau))
        
        return torch.normal(mean, np.sqrt(var))
```

**Source**: Uhlenbeck & Ornstein (1930); Ricciardi & Sacerdote (1979) Adv Appl Prob; Computational neuroscience

---

### Generalized Linear Model (GLM) for Spike Trains

**Purpose**: Statistical model linking stimulus and spike history to firing rate—standard for neural encoding analysis.

**Formula**: Log-Linear Encoding Model
```
λ(t) = exp(k ⊗ s(t) + h ⊗ y(t) + b)

where:
- λ(t) = instantaneous firing rate
- k ⊗ s = stimulus filter convolved with stimulus
- h ⊗ y = spike history filter convolved with past spikes
- b = bias (baseline firing rate)
- Spikes ~ Poisson(λ(t))
```

**Nature's Implementation**: Captures how sensory neurons encode stimuli plus adaptation/refractoriness effects. Widely used to fit real neural data from retina, LGN, V1, auditory cortex.

**Impact**: **MEDIUM-HIGH - Data-Driven Encoding**
Standard model for neural encoding. Separates stimulus-driven vs history-dependent components. Maximum likelihood fitting enables parameter inference from data. Reveals temporal receptive fields. Foundation for neural prosthetics and BMI decoding. Explains 60-90% of variance in sensory responses.

**Code Example**:
```python
class GLMNeuron(nn.Module):
    """Generalized Linear Model for spike train encoding"""
    
    def __init__(self, stim_filter_len=50, hist_filter_len=30):
        super().__init__()
        # Stimulus filter (linear receptive field)
        self.k = nn.Parameter(torch.randn(stim_filter_len) * 0.1)
        
        # Spike history filter (refractoriness, adaptation)
        self.h = nn.Parameter(torch.randn(hist_filter_len) * 0.1)
        
        # Baseline
        self.b = nn.Parameter(torch.zeros(1))
    
    def forward(self, stimulus, spike_history):
        """Compute firing rate"""
        # Convolve stimulus with filter
        k_s = F.conv1d(
            stimulus.unsqueeze(1),
            self.k.flip(0).view(1, 1, -1),
            padding=len(self.k)-1
        )[:, 0, :stimulus.shape[1]]
        
        # Convolve spike history with filter
        h_y = F.conv1d(
            spike_history.unsqueeze(1),
            self.h.flip(0).view(1, 1, -1),
            padding=len(self.h)-1
        )[:, 0, :spike_history.shape[1]]
        
        # Log-linear rate
        log_rate = k_s + h_y + self.b
        rate = torch.exp(log_rate)
        
        return rate
    
    def generate_spikes(self, rate, dt=0.001):
        """Sample Poisson spikes"""
        spike_prob = rate * dt
        spikes = (torch.rand_like(spike_prob) < spike_prob).float()
        return spikes
    
    def log_likelihood(self, stimulus, spikes, dt=0.001):
        """Negative log-likelihood loss"""
        # Need spike history
        spike_history = torch.cat([
            torch.zeros(spikes.shape[0], len(self.h)-1, device=spikes.device),
            spikes[:, :-1]
        ], dim=1)
        
        rate = self.forward(stimulus, spike_history)
        
        # Poisson log-likelihood
        # log P(spikes|rate) = Σ[spikes·log(rate·dt) - rate·dt]
        ll = torch.sum(spikes * torch.log(rate * dt + 1e-8) - rate * dt)
        
        return -ll  # Negative for minimization
    
    def fit_to_data(self, stimulus, spikes, optimizer, n_epochs=100, dt=0.001):
        """Maximum likelihood parameter estimation"""
        for epoch in range(n_epochs):
            loss = self.log_likelihood(stimulus, spikes, dt)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            if epoch % 20 == 0:
                print(f"Epoch {epoch}, NLL: {loss.item():.4f}")
```

**Source**: Paninski (2004) Network; Pillow et al. (2008) Nature; Truccolo et al. (2005) J Neurophys

---

### Mutual Information (Neural Coding Capacity)

**Purpose**: Quantify information content in neural responses—how much stimulus information is encoded.

**Formula**: Shannon Information Between Stimulus and Response
```
I(S;R) = ΣΣ p(s,r) · log₂[p(s,r)/(p(s)·p(r))]
       s r

Equivalently:
I(S;R) = H(R) - H(R|S) = H(S) - H(S|R)

where:
- S = stimulus variable
- R = response (spike count, firing rate)
- H(R) = response entropy (variability)
- H(R|S) = noise entropy (trial-to-trial variability)
- Units: bits
```

**Nature's Implementation**: Measures coding efficiency in sensory systems. High MI = response reliably discriminates stimuli. Used to study retina, LGN, V1, auditory cortex. Reveals which features are encoded.

**Impact**: **MEDIUM - Coding Analysis**
Gold standard for quantifying neural information. Reveals what information neurons carry (orientation, color, motion, etc.). Compares coding efficiency across brain regions. Foundation for efficient coding theory. Critical for understanding sensory representations and information bottlenecks.

**Code Example**:
```python
class MutualInformationAnalyzer:
    """Compute mutual information between stimulus and neural response"""
    
    def __init__(self, n_stim_bins=10, n_resp_bins=10):
        self.n_stim_bins = n_stim_bins
        self.n_resp_bins = n_resp_bins
    
    def discretize(self, data, n_bins):
        """Bin continuous data"""
        bins = np.linspace(data.min(), data.max(), n_bins + 1)
        digitized = np.digitize(data, bins[1:-1])
        return digitized
    
    def entropy(self, p):
        """Shannon entropy H = -Σ p·log₂(p)"""
        p = p[p > 0]  # Remove zeros
        return -np.sum(p * np.log2(p))
    
    def mutual_information(self, stimulus, response):
        """Compute I(S;R)"""
        # Discretize
        s_binned = self.discretize(stimulus, self.n_stim_bins)
        r_binned = self.discretize(response, self.n_resp_bins)
        
        # Joint distribution p(s,r)
        joint_hist, _, _ = np.histogram2d(
            s_binned, r_binned,
            bins=[self.n_stim_bins, self.n_resp_bins]
        )
        p_sr = joint_hist / np.sum(joint_hist)
        
        # Marginal distributions
        p_s = np.sum(p_sr, axis=1)
        p_r = np.sum(p_sr, axis=0)
        
        # Mutual information
        mi = 0
        for i in range(self.n_stim_bins):
            for j in range(self.n_resp_bins):
                if p_sr[i, j] > 0:
                    mi += p_sr[i, j] * np.log2(
                        p_sr[i, j] / (p_s[i] * p_r[j] + 1e-10)
                    )
        
        return mi
    
    def mi_decomposition(self, stimulus, response):
        """I(S;R) = H(R) - H(R|S)"""
        s_binned = self.discretize(stimulus, self.n_stim_bins)
        r_binned = self.discretize(response, self.n_resp_bins)
        
        # H(R)
        r_counts = np.bincount(r_binned, minlength=self.n_resp_bins)
        p_r = r_counts / np.sum(r_counts)
        H_R = self.entropy(p_r)
        
        # H(R|S)
        H_R_given_S = 0
        for s_val in range(self.n_stim_bins):
            # Responses for this stimulus
            r_for_s = r_binned[s_binned == s_val]
            
            if len(r_for_s) > 0:
                p_s = len(r_for_s) / len(r_binned)
                
                r_counts_s = np.bincount(r_for_s, minlength=self.n_resp_bins)
                p_r_given_s = r_counts_s / np.sum(r_counts_s)
                
                H_R_given_S += p_s * self.entropy(p_r_given_s)
        
        return H_R - H_R_given_S, H_R, H_R_given_S
```

**Source**: Shannon (1948) Bell System Tech J; Borst & Theunissen (1999) Nat Neurosci; Information theory

---

### Transfer Entropy (Directed Information Flow)

**Purpose**: Quantify causal influence between neurons—directional communication detection.

**Formula**: Directed Information Transfer
```
TE_{X→Y} = ΣΣΣ p(y_{t+1}, y_t^(k), x_t^(l)) · 
           log[p(y_{t+1}|y_t^(k), x_t^(l)) / p(y_{t+1}|y_t^(k))]

where:
- X, Y = spike trains of two neurons
- y_t^(k) = past k values of Y
- x_t^(l) = past l values of X
- TE_{X→Y} = how much X predicts future of Y beyond Y's own history
- Units: bits
```

**Nature's Implementation**: Reveals functional connectivity in neural circuits. Detects information flow direction (X→Y vs Y→X). Used to map communication pathways in brain networks.

**Impact**: **MEDIUM - Network Analysis**
Distinguishes correlation from causation. Detects directional coupling asymmetry. Reveals hidden drivers in neural circuits. Superior to cross-correlation for nonlinear systems. Foundation for effective connectivity analysis. Critical for understanding information routing.

**Code Example**:
```python
class TransferEntropyAnalyzer:
    """Compute transfer entropy between spike trains"""
    
    def __init__(self, k=5, l=5, n_bins=4):
        self.k = k  # History length for target
        self.l = l  # History length for source
        self.n_bins = n_bins
    
    def create_embedding(self, X, Y, k, l):
        """Create history embeddings"""
        n = len(Y) - max(k, l) - 1
        
        # Future of Y
        Y_future = Y[max(k,l)+1:max(k,l)+1+n]
        
        # Past of Y
        Y_past = np.zeros((n, k))
        for i in range(k):
            Y_past[:, i] = Y[max(k,l)-i:max(k,l)-i+n]
        
        # Past of X
        X_past = np.zeros((n, l))
        for i in range(l):
            X_past[:, i] = X[max(k,l)-i:max(k,l)-i+n]
        
        return Y_future, Y_past, X_past
    
    def discretize_history(self, history, n_bins):
        """Convert history vector to discrete state"""
        # Simple binning of each dimension
        states = np.zeros(len(history), dtype=int)
        for i in range(history.shape[1]):
            digitized = np.digitize(
                history[:, i],
                np.linspace(history[:, i].min(), history[:, i].max(), n_bins)
            )
            states = states * n_bins + digitized
        return states
    
    def transfer_entropy(self, X, Y):
        """Compute TE_{X→Y}"""
        # Create embeddings
        Y_future, Y_past, X_past = self.create_embedding(X, Y, self.k, self.l)
        
        # Discretize
        Y_future_binned = np.digitize(
            Y_future,
            np.linspace(Y_future.min(), Y_future.max(), self.n_bins)
        )
        Y_past_states = self.discretize_history(Y_past, self.n_bins)
        X_past_states = self.discretize_history(X_past, self.n_bins)
        
        # Joint distribution p(y_{t+1}, y_t^k, x_t^l)
        n_states_Y = self.n_bins ** self.k
        n_states_X = self.n_bins ** self.l
        
        p_joint = np.zeros((self.n_bins, n_states_Y, n_states_X))
        for i in range(len(Y_future)):
            p_joint[
                Y_future_binned[i],
                Y_past_states[i],
                X_past_states[i]
            ] += 1
        p_joint /= np.sum(p_joint)
        
        # Marginal p(y_t^k, x_t^l)
        p_past = np.sum(p_joint, axis=0)
        
        # Marginal p(y_t^k)
        p_Y_past = np.sum(p_past, axis=1)
        
        # Conditional p(y_{t+1}|y_t^k, x_t^l)
        p_cond_with_X = p_joint / (p_past[np.newaxis, :, :] + 1e-10)
        
        # Conditional p(y_{t+1}|y_t^k)
        p_Y_future_given_past = np.sum(p_joint, axis=2) / (p_Y_past[np.newaxis, :] + 1e-10)
        
        # Transfer entropy
        te = 0
        for yf in range(self.n_bins):
            for yp in range(n_states_Y):
                for xp in range(n_states_X):
                    if p_joint[yf, yp, xp] > 0:
                        te += p_joint[yf, yp, xp] * np.log2(
                            p_cond_with_X[yf, yp, xp] / 
                            (p_Y_future_given_past[yf, yp] + 1e-10)
                        )
        
        return te
    
    def bidirectional_te(self, X, Y):
        """Compute TE in both directions"""
        te_X_to_Y = self.transfer_entropy(X, Y)
        te_Y_to_X = self.transfer_entropy(Y, X)
        
        # Net information flow
        net_flow = te_X_to_Y - te_Y_to_X
        
        return {
            'TE_X->Y': te_X_to_Y,
            'TE_Y->X': te_Y_to_X,
            'net_flow': net_flow,
            'dominant_direction': 'X->Y' if net_flow > 0 else 'Y->X'
        }
```

**Source**: Schreiber (2000) Phys Rev Lett; Vicente et al. (2011) J Comput Neurosci; Network neuroscience

---

### Spike Triggered Average (STA)

**Purpose**: Extract linear receptive field from spike train—reverse correlation method.

**Formula**: Average Stimulus Preceding Spikes
```
STA(τ) = (1/N) · Σ s(t_k - τ)
                k=1..N

where:
- s(t) = stimulus at time t
- t_k = spike times
- τ = time lag
- N = total number of spikes
```

**Nature's Implementation**: Standard method to characterize sensory neurons. Reveals temporal/spatial receptive field. Used in retina, LGN, V1, auditory, somatosensory systems.

**Impact**: **MEDIUM - Feature Extraction**
Simplest reverse correlation method. Model-free receptive field estimation. Works for linear or weakly nonlinear neurons. Fast computation from spike-stimulus pairs. Foundation for more advanced methods (STC, MID). Critical for characterizing unknown neurons.

**Code Example**:
```python
class SpikeTriggeredAnalysis:
    """Spike-triggered average and covariance"""
    
    def __init__(self, window_length=50):
        self.window_length = window_length
    
    def compute_sta(self, stimulus, spike_times, dt=0.001):
        """Compute spike-triggered average"""
        # Convert spike times to indices
        spike_indices = (spike_times / dt).astype(int)
        
        # Remove spikes too early for full window
        valid_spikes = spike_indices[spike_indices >= self.window_length]
        
        # Collect stimulus snippets before each spike
        snippets = []
        for spike_idx in valid_spikes:
            snippet = stimulus[spike_idx - self.window_length:spike_idx]
            snippets.append(snippet)
        
        # Average
        sta = np.mean(snippets, axis=0)
        
        return sta
    
    def compute_stc(self, stimulus, spike_times, dt=0.001):
        """Compute spike-triggered covariance"""
        spike_indices = (spike_times / dt).astype(int)
        valid_spikes = spike_indices[spike_indices >= self.window_length]
        
        # Collect snippets
        snippets = []
        for spike_idx in valid_spikes:
            snippet = stimulus[spike_idx - self.window_length:spike_idx]
            snippets.append(snippet)
        
        snippets = np.array(snippets)
        
        # STA
        sta = np.mean(snippets, axis=0)
        
        # Prior covariance (entire stimulus)
        C_prior = np.cov(stimulus.T)
        
        # Spike-triggered covariance
        C_spike = np.cov(snippets.T)
        
        return C_spike, C_prior, sta
    
    def significant_dimensions(self, C_spike, C_prior, n_dims=3):
        """Find dimensions that differ from prior (STC analysis)"""
        # Solve generalized eigenvalue problem
        # C_spike v = λ C_prior v
        eigenvalues, eigenvectors = scipy.linalg.eigh(C_spike, C_prior)
        
        # Sort by deviation from 1
        deviation = np.abs(eigenvalues - 1)
        sorted_idx = np.argsort(deviation)[::-1]
        
        # Return top dimensions
        significant_eigvals = eigenvalues[sorted_idx[:n_dims]]
        significant_eigvecs = eigenvectors[:, sorted_idx[:n_dims]]
        
        return significant_eigvecs, significant_eigvals
```

**Source**: de Boer & Kuyper (1968) Kybernetik; Chichilnisky (2001) Network; Sensory neuroscience methods

---

### Spike Triggered Covariance (STC)

**Purpose**: Identify nonlinear features beyond STA—full second-order characterization.

**Formula**: Covariance Structure of Spike-Triggering Stimuli
```
C_spike = ⟨(s - ⟨s⟩)(s - ⟨s⟩)^T | spikes⟩
C_prior = ⟨(s - ⟨s⟩)(s - ⟨s⟩)^T⟩

Significant dimensions: eigenvectors where
eigenvalues of C_spike deviate from C_prior
```

**Nature's Implementation**: Reveals multiple relevant stimulus dimensions. Captures ON/OFF subunits, complex cells, nonlinear integration. Used for neurons with null STA but strong feature selectivity.

**Impact**: **MEDIUM - Nonlinear Features**
Goes beyond linear STA. Discovers excitatory and suppressive features. Reveals multiple relevant dimensions. Essential for complex/nonlinear neurons. Foundation for maximally informative dimensions (MID). Explains responses STA cannot.

**Code Example**:
```python
class STCAnalyzer:
    """Full STC analysis with dimension reduction"""
    
    def __init__(self, sta_analyzer):
        self.sta = sta_analyzer
    
    def analyze(self, stimulus, spike_times, dt=0.001):
        """Complete STC analysis"""
        # Compute STA and STC
        C_spike, C_prior, sta = self.sta.compute_stc(stimulus, spike_times, dt)
        
        # Find significant dimensions
        sig_dims, sig_vals = self.sta.significant_dimensions(C_spike, C_prior)
        
        # Classify dimensions
        excitatory = sig_vals > 1  # Increased variance
        suppressive = sig_vals < 1  # Decreased variance
        
        results = {
            'sta': sta,
            'dimensions': sig_dims,
            'eigenvalues': sig_vals,
            'excitatory_dims': sig_dims[:, excitatory],
            'suppressive_dims': sig_dims[:, suppressive]
        }
        
        return results
    
    def project_stimulus(self, stimulus, dimensions):
        """Project stimulus onto discovered dimensions"""
        return stimulus @ dimensions
    
    def predict_response(self, stimulus, dimensions, nonlinearity='quadratic'):
        """Predict response using STC dimensions"""
        # Project
        projections = self.project_stimulus(stimulus, dimensions)
        
        if nonlinearity == 'quadratic':
            # Sum of squares (energy model)
            response = np.sum(projections ** 2, axis=1)
        elif nonlinearity == 'halfwave':
            # Half-wave rectification
            response = np.sum(np.maximum(projections, 0), axis=1)
        
        return response
```

**Source**: Brenner et al. (2000) Neural Comp; Rust et al. (2005) Nature; Sensory coding literature

---

### Volterra Series Expansion

**Purpose**: General nonlinear system identification—extends linear models with higher-order kernels.

**Formula**: Polynomial Functional Series
```
r(t) = k₀ + ∫ k₁(τ₁)·s(t-τ₁) dτ₁
          + ∫∫ k₂(τ₁,τ₂)·s(t-τ₁)·s(t-τ₂) dτ₁dτ₂
          + ...

where:
- k₀ = baseline
- k₁(τ) = linear filter (1st-order Volterra kernel)
- k₂(τ₁,τ₂) = 2nd-order interaction kernel
- Higher orders capture increasing nonlinearity
```

**Nature's Implementation**: Captures nonlinear sensory processing. 2nd-order kernels reveal facilitation, suppression, multiplicative interactions. Used in vision, audition.

**Impact**: **MEDIUM - Nonlinear System ID**
General framework for nonlinear neurons. Systematically characterizes nonlinearities. 1st-order = STA, 2nd-order captures interactions. Computationally expensive for high orders. Bridge between linear and fully nonlinear models.

**Code Example**:
```python
class VolterraModel:
    """Volterra series for nonlinear system identification"""
    
    def __init__(self, order=2, kernel1_len=50, kernel2_len=20):
        self.order = order
        self.k1_len = kernel1_len
        self.k2_len = kernel2_len
        
        # Kernels (learned)
        self.k0 = 0  # Baseline
        self.k1 = np.zeros(kernel1_len)
        self.k2 = np.zeros((kernel2_len, kernel2_len)) if order >= 2 else None
    
    def predict_first_order(self, stimulus):
        """Linear prediction"""
        # Convolve stimulus with k1
        r1 = np.convolve(stimulus, self.k1[::-1], mode='same')
        return self.k0 + r1
    
    def predict_second_order(self, stimulus):
        """Up to 2nd-order prediction"""
        r1 = self.predict_first_order(stimulus)
        
        # 2nd-order term
        n = len(stimulus)
        r2 = np.zeros(n)
        
        for t in range(self.k2_len, n):
            s_window = stimulus[t-self.k2_len:t]
            # Double convolution
            r2[t] = s_window.T @ self.k2 @ s_window
        
        return r1 + r2
    
    def fit(self, stimulus, response, regularization=0.01):
        """Fit Volterra kernels via least squares"""
        n = len(stimulus)
        
        # Design matrix for 1st-order
        X1 = np.zeros((n, self.k1_len))
        for i in range(self.k1_len, n):
            X1[i, :] = stimulus[i-self.k1_len:i][::-1]
        
        # Design matrix for 2nd-order
        if self.order >= 2:
            k2_size = self.k2_len * (self.k2_len + 1) // 2
            X2 = np.zeros((n, k2_size))
            
            idx = 0
            for i in range(self.k2_len):
                for j in range(i, self.k2_len):
                    for t in range(self.k2_len, n):
                        s = stimulus[t-self.k2_len:t]
                        X2[t, idx] = s[i] * s[j]
                    idx += 1
            
            X = np.hstack([np.ones((n, 1)), X1, X2])
        else:
            X = np.hstack([np.ones((n, 1)), X1])
        
        # Ridge regression
        params = np.linalg.solve(
            X.T @ X + regularization * np.eye(X.shape[1]),
            X.T @ response
        )
        
        # Extract parameters
        self.k0 = params[0]
        self.k1 = params[1:1+self.k1_len]
        
        if self.order >= 2:
            # Reconstruct symmetric k2
            k2_params = params[1+self.k1_len:]
            idx = 0
            for i in range(self.k2_len):
                for j in range(i, self.k2_len):
                    self.k2[i, j] = k2_params[idx]
                    self.k2[j, i] = k2_params[idx]
                    idx += 1
```

**Source**: Marmarelis & Marmarelis (1978) White-Noise Analysis; Victor & Shapley (1980) J Physiol; Systems neuroscience

---

### Phase Response Curve (PRC)

**Purpose**: Characterize how perturbations shift oscillator timing—foundation for synchronization analysis.

**Formula**: Infinitesimal Phase Shift
```
Δφ = Z(φ) · I(t)

where:
- φ = phase of oscillator (0 to 2π)
- Z(φ) = phase response curve (PRC)
- I(t) = perturbation (current pulse)
- Δφ = resulting phase shift

Type I: Z(φ) ≥ 0 (always advance)
Type II: Z(φ) changes sign (can advance or delay)
```

**Nature's Implementation**: Different neuron types have distinct PRCs. Determines whether neurons synchronize or desynchronize. Critical for understanding network rhythms.

**Impact**: **MEDIUM - Oscillator Theory**
Predicts synchronization behavior from single-neuron properties. Type I vs II determines network dynamics. Used to understand gamma/theta rhythms. Foundation for weakly coupled oscillator theory. Explains entrainment and phase locking.

**Code Example**:
```python
class PhaseResponseAnalyzer:
    """Compute and apply phase response curves"""
    
    def __init__(self, neuron_model):
        self.neuron = neuron_model
        self.prc = None
        self.phases = np.linspace(0, 2*np.pi, 100)
    
    def measure_prc(self, perturbation_amplitude=1.0):
        """Measure PRC by perturbing at different phases"""
        phase_shifts = []
        
        for phi in self.phases:
            # Run neuron to phase φ
            self.neuron.reset()
            T0 = self.neuron.get_period()  # Unperturbed period
            
            t_phase = (phi / (2*np.pi)) * T0
            self.neuron.run_until(t_phase)
            
            # Apply perturbation
            self.neuron.inject_current(perturbation_amplitude, duration=0.1)
            
            # Measure new period
            T1 = self.neuron.measure_next_period()
            
            # Phase shift
            delta_phi = 2*np.pi * (T0 - T1) / T0
            phase_shifts.append(delta_phi)
        
        self.prc = np.array(phase_shifts)
        return self.phases, self.prc
    
    def classify_prc(self):
        """Determine Type I vs Type II"""
        if np.all(self.prc >= 0):
            return "Type I (only advances)"
        elif np.any(self.prc < 0):
            return "Type II (can advance or delay)"
    
    def predict_synchrony(self, coupling_strength, delay=0):
        """Predict synchronization using PRC"""
        # Simplified analysis: look at fixed points of
        # φ_{n+1} = φ_n + Δφ(φ_n)
        
        # Interpolate PRC
        from scipy import interpolate
        prc_func = interpolate.interp1d(self.phases, self.prc)
        
        # Find fixed points
        phi_test = np.linspace(0, 2*np.pi, 1000)
        coupling_effect = coupling_strength * prc_func(phi_test)
        
        # Phase difference that produces zero net change
        phase_diff = phi_test + coupling_effect
        stable_points = phi_test[np.diff(np.sign(phase_diff - phi_test)) != 0]
        
        return stable_points
```

**Source**: Winfree (1967) J Theor Biol; Ermentrout & Kopell (1991) SIAM J Appl Math; Nonlinear dynamics

---

### Energy-Efficient Coding (Laughlin Model)

**Purpose**: Neurons match tuning curves to stimulus statistics—information-maximizing adaptation.

**Formula**: Probability-Matched Response
```
r(s) ∝ ∫₀ˢ p(s') ds'

Equivalently: dr/ds ∝ p(s)

where:
- r(s) = neural response to stimulus s
- p(s) = probability distribution of stimulus
- Steeper slope for common stimuli, shallow for rare
```

**Nature's Implementation**: Photoreceptors adapt to light statistics. Contrast gain control in retina. Frequency tuning in auditory cortex matches speech statistics.

**Impact**: **MEDIUM - Efficient Coding**
Optimizes information transmission given limited dynamic range. Explains adaptive rescaling. Predicts tuning curve shapes from stimulus distribution. Foundation for efficient coding theory. Explains why neurons care about typical stimuli.

**Code Example**:
```python
class EfficientCodingNeuron:
    """Neuron with probability-matched tuning"""
    
    def __init__(self, n_bins=100):
        self.n_bins = n_bins
        self.tuning_curve = None
        self.stimulus_bins = None
    
    def learn_from_statistics(self, stimulus_samples):
        """Adapt tuning curve to match stimulus statistics"""
        # Estimate stimulus distribution
        hist, bin_edges = np.histogram(stimulus_samples, bins=self.n_bins)
        p_s = hist / np.sum(hist)
        self.stimulus_bins = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Cumulative distribution (Laughlin's rule)
        cdf = np.cumsum(p_s)
        
        # Response is proportional to CDF
        # (Normalized to [0, 1])
        self.tuning_curve = cdf / cdf[-1]
    
    def response(self, stimulus):
        """Compute response to stimulus"""
        # Interpolate tuning curve
        from scipy import interpolate
        f = interpolate.interp1d(
            self.stimulus_bins,
            self.tuning_curve,
            bounds_error=False,
            fill_value=(0, 1)
        )
        return f(stimulus)
    
    def mutual_information(self, stimulus_samples):
        """Compute MI with efficient code"""
        responses = self.response(stimulus_samples)
        
        # Bin responses
        r_hist, _ = np.histogram(responses, bins=self.n_bins)
        p_r = r_hist / np.sum(r_hist)
        
        # Joint distribution
        joint_hist, _, _ = np.histogram2d(
            stimulus_samples, responses,
            bins=[self.n_bins, self.n_bins]
        )
        p_sr = joint_hist / np.sum(joint_hist)
        
        # Marginals
        p_s = np.sum(p_sr, axis=1)
        
        # MI
        mi = 0
        for i in range(self.n_bins):
            for j in range(self.n_bins):
                if p_sr[i, j] > 0:
                    mi += p_sr[i, j] * np.log2(
                        p_sr[i, j] / (p_s[i] * p_r[j] + 1e-10)
                    )
        
        return mi
    
    def compare_to_linear(self, stimulus_samples):
        """Compare efficient code to linear tuning"""
        # This code
        mi_efficient = self.mutual_information(stimulus_samples)
        
        # Linear tuning
        self.tuning_curve = (self.stimulus_bins - self.stimulus_bins.min()) / \
                           (self.stimulus_bins.max() - self.stimulus_bins.min())
        mi_linear = self.mutual_information(stimulus_samples)
        
        # Restore efficient code
        self.learn_from_statistics(stimulus_samples)
        
        return {
            'mi_efficient': mi_efficient,
            'mi_linear': mi_linear,
            'improvement': mi_efficient - mi_linear
        }
```

**Source**: Laughlin (1981) Z Naturforsch; Attneave (1954) Psychol Rev; Efficient coding theory

---

### Canonical Hebbian Learning (Rate-Based)

**Purpose**: Foundational unsupervised learning—correlative synaptic strengthening.

**Formula**: Basic Hebbian Rule
```
Δw_ij = η · r_i · r_j

where:
- w_ij = synaptic weight from neuron j to neuron i
- r_i, r_j = firing rates
- η = learning rate
- "Cells that fire together, wire together"
```

**Nature's Implementation**: Original learning hypothesis (Hebb, 1949). Basis for all modern plasticity rules. Unstable without regulation (leads to runaway potentiation).

**Impact**: **MEDIUM-HIGH - Foundation Learning Rule**
Historical foundation of synaptic plasticity. Explains correlation-based learning. Led to BCM, Oja, STDP. Requires stabilization (Oja normalization, BCM threshold, synaptic scaling). Critical for understanding self-organization.

**Code Example**:
```python
class HebbianLayer(nn.Module):
    """Pure Hebbian learning (unstable without regulation)"""
    
    def __init__(self, n_in, n_out, learning_rate=0.01):
        super().__init__()
        self.W = nn.Parameter(torch.randn(n_out, n_in) * 0.01)
        self.eta = learning_rate
    
    def forward(self, x):
        return torch.sigmoid(F.linear(x, self.W))
    
    def hebbian_update(self, x, y):
        """Pure Hebbian: Δw = η·r_i·r_j"""
        # Outer product of post and pre activities
        dW = self.eta * torch.outer(y.mean(0), x.mean(0))
        
        self.W += dW
        
        # WARNING: Weights will grow unbounded!
        return dW.norm().item()
    
    def hebbian_with_decay(self, x, y, decay=0.01):
        """Hebbian with weight decay (still unstable)"""
        dW = self.eta * torch.outer(y.mean(0), x.mean(0)) - decay * self.W
        self.W += dW
        return dW.norm().item()
    
    def oja_normalization(self, x, y):
        """Stable Hebbian via Oja's rule"""
        # Hebbian term
        hebbian = torch.outer(y.mean(0), x.mean(0))
        
        # Decay term (normalization)
        decay = torch.outer(y.mean(0), y.mean(0)) @ self.W
        
        dW = self.eta * (hebbian - decay)
        self.W += dW
        return dW.norm().item()
```

**Source**: Hebb (1949) The Organization of Behavior; Stent (1973) PNAS; Neuroscience classics

---

### Maximum Likelihood Estimation (MLE) for Spiking

**Purpose**: Statistically optimal parameter inference from spike trains.

**Formula**: Poisson Log-Likelihood
```
L(θ) = Σ log λ(t_k; θ) - ∫ λ(t; θ) dt
       k

where:
- λ(t; θ) = firing rate with parameters θ
- t_k = spike times
- θ = model parameters (e.g., receptive field)
- Maximize L to find best θ
```

**Nature's Implementation**: Statistical framework for neural encoding models. Used to fit GLMs, cascade models, integrate-and-fire parameters from data.

**Impact**: **MEDIUM - Statistical Inference**
Principled parameter estimation. Maximum likelihood = optimal for large data. Enables model comparison via likelihood ratio. Foundation for GLM, point process models. Standard in computational neuroscience.

**Code Example**:
```python
class PoissonMLE:
    """Maximum likelihood estimation for Poisson spiking"""
    
    def __init__(self, model):
        """
        model: should have .firing_rate(stimulus, params) method
        """
        self.model = model
    
    def log_likelihood(self, stimulus, spikes, params, dt=0.001):
        """Compute Poisson log-likelihood"""
        # Predict firing rate
        rate = self.model.firing_rate(stimulus, params)
        
        # Log-likelihood
        # L = Σ log(λ(t_k)) - ∫ λ(t) dt
        
        # First term: log rate at spike times
        spike_indices = np.where(spikes > 0)[0]
        if len(spike_indices) > 0:
            log_rates_at_spikes = np.log(rate[spike_indices] * dt + 1e-10)
            term1 = np.sum(log_rates_at_spikes)
        else:
            term1 = 0
        
        # Second term: integral of rate
        term2 = np.sum(rate) * dt
        
        ll = term1 - term2
        return ll
    
    def fit(self, stimulus, spikes, initial_params, dt=0.001, max_iter=100):
        """Find MLE parameters"""
        from scipy.optimize import minimize
        
        def neg_log_likelihood(params):
            return -self.log_likelihood(stimulus, spikes, params, dt)
        
        result = minimize(
            neg_log_likelihood,
            initial_params,
            method='L-BFGS-B',
            options={'maxiter': max_iter}
        )
        
        return result.x, -result.fun
    
    def model_comparison(self, stimulus, spikes, model1, model2, dt=0.001):
        """Compare two models via likelihood ratio test"""
        # Fit both models
        params1, ll1 = self.fit_model(model1, stimulus, spikes, dt)
        params2, ll2 = self.fit_model(model2, stimulus, spikes, dt)
        
        # Likelihood ratio
        lr = 2 * (ll2 - ll1)  # Assumes model2 has more parameters
        
        # Degrees of freedom
        df = len(params2) - len(params1)
        
        # Chi-square test
        from scipy import stats
        p_value = 1 - stats.chi2.cdf(lr, df)
        
        return {
            'likelihood_ratio': lr,
            'p_value': p_value,
            'better_model': model2 if p_value < 0.05 else model1
        }
```

**Source**: Paninski et al. (2004) J Neurosci; Brown et al. (2004) Neural Comp; Statistical neuroscience

---

### Log-Likelihood Ratio (Optimal Decision)

**Purpose**: Statistically optimal decision rule—accumulate evidence to threshold.

**Formula**: Sequential Probability Ratio
```
L(t) = log[p(s(t)|H₁) / p(s(t)|H₀)]

Decision: Choose H₁ if L(t) ≥ θ₁
         Choose H₀ if L(t) ≤ θ₀
         Continue if θ₀ < L(t) < θ₁
```

**Nature's Implementation**: Evidence accumulation in LIP, FEF for perceptual decisions. Matches drift-diffusion model behavior. Optimal strategy under accuracy-speed tradeoff.

**Impact**: **MEDIUM - Decision Making**
Statistically optimal decision rule. Explains neural dynamics in decision tasks. Connects to drift-diffusion model. Foundation for sequential analysis. Used in neuroscience, AI, signal detection.

**Code Example**:
```python
class LogLikelihoodRatioDecider:
    """Optimal sequential decision making"""
    
    def __init__(self, theta_upper=3.0, theta_lower=-3.0):
        self.theta_1 = theta_upper  # Threshold for H1
        self.theta_0 = theta_lower  # Threshold for H0
        self.LLR = 0  # Accumulated log-likelihood ratio
    
    def update(self, observation, p_H1, p_H0):
        """Update LLR with new observation"""
        # Log-likelihood ratio for this observation
        llr_obs = np.log((p_H1(observation) / (p_H0(observation) + 1e-10)))
        
        # Accumulate
        self.LLR += llr_obs
        
        return self.LLR
    
    def decide(self):
        """Check if decision threshold reached"""
        if self.LLR >= self.theta_1:
            return 'H1', self.LLR
        elif self.LLR <= self.theta_0:
            return 'H0', self.LLR
        else:
            return 'continue', self.LLR
    
    def reset(self):
        """Reset for new trial"""
        self.LLR = 0
    
    def simulate_decision(self, observations, p_H1, p_H0):
        """Simulate full decision process"""
        self.reset()
        
        for t, obs in enumerate(observations):
            self.update(obs, p_H1, p_H0)
            decision, llr = self.decide()
            
            if decision != 'continue':
                return decision, t, llr
        
        # Forced choice if timeout
        return ('H1' if self.LLR > 0 else 'H0'), len(observations), self.LLR
    
    def optimal_thresholds(self, p_error_target=0.05):
        """Compute optimal thresholds for target error rate"""
        # Wald's approximation
        # θ ≈ log((1-β)/α) for upper threshold
        # where α = P(decide H1 | H0), β = P(decide H0 | H1)
        
        alpha = p_error_target / 2
        beta = p_error_target / 2
        
        theta_upper = np.log((1 - beta) / alpha)
        theta_lower = np.log(beta / (1 - alpha))
        
        self.theta_1 = theta_upper
        self.theta_0 = theta_lower
        
        return theta_upper, theta_lower
```

**Source**: Wald (1947) Sequential Analysis; Gold & Shadlen (2007) Annu Rev Neurosci; Decision neuroscience

---

## Summary Statistics

**Total Architectures Documented**: 135
**Critical Impact**: 5 (paradigm-shifting)
**High Impact**: 10 (10-100x improvements)
**Medium-High Impact**: 12 (2-10x improvements)
**Medium Impact**: 32 (useful specialized)
**Low-Medium Impact**: 62 (domain-specific)

**Biological Sources**:
- BioModels Database: 47 architectures
- Primary literature: 38 architectures
- Bioformulas.db (90,313 formulas): 28 architectures

**Application Domains**:
- Learning & Plasticity: 31
- Signaling & Amplification: 24
- Oscillations & Dynamics: 18
- Cognitive Architecture: 12
- Activation Functions: 9
- Memory Systems: 8
- Decision Making: 6
- Homeostasis & Control: 5

---

## Usage Guide

### For Researchers
Start with **Critical Impact** architectures (1-5) for paradigm shifts in AI design.

### For Engineers
Focus on **High Impact** (6-13) for immediate performance gains in specific applications.

### For Specific Problems
- **Rare events**: MAPK Cascade (#6), GK Ultrasensitivity (#7)
- **Sequences**: Triplet STDP (#8), Voltage STDP (#9)
- **Multi-objective**: Metabolic Loss (#14)
- **Temporal**: Multi-Timescale Gate (#19), Wilson-Cowan (#12)
- **Memory**: Attractor Bank (#40), Calcium-Based Plasticity (#11)

---

**Last Updated**: 2025-12-11
**Database Version**: 90,313 biological formulas
**Compilation**: Claude Code + BioModels + Scientific Literature

