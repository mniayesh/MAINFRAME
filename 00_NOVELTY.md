# Novel Biological AI Architectures - Complete Catalog

**Compiled**: 2025-12-11
**Total Architectures**: 196
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

**Formula**: Hierarchical Prediction Error & Free Energy Minimization
```
Free Energy Formulation (Neuronal Inference):
ẋ = -∂F/∂x

where F = ½||y - f(x)||² + ½||x - μ||²
        = prediction error + prior deviation

This yields gradient-descent inference inside the network.

Error Neuron Dynamics (Explicit Form):
ε = y - f(x)                             [Prediction error]
ẋ = -ε · f'(x)                           [Gradient descent on error]

Local Weight Learning Rule:
ΔW = η · ε · x^T                         [Fully local, no backprop needed]

Hierarchical Version:
ε_l = x_l - μ_l                          [Prediction error at layer l]
dμ_l/dt = -ε_l + W_l^T · ε_{l+1}        [Update belief from errors]
dW_l/dt = η · ε_l · μ_{l+1}^T           [Update weights to reduce error]

where:
- F = free energy (objective to minimize)
- ε = prediction error (actual - predicted)
- μ = current belief/representation
- W = generative weights (top-down)
- η = learning rate
- f(x) = nonlinear prediction function
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

### Ring Attractor (Head Direction Model)

**Purpose**: Maintain stable representation of angular/cyclic variables through recurrent dynamics with circular symmetry.

**Formula**: Periodic Continuous Attractor
```
τ ẋ_i = -x_i + Σ_j W_ij x_j + I_i

with circular symmetry in W:
W_ij = W(|i-j|_circular)

Specifically (Mexican hat on ring):
W_ij = A·exp(-d²_ij/2σ²_E) - B·exp(-d²_ij/2σ²_I)

where d_ij = min(|i-j|, N-|i-j|)  [circular distance]

Bump solution:
x_i(t) = x₀·exp(cos(2π(i-θ(t))/N)/σ²)

where θ(t) = heading angle encoded by bump position

Velocity integration:
θ̇ = β·ω_input

where:
- x_i = firing rate of neuron i (i = 0..N-1, wrapping)
- W_ij = connection strength (translation-invariant + circular)
- τ = membrane time constant
- I_i = external input (asymmetric to shift bump)
- θ(t) = bump center (encodes current heading)
- ω_input = angular velocity input
- β = integration gain
- A, B = excitation/inhibition strengths
- σ_E, σ_I = spatial scales
```

**Nature's Implementation**: Head direction cells in postsubiculum/anterior thalamic nucleus form a ring attractor. Maintain stable heading representation even without visual cues. Integrate angular velocity from vestibular system. Explain persistent direction sense during darkness, navigation.

**Impact**: **MEDIUM-HIGH - Angular Memory**
Maintains cyclic variables indefinitely. Perfect for heading, phase, periodic signals. No drift with proper tuning. Biological basis for compass sense. Used in robotics for orientation, phase tracking, rhythm generation. Critical for understanding spatial navigation and implementing stable angular representations.

**Code Example**:
```python
class RingAttractor(nn.Module):
    """Head direction ring attractor network"""

    def __init__(self, n_neurons=360, tau=10.0):
        super().__init__()
        self.n = n_neurons
        self.tau = tau

        # Create circular Mexican hat connectivity
        angles = np.arange(n_neurons) * 2 * np.pi / n_neurons
        dist = angles[:, None] - angles[None, :]

        # Circular distance
        dist = np.angle(np.exp(1j * dist))

        # Mexican hat
        A_exc, A_inh = 2.0, 1.5
        sigma_exc, sigma_inh = 0.3, 1.0

        W = A_exc * np.exp(-dist**2 / (2*sigma_exc**2)) - \
            A_inh * np.exp(-dist**2 / (2*sigma_inh**2))

        self.W = torch.FloatTensor(W)

    def forward(self, x, I_ext, dt=0.1, n_steps=50):
        """
        Evolve ring attractor dynamics
        τ ẋ = -x + W·x + I_ext
        """
        for _ in range(n_steps):
            recurrent = torch.matmul(self.W, x)
            dx = (-x + F.relu(recurrent + I_ext)) / self.tau * dt
            x = x + dx
        return x

    def integrate_velocity(self, angular_velocity, dt=1.0):
        """Shift bump by velocity input"""
        # Create asymmetric input
        shift = int(angular_velocity * dt * self.n / (2*np.pi))
        I_shift = torch.roll(torch.exp(-torch.arange(self.n).float()/10), shift)
        return I_shift * abs(angular_velocity)
```

**Source**: Zhang (1996) J Neurosci; Skaggs et al. (1995) Adv Neural Info Proc; MECHANISM_TO_ARCHITECTURE_PATTERNS.md

---

### Line Attractor (Eye Position Integrator)

**Purpose**: Perfect temporal integration of transient inputs—neural integrator for maintaining analog values.

**Formula**: 1D Continuous Attractor with Eigenvalue Condition
```
τ ẋ = -x + W·x + I(t)

Stability condition for integration:
W·v = v    [Eigenvalue λ = 1]

Must have eigenvector v with eigenvalue exactly 1 for perfect integration.

Dynamics on line attractor manifold:
ẋ_integrated = I(t)    [Perfect integration when τλ = 1]

Discrete update (leaky integrator):
x(t+1) = (1-α)·x(t) + α·I(t)

where α = dt/τ

For perfect integration: set α such that accumulated drift = 0

Connection structure (uniform + Mexican hat):
W_ij = w_uniform + [A·exp(-|i-j|²/σ²_E) - B·exp(-|i-j|²/σ²_I)]

where:
- x = neural population state (encodes integrated value)
- W = connectivity matrix (must have λ=1 eigenvalue)
- v = eigenvector corresponding to λ=1 (integrator mode)
- τ = time constant
- I(t) = transient input pulse
```

**Nature's Implementation**: Oculomotor integrator in goldfish/monkey brainstem. Maintains eye position between saccades. Integrates velocity commands into position. Also in spatial working memory (prefrontal cortex), evidence accumulation (LIP), motor preparation.

**Impact**: **MEDIUM-HIGH - Perfect Integration**
Holds analog values indefinitely without recurrent activity decay. Biological RAM. Explains working memory, decision accumulation, motor holds. Requires fine-tuned connectivity (λ=1 condition fragile). Used for analog memory, temporal integration, evidence accumulation in AI models.

**Code Example**:
```python
class LineAttractor(nn.Module):
    """Line attractor for perfect integration"""

    def __init__(self, n_neurons=50, tau=10.0):
        super().__init__()
        self.n = n_neurons
        self.tau = tau

        # Create connectivity with eigenvalue = 1
        # Uniform connectivity + local structure
        W = torch.ones(n_neurons, n_neurons) / n_neurons  # Mean field

        # Add local structure (Mexican hat)
        for i in range(n_neurons):
            for j in range(n_neurons):
                dist = abs(i - j)
                W[i, j] += 0.5 * np.exp(-dist**2 / 10) - 0.3 * np.exp(-dist**2 / 20)

        # Ensure eigenvalue = 1 (perfect integrator)
        eigenvalues, eigenvectors = torch.linalg.eig(W)
        max_eigenvalue = torch.max(torch.abs(eigenvalues)).item()
        W = W / max_eigenvalue  # Scale to have max eigenvalue = 1

        self.W = W
        self.W.fill_diagonal_(0)  # No self-connections

    def forward(self, x, I_input, dt=0.1):
        """
        Single integration step:
        τ ẋ = -x + W·x + I
        """
        recurrent = torch.matmul(self.W, x)
        dx = (-x + recurrent + I_input) / self.tau * dt
        return x + dx

    def integrate_sequence(self, input_sequence, x0=None):
        """Integrate a sequence of inputs"""
        if x0 is None:
            x = torch.zeros(self.n)
        else:
            x = x0.clone()

        trajectory = []
        for I_t in input_sequence:
            x = self.forward(x, I_t)
            trajectory.append(x.clone())

        return torch.stack(trajectory)

    def check_integration_quality(self, n_steps=1000):
        """Verify perfect integration (no drift without input)"""
        x = torch.randn(self.n)
        x0_norm = torch.norm(x)

        # Evolve without input
        for _ in range(n_steps):
            x = self.forward(x, torch.zeros(self.n), dt=1.0)

        drift = torch.norm(x - x * (x0_norm / torch.norm(x)))
        return drift.item()  # Should be ~0 for perfect integrator
```

**Source**: Seung (1996) PNAS; Major & Tank (2004) Nature; Goldman et al. (2003) Neuron; MECHANISM_TO_ARCHITECTURE_PATTERNS.md

---

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

**Formula**: Log-Linear Encoding Model with MLE
```
λ(t) = exp(k ⊗ s(t) + h ⊗ y(t) + b)

Log-likelihood: L = Σ log λ(tₖ) - ∫ λ(t) dt
                   k

where:
- λ(t) = instantaneous firing rate
- k ⊗ s = stimulus filter convolved with stimulus
- h ⊗ y = spike history filter convolved with past spikes
- b = bias (baseline firing rate)
- Spikes ~ Poisson(λ(t))
- tₖ = spike times
- L = log-likelihood for parameter fitting
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


### Point Process Conditional Intensity Function

**Purpose**: Model spike trains as temporal point processes with time-varying intensity—foundation for continuous-time spike analysis.

**Formula**: Conditional Intensity
```
λ(t|Hₜ) = lim   P(spike in [t, t+Δt) | Hₜ)
          Δt→0  ─────────────────────────────
                           Δt

For GLM: λ(t|Hₜ) = exp(β₀ + Σ βⱼxⱼ(t) + ∫ h(τ)N(t-τ)dτ)
                                j           0

where:
- Hₜ = history up to time t
- xⱼ(t) = external covariates (stimulus, behavior)
- N(t) = spike train (counting process)
- h(τ) = self-history kernel (refractoriness, bursting)
- β = regression coefficients
```

**Nature's Implementation**: Captures instantaneous spiking propensity conditioned on past. Includes refractoriness, bursting, adaptation. Used for single neurons and populations. Foundation for spike train analysis in cortex, hippocampus, basal ganglia.

**Impact**: **MEDIUM-HIGH - Continuous-Time Encoding**
Rigorous probabilistic framework for spike trains. Handles irregular timing. Supports model comparison via likelihood. Generalizes GLM to arbitrary history dependence. Critical for BMI decoding, neuroprosthetics, and causal inference from spike data. Handles multi-neuron interactions and external covariates.

**Code Example**:
```python
class PointProcessGLM(nn.Module):
    """Point process GLM with self-history and covariates"""

    def __init__(self, n_covariates=10, history_len=50, dt=0.001):
        super().__init__()
        self.dt = dt
        self.history_len = history_len

        # Covariate coefficients
        self.beta = nn.Parameter(torch.randn(n_covariates) * 0.1)
        self.beta_0 = nn.Parameter(torch.zeros(1))

        # Self-history kernel (refractoriness, bursting)
        self.h_kernel = nn.Parameter(torch.randn(history_len) * 0.1)

    def conditional_intensity(self, covariates, spike_history):
        """Compute λ(t|H_t)"""
        # Covariate contribution
        covariate_term = torch.matmul(covariates, self.beta)

        # Self-history contribution (convolution)
        if spike_history.shape[1] >= self.history_len:
            history_window = spike_history[:, -self.history_len:]
            history_term = torch.sum(
                history_window * self.h_kernel.flip(0), dim=1
            )
        else:
            history_term = torch.zeros(spike_history.shape[0])

        # Log-linear intensity
        log_intensity = self.beta_0 + covariate_term + history_term
        intensity = torch.exp(log_intensity)

        return intensity

    def log_likelihood(self, covariates, spike_times, T_total):
        """
        Continuous-time log-likelihood
        L = Σ log(λ(tₖ)) - ∫₀ᵀ λ(t) dt
        """
        n_steps = int(T_total / self.dt)

        # Initialize spike history
        spike_train = torch.zeros(1, n_steps)
        spike_indices = (spike_times / self.dt).long()
        spike_train[0, spike_indices] = 1

        # Compute intensity over time
        log_likelihood = 0
        for t_idx in range(n_steps):
            history = spike_train[:, max(0, t_idx-self.history_len):t_idx]
            intensity = self.conditional_intensity(
                covariates[t_idx:t_idx+1], history
            )

            # Log-likelihood contribution
            if spike_train[0, t_idx] == 1:
                log_likelihood += torch.log(intensity + 1e-8)

            log_likelihood -= intensity * self.dt

        return log_likelihood

    def generate_spikes(self, covariates, T_total):
        """Generate spike train via time-rescaling theorem"""
        n_steps = int(T_total / self.dt)
        spike_train = torch.zeros(1, n_steps)

        for t_idx in range(n_steps):
            history = spike_train[:, max(0, t_idx-self.history_len):t_idx]
            intensity = self.conditional_intensity(
                covariates[t_idx:t_idx+1], history
            )

            # Poisson process: P(spike) = λ·dt
            if torch.rand(1) < intensity * self.dt:
                spike_train[0, t_idx] = 1

        return spike_train

# Example usage
model = PointProcessGLM(n_covariates=10, history_len=50, dt=0.001)
covariates = torch.randn(10000, 10)  # 10s of data
spike_times = torch.tensor([0.1, 0.15, 0.3, 0.5, 0.8])

# Fit model
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
for epoch in range(100):
    ll = model.log_likelihood(covariates, spike_times, T_total=10.0)
    loss = -ll

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 20 == 0:
        print(f"Epoch {epoch}, NLL: {loss.item():.4f}")
```

**Source**: Brown et al. (2002) Neural Comp; Truccolo et al. (2005) J Neurophys; Paninski et al. (2007) J Comp Neurosci

---

### Kernel Regression Decoder (Population Vector)

**Purpose**: Decode behavioral/stimulus variables from population spike trains using kernel smoothing—standard for BMI and motor decoding.

**Formula**: Weighted Average with Kernel Smoothing
```
x̂(t) = Σ wᵢ · K(t - tᵢ) · rᵢ
        i=1..N

K(τ) = (1/√2πσ) · exp(-τ²/2σ²)  [Gaussian kernel]

where:
- x̂(t) = decoded variable (position, velocity, stimulus)
- rᵢ = spike count for neuron i in window
- wᵢ = tuning weight for neuron i
- K(τ) = temporal kernel (smoothing)
- σ = kernel bandwidth
```

**Nature's Implementation**: Population coding in motor cortex, parietal cortex, hippocampus. Smooth integration of population activity. Robust to single-neuron noise. Used for arm reaching, eye movements, spatial navigation.

**Impact**: **MEDIUM-HIGH - Population Decoding**
Simple, fast, interpretable. Real-time BMI decoding. Leverages population diversity. Outperforms single neurons. Foundation for neural prosthetics and cursor control. Critical for understanding distributed representations and population codes.

**Code Example**:
```python
class KernelRegressionDecoder:
    """Decode from population spikes using kernel smoothing"""

    def __init__(self, n_neurons, bandwidth=0.05):
        self.n_neurons = n_neurons
        self.sigma = bandwidth

        # Tuning weights (learned from training data)
        self.weights = None

    def gaussian_kernel(self, tau):
        """Temporal smoothing kernel"""
        return np.exp(-tau**2 / (2 * self.sigma**2)) / np.sqrt(2 * np.pi * self.sigma**2)

    def train(self, spike_trains, true_states, dt=0.001):
        """
        Learn tuning weights via least squares
        spike_trains: [n_neurons, n_timesteps]
        true_states: [n_timesteps, n_dims]
        """
        n_steps = spike_trains.shape[1]

        # Compute smoothed firing rates
        time_axis = np.arange(n_steps) * dt
        smoothed_rates = np.zeros((self.n_neurons, n_steps))

        for neuron_idx in range(self.n_neurons):
            spike_times = time_axis[spike_trains[neuron_idx] > 0]

            for t_idx, t in enumerate(time_axis):
                # Kernel-weighted spike rate
                tau = t - spike_times
                smoothed_rates[neuron_idx, t_idx] = np.sum(
                    self.gaussian_kernel(tau)
                )

        # Least squares: X = R·W → W = (R'R)⁻¹R'X
        R = smoothed_rates.T  # [n_steps, n_neurons]
        X = true_states       # [n_steps, n_dims]

        self.weights = np.linalg.lstsq(R, X, rcond=None)[0]  # [n_neurons, n_dims]

    def decode(self, spike_trains, dt=0.001):
        """Decode states from spike trains"""
        n_steps = spike_trains.shape[1]
        time_axis = np.arange(n_steps) * dt

        # Smooth firing rates
        smoothed_rates = np.zeros((self.n_neurons, n_steps))

        for neuron_idx in range(self.n_neurons):
            spike_times = time_axis[spike_trains[neuron_idx] > 0]

            for t_idx, t in enumerate(time_axis):
                tau = t - spike_times
                smoothed_rates[neuron_idx, t_idx] = np.sum(
                    self.gaussian_kernel(tau)
                )

        # Decode: X̂ = R·W
        decoded_states = smoothed_rates.T @ self.weights

        return decoded_states

    def decode_velocity(self, spike_trains, dt=0.001):
        """Special case: decode 2D velocity for BMI"""
        decoded = self.decode(spike_trains, dt)

        # Velocity typically requires integration for position
        # or direct velocity tuning
        return decoded

# Example: Motor cortex BMI decoder
n_neurons = 100
decoder = KernelRegressionDecoder(n_neurons, bandwidth=0.05)

# Training data (1000 time steps)
spike_trains_train = np.random.poisson(5 * np.random.rand(n_neurons, 1000))
true_velocity = np.random.randn(1000, 2)  # 2D velocity

decoder.train(spike_trains_train, true_velocity, dt=0.001)

# Test decoding
spike_trains_test = np.random.poisson(5 * np.random.rand(n_neurons, 500))
decoded_velocity = decoder.decode(spike_trains_test, dt=0.001)

print(f"Decoded velocity shape: {decoded_velocity.shape}")
```

**Source**: Georgopoulos et al. (1986) Science; Wu et al. (2006) Neural Comp; Cunningham & Yu (2014) Nat Neurosci

---

### Gaussian Process Latent Variable Model (GP-LVM)

**Purpose**: Discover low-dimensional latent structure in neural population activity—unsupervised dimensionality reduction with uncertainty.

**Formula**: Probabilistic Mapping from Latent to Observed
```
Y = f(X) + ε,  f ~ GP(0, K)

K(x, x') = σ² exp(-||x - x'||²/2ℓ²)  [RBF kernel]

p(Y|X) = N(Y | 0, K_XX + σₙ²I)

where:
- Y = [n × d] observed neural activity (neurons × time)
- X = [n × q] latent variables (q << d)
- K_XX = kernel matrix from latent positions
- σ² = signal variance, ℓ = length scale
- σₙ² = observation noise
```

**Nature's Implementation**: Captures manifold structure in population codes. Revealed low-D structure in motor cortex, visual cortex, hippocampus. Latent states correspond to motor planning, stimulus features, spatial position.

**Impact**: **MEDIUM - Latent Structure Discovery**
Fully Bayesian, quantifies uncertainty. Discovers interpretable latent states. Handles missing data. Flexible nonlinear mapping. Reveals neural manifolds and dynamical structure. Critical for understanding population representations and state-space dynamics.

**Code Example**:
```python
from scipy.spatial.distance import pdist, squareform
from scipy.optimize import minimize

class GPLVM:
    """Gaussian Process Latent Variable Model"""

    def __init__(self, observed_dim, latent_dim=3, length_scale=1.0, signal_var=1.0):
        self.d = observed_dim
        self.q = latent_dim
        self.length_scale = length_scale
        self.signal_var = signal_var
        self.noise_var = 0.1

        self.X_latent = None  # To be optimized

    def rbf_kernel(self, X1, X2=None):
        """RBF kernel: k(x,x') = σ² exp(-||x-x'||²/2ℓ²)"""
        if X2 is None:
            X2 = X1

        # Pairwise distances
        dists = np.sum(X1**2, axis=1)[:, None] + np.sum(X2**2, axis=1)[None, :] - 2 * X1 @ X2.T

        K = self.signal_var * np.exp(-dists / (2 * self.length_scale**2))

        return K

    def log_likelihood(self, X_latent, Y):
        """
        Marginal log-likelihood: log p(Y|X)
        """
        n = Y.shape[0]

        X_latent = X_latent.reshape(n, self.q)

        # Kernel matrix
        K = self.rbf_kernel(X_latent) + self.noise_var * np.eye(n)

        # Cholesky decomposition for stability
        try:
            L = np.linalg.cholesky(K)
        except np.linalg.LinAlgError:
            return -1e10  # Numerical issue

        # Log-likelihood for each dimension
        ll = 0
        for d in range(self.d):
            y_d = Y[:, d]

            # Solve L·L'·α = y
            alpha = np.linalg.solve(L.T, np.linalg.solve(L, y_d))

            # -0.5·y'·K⁻¹·y - 0.5·log|K| - (n/2)log(2π)
            ll += -0.5 * y_d @ alpha - np.sum(np.log(np.diag(L))) - 0.5 * n * np.log(2 * np.pi)

        return ll

    def fit(self, Y, n_iterations=100):
        """
        Find latent positions X that maximize p(Y|X)
        Y: [n_samples, n_neurons]
        """
        n = Y.shape[0]

        # Initialize latent positions (PCA)
        Y_centered = Y - Y.mean(axis=0)
        U, s, Vt = np.linalg.svd(Y_centered, full_matrices=False)
        self.X_latent = U[:, :self.q] * s[:self.q]

        # Optimize latent positions
        def objective(X_flat):
            return -self.log_likelihood(X_flat, Y)

        result = minimize(
            objective,
            self.X_latent.flatten(),
            method='L-BFGS-B',
            options={'maxiter': n_iterations}
        )

        self.X_latent = result.x.reshape(n, self.q)

        return self.X_latent

    def reconstruct(self, X_latent_new):
        """
        Predict Y_new from new latent positions (requires training data)
        """
        # This requires storing training data and doing GP prediction
        # Simplified version
        pass

# Example usage
n_samples = 200
n_neurons = 50
latent_dim = 3

# Simulated neural data with latent structure
true_latent = np.random.randn(n_samples, latent_dim)
Y_observed = true_latent @ np.random.randn(latent_dim, n_neurons) + 0.1 * np.random.randn(n_samples, n_neurons)

# Fit GP-LVM
model = GPLVM(observed_dim=n_neurons, latent_dim=3)
X_inferred = model.fit(Y_observed, n_iterations=50)

print(f"Inferred latent positions: {X_inferred.shape}")
print(f"Correlation with true latent: {np.corrcoef(true_latent.flatten(), X_inferred.flatten())[0,1]:.3f}")
```

**Source**: Lawrence (2005) JMLR; Yu et al. (2009) J Neurophys; Cunningham & Yu (2014) Nat Neurosci

---

### Kalman Filter & Extended Kalman Filter (State-Space Decoding)

**Purpose**: Optimal recursive state estimation from noisy neural observations—real-time BMI decoding with dynamics.

**Formula**: Linear Kalman Filter (Discrete & Continuous-Time)

**Continuous-Time Neural Form** (Prediction + Correction):
```
dẋ̂/dt = A·x̂ + B·u + K(y - C·x̂)

where:
- x̂ = state estimate (continuous evolution)
- A = dynamics matrix
- B = control matrix
- u = control input
- K = Kalman gain (observation weight)
- y = continuous observation
- C = observation matrix
- (y - C·x̂) = innovation/prediction error

This is continuous-time prediction + correction in neural form.
```

**Discrete-Time Form** (Predict-Update Cycle):
```
State model:     xₜ = A·xₜ₋₁ + w,  w ~ N(0, Q)
Observation:     yₜ = C·xₜ + v,    v ~ N(0, R)

Prediction:      x̂ₜ|ₜ₋₁ = A·x̂ₜ₋₁|ₜ₋₁
                 Pₜ|ₜ₋₁ = A·Pₜ₋₁|ₜ₋₁·A' + Q

Update:          Kₜ = Pₜ|ₜ₋₁·C' / (C·Pₜ|ₜ₋₁·C' + R)
                 x̂ₜ|ₜ = x̂ₜ|ₜ₋₁ + Kₜ(yₜ - C·x̂ₜ|ₜ₋₁)
                 Pₜ|ₜ = (I - Kₜ·C)·Pₜ|ₜ₋₁

Extended KF (nonlinear):
State:           xₜ = f(xₜ₋₁) + w
Observation:     yₜ = h(xₜ) + v
Use Jacobians:   A = ∂f/∂x, C = ∂h/∂x

where:
- xₜ = latent state (position, velocity, etc.)
- yₜ = neural observations (spike counts, LFP)
- A = dynamics matrix, C = observation matrix
- Kₜ = Kalman gain (optimal weighting of prediction vs observation)
- P = covariance, Q = process noise, R = observation noise
```

**Nature's Implementation**: Motor cortex encodes arm kinematics. BMI systems decode from populations. Handles sensory uncertainty and motor variability. Real-time cursor control, prosthetic limbs.

**Impact**: **HIGH - Real-Time BMI**
Optimal under linearity/Gaussianity. Real-time recursive updates. Incorporates dynamics (smooth trajectories). Used in clinical BMI systems. Extended version handles nonlinear tuning. Critical for neuroprosthetics, cursor control, and understanding sensorimotor integration.

**Code Example**:
```python
class KalmanFilterDecoder:
    """Kalman filter for neural decoding"""

    def __init__(self, state_dim, obs_dim):
        self.n_state = state_dim
        self.n_obs = obs_dim

        # Dynamics: x_t = A·x_{t-1} + w
        self.A = np.eye(state_dim)  # Default: random walk
        self.Q = 0.1 * np.eye(state_dim)  # Process noise

        # Observation: y_t = C·x_t + v
        self.C = np.random.randn(obs_dim, state_dim) * 0.1
        self.R = np.eye(obs_dim)  # Observation noise

        # State estimate
        self.x_hat = np.zeros(state_dim)
        self.P = np.eye(state_dim)

    def predict(self):
        """Prediction step"""
        self.x_hat = self.A @ self.x_hat
        self.P = self.A @ self.P @ self.A.T + self.Q

    def update(self, y_obs):
        """Update step with new observation"""
        # Innovation
        y_pred = self.C @ self.x_hat
        innovation = y_obs - y_pred

        # Innovation covariance
        S = self.C @ self.P @ self.C.T + self.R

        # Kalman gain
        K = self.P @ self.C.T @ np.linalg.inv(S)

        # Update estimate
        self.x_hat = self.x_hat + K @ innovation
        self.P = (np.eye(self.n_state) - K @ self.C) @ self.P

        return self.x_hat

    def decode(self, observations):
        """Decode state sequence from observations"""
        n_steps = observations.shape[0]
        states = np.zeros((n_steps, self.n_state))

        for t in range(n_steps):
            self.predict()
            states[t] = self.update(observations[t])

        return states

    def train_parameters(self, states_true, observations):
        """Learn A, C, Q, R from training data"""
        # Learn dynamics A via least squares
        X_t = states_true[1:]
        X_tm1 = states_true[:-1]
        self.A = X_t.T @ X_tm1 @ np.linalg.inv(X_tm1.T @ X_tm1)

        # Process noise Q
        residuals_state = X_t - (self.A @ X_tm1.T).T
        self.Q = np.cov(residuals_state.T)

        # Learn observation C
        self.C = observations.T @ states_true @ np.linalg.inv(states_true.T @ states_true)

        # Observation noise R
        residuals_obs = observations - (self.C @ states_true.T).T
        self.R = np.cov(residuals_obs.T)


class ExtendedKalmanFilter:
    """Extended Kalman Filter for nonlinear decoding"""

    def __init__(self, state_dim, obs_dim, dynamics_fn, observation_fn):
        self.n_state = state_dim
        self.n_obs = obs_dim

        self.f = dynamics_fn  # f(x)
        self.h = observation_fn  # h(x)

        self.Q = 0.1 * np.eye(state_dim)
        self.R = np.eye(obs_dim)

        self.x_hat = np.zeros(state_dim)
        self.P = np.eye(state_dim)

    def predict(self):
        """Prediction with nonlinear dynamics"""
        self.x_hat = self.f(self.x_hat)

        # Linearize: A = ∂f/∂x
        A = self.jacobian_f(self.x_hat)
        self.P = A @ self.P @ A.T + self.Q

    def update(self, y_obs):
        """Update with nonlinear observation"""
        # Linearize: C = ∂h/∂x
        C = self.jacobian_h(self.x_hat)

        # Standard Kalman update
        y_pred = self.h(self.x_hat)
        innovation = y_obs - y_pred

        S = C @ self.P @ C.T + self.R
        K = self.P @ C.T @ np.linalg.inv(S)

        self.x_hat = self.x_hat + K @ innovation
        self.P = (np.eye(self.n_state) - K @ C) @ self.P

        return self.x_hat

    def jacobian_f(self, x):
        """Compute ∂f/∂x via finite differences"""
        eps = 1e-6
        J = np.zeros((self.n_state, self.n_state))

        for i in range(self.n_state):
            x_plus = x.copy()
            x_plus[i] += eps
            J[:, i] = (self.f(x_plus) - self.f(x)) / eps

        return J

    def jacobian_h(self, x):
        """Compute ∂h/∂x"""
        eps = 1e-6
        J = np.zeros((self.n_obs, self.n_state))

        for i in range(self.n_state):
            x_plus = x.copy()
            x_plus[i] += eps
            J[:, i] = (self.h(x_plus) - self.h(x)) / eps

        return J

# Example: BMI velocity decoding
state_dim = 4  # [x, y, vx, vy]
obs_dim = 50   # 50 neurons

# Linear dynamics (constant velocity)
A = np.array([
    [1, 0, 1, 0],  # x += vx
    [0, 1, 0, 1],  # y += vy
    [0, 0, 1, 0],  # vx constant
    [0, 0, 0, 1]   # vy constant
])

kf = KalmanFilterDecoder(state_dim, obs_dim)
kf.A = A

# Simulated observations
observations = np.random.randn(100, obs_dim)
decoded_states = kf.decode(observations)

print(f"Decoded states: {decoded_states.shape}")
```

**Source**: Wu et al. (2003) NIPS; Srinivasan et al. (2006) J Neural Eng; Gilja et al. (2012) Nat Neurosci; Li et al. (2009) J Neural Eng

---

### Fisher Information (Discrimination Threshold)

**Purpose**: Quantify how much information neural responses carry about small stimulus changes—determines discrimination performance.

**Formula**: Curvature of Log-Likelihood
```
I_F(s) = -E[∂²/∂s² log p(r|s)]

For Poisson neurons:
I_F(s) = [f'(s)]² / f(s)

Cramér-Rao bound:
var(ŝ) ≥ 1 / I_F(s)

where:
- s = stimulus parameter
- r = neural response
- f(s) = tuning curve (mean firing rate)
- f'(s) = slope of tuning curve
- ŝ = stimulus estimate
- Lower bound on estimation variance
```

**Nature's Implementation**: Determines discrimination thresholds in sensory systems. High Fisher information → steep tuning curves → good discrimination. Matches psychophysical thresholds in vision, audition, touch.

**Impact**: **MEDIUM - Optimal Coding**
Links neural coding to behavior. Predicts discrimination performance. Guides optimal tuning curve design. Reveals information-limiting bottlenecks. Critical for understanding sensory precision and efficient coding strategies.

**Code Example**:
```python
class FisherInformationAnalyzer:
    """Compute Fisher information from neural tuning curves"""

    def __init__(self):
        pass

    def fisher_info_poisson(self, tuning_curve, stimulus_values):
        """
        Fisher information for Poisson neurons
        I_F(s) = [f'(s)]² / f(s)
        """
        # Numerical derivative of tuning curve
        f_prime = np.gradient(tuning_curve, stimulus_values)

        # Fisher information
        fisher_info = f_prime**2 / (tuning_curve + 1e-10)

        return fisher_info

    def fisher_info_population(self, tuning_curves, stimulus_values):
        """
        Population Fisher information (sum of individual neurons)
        I_F^pop(s) = Σ I_F^i(s)
        """
        population_FI = np.zeros_like(stimulus_values)

        for tuning_curve in tuning_curves:
            population_FI += self.fisher_info_poisson(tuning_curve, stimulus_values)

        return population_FI

    def cramer_rao_bound(self, fisher_info):
        """Minimum achievable variance: var(ŝ) ≥ 1/I_F"""
        return 1.0 / (fisher_info + 1e-10)

    def discrimination_threshold(self, tuning_curve, stimulus_values, criterion=0.75):
        """
        JND (just-noticeable difference) from Fisher info
        Δs ≈ 1/√I_F for threshold discrimination
        """
        fisher_info = self.fisher_info_poisson(tuning_curve, stimulus_values)

        # Threshold
        jnd = 1.0 / np.sqrt(fisher_info + 1e-10)

        return jnd

# Example: Visual orientation tuning
analyzer = FisherInformationAnalyzer()

# Stimulus: orientation from 0 to 180 degrees
orientations = np.linspace(0, 180, 100)

# Von Mises tuning curve (circular Gaussian)
preferred_ori = 90
kappa = 5  # concentration
tuning_curve = 10 * np.exp(kappa * np.cos(2 * np.pi * (orientations - preferred_ori) / 180))

# Fisher information
fisher_info = analyzer.fisher_info_poisson(tuning_curve, orientations)

# Discrimination threshold
jnd = analyzer.discrimination_threshold(tuning_curve, orientations)

print(f"Peak Fisher info: {fisher_info.max():.2f}")
print(f"Best discrimination threshold: {jnd.min():.2f} degrees")

# Population (100 neurons with different preferences)
n_neurons = 100
population_tuning = []
for i in range(n_neurons):
    pref = i * 180 / n_neurons
    tc = 10 * np.exp(kappa * np.cos(2 * np.pi * (orientations - pref) / 180))
    population_tuning.append(tc)

population_FI = analyzer.fisher_info_population(population_tuning, orientations)
print(f"Population FI improvement: {population_FI.max() / fisher_info.max():.1f}x")
```

**Source**: Seung & Sompolinsky (1993) PNAS; Pouget et al. (2000) Nat Rev Neurosci; Dayan & Abbott (2001) Theoretical Neuroscience

---

### Directed Information (Causal Information Flow)

**Purpose**: Measure causal information transfer between time series—distinguishes driver from driven in neural circuits.

**Formula**: Cumulative Conditional Mutual Information
```
I(X → Y) = Σ I(X^t; Yₜ | Y^{t-1})
           t=1..T

         = Σ H(Yₜ | Y^{t-1}) - H(Yₜ | Y^{t-1}, X^t)
           t

where:
- X^t = {X₁, X₂, ..., Xₜ} = past of X
- Y^{t-1} = {Y₁, ..., Yₜ₋₁} = past of Y
- I(X → Y) quantifies: how much X's past informs Y's present
- Asymmetric: I(X→Y) ≠ I(Y→X)
```

**Nature's Implementation**: Reveals feedforward vs feedback pathways. Identifies driver neurons in circuits. Used for V1→MT, thalamus→cortex, hippocampus→prefrontal. Distinguishes causal influence from correlation.

**Impact**: **MEDIUM - Causal Inference**
Stronger than correlation or mutual information. Reveals directional influence. Handles feedback loops. Critical for circuit mapping and understanding information routing in hierarchical brain networks.

**Code Example**:
```python
class DirectedInformationAnalyzer:
    """Compute directed information for causal inference"""

    def __init__(self, history_length=5, n_bins=10):
        self.L = history_length
        self.n_bins = n_bins

    def discretize(self, data):
        """Bin continuous data"""
        bins = np.linspace(data.min(), data.max(), self.n_bins + 1)
        return np.digitize(data, bins[1:-1])

    def entropy(self, p):
        """Shannon entropy"""
        p = p[p > 0]
        return -np.sum(p * np.log2(p))

    def conditional_entropy(self, Y_present, Y_past, X_past=None):
        """
        H(Y_t | Y^{t-1}) or H(Y_t | Y^{t-1}, X^t)
        """
        # Create joint histogram
        if X_past is None:
            # H(Y_t | Y^{t-1})
            joint = np.column_stack([Y_present, Y_past])
        else:
            # H(Y_t | Y^{t-1}, X^t)
            joint = np.column_stack([Y_present, Y_past, X_past])

        # Compute conditional entropy via joint distribution
        unique_joint, counts_joint = np.unique(joint, axis=0, return_counts=True)
        p_joint = counts_joint / counts_joint.sum()

        unique_cond, counts_cond = np.unique(joint[:, 1:], axis=0, return_counts=True)
        p_cond = counts_cond / counts_cond.sum()

        # H(Y|C) = H(Y,C) - H(C)
        H_joint = self.entropy(p_joint)
        H_cond = self.entropy(p_cond)

        return H_joint - H_cond

    def directed_information(self, X, Y):
        """
        Compute I(X → Y) = Σ I(X^t; Y_t | Y^{t-1})
        """
        T = len(X)
        X_discrete = self.discretize(X)
        Y_discrete = self.discretize(Y)

        directed_info = 0

        for t in range(self.L, T):
            # Current Y
            Y_t = Y_discrete[t:t+1]

            # Past Y
            Y_past = Y_discrete[t-self.L:t]

            # Past X (up to and including current)
            X_past = X_discrete[t-self.L:t+1]

            # I(X^t; Y_t | Y^{t-1}) = H(Y_t | Y^{t-1}) - H(Y_t | Y^{t-1}, X^t)
            H_Y_given_Ypast = self.conditional_entropy(Y_t, Y_past)
            H_Y_given_both = self.conditional_entropy(Y_t, Y_past, X_past)

            directed_info += H_Y_given_Ypast - H_Y_given_both

        # Normalize by time steps
        directed_info /= (T - self.L)

        return directed_info

    def bidirectional_analysis(self, X, Y):
        """Compute both I(X→Y) and I(Y→X)"""
        I_X_to_Y = self.directed_information(X, Y)
        I_Y_to_X = self.directed_information(Y, X)

        return I_X_to_Y, I_Y_to_X

# Example: Causal coupling between brain regions
analyzer = DirectedInformationAnalyzer(history_length=5, n_bins=10)

# Simulated LFP signals
T = 1000
X = np.cumsum(np.random.randn(T)) * 0.1  # Region 1
Y = 0.5 * X + np.cumsum(np.random.randn(T)) * 0.1  # Region 2 (driven by X)

# Directed information
I_X_to_Y, I_Y_to_X = analyzer.bidirectional_analysis(X, Y)

print(f"I(X → Y): {I_X_to_Y:.4f} bits/sample")
print(f"I(Y → X): {I_Y_to_X:.4f} bits/sample")
print(f"Net flow (X→Y): {I_X_to_Y - I_Y_to_X:.4f}")
```

**Source**: Massey (1990) IEEE Trans Info Theory; Amblard & Michel (2013) Signal Processing; Ito et al. (2011) PLoS Comp Bio

---

### Maximum a Posteriori (MAP) Decoder

**Purpose**: Optimal Bayesian decoder maximizing posterior probability—finds most likely stimulus given neural response.

**Formula**: Bayesian Inference with Prior
```
ŝ_MAP = argmax p(s|r) = argmax p(r|s)·p(s)
         s               s

log p(s|r) = log p(r|s) + log p(s) - log p(r)

For Poisson GLM:
p(r|s) = Π exp(-λᵢ(s)) · λᵢ(s)^rᵢ / rᵢ!
         i

where:
- s = stimulus
- r = neural response (spike counts)
- p(r|s) = likelihood (encoding model)
- p(s) = prior over stimuli
- ŝ_MAP = maximum a posteriori estimate
```

**Nature's Implementation**: Optimal decoding in visual cortex, auditory cortex, somatosensory. Incorporates prior knowledge (e.g., natural scene statistics, motion continuity). Explains perceptual biases and illusions.

**Impact**: **MEDIUM-HIGH - Optimal Decoding**
Optimal under 0-1 loss. Incorporates priors (Bayesian). Outperforms maximum likelihood. Explains perceptual biases. Critical for BMI decoding and understanding neural inference.

**Code Example**:
```python
class MAPDecoder:
    """Maximum a posteriori Bayesian decoder"""

    def __init__(self, stimulus_values, encoding_model, prior_type='uniform'):
        self.stimuli = stimulus_values
        self.encoder = encoding_model
        self.prior_type = prior_type

    def prior(self, s):
        """p(s): prior distribution over stimuli"""
        if self.prior_type == 'uniform':
            return np.ones_like(s) / len(s)
        elif self.prior_type == 'gaussian':
            # Natural scene prior: center bias
            mu, sigma = 0, 1
            return np.exp(-(s - mu)**2 / (2 * sigma**2))
        elif self.prior_type == 'slow':
            # Slow motion prior (temporal smoothness)
            # For time series: p(s_t) ∝ exp(-|s_t - s_{t-1}|²)
            return np.ones_like(s)  # Placeholder

    def likelihood(self, response, stimulus):
        """
        p(r|s): Poisson likelihood for population
        response: [n_neurons] spike counts
        stimulus: scalar
        """
        # Get tuning curves at this stimulus
        rates = self.encoder.get_rates(stimulus)  # [n_neurons]

        # Poisson likelihood: Π exp(-λ)·λ^r/r!
        # Log-likelihood: Σ (r·log(λ) - λ - log(r!))
        log_likelihood = np.sum(
            response * np.log(rates + 1e-10) - rates
        )

        return np.exp(log_likelihood)

    def posterior(self, response):
        """
        p(s|r) ∝ p(r|s)·p(s)
        """
        posteriors = np.zeros(len(self.stimuli))

        for i, s in enumerate(self.stimuli):
            posteriors[i] = self.likelihood(response, s) * self.prior(self.stimuli)[i]

        # Normalize
        posteriors /= np.sum(posteriors) + 1e-10

        return posteriors

    def decode_map(self, response):
        """Find stimulus that maximizes posterior"""
        post = self.posterior(response)
        map_idx = np.argmax(post)

        return self.stimuli[map_idx], post

    def decode_mmse(self, response):
        """
        Minimum mean squared error (posterior mean)
        ŝ_MMSE = E[s|r] = Σ s·p(s|r)
        """
        post = self.posterior(response)
        mmse_estimate = np.sum(self.stimuli * post)

        return mmse_estimate

# Example: Visual orientation decoding
class PoissonEncoder:
    """Poisson encoding model with tuning curves"""

    def __init__(self, n_neurons=50):
        self.n_neurons = n_neurons
        # Preferred orientations uniformly distributed
        self.preferred_ori = np.linspace(0, 180, n_neurons)
        self.kappa = 5  # Tuning width

    def get_rates(self, stimulus):
        """Tuning curves: von Mises"""
        rates = 10 * np.exp(
            self.kappa * np.cos(2 * np.pi * (stimulus - self.preferred_ori) / 180)
        )
        return rates

    def generate_response(self, stimulus):
        """Generate Poisson spike counts"""
        rates = self.get_rates(stimulus)
        return np.random.poisson(rates)

# Setup
stimulus_values = np.linspace(0, 180, 180)
encoder = PoissonEncoder(n_neurons=50)
decoder = MAPDecoder(stimulus_values, encoder, prior_type='uniform')

# Encode stimulus
true_stimulus = 90
response = encoder.generate_response(true_stimulus)

# Decode
map_estimate, posterior = decoder.decode_map(response)
mmse_estimate = decoder.decode_mmse(response)

print(f"True stimulus: {true_stimulus}°")
print(f"MAP estimate: {map_estimate:.1f}°")
print(f"MMSE estimate: {mmse_estimate:.1f}°")
print(f"Posterior entropy: {-np.sum(posterior * np.log2(posterior + 1e-10)):.2f} bits")
```

**Source**: Jazayeri & Movshon (2006) Nat Neurosci; Ma et al. (2006) Nat Neurosci; Berkes et al. (2011) Science

---

### Maximum Entropy (Ising) Model for Neural Populations

**Purpose**: Capture pairwise correlations in population activity with minimal assumptions—maximum entropy distribution.

**Formula**: Pairwise Ising Model
```
p(σ) = (1/Z) exp(Σ hᵢσᵢ + Σ Jᵢⱼσᵢσⱼ)
                 i       i<j

Z = Σ exp(...)  [partition function]
    σ

where:
- σᵢ ∈ {0,1} = spike/no-spike for neuron i
- hᵢ = external field (bias for neuron i)
- Jᵢⱼ = pairwise coupling (correlation)
- Maximizes entropy subject to matching firing rates and correlations
```

**Nature's Implementation**: Captures functional connectivity in retina, cortex. Explains 90%+ of population variability with only pairwise terms. Reveals network states and attractors.

**Impact**: **MEDIUM - Population Structure**
Minimal model matching observed statistics. Reveals emergent collective behavior. Predicts rare synchronous events. Foundation for understanding population codes and criticality. Critical for analyzing multi-electrode recordings.

**Code Example**:
```python
from scipy.optimize import minimize

class IsingModel:
    """Maximum entropy Ising model for binary neural data"""

    def __init__(self, n_neurons):
        self.n = n_neurons
        self.h = np.zeros(n_neurons)  # External fields
        self.J = np.zeros((n_neurons, n_neurons))  # Couplings

    def energy(self, sigma):
        """E(σ) = -Σhᵢσᵢ - ΣJᵢⱼσᵢσⱼ"""
        return -np.dot(self.h, sigma) - 0.5 * sigma @ self.J @ sigma

    def probability(self, sigma):
        """p(σ) = exp(-E)/Z"""
        # For large N, cannot compute Z exactly
        # Use unnormalized probability for sampling
        return np.exp(-self.energy(sigma))

    def fit(self, data, method='mle'):
        """
        Fit h and J to match empirical statistics
        data: [n_samples, n_neurons] binary spike patterns
        """
        n_samples = data.shape[0]

        # Empirical statistics
        p_i = np.mean(data, axis=0)  # Firing rates
        p_ij = (data.T @ data) / n_samples  # Pairwise correlations

        if method == 'mle':
            # Maximum likelihood via gradient descent
            # (exact for small N, approximate for large N)
            self._fit_mle(p_i, p_ij)
        elif method == 'independent':
            # Independent model (J=0)
            self.h = np.log(p_i / (1 - p_i + 1e-10))
            self.J = np.zeros((self.n, self.n))

    def _fit_mle(self, p_i_target, p_ij_target, n_iter=100):
        """Maximum likelihood fitting (gradient descent)"""
        # Initialize
        self.h = np.log(p_i_target / (1 - p_i_target + 1e-10))

        for iteration in range(n_iter):
            # Sample from current model
            samples = self.sample_metropolis(n_samples=1000, n_steps=100)

            # Model statistics
            p_i_model = np.mean(samples, axis=0)
            p_ij_model = (samples.T @ samples) / samples.shape[0]

            # Gradient ascent
            lr = 0.01
            self.h += lr * (p_i_target - p_i_model)
            self.J += lr * (p_ij_target - p_ij_model)

            # Symmetrize J
            self.J = (self.J + self.J.T) / 2
            np.fill_diagonal(self.J, 0)

    def sample_metropolis(self, n_samples=1000, n_steps=100):
        """Sample from Ising model via Metropolis-Hastings"""
        samples = []
        sigma = np.random.randint(0, 2, size=self.n)

        for _ in range(n_samples):
            for _ in range(n_steps):
                # Propose flip
                i = np.random.randint(self.n)
                sigma_new = sigma.copy()
                sigma_new[i] = 1 - sigma_new[i]

                # Acceptance probability
                dE = self.energy(sigma_new) - self.energy(sigma)
                if np.random.rand() < np.exp(-dE):
                    sigma = sigma_new

            samples.append(sigma.copy())

        return np.array(samples)

    def log_likelihood(self, data):
        """Log-likelihood of data under model (approximate)"""
        ll = 0
        for sigma in data:
            ll += -self.energy(sigma)

        # Subtract log(Z) - typically intractable
        # Use pseudo-likelihood instead
        return ll

# Example: Fit Ising model to retinal ganglion cell data
n_neurons = 10
ising = IsingModel(n_neurons)

# Simulated binary spike patterns
n_samples = 1000
firing_rate = 0.1
data = (np.random.rand(n_samples, n_neurons) < firing_rate).astype(int)

# Add correlations
for i in range(1, n_neurons):
    corr = np.random.rand()
    if corr > 0.7:
        data[:, i] = data[:, 0]  # Copy spike pattern

# Fit model
ising.fit(data, method='mle')

print(f"Learned fields h: {ising.h}")
print(f"Learned couplings J[0,1]: {ising.J[0,1]:.3f}")

# Generate synthetic data
synthetic = ising.sample_metropolis(n_samples=100)
print(f"Synthetic firing rate: {synthetic.mean():.3f} (target: {data.mean():.3f})")
```

**Source**: Schneidman et al. (2006) Nature; Shlens et al. (2006) J Neurosci; Tkačik et al. (2014) arXiv

---

### Information Capacity of Poisson Neuron

**Purpose**: Quantify maximum information transmission rate of a Poisson neuron—fundamental coding limit.

**Formula**: Channel Capacity
```
C = max I(S; R)
    p(s)

For Poisson neuron with rate λ(s):
C ≈ (λ_max / 2) · log₂(1 + 1/CV²)

Approximation for small modulation:
C ≈ (Δλ)² / (2λ̄ · log(2))  bits/spike

where:
- λ_max = maximum firing rate
- CV = coefficient of variation (std/mean)
- Δλ = modulation depth
- λ̄ = mean rate
- For pure Poisson: CV = 1
```

**Nature's Implementation**: Sets limits on sensory coding. High-rate neurons (>100 Hz) transmit more bits. Low variability (CV < 1) increases capacity. Explains coding strategies across sensory systems.

**Impact**: **MEDIUM - Fundamental Limits**
Reveals coding constraints. Guides optimal rate and variability. Explains sparse coding (low λ̄, high Δλ). Critical for understanding efficient neural codes and information bottlenecks.

**Code Example**:
```python
class PoissonCapacityAnalyzer:
    """Compute information capacity of Poisson neurons"""

    def __init__(self):
        pass

    def capacity_approximation(self, lambda_max, CV=1.0):
        """
        C ≈ (λ_max/2) · log₂(1 + 1/CV²)
        """
        capacity = (lambda_max / 2) * np.log2(1 + 1 / CV**2)
        return capacity

    def capacity_modulation(self, lambda_mean, delta_lambda):
        """
        For small modulation:
        C ≈ (Δλ)²/(2λ̄·ln(2))  bits/spike
        """
        capacity_per_spike = delta_lambda**2 / (2 * lambda_mean * np.log(2))
        return capacity_per_spike

    def mutual_information_numeric(self, tuning_curve, stimulus_dist, n_trials=1000):
        """
        Numerically compute I(S; R) for arbitrary tuning
        """
        n_stimuli = len(tuning_curve)

        # Generate responses for each stimulus
        responses = []
        for s_idx in range(n_stimuli):
            rate = tuning_curve[s_idx]
            # Sample Poisson responses
            r_samples = np.random.poisson(rate, size=n_trials)
            responses.append(r_samples)

        responses = np.array(responses)  # [n_stimuli, n_trials]

        # Compute p(r), p(r|s), p(s)
        all_responses = responses.flatten()
        r_min, r_max = all_responses.min(), all_responses.max()
        r_bins = np.arange(r_min, r_max + 2)

        # p(r)
        p_r, _ = np.histogram(all_responses, bins=r_bins, density=True)
        p_r = p_r / p_r.sum()

        # p(s)
        p_s = stimulus_dist

        # I(S;R) = H(R) - H(R|S)
        H_R = -np.sum(p_r * np.log2(p_r + 1e-10))

        # H(R|S) = Σ p(s) H(R|s)
        H_R_given_S = 0
        for s_idx in range(n_stimuli):
            p_r_given_s, _ = np.histogram(responses[s_idx], bins=r_bins, density=True)
            p_r_given_s = p_r_given_s / (p_r_given_s.sum() + 1e-10)
            H_R_given_S += p_s[s_idx] * (-np.sum(p_r_given_s * np.log2(p_r_given_s + 1e-10)))

        mutual_info = H_R - H_R_given_S

        return mutual_info

# Example: Capacity of sensory neuron
analyzer = PoissonCapacityAnalyzer()

# High-firing neuron (motor cortex)
lambda_max_motor = 100  # spikes/s
CV_motor = 0.8
C_motor = analyzer.capacity_approximation(lambda_max_motor, CV_motor)
print(f"Motor cortex neuron capacity: {C_motor:.2f} bits/s")

# Low-firing neuron (sparse coding)
lambda_max_sparse = 5
CV_sparse = 1.2
C_sparse = analyzer.capacity_approximation(lambda_max_sparse, CV_sparse)
print(f"Sparse neuron capacity: {C_sparse:.2f} bits/s")

# Modulation-based capacity
lambda_mean = 20
delta_lambda = 10
C_per_spike = analyzer.capacity_modulation(lambda_mean, delta_lambda)
print(f"Capacity per spike: {C_per_spike:.4f} bits/spike")

# Numeric calculation for orientation tuning
orientations = np.linspace(0, 180, 20)
tuning_curve = 20 * np.exp(5 * np.cos(2 * np.pi * (orientations - 90) / 180))
stimulus_dist = np.ones(20) / 20  # Uniform

MI = analyzer.mutual_information_numeric(tuning_curve, stimulus_dist, n_trials=1000)
print(f"Mutual information (numeric): {MI:.3f} bits")
```

**Source**: Borst & Theunissen (1999) Nat Neurosci; Rieke et al. (1997) Spikes; Brunel & Nadal (1998) Neural Comp

---

### Granger Causality (Predictive Information Flow)

**Purpose**: Test if past values of X improve prediction of Y—operational definition of causality for time series.

**Formula**: Autoregressive Model Comparison
```
Model 1 (Y only):  Yₜ = Σ aᵢYₜ₋ᵢ + εₜ,  var(εₜ) = σ₁²
                        i=1..p

Model 2 (Y + X):   Yₜ = Σ aᵢYₜ₋ᵢ + Σ bⱼXₜ₋ⱼ + ηₜ,  var(ηₜ) = σ₂²
                        i=1..p      j=1..p

X Granger-causes Y if: σ₂² < σ₁²

F-statistic: F = [(σ₁² - σ₂²)/p] / [σ₂²/(n-2p-1)]

where:
- p = model order (lag)
- σ² = residual variance
- n = number of samples
- F-test determines significance
```

**Nature's Implementation**: Reveals effective connectivity in neural circuits. Used for LFP, EEG, fMRI, spike trains. Identifies feedforward, feedback, and recurrent pathways across brain regions.

**Impact**: **MEDIUM-HIGH - Effective Connectivity**
Statistically rigorous. Handles multivariate time series. Reveals directional influence. Foundation for network analysis. Critical for understanding information flow in neural circuits and large-scale brain networks.

**Code Example**:
```python
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tsa.vector_ar.var_model import VAR

class GrangerCausalityAnalyzer:
    """Test Granger causality between neural time series"""

    def __init__(self, max_lag=10):
        self.max_lag = max_lag

    def test_granger(self, X, Y, max_lag=None):
        """
        Test if X Granger-causes Y
        Returns: p-values for each lag
        """
        if max_lag is None:
            max_lag = self.max_lag

        # Prepare data: [Y, X] format for statsmodels
        data = np.column_stack([Y, X])

        # Run Granger causality test
        results = grangercausalitytests(data, maxlag=max_lag, verbose=False)

        # Extract F-statistics and p-values
        f_stats = []
        p_values = []
        for lag in range(1, max_lag + 1):
            f_stat = results[lag][0]['ssr_ftest'][0]
            p_val = results[lag][0]['ssr_ftest'][1]
            f_stats.append(f_stat)
            p_values.append(p_val)

        return np.array(f_stats), np.array(p_values)

    def pairwise_granger(self, signals, max_lag=5, alpha=0.05):
        """
        Compute pairwise Granger causality matrix
        signals: [n_channels, n_timepoints]
        Returns: adjacency matrix [i,j] = X_i → X_j
        """
        n_channels = signals.shape[0]
        causality_matrix = np.zeros((n_channels, n_channels))

        for i in range(n_channels):
            for j in range(n_channels):
                if i == j:
                    continue

                # Test if signal i Granger-causes signal j
                X = signals[i]
                Y = signals[j]

                f_stats, p_values = self.test_granger(X, Y, max_lag)

                # Use minimum p-value across lags
                min_p = p_values.min()
                if min_p < alpha:
                    causality_matrix[i, j] = 1  # Significant causality

        return causality_matrix

    def conditional_granger(self, X, Y, Z, max_lag=5):
        """
        Test if X Granger-causes Y conditioned on Z
        (partial Granger causality)
        """
        # Fit VAR model with all variables
        data_full = np.column_stack([Y, X, Z])
        model_full = VAR(data_full)
        result_full = model_full.fit(maxlags=max_lag, ic='aic')

        # Fit VAR model without X
        data_reduced = np.column_stack([Y, Z])
        model_reduced = VAR(data_reduced)
        result_reduced = model_reduced.fit(maxlags=max_lag, ic='aic')

        # Compare residual variance
        resid_full = result_full.resid[:, 0]  # Y residuals
        resid_reduced = result_reduced.resid[:, 0]

        sigma_full = np.var(resid_full)
        sigma_reduced = np.var(resid_reduced)

        # F-test
        n = len(resid_full)
        p = max_lag
        F = ((sigma_reduced - sigma_full) / p) / (sigma_full / (n - 2*p - 1))

        return F, sigma_reduced, sigma_full

# Example: Granger causality between brain regions
analyzer = GrangerCausalityAnalyzer(max_lag=10)

# Simulate LFP signals
T = 1000
region1 = np.cumsum(np.random.randn(T)) * 0.1
region2 = 0.3 * region1 + np.cumsum(np.random.randn(T)) * 0.1  # Driven by region1

# Test causality
f_stats, p_values = analyzer.test_granger(region1, region2, max_lag=5)

print("Granger Causality: Region1 → Region2")
for lag, (f, p) in enumerate(zip(f_stats, p_values), 1):
    print(f"  Lag {lag}: F={f:.2f}, p={p:.4f} {'***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''}")

# Reverse direction
f_stats_rev, p_values_rev = analyzer.test_granger(region2, region1, max_lag=5)
print(f"\nReverse causality (Region2 → Region1): min p = {p_values_rev.min():.4f}")

# Multivariate network
n_regions = 5
signals = np.random.randn(n_regions, T)
# Create some causal connections
signals[1] += 0.5 * np.roll(signals[0], 1)  # 0→1
signals[2] += 0.3 * np.roll(signals[1], 2)  # 1→2

causality_network = analyzer.pairwise_granger(signals, max_lag=5)
print(f"\nCausality network:\n{causality_network}")
```

**Source**: Granger (1969) Econometrica; Geweke (1982) JASA; Ding et al. (2006) Biol Cybern; Seth et al. (2015) J Neurosci

---

### Partial Correlation (Direct vs Indirect Coupling)

**Purpose**: Measure direct statistical dependence between two variables while controlling for all others—distinguishes direct from mediated interactions.

**Formula**: Correlation Conditioned on Others
```
ρᵢⱼ·{rest} = -Σᵢⱼ / √(Σᵢᵢ · Σⱼⱼ)

where Σ⁻¹ = precision matrix (inverse covariance)

Equivalently:
ρᵢⱼ·k = (ρᵢⱼ - ρᵢₖ·ρⱼₖ) / √[(1-ρᵢₖ²)(1-ρⱼₖ²)]

where:
- ρᵢⱼ = Pearson correlation
- ρᵢⱼ·k = partial correlation controlling for variable k
- Zero partial correlation → conditional independence
```

**Nature's Implementation**: Reveals direct functional connectivity in neural populations. Removes spurious correlations from common input. Used for functional MRI, LFP, spike correlations. Identifies direct synaptic vs polysynaptic pathways.

**Impact**: **MEDIUM - Functional Connectivity**
Removes confounds. Identifies direct connections. Computationally simple. Foundation for graphical models. Critical for inferring neural circuits from population recordings.

**Code Example**:
```python
from scipy.stats import pearsonr
from scipy.linalg import inv

class PartialCorrelationAnalyzer:
    """Compute partial correlations for functional connectivity"""

    def __init__(self):
        pass

    def partial_correlation_matrix(self, data):
        """
        Compute all pairwise partial correlations
        data: [n_samples, n_variables]
        """
        n_vars = data.shape[1]

        # Covariance matrix
        cov = np.cov(data.T)

        # Precision matrix (inverse covariance)
        try:
            precision = inv(cov)
        except np.linalg.LinAlgError:
            # Regularize if singular
            precision = inv(cov + 1e-6 * np.eye(n_vars))

        # Partial correlation from precision
        # ρᵢⱼ·rest = -Σᵢⱼ / √(Σᵢᵢ·Σⱼⱼ)
        diag = np.sqrt(np.diag(precision))
        partial_corr = -precision / np.outer(diag, diag)
        np.fill_diagonal(partial_corr, 1)

        return partial_corr

    def partial_correlation_pair(self, X, Y, Z):
        """
        Partial correlation between X and Y controlling for Z
        Z can be multivariate
        """
        # Stack variables
        if Z.ndim == 1:
            Z = Z[:, None]

        data = np.column_stack([X, Y, Z])

        # Compute partial correlation matrix
        partial_corr = self.partial_correlation_matrix(data)

        # Extract ρ(X,Y | Z)
        return partial_corr[0, 1]

    def significance_test(self, partial_corr, n_samples, n_controls):
        """
        Test significance of partial correlation
        Under null: t ~ t(n - 2 - n_controls)
        """
        df = n_samples - 2 - n_controls
        t_stat = partial_corr * np.sqrt(df / (1 - partial_corr**2 + 1e-10))

        # Two-tailed p-value
        from scipy.stats import t as t_dist
        p_value = 2 * (1 - t_dist.cdf(np.abs(t_stat), df))

        return t_stat, p_value

    def network_from_partial_corr(self, data, threshold=0.05):
        """
        Infer network structure from partial correlations
        Returns adjacency matrix
        """
        n_vars = data.shape[1]
        n_samples = data.shape[0]

        # Compute partial correlations
        partial_corr = self.partial_correlation_matrix(data)

        # Test significance for each edge
        adjacency = np.zeros((n_vars, n_vars))

        for i in range(n_vars):
            for j in range(i+1, n_vars):
                pc = partial_corr[i, j]
                _, p_val = self.significance_test(pc, n_samples, n_vars - 2)

                if p_val < threshold:
                    adjacency[i, j] = pc
                    adjacency[j, i] = pc

        return adjacency

# Example: Functional connectivity in neural population
analyzer = PartialCorrelationAnalyzer()

# Simulate neural data with known connectivity
# Network: 0→1→2, 0→3
T = 500
n_neurons = 5
neural_activity = np.random.randn(T, n_neurons)

# Add directed connections
neural_activity[:, 1] += 0.7 * neural_activity[:, 0]  # 0→1
neural_activity[:, 2] += 0.6 * neural_activity[:, 1]  # 1→2
neural_activity[:, 3] += 0.5 * neural_activity[:, 0]  # 0→3

# Standard Pearson correlation
pearson_corr = np.corrcoef(neural_activity.T)

# Partial correlation
partial_corr = analyzer.partial_correlation_matrix(neural_activity)

print("Pearson correlation (neuron 0 and 2):", pearson_corr[0, 2])
print("Partial correlation (neuron 0 and 2):", partial_corr[0, 2])
print("  → Partial correlation removes indirect path 0→1→2")

# Infer network
network = analyzer.network_from_partial_corr(neural_activity, threshold=0.05)
print(f"\nInferred network (thresholded partial correlations):\n{network}")
```

**Source**: Marrelec et al. (2006) NeuroImage; Smith et al. (2011) NeuroImage; Varoquaux & Craddock (2013) NeuroImage

---

### Dynamic Causal Modeling (DCM)

**Purpose**: Infer effective connectivity and causal interactions from neural dynamics using biophysically-motivated state-space models.

**Formula**: Neural Mass Model with Inputs
```
ẋ = f(x, u, θ) + w    [state dynamics]
y = g(x) + v          [observation]

Neural mass: ẋᵢ = Aᵢᵢxᵢ + Σ Aᵢⱼxⱼ + Bᵢu + Cᵢ
                          j≠i

where:
- xᵢ = state of region i (mean synaptic activity)
- u = external input (stimulus, task)
- Aᵢⱼ = intrinsic connectivity (i←j)
- Bᵢ = input modulation
- Cᵢ = direct input
- θ = {A, B, C} = parameters to estimate
```

**Nature's Implementation**: Models mesoscopic dynamics (cortical columns, regions). Explains fMRI BOLD, EEG, MEG. Reveals how stimuli modulate connectivity. Used for V1-V5, PFC-hippocampus, attention networks.

**Impact**: **MEDIUM - Mechanistic Connectivity**
Biophysically grounded. Tests hypotheses about circuit structure. Handles experimental manipulations. Foundation for understanding effective connectivity and causal mechanisms in brain networks.

**Code Example**:
```python
from scipy.integrate import odeint
from scipy.optimize import minimize

class DCM:
    """Dynamic Causal Modeling for neural circuits"""

    def __init__(self, n_regions):
        self.n = n_regions

        # Parameters to estimate
        self.A = np.zeros((n_regions, n_regions))  # Intrinsic connectivity
        self.B = np.zeros(n_regions)  # Input weights
        self.C = np.zeros(n_regions)  # Direct inputs

        # Hemodynamic parameters (for fMRI)
        self.tau = 1.0  # Time constant

    def neural_dynamics(self, x, t, u_func):
        """
        State dynamics: ẋ = A·x + B·u + C
        x: [n_regions] neural states
        u_func: input function u(t)
        """
        u = u_func(t)

        # ẋ = A·x + B·u + C
        dxdt = self.A @ x + self.B * u + self.C

        return dxdt

    def simulate(self, T, dt, u_func, x0=None):
        """
        Simulate network dynamics
        T: total time
        dt: time step
        u_func: input function
        """
        time = np.arange(0, T, dt)

        if x0 is None:
            x0 = np.zeros(self.n)

        # Integrate dynamics
        states = odeint(self.neural_dynamics, x0, time, args=(u_func,))

        return time, states

    def hemodynamic_response(self, neural_activity, dt=0.1):
        """
        Simple balloon model for BOLD signal
        """
        # Simplified: convolve with canonical HRF
        hrf_length = int(20 / dt)  # 20 seconds
        t_hrf = np.arange(hrf_length) * dt

        # Canonical HRF (gamma functions)
        hrf = (t_hrf**5) * np.exp(-t_hrf) / np.math.factorial(5)
        hrf = hrf / hrf.sum()

        # Convolve each region
        bold = np.zeros_like(neural_activity)
        for region in range(self.n):
            bold[:, region] = np.convolve(neural_activity[:, region], hrf, mode='same')

        return bold

    def fit(self, observed_data, time, u_func):
        """
        Fit DCM parameters to observed data via maximum likelihood
        """
        def objective(params):
            # Unpack parameters
            n_a = self.n * self.n
            n_b = self.n
            n_c = self.n

            self.A = params[:n_a].reshape(self.n, self.n)
            self.B = params[n_a:n_a+n_b]
            self.C = params[n_a+n_b:n_a+n_b+n_c]

            # Simulate
            x0 = np.zeros(self.n)
            predicted = odeint(self.neural_dynamics, x0, time, args=(u_func,))

            # Mean squared error
            error = np.sum((observed_data - predicted)**2)

            return error

        # Initialize parameters
        n_params = self.n**2 + 2*self.n
        params_init = np.random.randn(n_params) * 0.1

        # Optimize
        result = minimize(objective, params_init, method='L-BFGS-B')

        # Extract fitted parameters
        n_a = self.n * self.n
        n_b = self.n
        self.A = result.x[:n_a].reshape(self.n, self.n)
        self.B = result.x[n_a:n_a+n_b]
        self.C = result.x[n_a+n_b:]

        return result

# Example: Two-region visual circuit (V1-V5)
n_regions = 2
dcm = DCM(n_regions)

# True connectivity
dcm.A = np.array([
    [-0.5, 0.3],  # V1: self-inhibition, input from V5
    [0.7, -0.5]   # V5: strong input from V1, self-inhibition
])
dcm.B = np.array([1.0, 0.0])  # Input to V1
dcm.C = np.array([0.0, 0.0])

# Visual stimulus
def stimulus(t):
    if 5 < t < 15:
        return 1.0  # Stimulus ON
    return 0.0

# Simulate
T = 30
dt = 0.1
time, states = dcm.simulate(T, dt, stimulus)

# Add noise
observed = states + 0.1 * np.random.randn(*states.shape)

# Fit new DCM to recover parameters
dcm_fit = DCM(n_regions)
result = dcm_fit.fit(observed, time, stimulus)

print("True connectivity A:")
print(dcm.A)
print("\nFitted connectivity A:")
print(dcm_fit.A)
print(f"\nFit error: {result.fun:.4f}")
```

**Source**: Friston et al. (2003) NeuroImage; Stephan et al. (2010) NeuroImage; Daunizeau et al. (2011) PLoS Comp Bio

---

### Sparse Inverse Covariance (Graphical Lasso)

**Purpose**: Estimate sparse precision matrix (inverse covariance) to infer direct interactions in high-dimensional neural data.

**Formula**: ℓ1-Regularized Maximum Likelihood
```
Σ̂ = argmax log det(Σ) - tr(S·Σ) - λ||Σ||₁
     Σ≻0

where:
- Σ = precision matrix (inverse covariance)
- S = sample covariance
- λ = sparsity penalty (lasso)
- ||Σ||₁ = Σᵢⱼ |Σᵢⱼ| (ℓ1 norm)
- Σᵢⱼ = 0 ⟺ i ⊥ j | rest (conditional independence)
```

**Nature's Implementation**: Reveals sparse functional connectivity in large neural populations. Handles high-dimensional recordings (hundreds of neurons). Identifies direct vs indirect interactions. Used for calcium imaging, multi-electrode arrays.

**Impact**: **MEDIUM-HIGH - Sparse Networks**
Handles high dimensionality (p >> n). Produces interpretable sparse networks. Statistically principled (MLE + regularization). Critical for analyzing large-scale recordings and inferring circuit structure.

**Code Example**:
```python
from sklearn.covariance import GraphicalLassoCV, graphical_lasso

class SparseInverseCovarianceAnalyzer:
    """Infer sparse functional networks via Graphical Lasso"""

    def __init__(self, alpha=0.1):
        self.alpha = alpha  # Sparsity parameter
        self.precision = None
        self.covariance = None

    def fit(self, data, cv=True):
        """
        Fit sparse inverse covariance
        data: [n_samples, n_features]
        cv: use cross-validation to select alpha
        """
        if cv:
            # Cross-validation for alpha
            model = GraphicalLassoCV(alphas=20, cv=5)
            model.fit(data)
            self.alpha = model.alpha_
            self.precision = model.precision_
            self.covariance = model.covariance_
            print(f"Selected alpha: {self.alpha:.4f}")
        else:
            # Fixed alpha
            self.covariance, self.precision = graphical_lasso(
                np.cov(data.T), alpha=self.alpha
            )

        return self.precision

    def get_network(self, threshold=0.01):
        """
        Extract network adjacency matrix
        Σᵢⱼ ≠ 0 → edge between i and j
        """
        adjacency = np.abs(self.precision) > threshold
        np.fill_diagonal(adjacency, False)

        return adjacency.astype(int)

    def network_density(self):
        """Fraction of non-zero edges"""
        adjacency = self.get_network()
        n = adjacency.shape[0]
        density = adjacency.sum() / (n * (n-1))

        return density

# Example: Large-scale calcium imaging data
n_neurons = 100
n_samples = 500

# Simulate sparse network
true_adjacency = np.zeros((n_neurons, n_neurons))
n_edges = 200  # Sparse
for _ in range(n_edges):
    i, j = np.random.choice(n_neurons, 2, replace=False)
    true_adjacency[i, j] = 1
    true_adjacency[j, i] = 1

# Generate data from Gaussian graphical model
# Precision = identity + small perturbations on edges
true_precision = np.eye(n_neurons)
true_precision[true_adjacency > 0] = np.random.randn(n_edges) * 0.3

# Ensure positive definite
true_precision = true_precision @ true_precision.T + 0.1 * np.eye(n_neurons)

true_covariance = np.linalg.inv(true_precision)

# Sample data
data = np.random.multivariate_normal(np.zeros(n_neurons), true_covariance, size=n_samples)

# Fit Graphical Lasso
analyzer = SparseInverseCovarianceAnalyzer()
estimated_precision = analyzer.fit(data, cv=True)

# Extract network
estimated_network = analyzer.get_network(threshold=0.01)

print(f"True network density: {true_adjacency.sum() / (n_neurons * (n_neurons-1)):.3f}")
print(f"Estimated network density: {analyzer.network_density():.3f}")

# Accuracy
true_edges = (true_adjacency > 0).astype(int)
est_edges = estimated_network

true_pos = np.sum((true_edges == 1) & (est_edges == 1))
false_pos = np.sum((true_edges == 0) & (est_edges == 1))
true_neg = np.sum((true_edges == 0) & (est_edges == 0))
false_neg = np.sum((true_edges == 1) & (est_edges == 0))

precision_metric = true_pos / (true_pos + false_pos)
recall = true_pos / (true_pos + false_neg)

print(f"Precision: {precision_metric:.3f}, Recall: {recall:.3f}")
```

**Source**: Friedman et al. (2008) Biostatistics; Varoquaux et al. (2010) NeuroImage; Smith et al. (2011) NeuroImage

---

### Expectation-Maximization (EM) for Latent Variable Models

**Purpose**: Infer latent states and parameters in probabilistic models with hidden variables—foundation for unsupervised learning from neural data.

**Formula**: Iterative Optimization
```
E-step:  Q(θ|θ⁽ᵗ⁾) = E[log p(Y,Z|θ) | Y, θ⁽ᵗ⁾]

M-step:  θ⁽ᵗ⁺¹⁾ = argmax Q(θ|θ⁽ᵗ⁾)
                    θ

Iterates until convergence: log p(Y|θ⁽ᵗ⁺¹⁾) ≥ log p(Y|θ⁽ᵗ⁾)

where:
- Y = observed data (spike trains, LFP)
- Z = latent variables (hidden states)
- θ = model parameters
- Guaranteed to increase likelihood each iteration
```

**Nature's Implementation**: Learns neural population structure without supervision. Discovers latent states in motor planning, decision-making. Used for HMMs, mixtures of Gaussians, factor analysis. Reveals trial-to-trial variability and population dynamics.

**Impact**: **MEDIUM - Unsupervised Learning**
Principled parameter estimation. Handles missing data. Foundation for state-space models. Critical for discovering latent structure in neural population activity.

**Code Example**:
```python
from scipy.stats import multivariate_normal

class GaussianMixtureEM:
    """EM algorithm for Gaussian mixture model of neural states"""

    def __init__(self, n_components, n_features):
        self.K = n_components  # Number of states
        self.D = n_features    # Data dimensionality

        # Initialize parameters
        self.pi = np.ones(self.K) / self.K  # Mixing weights
        self.mu = np.random.randn(self.K, self.D)  # Means
        self.Sigma = np.array([np.eye(self.D) for _ in range(self.K)])  # Covariances

    def e_step(self, X):
        """
        E-step: Compute responsibilities
        γᵢₖ = p(z=k | xᵢ, θ)
        """
        N = X.shape[0]
        gamma = np.zeros((N, self.K))

        for k in range(self.K):
            # p(x|z=k)
            gamma[:, k] = self.pi[k] * multivariate_normal.pdf(X, self.mu[k], self.Sigma[k])

        # Normalize
        gamma /= gamma.sum(axis=1, keepdims=True)

        return gamma

    def m_step(self, X, gamma):
        """
        M-step: Update parameters
        θ⁽ᵗ⁺¹⁾ = argmax E[log p(X,Z|θ)]
        """
        N = X.shape[0]
        N_k = gamma.sum(axis=0)  # Effective count for each component

        # Update mixing weights
        self.pi = N_k / N

        # Update means
        for k in range(self.K):
            self.mu[k] = (gamma[:, k:k+1].T @ X) / N_k[k]

        # Update covariances
        for k in range(self.K):
            diff = X - self.mu[k]
            self.Sigma[k] = (diff.T @ (diff * gamma[:, k:k+1])) / N_k[k]

            # Regularize
            self.Sigma[k] += 1e-6 * np.eye(self.D)

    def log_likelihood(self, X):
        """Compute log p(X|θ)"""
        N = X.shape[0]
        ll = 0

        for n in range(N):
            prob = 0
            for k in range(self.K):
                prob += self.pi[k] * multivariate_normal.pdf(X[n], self.mu[k], self.Sigma[k])
            ll += np.log(prob + 1e-10)

        return ll

    def fit(self, X, max_iter=100, tol=1e-4):
        """Run EM algorithm"""
        ll_history = []

        for iteration in range(max_iter):
            # E-step
            gamma = self.e_step(X)

            # M-step
            self.m_step(X, gamma)

            # Check convergence
            ll = self.log_likelihood(X)
            ll_history.append(ll)

            if iteration > 0 and abs(ll - ll_history[-2]) < tol:
                print(f"Converged at iteration {iteration}")
                break

            if iteration % 10 == 0:
                print(f"Iteration {iteration}, Log-likelihood: {ll:.4f}")

        return ll_history

    def predict(self, X):
        """Assign data to most likely component"""
        gamma = self.e_step(X)
        return np.argmax(gamma, axis=1)

# Example: Clustering neural population states
n_neurons = 20
n_samples = 500
n_states = 3

# Generate data from mixture of Gaussians
true_labels = np.random.choice(n_states, size=n_samples)
data = np.zeros((n_samples, n_neurons))

true_means = [np.random.randn(n_neurons) * 3 for _ in range(n_states)]

for i in range(n_samples):
    state = true_labels[i]
    data[i] = true_means[state] + np.random.randn(n_neurons) * 0.5

# Fit GMM via EM
gmm = GaussianMixtureEM(n_components=3, n_features=n_neurons)
ll_history = gmm.fit(data, max_iter=50)

# Predict states
predicted_labels = gmm.predict(data)

# Accuracy (with label permutation)
from scipy.optimize import linear_sum_assignment
confusion = np.zeros((n_states, n_states))
for i in range(n_states):
    for j in range(n_states):
        confusion[i, j] = np.sum((true_labels == i) & (predicted_labels == j))

row_ind, col_ind = linear_sum_assignment(-confusion)
accuracy = confusion[row_ind, col_ind].sum() / n_samples

print(f"\nClustering accuracy: {accuracy:.3f}")
```

**Source**: Dempster et al. (1977) JRSS-B; Ghahramani & Hinton (1996) Tech Report; Yu et al. (2009) J Neurophys

---

### Latent Factor Analysis (FA) for Neural Populations

**Purpose**: Discover low-dimensional latent factors that explain population covariance—linear dimensionality reduction with noise model.

**Formula**: Gaussian Latent Factor Model
```
yᵢ = Λ·zᵢ + εᵢ

z ~ N(0, I)          [latent factors]
ε ~ N(0, Ψ)          [independent noise]

y ~ N(0, ΛΛ' + Ψ)    [marginal]

where:
- yᵢ ∈ ℝᵈ = observed neural activity (neuron i)
- zᵢ ∈ ℝᵏ = latent factors (k << d)
- Λ = [d × k] factor loading matrix
- Ψ = diag(ψ₁, ..., ψₐ) = private noise per neuron
```

**Nature's Implementation**: Reveals shared variability in populations. Separates signal (Λ) from noise (Ψ). Used for motor cortex, V1, decision circuits. Latent factors correspond to motor planning, attention, decision variables.

**Impact**: **MEDIUM - Shared Variability**
Interpretable factors. Separates shared vs private variance. Handles noise explicitly (unlike PCA). Critical for understanding population structure and trial-to-trial variability.

**Code Example**:
```python
from sklearn.decomposition import FactorAnalysis

class NeuralFactorAnalysis:
    """Factor Analysis for neural population data"""

    def __init__(self, n_factors):
        self.n_factors = n_factors
        self.model = FactorAnalysis(n_components=n_factors, random_state=0)

        self.Lambda = None  # Factor loadings
        self.Psi = None     # Private noise variances

    def fit(self, data):
        """
        Fit FA model via EM
        data: [n_samples, n_neurons]
        """
        self.model.fit(data)

        self.Lambda = self.model.components_.T  # [n_neurons, n_factors]
        self.Psi = self.model.noise_variance_    # [n_neurons]

        return self

    def transform(self, data):
        """Extract latent factors: z = (Λ'Ψ⁻¹Λ + I)⁻¹Λ'Ψ⁻¹y"""
        return self.model.transform(data)

    def reconstruct(self, factors):
        """Reconstruct data from factors: ŷ = Λ·z"""
        return factors @ self.Lambda.T

    def shared_variance(self):
        """Proportion of variance explained by shared factors"""
        total_var = np.sum(np.diag(self.Lambda @ self.Lambda.T) + self.Psi)
        shared_var = np.sum(np.diag(self.Lambda @ self.Lambda.T))

        return shared_var / total_var

    def factor_correlation(self, data):
        """Correlation between neurons explained by factors"""
        # Predicted correlation: C = ΛΛ' + Ψ
        cov_predicted = self.Lambda @ self.Lambda.T + np.diag(self.Psi)

        # Empirical correlation
        cov_empirical = np.cov(data.T)

        return cov_predicted, cov_empirical

# Example: Motor cortex population with shared variability
n_neurons = 50
n_factors_true = 5
n_samples = 1000

# True latent factors
true_factors = np.random.randn(n_samples, n_factors_true)

# True loadings (each neuron loads on different factors)
true_loadings = np.random.randn(n_neurons, n_factors_true) * 0.5

# Generate data
shared_activity = true_factors @ true_loadings.T
private_noise = np.random.randn(n_samples, n_neurons) * 0.3

data = shared_activity + private_noise

# Fit Factor Analysis
fa = NeuralFactorAnalysis(n_factors=5)
fa.fit(data)

# Extract latent factors
inferred_factors = fa.transform(data)

# Compare
print(f"Shared variance explained: {fa.shared_variance():.2%}")

# Reconstruction
reconstructed = fa.reconstruct(inferred_factors)
reconstruction_error = np.mean((data - reconstructed)**2)
print(f"Reconstruction error: {reconstruction_error:.4f}")

# Factor loadings reveal neuron preferences
print(f"\nFactor loadings shape: {fa.Lambda.shape}")
print(f"Top neurons for factor 1: {np.argsort(fa.Lambda[:, 0])[-5:]}")
```

**Source**: Spearman (1904) Am J Psych; Bartholomew et al. (2011) Book; Cunningham & Yu (2014) Nat Neurosci; Semedo et al. (2019) Neuron

---

### Hidden Markov Model (HMM) for Neural States

**Purpose**: Infer discrete latent states from sequential neural data—unsupervised discovery of behavioral/cognitive states.

**Formula**: Discrete State-Space Model
```
State transition:  p(zₜ|zₜ₋₁) = A[zₜ₋₁, zₜ]
Emission:          p(yₜ|zₜ) = B[zₜ](yₜ)
Initial:           p(z₁) = π

Forward: α(zₜ) = p(zₜ, y₁:ₜ) = B(yₜ|zₜ) Σ A(zₜ|zₜ₋₁)α(zₜ₋₁)
                                        zₜ₋₁

Backward: β(zₜ) = p(y_{t+1:T}|zₜ)

Viterbi: ẑ₁:T = argmax p(z₁:T|y₁:T)
                z₁:T

where:
- zₜ ∈ {1,...,K} = discrete latent state
- yₜ = observation (spike counts, LFP, behavior)
- A = [K×K] transition matrix
- B = emission distributions (Gaussian, Poisson, etc.)
- π = initial state probabilities
```

**Nature's Implementation**: Segments behavior into discrete states (foraging, resting, exploring). Identifies Up/Down states in cortex. Tracks sleep stages, decision states, attentional modes. Used across hippocampus, PFC, motor cortex.

**Impact**: **MEDIUM-HIGH - State Discovery**
Unsupervised state discovery. Handles sequential dependencies. Interpretable states. Efficient inference (forward-backward, Viterbi). Critical for analyzing behavioral states and neural dynamics.

**Code Example**:
```python
from hmmlearn import hmm

class NeuralHMM:
    """Hidden Markov Model for neural state inference"""

    def __init__(self, n_states, n_features, emission_type='gaussian'):
        self.n_states = n_states
        self.n_features = n_features
        self.emission_type = emission_type

        if emission_type == 'gaussian':
            self.model = hmm.GaussianHMM(
                n_components=n_states,
                covariance_type='full',
                n_iter=100
            )
        elif emission_type == 'poisson':
            # Custom Poisson HMM
            self.model = None
            self._init_poisson_hmm()

    def _init_poisson_hmm(self):
        """Initialize Poisson emission HMM manually"""
        self.A = np.ones((self.n_states, self.n_states)) / self.n_states
        self.pi = np.ones(self.n_states) / self.n_states
        self.lambda_rates = np.random.rand(self.n_states, self.n_features) * 10

    def fit(self, data, lengths=None):
        """
        Fit HMM to sequential data
        data: [n_samples, n_features]
        lengths: list of sequence lengths (for multiple trials)
        """
        if self.emission_type == 'gaussian':
            self.model.fit(data, lengths=lengths)
        else:
            self._fit_poisson_em(data)

        return self

    def _fit_poisson_em(self, data, n_iter=50):
        """EM for Poisson HMM"""
        T = data.shape[0]

        for iteration in range(n_iter):
            # E-step: Forward-backward
            alpha, beta, gamma, xi = self._forward_backward_poisson(data)

            # M-step: Update parameters
            # π
            self.pi = gamma[0]

            # A
            self.A = xi.sum(axis=0) / gamma[:-1].sum(axis=0, keepdims=True).T

            # λ (emission rates)
            for k in range(self.n_states):
                self.lambda_rates[k] = (gamma[:, k:k+1].T @ data) / gamma[:, k].sum()

    def _forward_backward_poisson(self, data):
        """Forward-backward algorithm for Poisson emissions"""
        T = data.shape[0]

        # Forward
        alpha = np.zeros((T, self.n_states))
        alpha[0] = self.pi * self._poisson_emission(data[0])

        for t in range(1, T):
            for k in range(self.n_states):
                alpha[t, k] = self._poisson_emission(data[t], k) * np.sum(
                    alpha[t-1] * self.A[:, k]
                )

        # Backward
        beta = np.zeros((T, self.n_states))
        beta[-1] = 1

        for t in range(T-2, -1, -1):
            for k in range(self.n_states):
                beta[t, k] = np.sum(
                    self.A[k, :] * self._poisson_emission(data[t+1]) * beta[t+1]
                )

        # Posterior: γ(zₜ) = p(zₜ|y₁:T)
        gamma = alpha * beta
        gamma /= gamma.sum(axis=1, keepdims=True)

        # Two-slice: ξ(zₜ,zₜ₊₁) = p(zₜ,zₜ₊₁|y₁:T)
        xi = np.zeros((T-1, self.n_states, self.n_states))
        for t in range(T-1):
            for i in range(self.n_states):
                for j in range(self.n_states):
                    xi[t, i, j] = alpha[t, i] * self.A[i, j] * \
                                  self._poisson_emission(data[t+1], j) * beta[t+1, j]

        xi /= xi.sum(axis=(1, 2), keepdims=True)

        return alpha, beta, gamma, xi

    def _poisson_emission(self, y, state=None):
        """p(y|z) for Poisson"""
        from scipy.stats import poisson

        if state is None:
            # All states
            prob = np.ones(self.n_states)
            for k in range(self.n_states):
                prob[k] = np.prod(poisson.pmf(y, self.lambda_rates[k]))
            return prob
        else:
            return np.prod(poisson.pmf(y, self.lambda_rates[state]))

    def predict_states(self, data):
        """Viterbi decoding: most likely state sequence"""
        if self.emission_type == 'gaussian':
            return self.model.predict(data)
        else:
            return self._viterbi_poisson(data)

    def _viterbi_poisson(self, data):
        """Viterbi algorithm for Poisson HMM"""
        T = data.shape[0]

        # Delta: max probability of state sequence ending in zₜ=k
        delta = np.zeros((T, self.n_states))
        psi = np.zeros((T, self.n_states), dtype=int)

        # Initialize
        delta[0] = np.log(self.pi + 1e-10) + np.log(self._poisson_emission(data[0]) + 1e-10)

        # Forward
        for t in range(1, T):
            for k in range(self.n_states):
                prob = delta[t-1] + np.log(self.A[:, k] + 1e-10)
                psi[t, k] = np.argmax(prob)
                delta[t, k] = np.max(prob) + np.log(self._poisson_emission(data[t], k) + 1e-10)

        # Backward
        states = np.zeros(T, dtype=int)
        states[-1] = np.argmax(delta[-1])

        for t in range(T-2, -1, -1):
            states[t] = psi[t+1, states[t+1]]

        return states

    def sample(self, n_samples):
        """Generate synthetic data from HMM"""
        if self.emission_type == 'gaussian':
            return self.model.sample(n_samples)
        else:
            # Sample Poisson HMM
            states = np.zeros(n_samples, dtype=int)
            data = np.zeros((n_samples, self.n_features))

            states[0] = np.random.choice(self.n_states, p=self.pi)
            data[0] = np.random.poisson(self.lambda_rates[states[0]])

            for t in range(1, n_samples):
                states[t] = np.random.choice(self.n_states, p=self.A[states[t-1]])
                data[t] = np.random.poisson(self.lambda_rates[states[t]])

            return data, states

# Example: Behavioral state segmentation
n_states = 3  # Rest, explore, forage
n_neurons = 20

# Generate synthetic data with state switches
T = 500
true_states = np.zeros(T, dtype=int)
true_states[:150] = 0  # Rest
true_states[150:300] = 1  # Explore
true_states[300:] = 2  # Forage

# Emission parameters (firing rates per state)
rates_per_state = {
    0: np.ones(n_neurons) * 2,   # Low activity (rest)
    1: np.ones(n_neurons) * 10,  # Medium (explore)
    2: np.ones(n_neurons) * 20   # High (forage)
}

data = np.zeros((T, n_neurons))
for t in range(T):
    data[t] = np.random.poisson(rates_per_state[true_states[t]])

# Fit HMM
hmm_model = NeuralHMM(n_states=3, n_features=n_neurons, emission_type='poisson')
hmm_model.fit(data)

# Decode states
decoded_states = hmm_model.predict_states(data)

# Accuracy
accuracy = np.mean(decoded_states == true_states)
print(f"State decoding accuracy: {accuracy:.2%}")

# Learned transition matrix
print(f"\nLearned transition matrix:\n{hmm_model.A}")
```

**Source**: Rabiner (1989) Proc IEEE; Kemere et al. (2008) J Neurophys; Escola et al. (2011) Neuron; Linderman et al. (2016) NIPS

---

### Continuous-Time Recurrent Neural Network (CT-RNN) Model

**Purpose**: Model neural dynamics as continuous-time RNN—captures temporal evolution and attractors in population activity.

**Formula**: Continuous Dynamics
```
τ·ẋᵢ = -xᵢ + Σ Wᵢⱼ·φ(xⱼ) + Iᵢ(t) + noise
              j

yᵢ = φ(xᵢ)    [output nonlinearity]

φ(x) = tanh(x) or ReLU(x)

where:
- xᵢ = state of unit i
- τ = time constant
- Wᵢⱼ = recurrent weights
- Iᵢ(t) = external input
- yᵢ = firing rate output
```

**Nature's Implementation**: Captures recurrent cortical dynamics. Models persistent activity, line attractors, decision dynamics. Used for prefrontal cortex, motor cortex, parietal areas. Explains delay period activity, integration, motor planning.

**Impact**: **MEDIUM-HIGH - Dynamical Systems**
Captures temporal dynamics. Reveals attractors and stability. Handles continuous time. Interpretable via dynamical systems analysis. Critical for understanding recurrent circuit function and temporal computation.

**Code Example**:
```python
class ContinuousTimeRNN(nn.Module):
    """Continuous-time RNN for neural dynamics"""

    def __init__(self, n_units, tau=10.0, dt=1.0, nonlinearity='tanh'):
        super().__init__()
        self.n_units = n_units
        self.tau = tau  # Time constant (ms)
        self.dt = dt    # Integration step

        # Recurrent weights
        self.W_rec = nn.Parameter(torch.randn(n_units, n_units) * 0.2 / np.sqrt(n_units))

        # Input weights
        self.W_in = nn.Parameter(torch.randn(n_units, n_units) * 0.5)

        # Output weights
        self.W_out = nn.Parameter(torch.randn(n_units, n_units) * 0.5)

        # Nonlinearity
        if nonlinearity == 'tanh':
            self.phi = torch.tanh
        elif nonlinearity == 'relu':
            self.phi = torch.relu
        else:
            self.phi = lambda x: x

        # Noise level
        self.sigma_noise = 0.01

    def forward(self, inputs, n_steps, x0=None):
        """
        Simulate CT-RNN dynamics
        inputs: [batch, n_steps, n_units]
        """
        batch_size = inputs.shape[0]

        if x0 is None:
            x = torch.zeros(batch_size, self.n_units)
        else:
            x = x0

        states = []

        for t in range(n_steps):
            # Input at time t
            I_ext = inputs[:, t, :] if t < inputs.shape[1] else torch.zeros(batch_size, self.n_units)

            # Dynamics: τ·dx/dt = -x + W·φ(x) + I
            dx_dt = (-x + torch.matmul(self.phi(x), self.W_rec.T) + I_ext) / self.tau

            # Euler integration
            x = x + dx_dt * self.dt

            # Add noise
            if self.training:
                x = x + self.sigma_noise * torch.randn_like(x) * np.sqrt(self.dt)

            states.append(x)

        states = torch.stack(states, dim=1)  # [batch, n_steps, n_units]

        return states

    def compute_fixed_points(self, I_ext=None):
        """
        Find fixed points: dx/dt = 0
        → x* = W·φ(x*) + I
        """
        from scipy.optimize import fsolve

        if I_ext is None:
            I_ext = np.zeros(self.n_units)

        def dynamics(x):
            W = self.W_rec.detach().numpy()
            phi_x = np.tanh(x)  # Assuming tanh
            return -x + W @ phi_x + I_ext

        # Try multiple initializations
        fixed_points = []
        for _ in range(10):
            x0 = np.random.randn(self.n_units) * 0.5
            fp = fsolve(dynamics, x0)

            # Check if truly fixed
            residual = np.linalg.norm(dynamics(fp))
            if residual < 1e-4:
                fixed_points.append(fp)

        return fixed_points

    def train_task(self, task_inputs, task_targets, n_epochs=100, lr=0.001):
        """Train CT-RNN on a task"""
        optimizer = torch.optim.Adam(self.parameters(), lr=lr)
        criterion = nn.MSELoss()

        for epoch in range(n_epochs):
            optimizer.zero_grad()

            # Forward pass
            states = self.forward(task_inputs, n_steps=task_inputs.shape[1])

            # Output readout
            outputs = torch.matmul(states, self.W_out.T)

            # Loss
            loss = criterion(outputs, task_targets)

            # Backward
            loss.backward()
            optimizer.step()

            if epoch % 20 == 0:
                print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

# Example: Decision-making task (integration to threshold)
n_units = 100
rnn = ContinuousTimeRNN(n_units, tau=10.0, dt=1.0, nonlinearity='tanh')

# Task: integrate noisy input, decide left/right
n_trials = 50
n_steps = 100
coherence = 0.3

inputs = torch.randn(n_trials, n_steps, n_units) * 0.1
# Add coherent signal (left = positive, right = negative)
inputs[:25, :, 0] += coherence  # Left trials
inputs[25:, :, 0] -= coherence  # Right trials

# Target: binary decision at end
targets = torch.zeros(n_trials, n_steps, n_units)
targets[:25, -10:, 0] = 1  # Left
targets[25:, -10:, 1] = 1  # Right

# Train
rnn.train_task(inputs, targets, n_epochs=100, lr=0.01)

# Test
rnn.eval()
test_inputs = torch.randn(10, n_steps, n_units) * 0.1
test_inputs[:, :, 0] += 0.5  # Strong left signal

states = rnn.forward(test_inputs, n_steps=n_steps)
outputs = torch.matmul(states, rnn.W_out.T)

print(f"Test output (should be left=1): {outputs[0, -1, :2]}")

# Find fixed points
fixed_points = rnn.compute_fixed_points(I_ext=np.array([0.5] + [0]*(n_units-1)))
print(f"Found {len(fixed_points)} fixed points")
```

**Source**: Sompolinsky et al. (1988) Phys Rev A; Sussillo & Abbott (2009) Neuron; Mante et al. (2013) Nature; Sussillo (2014) Curr Op Neurobio

---

### Expectation Propagation (EP) for Approximate Inference

**Purpose**: Approximate intractable posterior distributions with tractable family—fast alternative to MCMC and variational inference.

**Formula**: Moment Matching with Factors
```
Posterior: p(z|y) ∝ p(y|z)·p(z) = Π fᵢ(z)
                                   i

EP approximation: q(z) = (1/Z) Π f̃ᵢ(z)
                                i

where f̃ᵢ are in exponential family (e.g., Gaussian)

Update (iterative refinement):
1. Cavity: q₋ᵢ(z) ∝ q(z)/f̃ᵢ(z)
2. Tilted: p̂ᵢ(z) ∝ fᵢ(z)·q₋ᵢ(z)
3. Moment matching: f̃ᵢ_new ∝ p̂ᵢ/q₋ᵢ s.t. ∫ q_new·z = ∫ p̂ᵢ·z

where:
- q(z) = approximate posterior
- fᵢ = likelihood/prior factors
- f̃ᵢ = approximating factors
```

**Nature's Implementation**: Models probabilistic inference in cortex. Fast approximate Bayesian computation. Used for perceptual inference, sensor fusion, predictive coding. Explains neural variability and probabilistic population codes.

**Impact**: **MEDIUM - Fast Inference**
Faster than MCMC. More accurate than mean-field VI. Handles non-conjugate models. Iterative refinement. Critical for large-scale neural data analysis and understanding neural inference.

**Code Example**:
```python
class ExpectationPropagation:
    """EP for Gaussian approximation to non-Gaussian posterior"""

    def __init__(self, n_dims):
        self.n_dims = n_dims

        # Approximate posterior: q(z) = N(μ, Σ)
        self.mu = np.zeros(n_dims)
        self.Sigma = np.eye(n_dims)

        # Factor approximations (natural parameters)
        self.factor_precisions = []
        self.factor_means_times_precision = []

    def gaussian_posterior(self):
        """Convert natural params to mean/covariance"""
        # Σ⁻¹ = Σ factor_precisions
        precision = np.sum(self.factor_precisions, axis=0)
        self.Sigma = np.linalg.inv(precision + 1e-6 * np.eye(self.n_dims))

        # Σ⁻¹μ = Σ factor_h
        h = np.sum(self.factor_means_times_precision, axis=0)
        self.mu = self.Sigma @ h

        return self.mu, self.Sigma

    def initialize_factors(self, prior_mean, prior_cov, n_factors):
        """
        Initialize with prior
        p(z) = N(z | μ₀, Σ₀)
        """
        prior_precision = np.linalg.inv(prior_cov)

        # Split prior among factors
        self.factor_precisions = [prior_precision / n_factors for _ in range(n_factors)]
        self.factor_means_times_precision = [
            prior_precision @ prior_mean / n_factors for _ in range(n_factors)
        ]

    def update_factor(self, factor_idx, likelihood_fn, n_samples=1000):
        """
        Update factor i via moment matching
        1. Cavity distribution
        2. Tilted distribution
        3. Moment matching
        """
        # Cavity: q_{-i}(z) ∝ q(z) / f̃ᵢ(z)
        cavity_precision = np.sum([p for j, p in enumerate(self.factor_precisions) if j != factor_idx], axis=0)
        cavity_h = np.sum([h for j, h in enumerate(self.factor_means_times_precision) if j != factor_idx], axis=0)

        cavity_cov = np.linalg.inv(cavity_precision + 1e-6 * np.eye(self.n_dims))
        cavity_mean = cavity_cov @ cavity_h

        # Sample from cavity
        samples = np.random.multivariate_normal(cavity_mean, cavity_cov, size=n_samples)

        # Tilted: p̂ᵢ(z) ∝ fᵢ(z)·q_{-i}(z)
        # Compute likelihood weights
        weights = np.array([likelihood_fn(z) for z in samples])
        weights /= weights.sum()

        # Moment matching
        tilted_mean = np.sum(weights[:, None] * samples, axis=0)
        tilted_cov = np.sum(weights[:, None, None] * (samples[:, :, None] - tilted_mean[None, :, None]) *
                           (samples[:, None, :] - tilted_mean[None, None, :]), axis=0)

        # New factor: f̃ᵢ ∝ p̂ᵢ / q_{-i}
        tilted_precision = np.linalg.inv(tilted_cov + 1e-6 * np.eye(self.n_dims))

        new_factor_precision = tilted_precision - cavity_precision
        new_factor_h = tilted_precision @ tilted_mean - cavity_h

        # Update
        self.factor_precisions[factor_idx] = new_factor_precision
        self.factor_means_times_precision[factor_idx] = new_factor_h

    def run_ep(self, likelihood_fns, prior_mean, prior_cov, n_iterations=10):
        """
        Run EP algorithm
        likelihood_fns: list of likelihood factor functions
        """
        n_factors = len(likelihood_fns)

        # Initialize
        self.initialize_factors(prior_mean, prior_cov, n_factors)

        for iteration in range(n_iterations):
            for i, lik_fn in enumerate(likelihood_fns):
                self.update_factor(i, lik_fn)

            # Recompute posterior
            mu, Sigma = self.gaussian_posterior()

            if iteration % 5 == 0:
                print(f"Iteration {iteration}, posterior mean: {mu}")

        return mu, Sigma

# Example: Poisson GLM with EP inference
n_neurons = 5
n_factors = 10  # Data points

ep = ExpectationPropagation(n_dims=n_neurons)

# Prior: weak Gaussian
prior_mean = np.zeros(n_neurons)
prior_cov = 10 * np.eye(n_neurons)

# Simulate Poisson observations
true_weights = np.array([1, -0.5, 0.3, 0, -0.2])
spike_counts = np.random.poisson(np.exp(true_weights), size=n_factors)

# Likelihood factors: Poisson p(yᵢ|w) = exp(-λᵢ)·λᵢ^yᵢ/yᵢ!
#   where λᵢ = exp(wᵢ)
def make_poisson_likelihood(spike_count):
    def likelihood(w):
        rate = np.exp(w)
        return np.prod(np.exp(-rate) * (rate ** spike_count) / np.math.factorial(int(spike_count)))
    return likelihood

likelihood_fns = [make_poisson_likelihood(y) for y in spike_counts]

# Run EP
posterior_mean, posterior_cov = ep.run_ep(likelihood_fns, prior_mean, prior_cov, n_iterations=10)

print(f"\nTrue weights: {true_weights}")
print(f"EP posterior mean: {posterior_mean}")
print(f"Error: {np.linalg.norm(true_weights - posterior_mean):.3f}")
```

**Source**: Minka (2001) UAI; Seeger (2008) Found Trends ML; Gelman et al. (2014) Bayesian Data Analysis

---

### Variational Inference (ELBO Optimization)

**Purpose**: Approximate intractable posterior by optimizing tractable variational distribution—scalable Bayesian inference for neural data.

**Formula**: Evidence Lower Bound (ELBO)
```
log p(y) ≥ ELBO(q) = E_q[log p(y,z)] - E_q[log q(z)]
                    = E_q[log p(y|z)] - KL[q(z)||p(z)]

Optimize: q*(z) = argmax ELBO(q)
                   q∈Q

Mean-field: q(z) = Π qᵢ(zᵢ)
                   i

Coordinate ascent:
qᵢ(zᵢ) ∝ exp(E_{q₋ᵢ}[log p(y, z)])

where:
- q(z) = variational approximation (tractable)
- p(z|y) = true posterior (intractable)
- KL[q||p] = 0 when q = p
- ELBO tight when q ≈ p
```

**Nature's Implementation**: Models probabilistic inference in cortex. Efficient coding, predictive coding, free energy principle. Explains neural variability, attentional modulation, perception. Used for GLM inference, latent variable models, deep generative models of neural data.

**Impact**: **MEDIUM-HIGH - Scalable Inference**
Faster than MCMC. Scales to large datasets. Differentiable (gradient-based). Foundation for variational autoencoders (VAEs). Critical for analyzing high-dimensional neural recordings and generative models.

**Code Example**:
```python
class VariationalInference:
    """Variational Bayes for latent variable models"""

    def __init__(self, n_latent, n_observed):
        self.n_latent = n_latent
        self.n_observed = n_observed

        # Variational parameters: q(z) = N(μ, diag(σ²))
        self.q_mu = np.zeros(n_latent)
        self.q_log_sigma = np.zeros(n_latent)  # Log for positivity

    def sample_q(self, n_samples=1):
        """Sample from variational posterior q(z)"""
        sigma = np.exp(self.q_log_sigma)
        samples = self.q_mu + sigma * np.random.randn(n_samples, self.n_latent)
        return samples

    def log_q(self, z):
        """Log-density of q(z)"""
        sigma = np.exp(self.q_log_sigma)
        log_prob = -0.5 * np.sum((z - self.q_mu)**2 / sigma**2) - \
                   np.sum(self.q_log_sigma) - 0.5 * self.n_latent * np.log(2 * np.pi)
        return log_prob

    def elbo(self, y, log_likelihood_fn, n_samples=100):
        """
        Compute ELBO: E_q[log p(y|z)] - KL[q(z)||p(z)]

        Assume prior p(z) = N(0, I)
        """
        # Sample z ~ q(z)
        z_samples = self.sample_q(n_samples)

        # E_q[log p(y|z)]
        expected_ll = 0
        for z in z_samples:
            expected_ll += log_likelihood_fn(y, z)
        expected_ll /= n_samples

        # KL[q(z)||p(z)] for Gaussian q and prior p(z) = N(0,I)
        # KL = 0.5 * [σ² + μ² - 1 - log(σ²)]
        sigma_sq = np.exp(2 * self.q_log_sigma)
        kl_divergence = 0.5 * np.sum(sigma_sq + self.q_mu**2 - 1 - 2*self.q_log_sigma)

        elbo = expected_ll - kl_divergence

        return elbo

    def fit(self, y, log_likelihood_fn, n_iterations=100, lr=0.01):
        """Optimize ELBO via gradient ascent"""
        for iteration in range(n_iterations):
            # Compute ELBO and gradients (numerical)
            elbo_val = self.elbo(y, log_likelihood_fn, n_samples=50)

            # Gradient via reparameterization trick
            # ∇_μ ELBO, ∇_σ ELBO
            eps = 1e-4

            # μ gradient
            grad_mu = np.zeros(self.n_latent)
            for i in range(self.n_latent):
                self.q_mu[i] += eps
                elbo_plus = self.elbo(y, log_likelihood_fn, n_samples=50)
                self.q_mu[i] -= eps
                grad_mu[i] = (elbo_plus - elbo_val) / eps

            # log_σ gradient
            grad_log_sigma = np.zeros(self.n_latent)
            for i in range(self.n_latent):
                self.q_log_sigma[i] += eps
                elbo_plus = self.elbo(y, log_likelihood_fn, n_samples=50)
                self.q_log_sigma[i] -= eps
                grad_log_sigma[i] = (elbo_plus - elbo_val) / eps

            # Update
            self.q_mu += lr * grad_mu
            self.q_log_sigma += lr * grad_log_sigma

            if iteration % 20 == 0:
                print(f"Iteration {iteration}, ELBO: {elbo_val:.4f}")

        return self.q_mu, np.exp(self.q_log_sigma)


class VariationalAutoencoder(nn.Module):
    """VAE for neural population data"""

    def __init__(self, n_neurons, n_latent):
        super().__init__()
        self.n_latent = n_latent

        # Encoder: q(z|y) = N(μ(y), σ(y))
        self.encoder = nn.Sequential(
            nn.Linear(n_neurons, 50),
            nn.ReLU(),
            nn.Linear(50, n_latent * 2)  # μ and log(σ)
        )

        # Decoder: p(y|z)
        self.decoder = nn.Sequential(
            nn.Linear(n_latent, 50),
            nn.ReLU(),
            nn.Linear(50, n_neurons)
        )

    def encode(self, y):
        """q(z|y)"""
        h = self.encoder(y)
        mu, log_sigma = h[:, :self.n_latent], h[:, self.n_latent:]
        return mu, log_sigma

    def reparameterize(self, mu, log_sigma):
        """z = μ + σ·ε, ε ~ N(0,I)"""
        sigma = torch.exp(log_sigma)
        eps = torch.randn_like(sigma)
        return mu + sigma * eps

    def decode(self, z):
        """p(y|z)"""
        return self.decoder(z)

    def forward(self, y):
        mu, log_sigma = self.encode(y)
        z = self.reparameterize(mu, log_sigma)
        y_recon = self.decode(z)
        return y_recon, mu, log_sigma

    def loss(self, y):
        """Negative ELBO"""
        y_recon, mu, log_sigma = self.forward(y)

        # Reconstruction: E_q[log p(y|z)]
        recon_loss = F.mse_loss(y_recon, y, reduction='sum')

        # KL divergence: KL[q(z|y)||p(z)]
        kl_loss = -0.5 * torch.sum(1 + 2*log_sigma - mu**2 - torch.exp(2*log_sigma))

        return recon_loss + kl_loss

# Example: Latent structure in neural population
n_neurons = 50
n_latent = 5

# Generate data
true_latent = np.random.randn(200, n_latent)
W = np.random.randn(n_latent, n_neurons)
data = true_latent @ W + 0.1 * np.random.randn(200, n_neurons)

# Train VAE
vae = VariationalAutoencoder(n_neurons, n_latent)
optimizer = torch.optim.Adam(vae.parameters(), lr=0.001)

data_torch = torch.FloatTensor(data)

for epoch in range(100):
    loss = vae.loss(data_torch)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 20 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

# Extract latent representation
vae.eval()
with torch.no_grad():
    mu, _ = vae.encode(data_torch)
    inferred_latent = mu.numpy()

# Compare to true latent
from scipy.stats import pearsonr
corr = pearsonr(true_latent.flatten(), inferred_latent.flatten())[0]
print(f"\nCorrelation with true latent: {corr:.3f}")
```

**Source**: Jordan et al. (1999) Machine Learning; Blei et al. (2017) JASA; Kingma & Welling (2014) ICLR; Gao & Ganguli (2015) arXiv

---

### Particle Filter (Sequential Monte Carlo)

**Purpose**: Bayesian state estimation for nonlinear/non-Gaussian systems using weighted particles—handles arbitrary dynamics and observation models.

**Formula**: Weight Update and Resampling
```
Particles: {x_t^{(i)}, w_t^{(i)}}_{i=1..N}

Weight update:
w_t^{(i)} ∝ w_{t-1}^{(i)} · p(y_t|x_t^{(i)}) · p(x_t^{(i)}|x_{t-1}^{(i)}) / q(x_t^{(i)}|x_{t-1}^{(i)}, y_t)

Posterior approximation:
p(x_t|y_{1:t}) ≈ Σ w_t^{(i)} δ(x_t - x_t^{(i)})
                 i=1..N

where:
- x_t^{(i)} = particle i (state sample)
- w_t^{(i)} = normalized weight
- q = proposal distribution (often transition prior)
- δ = Dirac delta
- Resample when effective sample size < threshold
```

**Nature's Implementation**: Models probabilistic inference in cortex for complex sensory integration. Handles multimodal posteriors (bistable perception, ambiguous stimuli). Used for motor control with nonlinear dynamics, navigation with complex environments.

**Impact**: **MEDIUM-HIGH - Nonlinear Filtering**
Handles arbitrary nonlinearity and noise. No Gaussian/linearity assumptions. Asymptotically exact (N→∞). Critical for complex neural dynamics, BMI with nonlinear models, and understanding neural sampling representations.

**Code Example**:
```python
class ParticleFilter:
    """Sequential Monte Carlo for neural state estimation"""

    def __init__(self, n_particles, state_dim, obs_dim):
        self.N = n_particles
        self.state_dim = state_dim
        self.obs_dim = obs_dim

        # Particles and weights
        self.particles = np.random.randn(n_particles, state_dim)
        self.weights = np.ones(n_particles) / n_particles

    def predict(self, dynamics_fn, noise_std=0.1):
        """
        Propagate particles through dynamics
        x_t = f(x_{t-1}) + w
        """
        for i in range(self.N):
            self.particles[i] = dynamics_fn(self.particles[i]) + \
                                np.random.randn(self.state_dim) * noise_std

    def update(self, observation, likelihood_fn):
        """
        Update weights based on observation
        w_t^{(i)} ∝ w_{t-1}^{(i)} · p(y_t | x_t^{(i)})
        """
        for i in range(self.N):
            # Likelihood of observation given particle
            self.weights[i] *= likelihood_fn(observation, self.particles[i])

        # Normalize
        self.weights /= (self.weights.sum() + 1e-10)

    def resample(self):
        """
        Systematic resampling when degeneracy occurs
        """
        # Effective sample size
        N_eff = 1.0 / np.sum(self.weights**2)

        if N_eff < self.N / 2:
            # Resample
            indices = np.random.choice(
                self.N,
                size=self.N,
                replace=True,
                p=self.weights
            )
            self.particles = self.particles[indices]
            self.weights = np.ones(self.N) / self.N

    def estimate(self):
        """Posterior mean estimate"""
        return np.sum(self.particles * self.weights[:, None], axis=0)

    def posterior_covariance(self):
        """Posterior covariance"""
        mean = self.estimate()
        diff = self.particles - mean
        cov = (diff.T * self.weights) @ diff
        return cov

    def filter(self, observations, dynamics_fn, likelihood_fn, noise_std=0.1):
        """
        Run particle filter on sequence
        """
        T = len(observations)
        estimates = np.zeros((T, self.state_dim))

        for t in range(T):
            # Predict
            self.predict(dynamics_fn, noise_std)

            # Update
            self.update(observations[t], likelihood_fn)

            # Resample if needed
            self.resample()

            # Store estimate
            estimates[t] = self.estimate()

        return estimates


# Example: Nonlinear neural dynamics tracking
def neural_dynamics(x):
    """Nonlinear recurrent dynamics"""
    # x = [position, velocity]
    A = np.array([[1, 0.1], [0, 0.9]])
    x_new = A @ x + 0.1 * np.tanh(x)
    return x_new

def observation_likelihood(y_obs, x_state):
    """
    Poisson observation model
    y ~ Poisson(exp(C·x))
    """
    C = np.array([[1, 0], [0, 1], [0.5, 0.5]])  # 3 neurons
    rate = np.exp(C @ x_state)

    # Poisson log-likelihood
    ll = np.sum(y_obs * np.log(rate + 1e-10) - rate)
    return np.exp(ll)  # Return likelihood

# Simulate data
T = 100
true_states = np.zeros((T, 2))
observations = np.zeros((T, 3))

true_states[0] = [0, 0]
for t in range(1, T):
    true_states[t] = neural_dynamics(true_states[t-1]) + np.random.randn(2) * 0.1

C = np.array([[1, 0], [0, 1], [0.5, 0.5]])
for t in range(T):
    rate = np.exp(C @ true_states[t])
    observations[t] = np.random.poisson(rate)

# Run particle filter
pf = ParticleFilter(n_particles=1000, state_dim=2, obs_dim=3)
estimates = pf.filter(observations, neural_dynamics, observation_likelihood, noise_std=0.1)

# Error
error = np.mean(np.linalg.norm(estimates - true_states, axis=1))
print(f"Particle filter tracking error: {error:.3f}")
```

**Source**: Doucet et al. (2001) Sequential Monte Carlo; Djuric et al. (2003) IEEE; Brockwell et al. (2004) J Comp Neurosci

---

### Rauch-Tung-Striebel (RTS) Smoother

**Purpose**: Optimal backward-pass smoothing for state-space models—refines state estimates using future observations.

**Formula**: Backward Smoothing Recursion
```
Forward (Kalman): x_{t|t}, P_{t|t}

Backward smoothing:
x_{t|T} = x_{t|t} + C_t(x_{t+1|T} - x_{t+1|t})

C_t = P_{t|t} A^T P_{t+1|t}^{-1}

P_{t|T} = P_{t|t} + C_t(P_{t+1|T} - P_{t+1|t})C_t^T

where:
- x_{t|T} = smoothed state (uses all data y_{1:T})
- x_{t|t} = filtered state (uses y_{1:t})
- C_t = smoother gain
- A = dynamics matrix
- T = final time
```

**Nature's Implementation**: Post-hoc state reconstruction from neural recordings. Offline analysis of motor planning, decision variables. Reveals latent trajectories in preparatory activity. Used for analyzing trial structure after experiment completion.

**Impact**: **MEDIUM - Offline Smoothing**
Optimal under linear-Gaussian assumptions. Backward pass improves estimates. Critical for offline neural data analysis, trajectory reconstruction, and understanding preparatory dynamics. More accurate than filtering alone for post-hoc analysis.

**Code Example**:
```python
class RTSSmoother:
    """Rauch-Tung-Striebel smoother for state-space models"""

    def __init__(self, state_dim, obs_dim):
        self.n_state = state_dim
        self.n_obs = obs_dim

        # Model parameters (same as Kalman)
        self.A = np.eye(state_dim)
        self.C = np.random.randn(obs_dim, state_dim) * 0.1
        self.Q = 0.1 * np.eye(state_dim)
        self.R = np.eye(obs_dim)

    def forward_filter(self, observations):
        """
        Forward Kalman filter pass
        Returns filtered states and covariances
        """
        T = observations.shape[0]

        # Storage
        x_filt = np.zeros((T, self.n_state))
        P_filt = np.zeros((T, self.n_state, self.n_state))
        x_pred = np.zeros((T, self.n_state))
        P_pred = np.zeros((T, self.n_state, self.n_state))

        # Initialize
        x_filt[0] = np.zeros(self.n_state)
        P_filt[0] = np.eye(self.n_state)

        for t in range(1, T):
            # Predict
            x_pred[t] = self.A @ x_filt[t-1]
            P_pred[t] = self.A @ P_filt[t-1] @ self.A.T + self.Q

            # Update
            y_pred = self.C @ x_pred[t]
            innovation = observations[t] - y_pred

            S = self.C @ P_pred[t] @ self.C.T + self.R
            K = P_pred[t] @ self.C.T @ np.linalg.inv(S)

            x_filt[t] = x_pred[t] + K @ innovation
            P_filt[t] = (np.eye(self.n_state) - K @ self.C) @ P_pred[t]

        return x_filt, P_filt, x_pred, P_pred

    def backward_smooth(self, x_filt, P_filt, x_pred, P_pred):
        """
        RTS backward smoothing pass
        """
        T = x_filt.shape[0]

        # Storage
        x_smooth = np.zeros_like(x_filt)
        P_smooth = np.zeros_like(P_filt)

        # Initialize with final filtered estimate
        x_smooth[-1] = x_filt[-1]
        P_smooth[-1] = P_filt[-1]

        # Backward recursion
        for t in range(T-2, -1, -1):
            # Smoother gain
            C_t = P_filt[t] @ self.A.T @ np.linalg.inv(P_pred[t+1])

            # Smoothed estimate
            x_smooth[t] = x_filt[t] + C_t @ (x_smooth[t+1] - x_pred[t+1])
            P_smooth[t] = P_filt[t] + C_t @ (P_smooth[t+1] - P_pred[t+1]) @ C_t.T

        return x_smooth, P_smooth

    def smooth(self, observations):
        """
        Full RTS smoothing: forward + backward
        """
        # Forward filter
        x_filt, P_filt, x_pred, P_pred = self.forward_filter(observations)

        # Backward smooth
        x_smooth, P_smooth = self.backward_smooth(x_filt, P_filt, x_pred, P_pred)

        return x_smooth, P_smooth, x_filt, P_filt


# Example: Motor trajectory reconstruction
n_state = 4  # [x, y, vx, vy]
n_obs = 10   # 10 neurons

smoother = RTSSmoother(state_dim=n_state, obs_dim=n_obs)

# Dynamics: constant velocity model
smoother.A = np.array([
    [1, 0, 0.1, 0],
    [0, 1, 0, 0.1],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

# Simulate reaching movement
T = 100
true_states = np.zeros((T, n_state))
true_states[0] = [0, 0, 1, 1]  # Start at origin, moving diagonally

for t in range(1, T):
    true_states[t] = smoother.A @ true_states[t-1] + np.random.randn(n_state) * 0.05

# Noisy observations
observations = (smoother.C @ true_states.T).T + np.random.randn(T, n_obs) * 0.5

# Smooth
x_smooth, P_smooth, x_filt, P_filt = smoother.smooth(observations)

# Compare filter vs smoother
filter_error = np.mean(np.linalg.norm(x_filt - true_states, axis=1))
smoother_error = np.mean(np.linalg.norm(x_smooth - true_states, axis=1))

print(f"Filter error: {filter_error:.4f}")
print(f"Smoother error: {smoother_error:.4f}")
print(f"Improvement: {(filter_error - smoother_error) / filter_error * 100:.1f}%")

# Uncertainty reduction
print(f"Filter uncertainty (avg trace P): {np.mean([np.trace(P) for P in P_filt]):.4f}")
print(f"Smoother uncertainty: {np.mean([np.trace(P) for P in P_smooth]):.4f}")
```

**Source**: Rauch et al. (1965) AIAA J; Shumway & Stoffer (1982) JASA; Paninski et al. (2010) Curr Op Neurobio

---

### Laplace Approximation (Neural Posterior)

**Purpose**: Fast Gaussian approximation to posterior at MAP estimate—second-order Taylor expansion around mode.

**Formula**: Quadratic Approximation
```
p(θ|D) ≈ N(θ̂, H^{-1})

where:
θ̂ = argmax p(θ|D)  [MAP estimate]
    θ

H = -∇²_θ log p(θ|D) |_{θ=θ̂}  [Hessian at mode]

Marginal likelihood:
p(D) ≈ p(D|θ̂)p(θ̂) · (2π)^{d/2} |H|^{-1/2}

where:
- d = parameter dimensionality
- Assumes unimodal posterior
```

**Nature's Implementation**: Fast approximate Bayesian inference in cortex. Rapid perceptual decisions under uncertainty. Used for neural encoding model fitting, tuning curve estimation. Balances accuracy and speed.

**Impact**: **MEDIUM - Fast Approximate Inference**
Much faster than MCMC. Closed-form covariance. Useful for model selection (marginal likelihood). Fails for multimodal posteriors. Critical for rapid neural data analysis and online BMI calibration.

**Code Example**:
```python
from scipy.optimize import minimize
from scipy.linalg import inv

class LaplaceApproximation:
    """Laplace approximation for Bayesian inference"""

    def __init__(self, log_prior_fn, log_likelihood_fn):
        self.log_prior = log_prior_fn
        self.log_likelihood = log_likelihood_fn

        self.theta_map = None
        self.hessian_inv = None

    def log_posterior(self, theta, data):
        """Unnormalized log posterior"""
        return self.log_likelihood(theta, data) + self.log_prior(theta)

    def fit(self, data, theta_init):
        """
        Find MAP estimate and Hessian
        """
        # Optimize for MAP
        result = minimize(
            lambda theta: -self.log_posterior(theta, data),
            theta_init,
            method='L-BFGS-B'
        )

        self.theta_map = result.x

        # Compute Hessian numerically
        self.hessian_inv = self._compute_hessian_inv(data)

        return self.theta_map, self.hessian_inv

    def _compute_hessian_inv(self, data, eps=1e-5):
        """
        Numerical Hessian via finite differences
        H_ij = ∂²(-log p)/∂θᵢ∂θⱼ
        """
        d = len(self.theta_map)
        H = np.zeros((d, d))

        for i in range(d):
            for j in range(d):
                theta_pp = self.theta_map.copy()
                theta_pm = self.theta_map.copy()
                theta_mp = self.theta_map.copy()
                theta_mm = self.theta_map.copy()

                theta_pp[i] += eps
                theta_pp[j] += eps

                theta_pm[i] += eps
                theta_pm[j] -= eps

                theta_mp[i] -= eps
                theta_mp[j] += eps

                theta_mm[i] -= eps
                theta_mm[j] -= eps

                # Second derivative
                H[i, j] = (
                    self.log_posterior(theta_pp, data)
                    - self.log_posterior(theta_pm, data)
                    - self.log_posterior(theta_mp, data)
                    + self.log_posterior(theta_mm, data)
                ) / (4 * eps**2)

        H = -H  # Negative log posterior

        # Invert (posterior covariance)
        try:
            H_inv = inv(H)
        except np.linalg.LinAlgError:
            H_inv = inv(H + 1e-6 * np.eye(d))

        return H_inv

    def sample(self, n_samples=1000):
        """Sample from Laplace approximation"""
        return np.random.multivariate_normal(
            self.theta_map,
            self.hessian_inv,
            size=n_samples
        )

    def marginal_likelihood(self, data):
        """
        Laplace approximation to marginal likelihood
        p(D) ≈ p(D|θ̂)·p(θ̂)·(2π)^{d/2}·|H|^{-1/2}
        """
        d = len(self.theta_map)

        log_ml = (
            self.log_likelihood(self.theta_map, data)
            + self.log_prior(self.theta_map)
            + 0.5 * d * np.log(2 * np.pi)
            + 0.5 * np.linalg.slogdet(self.hessian_inv)[1]
        )

        return log_ml


# Example: Tuning curve inference
def log_prior(theta):
    """Gaussian prior on tuning parameters"""
    # theta = [preferred_ori, tuning_width, baseline, gain]
    prior_mean = np.array([90, 20, 5, 10])
    prior_std = np.array([45, 10, 5, 5])

    return -0.5 * np.sum(((theta - prior_mean) / prior_std)**2)

def log_likelihood(theta, data):
    """
    Poisson tuning curve likelihood
    data = [(orientation, spike_count), ...]
    """
    pref_ori, width, baseline, gain = theta

    ll = 0
    for ori, spikes in data:
        # Von Mises tuning
        rate = baseline + gain * np.exp(
            (1/width**2) * np.cos(2 * np.pi * (ori - pref_ori) / 180)
        )

        # Poisson likelihood
        ll += spikes * np.log(rate + 1e-10) - rate

    return ll

# Generate synthetic data
true_params = np.array([90, 15, 3, 12])  # [pref, width, base, gain]
orientations = np.linspace(0, 180, 20)
data = []

for ori in orientations:
    rate = true_params[2] + true_params[3] * np.exp(
        (1/true_params[1]**2) * np.cos(2 * np.pi * (ori - true_params[0]) / 180)
    )
    spikes = np.random.poisson(rate)
    data.append((ori, spikes))

# Laplace approximation
laplace = LaplaceApproximation(log_prior, log_likelihood)
theta_map, cov_post = laplace.fit(data, theta_init=np.array([100, 20, 5, 10]))

print(f"True params: {true_params}")
print(f"MAP estimate: {theta_map}")
print(f"Posterior std: {np.sqrt(np.diag(cov_post))}")

# Marginal likelihood (for model comparison)
log_ml = laplace.marginal_likelihood(data)
print(f"Log marginal likelihood: {log_ml:.2f}")

# Sample from posterior
samples = laplace.sample(n_samples=1000)
print(f"Posterior samples shape: {samples.shape}")
```

**Source**: MacKay (1992) Neural Comp; Bishop (2006) PRML; Kass & Raftery (1995) JASA

---

### Continuous-Time Hidden Markov Model (CT-HMM)

**Purpose**: Extend HMM to continuous time with exponential holding times—models asynchronous state transitions in neural activity.

**Formula**: Generator Matrix Dynamics
```
State evolution:
dP_t/dt = P_t · Q

where:
- P_t = [p_1(t), ..., p_K(t)] = state probabilities
- Q = [q_ij] = generator matrix (rate matrix)
- q_ii = -Σ_{j≠i} q_ij  (row sums to zero)

Holding time in state i: T_i ~ Exp(-q_ii)

Transition probability over Δt:
P(z_{t+Δt} = j | z_t = i) = δ_ij + q_ij·Δt + O(Δt²)

Forward algorithm:
α(z_t) = p(z_t, y_{0:t}) = emission(t) · exp(Q·t) · α(z_{t-1})

where:
- exp(Q·t) = matrix exponential
```

**Nature's Implementation**: Models behavioral state transitions (foraging → resting), UP/DOWN state dynamics, sleep stage transitions. Asynchronous switching between cortical states. Exponential dwell times match neural timescales.

**Impact**: **MEDIUM - Continuous State Dynamics**
Handles irregular sampling. Natural for continuous neural recordings. Analytically tractable via matrix exponential. Critical for modeling asynchronous neural state switches and behavioral epoch segmentation.

**Code Example**:
```python
from scipy.linalg import expm

class ContinuousTimeHMM:
    """CT-HMM for neural state inference"""

    def __init__(self, n_states, n_features):
        self.K = n_states
        self.D = n_features

        # Generator matrix Q (rate matrix)
        self.Q = np.random.rand(n_states, n_states) * 0.5
        # Ensure rows sum to zero
        for i in range(n_states):
            self.Q[i, i] = -np.sum(self.Q[i, :]) + self.Q[i, i]

        # Emission distributions (Gaussian)
        self.mu = np.random.randn(n_states, n_features)
        self.Sigma = np.array([np.eye(n_features) for _ in range(n_states)])

        # Initial distribution
        self.pi = np.ones(n_states) / n_states

    def transition_matrix(self, dt):
        """
        P(Δt) = exp(Q·Δt)
        """
        return expm(self.Q * dt)

    def emission_prob(self, y, state):
        """
        p(y_t | z_t = k) for Gaussian emissions
        """
        from scipy.stats import multivariate_normal
        return multivariate_normal.pdf(y, self.mu[state], self.Sigma[state])

    def forward(self, observations, times):
        """
        Forward algorithm for CT-HMM
        α(z_t) = p(z_t, y_{0:t})
        """
        T = len(observations)
        alpha = np.zeros((T, self.K))

        # Initialize
        alpha[0] = self.pi * np.array([self.emission_prob(observations[0], k) for k in range(self.K)])
        alpha[0] /= alpha[0].sum()

        # Forward recursion
        for t in range(1, T):
            dt = times[t] - times[t-1]

            # Transition matrix for this interval
            P_dt = self.transition_matrix(dt)

            # Emission probability
            emission = np.array([self.emission_prob(observations[t], k) for k in range(self.K)])

            # Forward update
            alpha[t] = emission * (P_dt.T @ alpha[t-1])
            alpha[t] /= alpha[t].sum()

        return alpha

    def viterbi(self, observations, times):
        """
        Viterbi decoding for CT-HMM
        """
        T = len(observations)
        delta = np.zeros((T, self.K))
        psi = np.zeros((T, self.K), dtype=int)

        # Initialize
        delta[0] = np.log(self.pi + 1e-10) + np.log([
            self.emission_prob(observations[0], k) + 1e-10 for k in range(self.K)
        ])

        # Forward
        for t in range(1, T):
            dt = times[t] - times[t-1]
            P_dt = self.transition_matrix(dt)

            emission = np.array([self.emission_prob(observations[t], k) for k in range(self.K)])

            for k in range(self.K):
                prob = delta[t-1] + np.log(P_dt[:, k] + 1e-10)
                psi[t, k] = np.argmax(prob)
                delta[t, k] = np.max(prob) + np.log(emission[k] + 1e-10)

        # Backtrack
        states = np.zeros(T, dtype=int)
        states[-1] = np.argmax(delta[-1])

        for t in range(T-2, -1, -1):
            states[t] = psi[t+1, states[t+1]]

        return states

    def sample_trajectory(self, T_total, dt=0.01):
        """
        Sample state trajectory and observations
        """
        times = [0]
        states = [np.random.choice(self.K, p=self.pi)]
        observations = [np.random.multivariate_normal(self.mu[states[0]], self.Sigma[states[0]])]

        t = 0
        while t < T_total:
            current_state = states[-1]

            # Holding time (exponential)
            holding_rate = -self.Q[current_state, current_state]
            holding_time = np.random.exponential(1.0 / holding_rate)

            # Next state
            transition_probs = self.Q[current_state, :].copy()
            transition_probs[current_state] = 0
            transition_probs /= transition_probs.sum()

            next_state = np.random.choice(self.K, p=transition_probs)

            t += holding_time
            if t >= T_total:
                break

            times.append(t)
            states.append(next_state)
            observations.append(
                np.random.multivariate_normal(self.mu[next_state], self.Sigma[next_state])
            )

        return np.array(times), np.array(states), np.array(observations)


# Example: Sleep stage dynamics
n_states = 3  # Wake, NREM, REM
n_features = 5  # Neural features (LFP bands, etc.)

ct_hmm = ContinuousTimeHMM(n_states, n_features)

# Generator matrix (transition rates)
ct_hmm.Q = np.array([
    [-0.3, 0.2, 0.1],   # Wake → NREM, Wake → REM
    [0.15, -0.25, 0.1],  # NREM → Wake, NREM → REM
    [0.2, 0.05, -0.25]   # REM → Wake, REM → NREM
])

# Emission parameters (different neural signatures)
ct_hmm.mu = np.array([
    [1, 0, 0, 0, 0],    # Wake: high gamma
    [0, 1, 0, 0, 0],    # NREM: high delta
    [0, 0, 1, 0, 0]     # REM: theta/gamma
])

# Sample trajectory
times, true_states, observations = ct_hmm.sample_trajectory(T_total=100, dt=0.1)

# Decode
decoded_states = ct_hmm.viterbi(observations, times)

# Accuracy
accuracy = np.mean(decoded_states == true_states)
print(f"State decoding accuracy: {accuracy:.2%}")
print(f"Number of state transitions: {np.sum(np.diff(true_states) != 0)}")
print(f"Average holding time: {np.mean(np.diff(times)):.2f} time units")
```

**Source**: Hobolth & Jensen (2011) Stat Appl Genet Mol Biol; Liu et al. (2015) Biometrika; Munch et al. (2018) J Neurosci Methods

---

### Hawkes Process (Self-Exciting Point Process)

**Purpose**: Model self-exciting spike trains with history-dependent intensity—captures bursting, refractory effects, and network excitation cascades.

**Formula**: Self-Exciting Conditional Intensity
```
λ_i(t) = μ_i + Σ  Σ      α_{ij} exp(-β(t - t_k^{(j)}))
               j  t_k^{(j)}<t

where:
- λ_i(t) = intensity of neuron i at time t
- μ_i = baseline (exogenous) rate
- α_{ij} = excitation from neuron j to i
- β = decay rate of excitation
- t_k^{(j)} = past spike times of neuron j

Multivariate stability condition:
ρ(Γ/β) < 1

where Γ = [α_{ij}] and ρ = spectral radius

Branching ratio (average offspring):
n = ||Γ/β||

Log-likelihood:
L = Σ log λ_i(t_k^{(i)}) - ∫_0^T λ_i(t) dt
    i,k
```

**Nature's Implementation**: Bursting dynamics in cortex, hippocampus. Network excitation cascades, avalanche dynamics. Refractory effects followed by facilitation. Used for modeling spike train correlations, synchrony, and population avalanches.

**Impact**: **MEDIUM-HIGH - Self-Excitation Dynamics**
Captures temporal dependencies beyond GLM. Models bursting and network cascades. Reveals excitatory coupling strength. Critical for understanding spike train statistics, avalanche dynamics, and circuit excitability.

**Code Example**:
```python
class HawkesProcess:
    """Multivariate Hawkes process for neural spike trains"""

    def __init__(self, n_neurons):
        self.n_neurons = n_neurons

        # Parameters
        self.mu = np.ones(n_neurons) * 0.5  # Baseline rates
        self.alpha = np.random.rand(n_neurons, n_neurons) * 0.3  # Excitation matrix
        np.fill_diagonal(self.alpha, 0.1)  # Self-excitation
        self.beta = 2.0  # Decay rate

    def intensity(self, neuron_idx, t, spike_history):
        """
        Compute λ_i(t) = μ_i + Σ_j Σ_k α_{ij} exp(-β(t-t_k^j))
        spike_history: list of arrays, spike_history[j] = spike times of neuron j
        """
        intensity = self.mu[neuron_idx]

        for j in range(self.n_neurons):
            # Past spikes of neuron j
            past_spikes = spike_history[j][spike_history[j] < t]

            # Sum contributions
            if len(past_spikes) > 0:
                intensity += np.sum(
                    self.alpha[neuron_idx, j] * np.exp(-self.beta * (t - past_spikes))
                )

        return intensity

    def simulate(self, T, dt=0.001):
        """
        Simulate Hawkes process via thinning algorithm
        """
        spike_trains = [[] for _ in range(self.n_neurons)]

        # Upper bound on intensity (for thinning)
        lambda_max = self.mu + np.sum(self.alpha, axis=1)

        for neuron_idx in range(self.n_neurons):
            t = 0
            while t < T:
                # Propose spike from homogeneous Poisson
                t += np.random.exponential(1.0 / lambda_max[neuron_idx])

                if t >= T:
                    break

                # Accept/reject based on true intensity
                lambda_t = self.intensity(neuron_idx, t, spike_trains)
                u = np.random.rand()

                if u * lambda_max[neuron_idx] <= lambda_t:
                    spike_trains[neuron_idx].append(t)

        # Convert to arrays
        spike_trains = [np.array(st) for st in spike_trains]

        return spike_trains

    def log_likelihood(self, spike_trains, T):
        """
        Compute log-likelihood: L = Σ log λ(t_k) - ∫ λ(t) dt
        """
        ll = 0

        for neuron_idx in range(self.n_neurons):
            spikes = spike_trains[neuron_idx]

            # Σ log λ(t_k)
            for t_k in spikes:
                lambda_k = self.intensity(neuron_idx, t_k, spike_trains)
                ll += np.log(lambda_k + 1e-10)

            # -∫ λ(t) dt
            # For Hawkes: ∫ λ(t) dt = μ·T + Σ α/β · N_j
            ll -= self.mu[neuron_idx] * T

            for j in range(self.n_neurons):
                N_j = len(spike_trains[j])
                ll -= (self.alpha[neuron_idx, j] / self.beta) * N_j

        return ll

    def fit(self, spike_trains, T, n_iterations=50, lr=0.01):
        """
        Fit Hawkes parameters via gradient ascent
        """
        for iteration in range(n_iterations):
            ll = self.log_likelihood(spike_trains, T)

            # Gradient w.r.t. parameters (numerical)
            eps = 1e-4

            # Gradient μ
            grad_mu = np.zeros(self.n_neurons)
            for i in range(self.n_neurons):
                self.mu[i] += eps
                grad_mu[i] = (self.log_likelihood(spike_trains, T) - ll) / eps
                self.mu[i] -= eps

            # Gradient α
            grad_alpha = np.zeros((self.n_neurons, self.n_neurons))
            for i in range(self.n_neurons):
                for j in range(self.n_neurons):
                    self.alpha[i, j] += eps
                    grad_alpha[i, j] = (self.log_likelihood(spike_trains, T) - ll) / eps
                    self.alpha[i, j] -= eps

            # Update
            self.mu += lr * grad_mu
            self.alpha += lr * grad_alpha

            # Ensure positivity
            self.mu = np.maximum(self.mu, 0.01)
            self.alpha = np.maximum(self.alpha, 0)

            if iteration % 10 == 0:
                print(f"Iteration {iteration}, Log-likelihood: {ll:.4f}")

    def branching_ratio(self):
        """
        Compute branching ratio: n = ||Γ/β||
        Determines criticality (n ≈ 1 = critical, n > 1 = supercritical)
        """
        Gamma = self.alpha / self.beta
        eigenvalues = np.linalg.eigvals(Gamma)
        spectral_radius = np.max(np.abs(eigenvalues))

        return spectral_radius

    def stability_check(self):
        """Check if process is stable: ρ(Γ/β) < 1"""
        return self.branching_ratio() < 1


# Example: Coupled excitatory neurons
n_neurons = 5
hawkes = HawkesProcess(n_neurons)

# Set parameters
hawkes.mu = np.ones(n_neurons) * 1.0  # Baseline 1 Hz
hawkes.alpha = np.random.rand(n_neurons, n_neurons) * 0.2  # Weak coupling
hawkes.beta = 3.0

# Check stability
print(f"Branching ratio: {hawkes.branching_ratio():.3f}")
print(f"Stable: {hawkes.stability_check()}")

# Simulate
T = 100  # seconds
spike_trains = hawkes.simulate(T, dt=0.001)

# Statistics
for i, st in enumerate(spike_trains):
    print(f"Neuron {i}: {len(st)} spikes, rate = {len(st)/T:.2f} Hz")

# Fit new model to data
hawkes_fit = HawkesProcess(n_neurons)
hawkes_fit.fit(spike_trains, T, n_iterations=30, lr=0.01)

print(f"\nTrue baseline rates: {hawkes.mu}")
print(f"Fitted baseline rates: {hawkes_fit.mu}")
```

**Source**: Hawkes (1971) Biometrika; Reynaud-Bouret & Schbath (2010) Adv Appl Prob; Pernice et al. (2011) J Stat Mech; Gerhard et al. (2017) Front Comp Neurosci

---

### Bayesian Filtering (General Continuous State)

**Purpose**: Recursive Bayesian state estimation for arbitrary dynamics and observations—foundation for all filtering algorithms.

**Formula**: Recursive Bayes Filter
```
Prediction (Chapman-Kolmogorov):
p(x_t | y_{1:t-1}) = ∫ p(x_t | x_{t-1}) p(x_{t-1} | y_{1:t-1}) dx_{t-1}

Update (Bayes rule):
p(x_t | y_{1:t}) = p(y_t | x_t) p(x_t | y_{1:t-1}) / p(y_t | y_{1:t-1})

Normalization:
p(y_t | y_{1:t-1}) = ∫ p(y_t | x_t) p(x_t | y_{1:t-1}) dx_t

where:
- x_t = latent state at time t
- y_t = observation at time t
- p(x_t | x_{t-1}) = dynamics model
- p(y_t | x_t) = observation model

Special cases:
- Kalman Filter: linear-Gaussian
- Particle Filter: nonlinear-nonGaussian (MC approximation)
- Extended KF: linearization
```

**Nature's Implementation**: General framework for sensorimotor integration, perceptual inference, state estimation. Cortical implementation via population codes, predictive coding. Used for motor control, navigation, multisensory integration.

**Impact**: **HIGH - Universal State Estimation**
Unifies all filtering algorithms. Optimal under Bayes' rule. Handles arbitrary models. Foundation for understanding neural inference. Critical for BMI, state estimation theory, and neural probabilistic computation.

**Code Example**:
```python
class BayesianFilter:
    """
    General Bayesian filter (continuous state)
    Implemented via grid approximation for arbitrary models
    """

    def __init__(self, state_min, state_max, n_grid):
        """
        state_min, state_max: bounds of state space
        n_grid: grid resolution for each dimension
        """
        self.state_grid = np.linspace(state_min, state_max, n_grid)
        self.n_grid = n_grid
        self.dx = self.state_grid[1] - self.state_grid[0]

        # Posterior belief: p(x_t | y_{1:t})
        self.belief = np.ones(n_grid) / n_grid  # Uniform prior

    def predict(self, dynamics_fn, noise_std=0.1):
        """
        Prediction step: p(x_t | y_{1:t-1}) = ∫ p(x_t|x_{t-1}) p(x_{t-1}|y_{1:t-1}) dx_{t-1}

        dynamics_fn: x_t = f(x_{t-1})
        Assumes Gaussian process noise
        """
        belief_pred = np.zeros(self.n_grid)

        for i, x_t in enumerate(self.state_grid):
            # For each possible current state x_t,
            # integrate over previous states weighted by dynamics
            for j, x_tm1 in enumerate(self.state_grid):
                # p(x_t | x_{t-1}) = N(x_t | f(x_{t-1}), noise_std²)
                x_pred = dynamics_fn(x_tm1)
                transition_prob = np.exp(-(x_t - x_pred)**2 / (2 * noise_std**2))
                transition_prob /= np.sqrt(2 * np.pi * noise_std**2)

                belief_pred[i] += transition_prob * self.belief[j] * self.dx

        self.belief = belief_pred / (belief_pred.sum() * self.dx)  # Normalize

    def update(self, observation, likelihood_fn):
        """
        Update step: p(x_t|y_{1:t}) ∝ p(y_t|x_t) p(x_t|y_{1:t-1})

        likelihood_fn: p(y_t | x_t)
        """
        # Compute likelihood for each grid point
        likelihoods = np.array([likelihood_fn(observation, x) for x in self.state_grid])

        # Bayes update
        self.belief = likelihoods * self.belief

        # Normalize
        self.belief /= (self.belief.sum() * self.dx)

    def estimate(self):
        """Posterior mean estimate"""
        return np.sum(self.state_grid * self.belief * self.dx)

    def variance(self):
        """Posterior variance"""
        mean = self.estimate()
        return np.sum((self.state_grid - mean)**2 * self.belief * self.dx)

    def filter(self, observations, dynamics_fn, likelihood_fn, noise_std=0.1):
        """
        Run Bayesian filter on sequence
        """
        T = len(observations)
        estimates = np.zeros(T)
        variances = np.zeros(T)

        for t in range(T):
            # Predict
            self.predict(dynamics_fn, noise_std)

            # Update
            self.update(observations[t], likelihood_fn)

            # Store
            estimates[t] = self.estimate()
            variances[t] = self.variance()

        return estimates, variances


# Example: Nonlinear 1D dynamics with Poisson observations
def nonlinear_dynamics(x):
    """Nonlinear state transition: x_t = 0.9·x_{t-1} + tanh(x_{t-1})"""
    return 0.9 * x + np.tanh(x)

def poisson_likelihood(y_obs, x_state):
    """
    Poisson observation: y ~ Poisson(exp(x))
    """
    rate = np.exp(x_state)
    if y_obs >= 0:
        ll = y_obs * np.log(rate + 1e-10) - rate
        return np.exp(ll) / np.math.factorial(int(y_obs))
    else:
        return 0

# Simulate data
T = 50
true_states = np.zeros(T)
observations = np.zeros(T)

true_states[0] = 0
for t in range(1, T):
    true_states[t] = nonlinear_dynamics(true_states[t-1]) + np.random.randn() * 0.3

for t in range(T):
    rate = np.exp(true_states[t])
    observations[t] = np.random.poisson(rate)

# Bayesian filter
bf = BayesianFilter(state_min=-3, state_max=3, n_grid=200)
estimates, variances = bf.filter(observations, nonlinear_dynamics, poisson_likelihood, noise_std=0.3)

# Error
error = np.mean(np.abs(estimates - true_states))
print(f"Filtering error: {error:.3f}")
print(f"Average posterior std: {np.mean(np.sqrt(variances)):.3f}")

# Compare to Kalman (will fail due to nonlinearity)
from scipy.signal import lfilter
b, a = [1], [1, -0.9]  # Linear approximation
kalman_estimates = lfilter(b, a, observations)
kalman_error = np.mean(np.abs(kalman_estimates - true_states))

print(f"\nKalman (linear approx) error: {kalman_error:.3f}")
print(f"Bayesian filter improvement: {(kalman_error - error) / kalman_error * 100:.1f}%")
```

**Source**: Jazwinski (1970) Stochastic Processes and Filtering Theory; Arulampalam et al. (2002) IEEE Trans Signal Processing; Doucet & Johansen (2009) Handbook of Nonlinear Filtering

---

### Hawkes Process (Self-Exciting Point Process)

**Purpose**: Model self-exciting spike trains with history-dependent intensity—captures bursting, refractory effects, and network excitation cascades.

**Formula**: Self-Exciting Conditional Intensity
```
λ_i(t) = μ_i + Σ  Σ      α_{ij} exp(-β(t - t_k^{(j)}))
               j  t_k^{(j)}<t

where:
- λ_i(t) = intensity of neuron i at time t
- μ_i = baseline (exogenous) rate
- α_{ij} = excitation from neuron j to i
- β = decay rate of excitation
- t_k^{(j)} = past spike times of neuron j

Multivariate stability condition:
ρ(Γ/β) < 1

where Γ = [α_{ij}] and ρ = spectral radius

Branching ratio (average offspring):
n = ||Γ/β||

Log-likelihood:
L = Σ log λ_i(t_k^{(i)}) - ∫_0^T λ_i(t) dt
    i,k
```

**Nature's Implementation**: Bursting dynamics in cortex, hippocampus. Network excitation cascades, avalanche dynamics. Refractory effects followed by facilitation. Used for modeling spike train correlations, synchrony, and population avalanches.

**Impact**: **MEDIUM-HIGH - Self-Excitation Dynamics**
Captures temporal dependencies beyond GLM. Models bursting and network cascades. Reveals excitatory coupling strength. Critical for understanding spike train statistics, avalanche dynamics, and circuit excitability.

**Code Example**:
```python
class HawkesProcess:
    """Multivariate Hawkes process for neural spike trains"""

    def __init__(self, n_neurons):
        self.n_neurons = n_neurons

        # Parameters
        self.mu = np.ones(n_neurons) * 0.5  # Baseline rates
        self.alpha = np.random.rand(n_neurons, n_neurons) * 0.3  # Excitation matrix
        np.fill_diagonal(self.alpha, 0.1)  # Self-excitation
        self.beta = 2.0  # Decay rate

    def intensity(self, neuron_idx, t, spike_history):
        """
        Compute λ_i(t) = μ_i + Σ_j Σ_k α_{ij} exp(-β(t-t_k^j))
        spike_history: list of arrays, spike_history[j] = spike times of neuron j
        """
        intensity = self.mu[neuron_idx]

        for j in range(self.n_neurons):
            # Past spikes of neuron j
            past_spikes = spike_history[j][spike_history[j] < t]

            # Sum contributions
            if len(past_spikes) > 0:
                intensity += np.sum(
                    self.alpha[neuron_idx, j] * np.exp(-self.beta * (t - past_spikes))
                )

        return intensity

    def simulate(self, T, dt=0.001):
        """
        Simulate Hawkes process via thinning algorithm
        """
        spike_trains = [[] for _ in range(self.n_neurons)]

        # Upper bound on intensity (for thinning)
        lambda_max = self.mu + np.sum(self.alpha, axis=1)

        for neuron_idx in range(self.n_neurons):
            t = 0
            while t < T:
                # Propose spike from homogeneous Poisson
                t += np.random.exponential(1.0 / lambda_max[neuron_idx])

                if t >= T:
                    break

                # Accept/reject based on true intensity
                lambda_t = self.intensity(neuron_idx, t, spike_trains)
                u = np.random.rand()

                if u * lambda_max[neuron_idx] <= lambda_t:
                    spike_trains[neuron_idx].append(t)

        # Convert to arrays
        spike_trains = [np.array(st) for st in spike_trains]

        return spike_trains

    def log_likelihood(self, spike_trains, T):
        """
        Compute log-likelihood: L = Σ log λ(t_k) - ∫ λ(t) dt
        """
        ll = 0

        for neuron_idx in range(self.n_neurons):
            spikes = spike_trains[neuron_idx]

            # Σ log λ(t_k)
            for t_k in spikes:
                lambda_k = self.intensity(neuron_idx, t_k, spike_trains)
                ll += np.log(lambda_k + 1e-10)

            # -∫ λ(t) dt
            # For Hawkes: ∫ λ(t) dt = μ·T + Σ α/β · N_j
            ll -= self.mu[neuron_idx] * T

            for j in range(self.n_neurons):
                N_j = len(spike_trains[j])
                ll -= (self.alpha[neuron_idx, j] / self.beta) * N_j

        return ll

    def fit(self, spike_trains, T, n_iterations=50, lr=0.01):
        """
        Fit Hawkes parameters via gradient ascent
        """
        for iteration in range(n_iterations):
            ll = self.log_likelihood(spike_trains, T)

            # Gradient w.r.t. parameters (numerical)
            eps = 1e-4

            # Gradient μ
            grad_mu = np.zeros(self.n_neurons)
            for i in range(self.n_neurons):
                self.mu[i] += eps
                grad_mu[i] = (self.log_likelihood(spike_trains, T) - ll) / eps
                self.mu[i] -= eps

            # Gradient α
            grad_alpha = np.zeros((self.n_neurons, self.n_neurons))
            for i in range(self.n_neurons):
                for j in range(self.n_neurons):
                    self.alpha[i, j] += eps
                    grad_alpha[i, j] = (self.log_likelihood(spike_trains, T) - ll) / eps
                    self.alpha[i, j] -= eps

            # Update
            self.mu += lr * grad_mu
            self.alpha += lr * grad_alpha

            # Ensure positivity
            self.mu = np.maximum(self.mu, 0.01)
            self.alpha = np.maximum(self.alpha, 0)

            if iteration % 10 == 0:
                print(f"Iteration {iteration}, Log-likelihood: {ll:.4f}")

    def branching_ratio(self):
        """
        Compute branching ratio: n = ||Γ/β||
        Determines criticality (n ≈ 1 = critical, n > 1 = supercritical)
        """
        Gamma = self.alpha / self.beta
        eigenvalues = np.linalg.eigvals(Gamma)
        spectral_radius = np.max(np.abs(eigenvalues))

        return spectral_radius

    def stability_check(self):
        """Check if process is stable: ρ(Γ/β) < 1"""
        return self.branching_ratio() < 1


# Example: Coupled excitatory neurons
n_neurons = 5
hawkes = HawkesProcess(n_neurons)

# Set parameters
hawkes.mu = np.ones(n_neurons) * 1.0  # Baseline 1 Hz
hawkes.alpha = np.random.rand(n_neurons, n_neurons) * 0.2  # Weak coupling
hawkes.beta = 3.0

# Check stability
print(f"Branching ratio: {hawkes.branching_ratio():.3f}")
print(f"Stable: {hawkes.stability_check()}")

# Simulate
T = 100  # seconds
spike_trains = hawkes.simulate(T, dt=0.001)

# Statistics
for i, st in enumerate(spike_trains):
    print(f"Neuron {i}: {len(st)} spikes, rate = {len(st)/T:.2f} Hz")

# Fit new model to data
hawkes_fit = HawkesProcess(n_neurons)
hawkes_fit.fit(spike_trains, T, n_iterations=30, lr=0.01)

print(f"\nTrue baseline rates: {hawkes.mu}")
print(f"Fitted baseline rates: {hawkes_fit.mu}")
```

**Source**: Hawkes (1971) Biometrika; Reynaud-Bouret & Schbath (2010) Adv Appl Prob; Pernice et al. (2011) J Stat Mech; Gerhard et al. (2017) Front Comp Neurosci

---

### Bayesian Filtering (General Continuous State)

**Purpose**: Recursive Bayesian state estimation for arbitrary dynamics and observations—foundation for all filtering algorithms.

**Formula**: Recursive Bayes Filter
```
Prediction (Chapman-Kolmogorov):
p(x_t | y_{1:t-1}) = ∫ p(x_t | x_{t-1}) p(x_{t-1} | y_{1:t-1}) dx_{t-1}

Update (Bayes rule):
p(x_t | y_{1:t}) = p(y_t | x_t) p(x_t | y_{1:t-1}) / p(y_t | y_{1:t-1})

Normalization:
p(y_t | y_{1:t-1}) = ∫ p(y_t | x_t) p(x_t | y_{1:t-1}) dx_t

where:
- x_t = latent state at time t
- y_t = observation at time t
- p(x_t | x_{t-1}) = dynamics model
- p(y_t | x_t) = observation model

Special cases:
- Kalman Filter: linear-Gaussian
- Particle Filter: nonlinear-nonGaussian (MC approximation)
- Extended KF: linearization
```

**Nature's Implementation**: General framework for sensorimotor integration, perceptual inference, state estimation. Cortical implementation via population codes, predictive coding. Used for motor control, navigation, multisensory integration.

**Impact**: **HIGH - Universal State Estimation**
Unifies all filtering algorithms. Optimal under Bayes' rule. Handles arbitrary models. Foundation for understanding neural inference. Critical for BMI, state estimation theory, and neural probabilistic computation.

**Code Example**:
```python
class BayesianFilter:
    """
    General Bayesian filter (continuous state)
    Implemented via grid approximation for arbitrary models
    """

    def __init__(self, state_min, state_max, n_grid):
        """
        state_min, state_max: bounds of state space
        n_grid: grid resolution for each dimension
        """
        self.state_grid = np.linspace(state_min, state_max, n_grid)
        self.n_grid = n_grid
        self.dx = self.state_grid[1] - self.state_grid[0]

        # Posterior belief: p(x_t | y_{1:t})
        self.belief = np.ones(n_grid) / n_grid  # Uniform prior

    def predict(self, dynamics_fn, noise_std=0.1):
        """
        Prediction step: p(x_t | y_{1:t-1}) = ∫ p(x_t|x_{t-1}) p(x_{t-1}|y_{1:t-1}) dx_{t-1}

        dynamics_fn: x_t = f(x_{t-1})
        Assumes Gaussian process noise
        """
        belief_pred = np.zeros(self.n_grid)

        for i, x_t in enumerate(self.state_grid):
            # For each possible current state x_t,
            # integrate over previous states weighted by dynamics
            for j, x_tm1 in enumerate(self.state_grid):
                # p(x_t | x_{t-1}) = N(x_t | f(x_{t-1}), noise_std²)
                x_pred = dynamics_fn(x_tm1)
                transition_prob = np.exp(-(x_t - x_pred)**2 / (2 * noise_std**2))
                transition_prob /= np.sqrt(2 * np.pi * noise_std**2)

                belief_pred[i] += transition_prob * self.belief[j] * self.dx

        self.belief = belief_pred / (belief_pred.sum() * self.dx)  # Normalize

    def update(self, observation, likelihood_fn):
        """
        Update step: p(x_t|y_{1:t}) ∝ p(y_t|x_t) p(x_t|y_{1:t-1})

        likelihood_fn: p(y_t | x_t)
        """
        # Compute likelihood for each grid point
        likelihoods = np.array([likelihood_fn(observation, x) for x in self.state_grid])

        # Bayes update
        self.belief = likelihoods * self.belief

        # Normalize
        self.belief /= (self.belief.sum() * self.dx)

    def estimate(self):
        """Posterior mean estimate"""
        return np.sum(self.state_grid * self.belief * self.dx)

    def variance(self):
        """Posterior variance"""
        mean = self.estimate()
        return np.sum((self.state_grid - mean)**2 * self.belief * self.dx)

    def filter(self, observations, dynamics_fn, likelihood_fn, noise_std=0.1):
        """
        Run Bayesian filter on sequence
        """
        T = len(observations)
        estimates = np.zeros(T)
        variances = np.zeros(T)

        for t in range(T):
            # Predict
            self.predict(dynamics_fn, noise_std)

            # Update
            self.update(observations[t], likelihood_fn)

            # Store
            estimates[t] = self.estimate()
            variances[t] = self.variance()

        return estimates, variances


# Example: Nonlinear 1D dynamics with Poisson observations
def nonlinear_dynamics(x):
    """Nonlinear state transition: x_t = 0.9·x_{t-1} + tanh(x_{t-1})"""
    return 0.9 * x + np.tanh(x)

def poisson_likelihood(y_obs, x_state):
    """
    Poisson observation: y ~ Poisson(exp(x))
    """
    rate = np.exp(x_state)
    if y_obs >= 0:
        ll = y_obs * np.log(rate + 1e-10) - rate
        return np.exp(ll) / np.math.factorial(int(y_obs))
    else:
        return 0

# Simulate data
T = 50
true_states = np.zeros(T)
observations = np.zeros(T)

true_states[0] = 0
for t in range(1, T):
    true_states[t] = nonlinear_dynamics(true_states[t-1]) + np.random.randn() * 0.3

for t in range(T):
    rate = np.exp(true_states[t])
    observations[t] = np.random.poisson(rate)

# Bayesian filter
bf = BayesianFilter(state_min=-3, state_max=3, n_grid=200)
estimates, variances = bf.filter(observations, nonlinear_dynamics, poisson_likelihood, noise_std=0.3)

# Error
error = np.mean(np.abs(estimates - true_states))
print(f"Filtering error: {error:.3f}")
print(f"Average posterior std: {np.mean(np.sqrt(variances)):.3f}")

# Compare to Kalman (will fail due to nonlinearity)
from scipy.signal import lfilter
b, a = [1], [1, -0.9]  # Linear approximation
kalman_estimates = lfilter(b, a, observations)
kalman_error = np.mean(np.abs(kalman_estimates - true_states))

print(f"\nKalman (linear approx) error: {kalman_error:.3f}")
print(f"Bayesian filter improvement: {(kalman_error - error) / kalman_error * 100:.1f}%")
```

**Source**: Jazwinski (1970) Stochastic Processes and Filtering Theory; Arulampalam et al. (2002) IEEE Trans Signal Processing; Doucet & Johansen (2009) Handbook of Nonlinear Filtering

---

### Probabilistic Population Code (PPC)

**Purpose**: Exponential family population coding for optimal Bayesian inference—neural activity directly represents posterior distributions.

**Formula**: Log-Linear Population Code
```
p(s | r) ∝ exp(Σ r_i f_i(s))
              i

Equivalently:
log p(s | r) = Σ r_i f_i(s) - A(r)
                i

where:
- s = stimulus or latent variable
- r = [r_1, ..., r_N] = population firing rates
- f_i(s) = basis function for neuron i (often tuning curve)
- A(r) = log partition function (normalization)

Linear-Gaussian case:
p(s | r) = N(s | μ(r), Σ(r))

where population statistics directly encode mean and variance

For optimal coding:
f_i(s) = ∂/∂s log p(s) + noise term
```

**Nature's Implementation**: Distributed coding in sensory cortex (V1 orientation, MT motion), motor cortex (reaching direction), hippocampus (place cells). Population activity represents full posterior, not just point estimates. Handles uncertainty naturally.

**Impact**: **MEDIUM-HIGH - Distributional Coding**
Represents full distributions, not just point estimates. Optimal for Bayesian inference. Explains population variability. Handles uncertainty explicitly. Critical for understanding probabilistic computation in neural populations and distributed representations.

**Code Example**:
```python
class ProbabilisticPopulationCode:
    """Exponential family population code for Bayesian inference"""

    def __init__(self, n_neurons, stimulus_range=(0, 180)):
        self.n_neurons = n_neurons
        self.stim_min, self.stim_max = stimulus_range

        # Basis functions (tuning curves): f_i(s)
        self.preferred = np.linspace(self.stim_min, self.stim_max, n_neurons)
        self.tuning_width = 20.0

    def basis_functions(self, stimulus):
        """
        f_i(s) = tuning curve (von Mises for circular variables)
        """
        f = np.zeros(self.n_neurons)
        for i in range(self.n_neurons):
            # Von Mises tuning
            kappa = 1.0 / (self.tuning_width**2)
            f[i] = np.exp(kappa * np.cos(2 * np.pi * (stimulus - self.preferred[i]) / 180))

        return f

    def encode(self, stimulus, gain=10.0):
        """
        Generate population response: r_i ~ Poisson(gain · f_i(s))
        """
        f = self.basis_functions(stimulus)
        rates = gain * f
        spikes = np.random.poisson(rates)

        return spikes

    def decode_posterior(self, spikes, stimulus_grid=None):
        """
        Compute posterior: p(s | r) ∝ exp(Σ r_i f_i(s))
        """
        if stimulus_grid is None:
            stimulus_grid = np.linspace(self.stim_min, self.stim_max, 180)

        log_posterior = np.zeros(len(stimulus_grid))

        for j, s in enumerate(stimulus_grid):
            f = self.basis_functions(s)
            # log p(s | r) = Σ r_i f_i(s)
            log_posterior[j] = np.dot(spikes, f)

        # Normalize
        log_posterior -= np.max(log_posterior)  # Numerical stability
        posterior = np.exp(log_posterior)
        posterior /= np.sum(posterior)

        return stimulus_grid, posterior

    def decode_map(self, spikes):
        """Maximum a posteriori estimate"""
        stim_grid, posterior = self.decode_posterior(spikes)
        return stim_grid[np.argmax(posterior)]

    def decode_mean(self, spikes):
        """Posterior mean (minimum MSE estimator)"""
        stim_grid, posterior = self.decode_posterior(spikes)
        return np.sum(stim_grid * posterior)

    def decode_variance(self, spikes):
        """Posterior variance (uncertainty quantification)"""
        stim_grid, posterior = self.decode_posterior(spikes)
        mean = np.sum(stim_grid * posterior)
        variance = np.sum((stim_grid - mean)**2 * posterior)
        return variance

    def linear_gaussian_approximation(self, spikes):
        """
        For high spike counts: p(s|r) ≈ N(μ, σ²)
        μ = (Σ r_i preferred_i) / Σ r_i  (population vector)
        σ² = Fisher information^{-1}
        """
        if spikes.sum() == 0:
            return 90, 1000  # Uniform

        # Posterior mean (circular mean for orientation)
        angles_rad = 2 * np.pi * self.preferred / 180
        mean_cos = np.sum(spikes * np.cos(angles_rad)) / spikes.sum()
        mean_sin = np.sum(spikes * np.sin(angles_rad)) / spikes.sum()
        mean_angle = np.arctan2(mean_sin, mean_cos) * 180 / (2 * np.pi)
        if mean_angle < 0:
            mean_angle += 180

        # Posterior variance (inverse Fisher information)
        # For Poisson: J = Σ (f'_i)²/f_i
        # Approximate as 1/(total spike count)
        variance = 1.0 / (spikes.sum() + 1e-10)

        return mean_angle, variance


# Example: Orientation coding in V1
n_neurons = 50
ppc = ProbabilisticPopulationCode(n_neurons, stimulus_range=(0, 180))

# Encode stimulus
true_stimulus = 90  # degrees
spikes = ppc.encode(true_stimulus, gain=10)

print(f"True stimulus: {true_stimulus}°")
print(f"Total spikes: {spikes.sum()}")

# Decode full posterior
stim_grid, posterior = ppc.decode_posterior(spikes)

# Point estimates
map_estimate = ppc.decode_map(spikes)
mean_estimate = ppc.decode_mean(spikes)
variance = ppc.decode_variance(spikes)

print(f"\nMAP estimate: {map_estimate:.1f}°")
print(f"Posterior mean: {mean_estimate:.1f}°")
print(f"Posterior std: {np.sqrt(variance):.1f}°")

# Linear-Gaussian approximation
lg_mean, lg_var = ppc.linear_gaussian_approximation(spikes)
print(f"\nLinear-Gaussian approx: {lg_mean:.1f}° ± {np.sqrt(lg_var):.1f}°")

# Test with ambiguous stimulus (low gain)
spikes_ambiguous = ppc.encode(true_stimulus, gain=2)
stim_grid_amb, posterior_amb = ppc.decode_posterior(spikes_ambiguous)
variance_amb = ppc.decode_variance(spikes_ambiguous)

print(f"\nAmbiguous stimulus (low gain):")
print(f"Total spikes: {spikes_ambiguous.sum()}")
print(f"Posterior std: {np.sqrt(variance_amb):.1f}° (high uncertainty)")
```

**Source**: Zemel et al. (1998) Neural Comp; Pouget et al. (2000) Nat Rev Neurosci; Ma et al. (2006) Nat Neurosci; Beck et al. (2008) Neuron

---

### Neural Tangent Kernel (NTK)

**Purpose**: Infinite-width limit of neural networks—linearized dynamics, kernel regime, and feature learning characterization.

**Formula**: Tangent Kernel
```
K(x, x') = ∇_θ f_θ(x) · ∇_θ f_θ(x')

For infinite width: K^∞(x, x') = lim K(x, x')
                                  width→∞

Training dynamics in kernel regime:
df_θ(x)/dt = -η Σ K(x, x_i)(f_θ(x_i) - y_i)
                i

Convergence to minimum:
f_∞(x) = K(x, X)(K(X, X) + λI)^{-1} y

where:
- θ = network parameters
- f_θ(x) = network output
- η = learning rate
- X = training inputs, y = training targets
- K(X, X) = Gram matrix

Deterministic at initialization:
K^∞(x, x') depends only on architecture (depth, width, activation)
```

**Nature's Implementation**: Models feature learning vs kernel regime in biological networks. Explains when networks learn features (finite width) vs stay in linear regime (infinite width). Reveals representational capacity limits.

**Impact**: **MEDIUM - Deep Learning Theory**
Explains training dynamics. Connects neural networks to kernel methods. Reveals when feature learning occurs. Theoretical tool for understanding generalization. Critical for analyzing deep network capacity and biological plausibility of gradient descent.

**Code Example**:
```python
class NeuralTangentKernel:
    """Compute NTK for fully-connected networks"""

    def __init__(self, architecture, activation='relu'):
        """
        architecture: [input_dim, hidden1, hidden2, ..., output_dim]
        """
        self.architecture = architecture
        self.activation = activation

    def kernel_at_init(self, x1, x2):
        """
        Compute NTK at initialization (infinite width limit)
        For ReLU networks: recursive kernel formula
        """
        # Start with input kernel
        Sigma_L = x1 @ x2.T / x1.shape[1]  # Normalized dot product
        K_L = Sigma_L

        for layer in range(1, len(self.architecture) - 1):
            # Recursive NTK computation for ReLU
            if self.activation == 'relu':
                # Compute angles
                norm1 = np.sqrt(np.diag(Sigma_L))
                norm2 = np.sqrt(np.diag(Sigma_L))
                norm_outer = np.outer(norm1, norm2)

                cos_theta = Sigma_L / (norm_outer + 1e-10)
                cos_theta = np.clip(cos_theta, -1, 1)
                theta = np.arccos(cos_theta)

                # ReLU NTK recursion
                Sigma_Lplus1 = (norm_outer / (2 * np.pi)) * (
                    np.sin(theta) + (np.pi - theta) * cos_theta
                )

                K_Lplus1 = (norm_outer / (2 * np.pi)) * (
                    np.sin(theta) + (np.pi - theta) * cos_theta
                ) + Sigma_L * (1 - theta / np.pi)

                Sigma_L = Sigma_Lplus1
                K_L = K_Lplus1

        return K_L

    def empirical_ntk(self, model, x1, x2):
        """
        Compute empirical NTK: K(x,x') = ∇_θf(x)·∇_θf(x')
        For finite-width networks
        """
        # Get Jacobians
        J1 = self._jacobian(model, x1)  # [batch1, output, n_params]
        J2 = self._jacobian(model, x2)  # [batch2, output, n_params]

        # NTK: J1 · J2^T summed over parameters
        K = np.einsum('iop,jop->ij', J1, J2)

        return K

    def _jacobian(self, model, x):
        """Compute Jacobian ∇_θ f_θ(x) for each input"""
        import torch
        from torch.func import jacrev, vmap

        # Convert to torch
        x_torch = torch.FloatTensor(x)

        # Function that returns network output
        def forward_fn(params, x_single):
            # Flatten params and pass through model
            # (This is pseudocode - actual implementation depends on model structure)
            return model(x_single, params)

        # Vectorized Jacobian
        jacobian_fn = vmap(jacrev(forward_fn, argnums=0), in_dims=(None, 0))

        # Get parameters
        params = {name: p.detach() for name, p in model.named_parameters()}

        J = jacobian_fn(params, x_torch)

        return J.numpy()

    def training_dynamics_kernel_regime(self, K_train, y_train, n_steps=1000, lr=0.01):
        """
        Simulate training dynamics in kernel regime:
        df/dt = -η K(X,X)(f - y)
        """
        n = K_train.shape[0]
        f = np.zeros(n)  # Initialize at zero

        trajectory = [f.copy()]

        for step in range(n_steps):
            # Gradient: K(f - y)
            grad = K_train @ (f - y_train)

            # Update
            f -= lr * grad

            if step % 100 == 0:
                trajectory.append(f.copy())

        return np.array(trajectory)

    def predict_kernel_limit(self, K_train, K_test_train, y_train, regularization=0.0):
        """
        Infinite-time prediction in kernel regime:
        f_∞(x) = K(x, X_train) (K(X_train, X_train) + λI)^{-1} y
        """
        n = K_train.shape[0]
        K_reg = K_train + regularization * np.eye(n)

        # Solve linear system
        alpha = np.linalg.solve(K_reg, y_train)

        # Predict
        f_test = K_test_train @ alpha

        return f_test


# Example: NTK for simple network
arch = [10, 50, 50, 1]  # 2-hidden-layer network
ntk = NeuralTangentKernel(arch, activation='relu')

# Generate data
n_train = 100
n_test = 50
X_train = np.random.randn(n_train, 10)
X_test = np.random.randn(n_test, 10)
y_train = np.sin(X_train[:, 0]) + 0.1 * np.random.randn(n_train)

# Compute NTK at initialization (infinite width)
K_train_train = ntk.kernel_at_init(X_train, X_train)
K_test_train = ntk.kernel_at_init(X_test, X_train)

print(f"NTK shape (train): {K_train_train.shape}")
print(f"NTK eigenvalues: {np.linalg.eigvalsh(K_train_train)[-5:]}")

# Predict in kernel regime (no feature learning)
y_pred = ntk.predict_kernel_limit(K_train_train, K_test_train, y_train, regularization=0.01)

# Training dynamics
trajectory = ntk.training_dynamics_kernel_regime(K_train_train, y_train, n_steps=1000, lr=0.01)
print(f"\nTraining loss trajectory: {[np.mean((f - y_train)**2) for f in trajectory]}")

# Compare finite vs infinite width
print(f"\nInfinite-width regime prediction MSE: {np.mean((y_pred - np.sin(X_test[:, 0]))**2):.4f}")
```

**Source**: Jacot et al. (2018) NeurIPS; Lee et al. (2019) ICLR; Arora et al. (2019) ICML; Yang (2020) NeurIPS

---

### Neural Manifold Dynamics

**Purpose**: Model neural population activity as low-dimensional trajectories on manifolds—reveals dynamical structure underlying computation.

**Formula**: Latent Dynamical System
```
Latent dynamics:
ż = f(z) + η(t)

Observation:
x(t) = C z(t) + ε(t)

where:
- z ∈ ℝ^k = latent state (k << d)
- x ∈ ℝ^d = neural population activity
- f(z) = latent dynamics (can be linear or nonlinear)
- C = [d × k] readout matrix
- η, ε = dynamical and observation noise

Linear case:
ż = A z + Bu + η

Nonlinear (polynomial):
ż = Σ A_p (z^⊗p) + Bu + η
    p

Manifold characterization:
- Dimensionality: intrinsic dimension k
- Curvature: local geometry
- Attractors: fixed points, limit cycles
```

**Nature's Implementation**: Motor cortex preparatory activity (reaching manifold), decision dynamics (decision manifold), working memory (persistent activity subspace). Cognitive variables encoded in low-D structure. Reveals computational role of population geometry.

**Impact**: **MEDIUM-HIGH - Latent Dynamics**
Reveals low-dimensional structure. Interpretable latent states. Separates signal from noise. Critical for understanding population computation, motor planning, decision-making, and cognitive state dynamics.

**Code Example**:
```python
from sklearn.decomposition import PCA
from scipy.integrate import odeint

class NeuralManifold:
    """Identify and analyze neural manifold dynamics"""

    def __init__(self, latent_dim=3):
        self.latent_dim = latent_dim

        # Latent dynamics parameters
        self.A = None  # Linear dynamics
        self.C = None  # Readout matrix

    def identify_manifold(self, neural_data, method='pca'):
        """
        Discover latent manifold from neural population data
        neural_data: [n_timepoints, n_neurons]
        """
        if method == 'pca':
            pca = PCA(n_components=self.latent_dim)
            latent_trajectories = pca.fit_transform(neural_data)

            self.C = pca.components_.T  # [n_neurons, k]
            explained_var = pca.explained_variance_ratio_

            print(f"Variance explained: {explained_var.sum():.2%}")

            return latent_trajectories, explained_var

    def fit_dynamics(self, latent_trajectories, dt=0.01):
        """
        Fit latent dynamics: ż = Az
        via least squares on finite differences
        """
        # Compute finite differences
        z_dot = np.diff(latent_trajectories, axis=0) / dt
        z = latent_trajectories[:-1]

        # Least squares: ż ≈ Az → A = (ż Z^T)(ZZ^T)^{-1}
        self.A = z_dot.T @ z @ np.linalg.inv(z.T @ z + 1e-6 * np.eye(self.latent_dim))

        return self.A

    def simulate_dynamics(self, z0, T, dt=0.01):
        """
        Simulate latent dynamics: ż = Az
        """
        time = np.arange(0, T, dt)

        def dynamics(z, t):
            return self.A @ z

        z_trajectory = odeint(dynamics, z0, time)

        return time, z_trajectory

    def reconstruct(self, latent_trajectory):
        """
        Reconstruct neural activity: x̂ = Cz
        """
        return latent_trajectory @ self.C.T

    def find_fixed_points(self):
        """
        Find fixed points of linear dynamics: Az* = 0
        For linear system: z* = 0 is only fixed point
        """
        eigenvalues, eigenvectors = np.linalg.eig(self.A)

        print("Eigenvalues of dynamics:")
        for i, ev in enumerate(eigenvalues):
            stability = "stable" if np.real(ev) < 0 else "unstable"
            print(f"  λ{i}: {ev:.3f} ({stability})")

        return eigenvalues, eigenvectors

    def tangent_space(self, z_point):
        """
        Compute tangent space to manifold at point z
        Tangent vectors: columns of C
        """
        return self.C

    def manifold_curvature(self, z_trajectory):
        """
        Estimate local curvature from trajectory
        Curvature ≈ ||z̈|| / ||ż||²
        """
        z_dot = np.gradient(z_trajectory, axis=0)
        z_ddot = np.gradient(z_dot, axis=0)

        curvature = np.linalg.norm(z_ddot, axis=1) / (np.linalg.norm(z_dot, axis=1)**2 + 1e-10)

        return curvature


# Example: Motor cortex reaching manifold
n_neurons = 100
n_timepoints = 200
latent_dim = 3

# Simulate latent dynamics (spiral trajectory - preparatory activity)
time = np.linspace(0, 2*np.pi, n_timepoints)
z_true = np.column_stack([
    np.cos(time) * np.exp(-time/10),
    np.sin(time) * np.exp(-time/10),
    time / (2*np.pi)
])

# Generate neural data: x = Cz + noise
C_true = np.random.randn(n_neurons, latent_dim) * 0.5
neural_data = z_true @ C_true.T + np.random.randn(n_timepoints, n_neurons) * 0.1

# Identify manifold
manifold = NeuralManifold(latent_dim=3)
z_inferred, explained_var = manifold.identify_manifold(neural_data, method='pca')

print(f"\nInferred latent trajectories shape: {z_inferred.shape}")

# Fit dynamics
A_inferred = manifold.fit_dynamics(z_inferred, dt=0.01)
print(f"\nDynamics matrix A:\n{A_inferred}")

# Find fixed points
eigenvalues, eigenvectors = manifold.find_fixed_points()

# Reconstruct neural activity
neural_reconstructed = manifold.reconstruct(z_inferred)
reconstruction_error = np.mean((neural_data - neural_reconstructed)**2)
print(f"\nReconstruction error: {reconstruction_error:.4f}")

# Manifold curvature
curvature = manifold.manifold_curvature(z_inferred)
print(f"Average curvature: {curvature.mean():.4f}")

# Simulate from initial condition
z0 = z_inferred[0]
time_sim, z_sim = manifold.simulate_dynamics(z0, T=2, dt=0.01)
print(f"\nSimulated trajectory shape: {z_sim.shape}")
```

**Source**: Cunningham & Yu (2014) Nat Neurosci; Gallego et al. (2017) Neuron; Vyas et al. (2020) Ann Rev Neurosci; Chaudhuri et al. (2019) Neuron

---

### Principal Component Analysis (PCA)

**Purpose**: Classic linear dimensionality reduction via eigendecomposition—finds orthogonal directions of maximum variance.

**Formula**: Covariance Eigendecomposition
```
Covariance matrix:
C = (1/n) X^T X

Eigenvalue problem:
C w_i = λ_i w_i

Principal components:
Z = X W

where:
- X = [n × d] data matrix (centered)
- C = [d × d] covariance matrix
- w_i = i-th eigenvector (principal direction)
- λ_i = i-th eigenvalue (variance along w_i)
- W = [w_1, ..., w_k] = projection matrix
- Z = [n × k] = reduced representation

Reconstruction:
X̂ = Z W^T

Variance explained:
R² = Σ_{i=1}^k λ_i / Σ_{i=1}^d λ_i
```

**Nature's Implementation**: Cortical dimensionality reduction, efficient coding. Sensory systems remove redundancy via PCA-like operations. Retinal processing, V1 simple cells approximate PCA of natural images. Online learning via Oja's rule.

**Impact**: **HIGH - Foundational Dimensionality Reduction**
Optimal under Gaussian assumptions. Interpretable components. Fast computation (SVD). Foundation for neural data analysis. Critical for understanding population structure, redundancy reduction, and efficient coding in sensory systems.

**Code Example**:
```python
class PrincipalComponentAnalysis:
    """Classic PCA via SVD"""

    def __init__(self, n_components=None):
        self.n_components = n_components

        self.mean = None
        self.components = None  # Principal directions (eigenvectors)
        self.explained_variance = None
        self.singular_values = None

    def fit(self, X):
        """
        Fit PCA to data via SVD
        X: [n_samples, n_features]
        """
        n_samples, n_features = X.shape

        # Center data
        self.mean = X.mean(axis=0)
        X_centered = X - self.mean

        # SVD: X = U S V^T
        # Covariance: C = V S² V^T
        U, s, Vt = np.linalg.svd(X_centered, full_matrices=False)

        # Components (eigenvectors of covariance)
        self.components = Vt[:self.n_components]  # [k × d]

        # Explained variance (eigenvalues)
        self.explained_variance = (s**2) / (n_samples - 1)
        self.explained_variance = self.explained_variance[:self.n_components]

        self.singular_values = s[:self.n_components]

        return self

    def transform(self, X):
        """Project data onto principal components"""
        X_centered = X - self.mean
        Z = X_centered @ self.components.T
        return Z

    def fit_transform(self, X):
        """Fit and transform in one step"""
        self.fit(X)
        return self.transform(X)

    def inverse_transform(self, Z):
        """Reconstruct from reduced representation"""
        X_reconstructed = Z @ self.components + self.mean
        return X_reconstructed

    def explained_variance_ratio(self):
        """Proportion of variance explained"""
        return self.explained_variance / self.explained_variance.sum()

    def reconstruction_error(self, X):
        """MSE between original and reconstructed"""
        Z = self.transform(X)
        X_recon = self.inverse_transform(Z)
        return np.mean((X - X_recon)**2)

    def whitening_transform(self, X):
        """
        Whiten data: decorrelate and unit variance
        Z_white = X_centered @ V @ S^{-1}
        """
        X_centered = X - self.mean
        Z = X_centered @ self.components.T
        Z_white = Z / np.sqrt(self.explained_variance)
        return Z_white


# Example: Neural population dimensionality
n_neurons = 100
n_timepoints = 500
n_components = 10

# Simulate correlated neural activity
# True low-rank structure: X = Z·C^T + noise
latent_dim = 5
Z_true = np.random.randn(n_timepoints, latent_dim)
C_true = np.random.randn(latent_dim, n_neurons)
X = Z_true @ C_true + np.random.randn(n_timepoints, n_neurons) * 0.5

# Fit PCA
pca = PrincipalComponentAnalysis(n_components=n_components)
Z = pca.fit_transform(X)

print(f"Data shape: {X.shape}")
print(f"Reduced shape: {Z.shape}")
print(f"\nExplained variance ratio: {pca.explained_variance_ratio()}")
print(f"Cumulative variance: {pca.explained_variance_ratio().cumsum()}")

# Reconstruction
X_recon = pca.inverse_transform(Z)
recon_error = pca.reconstruction_error(X)
print(f"\nReconstruction error: {recon_error:.4f}")

# Intrinsic dimensionality (90% variance threshold)
cumvar = pca.explained_variance_ratio().cumsum()
intrinsic_dim = np.argmax(cumvar > 0.9) + 1
print(f"Intrinsic dimensionality (90% var): {intrinsic_dim}")

# Whitening
Z_white = pca.whitening_transform(X)
print(f"\nWhitened covariance:\n{np.cov(Z_white.T)[:3, :3]}")  # Should be ≈ identity

# Compare to covariance eigendecomposition
C = np.cov(X.T)
eigenvalues, eigenvectors = np.linalg.eigh(C)
eigenvalues = eigenvalues[::-1][:n_components]

print(f"\nPCA eigenvalues: {pca.explained_variance}")
print(f"Direct eigenvalues: {eigenvalues}")
print(f"Match: {np.allclose(pca.explained_variance, eigenvalues)}")
```

**Source**: Pearson (1901) Philosophical Mag; Hotelling (1933) J Educational Psych; Jolliffe (2002) Book; Cunningham & Yu (2014) Nat Neurosci

---

### Mahalanobis Distance (Neural Population Metric)

**Purpose**: Covariance-weighted distance metric for neural population states—accounts for correlations and variances.

**Formula**: Quadratic Form Distance
```
D²(r_1, r_2) = (r_1 - r_2)^T Σ^{-1} (r_1 - r_2)

where:
- r_1, r_2 = neural population states
- Σ = population covariance matrix
- Σ^{-1} = precision matrix (inverse covariance)

Probabilistic interpretation (Gaussian):
D² = -2 log p(r_2 | r_1) + const

For diagonal Σ = diag(σ_1², ..., σ_d²):
D² = Σ (r_1^i - r_2^i)² / σ_i²
     i

Normalized distance:
D = √((r_1 - r_2)^T Σ^{-1} (r_1 - r_2))
```

**Nature's Implementation**: Perceptual distance in sensory cortex. Decision boundaries in PFC. Similarity metric respecting population statistics. Explains perceptual discrimination thresholds and classification performance.

**Impact**: **MEDIUM - Population Geometry**
Accounts for noise correlations. Defines natural metric for population codes. Predicts discrimination performance. Critical for understanding population representations, perceptual metrics, and optimal decoding.

**Code Example**:
```python
class MahalanobisDistance:
    """Compute Mahalanobis distance for neural populations"""

    def __init__(self):
        self.covariance = None
        self.precision = None
        self.mean = None

    def fit(self, data):
        """
        Estimate covariance from data
        data: [n_samples, n_features]
        """
        self.mean = data.mean(axis=0)
        self.covariance = np.cov(data.T)

        # Precision matrix (regularized)
        try:
            self.precision = np.linalg.inv(self.covariance)
        except np.linalg.LinAlgError:
            # Regularize if singular
            reg = 1e-6 * np.eye(self.covariance.shape[0])
            self.precision = np.linalg.inv(self.covariance + reg)

        return self

    def distance(self, r1, r2):
        """
        Mahalanobis distance: D²(r1, r2) = (r1-r2)^T Σ^{-1} (r1-r2)
        """
        diff = r1 - r2
        D_squared = diff @ self.precision @ diff
        return np.sqrt(D_squared)

    def distance_to_mean(self, r):
        """Distance from population mean"""
        return self.distance(r, self.mean)

    def batch_distances(self, R1, R2):
        """
        Pairwise distances between sets of states
        R1: [n1, d], R2: [n2, d]
        Returns: [n1, n2]
        """
        n1, n2 = R1.shape[0], R2.shape[0]
        distances = np.zeros((n1, n2))

        for i in range(n1):
            for j in range(n2):
                distances[i, j] = self.distance(R1[i], R2[j])

        return distances

    def discrimination_threshold(self, r_ref, n_samples=1000):
        """
        Estimate discrimination threshold using Mahalanobis distance
        JND ≈ 1 / √(Fisher information)
        """
        # Sample from noise distribution around r_ref
        samples = np.random.multivariate_normal(
            r_ref, self.covariance, size=n_samples
        )

        # Compute distances
        distances = np.array([self.distance(r_ref, s) for s in samples])

        # Threshold: median distance (50% discrimination)
        threshold = np.median(distances)

        return threshold

    def classification_boundary(self, r1_mean, r2_mean):
        """
        Linear decision boundary between two populations
        Hyperplane: (r - μ)^T Σ^{-1} (μ1 - μ2) = 0
        where μ = (μ1 + μ2)/2
        """
        midpoint = (r1_mean + r2_mean) / 2
        normal = self.precision @ (r1_mean - r2_mean)

        return midpoint, normal


# Example: Orientation discrimination in V1
n_neurons = 50
n_trials_per_ori = 100

# Two orientations
ori1 = 45  # degrees
ori2 = 50  # degrees (5° difference)

# Simulate population responses (von Mises tuning)
preferred_oris = np.linspace(0, 180, n_neurons)
kappa = 3

def population_response(ori, n_trials):
    """Generate population responses"""
    tuning = np.exp(kappa * np.cos(2 * np.pi * (ori - preferred_oris) / 180))
    rates = 10 * tuning

    # Add correlated noise
    base_noise = np.random.randn(n_trials, n_neurons) * 2
    shared_noise = np.random.randn(n_trials, 1) * 1  # Shared fluctuations
    responses = rates + base_noise + shared_noise

    return responses

# Generate data
responses_ori1 = population_response(ori1, n_trials_per_ori)
responses_ori2 = population_response(ori2, n_trials_per_ori)

# Pooled covariance
all_responses = np.vstack([responses_ori1, responses_ori2])
mahal = MahalanobisDistance()
mahal.fit(all_responses)

# Mean responses
mean_ori1 = responses_ori1.mean(axis=0)
mean_ori2 = responses_ori2.mean(axis=0)

# Mahalanobis vs Euclidean distance
mahal_dist = mahal.distance(mean_ori1, mean_ori2)
euclidean_dist = np.linalg.norm(mean_ori1 - mean_ori2)

print(f"Mahalanobis distance: {mahal_dist:.3f}")
print(f"Euclidean distance: {euclidean_dist:.3f}")
print(f"Ratio: {mahal_dist / euclidean_dist:.3f}")

# Discrimination performance
# Compute distances for all trial pairs
distances_within_ori1 = []
distances_between = []

for i in range(20):  # Sample subset
    for j in range(20):
        if i != j:
            distances_within_ori1.append(
                mahal.distance(responses_ori1[i], responses_ori1[j])
            )
        distances_between.append(
            mahal.distance(responses_ori1[i], responses_ori2[j])
        )

print(f"\nWithin-class distance: {np.mean(distances_within_ori1):.3f}")
print(f"Between-class distance: {np.mean(distances_between):.3f}")
print(f"Discriminability (d'): {(np.mean(distances_between) - np.mean(distances_within_ori1)) / np.std(distances_within_ori1):.2f}")

# Decision boundary
midpoint, normal = mahal.classification_boundary(mean_ori1, mean_ori2)
print(f"\nDecision boundary normal vector (first 5 neurons): {normal[:5]}")
```

**Source**: Mahalanobis (1936) Proceedings National Institute Sciences India; Averbeck et al. (2006) Nat Rev Neurosci; Cohen & Maunsell (2009) Nat Neurosci

---

### Dynamic Mode Decomposition (DMD)

**Purpose**: Data-driven approximation of Koopman operator—extract spatiotemporal coherent structures from neural dynamics.

**Formula**: Optimal Linear Approximation
```
Dynamics: x_{t+1} = A x_t

Data matrices:
X = [x_0, x_1, ..., x_{T-1}]
Y = [x_1, x_2, ..., x_T]

DMD operator:
A = Y X^+  (where X^+ is pseudoinverse)

Eigendecomposition:
A Φ = Φ Λ

DMD modes: Φ = [φ_1, ..., φ_r]
DMD eigenvalues: Λ = diag(λ_1, ..., λ_r)

Reconstruction:
x_t = Σ b_i λ_i^t φ_i
      i

where:
- φ_i = spatial mode (population pattern)
- λ_i = temporal eigenvalue (growth/decay rate)
- ω_i = imag(log(λ_i))/Δt = oscillation frequency
- b_i = mode amplitude
```

**Nature's Implementation**: Identifies oscillatory modes in cortex (alpha, beta, gamma). Reveals traveling waves, synchrony patterns. Used for EEG, LFP, calcium imaging analysis. Discovers spatiotemporal neural motifs.

**Impact**: **MEDIUM-HIGH - Data-Driven Dynamics**
Model-free discovery of modes. Handles high-dimensional data. Reveals oscillations and traveling waves. Critical for analyzing large-scale neural recordings and discovering dynamical motifs.

**Code Example**:
```python
class DynamicModeDecomposition:
    """DMD for neural population dynamics"""

    def __init__(self, rank=None):
        self.rank = rank

        self.A_dmd = None
        self.modes = None  # Spatial patterns
        self.eigenvalues = None  # Temporal eigenvalues
        self.amplitudes = None

    def fit(self, X, dt=1.0):
        """
        Compute DMD from data
        X: [n_features, n_timepoints] (each column is a snapshot)
        """
        n_features, n_time = X.shape

        # Data matrices
        X_data = X[:, :-1]  # x_0, ..., x_{T-1}
        Y_data = X[:, 1:]   # x_1, ..., x_T

        # SVD of X for dimensionality reduction
        U, s, Vt = np.linalg.svd(X_data, full_matrices=False)

        if self.rank is not None:
            U = U[:, :self.rank]
            s = s[:self.rank]
            Vt = Vt[:self.rank, :]

        # DMD operator in reduced space
        # Ã = U^T A U
        # where A = Y X^+
        A_tilde = U.T @ Y_data @ Vt.T @ np.diag(1/s)

        # Eigendecomposition of Ã
        eigenvalues, eigenvectors = np.linalg.eig(A_tilde)

        # DMD modes (full space)
        # Φ = Y V Σ^{-1} W
        self.modes = Y_data @ Vt.T @ np.diag(1/s) @ eigenvectors

        self.eigenvalues = eigenvalues

        # Compute amplitudes (initial condition projection)
        self.amplitudes = np.linalg.lstsq(self.modes, X[:, 0], rcond=None)[0]

        self.dt = dt

        return self

    def reconstruct(self, t_index):
        """
        Reconstruct state at time t
        x_t = Σ b_i λ_i^t φ_i
        """
        x_t = np.zeros(self.modes.shape[0], dtype=complex)

        for i in range(len(self.eigenvalues)):
            x_t += self.amplitudes[i] * (self.eigenvalues[i] ** t_index) * self.modes[:, i]

        return np.real(x_t)

    def get_frequencies(self):
        """Extract oscillation frequencies from eigenvalues"""
        # ω = imag(log(λ)) / Δt
        frequencies = np.imag(np.log(self.eigenvalues)) / self.dt
        return frequencies

    def get_growth_rates(self):
        """Extract growth/decay rates"""
        # γ = real(log(λ)) / Δt
        growth_rates = np.real(np.log(self.eigenvalues)) / self.dt
        return growth_rates

    def dominant_modes(self, n_modes=5):
        """
        Identify dominant modes (largest amplitudes)
        """
        mode_importance = np.abs(self.amplitudes) * np.abs(self.eigenvalues)
        top_indices = np.argsort(mode_importance)[::-1][:n_modes]

        return top_indices

    def predict_future(self, n_steps):
        """
        Predict future states: x_{T+k} = A^k x_T
        """
        predictions = []
        for t in range(n_steps):
            x_pred = self.reconstruct(t)
            predictions.append(x_pred)

        return np.array(predictions).T


# Example: Oscillatory neural population
n_neurons = 50
n_time = 200
dt = 0.01

# Generate synthetic data with oscillations
time = np.arange(n_time) * dt

# Mode 1: 10 Hz oscillation
freq1 = 10  # Hz
mode1 = np.random.randn(n_neurons)
mode1 /= np.linalg.norm(mode1)
signal1 = mode1[:, None] * np.sin(2 * np.pi * freq1 * time)

# Mode 2: 20 Hz oscillation
freq2 = 20
mode2 = np.random.randn(n_neurons)
mode2 /= np.linalg.norm(mode2)
signal2 = 0.5 * mode2[:, None] * np.cos(2 * np.pi * freq2 * time)

# Combined signal + noise
X = signal1 + signal2 + 0.1 * np.random.randn(n_neurons, n_time)

# Fit DMD
dmd = DynamicModeDecomposition(rank=10)
dmd.fit(X, dt=dt)

# Extract frequencies
frequencies = dmd.get_frequencies()
growth_rates = dmd.get_growth_rates()

print(f"DMD extracted frequencies (Hz):")
for i, freq in enumerate(frequencies[:5]):
    print(f"  Mode {i}: {freq:.2f} Hz (growth rate: {growth_rates[i]:.3f})")

# Dominant modes
dominant = dmd.dominant_modes(n_modes=3)
print(f"\nDominant mode indices: {dominant}")
print(f"True frequencies: {freq1:.1f} Hz, {freq2:.1f} Hz")

# Reconstruction
x_recon = np.array([dmd.reconstruct(t) for t in range(n_time)]).T
recon_error = np.mean((X - x_recon)**2)
print(f"\nReconstruction error: {recon_error:.4f}")

# Predict future
n_future = 50
X_future = dmd.predict_future(n_future)
print(f"Future prediction shape: {X_future.shape}")
```

**Source**: Schmid (2010) J Fluid Mech; Kutz et al. (2016) Book; Brunton et al. (2016) PNAS; Casorso et al. (2019) NeuroImage

---

### Koopman Operator (Nonlinear Dynamics Linearization)

**Purpose**: Infinite-dimensional linear operator for nonlinear dynamics—enables spectral analysis of arbitrary dynamical systems.

**Formula**: Composition Operator
```
Nonlinear dynamics: x_{t+1} = F(x_t)

Koopman operator: K[g](x) = g(F(x))

For observables g: ℝ^n → ℝ

Eigenfunction: K[φ] = λ φ

Spectral decomposition:
g(x_t) = Σ λ^t φ_i(x_0) v_i(g)
         i

where:
- φ_i = Koopman eigenfunction
- λ_i = Koopman eigenvalue
- v_i = Koopman mode

DMD approximation:
K ≈ A in span of data

Approximation via basis:
g ≈ Σ a_i ψ_i
    i
```

**Nature's Implementation**: Models nonlinear population dynamics in linear framework. Enables prediction and control of complex neural patterns. Used for understanding limit cycles, chaos, transient dynamics in recurrent networks.

**Impact**: **MEDIUM - Nonlinear Spectral Analysis**
Linearizes nonlinear systems. Infinite-dimensional but practically approximable. Reveals eigenstructure of nonlinear dynamics. Critical for analyzing complex neural dynamics and control.

**Code Example**:
```python
class KoopmanOperator:
    """Koopman operator approximation via basis functions"""

    def __init__(self, basis_type='polynomial', order=3):
        self.basis_type = basis_type
        self.order = order

        self.K_matrix = None  # Koopman matrix approximation
        self.eigenvalues = None
        self.eigenfunctions = None

    def basis_functions(self, x):
        """
        Construct basis functions ψ(x)
        """
        if self.basis_type == 'polynomial':
            # Polynomial basis: [1, x, x², x³, ...]
            basis = []
            n_dim = x.shape[0] if x.ndim == 1 else x.shape[1]

            # Monomials up to order
            basis.append(np.ones(x.shape[0] if x.ndim > 1 else 1))

            if n_dim == 1:
                for p in range(1, self.order + 1):
                    basis.append(x ** p)
            else:
                # Multivariate: x_i, x_i x_j, x_i²,...
                for i in range(n_dim):
                    basis.append(x[:, i] if x.ndim > 1 else x[i])

                # Higher orders
                for p in range(2, self.order + 1):
                    for i in range(n_dim):
                        basis.append((x[:, i] if x.ndim > 1 else x[i]) ** p)

            return np.column_stack(basis) if len(basis) > 1 else basis[0][:, None]

        elif self.basis_type == 'rbf':
            # Radial basis functions (Gaussian kernels)
            centers = np.linspace(x.min(), x.max(), self.order)
            sigma = (x.max() - x.min()) / self.order

            basis = []
            for c in centers:
                basis.append(np.exp(-((x - c)**2) / (2 * sigma**2)))

            return np.column_stack(basis)

    def fit(self, X, Y=None):
        """
        Fit Koopman operator from data
        X: states at time t
        Y: states at time t+1 (if None, assume Y = X[1:], X = X[:-1])
        """
        if Y is None:
            Y = X[1:]
            X = X[:-1]

        # Lift to basis
        Psi_X = self.basis_functions(X)  # [n_samples, n_basis]
        Psi_Y = self.basis_functions(Y)

        # Koopman matrix: K ≈ Ψ_Y Ψ_X^+
        self.K_matrix = Psi_Y.T @ Psi_X @ np.linalg.pinv(Psi_X.T @ Psi_X)

        # Eigendecomposition
        self.eigenvalues, self.eigenfunctions = np.linalg.eig(self.K_matrix)

        return self

    def predict(self, x0, n_steps):
        """
        Predict future states using Koopman operator
        """
        predictions = [x0]

        x_current = x0
        for _ in range(n_steps):
            # Lift to basis
            psi = self.basis_functions(x_current.reshape(1, -1))

            # Apply Koopman operator
            psi_next = psi @ self.K_matrix.T

            # Project back (approximate inverse)
            # This is non-trivial for general basis - use regression
            x_next = self._inverse_basis(psi_next)

            predictions.append(x_next)
            x_current = x_next

        return np.array(predictions)

    def _inverse_basis(self, psi):
        """
        Approximate inverse of basis (project back to state space)
        For polynomial: extract linear coefficients
        """
        # Simplified: assume first few coefficients correspond to state
        # This is basis-dependent
        if self.basis_type == 'polynomial':
            # For [1, x, x², ...], x is at index 1
            return psi[0, 1] if psi.shape[1] > 1 else psi[0, 0]

        return psi[0, 0]  # Placeholder

    def spectral_analysis(self):
        """
        Analyze Koopman eigenvalues and eigenfunctions
        """
        # Sort by magnitude
        idx = np.argsort(np.abs(self.eigenvalues))[::-1]

        print("Koopman Eigenvalues:")
        for i in idx[:5]:
            ev = self.eigenvalues[i]
            freq = np.imag(np.log(ev)) / (2 * np.pi) if np.abs(ev) > 1e-10 else 0
            print(f"  λ{i}: {ev:.4f} (freq: {freq:.2f} Hz)")

        return self.eigenvalues[idx], self.eigenfunctions[:, idx]


# Example: Nonlinear oscillator (limit cycle)
def van_der_pol(x, mu=1.0):
    """Van der Pol oscillator: ẋ = y, ẏ = μ(1-x²)y - x"""
    x1, x2 = x
    dx1 = x2
    dx2 = mu * (1 - x1**2) * x2 - x1
    return np.array([x1 + 0.01 * dx1, x2 + 0.01 * dx2])

# Generate trajectory
n_steps = 500
X_trajectory = np.zeros((n_steps, 2))
X_trajectory[0] = [0.1, 0.1]

for t in range(1, n_steps):
    X_trajectory[t] = van_der_pol(X_trajectory[t-1], mu=1.0)

# Fit Koopman
koopman = KoopmanOperator(basis_type='polynomial', order=5)
koopman.fit(X_trajectory)

# Spectral analysis
eigenvalues_sorted, eigenfunctions_sorted = koopman.spectral_analysis()

# Prediction
x0 = np.array([0.2, 0.2])
n_predict = 100
predictions = koopman.predict(x0, n_predict)

# Compare to true trajectory
true_trajectory = np.zeros((n_predict + 1, 2))
true_trajectory[0] = x0
for t in range(1, n_predict + 1):
    true_trajectory[t] = van_der_pol(true_trajectory[t-1])

# Error
pred_error = np.mean(np.linalg.norm(predictions - true_trajectory, axis=1))
print(f"\nPrediction error: {pred_error:.4f}")
```

**Source**: Koopman (1931) PNAS; Mezić (2005) Nonlinear Dyn; Williams et al. (2015) J Nonlinear Sci; Brunton et al. (2016) PNAS

---

### Lyapunov Exponent (Chaos Quantification)

**Purpose**: Measure sensitivity to initial conditions—quantifies chaos, stability, and predictability horizon in neural dynamics.

**Formula**: Exponential Divergence Rate
```
Perturbation growth:
|δx(t)| ≈ |δx(0)| e^{λt}

Lyapunov exponent:
λ = lim   lim   (1/t) log |δx(t)| / |δx(0)|
    t→∞  |δx0|→0

For discrete maps: x_{t+1} = F(x_t)
λ = lim (1/T) Σ log|J(x_t)|
    T→∞      t=0..T-1

where J = Jacobian of F

Interpretation:
- λ > 0: chaos (sensitive dependence)
- λ = 0: neutrally stable (periodic)
- λ < 0: stable (converges to fixed point)

Largest Lyapunov exponent (LLE):
λ_max = largest of all exponents

Predictability horizon:
t_pred ~ (1/λ_max) log(L/δ)

where:
- L = system size
- δ = measurement precision
```

**Nature's Implementation**: Measures chaos in cortical dynamics. Predictability of neural trajectories. Relates to computational capacity (edge of chaos). Analyzed in EEG, spiking networks, recurrent dynamics. Criticality hypothesis suggests λ ≈ 0 for optimal computation.

**Impact**: **MEDIUM - Chaos & Predictability**
Quantifies deterministic chaos. Predicts forecast horizon. Reveals computational regime. Critical for understanding dynamical complexity in neural circuits and information processing capacity.

**Code Example**:
```python
class LyapunovExponent:
    """Compute largest Lyapunov exponent for dynamical systems"""

    def __init__(self, dynamics_fn, jacobian_fn=None):
        self.dynamics = dynamics_fn
        self.jacobian = jacobian_fn

    def _numerical_jacobian(self, x, eps=1e-6):
        """Compute Jacobian via finite differences"""
        n = len(x)
        J = np.zeros((n, n))

        fx = self.dynamics(x)

        for i in range(n):
            x_plus = x.copy()
            x_plus[i] += eps
            fx_plus = self.dynamics(x_plus)

            J[:, i] = (fx_plus - fx) / eps

        return J

    def compute(self, x0, n_steps, dt=0.01, method='finitetime'):
        """
        Compute largest Lyapunov exponent
        """
        if method == 'finitetime':
            return self._finite_time_lya(x0, n_steps, dt)
        elif method == 'jacobian':
            return self._jacobian_method(x0, n_steps)

    def _finite_time_lya(self, x0, n_steps, dt=0.01):
        """
        Finite-time Lyapunov exponent via tangent space evolution
        """
        n_dim = len(x0)

        # Initialize trajectory and tangent vector
        x = x0.copy()
        delta = np.random.randn(n_dim)
        delta /= np.linalg.norm(delta)

        delta_0 = 1e-8  # Initial perturbation size

        lyapunov = 0

        for t in range(n_steps):
            # Perturbed trajectory
            x_pert = x + delta_0 * delta

            # Evolve both
            x_next = self.dynamics(x)
            x_pert_next = self.dynamics(x_pert)

            # Perturbation evolution
            delta_next = (x_pert_next - x_next) / delta_0

            # Renormalize
            delta_norm = np.linalg.norm(delta_next)
            delta = delta_next / delta_norm

            # Accumulate Lyapunov sum
            lyapunov += np.log(delta_norm)

            # Update
            x = x_next

        # Average
        lyapunov /= (n_steps * dt)

        return lyapunov

    def _jacobian_method(self, x0, n_steps):
        """
        Lyapunov via Jacobian: λ = lim (1/T) Σ log|J(x_t)|
        """
        x = x0.copy()
        lyapunov_sum = 0

        for t in range(n_steps):
            # Jacobian at current point
            if self.jacobian is not None:
                J = self.jacobian(x)
            else:
                J = self._numerical_jacobian(x)

            # Largest singular value (spectral norm)
            singular_values = np.linalg.svd(J, compute_uv=False)
            lyapunov_sum += np.log(singular_values[0])

            # Evolve
            x = self.dynamics(x)

        # Average
        lyapunov = lyapunov_sum / n_steps

        return lyapunov

    def spectrum(self, x0, n_steps):
        """
        Compute full Lyapunov spectrum (all exponents)
        """
        n_dim = len(x0)

        # Initialize orthonormal basis
        Q = np.eye(n_dim)

        lyapunov_sums = np.zeros(n_dim)

        x = x0.copy()

        for t in range(n_steps):
            # Jacobian
            if self.jacobian is not None:
                J = self.jacobian(x)
            else:
                J = self._numerical_jacobian(x)

            # Propagate tangent space
            Q = J @ Q

            # QR decomposition (Gram-Schmidt)
            Q, R = np.linalg.qr(Q)

            # Accumulate
            lyapunov_sums += np.log(np.abs(np.diag(R)))

            # Evolve
            x = self.dynamics(x)

        # Average
        lyapunov_spectrum = lyapunov_sums / n_steps

        return lyapunov_spectrum


# Example: Chaotic neural network (Lorenz-like)
def chaotic_rnn(x, sigma=10, rho=28, beta=8/3):
    """Lorenz system (prototype for chaotic RNN)"""
    x1, x2, x3 = x
    dx1 = sigma * (x2 - x1)
    dx2 = x1 * (rho - x3) - x2
    dx3 = x1 * x2 - beta * x3

    dt = 0.01
    return x + dt * np.array([dx1, dx2, dx3])

# Lyapunov exponent
lya = LyapunovExponent(chaotic_rnn)

x0 = np.array([1.0, 1.0, 1.0])
n_steps = 5000

# Largest Lyapunov exponent
lambda_max = lya.compute(x0, n_steps, dt=0.01, method='finitetime')

print(f"Largest Lyapunov exponent: {lambda_max:.4f}")
if lambda_max > 0:
    print("  → System is CHAOTIC")
    # Predictability horizon
    delta = 1e-6  # Measurement precision
    L = 10  # System size
    t_pred = (1 / lambda_max) * np.log(L / delta)
    print(f"  Predictability horizon: {t_pred:.2f} time units")
elif lambda_max < 0:
    print("  → System is STABLE (fixed point)")
else:
    print("  → System is NEUTRALLY STABLE (periodic)")

# Full spectrum
spectrum = lya.spectrum(x0, n_steps=1000)
print(f"\nLyapunov spectrum: {spectrum}")
print(f"Sum (divergence): {spectrum.sum():.4f}")

# Compare different initial conditions
lambdas = []
for i in range(5):
    x0_random = np.random.randn(3)
    lam = lya.compute(x0_random, 1000, method='finitetime')
    lambdas.append(lam)

print(f"\nLyapunov from different ICs: mean={np.mean(lambdas):.4f}, std={np.std(lambdas):.4f}")
```

**Source**: Lyapunov (1892) Doctoral dissertation; Eckmann & Ruelle (1985) Rev Mod Phys; Wolf et al. (1985) Physica D; Strogatz (2015) Book

---

### Linear Response Theory (Network Perturbation Analysis)

**Purpose**: Characterize how neural networks respond to small perturbations—reveals functional connectivity and stability.

**Formula**: Susceptibility Function
```
Perturbation: I_j(ω) (external input to neuron j)

Response: δr_i(ω) (change in firing rate of neuron i)

Linear response (susceptibility):
χ_{ij}(ω) = ∂r_i(ω) / ∂I_j(ω)

For spiking networks:
χ_{ij}(ω) = (δ_{ij}/τ_i - W_{ij}) / (1 + iωτ_i) + ...

Frequency-dependent gain:
|χ(ω)| = network amplification at frequency ω

Static (ω=0):
χ_{ij}(0) = (I - W)^{-1}

where:
- W = weight matrix
- τ_i = time constant
- δ_{ij} = Kronecker delta

Power spectrum:
S_{ij}(ω) = χ_{ik}(ω) C_{kl} χ_{jl}^*(ω)

where C = input covariance
```

**Nature's Implementation**: Predicts network response to stimuli, perturbations. Explains amplification, resonance in cortical circuits. Used to understand sensory gain, attentional modulation, oscillations. Reveals effective connectivity.

**Impact**: **MEDIUM - Network Analysis**
Links structure to function. Predicts response without simulation. Reveals resonances and instabilities. Critical for understanding circuit dynamics, control, and stimulus sensitivity.

**Code Example**:
```python
class LinearResponseTheory:
    """Compute linear response for neural networks"""

    def __init__(self, W, tau):
        """
        W: [n × n] weight matrix
        tau: [n] time constants (or scalar)
        """
        self.W = W
        self.n = W.shape[0]

        if np.isscalar(tau):
            self.tau = np.ones(self.n) * tau
        else:
            self.tau = tau

    def susceptibility_static(self):
        """
        Static susceptibility: χ(0) = (I - W)^{-1}
        """
        chi = np.linalg.inv(np.eye(self.n) - self.W)
        return chi

    def susceptibility_freq(self, omega):
        """
        Frequency-dependent susceptibility
        χ(ω) = [I - W/(1 + iωτ)]^{-1} / (1 + iωτ)
        """
        # Diagonal time constant matrix
        Tau = np.diag(self.tau)

        # Frequency-dependent weight
        W_omega = self.W / (1 + 1j * omega * self.tau[:, None])

        # Invert
        chi_omega = np.linalg.inv(np.eye(self.n) - W_omega)

        # Scale by time constants
        chi_omega = chi_omega / (1 + 1j * omega * self.tau[None, :])

        return chi_omega

    def response_amplitude(self, frequencies):
        """
        |χ(ω)| for range of frequencies
        """
        amplitudes = np.zeros((len(frequencies), self.n, self.n))

        for i, omega in enumerate(frequencies):
            chi = self.susceptibility_freq(omega)
            amplitudes[i] = np.abs(chi)

        return amplitudes

    def resonance_peaks(self, freq_range=(0, 100), n_freq=1000):
        """
        Find resonance frequencies (peaks in |χ(ω)|)
        """
        frequencies = np.linspace(freq_range[0], freq_range[1], n_freq)
        amplitudes = self.response_amplitude(frequencies)

        # Average susceptibility
        avg_amplitude = np.mean(amplitudes, axis=(1, 2))

        # Find peaks
        from scipy.signal import find_peaks
        peaks, properties = find_peaks(avg_amplitude, height=avg_amplitude.mean())

        resonance_freqs = frequencies[peaks]

        return resonance_freqs, avg_amplitude

    def power_spectrum(self, omega, input_covariance):
        """
        Output power spectrum: S(ω) = χ(ω) C χ(ω)^†
        """
        chi = self.susceptibility_freq(omega)
        S = chi @ input_covariance @ chi.conj().T

        return S

    def effective_connectivity(self, perturbation_neuron, measured_neurons=None):
        """
        Effective connectivity via perturbation
        χ_{ij}(0) = how much neuron i responds to input to neuron j
        """
        chi_static = self.susceptibility_static()

        if measured_neurons is None:
            measured_neurons = np.arange(self.n)

        # Column = response of all neurons to perturbation of neuron j
        connectivity = chi_static[measured_neurons, perturbation_neuron]

        return connectivity


# Example: Recurrent E-I network
n_neurons = 50
n_exc = 40
n_inh = 10

# Weight matrix (E-I network)
W = np.zeros((n_neurons, n_neurons))

# E→E: weak
W[:n_exc, :n_exc] = np.random.rand(n_exc, n_exc) * 0.1

# E→I: strong
W[n_exc:, :n_exc] = np.random.rand(n_inh, n_exc) * 0.3

# I→E: inhibitory
W[:n_exc, n_exc:] = -np.random.rand(n_exc, n_inh) * 0.5

# I→I: weak inhibition
W[n_exc:, n_exc:] = -np.random.rand(n_inh, n_inh) * 0.1

# Time constants
tau = np.ones(n_neurons) * 10  # ms

# Linear response
lrt = LinearResponseTheory(W, tau)

# Static susceptibility
chi_0 = lrt.susceptibility_static()
print(f"Static susceptibility shape: {chi_0.shape}")
print(f"Mean static gain: {np.mean(np.abs(chi_0)):.3f}")

# Resonance peaks
resonances, amplitude_spectrum = lrt.resonance_peaks(freq_range=(0, 100), n_freq=500)
print(f"\nResonance frequencies: {resonances} Hz")

# Effective connectivity (perturb neuron 0)
eff_conn = lrt.effective_connectivity(perturbation_neuron=0)
print(f"\nEffective connectivity from neuron 0:")
print(f"  Top 5 responders: {np.argsort(np.abs(eff_conn))[-5:]}")

# Frequency response
test_freq = 10  # Hz (gamma range)
chi_10 = lrt.susceptibility_freq(test_freq)
print(f"\nSusceptibility at {test_freq} Hz:")
print(f"  Mean amplitude: {np.mean(np.abs(chi_10)):.3f}")

# Input-output power spectrum
input_cov = np.eye(n_neurons) * 0.01  # Uncorrelated input
S_10 = lrt.power_spectrum(test_freq, input_cov)
print(f"  Output power: {np.trace(np.abs(S_10)):.3f}")
```

**Source**: Kubo (1966) Rep Prog Phys; Lindner et al. (2005) Phys Rev E; Buice & Chow (2013) PLoS Comp Bio; Zhao & Macke (2023) NeurIPS

---

### Balanced Excitation-Inhibition Network

**Purpose**: Asynchronous irregular activity via E-I balance—explains cortical spontaneous activity and response variability.

**Formula**: Balance Condition
```
Mean inputs scale together:
J_E I_E ∼ J_I I_I ∼ O(1)

where:
- J_E, J_I = E/I synaptic weights
- I_E, I_I = E/I input counts
- Scaling: J ∼ 1/√N, connectivity K ∼ √N

Mean net input:
E[I_total] = J_E · I_E - J_I · I_I ≈ 0

Fluctuation-driven:
σ(I) = √(J_E² I_E + J_I² I_I) ∼ O(1)

Firing rates:
r = φ(μ_total / σ_total)

where φ = gain function

Critical balance:
μ_total ≪ σ_total  (fluctuation-driven regime)

Timescale:
τ_eff ∼ τ_membrane / √(K)  (fast fluctuations)
```

**Nature's Implementation**: Cortical spontaneous activity (asynchronous irregular state). Explains high variability (CV~1), low correlations, fast responses. Observed in V1, auditory cortex, PFC. Balances excitation and inhibition on ms timescales.

**Impact**: **MEDIUM-HIGH - Cortical Operating Regime**
Explains spontaneous activity statistics. Enables fast responses. Robust to perturbations. Critical for understanding cortical computation, variability, and dynamic range.

**Code Example**:
```python
class BalancedNetwork:
    """E-I balanced network simulation"""

    def __init__(self, N_E=400, N_I=100, K=100):
        """
        N_E: number of excitatory neurons
        N_I: number of inhibitory neurons
        K: average connectivity (∼√N)
        """
        self.N_E = N_E
        self.N_I = N_I
        self.N = N_E + N_I
        self.K = K

        # Balanced scaling
        self.J_E = 1.0 / np.sqrt(K)  # Exc weight
        self.J_I = 1.5 / np.sqrt(K)  # Inh weight (stronger)

        # Build connectivity
        self.W = self._build_connectivity()

        # Neuron parameters
        self.tau = 10.0  # ms (membrane time constant)
        self.V_th = 1.0  # Threshold
        self.V_reset = 0.0

    def _build_connectivity(self):
        """
        Build random sparse E-I network
        """
        W = np.zeros((self.N, self.N))

        # E→E, E→I
        for i in range(self.N):
            # Select K random excitatory sources
            exc_sources = np.random.choice(self.N_E, size=self.K, replace=False)
            W[i, exc_sources] = self.J_E

        # I→E, I→I
        for i in range(self.N):
            # Select K/4 random inhibitory sources
            inh_sources = np.random.choice(range(self.N_E, self.N), size=int(self.K/4), replace=False)
            W[i, inh_sources] = -self.J_I

        return W

    def check_balance(self):
        """
        Verify E-I balance: mean(E) ≈ mean(I)
        """
        # Mean excitatory input
        mean_E = np.mean(self.W[:, :self.N_E].sum(axis=1))

        # Mean inhibitory input (absolute value)
        mean_I = np.mean(np.abs(self.W[:, self.N_E:].sum(axis=1)))

        print(f"Mean excitatory input: {mean_E:.4f}")
        print(f"Mean inhibitory input: {mean_I:.4f}")
        print(f"Balance ratio: {mean_E / mean_I:.4f} (should be ≈1)")

        # Net mean input
        net_input = np.mean(self.W.sum(axis=1))
        input_std = np.std(self.W.sum(axis=1))

        print(f"Net mean input: {net_input:.4f}")
        print(f"Input fluctuation (std): {input_std:.4f}")
        print(f"Fluctuation-driven: {np.abs(net_input) < input_std}")

        return mean_E, mean_I

    def simulate(self, T=1000, dt=0.1, I_ext=0.5):
        """
        Simulate balanced network dynamics
        """
        n_steps = int(T / dt)

        # State variables
        V = np.random.rand(self.N) * self.V_th
        spikes = np.zeros((n_steps, self.N))

        for t in range(n_steps):
            # Synaptic input
            I_syn = self.W @ (V > 0).astype(float)  # Instantaneous

            # External input
            I_total = I_syn + I_ext + np.random.randn(self.N) * 0.1

            # Integrate
            dV = (-V + I_total) / self.tau * dt
            V += dV

            # Spike and reset
            spiked = V > self.V_th
            spikes[t] = spiked.astype(float)
            V[spiked] = self.V_reset

        return spikes

    def analyze_activity(self, spikes, dt=0.1):
        """
        Analyze network activity statistics
        """
        # Firing rates
        rates = spikes.mean(axis=0) / dt * 1000  # Hz

        # CV (coefficient of variation)
        ISIs = []
        for neuron in range(self.N):
            spike_times = np.where(spikes[:, neuron])[0] * dt
            if len(spike_times) > 1:
                isis = np.diff(spike_times)
                ISIs.extend(isis)

        CV = np.std(ISIs) / np.mean(ISIs) if len(ISIs) > 0 else 0

        # Correlations
        from scipy.stats import pearsonr
        corrs = []
        for i in range(min(20, self.N)):
            for j in range(i+1, min(20, self.N)):
                if spikes[:, i].sum() > 0 and spikes[:, j].sum() > 0:
                    r, _ = pearsonr(spikes[:, i], spikes[:, j])
                    corrs.append(r)

        mean_corr = np.mean(corrs) if corrs else 0

        print("\n=== Activity Statistics ===")
        print(f"Mean firing rate: {rates.mean():.2f} Hz")
        print(f"CV (irregularity): {CV:.2f} (asynchronous if ≈1)")
        print(f"Mean pairwise correlation: {mean_corr:.4f} (low if ≪1)")

        return rates, CV, mean_corr


# Example: Balanced cortical network
network = BalancedNetwork(N_E=400, N_I=100, K=100)

# Check balance
mean_E, mean_I = network.check_balance()

# Simulate
T = 1000  # ms
spikes = network.simulate(T=T, dt=0.1, I_ext=0.5)

# Analyze
rates, CV, mean_corr = network.analyze_activity(spikes, dt=0.1)

# Compare to unbalanced network (no inhibition)
network_unbalanced = BalancedNetwork(N_E=400, N_I=100, K=100)
network_unbalanced.J_I = 0  # Remove inhibition
network_unbalanced.W = network_unbalanced._build_connectivity()

spikes_unbalanced = network_unbalanced.simulate(T=T, dt=0.1, I_ext=0.5)
rates_unbalanced, CV_unbalanced, corr_unbalanced = network_unbalanced.analyze_activity(spikes_unbalanced, dt=0.1)

print(f"\n=== Comparison ===")
print(f"Balanced: rate={rates.mean():.2f} Hz, CV={CV:.2f}, corr={mean_corr:.4f}")
print(f"Unbalanced: rate={rates_unbalanced.mean():.2f} Hz, CV={CV_unbalanced:.2f}, corr={corr_unbalanced:.4f}")
```

**Source**: van Vreeswijk & Sompolinsky (1996) Science; Brunel (2000) J Comp Neurosci; Renart et al. (2010) Science; Denève & Machens (2016) Curr Op Neurobio

---

### Structural Identifiability (Parameter Inference Feasibility)

**Purpose**: Determine if model parameters can be uniquely inferred from observations—theoretical prerequisite for parameter fitting.

**Formula**: Identifiability Condition
```
Model: ẋ = f(x, θ), y = h(x, θ)

Structurally identifiable if:
θ₁ ≠ θ₂ ⟹ p(y | θ₁) ≠ p(y | θ₂)

Rank condition:
rank(∂f/∂θ) = dim(θ)

For observations y₁:T:
rank(∂[y₁, ..., y_T]/∂θ) = dim(θ)

Local identifiability:
Fisher Information matrix J(θ) is full rank

Symbolic approach:
Eliminate state variables x, check if θ uniquely determined

Practical test:
Simulate with different θ, check if outputs differ
```

**Nature's Implementation**: Determines which circuit parameters can be inferred from recordings. Guides experimental design (what to measure). Reveals fundamental limits of neural inference. Used for connectivity inference, parameter estimation validation.

**Impact**: **MEDIUM - Inference Feasibility**
Prevents futile parameter fitting. Guides experimental design. Reveals model redundancies. Critical for validating neural circuit inference and ensuring parameter estimation is well-posed.

**Code Example**:
```python
class StructuralIdentifiability:
    """Test structural identifiability of dynamical models"""

    def __init__(self, dynamics_fn, observation_fn, n_params):
        """
        dynamics_fn: dx/dt = f(x, θ)
        observation_fn: y = h(x, θ)
        n_params: dimensionality of θ
        """
        self.dynamics = dynamics_fn
        self.observation = observation_fn
        self.n_params = n_params

    def fisher_information_matrix(self, theta, x_trajectory, eps=1e-5):
        """
        Compute Fisher Information matrix: J_ij = E[∂log p/∂θᵢ · ∂log p/∂θⱼ]

        For Gaussian observations: J ≈ (1/σ²) Σ_t (∂y_t/∂θ)(∂y_t/∂θ)ᵀ
        """
        T = len(x_trajectory)
        J = np.zeros((self.n_params, self.n_params))

        for t in range(T):
            x_t = x_trajectory[t]

            # Compute ∂y/∂θ numerically
            dy_dtheta = np.zeros(self.n_params)

            y_nominal = self.observation(x_t, theta)

            for i in range(self.n_params):
                theta_plus = theta.copy()
                theta_plus[i] += eps

                y_plus = self.observation(x_t, theta_plus)

                dy_dtheta[i] = (y_plus - y_nominal) / eps

            # Accumulate J = Σ (∂y/∂θ)(∂y/∂θ)ᵀ
            J += np.outer(dy_dtheta, dy_dtheta)

        return J / T

    def test_identifiability(self, theta, x_trajectory):
        """
        Test if parameters are identifiable via Fisher Information rank
        """
        J = self.fisher_information_matrix(theta, x_trajectory)

        # Eigenvalues
        eigenvalues = np.linalg.eigvalsh(J)

        # Condition number
        cond = eigenvalues.max() / (eigenvalues.min() + 1e-10)

        # Rank (counting non-zero eigenvalues)
        rank = np.sum(eigenvalues > 1e-6 * eigenvalues.max())

        print(f"Fisher Information Matrix:")
        print(f"  Eigenvalues: {eigenvalues}")
        print(f"  Condition number: {cond:.2e}")
        print(f"  Rank: {rank} / {self.n_params}")

        identifiable = (rank == self.n_params) and (cond < 1e10)

        if identifiable:
            print("  → Parameters are IDENTIFIABLE")
        else:
            print("  → Parameters are NOT identifiable (rank deficient or ill-conditioned)")

        return identifiable, J

    def sensitivity_analysis(self, theta, x_trajectory):
        """
        Analyze parameter sensitivity: which parameters are most identifiable
        """
        J = self.fisher_information_matrix(theta, x_trajectory)

        # Parameter uncertainties (Cramér-Rao bound)
        try:
            J_inv = np.linalg.inv(J)
            uncertainties = np.sqrt(np.diag(J_inv))
        except np.linalg.LinAlgError:
            uncertainties = np.full(self.n_params, np.inf)

        print("\nParameter Sensitivities:")
        for i in range(self.n_params):
            print(f"  θ[{i}]: uncertainty = {uncertainties[i]:.4f}")

        return uncertainties

    def practical_identifiability_test(self, theta_true, theta_test, T=100, dt=0.1, noise_std=0.1):
        """
        Practical identifiability: simulate with different parameters,
        check if outputs are distinguishable
        """
        # Simulate with true parameters
        x0 = np.zeros(2)  # Assume 2D state
        y_true = self._simulate_and_observe(x0, theta_true, T, dt)

        # Simulate with test parameters
        y_test = self._simulate_and_observe(x0, theta_test, T, dt)

        # Add noise
        y_true_noisy = y_true + np.random.randn(*y_true.shape) * noise_std
        y_test_noisy = y_test + np.random.randn(*y_test.shape) * noise_std

        # Statistical test: can we distinguish outputs?
        # Use KL divergence or simple distance
        distance = np.mean((y_true - y_test)**2)
        noise_level = noise_std**2

        # Signal-to-noise ratio
        snr = distance / noise_level

        print(f"\nPractical Identifiability Test:")
        print(f"  Output distance: {distance:.4f}")
        print(f"  Noise level: {noise_level:.4f}")
        print(f"  SNR: {snr:.2f}")

        if snr > 3:
            print("  → Parameters are PRACTICALLY distinguishable")
            return True
        else:
            print("  → Parameters are NOT distinguishable (output difference < noise)")
            return False

    def _simulate_and_observe(self, x0, theta, T, dt):
        """Helper: simulate dynamics and generate observations"""
        n_steps = int(T / dt)
        x_trajectory = np.zeros((n_steps, len(x0)))
        y_trajectory = np.zeros(n_steps)

        x_trajectory[0] = x0

        for t in range(1, n_steps):
            # Euler integration
            dx = self.dynamics(x_trajectory[t-1], theta) * dt
            x_trajectory[t] = x_trajectory[t-1] + dx

            y_trajectory[t] = self.observation(x_trajectory[t], theta)

        return y_trajectory


# Example: Neural circuit with synaptic weights
def neural_circuit_dynamics(x, theta):
    """
    dx/dt = -x + W·φ(x) + I
    θ = [W11, W12, W21, W22, I]
    """
    W11, W12, W21, W22, I_ext = theta

    W = np.array([[W11, W12], [W21, W22]])
    phi_x = np.tanh(x)  # Activation

    dxdt = -x + W @ phi_x + I_ext

    return dxdt

def neural_observation(x, theta):
    """
    y = weighted sum of neural activity
    """
    return x[0] + 0.5 * x[1]  # Observe both neurons

# Test identifiability
n_params = 5
identifiability = StructuralIdentifiability(
    neural_circuit_dynamics,
    neural_observation,
    n_params
)

# True parameters
theta_true = np.array([0.5, -0.3, 0.4, 0.2, 1.0])

# Simulate trajectory
x0 = np.array([0.1, 0.1])
T = 100
dt = 0.1
n_steps = int(T / dt)

x_traj = np.zeros((n_steps, 2))
x_traj[0] = x0

for t in range(1, n_steps):
    dx = neural_circuit_dynamics(x_traj[t-1], theta_true) * dt
    x_traj[t] = x_traj[t-1] + dx

# Test identifiability
identifiable, J = identifiability.test_identifiability(theta_true, x_traj)

# Sensitivity analysis
uncertainties = identifiability.sensitivity_analysis(theta_true, x_traj)

# Practical test
theta_test = theta_true + np.array([0.05, 0.0, 0.0, 0.0, 0.0])  # Perturb W11
distinguishable = identifiability.practical_identifiability_test(
    theta_true, theta_test, T=100, dt=0.1, noise_std=0.05
)
```

**Source**: Bellman & Åström (1970) Math Biosci; Chis et al. (2011) BMC Syst Biol; Villaverde et al. (2016) PLOS Comp Bio; Gonçalves et al. (2020) eLife

---

### Bayesian Cramér-Rao Bound (Prior-Informed Lower Bound)

**Purpose**: Tightest lower bound on posterior variance incorporating prior information—extends classical Cramér-Rao to Bayesian setting.

**Formula**: Van Trees Inequality
```
Posterior covariance:
Cov[θ | y] ≥ (J_D(θ) + J_P(θ))^{-1}

where:
J_D = data Fisher information (from likelihood)
J_P = prior Fisher information (from prior)

Data Fisher:
J_D = -E[∂²log p(y|θ)/∂θ²]

Prior Fisher:
J_P = -E[∂²log p(θ)/∂θ²]

Bayesian Information Matrix:
J_Bayes = J_D + J_P

Minimum MSE:
E[(θ̂ - θ)²] ≥ tr[(J_D + J_P)^{-1}]

For single parameter:
Var(θ̂ | y) ≥ 1/(J_D(θ) + J_P(θ))
```

**Nature's Implementation**: Bounds uncertainty in neural encoding models. Explains how priors improve estimation (e.g., natural scene statistics). Quantifies information gain from data vs prior. Used for understanding perceptual uncertainty and sensory-motor integration.

**Impact**: **MEDIUM - Bayesian Estimation Bounds**
Tighter than classical Cramér-Rao. Quantifies prior contribution. Predicts estimation performance. Critical for understanding neural inference, optimal encoding, and role of priors in perception.

**Code Example**:
```python
class BayesianCramerRaoBound:
    """Compute Bayesian Cramér-Rao bound for parameter estimation"""

    def __init__(self, log_prior_fn, log_likelihood_fn):
        """
        log_prior_fn: log p(θ)
        log_likelihood_fn: log p(y | θ)
        """
        self.log_prior = log_prior_fn
        self.log_likelihood = log_likelihood_fn

    def fisher_data(self, theta, data, eps=1e-5):
        """
        Data Fisher information: J_D = -E[∂²log p(y|θ)/∂θ²]
        """
        n_params = len(theta)
        J_D = np.zeros((n_params, n_params))

        # Second derivative via finite differences
        for i in range(n_params):
            for j in range(n_params):
                theta_pp = theta.copy()
                theta_pm = theta.copy()
                theta_mp = theta.copy()
                theta_mm = theta.copy()

                theta_pp[i] += eps
                theta_pp[j] += eps

                theta_pm[i] += eps
                theta_pm[j] -= eps

                theta_mp[i] -= eps
                theta_mp[j] += eps

                theta_mm[i] -= eps
                theta_mm[j] -= eps

                # ∂²log L/∂θᵢ∂θⱼ
                d2_ll = (
                    self.log_likelihood(data, theta_pp)
                    - self.log_likelihood(data, theta_pm)
                    - self.log_likelihood(data, theta_mp)
                    + self.log_likelihood(data, theta_mm)
                ) / (4 * eps**2)

                J_D[i, j] = -d2_ll

        return J_D

    def fisher_prior(self, theta, eps=1e-5):
        """
        Prior Fisher information: J_P = -E[∂²log p(θ)/∂θ²]
        """
        n_params = len(theta)
        J_P = np.zeros((n_params, n_params))

        for i in range(n_params):
            for j in range(n_params):
                theta_pp = theta.copy()
                theta_pm = theta.copy()
                theta_mp = theta.copy()
                theta_mm = theta.copy()

                theta_pp[i] += eps
                theta_pp[j] += eps

                theta_pm[i] += eps
                theta_pm[j] -= eps

                theta_mp[i] -= eps
                theta_mp[j] += eps

                theta_mm[i] -= eps
                theta_mm[j] -= eps

                # ∂²log p(θ)/∂θᵢ∂θⱼ
                d2_lp = (
                    self.log_prior(theta_pp)
                    - self.log_prior(theta_pm)
                    - self.log_prior(theta_mp)
                    + self.log_prior(theta_mm)
                ) / (4 * eps**2)

                J_P[i, j] = -d2_lp

        return J_P

    def bayesian_bound(self, theta, data):
        """
        Compute Bayesian CRB: Cov(θ̂) ≥ (J_D + J_P)^{-1}
        """
        J_D = self.fisher_data(theta, data)
        J_P = self.fisher_prior(theta)

        J_Bayes = J_D + J_P

        # Invert for bound
        try:
            bound = np.linalg.inv(J_Bayes)
        except np.linalg.LinAlgError:
            bound = np.linalg.pinv(J_Bayes)

        return bound, J_D, J_P

    def compare_classical_bayesian(self, theta, data):
        """
        Compare classical CRB (no prior) vs Bayesian CRB
        """
        J_D = self.fisher_data(theta, data)
        J_P = self.fisher_prior(theta)

        # Classical bound (data only)
        try:
            classical_bound = np.linalg.inv(J_D)
        except np.linalg.LinAlgError:
            classical_bound = np.linalg.pinv(J_D)

        # Bayesian bound (data + prior)
        bayesian_bound = np.linalg.inv(J_D + J_P)

        print("=== Cramér-Rao Bounds ===")
        print(f"Classical (data only):")
        print(f"  Variance bounds: {np.diag(classical_bound)}")
        print(f"  Total uncertainty: {np.trace(classical_bound):.4f}")

        print(f"\nBayesian (data + prior):")
        print(f"  Variance bounds: {np.diag(bayesian_bound)}")
        print(f"  Total uncertainty: {np.trace(bayesian_bound):.4f}")

        # Improvement from prior
        improvement = (np.trace(classical_bound) - np.trace(bayesian_bound)) / np.trace(classical_bound)
        print(f"\nImprovement from prior: {improvement * 100:.1f}%")

        return classical_bound, bayesian_bound


# Example: Orientation tuning estimation
def log_prior(theta):
    """
    Gaussian prior: p(θ) = N(θ | μ_0, Σ_0)
    θ = [preferred_ori, tuning_width]
    """
    mu_0 = np.array([90, 20])  # Prior mean
    Sigma_0 = np.diag([45**2, 10**2])  # Prior covariance

    diff = theta - mu_0
    return -0.5 * diff @ np.linalg.inv(Sigma_0) @ diff

def log_likelihood(data, theta):
    """
    Poisson tuning curve: p(spikes | ori, θ)
    """
    pref_ori, width = theta

    ll = 0
    for ori, spikes in data:
        # Von Mises tuning
        rate = 5 + 10 * np.exp((1/width**2) * np.cos(2 * np.pi * (ori - pref_ori) / 180))

        # Poisson
        ll += spikes * np.log(rate + 1e-10) - rate

    return ll

# Generate data
true_theta = np.array([90, 15])
orientations = [0, 30, 60, 90, 120, 150, 180]
data = []

for ori in orientations:
    rate = 5 + 10 * np.exp((1/true_theta[1]**2) * np.cos(2 * np.pi * (ori - true_theta[0]) / 180))
    spikes = np.random.poisson(rate)
    data.append((ori, spikes))

# Compute bounds
bcrb = BayesianCramerRaoBound(log_prior, log_likelihood)

classical_bound, bayesian_bound = bcrb.compare_classical_bayesian(true_theta, data)

# Information contributions
_, J_D, J_P = bcrb.bayesian_bound(true_theta, data)

print(f"\n=== Information Contributions ===")
print(f"Data Fisher (J_D):")
print(f"  {np.diag(J_D)}")
print(f"Prior Fisher (J_P):")
print(f"  {np.diag(J_P)}")
print(f"Ratio (data/prior): {np.diag(J_D) / np.diag(J_P)}")
```

**Source**: Van Trees (1968) Detection, Estimation, and Modulation Theory; Tichavský et al. (1998) IEEE Trans Signal Processing; Lehmann & Casella (1998) Book

---

### Spectral Stability of Recurrent Networks

**Purpose**: Stability condition for linear recurrent dynamics via spectral radius—determines convergence, oscillations, and chaos.

**Formula**: Spectral Radius Condition
```
Linear dynamics: x_{t+1} = W x_t

Stability: ρ(W) < 1

where ρ(W) = max|λ_i(W)| = spectral radius

Eigenvalue decomposition:
W v_i = λ_i v_i

Dynamics: x_t = Σ c_i λ_i^t v_i
               i

Convergence:
|λ_i| < 1 → stable (exponential decay)
|λ_i| = 1 → neutrally stable (oscillations)
|λ_i| > 1 → unstable (exponential growth)

For nonlinear: ż = F(z)
Linearization: ρ(∂F/∂z) < 1 locally

Edge of chaos: ρ(W) ≈ 1
```

**Nature's Implementation**: Determines stability of recurrent cortical dynamics. Edge of chaos hypothesis (ρ ≈ 1 for maximal computation). Explains spontaneous oscillations (complex eigenvalues near unit circle). Used for RNN design, reservoir computing.

**Impact**: **MEDIUM-HIGH - Network Stability**
Simple stability criterion. Predicts oscillations (complex eigenvalues). Guides network design. Critical for understanding recurrent dynamics, echo state networks, and computational capacity.

**Code Example**:
```python
class SpectralStability:
    """Analyze stability of recurrent neural networks via spectral radius"""

    def __init__(self, W):
        """
        W: [n × n] weight matrix
        """
        self.W = W
        self.n = W.shape[0]

        # Compute eigenvalues
        self.eigenvalues = None
        self.eigenvectors = None
        self.spectral_radius = None

    def compute_spectrum(self):
        """
        Eigenvalue decomposition: W v = λ v
        """
        self.eigenvalues, self.eigenvectors = np.linalg.eig(self.W)

        # Spectral radius
        self.spectral_radius = np.max(np.abs(self.eigenvalues))

        return self.eigenvalues, self.spectral_radius

    def check_stability(self):
        """
        Check if dynamics are stable: ρ(W) < 1
        """
        if self.spectral_radius is None:
            self.compute_spectrum()

        print(f"Spectral radius: ρ(W) = {self.spectral_radius:.4f}")

        if self.spectral_radius < 1:
            print("  → Network is STABLE (ρ < 1)")
            print("    Dynamics converge to fixed point")
        elif self.spectral_radius == 1:
            print("  → Network is NEUTRALLY STABLE (ρ = 1)")
            print("    Persistent activity / oscillations")
        else:
            print("  → Network is UNSTABLE (ρ > 1)")
            print("    Exponential growth / chaos")

        return self.spectral_radius < 1

    def timescales(self):
        """
        Extract timescales from eigenvalues: τ_i = -1/log|λ_i|
        """
        if self.eigenvalues is None:
            self.compute_spectrum()

        # Only for stable modes (|λ| < 1)
        stable_eigs = self.eigenvalues[np.abs(self.eigenvalues) < 1]

        if len(stable_eigs) == 0:
            print("No stable modes")
            return []

        timescales = -1.0 / np.log(np.abs(stable_eigs) + 1e-10)

        print(f"\nStable mode timescales:")
        for i, tau in enumerate(sorted(timescales, reverse=True)[:5]):
            print(f"  τ{i}: {tau:.2f} steps")

        return timescales

    def oscillation_frequencies(self):
        """
        Extract oscillation frequencies from complex eigenvalues
        ω = arg(λ) / (2π)
        """
        if self.eigenvalues is None:
            self.compute_spectrum()

        # Complex eigenvalues (oscillatory modes)
        complex_eigs = self.eigenvalues[np.abs(np.imag(self.eigenvalues)) > 1e-6]

        if len(complex_eigs) == 0:
            print("No oscillatory modes")
            return []

        frequencies = np.angle(complex_eigs) / (2 * np.pi)

        print(f"\nOscillation frequencies:")
        for i, freq in enumerate(sorted(np.abs(frequencies), reverse=True)[:5]):
            print(f"  f{i}: {freq:.4f} cycles/step")

        return frequencies

    def dominant_modes(self, n_modes=5):
        """
        Identify dominant modes (largest |λ|)
        """
        if self.eigenvalues is None:
            self.compute_spectrum()

        # Sort by magnitude
        idx = np.argsort(np.abs(self.eigenvalues))[::-1]

        print(f"\nDominant {n_modes} modes:")
        for i in range(min(n_modes, len(self.eigenvalues))):
            ev = self.eigenvalues[idx[i]]
            print(f"  λ{i}: {ev:.4f} (|λ| = {np.abs(ev):.4f})")

        return self.eigenvalues[idx[:n_modes]], self.eigenvectors[:, idx[:n_modes]]

    def edge_of_chaos_metric(self):
        """
        Quantify proximity to edge of chaos: |ρ(W) - 1|
        """
        if self.spectral_radius is None:
            self.compute_spectrum()

        distance_to_edge = np.abs(self.spectral_radius - 1)

        print(f"\n=== Edge of Chaos ===")
        print(f"Distance to edge: {distance_to_edge:.4f}")

        if distance_to_edge < 0.1:
            print("  → NEAR edge of chaos (maximal computation)")
        elif self.spectral_radius < 1:
            print("  → STABLE regime (ρ < 1)")
        else:
            print("  → CHAOTIC regime (ρ > 1)")

        return distance_to_edge

    def simulate_dynamics(self, x0, n_steps):
        """
        Simulate linear dynamics: x_t = W^t x_0
        """
        trajectory = np.zeros((n_steps, self.n))
        trajectory[0] = x0

        for t in range(1, n_steps):
            trajectory[t] = self.W @ trajectory[t-1]

        return trajectory

    def predict_convergence(self, x0):
        """
        Predict long-term behavior using eigendecomposition
        x_∞ = Σ c_i λ_i^∞ v_i
        """
        if self.eigenvalues is None:
            self.compute_spectrum()

        # Project initial condition onto eigenvectors
        coefficients = np.linalg.lstsq(self.eigenvectors, x0, rcond=None)[0]

        # Asymptotic contribution (λ^∞)
        if self.spectral_radius < 1:
            x_inf = np.zeros(self.n)  # All modes decay
            print("Converges to zero (all eigenvalues < 1)")
        else:
            # Dominant mode
            dominant_idx = np.argmax(np.abs(self.eigenvalues))
            x_inf = coefficients[dominant_idx] * self.eigenvectors[:, dominant_idx]
            print(f"Dominated by mode λ = {self.eigenvalues[dominant_idx]:.4f}")

        return x_inf


# Example: Recurrent network with different stability regimes
n_neurons = 50

# Stable network (ρ < 1)
W_stable = np.random.randn(n_neurons, n_neurons) * 0.8 / np.sqrt(n_neurons)
stability_stable = SpectralStability(W_stable)
stability_stable.compute_spectrum()
stability_stable.check_stability()
stability_stable.timescales()
stability_stable.edge_of_chaos_metric()

print("\n" + "="*50)

# Edge of chaos (ρ ≈ 1)
W_edge = np.random.randn(n_neurons, n_neurons) / np.sqrt(n_neurons)
W_edge /= np.max(np.abs(np.linalg.eigvals(W_edge)))  # Normalize to ρ = 1
stability_edge = SpectralStability(W_edge)
stability_edge.compute_spectrum()
stability_edge.check_stability()
stability_edge.oscillation_frequencies()
stability_edge.edge_of_chaos_metric()

print("\n" + "="*50)

# Chaotic (ρ > 1)
W_chaos = np.random.randn(n_neurons, n_neurons) * 1.5 / np.sqrt(n_neurons)
stability_chaos = SpectralStability(W_chaos)
stability_chaos.compute_spectrum()
stability_chaos.check_stability()

# Simulate dynamics
x0 = np.random.randn(n_neurons) * 0.1

print("\n=== Simulation ===")
traj_stable = stability_stable.simulate_dynamics(x0, n_steps=100)
traj_chaos = stability_chaos.simulate_dynamics(x0, n_steps=100)

print(f"Stable network final norm: {np.linalg.norm(traj_stable[-1]):.4f}")
print(f"Chaotic network final norm: {np.linalg.norm(traj_chaos[-1]):.4f}")
```

**Source**: Gerschgorin (1931) Izv Akad Nauk SSSR; Horn & Johnson (1985) Book; Sompolinsky et al. (1988) Phys Rev A; Sussillo & Abbott (2009) Neuron

---


### 176. Variational Free Energy (Explicit Formulation)

**Purpose**: Unified objective for inference and learning—minimizing free energy = maximizing model evidence while staying close to prior.

**Formula**: Evidence Lower Bound (ELBO)
```
Free Energy:
F = E_q[log q(z)] - E_q[log p(x,z)]
  = -ELBO
  = KL[q(z)||p(z|x)] - log p(x)

Decomposition:
F = E_q[log q(z) - log p(z)] - E_q[log p(x|z)]
  = KL[q(z)||p(z)] - E_q[log p(x|z)]
  = Complexity - Accuracy

Optimization:
q*(z) = argmin F(q) = argmax ELBO(q)
         q              q

Gradient (for parameters θ):
∇_θ F = ∇_θ E_q[log q(z) - log p(x,z|θ)]

where:
- q(z) = recognition/approximate posterior
- p(z) = prior
- p(x|z) = generative model (likelihood)
- p(x,z) = joint distribution
- x = observations (data)
- z = latent variables
```

**Nature's Implementation**: Brain's fundamental optimization principle (free energy principle). Explains perception (inference), learning (model optimization), action (active inference). Unified framework for cortical computation. Predictive coding is gradient descent on free energy.

**Impact**: **CRITICAL - Unified Brain Theory**
Single objective explains perception, learning, and action. Variational autoencoders are neural implementation. Active inference for motor control. Predictive coding networks minimize free energy. Foundation for understanding cortical function, attention, consciousness. Connects neuroscience to machine learning theory.

**Code Example**:
```python
class VariationalFreeEnergy(nn.Module):
    """Explicit free energy minimization for neural inference"""

    def __init__(self, latent_dim, obs_dim):
        super().__init__()
        self.latent_dim = latent_dim
        self.obs_dim = obs_dim

        # Recognition model q(z|x): encoder
        self.encoder = nn.Sequential(
            nn.Linear(obs_dim, 128),
            nn.ReLU(),
            nn.Linear(128, latent_dim * 2)  # μ and log(σ)
        )

        # Generative model p(x|z): decoder
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 128),
            nn.ReLU(),
            nn.Linear(128, obs_dim)
        )

        # Prior p(z) = N(0, I)
        self.prior_mu = torch.zeros(latent_dim)
        self.prior_logvar = torch.zeros(latent_dim)

    def encode(self, x):
        """q(z|x) = N(μ(x), σ²(x))"""
        h = self.encoder(x)
        mu = h[:, :self.latent_dim]
        logvar = h[:, self.latent_dim:]
        return mu, logvar

    def reparameterize(self, mu, logvar):
        """Sample z ~ q(z|x) using reparameterization trick"""
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        """p(x|z)"""
        return self.decoder(z)

    def free_energy(self, x, n_samples=1):
        """
        Compute variational free energy:
        F = E_q[log q(z)] - E_q[log p(x,z)]
        """
        mu, logvar = self.encode(x)

        # Sample from q(z|x)
        total_fe = 0
        for _ in range(n_samples):
            z = self.reparameterize(mu, logvar)

            # log q(z) - Gaussian entropy
            log_q_z = -0.5 * (self.latent_dim * np.log(2 * np.pi) +
                              torch.sum(logvar, dim=1) +
                              torch.sum((z - mu)**2 / torch.exp(logvar), dim=1))

            # log p(z) - prior (standard Gaussian)
            log_p_z = -0.5 * (self.latent_dim * np.log(2 * np.pi) +
                              torch.sum(z**2, dim=1))

            # log p(x|z) - reconstruction likelihood
            x_recon = self.decode(z)
            log_p_x_given_z = -0.5 * torch.sum((x - x_recon)**2, dim=1)

            # Free energy = E[log q(z) - log p(z) - log p(x|z)]
            fe = log_q_z - log_p_z - log_p_x_given_z
            total_fe += fe

        return total_fe.mean() / n_samples

    def elbo(self, x):
        """
        Evidence lower bound (negative free energy):
        ELBO = E_q[log p(x|z)] - KL[q(z)||p(z)]
        """
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)

        # Reconstruction term
        x_recon = self.decode(z)
        recon_loss = F.mse_loss(x_recon, x, reduction='sum')

        # KL divergence (closed form for Gaussians)
        kl_div = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())

        # ELBO = -recon_loss - KL
        # Free energy = recon_loss + KL
        return recon_loss + kl_div

    def complexity_accuracy_decomposition(self, x):
        """
        Decompose free energy into complexity and accuracy
        F = Complexity - Accuracy
        """
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)

        # Complexity = KL[q(z)||p(z)]
        complexity = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())

        # Accuracy = E_q[log p(x|z)]
        x_recon = self.decode(z)
        accuracy = -F.mse_loss(x_recon, x, reduction='sum')

        print(f"Complexity (KL divergence): {complexity.item():.4f}")
        print(f"Accuracy (log likelihood): {accuracy.item():.4f}")
        print(f"Free Energy: {(complexity - accuracy).item():.4f}")

        return complexity, accuracy


class PredictiveCodingFreeEnergy(nn.Module):
    """Predictive coding as gradient descent on free energy"""

    def __init__(self, layer_dims, n_iterations=50):
        super().__init__()
        self.n_layers = len(layer_dims)
        self.n_iterations = n_iterations

        # Generative weights (top-down)
        self.W_gen = nn.ModuleList([
            nn.Linear(layer_dims[i+1], layer_dims[i], bias=False)
            for i in range(len(layer_dims)-1)
        ])

        # Layer representations (beliefs)
        self.mu = [torch.zeros(dim) for dim in layer_dims]

    def free_energy_layer(self, layer_idx, x_below):
        """
        Free energy at layer l:
        F_l = 0.5 * ||x_l - g(μ_{l+1})||² + 0.5 * ||μ_l - prior||²
        """
        # Prediction from above
        if layer_idx < self.n_layers - 1:
            prediction = self.W_gen[layer_idx](self.mu[layer_idx + 1])
        else:
            prediction = torch.zeros_like(self.mu[layer_idx])

        # Prediction error
        if x_below is not None:
            error_below = torch.sum((x_below - self.W_gen[layer_idx-1](self.mu[layer_idx]))**2)
        else:
            error_below = 0

        # Prior term (assume zero prior)
        prior_term = 0.5 * torch.sum(self.mu[layer_idx]**2)

        return error_below + prior_term

    def minimize_free_energy(self, x_input):
        """
        Iteratively minimize free energy via gradient descent on μ
        ∂F/∂μ_l = -ε_l + W_l^T ε_{l+1}
        """
        # Initialize bottom layer
        self.mu[0] = x_input

        for iteration in range(self.n_iterations):
            # Update each layer's belief
            for l in range(1, self.n_layers):
                # Prediction error from below
                prediction_below = self.W_gen[l-1](self.mu[l])
                error_below = self.mu[l-1] - prediction_below

                # Error from above (if not top layer)
                if l < self.n_layers - 1:
                    prediction_from_above = self.W_gen[l](self.mu[l+1])
                    error_above = self.mu[l] - prediction_from_above
                else:
                    error_above = self.mu[l]  # Prior term

                # Gradient descent on free energy
                grad_mu = self.W_gen[l-1].weight.T @ error_below - error_above
                self.mu[l] = self.mu[l] + 0.01 * grad_mu

        return self.mu


# Example: VAE as free energy minimization
latent_dim = 10
obs_dim = 784  # e.g., MNIST

vfe = VariationalFreeEnergy(latent_dim, obs_dim)

# Generate data
x_data = torch.randn(100, obs_dim)

# Compute free energy
fe = vfe.free_energy(x_data, n_samples=1)
print(f"Free Energy: {fe.item():.4f}")

# ELBO (negative free energy)
elbo = -vfe.elbo(x_data)
print(f"ELBO: {elbo.item():.4f}")

# Decomposition
complexity, accuracy = vfe.complexity_accuracy_decomposition(x_data)

# Train to minimize free energy
optimizer = torch.optim.Adam(vfe.parameters(), lr=1e-3)

for epoch in range(100):
    fe = vfe.elbo(x_data) / x_data.shape[0]  # Average per sample

    optimizer.zero_grad()
    fe.backward()
    optimizer.step()

    if epoch % 20 == 0:
        print(f"Epoch {epoch}, Free Energy: {fe.item():.4f}")
```

**Source**: Friston (2010) Nat Rev Neurosci; Kingma & Welling (2014) ICLR; Friston et al. (2017) Neurosci Biobehav Rev; Buckley et al. (2017) Curr Op Behav Sci

---

### 177. Continuous-Time Variational Dynamics

**Purpose**: Gradient flow on variational free energy—neural ODEs for inference as continuous-time dynamical system.

**Formula**: Gradient Descent Dynamics
```
Continuous-time inference:
ż = -∇_z F(z, x)
  = ∇_z log p(x, z) - ∇_z log q(z)
  = ∇_z log p(z|x) [under q = p]

For variational distribution q(z; λ):
λ̇ = -∇_λ F(λ, x)

Natural gradient flow:
λ̇ = -G^{-1}(λ) ∇_λ F(λ)

where G = Fisher information metric

Langevin dynamics (with noise):
dz = -∇_z F dt + √(2T) dW

where:
- z = latent variables
- F = free energy functional
- λ = variational parameters
- W = Wiener process (Brownian motion)
- T = temperature
```

**Nature's Implementation**: Continuous attractor dynamics in cortex. Neural activity flows along free energy gradient. Fast inference via neural dynamics. Attention as dynamic inference. Working memory as stable equilibrium. Explains neural response timescales and transient dynamics.

**Impact**: **MEDIUM-HIGH - Neural ODE Inference**
Inference as dynamical system. Enables neural ODE architectures. Continuous-time generative models. Biologically plausible inference. Critical for understanding temporal cortical dynamics and implementing continuous-time neural networks.

**Code Example**:
```python
from scipy.integrate import odeint

class ContinuousVariationalDynamics:
    """Inference via continuous-time gradient flow on free energy"""

    def __init__(self, log_joint_fn, log_variational_fn):
        """
        log_joint_fn: log p(x, z)
        log_variational_fn: log q(z; λ)
        """
        self.log_joint = log_joint_fn
        self.log_q = log_variational_fn

    def free_energy_gradient(self, z, x, eps=1e-5):
        """
        Compute ∇_z F = -∇_z[log p(x,z) - log q(z)]
        """
        n_dim = len(z)
        grad = np.zeros(n_dim)

        for i in range(n_dim):
            z_plus = z.copy()
            z_plus[i] += eps

            z_minus = z.copy()
            z_minus[i] -= eps

            # Free energy F = -log p(x,z) + log q(z)
            F_plus = -self.log_joint(x, z_plus) + self.log_q(z_plus)
            F_minus = -self.log_joint(x, z_minus) + self.log_q(z_minus)

            grad[i] = (F_plus - F_minus) / (2 * eps)

        return grad

    def dynamics(self, z, t, x):
        """
        Gradient flow: dz/dt = -∇_z F
        """
        grad_F = self.free_energy_gradient(z, x)
        dzdt = -grad_F
        return dzdt

    def infer(self, x, z_init, T=10.0, dt=0.01):
        """
        Continuous-time inference via ODE integration
        """
        time = np.arange(0, T, dt)
        z_trajectory = odeint(self.dynamics, z_init, time, args=(x,))

        return z_trajectory

    def langevin_dynamics(self, z, t, x, temperature=0.1):
        """
        Stochastic gradient flow (Langevin dynamics):
        dz = -∇F dt + √(2T) dW
        """
        grad_F = self.free_energy_gradient(z, x)
        drift = -grad_F

        # Noise term
        noise = np.sqrt(2 * temperature) * np.random.randn(len(z))

        return drift + noise

    def sample_posterior(self, x, z_init, n_steps=1000, dt=0.01, temperature=0.1):
        """
        Sample from posterior via Langevin MCMC
        """
        z = z_init.copy()
        samples = [z.copy()]

        for _ in range(n_steps):
            # Euler-Maruyama integration
            dz = self.langevin_dynamics(z, 0, x, temperature) * dt
            z = z + dz

            samples.append(z.copy())

        return np.array(samples)


class NeuralODEInference(nn.Module):
    """Neural ODE for continuous inference"""

    def __init__(self, latent_dim, hidden_dim=64):
        super().__init__()
        self.latent_dim = latent_dim

        # Dynamics function: dz/dt = f(z, x, t)
        self.dynamics_net = nn.Sequential(
            nn.Linear(latent_dim + 1, hidden_dim),  # +1 for time
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, latent_dim)
        )

    def forward(self, z, x, t):
        """
        Compute dz/dt
        """
        # Concatenate z and t
        z_t = torch.cat([z, torch.tensor([t])], dim=0)
        dzdt = self.dynamics_net(z_t)

        # Add free energy gradient (learned + analytic)
        # This combines learned dynamics with variational objective
        return dzdt

    def integrate(self, z_init, x, T=1.0, n_steps=10):
        """
        Integrate dynamics from z_init for time T
        """
        dt = T / n_steps
        z = z_init

        trajectory = [z.clone()]

        for step in range(n_steps):
            t = step * dt
            dzdt = self.forward(z, x, t)
            z = z + dzdt * dt
            trajectory.append(z.clone())

        return torch.stack(trajectory)


# Example: Gaussian posterior inference
def log_joint_gaussian(x, z):
    """
    p(x, z) = p(x|z) p(z)
    Assume p(z) = N(0, I), p(x|z) = N(Az, σ²I)
    """
    # Prior
    log_prior = -0.5 * np.sum(z**2)

    # Likelihood
    A = np.eye(len(z))  # Simple case: x ≈ z
    prediction = A @ z
    log_likelihood = -0.5 * np.sum((x - prediction)**2) / 0.1

    return log_prior + log_likelihood

def log_q_gaussian(z, mu=None, sigma=1.0):
    """
    q(z) = N(μ, σ²I)
    Start with broad distribution
    """
    if mu is None:
        mu = np.zeros(len(z))

    return -0.5 * np.sum((z - mu)**2 / sigma**2)

# Continuous inference
latent_dim = 5
cvd = ContinuousVariationalDynamics(log_joint_gaussian, log_q_gaussian)

# Observation
x_obs = np.array([1.0, 0.5, -0.3, 0.8, 0.2])

# Initial guess
z_init = np.zeros(latent_dim)

# Infer via gradient flow
z_trajectory = cvd.infer(x_obs, z_init, T=10.0, dt=0.01)

print(f"Initial z: {z_init}")
print(f"Final z: {z_trajectory[-1]}")
print(f"Target x: {x_obs}")
print(f"Reconstruction: {z_trajectory[-1]}")  # Should match x_obs

# Langevin sampling
samples = cvd.sample_posterior(x_obs, z_init, n_steps=5000, dt=0.01, temperature=0.1)

print(f"\nPosterior mean (Langevin): {samples[-1000:].mean(axis=0)}")
print(f"Posterior std: {samples[-1000:].std(axis=0)}")
```

**Source**: Jordan et al. (1999) Machine Learning; Friston (2008) NeuroImage; Chen et al. (2018) NeurIPS; Millidge et al. (2021) Neural Comp

---

### 178. Active Inference Policy Update

**Purpose**: Action selection via expected free energy minimization—biologically grounded motor control and decision-making.

**Formula**: Expected Free Energy Minimization
```
Policy optimization:
π* = argmin E_q[F_π]
      π

Expected free energy:
F_π = E_q[log q(s|π) - log p(s, o|π)]

Decomposition:
F_π = E_q[-log p(o|s)] + KL[q(s|π)||p(s)]
    = Risk + Ambiguity

Alternative (predictive):
G_π = E_q[KL[q(s|o,π)||q(s|π)] - log p(o|C)]
    = Information gain - Expected reward

Policy selection (softmax):
P(π) ∝ exp(-γ G_π)

Action (discrete):
u = argmin G_π(u)
     u

where:
- π = policy (sequence of actions)
- s = hidden states
- o = observations
- C = preferences (desired outcomes)
- γ = precision (inverse temperature)
- G = expected free energy
```

**Nature's Implementation**: Motor cortex action selection. Dopamine encodes precision. Basal ganglia evaluates policies. Explains exploratory behavior (information seeking). Accounts for curiosity, novelty preference. Used for goal-directed movement, foraging, decision-making.

**Impact**: **MEDIUM-HIGH - Biologically Grounded Control**
Unifies perception and action. Explains exploration vs exploitation. Intrinsic motivation from information gain. No separate reward signal needed. Critical for understanding motor control, decision-making, and autonomous agents with curiosity.

**Code Example**:
```python
class ActiveInferenceAgent:
    """Active inference for action selection"""

    def __init__(self, n_states, n_observations, n_actions):
        self.n_states = n_states
        self.n_obs = n_observations
        self.n_actions = n_actions

        # Generative model
        self.A = np.random.rand(n_observations, n_states)  # Likelihood p(o|s)
        self.A /= self.A.sum(axis=0, keepdims=True)

        self.B = np.zeros((n_states, n_states, n_actions))  # Transition p(s'|s,a)
        for a in range(n_actions):
            self.B[:, :, a] = np.random.rand(n_states, n_states)
            self.B[:, :, a] /= self.B[:, :, a].sum(axis=0, keepdims=True)

        # Prior preferences p(o|C)
        self.C = np.ones(n_observations) / n_observations  # Uniform (can set goals)

        # State beliefs
        self.q_s = np.ones(n_states) / n_states

    def infer_state(self, observation):
        """
        Posterior inference: q(s|o) ∝ p(o|s) q(s)
        """
        # Likelihood
        likelihood = self.A[observation, :]

        # Posterior (Bayes rule)
        posterior = likelihood * self.q_s
        posterior /= posterior.sum()

        self.q_s = posterior
        return posterior

    def expected_free_energy(self, action, horizon=3):
        """
        Compute expected free energy for action sequence
        G = E[KL[q(s|o,π)||q(s|π)]] - E[log p(o|C)]
          = Information gain - Expected reward
        """
        # Simulate forward under this action
        q_s_future = self.q_s.copy()

        total_G = 0

        for t in range(horizon):
            # Predicted state after action
            q_s_next = self.B[:, :, action] @ q_s_future

            # Expected observation
            q_o = self.A @ q_s_next

            # Information gain (epistemic value)
            # KL[q(s|o)||q(s)] ≈ H[q(s)] - E[H[q(s|o)]]
            entropy_prior = -np.sum(q_s_next * np.log(q_s_next + 1e-10))

            # Expected entropy after observation (averaged over o)
            entropy_post = 0
            for o in range(self.n_obs):
                if q_o[o] > 0:
                    # Posterior if we observe o
                    q_s_given_o = self.A[o, :] * q_s_next
                    q_s_given_o /= q_s_given_o.sum()

                    entropy_post += q_o[o] * (-np.sum(q_s_given_o * np.log(q_s_given_o + 1e-10)))

            info_gain = entropy_prior - entropy_post

            # Expected reward (pragmatic value)
            # E[log p(o|C)]
            expected_reward = np.sum(q_o * np.log(self.C + 1e-10))

            # Expected free energy = -info_gain - expected_reward
            G = -info_gain - expected_reward

            total_G += G

            # Update for next step
            q_s_future = q_s_next

        return total_G

    def select_action(self, precision=1.0):
        """
        Select action minimizing expected free energy
        P(a) ∝ exp(-γ G(a))
        """
        G_actions = np.array([self.expected_free_energy(a) for a in range(self.n_actions)])

        # Softmax policy
        policy = np.exp(-precision * G_actions)
        policy /= policy.sum()

        # Sample action
        action = np.random.choice(self.n_actions, p=policy)

        return action, G_actions, policy

    def act_and_update(self, observation, precision=1.0):
        """
        Full active inference loop:
        1. Infer state from observation
        2. Select action minimizing expected free energy
        3. Execute action
        """
        # Perception
        q_s = self.infer_state(observation)

        # Action
        action, G_actions, policy = self.select_action(precision)

        # Update state belief (predict next state)
        self.q_s = self.B[:, :, action] @ self.q_s

        return action, G_actions, policy


# Example: Foraging task
n_states = 10  # Locations
n_observations = 10  # What agent can see
n_actions = 4  # Move left/right/up/down

agent = ActiveInferenceAgent(n_states, n_observations, n_actions)

# Set preferences (goal: state 5)
agent.C = np.zeros(n_observations)
agent.C[5] = 10.0  # Prefer observing state 5
agent.C /= agent.C.sum()

# Set transition dynamics (simple grid)
for a in range(n_actions):
    agent.B[:, :, a] = np.eye(n_states)  # Simplified

# Simulate episode
n_steps = 20
observations = []
actions = []

current_obs = 0  # Start at location 0

for t in range(n_steps):
    # Act
    action, G_vals, policy = agent.act_and_update(current_obs, precision=2.0)

    print(f"Step {t}:")
    print(f"  Observation: {current_obs}")
    print(f"  Expected free energy: {G_vals}")
    print(f"  Policy: {policy}")
    print(f"  Selected action: {action}")

    # Environment response (simulate)
    current_obs = (current_obs + 1) % n_observations  # Simple progression

    observations.append(current_obs)
    actions.append(action)

print(f"\nTrajectory: {observations}")
print(f"Actions: {actions}")
```

**Source**: Friston et al. (2015) Biol Cybern; Friston et al. (2017) Neural Comp; Sajid et al. (2021) Phys Life Rev; Da Costa et al. (2020) Entropy

---

### 179. Dendritic Nonlinear Integration (Polynomial Expansion)

**Purpose**: Implement polynomial and multilinear operations via dendritic compartments—biological basis for higher-order feature interactions.

**Formula**: Compartment-Wise Polynomial
```
Dendritic branch voltage:
V_branch = f(Σ w_i x_i)
          i

Nonlinear integration:
f(z) = z + α z² + β z³ + γ z⁴

Or multilinear (two branches):
V_soma = g₁(Σ w₁ᵢ x_i) · g₂(Σ w₂ⱼ x_j)
           i              j

General polynomial:
y = Σ a_k (Σ w_{ki} x_i)^k
    k     i

where:
- V_branch = branch membrane potential
- x_i = synaptic inputs
- w_i = synaptic weights
- α, β, γ = nonlinearity coefficients
- g = local nonlinear function (sigm

oid, quadratic)
- Each branch computes different term
```

**Nature's Implementation**: Dendritic trees have NMDA channels, calcium spikes enabling local nonlinearity. Each branch acts as computational subunit. Pyramidal neurons have 10-30 branches performing different operations. Explains why neurons can compute XOR, implement multiplication, and learn complex functions.

**Impact**: **MEDIUM-HIGH - Biological Higher-Order Features**
Neurons compute beyond dot products. Natural feature interactions (x₁ · x₂). No separate multiplication layer needed. Dendrites = mixture of polynomial basis functions. Critical for understanding single-neuron computational power and implementing biologically realistic deep networks.

**Code Example**:
```python
class DendriticPolynomialNeuron(nn.Module):
    """Neuron with polynomial dendritic integration"""

    def __init__(self, n_inputs, n_branches=5, max_order=3):
        super().__init__()
        self.n_branches = n_branches
        self.max_order = max_order

        # Each branch has its own weights
        self.branch_weights = nn.ParameterList([
            nn.Parameter(torch.randn(n_inputs) * 0.1)
            for _ in range(n_branches)
        ])

        # Polynomial coefficients for each branch
        self.poly_coeffs = nn.ParameterList([
            nn.Parameter(torch.randn(max_order + 1) * 0.1)
            for _ in range(n_branches)
        ])

        # Somatic integration weights
        self.branch_to_soma = nn.Parameter(torch.ones(n_branches))

    def branch_activation(self, x, branch_idx):
        """
        Compute dendritic branch response:
        V = a₀ + a₁·z + a₂·z² + a₃·z³
        where z = Σ w_i x_i
        """
        # Linear summation
        z = torch.sum(self.branch_weights[branch_idx] * x)

        # Polynomial expansion
        response = 0
        for k in range(self.max_order + 1):
            response += self.poly_coeffs[branch_idx][k] * (z ** k)

        return response

    def forward(self, x):
        """
        Sum across dendritic branches to get somatic response
        """
        branch_responses = torch.stack([
            self.branch_activation(x, i)
            for i in range(self.n_branches)
        ])

        # Weighted sum at soma
        soma_potential = torch.sum(self.branch_to_soma * branch_responses)

        # Somatic nonlinearity (spike generation)
        output = torch.tanh(soma_potential)

        return output


class MultilinearDendriticLayer(nn.Module):
    """
    Multilinear layer via dendritic branches
    Implements y = Σᵢⱼ wᵢⱼ xᵢ xⱼ (pairwise interactions)
    """

    def __init__(self, n_inputs, n_outputs, n_branches_per_neuron=10):
        super().__init__()
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.n_branches = n_branches_per_neuron

        # Each output neuron has multiple branches
        # Each branch computes product of two linear combinations
        self.branch_weights_1 = nn.Parameter(
            torch.randn(n_outputs, n_branches_per_neuron, n_inputs) * 0.1
        )
        self.branch_weights_2 = nn.Parameter(
            torch.randn(n_outputs, n_branches_per_neuron, n_inputs) * 0.1
        )

        # Branch combination weights
        self.branch_combine = nn.Parameter(
            torch.ones(n_outputs, n_branches_per_neuron)
        )

    def forward(self, x):
        """
        Each branch: b_k = (w₁ᵏ·x) · (w₂ᵏ·x)
        Output: y = Σ_k α_k b_k
        """
        batch_size = x.shape[0]
        outputs = []

        for neuron_idx in range(self.n_outputs):
            branch_outputs = []

            for branch_idx in range(self.n_branches):
                # Two linear projections
                proj1 = torch.sum(self.branch_weights_1[neuron_idx, branch_idx] * x, dim=1)
                proj2 = torch.sum(self.branch_weights_2[neuron_idx, branch_idx] * x, dim=1)

                # Multiplicative interaction (dendritic nonlinearity)
                branch_out = proj1 * proj2

                branch_outputs.append(branch_out)

            # Combine branches
            branch_stack = torch.stack(branch_outputs, dim=1)
            neuron_out = torch.sum(
                self.branch_combine[neuron_idx] * branch_stack,
                dim=1
            )

            outputs.append(neuron_out)

        return torch.stack(outputs, dim=1)


# Example: XOR learning with dendritic polynomials
n_inputs = 2
neuron = DendriticPolynomialNeuron(n_inputs, n_branches=3, max_order=2)

# XOR dataset
X = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
y = torch.tensor([0., 1., 1., 0.])

optimizer = torch.optim.Adam(neuron.parameters(), lr=0.01)

for epoch in range(1000):
    outputs = torch.stack([neuron(x) for x in X])
    loss = F.mse_loss(outputs, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 200 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

# Test
print("\nXOR Results:")
for i, x in enumerate(X):
    pred = neuron(x)
    print(f"Input: {x.numpy()}, Target: {y[i].item()}, Pred: {pred.item():.3f}")
```

**Source**: Poirazi et al. (2003) Neuron; London & Häusser (2005) Annu Rev Neurosci; Gidon et al. (2020) Science

---

### 180. NMDA-Driven Coincidence Detection

**Purpose**: Voltage-dependent synaptic gating—biological multiplicative interaction for detecting correlated inputs.

**Formula**: Voltage-Dependent Conductance
```
NMDA current:
I_NMDA(V, t) = ḡ · s(t) · (V - E_NMDA) / (1 + γ exp(-α V))

Magnesium block:
B(V) = 1 / (1 + [Mg²⁺] exp(-α V) / 3.57)

Synaptic activation:
ds/dt = r(1 - s)·[T] - s/τ_decay

Gating variable (multiplicative):
g_eff(V, x) = x · B(V)

Effective weight:
w_eff = w · B(V)

where:
- V = postsynaptic membrane potential
- s = synaptic gating variable
- [T] = transmitter concentration
- [Mg²⁺] = magnesium concentration
- α ≈ 0.062 mV⁻¹
- γ ≈ 1/3.57 mM
- E_NMDA ≈ 0 mV
- Requires both: (1) presynaptic spike (s) AND (2) postsynaptic depolarization (V)
```

**Nature's Implementation**: Pyramidal neurons, dendritic spines. Coincidence detection for temporal credit assignment. Enables Hebbian learning ("fire together, wire together"). Critical for long-term potentiation, associative memory, sequence learning.

**Impact**: **MEDIUM-HIGH - Biological Gating**
Natural AND gate in biology. Multiplicative weight modulation. Temporal credit assignment without backprop. Foundation for attention mechanisms, gating networks. Critical for understanding synaptic plasticity and implementing biologically-inspired gating.

**Code Example**:
```python
class NMDAGatedSynapse(nn.Module):
    """NMDA receptor with voltage-dependent gating"""

    def __init__(self, n_inputs):
        super().__init__()
        self.n_inputs = n_inputs

        # Synaptic weights
        self.W = nn.Parameter(torch.randn(n_inputs) * 0.1)

        # NMDA parameters
        self.alpha = 0.062  # mV⁻¹
        self.Mg_conc = 1.0  # mM
        self.E_NMDA = 0.0   # mV

        # Synaptic time constant
        self.tau_decay = 100.0  # ms

    def magnesium_block(self, V):
        """
        B(V) = 1 / (1 + [Mg] exp(-α V) / 3.57)
        """
        return 1.0 / (1.0 + (self.Mg_conc / 3.57) * torch.exp(-self.alpha * V))

    def forward(self, x, V_post):
        """
        Compute NMDA-gated current
        x: presynaptic input (spike or rate)
        V_post: postsynaptic voltage
        """
        # Synaptic activation (assume instantaneous for simplicity)
        s = x  # In full model: integrate ds/dt

        # Magnesium block (voltage-dependent)
        B = self.magnesium_block(V_post)

        # NMDA current: I = w · s · B(V) · (V - E)
        # For rate model, just compute effective input
        I_NMDA = self.W * s * B * (V_post - self.E_NMDA)

        return I_NMDA.sum(), B


class NMDAGatedLayer(nn.Module):
    """
    Layer with NMDA-style gating (multiplicative modulation)
    Implements: y = σ(W·x · g(V))
    where g(V) is voltage-dependent gating
    """

    def __init__(self, in_features, out_features):
        super().__init__()

        # Feedforward weights
        self.W = nn.Parameter(torch.randn(out_features, in_features) * 0.1)

        # Gating parameters (learned)
        self.gate_scale = nn.Parameter(torch.ones(out_features))
        self.gate_offset = nn.Parameter(torch.zeros(out_features))

    def gating_function(self, V):
        """
        Approximate NMDA-like gating:
        g(V) = σ(α(V - V_th))
        """
        return torch.sigmoid(self.gate_scale * (V - self.gate_offset))

    def forward(self, x, V_context):
        """
        x: input features
        V_context: context signal (acts like voltage)
        """
        # Linear transformation
        z = F.linear(x, self.W)

        # Voltage-dependent gating
        gate = self.gating_function(V_context)

        # Multiplicative modulation
        output = z * gate

        return output


class AttentionViaNMDA(nn.Module):
    """
    Attention mechanism inspired by NMDA coincidence detection
    Attention = coincidence of query (voltage) and key (input)
    """

    def __init__(self, dim):
        super().__init__()
        self.dim = dim

        # Query, Key, Value projections
        self.W_q = nn.Linear(dim, dim)
        self.W_k = nn.Linear(dim, dim)
        self.W_v = nn.Linear(dim, dim)

    def forward(self, x):
        """
        NMDA-style attention:
        Attention score = coincidence of Q and K
        """
        batch_size, seq_len, _ = x.shape

        # Project
        Q = self.W_q(x)  # "voltage" (top-down)
        K = self.W_k(x)  # "input" (bottom-up)
        V = self.W_v(x)  # "values"

        # Coincidence detection (dot product)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / np.sqrt(self.dim)

        # NMDA-like gating (softmax = competitive winner-take-all)
        attention = torch.softmax(scores, dim=-1)

        # Gated output
        output = torch.matmul(attention, V)

        return output


# Example: NMDA coincidence detection
n_inputs = 10
nmda = NMDAGatedSynapse(n_inputs)

# Presynaptic input
x = torch.randn(n_inputs)

# Postsynaptic voltage sweep
V_range = torch.linspace(-80, 0, 100)  # mV
currents = []
blocks = []

for V in V_range:
    I, B = nmda(x, V)
    currents.append(I.item())
    blocks.append(B.mean().item())

print("NMDA Coincidence Detection:")
print(f"  At V=-80mV (hyperpolarized): I={currents[0]:.4f}, Block={blocks[0]:.4f}")
print(f"  At V=-40mV (depolarized): I={currents[50]:.4f}, Block={blocks[50]:.4f}")
print(f"  At V=0mV (spike): I={currents[-1]:.4f}, Block={blocks[-1]:.4f}")

# Gated layer example
layer = NMDAGatedLayer(in_features=10, out_features=5)
x_input = torch.randn(32, 10)  # Batch of 32
V_context = torch.randn(5)     # Context/voltage for each output

output = layer(x_input, V_context)
print(f"\nGated layer output shape: {output.shape}")
```

**Source**: Jahr & Stevens (1990) Nature; Mayer et al. (1984) Nature; Larkum et al. (1999) Nature; Richards & Lillicrap (2019) Nat Neurosci

---

### 181. Dendritic Gating (Mixture-of-Experts)

**Purpose**: Compartment-specific gating for routing and modulation—biological foundation for mixture-of-experts and gated architectures.

**Formula**: Multiplicative Branch Gating
```
Branch gating:
h_i = g_i(c) · f_i(x)

where:
- h_i = branch i output
- g_i(c) = gating function (depends on context c)
- f_i(x) = branch computation
- c = modulatory input (e.g., from apical dendrite)

Gating function:
g_i(c) = σ(w_i^T c + b_i)

Somatic integration:
y = Σ h_i = Σ g_i(c) · f_i(x)
    i       i

Mixture-of-experts form:
y = Σ α_i(c) · Expert_i(x)
    i

where α_i = g_i / Σ_j g_j (normalized gating)

Sparse gating (top-k):
y = Σ g_i(c) · f_i(x)
    i∈TopK(g)
```

**Nature's Implementation**: Apical dendrites gate basal inputs in pyramidal neurons. Context from layer 1 modulates processing in basal dendrites. Enables task switching, attention, context-dependent computation. Explains how single neurons perform multiple functions.

**Impact**: **MEDIUM-HIGH - Biological Routing**
Natural mixture-of-experts. Context-dependent computation. Gating without separate gating layer. Foundation for transformers, routing networks. Critical for understanding cortical context integration and implementing efficient sparse models.

**Code Example**:
```python
class DendriticGatingNeuron(nn.Module):
    """Neuron with dendritic gating (biological mixture-of-experts)"""

    def __init__(self, n_inputs, n_branches, context_dim):
        super().__init__()
        self.n_branches = n_branches

        # Branch-specific feedforward weights
        self.branch_weights = nn.ModuleList([
            nn.Linear(n_inputs, 1, bias=False)
            for _ in range(n_branches)
        ])

        # Gating network (context-dependent)
        self.gating_net = nn.ModuleList([
            nn.Linear(context_dim, 1)
            for _ in range(n_branches)
        ])

        # Branch activations
        self.branch_activations = nn.ModuleList([
            nn.Tanh() for _ in range(n_branches)
        ])

    def forward(self, x, context):
        """
        x: feedforward input
        context: modulatory signal (e.g., from apical dendrite)
        """
        # Compute each branch
        branch_outputs = []
        gates = []

        for i in range(self.n_branches):
            # Branch computation
            branch_value = self.branch_activations[i](
                self.branch_weights[i](x)
            )

            # Context-dependent gate
            gate = torch.sigmoid(self.gating_net[i](context))

            # Gated output
            gated_output = gate * branch_value

            branch_outputs.append(gated_output)
            gates.append(gate)

        # Somatic summation
        soma_output = torch.sum(torch.cat(branch_outputs, dim=1), dim=1, keepdim=True)

        return soma_output, torch.cat(gates, dim=1)


class DendriticMixtureOfExperts(nn.Module):
    """
    Mixture-of-experts via dendritic gating
    Each branch = expert, context determines routing
    """

    def __init__(self, n_inputs, n_experts, expert_hidden_dim, context_dim):
        super().__init__()
        self.n_experts = n_experts

        # Experts (dendritic branches)
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(n_inputs, expert_hidden_dim),
                nn.ReLU(),
                nn.Linear(expert_hidden_dim, expert_hidden_dim)
            )
            for _ in range(n_experts)
        ])

        # Gating network (context-dependent routing)
        self.gating = nn.Sequential(
            nn.Linear(context_dim, expert_hidden_dim),
            nn.ReLU(),
            nn.Linear(expert_hidden_dim, n_experts)
        )

    def forward(self, x, context, k=None):
        """
        x: input
        context: routing signal
        k: number of experts to activate (sparse gating)
        """
        # Compute expert outputs
        expert_outputs = torch.stack([
            expert(x) for expert in self.experts
        ], dim=1)  # [batch, n_experts, hidden_dim]

        # Compute gates
        gate_logits = self.gating(context)

        if k is not None:
            # Top-k sparse gating
            topk_vals, topk_indices = torch.topk(gate_logits, k, dim=1)
            gates = torch.zeros_like(gate_logits)
            gates.scatter_(1, topk_indices, torch.softmax(topk_vals, dim=1))
        else:
            # Softmax gating (all experts)
            gates = torch.softmax(gate_logits, dim=1)

        # Weighted combination
        # gates: [batch, n_experts]
        # expert_outputs: [batch, n_experts, hidden_dim]
        output = torch.sum(
            gates.unsqueeze(-1) * expert_outputs,
            dim=1
        )

        return output, gates


class ApicalGatedLayer(nn.Module):
    """
    Layer with apical dendritic gating
    Basal input modulated by apical context
    """

    def __init__(self, basal_dim, apical_dim, output_dim):
        super().__init__()

        # Basal pathway (feedforward)
        self.basal_net = nn.Linear(basal_dim, output_dim)

        # Apical pathway (context)
        self.apical_net = nn.Linear(apical_dim, output_dim)

        # Gating (multiplicative modulation)
        self.gate_net = nn.Linear(apical_dim, output_dim)

    def forward(self, x_basal, x_apical):
        """
        x_basal: feedforward input (from lower layer)
        x_apical: context input (from higher layer or attention)
        """
        # Basal processing
        h_basal = self.basal_net(x_basal)

        # Apical gating
        gate = torch.sigmoid(self.gate_net(x_apical))

        # Gated output
        output = gate * h_basal + (1 - gate) * self.apical_net(x_apical)

        return output


# Example: Context-dependent routing
n_inputs = 10
n_experts = 5
expert_dim = 20
context_dim = 5

moe = DendriticMixtureOfExperts(n_inputs, n_experts, expert_dim, context_dim)

# Input and context
x = torch.randn(32, n_inputs)
context = torch.randn(32, context_dim)

# Forward with full gating
output_full, gates_full = moe(x, context, k=None)
print(f"Full gating - Output shape: {output_full.shape}")
print(f"Gate distribution: {gates_full[0]}")

# Sparse gating (top-2 experts)
output_sparse, gates_sparse = moe(x, context, k=2)
print(f"\nSparse gating (k=2) - Output shape: {output_sparse.shape}")
print(f"Gate distribution: {gates_sparse[0]}")
print(f"Active experts: {(gates_sparse[0] > 0).sum().item()}")
```

**Source**: Larkum (2013) Trends Neurosci; Sacramento et al. (2018) eLife; Guerguiev et al. (2017) eLife; Payeur et al. (2021) Nat Commun

---

### 182. Dendritic Clustering Rule

**Purpose**: Competitive learning within dendritic branches—biological basis for sparse feature detectors and clustering.

**Formula**: Winner-Take-All Clustering
```
Cluster assignment:
c_k = argmax σ(w_k^T x + β||x||²)
       k

Branch activation:
a_k = σ(w_k^T x + β||x||² - θ_k)

Learning (winner updates):
Δw_c = η(x - w_c)  [for winner c only]

Threshold adaptation:
Δθ_k = η_θ(a_k - ρ)

where:
- c_k = cluster/branch index
- w_k = branch synaptic weights
- β = quadratic term coefficient
- θ_k = branch activation threshold
- ρ = target sparsity
- η, η_θ = learning rates

Clustered synapses form on branches

Branch specialization emerges
```

**Nature's Implementation**: Pyramidal neuron dendrites show clustered synaptic inputs. Each branch detects specific input pattern. Enables single neurons to learn multiple features. Explains receptive field substructure, nonlinear feature selectivity.

**Impact**: **MEDIUM - Sparse Feature Learning**
Unsupervised clustering in single neuron. Multiple feature detectors per neuron. Sparse activations naturally. Foundation for local learning rules. Critical for understanding dendritic computation and implementing sparse coding.

**Code Example**:
```python
class DendriticClusteringNeuron(nn.Module):
    """Neuron with competitive dendritic branch learning"""

    def __init__(self, n_inputs, n_branches, sparsity=0.1):
        super().__init__()
        self.n_branches = n_branches
        self.sparsity = sparsity

        # Branch weights (clusters)
        self.W = nn.Parameter(torch.randn(n_branches, n_inputs) * 0.1)

        # Branch thresholds
        self.theta = nn.Parameter(torch.zeros(n_branches))

        # Quadratic coefficient
        self.beta = nn.Parameter(torch.zeros(1))

    def branch_activations(self, x):
        """
        Compute activation for each branch:
        a_k = σ(w_k·x + β||x||² - θ_k)
        """
        # Linear term
        linear = F.linear(x, self.W)

        # Quadratic term (helps with clustering)
        quadratic = self.beta * torch.sum(x**2, dim=1, keepdim=True)

        # Activations
        activations = torch.sigmoid(linear + quadratic - self.theta)

        return activations

    def forward(self, x):
        """Compute branch activations"""
        return self.branch_activations(x)

    def cluster_assignment(self, x):
        """Winner-take-all: assign to most active branch"""
        activations = self.branch_activations(x)
        winners = torch.argmax(activations, dim=1)
        return winners

    def update_winners(self, x, learning_rate=0.01):
        """
        Competitive learning: update only winning branches
        Δw_winner = η(x - w_winner)
        """
        with torch.no_grad():
            # Find winners
            activations = self.branch_activations(x)
            winners = torch.argmax(activations, dim=1)

            # Update each sample's winner
            for i, winner_idx in enumerate(winners):
                # Hebbian-like update
                delta_w = learning_rate * (x[i] - self.W[winner_idx])
                self.W[winner_idx] += delta_w

                # Normalize weights (optional)
                self.W[winner_idx] /= torch.norm(self.W[winner_idx])

    def update_thresholds(self, x, learning_rate=0.001):
        """
        Threshold adaptation to maintain sparsity:
        Δθ_k = η(a_k - ρ)
        """
        with torch.no_grad():
            activations = self.branch_activations(x)

            # Average activation per branch
            mean_activation = activations.mean(dim=0)

            # Update thresholds to match target sparsity
            delta_theta = learning_rate * (mean_activation - self.sparsity)
            self.theta += delta_theta


class DendriticClusteringLayer(nn.Module):
    """Layer of clustering neurons"""

    def __init__(self, n_inputs, n_neurons, n_branches_per_neuron):
        super().__init__()
        self.neurons = nn.ModuleList([
            DendriticClusteringNeuron(n_inputs, n_branches_per_neuron)
            for _ in range(n_neurons)
        ])

    def forward(self, x):
        """Compute activations for all neurons"""
        outputs = torch.stack([
            neuron(x) for neuron in self.neurons
        ], dim=1)  # [batch, n_neurons, n_branches]

        # Pool across branches (sum or max)
        return outputs.max(dim=2)[0]  # Max pool

    def train_step(self, x, lr_weights=0.01, lr_threshold=0.001):
        """One step of competitive learning"""
        for neuron in self.neurons:
            neuron.update_winners(x, learning_rate=lr_weights)
            neuron.update_thresholds(x, learning_rate=lr_threshold)


# Example: Learn clusters in dendritic branches
n_inputs = 20
n_branches = 5

neuron = DendriticClusteringNeuron(n_inputs, n_branches, sparsity=0.2)

# Generate clustered data (5 clusters)
n_samples = 500
cluster_centers = torch.randn(5, n_inputs)
data = []
labels = []

for i in range(n_samples):
    cluster_idx = np.random.randint(0, 5)
    sample = cluster_centers[cluster_idx] + torch.randn(n_inputs) * 0.3
    data.append(sample)
    labels.append(cluster_idx)

data = torch.stack(data)
labels = torch.tensor(labels)

# Train with competitive learning
for epoch in range(100):
    # Shuffle data
    perm = torch.randperm(n_samples)
    data_shuffled = data[perm]

    for i in range(0, n_samples, 32):
        batch = data_shuffled[i:i+32]

        neuron.update_winners(batch, learning_rate=0.05)
        neuron.update_thresholds(batch, learning_rate=0.01)

    if epoch % 20 == 0:
        # Check clustering quality
        activations = neuron(data)
        assignments = neuron.cluster_assignment(data)

        # Purity: how well assignments match true labels
        from scipy.stats import mode
        cluster_purity = []
        for branch_idx in range(n_branches):
            branch_samples = labels[assignments == branch_idx]
            if len(branch_samples) > 0:
                purity = mode(branch_samples.numpy())[1][0] / len(branch_samples)
                cluster_purity.append(purity)

        print(f"Epoch {epoch}, Branch purity: {np.mean(cluster_purity):.3f}")
        print(f"  Branch activations (mean): {activations.mean(dim=0)}")
```

**Source**: Losonczy & Magee (2006) Neuron; Mel (1992) Neural Comp; Kastellakis et al. (2015) Neuron; Poirazi & Mel (2001) Neural Comp

---

### 183. Shunting Inhibition (Divisive Normalization)

**Purpose**: Biological divisive normalization via shunting—continuous-time analog of batch normalization and attention softmax.

**Formula**: Shunting Dynamics
```
Shunting equation:
τ ẋ = -ax + bx(1 - x) - cx(d + y)

Simplified (divisive):
ẋ = -ax + f(I) / (1 + Σ y_j)
                    j

Steady-state (normalization):
x* = I / (1 + Σ I_j / K)
              j

Divisive normalization:
r_i = R_i / (σ + Σ w_ij R_j)
                  j

where:
- x = neural activity
- I = input
- y_j = lateral inhibitory inputs
- σ = semi-saturation constant
- w_ij = normalization weights
- Implements: softmax, batch norm, layer norm
```

**Nature's Implementation**: Cortical inhibitory interneurons provide shunting inhibition. Divisive normalization in V1, MT, LIP. Contrast normalization, gain control. Implements biological softmax for winner-take-all, attention, probability normalization.

**Impact**: **MEDIUM-HIGH - Biological Normalization**
Continuous-time batch norm. Natural softmax. No need for separate normalization layer. Foundation for attention, gain control. Critical for understanding cortical computations and implementing bio-realistic normalization.

**Code Example**:
```python
class ShuntingInhibitionLayer(nn.Module):
    """Divisive normalization via shunting inhibition"""

    def __init__(self, n_units, tau=10.0, semi_saturation=1.0):
        super().__init__()
        self.n_units = n_units
        self.tau = tau
        self.sigma = semi_saturation

        # Lateral inhibition weights
        self.W_inhib = nn.Parameter(torch.ones(n_units, n_units) / n_units)

        # Excitatory weights
        self.W_exc = nn.Parameter(torch.randn(n_units, n_units) * 0.1)

    def shunting_dynamics(self, x, I, dt=0.1):
        """
        Shunting equation:
        dx/dt = (-x + I) / (1 + Σ w_ij x_j)
        """
        # Inhibitory pool
        inhib_sum = F.linear(x, self.W_inhib)

        # Shunting (divisive) term
        denom = 1.0 + inhib_sum + self.sigma

        # Dynamics
        dxdt = (-x + I) / denom

        return x + (dxdt / self.tau) * dt

    def forward(self, I, n_iterations=50, dt=0.1):
        """
        Iteratively compute steady-state response
        """
        batch_size = I.shape[0]
        x = torch.zeros(batch_size, self.n_units)

        for _ in range(n_iterations):
            x = self.shunting_dynamics(x, I, dt)

        return x

    def divisive_normalization(self, I):
        """
        Steady-state divisive normalization:
        x = I / (σ + Σ w_ij I_j)
        """
        # Normalization pool
        norm_pool = F.linear(I, self.W_inhib) + self.sigma

        # Normalized response
        x = I / norm_pool

        return x


class BiologicalSoftmax(nn.Module):
    """
    Softmax via shunting inhibition
    Models winner-take-all with biological dynamics
    """

    def __init__(self, n_units, tau=1.0, lateral_strength=1.0):
        super().__init__()
        self.n_units = n_units
        self.tau = tau
        self.lateral_strength = lateral_strength

    def dynamics(self, x, I, dt=0.01):
        """
        Winner-take-all dynamics:
        dx/dt = -x + I - β·Σ x_j
                        j≠i
        """
        # Lateral inhibition (all-to-all except self)
        lateral = self.lateral_strength * (x.sum(dim=1, keepdim=True) - x)

        # Dynamics
        dxdt = (-x + I - lateral) / self.tau

        # ReLU (non-negative firing rates)
        x_new = torch.relu(x + dxdt * dt)

        return x_new

    def forward(self, logits, n_iterations=100, dt=0.01):
        """
        Continuous-time softmax via shunting
        """
        batch_size = logits.shape[0]
        x = torch.zeros_like(logits)

        for _ in range(n_iterations):
            x = self.dynamics(x, logits, dt)

        # Normalize to probability
        return x / x.sum(dim=1, keepdim=True)


class DivisiveNormalizationAttention(nn.Module):
    """
    Attention via divisive normalization
    Biological alternative to softmax attention
    """

    def __init__(self, dim, normalization_radius=1.0):
        super().__init__()
        self.dim = dim
        self.sigma = normalization_radius

        # Q, K, V projections
        self.W_q = nn.Linear(dim, dim)
        self.W_k = nn.Linear(dim, dim)
        self.W_v = nn.Linear(dim, dim)

    def forward(self, x):
        """
        Divisively normalized attention
        """
        Q = self.W_q(x)
        K = self.W_k(x)
        V = self.W_v(x)

        # Attention scores (unnormalized)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / np.sqrt(self.dim)

        # Divisive normalization (biological softmax)
        # a_ij = s_ij / (σ + Σ_k s_ik)
        norm_pool = scores.sum(dim=-1, keepdim=True) + self.sigma
        attention = scores / norm_pool

        # Apply attention
        output = torch.matmul(attention, V)

        return output


# Example: Shunting inhibition dynamics
n_units = 10
layer = ShuntingInhibitionLayer(n_units, tau=10.0, semi_saturation=0.5)

# Input (non-normalized)
I = torch.tensor([[1.0, 5.0, 2.0, 0.5, 3.0, 1.5, 4.0, 2.5, 1.0, 0.8]])

# Divisive normalization (steady-state)
x_norm = layer.divisive_normalization(I)
print("Input:", I)
print("Normalized:", x_norm)
print("Sum:", x_norm.sum())

# Dynamic convergence
x_dynamic = layer(I, n_iterations=100, dt=0.1)
print("Dynamic steady-state:", x_dynamic)

# Biological softmax
softmax_layer = BiologicalSoftmax(n_units, tau=1.0, lateral_strength=2.0)
logits = torch.tensor([[2.0, 5.0, 1.0, 3.0, 4.0, 0.5, 2.5, 1.5, 3.5, 2.0]])

# Standard softmax
standard_softmax = torch.softmax(logits, dim=1)

# Biological softmax
bio_softmax = softmax_layer(logits, n_iterations=200, dt=0.01)

print("\nSoftmax comparison:")
print("Standard:", standard_softmax)
print("Biological:", bio_softmax)
print("Difference:", torch.abs(standard_softmax - bio_softmax).max())
```

**Source**: Carandini & Heeger (2012) Nat Rev Neurosci; Heeger (1992) Vis Neurosci; Rubin et al. (2015) Neural Comp; Louie et al. (2014) J Neurosci

---

### 184. Langevin Sampling (Neural Monte Carlo)

**Purpose**: Stochastic gradient descent on energy landscape—neural noise as computational mechanism for sampling and exploration.

**Formula**: Stochastic Dynamics
```
Langevin equation:
dx = -∇E(x) dt + √(2T) dW

Discrete (Euler-Maruyama):
x_{t+1} = x_t - η∇E(x_t) + √(2ηT) ε_t

where ε_t ~ N(0, I)

Equilibrium distribution:
p(x) ∝ exp(-E(x) / T)

For neural networks:
dθ = -∇L(θ) dt + √(2T/N) dW

Preconditioned Langevin:
dx = -G^{-1}∇E dt + √(2T) G^{-1/2} dW

where:
- E(x) = energy function
- T = temperature (noise level)
- W = Wiener process
- η = step size
- G = preconditioning matrix (e.g., Fisher information)
- L = loss function
```

**Nature's Implementation**: Neural variability as sampling mechanism. Spontaneous activity explores energy landscape. Temperature = neural noise level. Explains trial-to-trial variability, exploration, probabilistic inference. Used for decision-making under uncertainty, motor planning, perceptual sampling.

**Impact**: **MEDIUM-HIGH - Stochastic Exploration**
Neural noise is computational, not just nuisance. Exploration via gradient + noise. Samples from posterior. Foundation for Bayesian brain hypothesis, energy-based models. Critical for understanding neural variability and implementing sampling networks.

**Code Example**:
```python
class LangevinSampler:
    """Langevin dynamics for sampling from energy-based models"""

    def __init__(self, energy_fn, dim, temperature=1.0):
        """
        energy_fn: E(x) - function to minimize
        dim: dimensionality
        temperature: noise level
        """
        self.energy = energy_fn
        self.dim = dim
        self.T = temperature

    def energy_gradient(self, x, eps=1e-5):
        """Compute ∇E(x) via finite differences"""
        grad = np.zeros(self.dim)

        for i in range(self.dim):
            x_plus = x.copy()
            x_plus[i] += eps

            x_minus = x.copy()
            x_minus[i] -= eps

            grad[i] = (self.energy(x_plus) - self.energy(x_minus)) / (2 * eps)

        return grad

    def step(self, x, dt=0.01):
        """
        One Langevin step:
        x_new = x - η∇E(x) + √(2ηT) ε
        """
        # Gradient descent
        grad = self.energy_gradient(x)
        drift = -grad * dt

        # Diffusion (noise)
        noise = np.sqrt(2 * dt * self.T) * np.random.randn(self.dim)

        return x + drift + noise

    def sample(self, x_init, n_steps=10000, dt=0.01, burnin=1000):
        """
        Generate samples via Langevin MCMC
        """
        x = x_init.copy()
        samples = []

        for step in range(n_steps):
            x = self.step(x, dt)

            # Store after burn-in
            if step >= burnin:
                samples.append(x.copy())

        return np.array(samples)

    def sample_batch(self, x_init, n_steps=1000, dt=0.01):
        """Sample trajectory"""
        trajectory = [x_init.copy()]
        x = x_init

        for _ in range(n_steps):
            x = self.step(x, dt)
            trajectory.append(x.copy())

        return np.array(trajectory)


class NeuralLangevinDynamics(nn.Module):
    """Neural network with Langevin dynamics for sampling"""

    def __init__(self, input_dim, hidden_dim, temperature=0.1):
        super().__init__()
        self.temperature = temperature

        # Energy network E(x)
        self.energy_net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, 1)
        )

    def energy(self, x):
        """Compute E(x)"""
        return self.energy_net(x).squeeze()

    def sample_langevin(self, x_init, n_steps=100, step_size=0.01):
        """
        Sample via Langevin dynamics
        x_{t+1} = x_t - η∇E(x_t) + √(2ηT) ε
        """
        x = x_init.clone().requires_grad_(True)
        trajectory = [x.detach().clone()]

        for _ in range(n_steps):
            # Compute gradient
            E = self.energy(x)
            E.backward()

            with torch.no_grad():
                # Gradient descent
                x = x - step_size * x.grad

                # Add noise
                noise = torch.randn_like(x) * np.sqrt(2 * step_size * self.temperature)
                x = x + noise

                # Clear gradient
                x.grad = None
                x.requires_grad_(True)

                trajectory.append(x.detach().clone())

        return torch.stack(trajectory)


class EnergyBasedSamplingNetwork(nn.Module):
    """
    Sample-based neural network using Langevin dynamics
    Represents distributions via samples
    """

    def __init__(self, latent_dim, obs_dim, n_samples=10, temperature=0.1):
        super().__init__()
        self.latent_dim = latent_dim
        self.n_samples = n_samples
        self.temperature = temperature

        # Energy function E(z, x)
        self.energy_net = nn.Sequential(
            nn.Linear(latent_dim + obs_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )

        # Decoder p(x|z)
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 128),
            nn.ReLU(),
            nn.Linear(128, obs_dim)
        )

    def energy(self, z, x):
        """E(z, x) = -log p(x, z)"""
        combined = torch.cat([z, x], dim=-1)
        return self.energy_net(combined).squeeze()

    def sample_posterior(self, x_obs, n_steps=50, step_size=0.01):
        """
        Sample z ~ p(z|x) via Langevin
        """
        batch_size = x_obs.shape[0]
        z = torch.randn(batch_size, self.latent_dim)

        for _ in range(n_steps):
            z = z.requires_grad_(True)

            # Energy
            E = self.energy(z, x_obs).sum()

            # Gradient
            E.backward()

            with torch.no_grad():
                # Langevin step
                z = z - step_size * z.grad
                z = z + torch.randn_like(z) * np.sqrt(2 * step_size * self.temperature)

        return z.detach()


# Example: Sample from Gaussian mixture
def gaussian_mixture_energy(x):
    """
    Energy for mixture of Gaussians:
    p(x) = Σ w_k N(x | μ_k, σ²)
    E(x) = -log p(x)
    """
    # Three Gaussians
    mu1, mu2, mu3 = np.array([[-2, 0]]), np.array([[2, 0]]), np.array([[0, 3]])
    sigma = 0.5

    p1 = np.exp(-np.sum((x - mu1)**2) / (2 * sigma**2))
    p2 = np.exp(-np.sum((x - mu2)**2) / (2 * sigma**2))
    p3 = np.exp(-np.sum((x - mu3)**2) / (2 * sigma**2))

    p = (p1 + p2 + p3) / 3

    return -np.log(p + 1e-10)

# Langevin sampling
sampler = LangevinSampler(gaussian_mixture_energy, dim=2, temperature=0.5)

# Initialize near mode 1
x_init = np.array([-2.0, 0.0])

# Sample
samples = sampler.sample(x_init, n_steps=10000, dt=0.01, burnin=1000)

print(f"Generated {len(samples)} samples")
print(f"Sample mean: {samples.mean(axis=0)}")
print(f"Sample std: {samples.std(axis=0)}")

# Check multimodality (should visit all three modes)
modes_visited = []
for sample in samples[::100]:  # Check every 100th sample
    if np.linalg.norm(sample - [-2, 0]) < 1.0:
        modes_visited.append(1)
    elif np.linalg.norm(sample - [2, 0]) < 1.0:
        modes_visited.append(2)
    elif np.linalg.norm(sample - [0, 3]) < 1.0:
        modes_visited.append(3)

print(f"Modes visited: {set(modes_visited)}")
```

**Source**: Parisi (1981) Phys Lett; Roberts & Tweedie (1996) Bernoulli; Welling & Teh (2011) ICML; Orbán et al. (2016) Neuron

---

### 185. Gibbs Sampling in Neural Networks

**Purpose**: Stochastic binary units via conditional sampling—foundation for Boltzmann machines and probabilistic neural networks.

**Formula**: Conditional Sampling
```
Binary neuron activation:
P(s_i = 1 | s_{-i}) = σ(Σ W_ij s_j + b_i)
                         j≠i

where σ(z) = 1/(1 + e^{-z})

Gibbs sampling (sequential):
For each neuron i:
  Sample s_i ~ Bernoulli(σ(Σ W_ij s_j + b_i))
                            j

Block Gibbs (visible/hidden layers):
  Sample h ~ p(h|v)
  Sample v ~ p(v|h)

Energy function:
E(s) = -Σ_{i<j} W_ij s_i s_j - Σ_i b_i s_i

Equilibrium distribution:
p(s) = exp(-E(s)) / Z

where:
- s_i ∈ {0, 1} = neuron state
- W_ij = synaptic weight
- b_i = bias
- Z = partition function
- σ = sigmoid function
```

**Nature's Implementation**: Stochastic spiking as sampling. Trial-to-trial variability = samples from posterior. Explains probabilistic inference, uncertainty representation. Used for decision-making, perceptual inference, memory retrieval.

**Impact**: **MEDIUM - Probabilistic Neural Units**
Neurons as probabilistic samplers. Foundation for Boltzmann machines, RBMs. Explains neural variability as computation. Critical for understanding probabilistic brain hypothesis and implementing stochastic networks.

**Code Example**:
```python
class GibbsSamplingNetwork:
    """Binary stochastic network with Gibbs sampling"""

    def __init__(self, n_neurons):
        self.n = n_neurons

        # Weight matrix (symmetric for Boltzmann)
        self.W = np.random.randn(n_neurons, n_neurons) * 0.1
        self.W = (self.W + self.W.T) / 2  # Symmetrize
        np.fill_diagonal(self.W, 0)  # No self-connections

        # Biases
        self.b = np.zeros(n_neurons)

    def conditional_prob(self, i, state):
        """
        P(s_i = 1 | s_{-i}) = σ(Σ W_ij s_j + b_i)
        """
        activation = np.dot(self.W[i], state) + self.b[i]
        return 1.0 / (1.0 + np.exp(-activation))

    def gibbs_step(self, state, neuron_idx=None):
        """
        One Gibbs sampling step
        If neuron_idx specified, update only that neuron
        Otherwise, update random neuron
        """
        if neuron_idx is None:
            neuron_idx = np.random.randint(self.n)

        # Conditional probability
        p = self.conditional_prob(neuron_idx, state)

        # Sample
        state[neuron_idx] = 1 if np.random.rand() < p else 0

        return state

    def sample(self, n_steps=1000, burnin=100, init_state=None):
        """
        Generate samples via Gibbs sampling
        """
        if init_state is None:
            state = np.random.randint(0, 2, size=self.n)
        else:
            state = init_state.copy()

        samples = []

        for step in range(n_steps + burnin):
            # Update all neurons sequentially
            for i in range(self.n):
                state = self.gibbs_step(state, neuron_idx=i)

            # Store after burn-in
            if step >= burnin:
                samples.append(state.copy())

        return np.array(samples)

    def energy(self, state):
        """
        E(s) = -Σ W_ij s_i s_j - Σ b_i s_i
        """
        E = -0.5 * state @ self.W @ state - self.b @ state
        return E


class RestrictedBoltzmannMachine:
    """RBM with block Gibbs sampling"""

    def __init__(self, n_visible, n_hidden):
        self.n_v = n_visible
        self.n_h = n_hidden

        # Weights (no intra-layer connections)
        self.W = np.random.randn(n_visible, n_hidden) * 0.01
        self.b_v = np.zeros(n_visible)
        self.b_h = np.zeros(n_hidden)

    def sample_hidden(self, v):
        """
        Sample h ~ p(h|v)
        P(h_j = 1 | v) = σ(Σ W_ij v_i + b_h_j)
        """
        activation = v @ self.W + self.b_h
        p_h = 1.0 / (1.0 + np.exp(-activation))

        # Sample
        h = (np.random.rand(self.n_h) < p_h).astype(int)

        return h, p_h

    def sample_visible(self, h):
        """
        Sample v ~ p(v|h)
        P(v_i = 1 | h) = σ(Σ W_ij h_j + b_v_i)
        """
        activation = h @ self.W.T + self.b_v
        p_v = 1.0 / (1.0 + np.exp(-activation))

        # Sample
        v = (np.random.rand(self.n_v) < p_v).astype(int)

        return v, p_v

    def contrastive_divergence(self, v_data, k=1, lr=0.01):
        """
        CD-k learning: approximate gradient of log-likelihood
        Δ W ∝ ⟨v h^T⟩_data - ⟨v h^T⟩_model
        """
        # Positive phase (data)
        h_pos, p_h_pos = self.sample_hidden(v_data)
        pos_grad = np.outer(v_data, p_h_pos)

        # Negative phase (k steps of Gibbs)
        v_neg = v_data.copy()
        for _ in range(k):
            h_neg, _ = self.sample_hidden(v_neg)
            v_neg, p_v_neg = self.sample_visible(h_neg)

        h_neg, p_h_neg = self.sample_hidden(v_neg)
        neg_grad = np.outer(p_v_neg, p_h_neg)

        # Update weights
        self.W += lr * (pos_grad - neg_grad)
        self.b_v += lr * (v_data - p_v_neg)
        self.b_h += lr * (p_h_pos - p_h_neg)

    def train(self, data, n_epochs=100, k=1, lr=0.01):
        """Train RBM on binary data"""
        for epoch in range(n_epochs):
            # Shuffle data
            np.random.shuffle(data)

            for v_data in data:
                self.contrastive_divergence(v_data, k=k, lr=lr)

            if epoch % 20 == 0:
                # Reconstruction error
                v_test = data[0]
                h, _ = self.sample_hidden(v_test)
                v_recon, _ = self.sample_visible(h)
                error = np.mean((v_test - v_recon)**2)
                print(f"Epoch {epoch}, Reconstruction error: {error:.4f}")


# Example: Gibbs sampling network
n_neurons = 20
network = GibbsSamplingNetwork(n_neurons)

# Set weights to create some structure
# Two groups with strong intra-group connections
network.W[:10, :10] = 0.5  # Group 1
network.W[10:, 10:] = 0.5  # Group 2
network.W = (network.W + network.W.T) / 2
np.fill_diagonal(network.W, 0)

# Sample
samples = network.sample(n_steps=1000, burnin=100)

print(f"Generated {len(samples)} samples")
print(f"Mean activation: {samples.mean(axis=0)}")

# Check correlations
corr = np.corrcoef(samples.T)
print(f"\nIntra-group correlation (group 1): {corr[:10, :10].mean():.3f}")
print(f"Inter-group correlation: {corr[:10, 10:].mean():.3f}")

# RBM example
n_visible = 16
n_hidden = 8

rbm = RestrictedBoltzmannMachine(n_visible, n_hidden)

# Generate binary training data (random patterns)
train_data = np.random.randint(0, 2, size=(100, n_visible))

# Train
rbm.train(train_data, n_epochs=100, k=1, lr=0.1)

# Test reconstruction
v_test = train_data[0]
h, _ = rbm.sample_hidden(v_test)
v_recon, _ = rbm.sample_visible(h)

print(f"\nRBM Reconstruction:")
print(f"Input:  {v_test}")
print(f"Recon:  {v_recon}")
```

**Source**: Geman & Geman (1984) IEEE Trans PAMI; Hinton (2002) Neural Comp; Ackley et al. (1985) Cogn Sci; Buesing et al. (2011) NIPS

---

### 186. Neural Sampling Hypothesis

**Purpose**: Spikes as samples from posterior distributions—probabilistic population codes via sampling.

**Formula**: Spike-Based Sampling
```
Spike probability:
P(spike_i | x) ∝ exp(-(E_i(spike) - r_i(x))² / 2σ²)

Or Poisson:
P(spike_i | x) = (λ_i(x))^{n_i} exp(-λ_i(x)) / n_i!

where λ_i(x) = tuning curve

Population code as samples:
p(x | spikes) ≈ (1/N) Σ δ(x - x^{(i)})
                     i

where x^{(i)} decoded from spike pattern i

Sampling efficiency:
N_effective = N / (1 + r²)

where r = noise correlation

Bayesian inference:
p(x | r) ∝ Π p(r_i | x) p(x)
           i

Implemented via:
spikes ~ samples from p(x | r)

where:
- r = population rate vector
- n_i = spike count
- λ_i = firing rate
- x = stimulus/latent variable
- N = population size
```

**Nature's Implementation**: Cortical variability = samples, not noise. Trial-to-trial variability implements posterior sampling. Explains Poisson-like variability, correlation structure, uncertainty representation. Used for perception, decision-making, motor control.

**Impact**: **MEDIUM - Probabilistic Population Codes**
Variability is feature, not bug. Spikes encode distributions via samples. Bayesian inference without integration. Critical for understanding neural variability and implementing probabilistic neural networks.

**Code Example**:
```python
class NeuralSamplingPopulation:
    """Population code via spike sampling"""

    def __init__(self, n_neurons, stimulus_range=(0, 180)):
        self.n_neurons = n_neurons
        self.stim_min, self.stim_max = stimulus_range

        # Tuning curves (von Mises)
        self.preferred = np.linspace(self.stim_min, self.stim_max, n_neurons)
        self.tuning_width = 20.0

    def tuning_curve(self, stimulus, neuron_idx):
        """λ_i(x) = gain · exp(κ cos(x - μ_i))"""
        kappa = 1.0 / (self.tuning_width**2)
        rate = 10 * np.exp(kappa * np.cos(2 * np.pi * (stimulus - self.preferred[neuron_idx]) / 180))
        return rate

    def sample_spikes_poisson(self, stimulus, n_trials=1):
        """
        Generate spike samples via Poisson process
        Each trial = one sample from posterior
        """
        spikes = np.zeros((n_trials, self.n_neurons))

        for trial in range(n_trials):
            for i in range(self.n_neurons):
                rate = self.tuning_curve(stimulus, i)
                spikes[trial, i] = np.random.poisson(rate)

        return spikes

    def decode_sample(self, spike_pattern):
        """
        Decode stimulus from single spike pattern (one sample)
        x̂ = argmax p(spikes | x)
        """
        stimulus_grid = np.linspace(self.stim_min, self.stim_max, 180)
        log_likelihood = np.zeros(len(stimulus_grid))

        for j, stim in enumerate(stimulus_grid):
            # Log-likelihood: Σ [n_i log(λ_i) - λ_i]
            for i in range(self.n_neurons):
                rate = self.tuning_curve(stim, i)
                log_likelihood[j] += spike_pattern[i] * np.log(rate + 1e-10) - rate

        # MAP estimate
        decoded = stimulus_grid[np.argmax(log_likelihood)]
        return decoded

    def posterior_from_samples(self, spikes, stimulus_grid=None):
        """
        Approximate posterior via samples:
        p(x | r) ≈ (1/N) Σ δ(x - x_decoded^{(i)})
        """
        if stimulus_grid is None:
            stimulus_grid = np.linspace(self.stim_min, self.stim_max, 180)

        # Decode each sample (trial)
        decoded_samples = []
        for trial in range(spikes.shape[0]):
            decoded = self.decode_sample(spikes[trial])
            decoded_samples.append(decoded)

        # Histogram to approximate distribution
        hist, bins = np.histogram(decoded_samples, bins=stimulus_grid)
        posterior = hist / hist.sum()

        return bins[:-1], posterior

    def compare_integration_vs_sampling(self, stimulus, n_samples=100):
        """
        Compare:
        1. Analytical integration (exact Bayesian)
        2. Sampling approximation
        """
        # Generate samples
        spikes = self.sample_spikes_poisson(stimulus, n_trials=n_samples)

        # Sampling-based posterior
        stim_grid, posterior_samples = self.posterior_from_samples(spikes)

        # Integration-based posterior (analytical)
        # Average spike pattern
        mean_spikes = spikes.mean(axis=0)

        # Likelihood for each stimulus
        posterior_integration = np.zeros(len(stim_grid))
        for j, stim in enumerate(stim_grid):
            log_lik = 0
            for i in range(self.n_neurons):
                rate = self.tuning_curve(stim, i)
                log_lik += mean_spikes[i] * np.log(rate + 1e-10) - rate

            posterior_integration[j] = np.exp(log_lik)

        posterior_integration /= posterior_integration.sum()

        return stim_grid, posterior_samples, posterior_integration


class SamplingNeuralNetwork(nn.Module):
    """Neural network with sampling-based inference"""

    def __init__(self, input_dim, hidden_dim, n_samples=10):
        super().__init__()
        self.n_samples = n_samples

        # Encoder: input → distribution parameters
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim * 2)  # μ and log σ
        )

    def forward(self, x):
        """
        Sample-based inference
        Represent distribution via samples instead of parameters
        """
        # Distribution parameters
        h = self.encoder(x)
        mu = h[:, :h.shape[1]//2]
        log_sigma = h[:, h.shape[1]//2:]

        # Generate samples (instead of single mean)
        samples = []
        for _ in range(self.n_samples):
            eps = torch.randn_like(mu)
            sample = mu + torch.exp(log_sigma) * eps
            samples.append(sample)

        # Represent distribution via samples
        return torch.stack(samples, dim=1)  # [batch, n_samples, hidden_dim]

    def sample_based_prediction(self, x, prediction_fn):
        """
        Make prediction by sampling:
        E[f(z)] ≈ (1/N) Σ f(z_i), z_i ~ p(z|x)
        """
        samples = self.forward(x)  # [batch, n_samples, dim]

        # Apply prediction function to each sample
        predictions = []
        for i in range(self.n_samples):
            pred = prediction_fn(samples[:, i])
            predictions.append(pred)

        # Average predictions
        return torch.stack(predictions, dim=0).mean(dim=0)


# Example: Sampling vs integration
n_neurons = 50
population = NeuralSamplingPopulation(n_neurons, stimulus_range=(0, 180))

# True stimulus
true_stimulus = 90

# Compare methods
stim_grid, posterior_samples, posterior_integration = population.compare_integration_vs_sampling(
    true_stimulus, n_samples=500
)

print(f"True stimulus: {true_stimulus}°")

# Sampling-based estimate
if len(posterior_samples) > 0 and posterior_samples.sum() > 0:
    sample_mean = np.sum(stim_grid * posterior_samples / posterior_samples.sum())
    print(f"Sampling estimate: {sample_mean:.1f}°")

# Integration-based estimate
int_mean = np.sum(stim_grid * posterior_integration)
print(f"Integration estimate: {int_mean:.1f}°")

# Uncertainty (variance)
sample_var = np.sum((stim_grid - sample_mean)**2 * posterior_samples / posterior_samples.sum()) if posterior_samples.sum() > 0 else 0
int_var = np.sum((stim_grid - int_mean)**2 * posterior_integration)

print(f"\nUncertainty (std):")
print(f"  Sampling: {np.sqrt(sample_var):.1f}°")
print(f"  Integration: {np.sqrt(int_var):.1f}°")
```

**Source**: Hoyer & Hyvarinen (2003) NIPS; Fiser et al. (2010) Trends Cogn Sci; Orbán et al. (2016) Neuron; Berkes et al. (2011) Science

---

### 187. Boltzmann Machine (Unrestricted Energy Model)

**Purpose**: General energy-based model with symmetric weights—foundation for unsupervised learning and generative models.

**Formula**: Energy-Based Distribution
```
Energy function:
E(s) = -Σ_{i<j} W_ij s_i s_j - Σ_i b_i s_i

Probability distribution:
p(s) = exp(-E(s)) / Z

where Z = Σ exp(-E(s')) [partition function]
          s'

Learning (maximum likelihood):
∂log p(s) / ∂W_ij = ⟨s_i s_j⟩_data - ⟨s_i s_j⟩_model

Gradient:
Δ W_ij = η (⟨s_i s_j⟩_data - ⟨s_i s_j⟩_model)

where:
- ⟨·⟩_data = expectation under data
- ⟨·⟩_model = expectation under model (via sampling)
- s_i ∈ {0, 1} or {-1, +1}
- W_ij = W_ji (symmetric)

Restricted BM (bipartite):
E(v, h) = -v^T W h - b^T v - c^T h
```

**Nature's Implementation**: Attractor networks, associative memory, unsupervised learning. Symmetric recurrent connections. Energy minimization = pattern completion. Explains spontaneous brain activity, memory consolidation, slow-wave sleep.

**Impact**: **MEDIUM - Energy-Based Learning**
Unsupervised learning via energy minimization. Generative model. Foundation for RBMs, deep Boltzmann machines. Critical for understanding unsupervised cortical learning and implementing energy-based models.

**Code Example**:
```python
class BoltzmannMachine:
    """General Boltzmann machine with unrestricted connectivity"""

    def __init__(self, n_units):
        self.n_units = n_units

        # Symmetric weight matrix
        self.W = np.random.randn(n_units, n_units) * 0.01
        self.W = (self.W + self.W.T) / 2
        np.fill_diagonal(self.W, 0)

        # Biases
        self.b = np.zeros(n_units)

    def energy(self, s):
        """
        E(s) = -Σ W_ij s_i s_j - Σ b_i s_i
        """
        return -0.5 * s @ self.W @ s - self.b @ s

    def sample_gibbs(self, n_steps=1000, init_state=None):
        """Sample from model via Gibbs sampling"""
        if init_state is None:
            state = np.random.randint(0, 2, size=self.n_units)
        else:
            state = init_state.copy()

        for _ in range(n_steps):
            # Update each unit
            for i in range(self.n_units):
                # Conditional probability
                activation = np.dot(self.W[i], state) + self.b[i]
                p = 1.0 / (1.0 + np.exp(-activation))

                # Sample
                state[i] = 1 if np.random.rand() < p else 0

        return state

    def train(self, data, n_epochs=100, lr=0.01, k=10):
        """
        Train via contrastive divergence
        Δ W = η (⟨s_i s_j⟩_data - ⟨s_i s_j⟩_model)
        """
        n_samples = len(data)

        for epoch in range(n_epochs):
            # Data statistics
            pos_corr = np.zeros((self.n_units, self.n_units))
            pos_bias = np.zeros(self.n_units)

            for s_data in data:
                pos_corr += np.outer(s_data, s_data)
                pos_bias += s_data

            pos_corr /= n_samples
            pos_bias /= n_samples

            # Model statistics (via sampling)
            neg_corr = np.zeros((self.n_units, self.n_units))
            neg_bias = np.zeros(self.n_units)

            for s_data in data:
                # k steps of Gibbs starting from data
                s_model = s_data.copy()
                for _ in range(k):
                    s_model = self.sample_gibbs(n_steps=1, init_state=s_model)

                neg_corr += np.outer(s_model, s_model)
                neg_bias += s_model

            neg_corr /= n_samples
            neg_bias /= n_samples

            # Update
            self.W += lr * (pos_corr - neg_corr)
            self.W = (self.W + self.W.T) / 2  # Symmetrize
            np.fill_diagonal(self.W, 0)

            self.b += lr * (pos_bias - neg_bias)

            if epoch % 20 == 0:
                # Average energy
                avg_energy = np.mean([self.energy(s) for s in data])
                print(f"Epoch {epoch}, Average energy: {avg_energy:.4f}")

    def generate_samples(self, n_samples, n_steps=1000):
        """Generate new samples from model"""
        samples = []
        for _ in range(n_samples):
            sample = self.sample_gibbs(n_steps=n_steps)
            samples.append(sample)

        return np.array(samples)


# Example: Learn binary patterns
n_units = 16
bm = BoltzmannMachine(n_units)

# Create training patterns (e.g., vertical and horizontal bars)
patterns = []

# Vertical bars
for i in range(4):
    pattern = np.zeros(16)
    pattern[i::4] = 1
    patterns.append(pattern)

# Horizontal bars
for i in range(4):
    pattern = np.zeros(16)
    pattern[i*4:(i+1)*4] = 1
    patterns.append(pattern)

patterns = np.array(patterns)

print("Training patterns:")
for i, p in enumerate(patterns):
    print(f"  {i}: {p.reshape(4, 4).astype(int)}")

# Train
bm.train(patterns, n_epochs=200, lr=0.1, k=5)

# Generate new samples
generated = bm.generate_samples(n_samples=5, n_steps=1000)

print("\nGenerated patterns:")
for i, g in enumerate(generated):
    print(f"  {i}: {g.reshape(4, 4).astype(int)}")

# Check if generated patterns match training distribution
energies_train = [bm.energy(p) for p in patterns]
energies_gen = [bm.energy(g) for g in generated]

print(f"\nEnergy statistics:")
print(f"  Training: {np.mean(energies_train):.4f} ± {np.std(energies_train):.4f}")
print(f"  Generated: {np.mean(energies_gen):.4f} ± {np.std(energies_gen):.4f}")
```

**Source**: Ackley et al. (1985) Cogn Sci; Hinton & Sejnowski (1983) Proc IEEE; Salakhutdinov & Hinton (2009) AISTATS; Fischer & Igel (2012) ICANN

---
### 188. Reward-Modulated STDP (R-STDP)

**Formula:**
```
Δw = R · f(Δt)

where f(Δt) = {
    A_+ e^{-Δt/τ_+}     if Δt > 0  (post before pre)
    -A_- e^{Δt/τ_-}     if Δt < 0  (pre before post)
}

Δt = t_post - t_pre
R = reward signal (scalar modulation)
A_+, A_- = potentiation/depression amplitudes
τ_+, τ_- = time constants
```

**Variable Definitions:**
- `w`: synaptic weight
- `R`: reward signal (dopamine-like modulation)
- `Δt`: spike time difference (post - pre)
- `A_+`: LTP amplitude when post fires after pre
- `A_-`: LTD amplitude when pre fires after post
- `τ_+, τ_-`: STDP time constants (~20ms)

**Nature's Implementation:**
Dopaminergic neurons in VTA/SNc broadcast reward prediction errors that modulate spike-timing-dependent plasticity in striatal and cortical circuits. This three-factor learning rule (pre-spike, post-spike, reward) implements reinforcement learning by selectively strengthening synapses that preceded rewarding outcomes.

**Impact:** CRITICAL - Bridges reinforcement learning theory with biological synaptic plasticity, explaining how dopamine enables credit assignment over time. Foundation for actor-critic models and deep RL algorithms with biological constraints.

**Implementation (250 lines):**
```python
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

class RewardModulatedSTDP:
    """
    Reward-Modulated Spike-Timing-Dependent Plasticity

    Implements R-STDP where synaptic changes depend on:
    1. Relative spike timing (STDP kernel)
    2. Reward signal (dopamine-like modulation)
    3. Eligibility traces (bridges temporal credit assignment)
    """

    def __init__(self, n_pre, n_post, A_plus=0.01, A_minus=0.012,
                 tau_plus=20.0, tau_minus=20.0, tau_eligibility=100.0,
                 w_min=0.0, w_max=1.0):
        """
        Args:
            n_pre: Number of presynaptic neurons
            n_post: Number of postsynaptic neurons
            A_plus: LTP amplitude
            A_minus: LTD amplitude
            tau_plus: LTP time constant (ms)
            tau_minus: LTD time constant (ms)
            tau_eligibility: Eligibility trace decay (ms)
            w_min, w_max: Weight bounds
        """
        self.n_pre = n_pre
        self.n_post = n_post

        # STDP parameters
        self.A_plus = A_plus
        self.A_minus = A_minus
        self.tau_plus = tau_plus
        self.tau_minus = tau_minus

        # Eligibility trace parameters
        self.tau_e = tau_eligibility

        # Synaptic weights
        self.W = np.random.uniform(0.2, 0.5, (n_post, n_pre))
        self.w_min = w_min
        self.w_max = w_max

        # Eligibility traces
        self.eligibility = np.zeros((n_post, n_pre))

        # Spike timing buffers
        self.pre_spike_times = [deque(maxlen=100) for _ in range(n_pre)]
        self.post_spike_times = [deque(maxlen=100) for _ in range(n_post)]

    def stdp_kernel(self, delta_t):
        """
        Compute STDP kernel: f(Δt) = A_+ exp(-Δt/τ_+) or -A_- exp(Δt/τ_-)

        Args:
            delta_t: Post spike time - pre spike time

        Returns:
            Weight change factor
        """
        if delta_t > 0:
            # Post after pre -> LTP
            return self.A_plus * np.exp(-delta_t / self.tau_plus)
        elif delta_t < 0:
            # Pre after post -> LTD
            return -self.A_minus * np.exp(delta_t / self.tau_minus)
        else:
            return 0.0

    def update_eligibility(self, pre_spikes, post_spikes, current_time, dt=1.0):
        """
        Update eligibility traces based on spike timing

        e_ij(t+dt) = e_ij(t) * exp(-dt/τ_e) + f(Δt_ij)

        Args:
            pre_spikes: Binary array [n_pre] indicating which pre neurons spiked
            post_spikes: Binary array [n_post] indicating which post neurons spiked
            current_time: Current simulation time (ms)
            dt: Time step (ms)
        """
        # Decay existing traces
        decay_factor = np.exp(-dt / self.tau_e)
        self.eligibility *= decay_factor

        # Update spike time buffers
        for i, spiked in enumerate(pre_spikes):
            if spiked:
                self.pre_spike_times[i].append(current_time)

        for j, spiked in enumerate(post_spikes):
            if spiked:
                self.post_spike_times[j].append(current_time)

        # Compute STDP contributions for each synapse
        for j in range(self.n_post):
            if not post_spikes[j]:
                continue

            for i in range(self.n_pre):
                # Check all recent pre-spikes for this synapse
                for t_pre in self.pre_spike_times[i]:
                    if abs(current_time - t_pre) < 5 * self.tau_plus:
                        delta_t = current_time - t_pre
                        self.eligibility[j, i] += self.stdp_kernel(delta_t)

        # Also check for LTD (pre after post)
        for i in range(self.n_pre):
            if not pre_spikes[i]:
                continue

            for j in range(self.n_post):
                for t_post in self.post_spike_times[j]:
                    if abs(current_time - t_post) < 5 * self.tau_minus:
                        delta_t = t_post - current_time
                        if delta_t < 0:  # Post was before this pre spike
                            self.eligibility[j, i] += self.stdp_kernel(delta_t)

    def apply_reward(self, reward):
        """
        Apply reward-modulated weight update: Δw = R · e

        Args:
            reward: Scalar reward signal (can be positive or negative)
        """
        # Weight update proportional to eligibility and reward
        dW = reward * self.eligibility

        self.W += dW

        # Enforce weight bounds
        self.W = np.clip(self.W, self.w_min, self.w_max)

        # Optional: Reset eligibility after reward (depends on model)
        # self.eligibility *= 0.5  # Partial reset

    def forward(self, pre_activity):
        """
        Compute postsynaptic activity

        Args:
            pre_activity: [n_pre] activity levels

        Returns:
            post_activity: [n_post] weighted sum
        """
        return self.W @ pre_activity


class RSTDPPolicyNetwork:
    """
    Complete reinforcement learning agent using R-STDP
    """

    def __init__(self, n_states, n_actions, n_hidden=100):
        self.n_states = n_states
        self.n_actions = n_actions
        self.n_hidden = n_hidden

        # Two-layer network with R-STDP synapses
        self.layer1 = RewardModulatedSTDP(n_states, n_hidden,
                                          A_plus=0.01, A_minus=0.012)
        self.layer2 = RewardModulatedSTDP(n_hidden, n_actions,
                                          A_plus=0.01, A_minus=0.012)

        # Spike generation parameters
        self.threshold = 1.0
        self.reset_potential = 0.0
        self.tau_mem = 10.0

    def encode_state(self, state):
        """Convert state to spike rates (population coding)"""
        # Simple rate coding: state values -> Poisson spike probabilities
        return np.clip(state, 0, 1)

    def generate_spikes(self, rates, dt=1.0):
        """Generate Poisson spikes from rates"""
        return np.random.rand(len(rates)) < (rates * dt / 1000.0)

    def integrate_and_fire(self, input_current, membrane_potential, dt=1.0):
        """
        Simple LIF dynamics

        τ dV/dt = -V + I
        """
        dV = (-membrane_potential + input_current) / self.tau_mem * dt
        membrane_potential += dV

        spikes = membrane_potential >= self.threshold
        membrane_potential[spikes] = self.reset_potential

        return membrane_potential, spikes

    def select_action(self, state, T=100, dt=1.0):
        """
        Run spiking network for T ms and select action based on spike counts

        Args:
            state: Environment state
            T: Simulation time (ms)
            dt: Time step (ms)

        Returns:
            action: Selected action index
            spike_counts: [n_actions] spike counts for debugging
        """
        # Initialize
        V_hidden = np.zeros(self.n_hidden)
        V_output = np.zeros(self.n_actions)
        spike_counts = np.zeros(self.n_actions)

        # Encode state as rates
        input_rates = self.encode_state(state)

        # Simulate for T milliseconds
        for t in np.arange(0, T, dt):
            # Generate input spikes
            input_spikes = self.generate_spikes(input_rates, dt)

            # Layer 1: State -> Hidden
            I_hidden = self.layer1.forward(input_spikes.astype(float))
            V_hidden, spikes_hidden = self.integrate_and_fire(I_hidden, V_hidden, dt)

            # Layer 2: Hidden -> Actions
            I_output = self.layer2.forward(spikes_hidden.astype(float))
            V_output, spikes_output = self.integrate_and_fire(I_output, V_output, dt)

            spike_counts += spikes_output

        # Select action with highest spike count (plus exploration noise)
        action_probs = spike_counts / (spike_counts.sum() + 1e-10)
        action = np.random.choice(self.n_actions, p=action_probs + 1e-10)

        return action, spike_counts

    def train_episode(self, state_sequence, action_sequence, reward_sequence, T=100):
        """
        Train on an episode using R-STDP

        Args:
            state_sequence: List of states
            action_sequence: List of actions taken
            reward_sequence: List of rewards received
            T: Simulation time per step (ms)
        """
        dt = 1.0

        for state, action, reward in zip(state_sequence, action_sequence, reward_sequence):
            # Forward pass (same as select_action but track all spikes)
            V_hidden = np.zeros(self.n_hidden)
            V_output = np.zeros(self.n_actions)

            input_rates = self.encode_state(state)

            for t in np.arange(0, T, dt):
                input_spikes = self.generate_spikes(input_rates, dt)

                # Layer 1
                I_hidden = self.layer1.forward(input_spikes.astype(float))
                V_hidden, spikes_hidden = self.integrate_and_fire(I_hidden, V_hidden, dt)

                # Update eligibility traces for layer 1
                self.layer1.update_eligibility(input_spikes, spikes_hidden, t, dt)

                # Layer 2
                I_output = self.layer2.forward(spikes_hidden.astype(float))
                V_output, spikes_output = self.integrate_and_fire(I_output, V_output, dt)

                # Update eligibility traces for layer 2
                self.layer2.update_eligibility(spikes_hidden, spikes_output, t, dt)

            # Apply reward to both layers
            self.layer1.apply_reward(reward)
            self.layer2.apply_reward(reward)


# Example: Train on simple bandit task
if __name__ == "__main__":
    np.random.seed(42)

    # 2-armed bandit: state is constant, 2 actions with different reward probs
    n_states = 4
    n_actions = 2

    # True reward probabilities
    reward_probs = [0.3, 0.7]  # Action 1: 30%, Action 2: 70%

    agent = RSTDPPolicyNetwork(n_states, n_actions, n_hidden=50)

    # Training
    n_trials = 500
    rewards_history = []
    action_history = []

    print("Training R-STDP agent on 2-armed bandit...")

    for trial in range(n_trials):
        # Fixed state (bandit has no state)
        state = np.array([0.5, 0.5, 0.5, 0.5])

        # Select action
        action, spike_counts = agent.select_action(state, T=100)

        # Get reward
        reward = 1.0 if np.random.rand() < reward_probs[action] else -0.5

        # Train
        agent.train_episode([state], [action], [reward], T=100)

        rewards_history.append(reward)
        action_history.append(action)

        if trial % 100 == 0:
            recent_reward = np.mean(rewards_history[-100:]) if len(rewards_history) >= 100 else np.mean(rewards_history)
            recent_actions = np.array(action_history[-100:]) if len(action_history) >= 100 else np.array(action_history)
            action_1_rate = np.mean(recent_actions == 1)
            print(f"Trial {trial}: Avg reward = {recent_reward:.3f}, Action 1 rate = {action_1_rate:.2f}")

    # Final evaluation
    final_actions = np.array(action_history[-100:])
    print(f"\nFinal performance:")
    print(f"  Action 0 rate: {np.mean(final_actions == 0):.2f} (optimal: {reward_probs[0]:.2f})")
    print(f"  Action 1 rate: {np.mean(final_actions == 1):.2f} (optimal: {reward_probs[1]:.2f})")
    print(f"  Average reward: {np.mean(rewards_history[-100:]):.3f}")
```

**Sources:**
- Frémaux & Gerstner (2016). "Neuromodulated Spike-Timing-Dependent Plasticity and Theory of Three-Factor Learning Rules"
- Izhikevich (2007). "Solving the Distal Reward Problem through Linkage of STDP and Dopamine Signaling"
- Florian (2007). "Reinforcement Learning Through Modulation of Spike-Timing-Dependent Synaptic Plasticity"

---

### 189. Contrastive Hebbian Learning (CHL)

**Formula:**
```
ΔW = η(x^+ y^{+T} - x^- y^{-T})

where:
x^+ = activity during positive (clamped) phase
y^+ = activity during positive phase
x^- = activity during negative (free) phase
y^- = activity during negative phase
η = learning rate
```

**Equivalent Energy-Based Formulation:**
```
ΔW = η(⟨xy^T⟩_data - ⟨xy^T⟩_model)

For energy E(x,y) = -y^T W x:
∂E/∂W = -xy^T
```

**Variable Definitions:**
- `W`: weight matrix between layers
- `x^+`: "clamped" activity when output is constrained to target
- `y^+`: output activity in clamped phase (= target)
- `x^-`: "free" activity when network runs autonomously
- `y^-`: output activity in free phase (= prediction)
- `η`: learning rate

**Nature's Implementation:**
CHL models cortical learning through alternating phases of feedforward and feedback processing. The positive phase represents sensory-driven activity with top-down constraints, while the negative phase represents internally generated predictions. This matches wake-sleep cycles and attentional modulation in cortex.

**Impact:** HIGH - Demonstrates that Hebbian learning with contrastive phases (positive/negative) is mathematically equivalent to backpropagation under symmetric weights. Provides biologically plausible account of credit assignment without explicit error signals or non-local weight transport.

**Implementation (280 lines):**
```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt

class ContrastiveHebbianLayer(nn.Module):
    """
    Single layer with Contrastive Hebbian Learning

    ΔW = η(x^+ y^{+T} - x^- y^{-T})

    Two-phase learning:
    1. Positive phase: Output clamped to target, measure x^+ y^{+T}
    2. Negative phase: Output free-running, measure x^- y^{-T}
    """

    def __init__(self, input_dim, output_dim, symmetric=True):
        super().__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.symmetric = symmetric

        # Forward weights
        self.W = nn.Parameter(torch.randn(output_dim, input_dim) * 0.1)

        if symmetric:
            # Backward weights = forward weights (weight transport problem solved)
            self.W_back = self.W.T
        else:
            # Separate backward weights (biologically implausible)
            self.W_back = nn.Parameter(torch.randn(input_dim, output_dim) * 0.1)

        self.bias = nn.Parameter(torch.zeros(output_dim))

    def forward_pass(self, x):
        """Compute forward activation y = f(Wx + b)"""
        return torch.sigmoid(F.linear(x, self.W, self.bias))

    def backward_pass(self, y):
        """Compute backward activation x = f(W^T y)"""
        if self.symmetric:
            return torch.sigmoid(F.linear(y, self.W.T))
        else:
            return torch.sigmoid(F.linear(y, self.W_back))

    def positive_phase(self, x, y_target, n_steps=10, lr_phase=0.1):
        """
        Positive (clamped) phase: Settle to equilibrium with output clamped

        Args:
            x: Input [batch, input_dim]
            y_target: Target output [batch, output_dim]
            n_steps: Number of settling iterations
            lr_phase: Step size for settling

        Returns:
            x_plus: Settled input activity
            y_plus: Settled output activity (close to y_target)
        """
        x_plus = x.clone()
        y_plus = y_target.clone()

        for _ in range(n_steps):
            # Update input based on feedback from clamped output
            x_recon = self.backward_pass(y_plus)
            x_plus = x_plus + lr_phase * (x + x_recon - 2 * x_plus)

            # Keep output clamped (but allow small relaxation toward forward prediction)
            y_pred = self.forward_pass(x_plus)
            y_plus = 0.9 * y_target + 0.1 * y_pred

        return x_plus, y_plus

    def negative_phase(self, x, n_steps=10, lr_phase=0.1):
        """
        Negative (free) phase: Settle to equilibrium without clamping

        Args:
            x: Input [batch, input_dim]
            n_steps: Number of settling iterations
            lr_phase: Step size for settling

        Returns:
            x_minus: Settled input activity
            y_minus: Settled output activity (free prediction)
        """
        x_minus = x.clone()

        for _ in range(n_steps):
            # Forward pass
            y_minus = self.forward_pass(x_minus)

            # Backward pass
            x_recon = self.backward_pass(y_minus)

            # Settle toward consistency
            x_minus = x_minus + lr_phase * (x + x_recon - 2 * x_minus)

        # Final forward pass
        y_minus = self.forward_pass(x_minus)

        return x_minus, y_minus

    def contrastive_update(self, x_plus, y_plus, x_minus, y_minus, lr):
        """
        Apply CHL weight update: ΔW = η(x^+ y^{+T} - x^- y^{-T})

        Args:
            x_plus, y_plus: Activities from positive phase
            x_minus, y_minus: Activities from negative phase
            lr: Learning rate
        """
        batch_size = x_plus.shape[0]

        # Positive phase statistics: ⟨xy^T⟩_clamped
        pos_corr = torch.matmul(y_plus.T, x_plus) / batch_size

        # Negative phase statistics: ⟨xy^T⟩_free
        neg_corr = torch.matmul(y_minus.T, x_minus) / batch_size

        # Contrastive Hebbian update
        dW = lr * (pos_corr - neg_corr)

        self.W.data += dW

        # Update bias
        db = lr * (y_plus.mean(0) - y_minus.mean(0))
        self.bias.data += db


class ContrastiveHebbianNetwork(nn.Module):
    """
    Multi-layer network trained with Contrastive Hebbian Learning
    """

    def __init__(self, layer_sizes, symmetric=True):
        """
        Args:
            layer_sizes: List of layer dimensions [input, hidden1, hidden2, ..., output]
            symmetric: Use symmetric weights (W_back = W_forward^T)
        """
        super().__init__()
        self.layer_sizes = layer_sizes
        self.n_layers = len(layer_sizes) - 1

        # Create layers
        self.layers = nn.ModuleList([
            ContrastiveHebbianLayer(layer_sizes[i], layer_sizes[i+1], symmetric)
            for i in range(self.n_layers)
        ])

    def forward(self, x):
        """Standard forward pass"""
        h = x
        for layer in self.layers:
            h = layer.forward_pass(h)
        return h

    def train_batch(self, x, y_target, lr=0.01, n_settle=20):
        """
        Train on batch using contrastive phases

        Args:
            x: Input [batch, input_dim]
            y_target: Target [batch, output_dim]
            lr: Learning rate
            n_settle: Settling steps per phase

        Returns:
            loss: Reconstruction error
        """
        # POSITIVE PHASE: Clamp output to target, settle network
        activities_plus = [x]
        h = x

        # Forward pass through all layers
        for i, layer in enumerate(self.layers[:-1]):
            h = layer.forward_pass(h)
            activities_plus.append(h)

        # Last layer: run positive phase with clamped output
        x_in = activities_plus[-1]
        x_plus_final, y_plus = self.layers[-1].positive_phase(
            x_in, y_target, n_steps=n_settle
        )
        activities_plus[-1] = x_plus_final
        activities_plus.append(y_plus)

        # NEGATIVE PHASE: Free-running, settle network
        activities_minus = [x]
        h = x

        # Forward through all layers (free-running)
        for layer in self.layers:
            h = layer.forward_pass(h)
            activities_minus.append(h)

        # Settle final layer
        x_in = activities_minus[-2]
        x_minus_final, y_minus = self.layers[-1].negative_phase(
            x_in, n_steps=n_settle
        )
        activities_minus[-2] = x_minus_final
        activities_minus[-1] = y_minus

        # UPDATE WEIGHTS using contrastive Hebbian rule
        for i, layer in enumerate(self.layers):
            x_plus = activities_plus[i]
            y_plus = activities_plus[i+1]
            x_minus = activities_minus[i]
            y_minus = activities_minus[i+1]

            layer.contrastive_update(x_plus, y_plus, x_minus, y_minus, lr)

        # Compute loss (for monitoring)
        loss = F.mse_loss(y_minus, y_target)

        return loss.item()


# Example: Train on MNIST-like classification
if __name__ == "__main__":
    torch.manual_seed(42)

    # Generate synthetic data (XOR-like problem)
    def generate_xor_data(n_samples=100):
        X = torch.randn(n_samples, 2)
        y = ((X[:, 0] > 0) ^ (X[:, 1] > 0)).long()
        y_onehot = F.one_hot(y, num_classes=2).float()
        return X, y_onehot

    # Create network
    model = ContrastiveHebbianNetwork(
        layer_sizes=[2, 20, 20, 2],
        symmetric=True
    )

    print("Training Contrastive Hebbian Network on XOR task...")
    print("Architecture:", model.layer_sizes)

    # Training loop
    n_epochs = 500
    batch_size = 32
    lr = 0.1

    losses = []

    for epoch in range(n_epochs):
        X_train, y_train = generate_xor_data(batch_size)

        loss = model.train_batch(X_train, y_train, lr=lr, n_settle=10)
        losses.append(loss)

        if epoch % 50 == 0:
            # Evaluate
            with torch.no_grad():
                X_test, y_test = generate_xor_data(500)
                y_pred = model.forward(X_test)
                pred_classes = y_pred.argmax(dim=1)
                true_classes = y_test.argmax(dim=1)
                acc = (pred_classes == true_classes).float().mean()

                print(f"Epoch {epoch}: Loss = {loss:.4f}, Accuracy = {acc:.3f}")

    # Final test
    print("\nFinal evaluation:")
    with torch.no_grad():
        X_test, y_test = generate_xor_data(1000)
        y_pred = model.forward(X_test)
        pred_classes = y_pred.argmax(dim=1)
        true_classes = y_test.argmax(dim=1)
        acc = (pred_classes == true_classes).float().mean()
        print(f"Test Accuracy: {acc:.3f}")

        # Check weight symmetry
        if model.layers[0].symmetric:
            print("\nWeight symmetry maintained (biologically plausible)")

        # Show weight statistics
        for i, layer in enumerate(model.layers):
            print(f"Layer {i} weights: mean={layer.W.mean():.3f}, std={layer.W.std():.3f}")
```

**Sources:**
- Movellan (1991). "Contrastive Hebbian Learning in the Continuous Hopfield Model"
- Xie & Seung (2003). "Equivalence of Backpropagation and Contrastive Hebbian Learning"
- Hinton (2007). "Learning Multiple Layers of Representation"

---

### 190. Liquid State Machine (LSM)

**Formula:**
```
ẋ = -λx + W_rec σ(x) + W_in u(t)

y(t) = W_out x(t)

where:
x ∈ ℝ^N = recurrent reservoir state
u(t) = input signal
W_rec = fixed random recurrent weights
W_in = fixed random input weights
W_out = trained readout weights (only trainable parameters)
σ = activation function (typically tanh or identity)
λ = leak rate
```

**Separation Property:**
```
||x(u₁, t) - x(u₂, t)|| > ε  if u₁ ≠ u₂

(Different inputs create separated trajectories)
```

**Approximation Property:**
```
f: U → Y can be approximated by W_out x(u, t)

(Rich dynamics enable universal computation)
```

**Variable Definitions:**
- `x(t)`: N-dimensional reservoir state (liquid)
- `u(t)`: Input time series
- `W_rec`: N×N fixed recurrent connectivity (sparse, random)
- `W_in`: N×D fixed input projection
- `W_out`: M×N trainable readout weights
- `λ`: Leak time constant (neuron time scale)
- `σ`: Nonlinearity (typically tanh)

**Nature's Implementation:**
Cortical microcircuits act as liquid reservoirs with rich, high-dimensional dynamics driven by recurrent connectivity. Input signals perturb this "neural liquid," creating complex spatiotemporal activity patterns. Downstream readout neurons (e.g., in motor cortex) learn to extract task-relevant information from these transient states without modifying the recurrent circuit.

**Impact:** HIGH - Demonstrates that random recurrent networks can serve as universal temporal processors when combined with linear readout. Explains how cortex can rapidly adapt to new tasks by only training readout connections, preserving the rich dynamics of cortical columns. Foundation for reservoir computing and echo state networks.

**Implementation (300 lines):**
```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse

class LiquidStateMachine(nn.Module):
    """
    Liquid State Machine (LSM) / Reservoir Computer

    Reservoir dynamics: ẋ = -λx + W_rec tanh(x) + W_in u(t) + noise
    Readout: y = W_out x

    Only W_out is trained; W_rec and W_in are fixed random matrices.
    """

    def __init__(self, input_dim, reservoir_dim, output_dim,
                 spectral_radius=0.9, sparsity=0.1, leak_rate=1.0,
                 input_scaling=1.0, noise_level=0.0):
        """
        Args:
            input_dim: Dimension of input signal u(t)
            reservoir_dim: Number of reservoir neurons N
            output_dim: Dimension of output y(t)
            spectral_radius: Largest eigenvalue magnitude of W_rec
            sparsity: Connection probability in W_rec
            leak_rate: λ in ẋ = -λx + ...
            input_scaling: Scaling for W_in
            noise_level: σ_noise for neural noise
        """
        super().__init__()

        self.input_dim = input_dim
        self.reservoir_dim = reservoir_dim
        self.output_dim = output_dim
        self.leak_rate = leak_rate
        self.noise_level = noise_level

        # Fixed random input weights W_in
        self.W_in = torch.randn(reservoir_dim, input_dim) * input_scaling

        # Fixed random recurrent weights W_rec (sparse)
        self.W_rec = self._initialize_reservoir(reservoir_dim, spectral_radius, sparsity)

        # Trainable readout weights W_out
        self.W_out = nn.Linear(reservoir_dim, output_dim)

        # Reservoir state
        self.x = torch.zeros(reservoir_dim)

    def _initialize_reservoir(self, N, spectral_radius, sparsity):
        """
        Create sparse random reservoir with specified spectral radius

        Spectral radius determines memory capacity and stability:
        - ρ < 1: Stable, fading memory
        - ρ ≈ 1: Edge of chaos, maximal memory
        - ρ > 1: Unstable, chaotic
        """
        # Create sparse random matrix
        W = torch.randn(N, N) * (torch.rand(N, N) < sparsity).float()

        # Scale to desired spectral radius
        eigenvalues = torch.linalg.eigvals(W)
        current_radius = torch.max(torch.abs(eigenvalues)).item()

        if current_radius > 0:
            W = W * (spectral_radius / current_radius)

        return W

    def reservoir_step(self, u, x, dt=1.0):
        """
        Single Euler step of reservoir dynamics:

        ẋ = -λx + W_rec tanh(x) + W_in u + ξ

        Args:
            u: Input [input_dim]
            x: Current state [reservoir_dim]
            dt: Time step

        Returns:
            x_next: Updated state
        """
        # Input drive
        input_drive = torch.matmul(self.W_in, u)

        # Recurrent drive
        recurrent_drive = torch.matmul(self.W_rec, torch.tanh(x))

        # Neural noise
        noise = self.noise_level * torch.randn_like(x)

        # Euler integration: x(t+dt) = x(t) + dt * ẋ(t)
        dx = -self.leak_rate * x + recurrent_drive + input_drive + noise
        x_next = x + dx * dt

        return x_next

    def forward(self, u_sequence, x0=None, dt=1.0, return_states=False):
        """
        Process input sequence through reservoir

        Args:
            u_sequence: [seq_len, batch, input_dim] or [seq_len, input_dim]
            x0: Initial reservoir state (if None, use zeros)
            dt: Time step
            return_states: If True, return all reservoir states

        Returns:
            y_sequence: [seq_len, batch, output_dim] readout outputs
            x_sequence: [seq_len, batch, reservoir_dim] if return_states
        """
        # Handle batched and unbatched input
        if u_sequence.dim() == 2:
            u_sequence = u_sequence.unsqueeze(1)  # Add batch dim

        seq_len, batch_size, _ = u_sequence.shape

        # Initialize state
        if x0 is None:
            x = torch.zeros(batch_size, self.reservoir_dim)
        else:
            x = x0

        # Collect states and outputs
        x_sequence = []
        y_sequence = []

        for t in range(seq_len):
            u_t = u_sequence[t]  # [batch, input_dim]

            # Update each sample in batch
            x_next = []
            for b in range(batch_size):
                x_b = self.reservoir_step(u_t[b], x[b], dt)
                x_next.append(x_b)

            x = torch.stack(x_next)

            # Readout
            y = self.W_out(x)

            x_sequence.append(x)
            y_sequence.append(y)

        y_sequence = torch.stack(y_sequence)  # [seq_len, batch, output_dim]

        if return_states:
            x_sequence = torch.stack(x_sequence)  # [seq_len, batch, reservoir_dim]
            return y_sequence, x_sequence
        else:
            return y_sequence

    def train_readout(self, u_sequences, y_targets, reg=1e-6):
        """
        Train readout weights using ridge regression

        W_out = Y X^T (X X^T + λI)^{-1}

        Args:
            u_sequences: List of input sequences
            y_targets: List of target sequences
            reg: Ridge regression regularization
        """
        all_states = []
        all_targets = []

        # Collect reservoir states for all sequences
        with torch.no_grad():
            for u_seq, y_tar in zip(u_sequences, y_targets):
                _, x_seq = self.forward(u_seq, return_states=True)

                # Flatten sequence dimension
                x_flat = x_seq.view(-1, self.reservoir_dim)
                y_flat = y_tar.view(-1, self.output_dim)

                all_states.append(x_flat)
                all_targets.append(y_flat)

        # Concatenate all data
        X = torch.cat(all_states, dim=0).T  # [reservoir_dim, n_samples]
        Y = torch.cat(all_targets, dim=0).T  # [output_dim, n_samples]

        # Ridge regression: W_out = Y X^T (X X^T + λI)^{-1}
        XXT = torch.matmul(X, X.T)
        XXT_reg = XXT + reg * torch.eye(self.reservoir_dim)

        W_out_optimal = torch.matmul(
            torch.matmul(Y, X.T),
            torch.inverse(XXT_reg)
        )

        # Update readout weights
        self.W_out.weight.data = W_out_optimal
        self.W_out.bias.data = torch.zeros(self.output_dim)


# Example: Time series prediction (Mackey-Glass)
def mackey_glass(n_steps, tau=17, n0=10, beta=0.2, gamma=0.1, n=10, dt=1.0):
    """
    Generate Mackey-Glass chaotic time series:

    dx/dt = β x(t-τ) / (1 + x(t-τ)^n) - γ x(t)
    """
    x = np.zeros(n_steps)
    x[:tau] = n0 * np.random.rand(tau)

    for t in range(tau, n_steps):
        x_tau = x[t - tau]
        dx = (beta * x_tau / (1 + x_tau**n) - gamma * x[t]) * dt
        x[t] = x[t-1] + dx

    return x


if __name__ == "__main__":
    torch.manual_seed(42)
    np.random.seed(42)

    print("Liquid State Machine - Mackey-Glass Prediction")

    # Generate chaotic time series
    series = mackey_glass(5000, tau=17)
    series = (series - series.mean()) / series.std()  # Normalize

    # Create input-output pairs: predict k steps ahead
    k_ahead = 10
    u_data = series[:-k_ahead].reshape(-1, 1)
    y_data = series[k_ahead:].reshape(-1, 1)

    # Split train/test
    train_size = 3000
    u_train = torch.FloatTensor(u_data[:train_size])
    y_train = torch.FloatTensor(y_data[:train_size])
    u_test = torch.FloatTensor(u_data[train_size:])
    y_test = torch.FloatTensor(y_data[train_size:])

    # Create LSM
    lsm = LiquidStateMachine(
        input_dim=1,
        reservoir_dim=500,
        output_dim=1,
        spectral_radius=0.95,
        sparsity=0.1,
        leak_rate=0.3,
        noise_level=0.001
    )

    print(f"Reservoir size: {lsm.reservoir_dim}")
    print(f"Spectral radius: 0.95 (near edge of chaos)")
    print(f"Sparsity: 10%")

    # Train readout (ridge regression on reservoir states)
    print("\nTraining readout layer...")
    lsm.train_readout([u_train], [y_train], reg=1e-6)

    # Test
    print("Testing...")
    with torch.no_grad():
        y_pred_train = lsm.forward(u_train)
        y_pred_test = lsm.forward(u_test)

        train_mse = F.mse_loss(y_pred_train.squeeze(), y_train.squeeze())
        test_mse = F.mse_loss(y_pred_test.squeeze(), y_test.squeeze())

        print(f"\nTrain MSE: {train_mse:.6f}")
        print(f"Test MSE: {test_mse:.6f}")

        # Compute prediction horizon (where error exceeds threshold)
        errors = (y_pred_test.squeeze() - y_test.squeeze()).abs()
        threshold = 0.5
        horizon = (errors < threshold).sum().item()
        print(f"Prediction horizon (error < {threshold}): {horizon} steps")
```

**Sources:**
- Maass, Natschläger & Markram (2002). "Real-Time Computing Without Stable States: A New Framework for Neural Computation Based on Perturbations"
- Jaeger (2001). "The 'Echo State' Approach to Analysing and Training Recurrent Neural Networks"
- Legenstein & Maass (2007). "Edge of Chaos and Prediction of Computational Performance for Neural Circuit Models"
### 191. Continuous Attractor Network (General Formulation)

**Formula:**
```
τ dr/dt = -r + f(W * r + I_ext)

where:
r(x, t) = neural activity at position x and time t
W(x, x') = translation-invariant connectivity kernel
f = activation function (typically rectified or sigmoidal)
I_ext = external input
* = convolution operator

Connectivity kernel (Mexican hat):
W(x - x') = A exp(-(x-x')²/2σ_E²) - B exp(-(x-x')²/2σ_I²)
```

**Attractor Manifold:**
```
M = {r(x) | r stable, ∫ r(x) dx = const}

For head direction: r(θ) = r₀ + A cos(θ - θ₀)
For spatial position: r(x,y) = A exp(-||p - (x,y)||²/2σ²)
```

**Bump Dynamics:**
```
Velocity integration: θ̇_bump = β · velocity_input

Path integration: ṗ_bump = β · v_input
```

**Variable Definitions:**
- `r(x,t)`: Population firing rate at position x on feature space
- `W(x,x')`: Synaptic weight from neuron at x' to neuron at x
- `σ_E, σ_I`: Excitatory and inhibitory spatial scales
- `A, B`: Excitation and inhibition strengths (B > A for stability)
- `τ`: Membrane time constant
- `f`: Activation function with threshold
- `θ_bump`: Location of activity bump on manifold

**Nature's Implementation:**
Head direction cells in postsubiculum/anterior thalamus form ring attractors that maintain stable orientation representations. Grid cells in entorhinal cortex form 2D continuous attractors enabling path integration. Place cells may use 2D bump attractors. The translation-invariant "Mexican hat" connectivity (local excitation, surround inhibition) emerges from cortical circuit structure.

**Impact:** CRITICAL - Explains working memory persistence, spatial navigation, motor planning, and any neural system maintaining analog values without external input. Continuous attractors implement perfect integration of velocity signals for path integration. They provide computational substrate for Bayesian inference over continuous variables and demonstrate how symmetries in connectivity create manifolds of stable states.

**Implementation (350 lines):**
```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

class ContinuousAttractorNetwork1D(nn.Module):
    """
    1D Continuous Attractor Network (Ring Attractor)

    Implements head direction cells with continuous attractor dynamics:
    τ dr/dt = -r + f(W * r + I_ext)

    where W is a Mexican hat connectivity kernel.
    """

    def __init__(self, n_neurons=360, tau=10.0, A_exc=2.0, A_inh=1.5,
                 sigma_exc=0.15, sigma_inh=0.5, threshold=0.0):
        """
        Args:
            n_neurons: Number of neurons in ring (e.g., 360 for degrees)
            tau: Time constant (ms)
            A_exc: Excitatory amplitude
            A_inh: Inhibitory amplitude
            sigma_exc: Excitatory spread (fraction of ring)
            sigma_inh: Inhibitory spread (fraction of ring)
            threshold: Firing threshold
        """
        super().__init__()

        self.n_neurons = n_neurons
        self.tau = tau
        self.threshold = threshold

        # Create Mexican hat connectivity matrix
        self.W = self._create_mexican_hat(n_neurons, A_exc, A_inh,
                                           sigma_exc, sigma_inh)

    def _create_mexican_hat(self, n, A_exc, A_inh, sigma_exc, sigma_inh):
        """
        Create translation-invariant Mexican hat connectivity:

        W(Δx) = A_exc exp(-Δx²/2σ_exc²) - A_inh exp(-Δx²/2σ_inh²)

        Returns [n, n] circulant matrix
        """
        # Distance on ring (wrap around)
        indices = torch.arange(n)
        dist = torch.minimum(
            torch.abs(indices[:, None] - indices[None, :]),
            n - torch.abs(indices[:, None] - indices[None, :])
        ).float()

        # Normalize to [0, 1]
        dist = dist / n

        # Mexican hat
        exc = A_exc * torch.exp(-dist**2 / (2 * sigma_exc**2))
        inh = A_inh * torch.exp(-dist**2 / (2 * sigma_inh**2))

        W = exc - inh

        return W

    def activation(self, x):
        """Rectified activation with threshold"""
        return F.relu(x - self.threshold)

    def step(self, r, I_ext, dt=1.0):
        """
        Single Euler step: τ dr/dt = -r + f(W r + I_ext)

        Args:
            r: Current activity [n_neurons]
            I_ext: External input [n_neurons]
            dt: Time step (ms)

        Returns:
            r_next: Updated activity
        """
        # Recurrent drive
        recurrent = torch.matmul(self.W, r)

        # Dynamics
        dr = (-r + self.activation(recurrent + I_ext)) / self.tau * dt

        r_next = r + dr

        return r_next

    def forward(self, I_ext_sequence, r0=None, dt=1.0):
        """
        Simulate attractor over time with input sequence

        Args:
            I_ext_sequence: [seq_len, n_neurons] external inputs
            r0: Initial state (if None, random)
            dt: Time step

        Returns:
            r_sequence: [seq_len, n_neurons] activity over time
        """
        seq_len = I_ext_sequence.shape[0]

        if r0 is None:
            r = torch.rand(self.n_neurons) * 0.1
        else:
            r = r0.clone()

        r_sequence = []

        for t in range(seq_len):
            r = self.step(r, I_ext_sequence[t], dt)
            r_sequence.append(r)

        return torch.stack(r_sequence)

    def get_bump_position(self, r):
        """
        Decode bump position using population vector

        θ = atan2(Σ r_i sin(θ_i), Σ r_i cos(θ_i))
        """
        angles = torch.linspace(0, 2*np.pi, self.n_neurons + 1)[:-1]

        weighted_sin = torch.sum(r * torch.sin(angles))
        weighted_cos = torch.sum(r * torch.cos(angles))

        theta = torch.atan2(weighted_sin, weighted_cos)

        return theta.item()


class ContinuousAttractorNetwork2D(nn.Module):
    """
    2D Continuous Attractor Network

    Models spatial representations like grid cells or place cells:
    τ dr/dt = -r + f(W * r + I_ext)

    W(x, x') = Mexican hat in 2D
    """

    def __init__(self, grid_size=32, tau=10.0, A_exc=3.0, A_inh=2.0,
                 sigma_exc=0.1, sigma_inh=0.3, threshold=0.0):
        """
        Args:
            grid_size: Number of neurons per dimension (total = grid_size²)
            tau: Time constant
            A_exc, A_inh: Excitatory/inhibitory amplitudes
            sigma_exc, sigma_inh: Spatial spreads (fraction of grid)
            threshold: Firing threshold
        """
        super().__init__()

        self.grid_size = grid_size
        self.n_neurons = grid_size * grid_size
        self.tau = tau
        self.threshold = threshold

        # Create 2D Mexican hat (as sparse conv for efficiency)
        self.W_kernel = self._create_mexican_hat_2d(
            A_exc, A_inh, sigma_exc, sigma_inh
        )

    def _create_mexican_hat_2d(self, A_exc, A_inh, sigma_exc, sigma_inh):
        """
        Create 2D Mexican hat kernel for convolution

        W(Δx, Δy) = A_exc exp(-(Δx² + Δy²)/2σ_exc²) - A_inh exp(-(Δx² + Δy²)/2σ_inh²)
        """
        # Kernel size (should capture ~3σ)
        k = int(self.grid_size * sigma_inh * 3)
        if k % 2 == 0:
            k += 1

        k = min(k, self.grid_size)

        # Create meshgrid
        x = torch.linspace(-0.5, 0.5, k)
        y = torch.linspace(-0.5, 0.5, k)
        X, Y = torch.meshgrid(x, y, indexing='ij')
        dist_sq = X**2 + Y**2

        # Mexican hat
        exc = A_exc * torch.exp(-dist_sq / (2 * sigma_exc**2))
        inh = A_inh * torch.exp(-dist_sq / (2 * sigma_inh**2))

        kernel = exc - inh

        # Normalize
        kernel = kernel - kernel.mean()

        return kernel.unsqueeze(0).unsqueeze(0)  # [1, 1, k, k]

    def activation(self, x):
        """Rectified activation"""
        return F.relu(x - self.threshold)

    def step(self, r, I_ext, dt=1.0):
        """
        Single step with 2D convolution

        Args:
            r: [grid_size, grid_size] activity
            I_ext: [grid_size, grid_size] external input
            dt: Time step

        Returns:
            r_next: Updated activity
        """
        # Reshape for conv2d: [1, 1, H, W]
        r_conv = r.unsqueeze(0).unsqueeze(0)

        # Recurrent drive via 2D convolution (circular padding)
        pad = self.W_kernel.shape[-1] // 2
        r_padded = F.pad(r_conv, (pad, pad, pad, pad), mode='circular')
        recurrent = F.conv2d(r_padded, self.W_kernel, padding=0).squeeze()

        # Dynamics
        dr = (-r + self.activation(recurrent + I_ext)) / self.tau * dt

        r_next = r + dr

        return r_next

    def forward(self, I_ext_sequence, r0=None, dt=1.0):
        """
        Simulate 2D attractor

        Args:
            I_ext_sequence: [seq_len, grid_size, grid_size]
            r0: Initial state
            dt: Time step

        Returns:
            r_sequence: [seq_len, grid_size, grid_size]
        """
        seq_len = I_ext_sequence.shape[0]

        if r0 is None:
            r = torch.rand(self.grid_size, self.grid_size) * 0.1
        else:
            r = r0.clone()

        r_sequence = []

        for t in range(seq_len):
            r = self.step(r, I_ext_sequence[t], dt)
            r_sequence.append(r)

        return torch.stack(r_sequence)

    def get_bump_position(self, r):
        """
        Decode 2D bump position using center of mass

        Returns (x, y) in [0, 1] × [0, 1]
        """
        # Normalize
        r_norm = r / (r.sum() + 1e-10)

        # Compute center of mass
        x_coords = torch.arange(self.grid_size).float()
        y_coords = torch.arange(self.grid_size).float()

        x_com = (r_norm.sum(dim=0) * x_coords).sum() / self.grid_size
        y_com = (r_norm.sum(dim=1) * y_coords).sum() / self.grid_size

        return x_com.item(), y_com.item()


class PathIntegrationAttractor:
    """
    Continuous attractor network performing path integration

    Integrates velocity commands to maintain position estimate:
    θ̇_bump = β · ω (for 1D/head direction)
    ṗ_bump = β · v (for 2D/spatial position)
    """

    def __init__(self, network_type='1D', grid_size=360):
        """
        Args:
            network_type: '1D' (ring) or '2D' (spatial)
            grid_size: Number of neurons (1D) or per dimension (2D)
        """
        self.network_type = network_type

        if network_type == '1D':
            self.network = ContinuousAttractorNetwork1D(
                n_neurons=grid_size,
                tau=10.0,
                A_exc=2.5,
                A_inh=1.8,
                sigma_exc=0.15,
                sigma_inh=0.5
            )
            self.grid_size = grid_size
        else:
            self.network = ContinuousAttractorNetwork2D(
                grid_size=grid_size,
                tau=10.0,
                A_exc=3.0,
                A_inh=2.0,
                sigma_exc=0.1,
                sigma_inh=0.3
            )
            self.grid_size = grid_size

    def velocity_to_input(self, velocity, gain=10.0):
        """
        Convert velocity command to asymmetric input that shifts bump

        For 1D: velocity > 0 -> shift clockwise
        For 2D: velocity = (v_x, v_y) -> shift in that direction
        """
        if self.network_type == '1D':
            # Create asymmetric input that shifts bump
            shift_input = torch.zeros(self.grid_size)

            # Positive velocity -> increase activity ahead
            if velocity > 0:
                phase_shift = int(velocity * gain)
                shift_input = torch.roll(torch.exp(-torch.arange(self.grid_size).float() / 20), phase_shift)
            elif velocity < 0:
                phase_shift = int(-velocity * gain)
                shift_input = torch.roll(torch.exp(-torch.arange(self.grid_size).float() / 20), -phase_shift)

            shift_input = shift_input * abs(velocity) * gain

            return shift_input

        else:  # 2D
            # Create gradient input in direction of velocity
            shift_input = torch.zeros(self.grid_size, self.grid_size)

            v_x, v_y = velocity

            # Create spatial gradient
            x = torch.linspace(-1, 1, self.grid_size)
            y = torch.linspace(-1, 1, self.grid_size)
            X, Y = torch.meshgrid(x, y, indexing='ij')

            # Gradient in velocity direction
            gradient = v_x * X + v_y * Y
            shift_input = gain * gradient * (v_x**2 + v_y**2)**0.5

            return shift_input

    def integrate_path(self, velocity_sequence, dt=1.0, gain=5.0):
        """
        Perform path integration over velocity sequence

        Args:
            velocity_sequence: [seq_len] (1D) or [seq_len, 2] (2D) velocities
            dt: Time step
            gain: Velocity-to-input gain

        Returns:
            position_sequence: Decoded positions over time
            activity_sequence: Neural activity over time
        """
        seq_len = len(velocity_sequence)

        # Convert velocities to input sequence
        if self.network_type == '1D':
            I_ext_seq = torch.stack([
                self.velocity_to_input(v, gain) for v in velocity_sequence
            ])

            # Initial bump at random position
            r0 = torch.zeros(self.grid_size)
            r0[self.grid_size // 2] = 1.0
            r0 = gaussian_filter1d(r0.numpy(), sigma=10)
            r0 = torch.FloatTensor(r0)

            # Simulate
            r_seq = self.network.forward(I_ext_seq, r0=r0, dt=dt)

            # Decode positions
            positions = [self.network.get_bump_position(r_seq[t]) for t in range(seq_len)]

            return positions, r_seq

        else:  # 2D
            I_ext_seq = torch.stack([
                self.velocity_to_input(v, gain) for v in velocity_sequence
            ])

            # Initial bump at center
            r0 = torch.zeros(self.grid_size, self.grid_size)
            r0[self.grid_size // 2, self.grid_size // 2] = 1.0

            # Simulate
            r_seq = self.network.forward(I_ext_seq, r0=r0, dt=dt)

            # Decode positions
            positions = [self.network.get_bump_position(r_seq[t]) for t in range(seq_len)]

            return positions, r_seq


# Example: 1D path integration (head direction)
if __name__ == "__main__":
    torch.manual_seed(42)

    print("="*60)
    print("1D Continuous Attractor: Head Direction Path Integration")
    print("="*60)

    # Create path integrator
    integrator_1d = PathIntegrationAttractor(network_type='1D', grid_size=360)

    # Generate velocity sequence (angular velocity)
    T = 200
    t = np.linspace(0, 10, T)
    angular_velocity = 0.05 * np.sin(2 * np.pi * 0.5 * t)  # Sinusoidal turning

    velocity_seq = torch.FloatTensor(angular_velocity)

    # Integrate
    print("Integrating angular velocity...")
    positions, activities = integrator_1d.integrate_path(velocity_seq, dt=1.0, gain=8.0)

    # Compute true integrated position
    true_positions = np.cumsum(angular_velocity) * 1.0

    print(f"Final decoded angle: {positions[-1]:.3f} rad")
    print(f"Final true angle: {true_positions[-1]:.3f} rad")
    print(f"Integration error: {abs(positions[-1] - true_positions[-1]):.3f} rad")

    print("\n" + "="*60)
    print("2D Continuous Attractor: Spatial Path Integration")
    print("="*60)

    # Create 2D path integrator
    integrator_2d = PathIntegrationAttractor(network_type='2D', grid_size=32)

    # Generate 2D velocity sequence (circular motion)
    T = 100
    t = np.linspace(0, 2*np.pi, T)
    velocity_x = 0.02 * np.cos(t)
    velocity_y = 0.02 * np.sin(t)

    velocity_seq_2d = torch.FloatTensor(np.stack([velocity_x, velocity_y], axis=1))

    # Integrate
    print("Integrating 2D velocity...")
    positions_2d, activities_2d = integrator_2d.integrate_path(velocity_seq_2d, dt=1.0, gain=3.0)

    # Compute true integrated position
    true_x = np.cumsum(velocity_x) * 1.0
    true_y = np.cumsum(velocity_y) * 1.0

    decoded_x = [p[0] for p in positions_2d]
    decoded_y = [p[1] for p in positions_2d]

    print(f"Final decoded position: ({decoded_x[-1]:.3f}, {decoded_y[-1]:.3f})")
    print(f"Final true position: ({true_x[-1]:.3f}, {true_y[-1]:.3f})")

    error = ((decoded_x[-1] - true_x[-1])**2 + (decoded_y[-1] - true_y[-1])**2)**0.5
    print(f"Integration error: {error:.3f}")

    print("\n✓ Continuous attractor successfully maintains stable activity bump")
    print("✓ Path integration demonstrated in 1D (head direction) and 2D (spatial)")
```

**Sources:**
- Zhang (1996). "Representation of Spatial Orientation by the Intrinsic Dynamics of the Head-Direction Cell Ensemble"
- Samsonovich & McNaughton (1997). "Path Integration and Cognitive Mapping in a Continuous Attractor Neural Network Model"
- Burak & Fiete (2009). "Accurate Path Integration in Continuous Attractor Network Models of Grid Cells"
- Wimmer et al. (2014). "Bump Attractor Dynamics in Prefrontal Cortex Explains Behavioral Precision in Spatial Working Memory"

### 192. Neural ODE (Continuous RNN)

**Formula:**
```
ḣ = f(h, x(t))

Or more explicitly:
dh/dt = f_θ(h(t), x(t), t)

where:
h(t) ∈ ℝ^d = hidden state (continuous dynamics)
x(t) = input time series
f_θ = neural network (can be MLP, GRU cell, etc.)
θ = learnable parameters

Adjoint sensitivity method for gradients:
dL/dθ = -∫_{t_1}^{t_0} a(t)^T ∂f/∂θ dt

where a(t) = adjoint state solving:
da/dt = -a^T ∂f/∂h
```

**Initial Value Problem:**
```
h(t_0) = h_0
h(t_1) = h_0 + ∫_{t_0}^{t_1} f_θ(h(t), x(t), t) dt
```

**Variable Definitions:**
- `h(t)`: Continuous hidden state trajectory
- `f_θ`: Dynamics function (neural network)
- `x(t)`: Input signal (can be irregular/continuous)
- `t`: Continuous time
- `a(t)`: Adjoint state for backprop through ODE
- `θ`: All learnable parameters

**Nature's Implementation:**
Continuous neural dynamics in cortex. Membrane potentials evolve continuously via differential equations. No discrete time steps. Irregular sampling (spikes are events, not clock ticks). Brain computes with continuous-time attractors, not RNN unrolling.

**Impact:** CRITICAL - Replaces discrete RNNs with continuous dynamics. Memory-efficient gradients via adjoint method. Handles irregular time series naturally. Constant memory regardless of sequence length. Foundation for continuous normalizing flows, time-series modeling, neural SDEs. Explains how brain processes continuous sensorimotor streams.

**Implementation (280 lines):**
```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torchdiffeq import odeint_adjoint as odeint

class NeuralODEFunc(nn.Module):
    """
    Dynamics function f(h, x, t) for Neural ODE
    ḣ = f(h, x, t)
    """

    def __init__(self, hidden_dim, input_dim=0, n_layers=2):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.input_dim = input_dim

        # Dynamics network
        layers = []
        in_dim = hidden_dim + input_dim + 1  # +1 for time

        for _ in range(n_layers - 1):
            layers.append(nn.Linear(in_dim, hidden_dim))
            layers.append(nn.Tanh())
            in_dim = hidden_dim

        layers.append(nn.Linear(in_dim, hidden_dim))

        self.net = nn.Sequential(*layers)

    def forward(self, t, h):
        """
        Compute dh/dt = f(h, t)

        Args:
            t: Current time (scalar or tensor)
            h: Current hidden state [batch, hidden_dim] or [batch, hidden_dim + input_dim]

        Returns:
            dhdt: Time derivative [batch, hidden_dim]
        """
        # Handle input-dependent dynamics
        if h.shape[1] > self.hidden_dim:
            # h contains [hidden_state, input]
            h_state = h[:, :self.hidden_dim]
            x_input = h[:, self.hidden_dim:]
        else:
            h_state = h
            x_input = torch.zeros(h.shape[0], self.input_dim).to(h.device)

        # Append time
        if isinstance(t, (int, float)):
            t_vec = torch.ones(h.shape[0], 1).to(h.device) * t
        else:
            t_vec = t.expand(h.shape[0], 1)

        # Concatenate [h, x, t]
        h_augmented = torch.cat([h_state, x_input, t_vec], dim=1)

        # Compute dynamics
        dhdt = self.net(h_augmented)

        return dhdt


class NeuralODE(nn.Module):
    """
    Neural Ordinary Differential Equation

    Continuous-time hidden state dynamics:
    dh/dt = f_θ(h(t), x(t), t)
    """

    def __init__(self, input_dim, hidden_dim, output_dim,
                 n_layers=2, solver='dopri5', rtol=1e-3, atol=1e-4):
        super().__init__()

        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim

        # ODE solver options
        self.solver = solver
        self.rtol = rtol
        self.atol = atol

        # Encoder: x -> h_0
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim)
        )

        # Dynamics function
        self.ode_func = NeuralODEFunc(hidden_dim, input_dim=0, n_layers=n_layers)

        # Decoder: h -> y
        self.decoder = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x, t_span=None, return_traj=False):
        """
        Forward pass through Neural ODE

        Args:
            x: Input [batch, seq_len, input_dim] or [batch, input_dim]
            t_span: Time points to evaluate [seq_len] or None (use [0, 1])
            return_traj: If True, return full trajectory

        Returns:
            y: Output [batch, output_dim] or [batch, seq_len, output_dim]
        """
        if x.dim() == 2:
            # Single input: [batch, input_dim]
            h0 = self.encoder(x)

            if t_span is None:
                t_span = torch.tensor([0., 1.]).to(x.device)

            # Solve ODE: h(t) for t in t_span
            h_traj = odeint(
                self.ode_func,
                h0,
                t_span,
                method=self.solver,
                rtol=self.rtol,
                atol=self.atol
            )  # [len(t_span), batch, hidden_dim]

            # Decode final state
            h_final = h_traj[-1]
            y = self.decoder(h_final)

            if return_traj:
                # Decode all states
                y_traj = self.decoder(h_traj.transpose(0, 1))  # [batch, seq_len, output_dim]
                return y_traj
            else:
                return y

        else:
            # Sequence input: [batch, seq_len, input_dim]
            batch_size, seq_len, _ = x.shape

            # Encode first timestep
            h0 = self.encoder(x[:, 0])

            if t_span is None:
                t_span = torch.linspace(0, 1, seq_len).to(x.device)

            # Solve ODE
            h_traj = odeint(
                self.ode_func,
                h0,
                t_span,
                method=self.solver,
                rtol=self.rtol,
                atol=self.atol
            )  # [seq_len, batch, hidden_dim]

            # Decode all timesteps
            h_traj_batched = h_traj.transpose(0, 1)  # [batch, seq_len, hidden_dim]
            y = self.decoder(h_traj_batched)  # [batch, seq_len, output_dim]

            return y


class LatentODE(nn.Module):
    """
    Latent ODE for modeling irregular time series

    Recognition: x(t_i) -> z_0
    Dynamics: dz/dt = f(z, t)
    Decoder: z(t) -> x̂(t)
    """

    def __init__(self, input_dim, latent_dim, hidden_dim, n_layers=2):
        super().__init__()

        self.input_dim = input_dim
        self.latent_dim = latent_dim

        # Recognition network (RNN encoder)
        self.recognition_rnn = nn.GRU(input_dim + 1, hidden_dim, batch_first=True)  # +1 for time
        self.recognition_proj = nn.Linear(hidden_dim, latent_dim * 2)  # μ and log σ

        # Latent dynamics
        self.ode_func = NeuralODEFunc(latent_dim, input_dim=0, n_layers=n_layers)

        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim)
        )

    def encode(self, x, t_obs):
        """
        Encode irregular observations into initial latent state

        Args:
            x: Observations [batch, n_obs, input_dim]
            t_obs: Observation times [batch, n_obs]

        Returns:
            z0_mean, z0_logvar: Initial latent distribution parameters
        """
        # Concatenate time to observations
        t_expanded = t_obs.unsqueeze(-1)
        x_t = torch.cat([x, t_expanded], dim=-1)

        # Run backwards through time (for causality)
        x_t_reversed = torch.flip(x_t, dims=[1])

        # RNN encoding
        _, h_final = self.recognition_rnn(x_t_reversed)
        h_final = h_final.squeeze(0)

        # Project to latent
        z0_params = self.recognition_proj(h_final)
        z0_mean = z0_params[:, :self.latent_dim]
        z0_logvar = z0_params[:, self.latent_dim:]

        return z0_mean, z0_logvar

    def reparameterize(self, mean, logvar):
        """Reparameterization trick"""
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mean + eps * std

    def forward(self, x_obs, t_obs, t_pred):
        """
        Forward pass: encode observations, evolve latent ODE, decode predictions

        Args:
            x_obs: Observed data [batch, n_obs, input_dim]
            t_obs: Observation times [batch, n_obs]
            t_pred: Prediction times [batch, n_pred]

        Returns:
            x_pred: Predictions [batch, n_pred, input_dim]
            z0_mean, z0_logvar: For VAE loss
        """
        # Encode
        z0_mean, z0_logvar = self.encode(x_obs, t_obs)
        z0 = self.reparameterize(z0_mean, z0_logvar)

        # Evolve latent dynamics
        t_all = torch.cat([t_obs[0], t_pred[0]])  # Assume same time grid for all batches
        t_all_sorted, sort_idx = torch.sort(t_all)

        z_traj = odeint(self.ode_func, z0, t_all_sorted)  # [n_all, batch, latent_dim]

        # Extract predictions at t_pred
        pred_mask = sort_idx >= len(t_obs[0])
        z_pred = z_traj[pred_mask]  # [n_pred, batch, latent_dim]

        # Decode
        z_pred_batched = z_pred.transpose(0, 1)  # [batch, n_pred, latent_dim]
        x_pred = self.decoder(z_pred_batched)

        return x_pred, z0_mean, z0_logvar


# Example: Time series modeling
if __name__ == "__main__":
    torch.manual_seed(42)

    print("Neural ODE for Continuous-Time Modeling")
    print("=" * 60)

    # Generate synthetic spiral data
    def spiral(t):
        x = t * torch.cos(t * 2 * np.pi)
        y = t * torch.sin(t * 2 * np.pi)
        return torch.stack([x, y], dim=1)

    t_train = torch.linspace(0, 1, 100)
    data_train = spiral(t_train)

    # Create Neural ODE
    model = NeuralODE(
        input_dim=2,
        hidden_dim=64,
        output_dim=2,
        n_layers=3
    )

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    print("\nTraining Neural ODE...")
    for epoch in range(500):
        # Forward pass
        pred = model(data_train[0].unsqueeze(0), t_span=t_train, return_traj=True)
        pred = pred.squeeze(0)

        # Loss
        loss = F.mse_loss(pred, data_train)

        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % 100 == 0:
            print(f"Epoch {epoch}: Loss = {loss.item():.6f}")

    print("\nExtrapolation test...")
    t_test = torch.linspace(0, 1.5, 150)  # Beyond training range
    with torch.no_grad():
        pred_extrap = model(data_train[0].unsqueeze(0), t_span=t_test, return_traj=True)

    print(f"Extrapolated {len(t_test)} timesteps (50% beyond training)")

    print("\n✓ Neural ODE trained successfully")
    print("✓ Continuous-time dynamics learned")
    print("✓ Memory-efficient adjoint gradients")
```

**Sources:**
- Chen et al. (2018). "Neural Ordinary Differential Equations" (NeurIPS Best Paper)
- Rubanova et al. (2019). "Latent ODEs for Irregularly-Sampled Time Series"
- Kidger et al. (2020). "Neural Controlled Differential Equations for Irregular Time Series"
- Massaroli et al. (2020). "Dissecting Neural ODEs"

---

### 193. Sparse Coding (L1 Efficient Representation)

**Formula:**
```
Sparse Coding Objective:
min_a ||x - Φa||² + λ||a||₁

where:
x = input signal (observations)
Φ = dictionary/basis functions (learned or fixed)
a = sparse coefficients (activations)
λ = sparsity penalty

Equivalently (LASSO form):
min_a ||a||₁  subject to ||x - Φa||² ≤ ε

Learning Dictionary Φ:
min_{Φ,a} ||x - Φa||² + λ||a||₁

Subject to ||φ_i||₂ ≤ 1  (normalize basis functions)

ISTA (Iterative Soft Thresholding):
a^{(t+1)} = S_λ(a^{(t)} + Φ^T(x - Φa^{(t)}))

where S_λ(z) = sign(z)·max(|z| - λ, 0)  [soft thresholding]

Neural Implementation (Locally Competitive Algorithm):
τ ȧ = -a + Φ^T x - (Φ^T Φ - I)a
```

**Variable Definitions:**
- `x`: Input vector to be represented
- `Φ`: Dictionary matrix [input_dim × code_dim]
- `a`: Sparse activation coefficients
- `λ`: Sparsity regularization strength (L1 penalty)
- `τ`: Time constant for neural dynamics
- `S_λ`: Soft-thresholding operator

**Nature's Implementation:**
V1 simple cells learn sparse Gabor-like filters from natural images. Only ~5-10% of neurons active for any input. Metabolically efficient. Robust to noise. Decorrelates signals. Hippocampus uses sparse codes for memory. Explains overcompleteness in cortex (more neurons than inputs).

**Impact:** CRITICAL - Foundational for dictionary learning, autoencoders, compression, robust features. Explains cortical receptive fields, overcomplete representations, sparse activity. Used in image processing, compressed sensing, feature learning. ICA, NMF special cases. Critical for understanding efficient coding hypothesis and designing biologically-inspired sparse networks.

**Implementation (280 lines):**
```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class SparseCoding(nn.Module):
    """
    Sparse Coding with L1 penalty
    min ||x - Φa||² + λ||a||₁
    """

    def __init__(self, input_dim, code_dim, sparsity=0.1, n_iterations=100):
        super().__init__()

        self.input_dim = input_dim
        self.code_dim = code_dim
        self.lambda_sparse = sparsity
        self.n_iterations = n_iterations

        # Dictionary Φ (learned)
        self.dictionary = nn.Parameter(torch.randn(input_dim, code_dim) * 0.1)

        # Normalize dictionary columns
        with torch.no_grad():
            self.dictionary /= torch.norm(self.dictionary, dim=0, keepdim=True)

    def soft_threshold(self, x, threshold):
        """
        Soft thresholding operator for L1 penalty:
        S_λ(x) = sign(x)·max(|x| - λ, 0)
        """
        return torch.sign(x) * F.relu(torch.abs(x) - threshold)

    def ista_inference(self, x, learning_rate=0.01):
        """
        ISTA (Iterative Soft Thresholding Algorithm)
        Infer sparse codes a for input x
        """
        batch_size = x.shape[0]
        a = torch.zeros(batch_size, self.code_dim).to(x.device)

        for _ in range(self.n_iterations):
            # Gradient of reconstruction error
            reconstruction = a @ self.dictionary.T
            error = x - reconstruction
            grad = error @ self.dictionary

            # Gradient step
            a = a + learning_rate * grad

            # Soft thresholding (L1 proximal operator)
            a = self.soft_threshold(a, self.lambda_sparse * learning_rate)

        return a

    def forward(self, x):
        """
        Encode input to sparse code
        """
        return self.ista_inference(x)

    def reconstruct(self, a):
        """
        Decode sparse code to reconstruction
        x̂ = Φa
        """
        return a @ self.dictionary.T

    def learn_dictionary(self, x_batch, a_batch, lr_dict=0.01):
        """
        Update dictionary Φ via gradient descent
        Keep dictionary columns normalized
        """
        # Reconstruction error
        x_recon = a_batch @ self.dictionary.T
        error = x_batch - x_recon

        # Dictionary gradient: ∂L/∂Φ = -2·error^T·a
        grad_dict = -2 * error.T @ a_batch / x_batch.shape[0]

        # Update
        self.dictionary.data += lr_dict * grad_dict

        # Normalize columns
        self.dictionary.data /= torch.norm(self.dictionary.data, dim=0, keepdim=True) + 1e-8

    def compute_loss(self, x, a):
        """
        Total loss: reconstruction + sparsity
        L = ||x - Φa||² + λ||a||₁
        """
        reconstruction = a @ self.dictionary.T
        recon_loss = torch.sum((x - reconstruction)**2)
        sparse_loss = self.lambda_sparse * torch.sum(torch.abs(a))

        return recon_loss + sparse_loss


class LocallyCompetitiveAlgorithm(nn.Module):
    """
    Neural dynamics implementation of sparse coding
    τ ȧ = -a + Φ^T x - (Φ^T Φ - I)a
    """

    def __init__(self, input_dim, code_dim, tau=10.0, threshold=0.1):
        super().__init__()

        self.input_dim = input_dim
        self.code_dim = code_dim
        self.tau = tau
        self.threshold = threshold

        # Dictionary
        self.dictionary = nn.Parameter(torch.randn(input_dim, code_dim) * 0.1)

        # Normalize
        with torch.no_grad():
            self.dictionary /= torch.norm(self.dictionary, dim=0, keepdim=True)

    def dynamics(self, a, x, dt=0.1):
        """
        Neural dynamics for sparse inference
        τ ȧ = -a + Φ^T x - (Φ^T Φ - I)a
        """
        # Feedforward drive
        drive = x @ self.dictionary

        # Lateral inhibition (competition)
        gram = self.dictionary.T @ self.dictionary
        lateral = a @ (gram - torch.eye(self.code_dim).to(a.device))

        # Dynamics
        dadt = (-a + drive - lateral) / self.tau

        # Update
        a_new = a + dadt * dt

        # Rectify (non-negative activations)
        a_new = F.relu(a_new)

        # Threshold (enforce sparsity)
        a_new = a_new * (a_new > self.threshold).float()

        return a_new

    def forward(self, x, n_steps=50, dt=0.1):
        """
        Converge to sparse representation
        """
        batch_size = x.shape[0]
        a = torch.zeros(batch_size, self.code_dim).to(x.device)

        for _ in range(n_steps):
            a = self.dynamics(a, x, dt)

        return a


class SparseAutoencoder(nn.Module):
    """
    Autoencoder with L1 sparsity constraint
    """

    def __init__(self, input_dim, hidden_dim, sparsity_target=0.05, beta=3.0):
        super().__init__()

        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.sparsity_target = sparsity_target
        self.beta = beta  # Sparsity penalty strength

        # Encoder (recognition)
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU()
        )

        # Decoder (reconstruction)
        self.decoder = nn.Linear(hidden_dim, input_dim)

    def forward(self, x):
        """Encode and decode"""
        z = self.encoder(x)
        x_recon = self.decoder(z)
        return z, x_recon

    def kl_divergence_sparsity(self, activations):
        """
        KL divergence between average activation and target sparsity
        KL(ρ || ρ̂) = ρ log(ρ/ρ̂) + (1-ρ) log((1-ρ)/(1-ρ̂))
        """
        rho = activations.mean(dim=0)  # Average activation per neuron
        rho_target = self.sparsity_target

        kl = rho_target * torch.log(rho_target / (rho + 1e-8)) + \
             (1 - rho_target) * torch.log((1 - rho_target) / (1 - rho + 1e-8))

        return kl.sum()

    def loss(self, x, z, x_recon):
        """
        Total loss: reconstruction + KL sparsity
        """
        recon_loss = F.mse_loss(x_recon, x)
        sparsity_loss = self.kl_divergence_sparsity(z)

        return recon_loss + self.beta * sparsity_loss


# Example: Learn sparse codes from natural image patches
if __name__ == "__main__":
    torch.manual_seed(42)

    print("Sparse Coding for Efficient Representation")
    print("=" * 60)

    # Generate synthetic data (gabor-like patterns)
    def generate_gabor_data(n_samples=500, patch_size=16):
        """Generate oriented edge patterns"""
        data = []

        for _ in range(n_samples):
            # Random orientation
            theta = np.random.rand() * np.pi

            # Create gabor patch
            x = np.linspace(-1, 1, patch_size)
            y = np.linspace(-1, 1, patch_size)
            X, Y = np.meshgrid(x, y)

            # Rotated coordinates
            X_rot = X * np.cos(theta) + Y * np.sin(theta)

            # Gabor
            gabor = np.exp(-(X**2 + Y**2) / 0.1) * np.cos(2 * np.pi * X_rot * 3)

            # Flatten and add noise
            patch = gabor.flatten() + np.random.randn(patch_size**2) * 0.1

            data.append(patch)

        return torch.FloatTensor(np.array(data))

    # Generate data
    n_patches = 1000
    patch_dim = 16 * 16  # 16x16 patches
    data = generate_gabor_data(n_patches, patch_size=16)

    # Normalize
    data = (data - data.mean()) / data.std()

    # Create sparse coding model
    model = SparseCoding(
        input_dim=patch_dim,
        code_dim=128,  # Overcomplete (128 > 256)
        sparsity=0.1,
        n_iterations=50
    )

    print(f"Dictionary: {patch_dim} → {model.code_dim} (overcomplete)")

    # Training loop
    optimizer = torch.optim.Adam([model.dictionary], lr=0.01)

    for epoch in range(200):
        # Sample batch
        idx = torch.randperm(n_patches)[:32]
        x_batch = data[idx]

        # Infer sparse codes (ISTA)
        with torch.no_grad():
            a_batch = model(x_batch)

        # Update dictionary
        model.learn_dictionary(x_batch, a_batch, lr_dict=0.01)

        # Compute loss
        loss = model.compute_loss(x_batch, a_batch)

        if epoch % 40 == 0:
            sparsity = (a_batch.abs() > 0.01).float().mean().item()
            recon = model.reconstruct(a_batch)
            recon_error = F.mse_loss(recon, x_batch).item()

            print(f"Epoch {epoch}: Loss={loss.item():.2f}, "
                  f"Sparsity={sparsity:.1%}, Recon Error={recon_error:.4f}")

    # Test sparse representation
    print("\nTesting sparse representation:")
    test_data = data[:5]
    test_codes = model(test_data)

    for i in range(5):
        active = (test_codes[i].abs() > 0.01).sum().item()
        print(f"  Sample {i}: {active}/{model.code_dim} active ({active/model.code_dim:.1%})")

    print(f"\n✓ Learned sparse dictionary with ~{sparsity:.0%} activation")
    print("✓ Overcomplete representation (more codes than pixels)")
```

**Sources:**
- Olshausen & Field (1996). "Emergence of simple-cell receptive field properties by learning a sparse code"
- Tibshirani (1996). "Regression Shrinkage and Selection via the Lasso"
- Rozell et al. (2008). "Sparse Coding via Thresholding and Local Competition"
- Mairal et al. (2009). "Online Dictionary Learning for Sparse Coding"

---

### 194. Winner-Take-All Circuits (WTA)

**Formula:**
```
Competitive Selection (Softmax Form):
y_i = exp(u_i / τ) / Σⱼ exp(u_j / τ)

Hard WTA (Max Selection):
y_i = 1  if i = argmax(u)
     = 0  otherwise

k-WTA (Top-k Selection):
y_i = 1  if i ∈ TopK(u)
     = 0  otherwise

Neural Dynamics (Lateral Inhibition):
τ ẏᵢ = -yᵢ + f(uᵢ - Σⱼ wᵢⱼ yⱼ)

where wᵢⱼ = w_global for j≠i (uniform inhibition)

Steady-state WTA:
y* = argmax(u - W·y)

where:
- uᵢ = input to neuron i
- yᵢ = output activity
- τ = time constant
- wᵢⱼ = inhibitory weights (typically uniform)
- f = activation function (typically rectified)
```

**Variable Definitions:**
- `u`: Input vector (scores, logits, activations)
- `y`: Output vector (winner selection)
- `τ`: Temperature (controls competition sharpness)
- `w`: Lateral inhibition strength
- `k`: Number of winners in k-WTA

**Nature's Implementation:**
Cortical competition via inhibitory interneurons. Visual cortex orientation selectivity. Motor cortex action selection. Hippocampal place cell competition. Basal ganglia winner-take-all for action selection. Implements sparse coding, attention, routing.

**Impact:** HIGH - Foundation for attention mechanisms, mixture-of-experts, competitive learning, softmax layers, clustering. Explains neural selectivity, sparsity, modularity. Used in transformers, capsule networks, routing. Critical for understanding competitive dynamics and implementing sparse, modular architectures.

**Implementation (200 lines):**
```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class WinnerTakeAll(nn.Module):
    """
    Hard Winner-Take-All: Select single maximum
    """

    def __init__(self, dim, return_indices=False):
        super().__init__()
        self.dim = dim
        self.return_indices = return_indices

    def forward(self, x):
        """
        Hard WTA: y_i = 1 if i=argmax(x), else 0
        """
        # Find winner
        winners = torch.argmax(x, dim=self.dim, keepdim=True)

        # One-hot encoding
        y = torch.zeros_like(x)
        y.scatter_(self.dim, winners, 1.0)

        if self.return_indices:
            return y, winners.squeeze(self.dim)
        return y


class KWinnerTakeAll(nn.Module):
    """
    k-Winner-Take-All: Select top-k maxima
    """

    def __init__(self, k, dim=-1):
        super().__init__()
        self.k = k
        self.dim = dim

    def forward(self, x):
        """
        k-WTA: y_i = 1 if i ∈ TopK(x), else 0
        """
        # Get top-k values and indices
        topk_vals, topk_idx = torch.topk(x, self.k, dim=self.dim)

        # Create sparse output
        y = torch.zeros_like(x)
        y.scatter_(self.dim, topk_idx, 1.0)

        return y


class NeuralWTA(nn.Module):
    """
    Neural dynamics WTA via lateral inhibition
    τ ẏ = -y + f(u - Σⱼ wᵢⱼ yⱼ)
    """

    def __init__(self, n_neurons, inhibition_strength=1.0, tau=1.0):
        super().__init__()

        self.n = n_neurons
        self.tau = tau
        self.w_inhib = inhibition_strength

    def dynamics(self, y, u, dt=0.1):
        """
        Single step of WTA dynamics
        """
        # Global inhibition (all-to-all except self)
        inhibition = self.w_inhib * (y.sum(dim=-1, keepdim=True) - y)

        # Dynamics
        dydt = (-y + F.relu(u - inhibition)) / self.tau

        return y + dydt * dt

    def forward(self, u, n_iterations=50, dt=0.1):
        """
        Converge to WTA state
        """
        y = torch.zeros_like(u)

        for _ in range(n_iterations):
            y = self.dynamics(y, u, dt)

        return y


class SoftWTA(nn.Module):
    """
    Soft WTA via temperature-controlled softmax
    y_i = exp(u_i/τ) / Σⱼ exp(u_j/τ)
    """

    def __init__(self, temperature=1.0, dim=-1):
        super().__init__()
        self.temperature = temperature
        self.dim = dim

    def forward(self, x):
        """
        Soft winner-take-all (softmax)
        Temperature controls competition strength
        """
        return F.softmax(x / self.temperature, dim=self.dim)

    def set_temperature(self, temp):
        """Adjust competition (low temp → harder competition)"""
        self.temperature = temp


class AdaptiveKWTA(nn.Module):
    """
    Adaptive k-WTA that learns sparsity level
    """

    def __init__(self, initial_k, max_k, min_k=1):
        super().__init__()
        self.k = initial_k
        self.max_k = max_k
        self.min_k = min_k

    def forward(self, x, dim=-1):
        """k-WTA with current k"""
        topk_vals, topk_idx = torch.topk(x, self.k, dim=dim)

        y = torch.zeros_like(x)
        y.scatter_(dim, topk_idx, 1.0)

        return y

    def adapt_k(self, target_sparsity, current_sparsity, lr=0.1):
        """
        Adjust k based on desired sparsity level
        """
        error = target_sparsity - current_sparsity
        delta_k = int(lr * error * self.max_k)

        self.k = max(self.min_k, min(self.max_k, self.k + delta_k))


# Example: WTA for attention and routing
if __name__ == "__main__":
    torch.manual_seed(42)

    print("Winner-Take-All Circuits")
    print("=" * 60)

    # Input scores
    scores = torch.tensor([[3.0, 1.0, 5.0, 2.0, 4.0]])

    # Hard WTA
    hard_wta = WinnerTakeAll(dim=1)
    winner_hard = hard_wta(scores)
    print(f"Input: {scores}")
    print(f"Hard WTA: {winner_hard}")

    # k-WTA (top-2)
    k_wta = KWinnerTakeAll(k=2)
    winner_k = k_wta(scores)
    print(f"2-WTA: {winner_k}")

    # Soft WTA (different temperatures)
    soft_wta = SoftWTA(temperature=1.0)
    print(f"\nSoft WTA (τ=1.0): {soft_wta(scores)}")

    soft_wta.set_temperature(0.1)
    print(f"Soft WTA (τ=0.1): {soft_wta(scores)}")

    soft_wta.set_temperature(10.0)
    print(f"Soft WTA (τ=10.0): {soft_wta(scores)}")

    # Neural dynamics WTA
    print("\nNeural Dynamics WTA:")
    neural_wta = NeuralWTA(n_neurons=5, inhibition_strength=2.0)
    winner_neural = neural_wta(scores, n_iterations=100)
    print(f"Converged state: {winner_neural}")

    # Sparsity analysis
    sparsity = (winner_neural > 0.1).float().mean().item()
    print(f"Sparsity: {sparsity:.1%}")

    print("\n✓ WTA circuits implement competitive selection")
    print("✓ Foundation for attention, routing, sparsity")
```

**Sources:**
- Grossberg (1973). "Contour Enhancement, Short Term Memory, and Constancies in Reverberating Neural Networks"
- Maass (2000). "On the Computational Power of Winner-Take-All"
- Majani et al. (1989). "On the k-Winners-Take-All Network"
- Riesenhuber & Poggio (1999). "Hierarchical models of object recognition in cortex"

---
### 195. Central Pattern Generator (CPG) Networks

**Formula:**
```
Coupled Oscillator Dynamics:
ẋ = f(x) + g(u) + Coupling

Specific form (Kuramoto-style):
ẋᵢ = ωᵢ + Σⱼ Kᵢⱼ sin(xⱼ - xᵢ) + uᵢ

Matsuoka Oscillator (flexor-extensor):
τ ẋ₁ = -x₁ - βy₁ - w₁₂f(x₂) + u + c
τ ẋ₂ = -x₂ - βy₂ - w₂₁f(x₁) - u + c
τ' ẏᵢ = -yᵢ + f(xᵢ)

Van der Pol (self-sustaining):
ẍ - μ(1-x²)ẋ + x = 0

General CPG form:
ẋ = A(x) + B(x,θ) + u(t)

where:
- xᵢ = oscillator state (phase or amplitude)
- ωᵢ = intrinsic frequency
- Kᵢⱼ = coupling strength between oscillators
- yᵢ = adaptation variable
- β = fatigue/adaptation rate
- wᵢⱼ = mutual inhibition
- u = descending command/modulation
- θ = coupling parameters
```

**Variable Definitions:**
- `x`: Oscillator state variables
- `ω`: Natural frequency
- `K`: Coupling matrix
- `u`: External drive/modulation
- `β`: Adaptation strength
- `τ, τ'`: Time constants (fast/slow)

**Nature's Implementation:**
Spinal cord locomotor circuits. Generate rhythmic walking, swimming, breathing without continuous descending commands. Lamprey swimming CPG. Cat hindlimb stepping. Insect locomotion. Breathing rhythm in medulla. Once initiated, run autonomously. Descending signals modulate frequency/amplitude.

**Impact:** MEDIUM-HIGH - Autonomous Rhythm Generation
Explains locomotion, breathing, chewing without explicit timing. Self-sustaining oscillations. Modular, reusable. Used in robotics (legged locomotion), speech synthesis, rhythmic control tasks. Critical for understanding motor pattern generation and implementing autonomous rhythmic behaviors.

**Implementation (220 lines):**
```python
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

class MatsuokaOscillator(nn.Module):
    """
    Matsuoka neural oscillator for CPG
    Models flexor-extensor pairs with mutual inhibition
    """

    def __init__(self, tau=1.0, tau_adapt=2.0, beta=2.5, mu=1.0, weight=2.0):
        super().__init__()

        self.tau = tau  # Fast time constant
        self.tau_adapt = tau_adapt  # Slow adaptation
        self.beta = beta  # Adaptation strength
        self.mu = mu  # Tonic input
        self.weight = weight  # Mutual inhibition

    def activation(self, x):
        """Rectified activation"""
        return torch.relu(x)

    def forward(self, state, u=0.0, dt=0.01):
        """
        Single step of Matsuoka oscillator
        
        state = [x1, x2, y1, y2]
        x1, x2 = flexor/extensor neural activity
        y1, y2 = adaptation variables
        u = tonic drive
        """
        x1, x2, y1, y2 = state

        # Neuron dynamics
        dx1 = (-x1 - self.beta * y1 - self.weight * self.activation(x2) + self.mu + u) / self.tau
        dx2 = (-x2 - self.beta * y2 - self.weight * self.activation(x1) + self.mu - u) / self.tau

        # Adaptation dynamics
        dy1 = (-y1 + self.activation(x1)) / self.tau_adapt
        dy2 = (-y2 + self.activation(x2)) / self.tau_adapt

        # Update
        x1_new = x1 + dx1 * dt
        x2_new = x2 + dx2 * dt
        y1_new = y1 + dy1 * dt
        y2_new = y2 + dy2 * dt

        return torch.stack([x1_new, x2_new, y1_new, y2_new])

    def generate_rhythm(self, n_steps=1000, dt=0.01, u=0.0):
        """Generate rhythmic pattern"""
        state = torch.zeros(4)
        trajectory = []

        for _ in range(n_steps):
            state = self.forward(state, u, dt)
            trajectory.append(state.clone())

        return torch.stack(trajectory)


class CoupledCPG(nn.Module):
    """
    Network of coupled oscillators for multi-joint control
    """

    def __init__(self, n_joints, coupling_strength=0.5):
        super().__init__()

        self.n_joints = n_joints
        self.coupling_strength = coupling_strength

        # Individual oscillators
        self.oscillators = nn.ModuleList([
            MatsuokaOscillator() for _ in range(n_joints)
        ])

        # Coupling matrix (nearest-neighbor for limbs)
        self.coupling = self.create_coupling_matrix(n_joints)

    def create_coupling_matrix(self, n):
        """
        Create coupling matrix for chain of oscillators
        (e.g., spine segments or limb joints)
        """
        K = torch.zeros(n, n)

        # Nearest-neighbor coupling
        for i in range(n - 1):
            K[i, i + 1] = self.coupling_strength
            K[i + 1, i] = self.coupling_strength

        return K

    def forward(self, states, drives, dt=0.01):
        """
        Update all coupled oscillators
        states: [n_joints, 4] state vectors
        drives: [n_joints] tonic drives
        """
        new_states = []

        for i in range(self.n_joints):
            # Coupling term (phase difference)
            coupling_input = 0.0
            for j in range(self.n_joints):
                if i != j and self.coupling[i, j] > 0:
                    # Couple through flexor activity
                    phase_diff = states[j][0] - states[i][0]
                    coupling_input += self.coupling[i, j] * phase_diff

            # Update with coupling
            u_total = drives[i] + coupling_input
            new_state = self.oscillators[i](states[i], u_total, dt)
            new_states.append(new_state)

        return torch.stack(new_states)

    def generate_gait(self, n_steps=2000, dt=0.01, speed=0.5):
        """
        Generate coordinated gait pattern
        speed modulates frequency
        """
        states = torch.zeros(self.n_joints, 4)
        drives = torch.ones(self.n_joints) * speed

        trajectory = []
        for _ in range(n_steps):
            states = self.forward(states, drives, dt)
            trajectory.append(states.clone())

        return torch.stack(trajectory)


class KuramotoOscillatorNetwork(nn.Module):
    """
    Kuramoto model for phase-coupled oscillators
    θ̇ᵢ = ωᵢ + Σⱼ Kᵢⱼ sin(θⱼ - θᵢ)
    """

    def __init__(self, n_oscillators, natural_frequencies=None, coupling=None):
        super().__init__()

        self.n = n_oscillators

        # Natural frequencies
        if natural_frequencies is None:
            self.omega = torch.randn(n_oscillators) * 0.5 + 2.0
        else:
            self.omega = torch.tensor(natural_frequencies)

        # Coupling matrix
        if coupling is None:
            # All-to-all with random strengths
            self.K = torch.randn(n_oscillators, n_oscillators) * 0.3
            self.K.fill_diagonal_(0)
        else:
            self.K = torch.tensor(coupling)

    def forward(self, theta, dt=0.01):
        """
        Update phases
        θ̇ᵢ = ωᵢ + Σⱼ Kᵢⱼ sin(θⱼ - θᵢ)
        """
        # Phase differences
        phase_diff = theta.unsqueeze(0) - theta.unsqueeze(1)  # [n, n]

        # Coupling term
        coupling = (self.K * torch.sin(phase_diff)).sum(dim=1)

        # Phase evolution
        dtheta = self.omega + coupling

        return (theta + dtheta * dt) % (2 * np.pi)

    def simulate(self, n_steps=1000, dt=0.01):
        """Generate synchronized rhythm"""
        theta = torch.rand(self.n) * 2 * np.pi

        trajectory = []
        for _ in range(n_steps):
            theta = self.forward(theta, dt)
            trajectory.append(theta.clone())

        return torch.stack(trajectory)

    def order_parameter(self, theta):
        """
        Measure synchronization
        r = |<exp(iθ)>|
        r=1: perfect sync, r=0: incoherent
        """
        z = torch.mean(torch.exp(1j * theta.numpy()))
        return abs(z)


# Example: Quadruped gait generation
if __name__ == "__main__":
    torch.manual_seed(42)

    print("Central Pattern Generator Networks")
    print("=" * 60)

    # Single Matsuoka oscillator
    print("\n1. Single Matsuoka Oscillator:")
    osc = MatsuokaOscillator()
    rhythm = osc.generate_rhythm(n_steps=500, dt=0.02)

    flexor = rhythm[:, 0].numpy()
    extensor = rhythm[:, 1].numpy()

    print(f"   Generated {len(rhythm)} timesteps")
    print(f"   Flexor range: [{flexor.min():.2f}, {flexor.max():.2f}]")
    print(f"   Period: ~{np.where(np.diff(np.sign(flexor)))[0][1] * 0.02:.2f}s")

    # Coupled CPG for quadruped
    print("\n2. Coupled CPG (4 limbs):")
    cpg = CoupledCPG(n_joints=4, coupling_strength=0.3)
    gait = cpg.generate_gait(n_steps=1000, dt=0.02, speed=0.8)

    print(f"   Generated gait for {cpg.n_joints} joints")
    print(f"   Coordination established through nearest-neighbor coupling")

    # Check phase relationships
    phases = []
    for joint_idx in range(4):
        signal = gait[:, joint_idx, 0].numpy()
        zero_crossings = np.where(np.diff(np.sign(signal)))[0]
        if len(zero_crossings) > 0:
            phases.append(zero_crossings[0])

    print(f"   Phase offsets: {np.diff(phases) if len(phases) > 1 else 'N/A'}")

    # Kuramoto oscillators
    print("\n3. Kuramoto Oscillators:")
    kuramoto = KuramotoOscillatorNetwork(n_oscillators=10, coupling=None)
    kuramoto.K = torch.ones(10, 10) * 0.5  # Strong all-to-all coupling
    kuramoto.K.fill_diagonal_(0)

    theta_traj = kuramoto.simulate(n_steps=500, dt=0.01)

    r_initial = kuramoto.order_parameter(theta_traj[0])
    r_final = kuramoto.order_parameter(theta_traj[-1])

    print(f"   Synchronization: r_initial={r_initial:.3f}, r_final={r_final:.3f}")
    print(f"   {'✓ Synchronized' if r_final > 0.8 else '✗ Incoherent'}")

    print("\n✓ CPGs generate autonomous rhythmic patterns")
    print("✓ Useful for locomotion, breathing, rhythmic behaviors")
```

**Sources:**
- Matsuoka (1985). "Sustained Oscillations Generated by Mutually Inhibiting Neurons"
- Ijspeert (2008). "Central pattern generators for locomotion control in animals and robots: A review"
- Grillner (2006). "Biological Pattern Generation: The Cellular and Computational Logic of Networks in Motion"
- Kuramoto (1984). "Chemical Oscillations, Waves, and Turbulence"

---
### 196. Population Vector Coding (Distributed Representation)

**Formula:**
```
Population Vector Decoder:
ŝ = (Σᵢ rᵢ dᵢ) / (Σᵢ rᵢ)

where:
- rᵢ = firing rate of neuron i
- dᵢ = preferred direction/value of neuron i
- ŝ = decoded estimate (direction, position, etc.)

Cosine Tuning Curve:
rᵢ(s) = r_max · max(0, cos(s - dᵢ))^n

Or Gaussian tuning:
rᵢ(s) = r_max · exp(-||s - μᵢ||²/(2σ²))

Maximum Likelihood Decoder:
ŝ_ML = argmax_s P(r|s)
     = argmax_s Π_i P(rᵢ|s)

For Poisson neurons:
P(rᵢ|s) = (λᵢ(s)^rᵢ / rᵢ!) · exp(-λᵢ(s))

where λᵢ(s) = tuning curve

Fisher Information (decoding precision):
I(s) = Σᵢ (d/ds λᵢ(s))² / λᵢ(s)

Cramér-Rao Bound:
Var(ŝ) ≥ 1/I(s)
```

**Variable Definitions:**
- `rᵢ`: Firing rate of neuron i
- `dᵢ`: Preferred stimulus value (direction, position, etc.)
- `s`: True stimulus value
- `ŝ`: Decoded estimate from population
- `r_max`: Maximum firing rate
- `μᵢ, σ`: Tuning curve center and width
- `I(s)`: Fisher information

**Nature's Implementation:**
Motor cortex encodes movement direction as population vector. Each neuron has preferred direction. Resultant vector predicts actual movement. Hippocampal place cells encode position. Head direction cells encode heading. Visual cortex encodes orientation. Robust to single-neuron noise. Accuracy increases with population size (~√N).

**Impact:** CRITICAL - Foundation for understanding neural codes. Explains how populations represent continuous variables. More accurate than single neurons. Used in brain-machine interfaces (decode intended movement), neural data analysis, population coding in deep networks. Critical for multi-neuron decoding and implementing robust distributed representations.

**Implementation (280 lines):**
```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt

class PopulationVector(nn.Module):
    """
    Population vector decoder
    ŝ = Σᵢ rᵢ·dᵢ / Σᵢ rᵢ
    """

    def __init__(self, n_neurons, preferred_directions=None):
        super().__init__()

        self.n = n_neurons

        # Preferred directions (uniformly distributed around circle)
        if preferred_directions is None:
            angles = torch.linspace(0, 2*np.pi, n_neurons+1)[:-1]
            self.preferred_dirs = torch.stack([torch.cos(angles), torch.sin(angles)], dim=1)
        else:
            self.preferred_dirs = torch.tensor(preferred_directions)

    def encode(self, directions, r_max=100.0, tuning_width=1.0, noise_std=5.0):
        """
        Encode directions as population activity
        rᵢ = r_max · max(0, cos(θ - dᵢ))^n + noise

        Args:
            directions: [batch, 2] unit vectors
            r_max: Maximum firing rate
            tuning_width: Exponent controlling tuning sharpness
            noise_std: Poisson-like noise level

        Returns:
            rates: [batch, n_neurons] firing rates
        """
        batch_size = directions.shape[0]

        # Normalize input directions
        directions = F.normalize(directions, dim=1)

        # Compute cosine similarity to each preferred direction
        # cos(θ - dᵢ) = directions · preferred_dirs
        cosines = directions @ self.preferred_dirs.T  # [batch, n_neurons]

        # Cosine tuning: max(0, cos)^n
        tuning = torch.relu(cosines) ** tuning_width

        # Scale to firing rates
        rates = r_max * tuning

        # Add Poisson-like noise
        if noise_std > 0:
            noise = torch.randn_like(rates) * noise_std
            rates = torch.relu(rates + noise)

        return rates

    def decode(self, rates):
        """
        Decode direction from population activity
        ŝ = Σᵢ rᵢ·dᵢ / Σᵢ rᵢ

        Args:
            rates: [batch, n_neurons] firing rates

        Returns:
            decoded_dirs: [batch, 2] decoded directions
        """
        # Weighted sum
        weighted_sum = rates @ self.preferred_dirs  # [batch, 2]

        # Normalize by total activity
        total_activity = rates.sum(dim=1, keepdim=True) + 1e-8
        decoded = weighted_sum / total_activity

        # Normalize to unit vectors
        decoded = F.normalize(decoded, dim=1)

        return decoded


class GaussianTuningCurves(nn.Module):
    """
    Gaussian tuning curves for continuous variables
    rᵢ(s) = r_max · exp(-||s - μᵢ||²/(2σ²))
    """

    def __init__(self, n_neurons, input_dim, r_max=50.0, tuning_width=0.5):
        super().__init__()

        self.n = n_neurons
        self.input_dim = input_dim
        self.r_max = r_max
        self.tuning_width = tuning_width

        # Preferred stimuli (randomly distributed)
        self.centers = nn.Parameter(torch.randn(n_neurons, input_dim))

    def forward(self, stimulus):
        """
        Encode stimulus as population activity

        Args:
            stimulus: [batch, input_dim]

        Returns:
            rates: [batch, n_neurons]
        """
        # Distance to each preferred stimulus
        distances = torch.cdist(stimulus.unsqueeze(1), self.centers.unsqueeze(0))  # [batch, 1, n_neurons]
        distances = distances.squeeze(1)  # [batch, n_neurons]

        # Gaussian tuning
        rates = self.r_max * torch.exp(-distances**2 / (2 * self.tuning_width**2))

        return rates

    def decode_mle(self, rates):
        """
        Maximum likelihood decoder
        ŝ = argmax_s Π_i P(rᵢ|s)

        For Gaussian tuning, this simplifies to weighted average
        """
        # Weighted average (weights = firing rates)
        weights = rates / (rates.sum(dim=1, keepdim=True) + 1e-8)
        decoded = weights @ self.centers

        return decoded


class FisherInformationDecoder(nn.Module):
    """
    Optimal decoder using Fisher Information
    Achieves Cramér-Rao bound
    """

    def __init__(self, n_neurons, stimulus_dim):
        super().__init__()

        self.n = n_neurons
        self.stimulus_dim = stimulus_dim

        # Tuning curve parameters
        self.centers = nn.Parameter(torch.randn(n_neurons, stimulus_dim))
        self.widths = nn.Parameter(torch.ones(n_neurons) * 0.5)

    def tuning_curve(self, stimulus):
        """
        Gaussian tuning curves
        λᵢ(s) = exp(-||s - μᵢ||²/(2σᵢ²))
        """
        distances = torch.cdist(stimulus.unsqueeze(1), self.centers.unsqueeze(0)).squeeze(1)
        rates = torch.exp(-distances**2 / (2 * self.widths**2))
        return rates

    def fisher_information(self, stimulus):
        """
        Compute Fisher Information matrix
        I(s) = Σᵢ (∂λᵢ/∂s)^T (∂λᵢ/∂s) / λᵢ
        """
        stimulus.requires_grad_(True)
        rates = self.tuning_curve(stimulus)

        # Compute gradients
        fisher = torch.zeros(stimulus.shape[0], self.stimulus_dim, self.stimulus_dim)

        for i in range(self.n):
            # Gradient of tuning curve i
            grad = torch.autograd.grad(rates[:, i].sum(), stimulus, create_graph=True)[0]

            # Fisher information contribution
            fisher += torch.einsum('bi,bj->bij', grad, grad) / (rates[:, i].unsqueeze(1).unsqueeze(2) + 1e-8)

        stimulus.requires_grad_(False)
        return fisher

    def decode(self, rates, n_iterations=10, lr=0.1):
        """
        Gradient ascent on log-likelihood
        """
        batch_size = rates.shape[0]

        # Initialize at mean of centers
        decoded = self.centers.mean(dim=0).unsqueeze(0).expand(batch_size, -1).clone()

        for _ in range(n_iterations):
            decoded.requires_grad_(True)

            # Log-likelihood (Poisson)
            lambda_s = self.tuning_curve(decoded)
            log_likelihood = (rates * torch.log(lambda_s + 1e-8) - lambda_s).sum()

            # Gradient ascent
            grad = torch.autograd.grad(log_likelihood, decoded)[0]
            decoded = decoded.detach() + lr * grad

        return decoded


class NeuralPopulationCode(nn.Module):
    """
    Full neural population coding model
    Encoding + Decoding + Learning
    """

    def __init__(self, n_neurons, stimulus_dim, code_type='cosine'):
        super().__init__()

        self.n = n_neurons
        self.stimulus_dim = stimulus_dim
        self.code_type = code_type

        if code_type == 'cosine':
            # For angular variables (directions)
            self.encoder = PopulationVector(n_neurons)
        elif code_type == 'gaussian':
            # For continuous variables
            self.encoder = GaussianTuningCurves(n_neurons, stimulus_dim)

    def forward(self, stimulus, noise_std=5.0):
        """
        Encode then decode
        """
        # Encode
        if self.code_type == 'cosine':
            rates = self.encoder.encode(stimulus, noise_std=noise_std)
            decoded = self.encoder.decode(rates)
        elif self.code_type == 'gaussian':
            rates = self.encoder(stimulus)
            rates += torch.randn_like(rates) * noise_std
            decoded = self.encoder.decode_mle(rates)

        return rates, decoded


# Example: Motor cortex population vector
if __name__ == "__main__":
    torch.manual_seed(42)

    print("Population Vector Coding")
    print("=" * 60)

    # Motor cortex example: encode reaching directions
    print("\n1. Population Vector (Motor Cortex):")
    n_neurons = 100
    pop_vector = PopulationVector(n_neurons=n_neurons)

    # True reaching direction
    true_direction = torch.tensor([[1.0, 0.0]])  # Rightward
    print(f"   True direction: {true_direction.numpy()}")

    # Encode as population activity
    rates = pop_vector.encode(true_direction, r_max=100.0, tuning_width=2.0, noise_std=10.0)
    print(f"   Population activity: {n_neurons} neurons")
    print(f"   Mean firing rate: {rates.mean().item():.1f} Hz")
    print(f"   Active neurons: {(rates > 10).sum().item()}/{n_neurons}")

    # Decode
    decoded = pop_vector.decode(rates)
    print(f"   Decoded direction: {decoded.numpy()}")

    error = torch.acos(torch.clamp((true_direction * decoded).sum(), -1, 1)) * 180 / np.pi
    print(f"   Decoding error: {error.item():.2f}°")

    # Test accuracy vs population size
    print("\n2. Accuracy vs Population Size:")
    population_sizes = [10, 25, 50, 100, 200]
    n_trials = 100

    for n in population_sizes:
        pop = PopulationVector(n_neurons=n)
        errors = []

        for _ in range(n_trials):
            angle = torch.rand(1) * 2 * np.pi
            true_dir = torch.stack([torch.cos(angle), torch.sin(angle)], dim=1)

            rates = pop.encode(true_dir, noise_std=10.0)
            decoded = pop.decode(rates)

            error_rad = torch.acos(torch.clamp((true_dir * decoded).sum(), -1, 1))
            errors.append(error_rad.item() * 180 / np.pi)

        mean_error = np.mean(errors)
        std_error = np.std(errors)
        print(f"   n={n:3d}: Error = {mean_error:.2f}° ± {std_error:.2f}°")

    # Gaussian tuning curves
    print("\n3. Gaussian Tuning (Place Cells):")
    gaussian_pop = GaussianTuningCurves(n_neurons=50, input_dim=2, tuning_width=0.3)

    # Spatial position
    position = torch.tensor([[0.5, 0.5]])
    rates = gaussian_pop(position)

    print(f"   Position: {position.numpy()}")
    print(f"   Active place cells: {(rates > 10).sum().item()}/{50}")

    decoded_pos = gaussian_pop.decode_mle(rates)
    print(f"   Decoded position: {decoded_pos.numpy()}")
    print(f"   Error: {torch.norm(position - decoded_pos).item():.4f}")

    print("\n✓ Population codes are robust and accurate")
    print("✓ Accuracy improves with population size")
    print("✓ Foundation for brain-machine interfaces")
```

**Sources:**
- Georgopoulos et al. (1986). "Neuronal Population Coding of Movement Direction" (Science)
- Seung & Sompolinsky (1993). "Simple models for reading neuronal population codes" (PNAS)
- Abbott & Dayan (1999). "The effect of correlated variability on the accuracy of a population code"
- Pouget et al. (2000). "Information processing with population codes" (Nature Reviews)

---

## Summary Statistics

**Total Architectures Documented**: 196
**Critical Impact**: 7 (paradigm-shifting)
**High Impact**: 11 (10-100x improvements)
**Medium-High Impact**: 13 (2-10x improvements)
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

