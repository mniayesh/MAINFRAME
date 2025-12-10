# Mechanism-to-Architecture Patterns: Operational Guide for Biomimetic AI

## Overview

This document translates biological mechanisms directly into architectural components, design patterns, and implementation choices. Each mechanism is:
- **Named** (biological source)
- **Formalized** (differential equation / algorithm)
- **Mapped** (to architectural module)
- **Parametrized** (how it scales with constraints)
- **Differentiated** (vs transformers/RNNs/CNNs)

---

## 1. GENETIC & MOLECULAR LAYER → Meta-Learning & Mode Control

### 1.1 Gene Expression Dynamics as Hyperparameter Evolution

**Biological Mechanism**:
```
dR/dt = k_tx · [TF]^n / (K_d^n + [TF]^n) - γ_R · R     [Transcription]
dP/dt = k_tl · R - γ_P · P                             [Translation]
```

**Key properties**:
- Slow timescale (seconds to minutes)
- Nonlinear response (Hill coefficient = cooperativity)
- Autocatalytic/oscillatory possible (repressilators)

**Architectural mapping**:

```python
class GeneExpressionMetaLayer:
    """
    Slowpoke hyperparameter controller.

    Instead of static η, β, θ:
    - Let them evolve according to gene-expression-like dynamics
    - "Transcription factors" are system state (error rate, surprise, data scarcity)
    """

    def __init__(self, n_hyperparams):
        self.R = zeros(n_hyperparams)           # mRNA (intermediate)
        self.P = zeros(n_hyperparams)           # Protein (final hyperparameter)

        self.k_tx = 0.01  # transcription rate
        self.k_tl = 0.05  # translation rate
        self.gamma_R = 0.1 / tau_mrna
        self.gamma_P = 0.01 / tau_protein

        self.Hill_coef = 2.0  # cooperativity
        self.K_d = 0.5        # threshold

    def compute_transcription_factor(self, system_state):
        """
        Map system state (loss trajectory, novelty, etc.) to "TF concentration".

        Examples:
        - High loss → high TF → increase plasticity
        - High surprise → high TF → increase learning rate
        - Low error rate → low TF → consolidation mode
        """
        loss = system_state['loss']
        surprise = system_state['surprise']
        error_rate = system_state['error_rate']

        # Weighted combination of signals
        TF = (0.3 * (loss / baseline_loss) +
              0.4 * surprise +
              0.3 * error_rate)

        return TF

    def step(self, system_state, dt=1.0):
        """Update hyperparameters via gene-expression dynamics."""

        TF = self.compute_transcription_factor(system_state)

        # Hill function: nonlinear activation
        TF_effect = (TF ** self.Hill_coef) / (self.K_d ** self.Hill_coef + TF ** self.Hill_coef)

        # Transcription: TF drives mRNA production
        dR_dt = self.k_tx * TF_effect - self.gamma_R * self.R
        self.R += dR_dt * dt

        # Translation: mRNA drives protein production
        dP_dt = self.k_tl * self.R - self.gamma_P * self.P
        self.P += dP_dt * dt

        return self.P  # These become current hyperparameters

    @property
    def learning_rate(self):
        """Map protein level to learning rate."""
        return 0.001 * (1.0 + 10.0 * self.P[0])  # Scales from 0.001 to 0.011

    @property
    def plasticity_mode(self):
        """Mode switch based on repressilator-like oscillation."""
        # Oscillatory circuit: A → ⊣ B, B → ⊣ A (negative feedback loop)
        # Result: alternating high/low states

        osc_phase = (self.P[1] - self.P[2]) > 0
        return 'online_learning' if osc_phase else 'consolidation'

    @property
    def exploration_temperature(self):
        """Epistemic uncertainty → higher temperature = more exploration."""
        return 0.1 + 2.0 * self.P[1]
```

**Design patterns**:

1. **Slow meta-learning**: Hyperparameters change on a longer timescale than weights
2. **Hill-driven mode switching**: Nonlinearity allows sharp transitions at thresholds
3. **Oscillatory internal clocks**: Repressilator-like circuits trigger periodic events:
   - Memory replay
   - Attention resets
   - Compression/pruning passes

**vs Transformers**:
| Aspect | Transformers | Gene-Driven System |
|--------|--------------|-------------------|
| Learning rate | Static (0.001) | Dynamic (0.001 → 0.011) based on loss |
| Mode switching | Hard-coded in code | Emergent from Hill functions |
| Internal state | Activations only | Activations + slow protein state |
| Adaptation | Only via weight updates | Via both weights + hyperparameter dynamics |

---

## 2. DENDRITIC LAYER → Sub-Neuron Computation & Local Programs

### 2.1 Multi-Compartment Neurons (Cable Equation)

**Biological mechanism**:
```
λ²·∂²V/∂x² = τ·∂V/∂t + V - V_rest     [Cable equation - passive propagation]
C·dV_i/dt = Σ(g_ij(V_j - V_i)) + I_syn - I_leak  [Compartmental - active]
```

**Key properties**:
- Spatial structure inside a neuron
- Different compartments (basal, apical, distal) can compute independently
- Voltage coupling between compartments
- Enables multi-input integration with different rules per compartment

**Architectural mapping**:

```python
class MultiCompartmentNeuron:
    """
    Instead of neuron = scalar activation:
    neuron = small internal network of compartments.

    Enables:
    - Dendritic error signals (apical)
    - Feedforward inputs (basal)
    - Context/neuromodulation (distal)
    """

    def __init__(self, n_basal, n_apical, n_distal):
        # Three dendritic zones
        self.V_basal = zeros(n_basal)      # Feed-forward inputs
        self.V_apical = zeros(n_apical)    # Top-down predictions (errors)
        self.V_distal = zeros(n_distal)    # Context/neuromodulation

        self.soma_V = 0.0                  # Cell body voltage
        self.soma_threshold = 0.2
        self.soma_refract = 0

        # Coupling conductances (determined by dendritic geometry)
        self.g_basal_to_soma = 1.0
        self.g_apical_to_soma = 0.5        # Weaker coupling (further away)
        self.g_distal_to_soma = 0.3

        # Time constants (different for different compartments)
        self.tau_basal = 5.0   # Fast (distal = far from soma)
        self.tau_apical = 10.0
        self.tau_distal = 20.0
        self.tau_soma = 2.0    # Fast (soma = trigger zone)

        self.C = 1.0
        self.leak = 0.1

    def receive_inputs(self, feedforward, top_down_error, context, dt=0.1):
        """
        Compartment-specific inputs:
        - feedforward → basal dendrite
        - top_down_error → apical dendrite
        - context → distal dendrite
        """

        # Passive decay + input in each compartment
        self.V_basal = (1 - self.leak * dt) * self.V_basal + feedforward * dt
        self.V_apical = (1 - self.leak * dt) * self.V_apical + top_down_error * dt
        self.V_distal = (1 - self.leak * dt) * self.V_distal + context * dt

        # Coupling: dendritic voltages drive soma
        dV_soma = (
            (self.g_basal_to_soma * self.V_basal +
             self.g_apical_to_soma * self.V_apical +
             self.g_distal_to_soma * self.V_distal) -
            self.soma_V
        ) / self.tau_soma - self.leak * self.soma_V

        self.soma_V += dV_soma * dt

    def spike(self):
        """Fire if soma crosses threshold (and not refractory)."""
        if self.soma_V > self.soma_threshold and self.soma_refract == 0:
            self.soma_V = 0.0  # Reset
            self.soma_refract = 5  # 5 timesteps refractory
            return 1.0

        if self.soma_refract > 0:
            self.soma_refract -= 1

        return 0.0

    def local_plasticity(self, pre, post_basal, post_apical, post_soma):
        """
        Compartment-specific plasticity:
        - Apical predicts basal (predictive coding)
        - Distal gates basal (context-dependent learning)
        """

        # Predictive coding error
        prediction_error = post_basal - post_apical  # Apical tries to predict basal

        # Apical weights learn to predict basal
        dW_apical = 0.01 * prediction_error * pre  # Reduces error

        # Basal-to-soma weights gated by distal context
        gating = post_distal  # High distal = allow learning
        dW_basal = 0.01 * post_soma * pre * gating

        return dW_apical, dW_basal
```

**Design patterns**:

1. **Three-factor learning**: Apical signals provide a teaching signal (like backprop)
2. **Dendritic gating**: Distal dendrite gates learning in basal synapses → context-dependent plasticity
3. **Error signal locality**: Apical dendrite computes prediction error locally, no need for layer-wise backprop

**vs Transformers**:
| Aspect | Transformers | Multi-Compartment |
|--------|--------------|------------------|
| Neuron model | Scalar with nonlinearity | Three-part: basal + apical + distal |
| Error signal | Global backprop | Local apical dendrite |
| Learning | Weight-centric | Compartment-aware, context-gated |
| Computation | Linear + nonlinearity | Nonlinear coupling of compartments |

---

### 2.2 Temporal Integration & Decay (Working Memory)

**Biological mechanism**:
```
τ·dV/dt = -(V - V_rest) + R·I           [Leaky integrate-and-fire]
V(t) = V_0·exp(-t/τ)                    [Exponential decay]
```

**Architectural mapping**:

```python
class TemporalIntegrationUnit:
    """
    Biologically realistic short-term memory cell.

    Unlike LSTM gates (which are learned), time constants τ are:
    - Set biologically (milliseconds for fast synapses, seconds for slow)
    - Scaled based on hardware constraints
    """

    def __init__(self, capacity, tau_short=5.0, tau_long=100.0):
        """
        tau: milliseconds (can scale to device)

        On edge device (low power):
          tau_short = 2.0 ms, tau_long = 20.0 ms (faster decay)
        On server (rich compute):
          tau_short = 50.0 ms, tau_long = 500.0 ms (longer memory)
        """
        self.state = zeros(capacity)
        self.tau = ones(capacity) * tau_short  # Base time constant
        self.V_rest = -0.1
        self.R = 1.0  # Resistance

    def step(self, input_current, dt=0.001):
        """
        Leaky integration:
        dV/dt = -(V - V_rest) / τ + R * I

        Slow decay → long working memory
        Fast decay → attention to recent inputs
        """

        leak = -((self.state - self.V_rest) / self.tau)
        input_effect = self.R * input_current

        self.state += (leak + input_effect) * (dt / self.tau)

        return self.state

    @staticmethod
    def decay_constant(capacity_bits, timescale_ms, hardware_budget):
        """
        Compute optimal τ based on task needs.

        Principle: Larger working memory → longer τ
        """
        # Information-theoretic lower bound on decay time
        tau_min = capacity_bits * 0.1  # At least 0.1 ms per bit

        # Hardware constraint: fewer neurons → shorter τ
        tau_hardware = hardware_budget  # milliseconds

        # Task-driven: working memory timescale
        tau_task = timescale_ms

        return max(tau_min, min(tau_hardware, tau_task))
```

**Design patterns**:

1. **Automatic timescale tuning**: τ is derived from capacity + hardware, not hand-tuned
2. **Exponential decay built-in**: Natural forgetfulness without explicit gates
3. **Layered τ values**: Different τ per neuron → hierarchical temporal structure

---

## 3. SYNAPTIC PLASTICITY LAYER → Multiple Parallel Learning Systems

### 3.1 Hebbian, Oja, BCM, STDP Selection

**Biological mechanisms**:
```
Hebbian:              Δw = η·x·y
Oja:                  Δw = η·y·(x - w·y)
BCM:                  dw/dt = η·y·(y - θ)·x
STDP:                 Δw(Δt) = A_+·exp(-|Δt|/τ_+) - A_-·exp(-|Δt|/τ_-)
Short-term:           dx/dt = (1-x)/τ_rec;  u → u + U·(1-u)  after spike
```

**Architectural mapping**:

```python
class SynapseWithSelectablePlasticity:
    """
    Each synapse (or synapse group) has a learning-rule ID.
    The system dynamically selects which rule to apply based on:
    - Layer/module role (memory, decision, prediction)
    - Task type (RL, supervised, unsupervised)
    - Energy budget
    """

    def __init__(self,
                 pre_neurons, post_neurons,
                 learning_rule='hebbian',
                 plasticity_enabled=True):
        self.W = randn(pre_neurons, post_neurons) * 0.01
        self.learning_rule = learning_rule  # 'hebbian', 'oja', 'bcm', 'stdp'
        self.plasticity_enabled = plasticity_enabled

        # STDP timing history
        self.last_pre_spikes = zeros(pre_neurons)
        self.last_post_spikes = zeros(post_neurons)
        self.spike_times = deque(maxlen=1000)

    def apply_learning_rule(self, pre, post, dt):
        """
        Apply selected learning rule.

        Each rule captures a different property:
        - Hebbian: co-occurrence → association
        - Oja: normalization → competitive learning
        - BCM: sliding threshold → stability + adaptation
        - STDP: causality → sequence learning
        """

        if not self.plasticity_enabled:
            return

        eta = 0.01  # Learning rate

        if self.learning_rule == 'hebbian':
            # Simple co-occurrence
            dW = eta * outer(pre, post)
            self.W += dW

        elif self.learning_rule == 'oja':
            # Hebbian + weight decay → weight normalization (PCA)
            dW = eta * outer(pre, post)
            decay = eta * outer(post**2, post) * self.W
            self.W += dW - decay

        elif self.learning_rule == 'bcm':
            # Sliding threshold: theta = <post²>
            theta = mean(post**2)  # Running average
            dW = eta * outer(pre, post * (post - theta))
            self.W += dW

        elif self.learning_rule == 'stdp':
            # Spike-timing dependent plasticity
            for i, pre_spike_time in enumerate(self.last_pre_spikes):
                for j, post_spike_time in enumerate(self.last_post_spikes):
                    delta_t = post_spike_time - pre_spike_time

                    # Causal window: pre before post = potentiation
                    if 0 < delta_t < 20.0:  # 20 ms window
                        self.W[i, j] += 0.01 * exp(-delta_t / 20.0)
                    elif -20.0 < delta_t < 0:  # Anti-causal
                        self.W[i, j] -= 0.01 * exp(abs(delta_t) / 20.0)

        elif self.learning_rule == 'short_term':
            # Resource dynamics (Tsodyks-Markram)
            # Not a weight change, but synapse state
            # Implement in separate resource_state
            pass

        # Clip weights to prevent runaway
        self.W = clip(self.W, -1.0, 1.0)

    def select_learning_rule_dynamically(self, context):
        """
        System can switch learning rules based on task/state.

        Example heuristic:
        - high error → use BCM (adaptive threshold helps)
        - learning sequences → use STDP (temporal structure)
        - memorization → use Hebbian (direct association)
        """

        error = context.get('loss', 0.0)
        task_type = context.get('task_type', 'classification')
        energy_budget = context.get('energy_budget', 1.0)

        if task_type == 'reinforcement_learning':
            self.learning_rule = 'stdp'  # Temporal structure matters
        elif task_type == 'sequence':
            self.learning_rule = 'stdp'
        elif error > 0.5:
            self.learning_rule = 'bcm'  # Adaptive threshold
        else:
            self.learning_rule = 'hebbian'  # Simple when stable

        # On low-power devices, reduce STDP complexity
        if energy_budget < 0.3:
            self.learning_rule = 'hebbian'
```

**Design patterns**:

1. **Heterogeneous plasticity**: Different synapses use different rules
2. **Task-aware selection**: Architecture chooses learning rule based on context
3. **Energy-aware learning**: Low-power devices use simpler rules (Hebbian) vs rich hardware (STDP)

**vs Transformers**:
| Aspect | Transformers | Multi-Rule Plasticity |
|--------|--------------|----------------------|
| Learning | Backprop everywhere | Multiple rules: Hebbian, STDP, BCM, etc. |
| Adaptation | Via weight updates | Via rule selection + weight updates |
| Temporal | No explicit timing | STDP captures causality |
| Efficiency | High (parallel backprop) | Varies by rule (STDP expensive) |

---

## 4. NORMALIZATION LAYER → Competition & Resource Allocation

### 4.1 Divisive Normalization as Capacity Constraint

**Biological mechanism**:
```
y_i = x_i / (σ + Σ_j x_j)     [Divisive normalization - competition]
y_i = exp(x_i) / Σ_j exp(x_j)  [Softmax - probabilistic]
```

**Architectural mapping**:

```python
class DivisiveNormalizationLayer:
    """
    Normalization is not just statistical; it's a capacity constraint.

    Biological interpretation:
    - Limited metabolic budget
    - Winner-take-all competition
    - Attention-like gating
    """

    def __init__(self, n_units, capacity='unlimited'):
        self.n_units = n_units
        self.capacity = capacity  # bits, neurons, or None

        # Adaptive sigma for normalization strength
        self.sigma = 0.1
        self.sigma_adapt_rate = 0.001

    def forward(self, x):
        """
        Divisive normalization:
        y_i = x_i / (sigma + sum(x))

        Effect: strong competition, suppresses weak signals
        """
        x = relu(x)  # Non-negative activations
        sum_x = sum(x) + self.sigma
        y = x / sum_x

        return y

    def adaptive_capacity(self, context):
        """
        Adjust normalization strength based on available resources.

        High capacity → softer competition (sigma increases)
        Low capacity → harder competition (sigma decreases)
        """
        if self.capacity == 'unlimited':
            return

        available_bits = context.get('available_bits', self.capacity)
        entropy = -sum(y * log(y + 1e-8) for y in self.y)

        # If using too many bits, increase competition
        if entropy > available_bits:
            self.sigma *= (1.0 + self.sigma_adapt_rate)
        else:
            self.sigma *= (1.0 - self.sigma_adapt_rate)

        self.sigma = clip(self.sigma, 0.01, 1.0)

    def attention_as_normalization(self, queries, keys, values):
        """
        Softmax attention is divisive normalization in disguise:
        scores = exp(q·k) / sum(exp(q·k))

        Can be replaced with biological normalization for robustness.
        """

        # Biologically inspired: threshold + competition
        scores = max(0, queries @ keys.T - threshold)
        attention = self.forward(scores)  # Divisive norm instead of softmax

        output = attention @ values
        return output
```

**Design patterns**:

1. **Capacity-aware normalization**: σ adapts to available resources
2. **Competition instead of softmax**: Harder to learn but more biologically grounded
3. **Automatic bandwidth limiting**: System naturally limits information flow

---

## 5. ATTRACTOR NETWORKS → Memory, Concepts, States

### 5.1 Hopfield Networks & Continuous Attractors

**Biological mechanism**:
```
E = -½ Σ_ij w_ij s_i s_j - Σ_i θ_i s_i   [Hopfield energy]
dx/dt = -x + f(W·x + I)                    [Continuous attractor]
```

**Architectural mapping**:

```python
class AttractorMemoryBank:
    """
    Dedicated region for storing and retrieving patterns.

    Each stable attractor = a concept/goal/situation.
    Partial cue → full pattern completion via relaxation.
    """

    def __init__(self, n_neurons, n_patterns, attractor_type='hopfield'):
        self.n = n_neurons
        self.n_patterns = n_patterns
        self.W = zeros((n_neurons, n_neurons))
        self.type = attractor_type

        # Learning/consolidation parameters
        self.consolidation_rate = 0.001  # Slow weight changes
        self.relaxation_steps = 50
        self.temperature = 0.1

    def encode_pattern(self, pattern):
        """
        Learn a pattern via Hebbian-like rule.

        Biological: neurons fire together, synapse strengthens.
        """
        # Outer product: pattern reinforces itself
        dW = outer(pattern, pattern) / len(pattern)
        self.W += dW * self.consolidation_rate

        # Remove self-connections (no autapses)
        diag_indices = diag_indices_from((self.n, self.n))
        self.W[diag_indices] = 0

        # Normalize to prevent runaway
        self.W = self.W / max(abs(self.W))

    def retrieve(self, cue, noisy=False):
        """
        Settle from partial cue to full pattern.

        Iteratively apply:
        x ← f(W·x + noise)

        Noise helps escape local minima and adds robustness.
        """
        x = cue.copy()

        for _ in range(self.relaxation_steps):
            # Energy function (for Hopfield)
            u = self.W @ x

            # Nonlinear activation (can be anything from threshold to sigmoid)
            x_new = tanh(u)

            # Add noise for robustness
            if noisy:
                x_new += randn(len(x)) * self.temperature

            # Check for convergence
            if max(abs(x_new - x)) < 1e-6:
                break

            x = x_new

        return x

    def consolidate(self, recent_patterns, sleep_duration=100):
        """
        Offline consolidation: replayed during "sleep".

        Strengthens patterns in long-term storage.
        """
        for _ in range(sleep_duration):
            # Pick random pattern, reactivate it
            pattern = random.choice(recent_patterns)

            # Retrieve and re-encode (strengthens memory)
            retrieved = self.retrieve(pattern, noisy=True)
            self.encode_pattern(retrieved)
```

**Design patterns**:

1. **Pattern completion**: Partial cue → full pattern
2. **Offline consolidation**: Replay during "sleep" strengthens memories
3. **Noise-driven robustness**: Small noise prevents getting stuck

---

## 6. PREDICTIVE CODING → Core Inference

### 6.1 Hierarchical Prediction Error Minimization

**Biological mechanism**:
```
ε_l = x_l - μ_l                           [Prediction error]
dμ_l/dt ∝ -ε_l + ε_{l-1}                 [Belief update from errors]
dμ_{l+1}/dt ∝ ε_l·f'(·)                  [Top-down correction]
```

**Architectural mapping**:

```python
class PredictiveCodingLayer:
    """
    Replaces feedforward inference with error-minimization dynamics.

    Instead of:
      x → [dense] → y  (one-pass forward)

    Do:
      x → [PC layer] → error minimization → y  (iterative)

    Advantages:
    - Bidirectional inference
    - Built-in uncertainty
    - No explicit backprop needed
    """

    def __init__(self,
                 in_dim, out_dim,
                 n_iterations=10,
                 learning_rate=0.01):
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.n_iterations = n_iterations
        self.learning_rate = learning_rate

        # Generative model: μ ← f(μ_{l+1})
        self.W_gen = randn(out_dim, in_dim) * 0.1
        self.b_gen = zeros(in_dim)

        # Inference: μ ← [correction from errors]
        self.mu = zeros(out_dim)  # Latent belief
        self.x = None  # Observed input

    def predict(self):
        """Generate prediction from latent μ."""
        return self.mu @ self.W_gen + self.b_gen

    def compute_error(self):
        """Prediction error: ε = x - μ_prediction."""
        prediction = self.predict()
        error = self.x - prediction
        precision = 1.0 / (1.0 + 0.1 * error**2)  # Estimate precision
        return error, precision

    def infer(self, x, error_from_above=None):
        """
        Minimize prediction error iteratively.

        dμ/dt ∝ error_from_below + error_from_above
        """
        self.x = x

        for iteration in range(self.n_iterations):
            error, precision = self.compute_error()

            # Gradient on μ to minimize error
            grad_mu = error @ self.W_gen.T

            # If there's error from the layer above, include it
            if error_from_above is not None:
                grad_mu += error_from_above

            # Update latent belief
            self.mu += self.learning_rate * grad_mu * precision

        return self.mu

    def update_generative_model(self, grad_from_above=None):
        """
        Update W_gen to better predict x from μ.

        Uses EM-like steps (expectation is pc_inference, maximization here).
        """
        prediction = self.predict()
        error = self.x - prediction

        # Gradient w.r.t. W_gen
        dW = outer(error, self.mu)
        self.W_gen += self.learning_rate * dW


class PredictiveCodingNetwork:
    """
    Stack of PC layers forming a hierarchy.

    Each layer:
    1. Predicts the layer below
    2. Minimizes prediction error
    3. Sends errors upward
    """

    def __init__(self, layer_dims, n_iterations_per_layer=10):
        self.layers = []
        for i in range(len(layer_dims) - 1):
            layer = PredictiveCodingLayer(
                layer_dims[i], layer_dims[i+1],
                n_iterations=n_iterations_per_layer
            )
            self.layers.append(layer)

    def forward(self, x):
        """
        Forward pass = predictive coding inference.

        x → layer 0 → error → layer 1 → error → ... → output
        """
        errors = [x]

        for i, layer in enumerate(self.layers):
            error_from_above = errors[-1] if i > 0 else None
            mu = layer.infer(errors[-1], error_from_above)
            errors.append(layer.predict())

        return self.layers[-1].mu

    def backward(self):
        """
        Learning = updating generative models.

        Each layer learns to better predict the layer below.
        """
        for layer in reversed(self.layers):
            layer.update_generative_model()
```

**Design patterns**:

1. **Bidirectional inference**: Top-down predictions + bottom-up errors
2. **No backprop needed**: Errors propagate automatically
3. **Built-in uncertainty**: Can track precision of beliefs

---

## 7. DECISION SYSTEMS → Drift-Diffusion + Bayesian + Habits

### 7.1 Multi-System Decision Arbitration

**Biological mechanisms**:
```
Drift-diffusion:    dx/dt = μ·I + σ·ξ(t)
Bayesian:           P(θ|D) = P(D|θ)·P(θ)/P(D)
Habit:              Q_MF ← Q_MF + α·δ
Goal:               Q_MB = Σ P(s'|s,a) max Q(s',a')
Arbitration:        Q_total = w·Q_MB + (1-w)·Q_MF
```

**Architectural mapping**:

```python
class MultiSystemDecisionMaker:
    """
    Parallel decision systems with reliability-weighted arbitration.

    Systems:
    1. Drift-diffusion: Fast, low-cognitive load
    2. Bayesian inference: Slow, principled
    3. Habit (model-free): Very fast, unconscious
    4. Goal (model-based): Slower, conscious planning
    """

    def __init__(self, n_actions, n_states=None):
        self.n_actions = n_actions
        self.n_states = n_states

        # System 1: Drift-diffusion accumulators
        self.accumulators = zeros(n_actions)
        self.drift_rates = ones(n_actions) * 0.1
        self.noise_level = 0.01
        self.threshold = 1.0
        self.urgency_signal = 0.0

        # System 2: Bayesian beliefs
        self.prior_beliefs = ones(n_actions) / n_actions
        self.likelihood = ones(n_actions)
        self.posterior = self.prior_beliefs.copy()

        # System 3: Habit (Q-learning)
        self.Q_habit = zeros((n_states, n_actions)) if n_states else zeros(n_actions)
        self.habit_reliability = 0.5

        # System 4: Goal (planning)
        self.Q_goal = zeros((n_states, n_actions)) if n_states else zeros(n_actions)
        self.goal_reliability = 0.5

        # Arbitration weight
        self.w_goal = 0.5  # Mix goal and habit

    def drift_diffusion_step(self, evidence, dt=0.01):
        """
        System 1: Accumulate evidence over time.

        Matches RT data from human decision-making.
        """
        # Drift: evidence weighted by drift rate
        drift = evidence * self.drift_rates

        # Noise: unbiased random walk
        noise = randn(self.n_actions) * self.noise_level

        # Time-varying threshold (urgency: threshold lowers over time)
        dynamic_threshold = self.threshold * (1.0 - self.urgency_signal)

        self.accumulators += (drift + noise) * dt

        # Check for decision
        if max(self.accumulators) >= dynamic_threshold:
            action = argmax(self.accumulators)
            reaction_time = self.compute_reaction_time()
            return action, reaction_time

        return None, None

    def bayesian_inference_step(self, observation):
        """
        System 2: Update beliefs via Bayes rule.

        Principled but slow.
        """
        # Likelihood: P(obs | action)
        self.likelihood = compute_likelihood(observation, self.n_actions)

        # Bayes rule
        self.posterior = (self.likelihood * self.prior_beliefs) / (
            sum(self.likelihood * self.prior_beliefs) + 1e-10
        )

        # Confidence: inverse entropy
        entropy = -sum(self.posterior * log(self.posterior + 1e-10))
        confidence = 1.0 - (entropy / log(self.n_actions))

        return argmax(self.posterior), confidence

    def habit_step(self, state):
        """System 3: Fast, learned associations (model-free)."""
        Q_values = self.Q_habit[state]
        return argmax(Q_values), self.habit_reliability

    def goal_step(self, state, model):
        """System 4: Deliberative planning (model-based)."""
        # Simulate forward: state → action → next_state
        Q_goal = zeros(self.n_actions)
        for a in range(self.n_actions):
            next_state = model.predict(state, a)
            Q_goal[a] = model.reward(state, a) + 0.9 * max(self.Q_goal[next_state])

        return argmax(Q_goal), self.goal_reliability

    def arbitrate(self, decisions):
        """
        Combine decisions from all systems.

        weighted = w_goal * goal_decision + (1-w_goal) * habit_decision
        """
        habit_action, habit_conf = decisions['habit']
        goal_action, goal_conf = decisions['goal']

        # Update arbitration weight based on reliability
        self.habit_reliability = compute_reliability(self.Q_habit)
        self.goal_reliability = compute_reliability(self.Q_goal)

        # Weighted combination
        total_reliability = self.habit_reliability + self.goal_reliability
        self.w_goal = self.goal_reliability / (total_reliability + 1e-10)

        # Soft mixture (use w to blend actions)
        if random() < self.w_goal:
            return goal_action
        else:
            return habit_action

    def full_decision(self, state, observation, evidence, model):
        """
        Orchestrate all systems and arbitrate.
        """

        # Gather decisions from all systems
        drift_action, dd_rt = self.drift_diffusion_step(evidence)
        bayes_action, bayes_conf = self.bayesian_inference_step(observation)
        habit_action, habit_conf = self.habit_step(state)
        goal_action, goal_conf = self.goal_step(state, model)

        decisions = {
            'drift_diffusion': (drift_action, dd_rt),
            'bayesian': (bayes_action, bayes_conf),
            'habit': (habit_action, habit_conf),
            'goal': (goal_action, goal_conf),
        }

        # Which system is fastest/most confident?
        if drift_action is not None and dd_rt < threshold_rt:
            # Fast automatic decision
            return drift_action, 'automatic'

        # Otherwise, arbitrate between habit and goal
        action = self.arbitrate({'habit': (habit_action, habit_conf),
                                 'goal': (goal_action, goal_conf)})
        return action, 'deliberative'
```

**Design patterns**:

1. **Parallel processing**: Multiple systems compute in parallel
2. **Dynamic arbitration**: System switches based on reliability
3. **RT matching**: Drift-diffusion produces realistic reaction times
4. **Uncertainty propagation**: Each system reports confidence

---

## 8. GLOBAL WORKSPACE → Executive Control & Awareness

### 8.1 Competition for Global Broadcast

**Biological mechanism**:
```
Multiple "processors" (brain regions) compete for access to a global workspace.
Winner broadcasts to all others → conscious awareness.
```

**Architectural mapping**:

```python
class GlobalWorkspaceWithCompetition:
    """
    Implements Baars' Global Workspace Theory.

    Multiple processors compete; winner broadcasts → conscious event.
    All other processors receive broadcast → learn from it.
    """

    def __init__(self, n_processors, workspace_dim):
        self.processors = [Processor(workspace_dim) for _ in range(n_processors)]
        self.workspace = zeros(workspace_dim)
        self.broadcast_threshold = 0.5
        self.competition_period = 1.0  # seconds

        self.consciousness_events = []
        self.broadcast_history = deque(maxlen=100)

    def compute_processor_bids(self):
        """
        Each processor computes how "important" its content is.

        Bid = activation level * recency * novelty
        """
        bids = []
        for i, proc in enumerate(self.processors):
            activation = proc.activation_level()
            recency = 1.0 if proc.just_activated() else 0.5
            novelty = proc.compute_novelty()

            bid = activation * recency * novelty
            bids.append((bid, i))

        return sorted(bids, reverse=True)

    def competition_phase(self):
        """
        Processors compete for workspace access.
        """
        bids = self.compute_processor_bids()

        if len(bids) == 0:
            return None

        winner_bid, winner_idx = bids[0]

        # Does winner exceed broadcast threshold?
        if winner_bid > self.broadcast_threshold:
            return winner_idx

        return None  # No conscious event this cycle

    def broadcast_phase(self, winner_idx):
        """
        Winner broadcasts to all processors.

        All processors update their beliefs based on broadcast.
        """
        winner_message = self.processors[winner_idx].extract_message()

        self.workspace = winner_message
        self.broadcast_history.append(winner_message)

        # All processors receive broadcast
        for i, proc in enumerate(self.processors):
            if i != winner_idx:
                proc.receive_broadcast(winner_message)

        return winner_message

    def full_cycle(self):
        """
        One cycle of competition + broadcast = one "conscious moment".
        """
        winner_idx = self.competition_phase()

        if winner_idx is not None:
            broadcast = self.broadcast_phase(winner_idx)
            self.consciousness_events.append({
                'winner': winner_idx,
                'message': broadcast,
                'timestamp': current_time
            })
            return broadcast

        return None


class ConsciousnessMonitor:
    """
    Track global workspace activity.

    Consciousness = high-bandwidth broadcast event.
    """

    def __init__(self):
        self.consciousness_level = 0.0
        self.recent_broadcasts = deque(maxlen=10)

    def measure_consciousness(self, workspace_activity, broadcast_frequency):
        """
        Consciousness level depends on:
        - How much information is broadcast (workspace activity)
        - How frequently (broadcast rate)
        """
        info_content = entropy(workspace_activity)
        broadcast_rate = broadcast_frequency

        # High information + frequent broadcasts = high consciousness
        self.consciousness_level = (info_content * 0.5 +
                                    broadcast_rate * 0.5)

        return self.consciousness_level
```

**Design patterns**:

1. **Multiple unconscious processors**: Each solves part of the problem
2. **Winner-take-all competition**: Only one message broadcast at a time
3. **Global state sharing**: All processors informed of broadcast
4. **Learning from broadcast**: All processors update based on winner's message

---

## 9. Summary: From Mechanisms to Architecture

### 9.1 Mechanism → Module → System

```
Biological Mechanism
        ↓
Formalized Equation
        ↓
Canonical Primitive
        ↓
Configurable Module
        ↓
System Component
        ↓
Complete AI System
```

### 9.2 Design Decisions Summary

| Level | Mechanism | Module | Parameter |
|-------|-----------|--------|-----------|
| Meta | Gene expression | Hyperparameter controller | Hill coefficient, τ, TF signal |
| Dendritic | Cable equation | Multi-compartment neuron | λ, τ, coupling weights |
| Synaptic | STDP/BCM/Oja | Synapse group | Learning rule, η, time constants |
| Population | Attractors | Memory bank | n_patterns, consolidation rate |
| Network | Predictive coding | PC layer | n_iterations, learning rate |
| Decision | Drift-diffusion | Accumulator | drift_rate, noise, threshold |
| Executive | Global workspace | Processor competition | broadcast_threshold |

### 9.3 Scaling Formula

```python
def architecture_scale(hardware_budget, task_complexity):
    """
    Derive system size from constraints.
    """

    # Neuron count
    N = sqrt(hardware_budget * task_complexity)

    # Dendritic complexity
    dendritic_branches = 10 + N / 100

    # Working memory capacity (bits)
    working_memory = log(N / 2)

    # Long-term memory patterns
    n_patterns = N * 0.1

    # Timestep (smaller hardware = faster timescale)
    dt = 0.001 / sqrt(hardware_budget)

    # Learning rate (constrained by stability)
    eta = 0.01 / sqrt(N)

    return {
        'n_neurons': int(N),
        'dendritic_branches': int(dendritic_branches),
        'working_memory_bits': int(working_memory),
        'n_patterns': int(n_patterns),
        'dt': dt,
        'learning_rate': eta,
    }
```

---

## Conclusion: The Paradigm Shift

**Traditional AI**:
- Fix architecture
- Train weights
- Deploy

**Biomimetic MDA**:
- Load mechanisms
- Assemble architecture from primitives
- Scale based on constraints
- System self-regulates learning, memory, decision-making
- Deploy with full explainability

Every component is traceable to biology. The system is as much biology simulator as it is AI.

This is fundamentally different.

---
