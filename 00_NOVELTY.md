# Novel Biological AI Architectures - Complete Catalog

**Compiled**: 2025-12-11
**Total Architectures**: 113+
**Organization**: Ordered by AI Impact (Highest → Lowest)

---

## CRITICAL IMPACT (Paradigm-Shifting Architectures)

These architectures fundamentally change how AI systems are designed and operated.

---

### 1. Mechanism-Driven Architecture (MDA)

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

### 2. Self-Learning Brain (Gene Expression Meta-Layer)

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

### 3. Predictive Coding Hierarchy

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

### 4. Global Workspace Theory (Conscious AI)

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

### 5. Multi-Compartment Dendritic Neurons

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

### 6. MAPK Amplifying Cascade

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

### 7. Goldbeter-Koshland Ultrasensitivity

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

### 8. Triplet STDP (Sequence Learning)

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

### 9. Voltage-Dependent STDP (Clopath Rule)

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

### 10. Dopamine-Modulated STDP (Reward Learning)

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

### 11. Calcium-Based Plasticity (Shouval Model)

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

### 12. Wilson-Cowan E-I Dynamics

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

### 13. Kuramoto Synchronization

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

### 14. Metabolic Loss Function (65 Objectives)

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

### 15. Hill Activation (Adaptive Cooperativity)

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

### 16. Michaelis-Menten Activation

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

### 17. Energy-Aware Neurons (ATP Budgeting)

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

### 18. Dual-Channel Neurons (Fast + Slow)

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

### 19. Multi-Timescale Gate

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

### 20. Synaptic Convolution (Dual-Exponential Kernels)

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

### 21. Leaky Residual Block (LIF-Inspired)

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

### 22. BCM Learning Rule (Sliding Threshold)

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

### 23. Oja's Rule (Automatic PCA)

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

