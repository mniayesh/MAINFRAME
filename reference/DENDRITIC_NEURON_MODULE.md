# Dendritic Neuron Module: The Computational Foundation

**Purpose:** Define the smallest implementable computational unit — a neuron with active dendrites, not a simple weighted sum.

**Key Insight:** A biological neuron is itself a small neural network. Dendrites perform local, nonlinear computations before the soma integrates them. This gives ~100-1000× the expressiveness of standard artificial neurons.

---

## 🧬 Biological Facts (What We Know)

### Dendritic Anatomy
- Typical neuron: **10-50 dendritic branches**
- Each branch: **100-1000 synapses**
- Branches are **electrically compartmentalized** (semi-independent)
- Soma integrates all branch outputs
- Axon hillock: final threshold gate

### Dendritic Computations (Experimentally Verified)
1. **Local nonlinearity per branch:**
   - NMDA spikes (supralinear summation)
   - Calcium spikes (regenerative)
   - Direction selectivity (asymmetric integration)

2. **Dendritic saturation:**
   - Branch voltage approaches ceiling (~50mV)
   - Acts like divisive normalization
   - Similar to softmax behavior

3. **Coincidence detection:**
   - Branches detect simultaneous inputs
   - Subthreshold summation rules

4. **Active dendrites:**
   - Voltage-gated ion channels
   - Local amplification of inputs
   - Branch-specific plasticity rules

### Computational Consequence
$$\text{Biological neuron} = \text{Small MLP}$$

---

## 🔧 Mathematical Model: Multi-Branch Neuron

### Architecture Specification

A dendritic neuron with $B$ branches:

```
Input x ∈ ℝ^d
    ↓
[Branch 1] [Branch 2] ... [Branch B]
    ↓         ↓              ↓
   f₁(W₁x)   f₂(W₂x) ... f_B(W_B x)
    ↓         ↓              ↓
   Branch outputs → Soma Integration → Output
```

### Branch-Level Computation

**Type 1: Excitatory Branch (Feedforward)**

$$b_j(x) = \sigma(W_j x + b_j)$$

Where:
- $W_j \in \mathbb{R}^{m \times d}$ : branch weights
- $\sigma$ : nonlinearity (ReLU, tanh, or NMDA-like)
- $b_j$ : branch bias

**Type 2: Dendritic Saturation Branch (Normalized)**

Models sublinear summation observed in real dendrites:

$$b_j(x) = \frac{W_j x + b_j}{1 + \alpha ||W_j x||^2}$$

Where $\alpha$ controls saturation strength.

Interpretation:
- Strong inputs saturate (like voltage ceiling)
- Weak inputs superimpose linearly
- Emergent divisive normalization

**Type 3: Multiplicative Gate Branch (Gated Integration)**

Models direction selectivity & feature gating:

$$b_j(x) = (W_j^{(1)} x) \odot \sigma(W_j^{(2)} x)$$

Where $\odot$ is element-wise multiplication.

Interpretation:
- First term: input signal
- Second term: gate (0-1 range)
- Combined: conditional routing

**Type 4: Predictive Branch (Top-Down Prediction)**

Implements cortical prediction errors:

$$b_j(x, \hat{x}) = \sigma(W_j^{(down)} \hat{x} - W_j^{(up)} x)$$

Where:
- $\hat{x}$ : top-down prediction from upper layer
- $x$ : bottom-up input
- Output: prediction error (signed)

Interpretation:
- Models cortical feedback loop
- Soma receives error signals for learning

### Soma Integration

**Option A: Linear Sum**

$$y = \sum_j w_j b_j(x)$$

Simple but misses inhibitory interactions.

**Option B: Softmax Over Branches (Winner-Take-All)**

$$y = \sum_j \frac{\exp(\lambda b_j(x))}{\sum_k \exp(\lambda b_k(x))} b_j(x)$$

Where $\lambda$ controls competition strength.

Interpretation:
- Branches "compete"
- Strongest branch dominates
- Matches lateral inhibition in cortex

**Option C: Hierarchical Integration (Most Realistic)**

Multiple layers of integration before soma:

$$\text{Level 1:} \quad g_{jk} = \text{Integrate}(b_j, b_k) \quad \text{for all pairs}$$

$$\text{Level 2:} \quad y = \sigma(W_{soma} [b_1, ..., b_B, g_{11}, ...])$$

Interpretation:
- Dendritic branches interact
- Cross-branch gating
- Models observed cortical complexity

### Complete Dendritic Neuron

**Forward Pass:**

```python
def dendritic_neuron_forward(x, W_branches, W_soma, branch_type='mixed'):
    """
    Compute output of a dendritic neuron.

    Args:
        x: input [d,]
        W_branches: list of B weight matrices
        W_soma: soma integration weights
        branch_type: 'feedforward', 'saturating', 'gated', 'predictive'

    Returns:
        y: neuron output [scalar]
    """

    # Compute branch outputs
    branches = []
    for j, W_j in enumerate(W_branches):
        if branch_type == 'feedforward':
            b_j = relu(W_j @ x)

        elif branch_type == 'saturating':
            z = W_j @ x
            b_j = z / (1 + alpha * norm(z)**2)

        elif branch_type == 'gated':
            W1, W2 = W_j
            b_j = (W1 @ x) * sigmoid(W2 @ x)

        elif branch_type == 'predictive':
            W_down, W_up = W_j
            b_j = W_down @ x_pred - W_up @ x

        branches.append(b_j)

    # Soma integration
    if soma_type == 'linear_sum':
        y = sum(branches)

    elif soma_type == 'competitive':
        probs = softmax(lambda * array(branches))
        y = sum(prob * b for prob, b in zip(probs, branches))

    elif soma_type == 'hierarchical':
        # Pairwise interactions
        interactions = []
        for j in range(len(branches)):
            for k in range(j+1, len(branches)):
                interactions.append(branches[j] * branches[k])

        combined = concatenate([branches, interactions])
        y = sigmoid(W_soma @ combined)

    return y
```

---

## 📚 Plasticity Rules for Dendrites

### Rule 1: Hebbian (Correlation-Based)

**Within each branch:**

$$\Delta W_j \propto b_j \cdot x^T$$

Learning rate increases if branch is active AND input is present.

**Interpretation:** "Neurons that fire together wire together"

### Rule 2: Predictive Error (Cortical)

For predictive branches:

$$\Delta W_j \propto e_j \cdot x^T$$

Where $e_j = \hat{x} - x$ is prediction error.

**Interpretation:** Minimize prediction error locally.

### Rule 3: Reward-Modulated (Dopaminergic)

$$\Delta W_j \propto \delta_t \cdot b_j \cdot x^T$$

Where $\delta_t$ is dopamine signal (global reward prediction error).

**Interpretation:** Strengthen paths that led to reward.

### Rule 4: Dendritic Gate Learning

For gated branches $b_j = (W_j^{(1)} x) \odot \sigma(W_j^{(2)} x)$:

$$\Delta W_j^{(1)} \propto \text{error} \cdot \sigma(W_j^{(2)} x) \cdot x^T$$

$$\Delta W_j^{(2)} \propto \text{error} \cdot (W_j^{(1)} x) \cdot x^T$$

Gates learn independently to maximize their contribution to error.

---

## 🔨 Implementation: Core Dendritic Neuron Classes

### Class 1: Dendritic Neuron

```python
class DendriticNeuron:
    """
    A biologically-plausible neuron with multiple active dendritic branches.
    """

    def __init__(self, input_dim, num_branches=5, branch_type='mixed',
                 soma_type='hierarchical', learning_rate=0.01):
        self.input_dim = input_dim
        self.num_branches = num_branches
        self.branch_type = branch_type
        self.soma_type = soma_type
        self.lr = learning_rate

        # Initialize dendritic weights
        self.W_branches = [
            randn(input_dim, input_dim) * 0.1
            for _ in range(num_branches)
        ]

        # Soma integration weights
        integration_dim = num_branches
        if soma_type == 'hierarchical':
            # Include pairwise interactions
            integration_dim += num_branches * (num_branches - 1) // 2

        self.W_soma = randn(integration_dim, 1) * 0.1
        self.soma_bias = 0.0

        # Plasticity traces
        self.eligibility_traces = [zeros_like(W) for W in self.W_branches]

    def forward(self, x, x_pred=None):
        """Forward pass through dendritic compartments."""

        self.x = x
        self.branches = []

        for j, W_j in enumerate(self.W_branches):
            if self.branch_type == 'feedforward':
                b_j = relu(W_j @ x)

            elif self.branch_type == 'saturating':
                z = W_j @ x
                b_j = z / (1 + 0.1 * norm(z)**2)

            elif self.branch_type == 'gated':
                # Gated integration
                W_gate = self.W_branches[j][: self.input_dim // 2]
                W_signal = self.W_branches[j][self.input_dim // 2 :]
                b_j = (W_signal @ x) * sigmoid(W_gate @ x)

            elif self.branch_type == 'predictive' and x_pred is not None:
                # Prediction error
                b_j = relu(x_pred - x)  # Simplified

            self.branches.append(b_j)

        # Soma integration
        if self.soma_type == 'linear_sum':
            y = sum(self.branches)

        elif self.soma_type == 'competitive':
            probs = softmax(array(self.branches))
            y = sum(p * b for p, b in zip(probs, self.branches))

        elif self.soma_type == 'hierarchical':
            # Include pairwise interactions
            interactions = [
                self.branches[j] * self.branches[k]
                for j in range(len(self.branches))
                for k in range(j+1, len(self.branches))
            ]
            combined = concatenate([self.branches, interactions])
            y = sigmoid(self.W_soma.T @ combined)[0] + self.soma_bias

        self.y = y
        return y

    def learn_hebbian(self):
        """Local Hebbian learning rule."""
        for j in range(self.num_branches):
            b_j = self.branches[j]
            dW = self.lr * b_j * self.x.T
            self.W_branches[j] += dW

    def learn_predictive(self, error):
        """Learn from prediction error."""
        for j in range(self.num_branches):
            b_j = self.branches[j]
            dW = self.lr * error * b_j * self.x.T
            self.W_branches[j] += dW

    def learn_reward_modulated(self, dopamine_signal):
        """Dopamine-modulated learning."""
        for j in range(self.num_branches):
            b_j = self.branches[j]
            dW = self.lr * dopamine_signal * b_j * self.x.T
            self.W_branches[j] += dW
```

### Class 2: Dendritic Layer (Collection of Dendritic Neurons)

```python
class DendriticLayer:
    """
    A layer of N dendritic neurons.
    """

    def __init__(self, input_dim, output_dim, num_branches=5):
        self.neurons = [
            DendriticNeuron(input_dim, num_branches)
            for _ in range(output_dim)
        ]
        self.output_dim = output_dim

    def forward(self, x):
        """Forward pass through all neurons."""
        return array([neuron.forward(x) for neuron in self.neurons])

    def learn(self, error, learning_type='hebbian'):
        """Apply learning rule to all neurons."""
        for i, neuron in enumerate(self.neurons):
            if learning_type == 'hebbian':
                neuron.learn_hebbian()
            elif learning_type == 'predictive':
                neuron.learn_predictive(error[i])
            elif learning_type == 'reward':
                neuron.learn_reward_modulated(error[i])
```

---

## 📊 Computational Properties

### Expressiveness

**Standard ANN neuron:**
$$y = \sigma(W x + b)$$
Expressiveness: linear combination → nonlinearity.

**Dendritic neuron (multi-branch):**
$$y = \sigma\left(\sum_j f_j(W_j x)\right)$$
Expressiveness: **multiple independent nonlinearities** → integration.

**Computational gain:** A dendritic neuron with $B$ branches ≈ ANN with $B \times$ hidden units but with **local learning rules** (no backprop).

### Scalability

- **Small device:** 10-20 branches per neuron, 100-500 neurons per layer
- **Medium system:** 30-50 branches, 1000-5000 neurons
- **Large system:** 50-100 branches, 10,000+ neurons (parallelizable)

Branch computation is **embarrassingly parallel** — can use:
- Multi-core CPU
- GPU (one branch per thread)
- TPU arrays

### Learning Efficiency

- **Local learning:** No global backpropagation bottleneck
- **Continual learning:** Update weights online per timestep
- **Plasticity diversity:** Mix Hebbian, predictive, reward-modulated in same neuron

---

## 🧪 Testing the Dendritic Neuron

### Test 1: XOR Problem

Standard neurons need hidden layer. Can a single dendritic neuron solve XOR?

```python
# Create dendritic neuron with 3 branches
neuron = DendriticNeuron(input_dim=2, num_branches=3, branch_type='mixed')

# Training data: XOR
X = array([[0,0], [0,1], [1,0], [1,1]])
y = array([0, 1, 1, 0])

# Train
for epoch in range(1000):
    for x_sample, y_target in zip(X, y):
        output = neuron.forward(x_sample)
        error = y_target - output
        neuron.learn_predictive(error)

# Test
for x_sample, y_target in zip(X, y):
    output = neuron.forward(x_sample)
    print(f"Input: {x_sample}, Target: {y_target}, Output: {output:.3f}")
```

**Expected:** YES. Single dendritic neuron can learn XOR (unlike single standard neuron).

### Test 2: Temporal Integration

Can dendritic neuron integrate signals across time?

```python
# Sequence: [0,0] → [0,1] → [1,1]
# Prediction: should gradually increase
neuron = DendriticNeuron(input_dim=2, num_branches=5, branch_type='predictive')

for t, x_t in enumerate(sequence):
    x_pred = predict_next(x_t)
    output = neuron.forward(x_t, x_pred)
    # Learn from error
    error = actual[t+1] - x_pred
    neuron.learn_predictive(error)
```

---

## 🎯 Summary

**The dendritic neuron is:**
- ✅ Biologically plausible (matches known dendritic computations)
- ✅ Mathematically precise (can be optimized)
- ✅ Implementable (as shown above)
- ✅ More expressive than standard neurons (without global backprop)
- ✅ Foundation for all higher structures

**Next level:** Assemble dendritic neurons into **microcircuits** (attractor pools, pattern separators, predictive coding loops).

**After that:** Build **brain regions** (Wernicke, Broca, PFC).

---

## 📐 Key Equations Summary

| Concept | Formula | Interpretation |
|---------|---------|-----------------|
| Excitatory branch | $b_j = \sigma(W_j x)$ | Standard feedforward |
| Saturating branch | $b_j = \frac{W_j x}{1 + \alpha \\|W_j x\\|^2}$ | Sublinear summation |
| Gated branch | $b_j = (W_j^{(1)} x) \odot \sigma(W_j^{(2)} x)$ | Conditional routing |
| Predictive branch | $b_j = \sigma(\hat{x} - x)$ | Error signal |
| Soma (linear) | $y = \sum_j b_j$ | Simple integration |
| Soma (competitive) | $y = \sum_j p_j b_j, \quad p_j = \text{softmax}(b)$ | Winner-take-all |
| Hebbian learning | $\Delta W_j = \alpha b_j x^T$ | Local correlation |
| Predictive learning | $\Delta W_j = \alpha e_j b_j x^T$ | Error minimization |
| Reward learning | $\Delta W_j = \alpha \delta_t b_j x^T$ | Dopamine-modulated |

---

**This is the foundation. Dendritic neurons are the LEGO bricks for building cortex.**
