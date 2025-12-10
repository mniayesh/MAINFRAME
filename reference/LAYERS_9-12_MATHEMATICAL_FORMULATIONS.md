# Mathematical Formulations for Biological Layers 9-12
## Systems Through Metacognition: Complete Reference

**Document Purpose:** Comprehensive mathematical formulations, neural implementations, and parameter specifications for high-level cognitive layers.

**Scope:** Region/System → Network/Global Workspace → Cognitive Functions → Metacognition

**Date:** December 10, 2025

---

# LAYER 9: REGION/SYSTEM LAYER

## Overview

The Region/System Layer implements specialized computational zones with distinct topographic organizations, internal routing mechanisms, and pathway dynamics. This layer bridges local microcircuits to global brain networks.

---

## 9.1 Regional Specialization Models

### 9.1.1 Mathematical Framework

**Regional Specialization Function:**

Each brain region $R_i$ develops a specialization profile $S_i$ through activity-dependent learning:

$$S_i(t+1) = S_i(t) + \eta \cdot \nabla_{\theta_i} \mathcal{L}_{\text{task}}(x; \theta_i)$$

Where:
- $S_i$ = specialization vector (high values = preferred features)
- $\theta_i$ = region-specific parameters
- $\mathcal{L}_{\text{task}}$ = task-specific loss function
- $\eta$ = specialization learning rate (slow: 0.0001-0.001)

**Competitive Specialization Dynamics:**

Regions compete for task allocation via softmax specialization:

$$P(R_i | \text{task}) = \frac{\exp(\beta \cdot S_i \cdot \mathbf{t})}{\sum_{j} \exp(\beta \cdot S_j \cdot \mathbf{t})}$$

Where:
- $\mathbf{t}$ = task feature vector
- $\beta$ = competition strength (typically 5-10)

**Regional Efficiency Metric:**

Each region develops computational efficiency for its specialization:

$$E_i = \frac{\text{Performance}_i}{\text{Energy}_i \times \text{Latency}_i}$$

Regions with high $E_i$ for a task domain win long-term allocation.

### 9.1.2 Neural Circuit Implementation

**Canonical Regional Architecture:**

```
Input Layer (L4)
    ↓
Integration Layer (L2/3) ← Lateral inhibition (specialization sharpening)
    ↓
Output Layer (L5) → Feedforward to next region
    ↑
Feedback (L6) ← Prediction from higher regions
```

**Hebbian Specialization Rule:**

$$\Delta W_{ij} = \alpha \cdot r_i \cdot r_j \cdot (1 - S_{\text{overlap}})$$

Where $S_{\text{overlap}}$ = similarity to neighboring regions (promotes differentiation)

### 9.1.3 Governing Equations

**Regional Activity Dynamics:**

$$\tau_r \frac{dh_i}{dt} = -h_i + \sum_j W_{ij} r_j + I_{\text{ext}} + \xi(t)$$

Where:
- $h_i$ = membrane potential of region $i$
- $\tau_r$ = regional time constant (100-500ms)
- $W_{ij}$ = inter-regional connectivity
- $I_{\text{ext}}$ = external input
- $\xi(t)$ = noise term

**Firing Rate Transfer Function:**

$$r_i = \frac{r_{\max}}{1 + \exp(-\beta(h_i - \theta_i))}$$

### 9.1.4 Parameters

| Parameter | Symbol | Typical Value | Range | Units |
|-----------|--------|---------------|-------|-------|
| Regional time constant | $\tau_r$ | 200 | 100-500 | ms |
| Max firing rate | $r_{\max}$ | 100 | 50-200 | Hz |
| Specialization learning rate | $\eta$ | 0.001 | 0.0001-0.01 | - |
| Competition strength | $\beta$ | 7 | 5-15 | - |
| Lateral inhibition strength | $w_{\text{lat}}$ | -2.0 | -5.0 to -1.0 | mV |

---

## 9.2 Topographic Mapping Mathematics

### 9.2.1 Self-Organizing Maps (SOM)

**Kohonen Map Update Rule:**

$$\mathbf{w}_i(t+1) = \mathbf{w}_i(t) + \alpha(t) \cdot h_{ci}(t) \cdot [\mathbf{x}(t) - \mathbf{w}_i(t)]$$

Where:
- $\mathbf{w}_i$ = weight vector for neuron $i$
- $\alpha(t)$ = learning rate (decays: $\alpha(t) = \alpha_0 \exp(-t/\tau_\alpha)$)
- $h_{ci}(t)$ = neighborhood function centered on winner $c$

**Neighborhood Function:**

$$h_{ci}(t) = \exp\left(-\frac{||\mathbf{r}_c - \mathbf{r}_i||^2}{2\sigma^2(t)}\right)$$

Where:
- $\mathbf{r}_c, \mathbf{r}_i$ = spatial positions in map
- $\sigma(t)$ = neighborhood radius (shrinks over time)

### 9.2.2 Retinotopic/Tonotopic Organization

**Continuous Mapping Function:**

For visual space $(x_v, y_v)$ to cortical space $(x_c, y_c)$:

$$x_c = k_1 \log(1 + k_2 x_v)$$
$$y_c = k_3 \log(1 + k_4 y_v)$$

This captures the logarithmic magnification of central (foveal) regions.

**Magnification Factor:**

$$M(r) = \frac{d(\text{cortical distance})}{d(\text{visual angle})} = \frac{k}{r + r_0}$$

Where $r$ = eccentricity from fovea/center

### 9.2.3 Parameters

| Parameter | Symbol | Value | Range | Units |
|-----------|--------|-------|-------|-------|
| Initial learning rate | $\alpha_0$ | 0.5 | 0.1-0.9 | - |
| Learning rate decay | $\tau_\alpha$ | 10000 | 5000-50000 | iterations |
| Initial neighborhood | $\sigma_0$ | 5.0 | 2.0-10.0 | neurons |
| Final neighborhood | $\sigma_\infty$ | 0.5 | 0.1-1.0 | neurons |
| Magnification constant | $k$ | 15.0 | 10-25 | mm/degree |

---

## 9.3 Information Routing Principles

### 9.3.1 Attention-Based Routing

**Routing Weight Matrix:**

$$R_{ij}(t) = \text{softmax}_j\left(\frac{Q_i K_j^T}{\sqrt{d_k}} + b_{\text{att}}(t)\right)$$

Where:
- $R_{ij}$ = routing strength from region $i$ to region $j$
- $Q_i$ = query from region $i$
- $K_j$ = key from region $j$
- $b_{\text{att}}(t)$ = top-down attention bias

**Routed Signal:**

$$h_j^{\text{routed}} = \sum_i R_{ij} \cdot V_i$$

Where $V_i$ = value (message) from region $i$

### 9.3.2 Dynamic Pathway Selection

**Pathway Gating:**

Each pathway $p$ has a gating variable $g_p(t) \in [0,1]$:

$$g_p(t) = \sigma\left(\sum_k w_k^p \cdot s_k(t) - \theta_p\right)$$

Where:
- $s_k(t)$ = contextual signals (task demand, neuromodulation, etc.)
- $w_k^p$ = pathway sensitivity to signal $k$
- $\theta_p$ = pathway threshold

**Information Flow:**

$$I_{\text{path}}(t) = g_p(t) \cdot f_p(I_{\text{in}}(t))$$

### 9.3.3 Predictive Routing

**Bayesian Route Selection:**

$$P(\text{route}_j | \mathbf{x}, \mathbf{g}) = \frac{P(\mathbf{x} | \text{route}_j, \mathbf{g}) \cdot P(\text{route}_j | \mathbf{g})}{\sum_k P(\mathbf{x} | \text{route}_k, \mathbf{g}) \cdot P(\text{route}_k | \mathbf{g})}$$

Where:
- $\mathbf{x}$ = input signal
- $\mathbf{g}$ = current goal/context
- $P(\text{route}_j | \mathbf{g})$ = prior probability (learned task statistics)

### 9.3.4 Parameters

| Parameter | Symbol | Value | Range | Units |
|-----------|--------|-------|-------|-------|
| Routing temperature | $T_{\text{route}}$ | 0.5 | 0.1-2.0 | - |
| Pathway threshold | $\theta_p$ | 0.5 | 0.2-0.8 | - |
| Attention key dimension | $d_k$ | 128 | 64-512 | - |
| Context integration time | $\tau_{\text{context}}$ | 500 | 200-1000 | ms |

---

## 9.4 Pathway Dynamics

### 9.4.1 Synaptic Transmission Delays

**Axonal Conduction Model:**

$$v_{\text{conduct}} = \frac{d}{\tau_{\text{axon}}} = \frac{d}{d/v_0}$$

Where:
- $v_0$ = base conduction velocity (0.5-120 m/s depending on myelination)
- $d$ = pathway distance
- $\tau_{\text{axon}}$ = transmission delay

**Delay Distribution:**

For pathway of length $L$ with $N$ synapses:

$$\tau_{\text{total}} = \tau_{\text{axon}} + N \cdot \tau_{\text{syn}}$$

Where $\tau_{\text{syn}}$ = synaptic delay (0.5-2 ms per synapse)

### 9.4.2 Pathway Plasticity

**Pathway Strengthening:**

Activity-dependent pathway enhancement:

$$\frac{dW_p}{dt} = \eta_p \cdot \text{corr}(A_{\text{pre}}, A_{\text{post}}) - \lambda_p \cdot W_p$$

Where:
- $W_p$ = pathway efficacy
- $\text{corr}$ = correlation between pre- and post-synaptic regions
- $\lambda_p$ = decay rate

**Pathway Pruning:**

Inactive pathways decay:

$$W_p(t+1) = \begin{cases}
W_p(t) \cdot (1 - \delta_{\text{prune}}) & \text{if } A_p < \theta_{\text{activity}} \\
W_p(t) & \text{otherwise}
\end{cases}$$

### 9.4.3 Multi-Timescale Pathway Dynamics

**Fast Dynamics (Spiking):**

$$\tau_{\text{fast}} \frac{dI_p}{dt} = -I_p + \sum_{\text{spikes}} W_p \cdot \delta(t - t_{\text{spike}})$$

**Medium Dynamics (Synaptic Depression/Facilitation):**

$$\frac{dx}{dt} = \frac{1-x}{\tau_{\text{rec}}} - u \cdot x \cdot \delta_{\text{spike}}$$
$$\frac{du}{dt} = \frac{U-u}{\tau_{\text{fac}}} + U(1-u) \cdot \delta_{\text{spike}}$$

Where:
- $x$ = available synaptic resources (0-1)
- $u$ = release probability
- $U$ = baseline release probability

**Slow Dynamics (Structural Plasticity):**

$$\tau_{\text{struct}} \frac{dN_{\text{syn}}}{dt} = \alpha_{\text{growth}} \cdot A_p - \beta_{\text{prune}} \cdot (1-A_p)$$

Where $N_{\text{syn}}$ = number of synapses in pathway

### 9.4.4 Parameters

| Parameter | Symbol | Value | Range | Units |
|-----------|--------|-------|-------|-------|
| Unmyelinated velocity | $v_{\text{slow}}$ | 2 | 0.5-5 | m/s |
| Myelinated velocity | $v_{\text{fast}}$ | 80 | 50-120 | m/s |
| Synaptic delay | $\tau_{\text{syn}}$ | 1.0 | 0.5-2.0 | ms |
| Depression time constant | $\tau_{\text{rec}}$ | 800 | 200-1500 | ms |
| Facilitation time constant | $\tau_{\text{fac}}$ | 100 | 50-500 | ms |
| Structural plasticity time | $\tau_{\text{struct}}$ | 3600000 | 1800000-7200000 | ms (hours) |

---

## 9.5 Neural Field Theory for Regions

### 9.5.1 Wilson-Cowan Equations for Regional Activity

**Population Activity Dynamics:**

$$\tau_E \frac{dE(\mathbf{x},t)}{dt} = -E(\mathbf{x},t) + S_E\left(\int w_{EE}(\mathbf{x},\mathbf{x}') E(\mathbf{x}',t) d\mathbf{x}' - \int w_{EI}(\mathbf{x},\mathbf{x}') I(\mathbf{x}',t) d\mathbf{x}' + P(\mathbf{x},t)\right)$$

$$\tau_I \frac{dI(\mathbf{x},t)}{dt} = -I(\mathbf{x},t) + S_I\left(\int w_{IE}(\mathbf{x},\mathbf{x}') E(\mathbf{x}',t) d\mathbf{x}' - \int w_{II}(\mathbf{x},\mathbf{x}') I(\mathbf{x}',t) d\mathbf{x}'\right)$$

Where:
- $E(\mathbf{x},t)$ = excitatory population activity at position $\mathbf{x}$
- $I(\mathbf{x},t)$ = inhibitory population activity
- $w_{XY}(\mathbf{x},\mathbf{x}')$ = connectivity kernel from population $Y$ to $X$
- $S_E, S_I$ = sigmoid activation functions
- $P(\mathbf{x},t)$ = external input

**Connection Kernel (Mexican Hat):**

$$w_{EE}(\mathbf{x},\mathbf{x}') = A_E \exp\left(-\frac{||\mathbf{x}-\mathbf{x}'||^2}{2\sigma_E^2}\right)$$

$$w_{EI}(\mathbf{x},\mathbf{x}') = A_I \exp\left(-\frac{||\mathbf{x}-\mathbf{x}'||^2}{2\sigma_I^2}\right)$$

With $A_E > 0, \sigma_E < \sigma_I$ (local excitation, surround inhibition)

### 9.5.2 Traveling Wave Solutions

**Wave Equation for Activity Propagation:**

$$\frac{\partial^2 u}{\partial t^2} = c^2 \nabla^2 u - \gamma \frac{\partial u}{\partial t} + f(u)$$

Where:
- $c$ = wave speed
- $\gamma$ = damping coefficient
- $f(u)$ = nonlinear activation

**Oscillatory Patterns:**

Regional oscillations emerge from:

$$u(\mathbf{x},t) = A(\mathbf{x}) \sin(\omega t + \phi(\mathbf{x}))$$

Where phase gradient $\nabla \phi$ determines wave direction.

### 9.5.3 Parameters

| Parameter | Symbol | Value | Range | Units |
|-----------|--------|-------|-------|-------|
| Excitatory time constant | $\tau_E$ | 10 | 5-20 | ms |
| Inhibitory time constant | $\tau_I$ | 20 | 10-50 | ms |
| Excitatory kernel width | $\sigma_E$ | 0.5 | 0.2-1.0 | mm |
| Inhibitory kernel width | $\sigma_I$ | 2.0 | 1.0-5.0 | mm |
| Wave speed | $c$ | 0.3 | 0.1-1.0 | m/s |

---

# LAYER 10: NETWORK/GLOBAL WORKSPACE LAYER

## Overview

The Network/Global Workspace Layer implements large-scale coordination across brain regions through broadcast mechanisms, competitive dynamics, and oscillatory synchronization. This is the substrate for conscious access and flexible cognition.

---

## 10.1 Global Workspace Theory

### 10.1.1 Mathematical Framework

**Workspace Contents:**

The global workspace at time $t$ contains a set of representations $\mathcal{W}(t)$:

$$\mathcal{W}(t) = \{r_i : s_i(t) > \theta_{\text{broadcast}}\}$$

Where:
- $r_i$ = representation from region $i$
- $s_i(t)$ = salience/activation strength
- $\theta_{\text{broadcast}}$ = broadcast threshold

**Broadcast Amplification:**

When $r_i$ enters workspace, it receives amplification:

$$A_i^{\text{broadcast}}(t) = A_i^{\text{local}}(t) \times G_{\text{broadcast}}$$

Where $G_{\text{broadcast}} = 10-100$ (amplification gain)

**Global Availability:**

All regions receive broadcast:

$$I_j^{\text{workspace}}(t) = \sum_{i \in \mathcal{W}(t)} w_{ji} \cdot A_i^{\text{broadcast}}(t)$$

### 10.1.2 Winner-Take-All Dynamics at Network Scale

**Competition Equation:**

$$\frac{dx_i}{dt} = -x_i + f(s_i - \beta \sum_{j \neq i} x_j) + \xi_i$$

Where:
- $x_i$ = activation of representation $i$
- $s_i$ = input strength
- $\beta$ = lateral inhibition strength
- $f$ = rectified nonlinearity
- $\xi_i$ = noise

**Softmax Selection (Probabilistic):**

$$P(r_i \in \mathcal{W}) = \frac{\exp(\gamma \cdot s_i)}{\sum_j \exp(\gamma \cdot s_j)}$$

Where $\gamma$ = inverse temperature (high $\gamma$ = sharp winner selection)

### 10.1.3 Workspace Capacity Limit

**Limited Capacity (Miller's Law):**

$$|\mathcal{W}(t)| \leq K$$

Where $K \approx 4-7$ (working memory capacity)

**Information Bottleneck:**

Workspace acts as information bottleneck:

$$I(\mathcal{W}; \mathcal{R}) \leq \log_2(K) + H(\mathcal{W})$$

Where:
- $\mathcal{R}$ = all regional representations
- $I$ = mutual information
- $H$ = entropy

### 10.1.4 Parameters

| Parameter | Symbol | Value | Range | Units |
|-----------|--------|-------|-------|-------|
| Broadcast threshold | $\theta_{\text{broadcast}}$ | 0.7 | 0.5-0.9 | normalized |
| Amplification gain | $G_{\text{broadcast}}$ | 50 | 10-100 | - |
| Lateral inhibition | $\beta$ | 0.5 | 0.1-1.0 | - |
| Workspace capacity | $K$ | 5 | 4-7 | items |
| Selection temperature | $\gamma$ | 10 | 5-20 | - |

---

## 10.2 Competition and Cooperation Dynamics

### 10.2.1 Competitive Selection Model

**Biased Competition:**

$$\tau \frac{da_i}{dt} = -a_i + (1-a_i) \cdot I_i^{\text{exc}} - a_i \cdot I_i^{\text{inh}}$$

Where:
- $I_i^{\text{exc}} = s_i + \text{att}_i$ (stimulus + attention)
- $I_i^{\text{inh}} = \sum_{j \neq i} w_{ij} a_j$ (competition from others)

**Attention Modulation:**

$$\text{att}_i = \alpha_{\text{top-down}} \cdot \text{match}(r_i, g_{\text{goal}})$$

Where:
- $\alpha_{\text{top-down}}$ = attention strength
- $g_{\text{goal}}$ = current goal representation

### 10.2.2 Cooperative Binding

**Synchronized Coalitions:**

Representations bind by phase synchronization:

$$\frac{d\phi_i}{dt} = \omega_i + \sum_{j \in \text{coalition}} K_{ij} \sin(\phi_j - \phi_i)$$

Where:
- $\phi_i$ = phase of oscillation for representation $i$
- $K_{ij}$ = coupling strength
- Coalition = coherent phase cluster

**Binding Strength:**

$$B_{ij} = \langle \cos(\phi_i(t) - \phi_j(t)) \rangle_t$$

Strong binding: $B_{ij} \approx 1$ (synchronized)

### 10.2.3 Meta-Stable States

Workspace dynamics exhibit meta-stability:

$$\tau_{\text{switch}} = \tau_0 \exp\left(\frac{\Delta E}{kT_{\text{noise}}}\right)$$

Where:
- $\Delta E$ = energy barrier between workspace states
- $T_{\text{noise}}$ = effective noise temperature
- Typical $\tau_{\text{switch}} \approx 100-500$ ms

### 10.2.4 Parameters

| Parameter | Symbol | Value | Range | Units |
|-----------|--------|-------|-------|-------|
| Competition time constant | $\tau$ | 50 | 20-100 | ms |
| Attention strength | $\alpha_{\text{top-down}}$ | 2.0 | 1.0-5.0 | - |
| Coupling strength | $K_{ij}$ | 0.5 | 0.1-2.0 | - |
| Switching time | $\tau_{\text{switch}}$ | 300 | 100-800 | ms |

---

## 10.3 Broadcast Mechanisms

### 10.3.1 Divergent Broadcast Architecture

**Fan-Out Connectivity:**

Workspace neurons project to N target regions:

$$\text{Fan-out} = \frac{\sum_i N_{\text{targets}}(i)}{N_{\text{workspace}}}$$

Typically: Fan-out $\approx 1000-10000$ (massively divergent)

**Broadcast Signal:**

$$B(t) = \sum_{i \in \mathcal{W}(t)} w_i \cdot r_i(t)$$

Where $w_i$ = broadcast weight (strength of representation)

### 10.3.2 Thalamo-Cortical Broadcast Loop

**Thalamic Relay:**

$$T(t) = f_{\text{thal}}(C_{\text{cortex}}(t))$$
$$C_{\text{cortex}}(t+\Delta t) = f_{\text{cortex}}(T(t) + I_{\text{sensory}}(t))$$

Implements recurrent broadcast loop with delay $\Delta t \approx 10-20$ ms

**Ignition Criterion:**

Workspace "ignites" when:

$$\sum_{i} a_i(t) > \Theta_{\text{ignition}} \text{ AND } \sum_{i,j} a_i a_j C_{ij} > \Theta_{\text{coherence}}$$

Where:
- $\Theta_{\text{ignition}}$ = total activity threshold
- $C_{ij}$ = correlation between regions $i,j$
- $\Theta_{\text{coherence}}$ = synchrony threshold

### 10.3.3 Sustained Activity Mechanism

**Recurrent Maintenance:**

$$\tau_{\text{WM}} \frac{da}{dt} = -a + f(Wa + I_{\text{broadcast}} + I_{\text{ext}})$$

Where:
- $W$ = recurrent weight matrix (strong recurrence maintains activity)
- $I_{\text{broadcast}}$ = ongoing workspace input
- Stable states exist when $f(Wa) \approx a$

### 10.3.4 Parameters

| Parameter | Symbol | Value | Range | Units |
|-----------|--------|-------|-------|-------|
| Broadcast fan-out | - | 5000 | 1000-10000 | targets/neuron |
| Ignition threshold | $\Theta_{\text{ignition}}$ | 0.6 | 0.4-0.8 | normalized |
| Coherence threshold | $\Theta_{\text{coherence}}$ | 0.5 | 0.3-0.7 | - |
| Thalamic delay | $\Delta t$ | 15 | 10-25 | ms |
| Working memory time const | $\tau_{\text{WM}}$ | 1000 | 500-2000 | ms |

---

## 10.4 Binding by Synchrony

### 10.4.1 Phase Locking Mechanisms

**Kuramoto Model:**

$$\frac{d\theta_i}{dt} = \omega_i + \frac{K}{N} \sum_{j=1}^N \sin(\theta_j - \theta_i)$$

Where:
- $\theta_i$ = phase of oscillator $i$
- $\omega_i$ = natural frequency
- $K$ = coupling strength

**Order Parameter:**

Synchronization measured by:

$$r e^{i\psi} = \frac{1}{N} \sum_{j=1}^N e^{i\theta_j}$$

Where:
- $r \in [0,1]$ = synchronization strength
- $\psi$ = mean phase
- $r \approx 1$ = full synchrony, $r \approx 0$ = no synchrony

### 10.4.2 Gamma-Band Binding

**Pyramidal-Interneuron Gamma (PING):**

$$\tau_E \frac{dE}{dt} = -E + S(I_E - g_{EI} I)$$
$$\tau_I \frac{dI}{dt} = -I + S(g_{IE} E - I_I)$$

Produces gamma oscillations (30-80 Hz) when:
- $g_{EI}$ (E→I) and $g_{IE}$ (I→E) sufficiently strong
- $\tau_E < \tau_I$ (E faster than I)

**Coherence Measure:**

$$\text{Coh}_{ij}(f) = \frac{|S_{ij}(f)|^2}{S_{ii}(f) S_{jj}(f)}$$

Where $S_{ij}(f)$ = cross-spectral density at frequency $f$

### 10.4.3 Communication Through Coherence

**Phase-Amplitude Coupling:**

Low frequency phase modulates high frequency amplitude:

$$A_{\text{high}}(t) = A_0 + A_1 \cos(\phi_{\text{low}}(t))$$

Enables hierarchical information integration.

**Effective Connectivity:**

$$\text{EC}_{i \to j} = \text{Coh}_{ij}(\omega) \times \Delta \phi_{ij}$$

Where $\Delta \phi_{ij}$ = phase lead/lag (determines direction)

### 10.4.4 Parameters

| Parameter | Symbol | Value | Range | Units |
|-----------|--------|-------|-------|-------|
| Coupling strength | $K$ | 1.5 | 0.5-5.0 | - |
| Gamma frequency | $f_\gamma$ | 50 | 30-80 | Hz |
| Beta frequency | $f_\beta$ | 20 | 15-30 | Hz |
| Theta frequency | $f_\theta$ | 6 | 4-8 | Hz |
| PING E time constant | $\tau_E$ | 10 | 5-15 | ms |
| PING I time constant | $\tau_I$ | 20 | 10-30 | ms |

---

# LAYER 11: COGNITIVE FUNCTION LAYER

## Overview

The Cognitive Function Layer implements high-level cognitive operations: working memory maintenance, attention control, decision-making, and planning. These functions emerge from coordinated regional and network dynamics.

---

## 11.1 Working Memory Models

### 11.1.1 Attractor Dynamics Model

**Multi-Stable Attractor Network:**

$$\tau \frac{dh_i}{dt} = -h_i + \sum_j W_{ij} f(h_j) + I_i + \eta_i$$

Where:
- $W_{ij}$ has structure supporting multiple fixed points
- Each fixed point = stored memory item

**Capacity:**

Number of stable attractors:

$$C \approx \frac{\alpha N}{\log N}$$

Where:
- $N$ = number of neurons
- $\alpha \approx 0.14$ (empirical constant)

**Maintenance Energy:**

Sustained activity requires:

$$E_{\text{maintain}} = \int_0^T \sum_i r_i^2(t) dt$$

### 11.1.2 Synaptic Theory (Mongillo Model)

**Calcium-Based Working Memory:**

$$\frac{dx}{dt} = -\frac{x}{\tau_x} + \gamma (1-x) S(t)$$

$$\frac{dCa}{dt} = -\frac{Ca}{\tau_{Ca}} + \alpha u x S(t)$$

$$\frac{du}{dt} = -\frac{u-U}{\tau_u} + U(1-u) S(t)$$

Where:
- $x$ = available resources
- $Ca$ = calcium concentration (memory trace)
- $u$ = release probability
- $S(t)$ = spike train

Memory persists via elevated $Ca$ for seconds without spiking.

### 11.1.3 Prefrontal Delay Activity

**Persistent Activity Equation:**

$$\tau \frac{dr}{dt} = -r + f\left(\sum_j W_{ij} r_j + h + I_{\text{stim}}\right)$$

With strong recurrent weights $W_{ij}$ supporting bistability.

**Bump Attractor for Spatial WM:**

$$W(x,x') = J_0 - J_1 \cos(x - x')$$

Supports spatially tuned persistent activity bumps.

### 11.1.4 Parameters

| Parameter | Symbol | Value | Range | Units |
|-----------|--------|-------|-------|-------|
| WM time constant | $\tau$ | 1000 | 500-2000 | ms |
| Capacity | $C$ | 4 | 3-7 | items |
| Calcium decay | $\tau_{Ca}$ | 3000 | 1000-10000 | ms |
| Resource recovery | $\tau_x$ | 800 | 500-1500 | ms |
| Recurrent strength | $J_0$ | 2.5 | 2.0-4.0 | - |

---

## 11.2 Attention Mechanisms

### 11.2.1 Biased Competition Model

**Attention as Gain Modulation:**

$$r_i^{\text{attended}} = g(\alpha) \cdot r_i^{\text{unattended}}$$

Where:
- $g(\alpha) = 1 + \alpha$ (multiplicative gain)
- $\alpha \in [0, 2]$ (attention strength)

**Competition Equation:**

$$\frac{dr_i}{dt} = -r_i + f\left(\text{input}_i + \alpha_i - \beta \sum_{j \neq i} r_j\right)$$

Where:
- $\alpha_i$ = top-down attention to item $i$
- $\beta$ = competition strength

### 11.2.2 Normalization Model of Attention

**Divisive Normalization:**

$$r_i = \frac{c_i s_i}{\sigma + \sum_j s_j}$$

Where:
- $c_i$ = attention field at location $i$
- $s_i$ = stimulus drive
- $\sigma$ = semi-saturation constant

**Attention Field:**

$$c(x) = A \exp\left(-\frac{(x-x_{\text{att}})^2}{2\sigma_{\text{att}}^2}\right)$$

Gaussian spotlight centered at attended location.

### 11.2.3 Feature-Based Attention

**Template Matching:**

$$\alpha_i = \text{match}(f_i, f_{\text{target}}) = \frac{f_i \cdot f_{\text{target}}}{||f_i|| \cdot ||f_{\text{target}}||}$$

Where:
- $f_i$ = features at location $i$
- $f_{\text{target}}$ = attended feature template

### 11.2.4 Parameters

| Parameter | Symbol | Value | Range | Units |
|-----------|--------|-------|-------|-------|
| Attention gain | $\alpha$ | 1.5 | 1.0-3.0 | - |
| Competition | $\beta$ | 0.3 | 0.1-0.5 | - |
| Semi-saturation | $\sigma$ | 0.5 | 0.1-1.0 | - |
| Spotlight width | $\sigma_{\text{att}}$ | 2.0 | 1.0-5.0 | degrees visual angle |
| Attention shift time | $\tau_{\text{shift}}$ | 200 | 100-400 | ms |

---

## 11.3 Decision-Making Models

### 11.3.1 Drift-Diffusion Model (DDM)

**Evidence Accumulation:**

$$dx = \mu \cdot dt + \sigma \cdot dW$$

Where:
- $x$ = accumulated evidence
- $\mu$ = drift rate (depends on stimulus strength)
- $\sigma$ = noise diffusion coefficient
- $dW$ = Wiener process increment

**Decision Rule:**

Decide for option A when $x$ reaches threshold $a$, option B when reaches $-b$.

**Reaction Time Distribution:**

$$RT = \frac{a}{\mu} + T_{\text{non-decision}}$$

(for simple case $a=b$, high signal-to-noise)

### 11.3.2 Attractor Model of Decision-Making

**Two-Pool Competition:**

$$\tau \frac{dr_1}{dt} = -r_1 + f(W_{11} r_1 - W_{12} r_2 + I_1)$$
$$\tau \frac{dr_2}{dt} = -r_2 + f(W_{22} r_2 - W_{21} r_1 + I_2)$$

Where:
- $r_1, r_2$ = firing rates for option 1, 2
- $W_{ii}$ = recurrent excitation
- $W_{ij}$ = mutual inhibition
- $I_i$ = evidence for option $i$

**Winning Pool:**

Decision made when $r_i > \theta_{\text{decision}}$ and $r_i - r_j > \Delta_{\text{min}}$

### 11.3.3 Urgency Signal

**Time-Dependent Threshold:**

$$\theta(t) = \theta_0 - k \cdot t$$

Decreasing threshold creates urgency, speeds decisions under time pressure.

**Urgency Gating:**

$$u(t) = u_0 + \beta_u \cdot t$$

Multiplicatively gates sensory evidence:

$$\frac{dx}{dt} = u(t) \cdot \mu + \sigma \cdot \xi(t)$$

### 11.3.4 Parameters

| Parameter | Symbol | Value | Range | Units |
|-----------|--------|-------|-------|-------|
| Drift rate | $\mu$ | 0.3 | 0.1-1.0 | evidence/s |
| Noise | $\sigma$ | 0.1 | 0.05-0.3 | - |
| Threshold | $a, b$ | 1.0 | 0.5-2.0 | evidence units |
| Non-decision time | $T_{\text{non-decision}}$ | 300 | 200-500 | ms |
| Urgency rate | $\beta_u$ | 0.001 | 0.0005-0.005 | 1/ms |

---

## 11.4 Planning and Sequence Generation

### 11.4.1 Tree Search Model

**Forward Simulation:**

State-action tree expansion:

$$V(s) = \max_a \left[R(s,a) + \gamma \sum_{s'} P(s'|s,a) V(s')\right]$$

With:
- $V(s)$ = value of state $s$
- $R(s,a)$ = immediate reward
- $\gamma$ = discount factor
- $P(s'|s,a)$ = transition probability

**Limited Depth:**

Brain approximates with depth $d \approx 3-5$ steps:

$$V_d(s) = \max_a \left[R(s,a) + \gamma \sum_{s'} P(s'|s,a) V_{d-1}(s')\right]$$

### 11.4.2 Trajectory Optimization

**Model-Based Control:**

$$\min_{\mathbf{u}} \sum_{t=0}^T \left[C(x_t, u_t) + \lambda ||\mathbf{u}||^2\right]$$

Subject to:
$$x_{t+1} = f(x_t, u_t)$$

Where:
- $\mathbf{u} = (u_0, ..., u_T)$ = action sequence
- $C(x,u)$ = cost function
- $f$ = forward model (learned or known)

### 11.4.3 Hierarchical Planning

**Goal Decomposition:**

High-level goal $G$ decomposes into subgoals:

$$G = \langle g_1, g_2, ..., g_n \rangle$$

Each $g_i$ achieved by policy $\pi_i$:

$$\pi_i : S \to A$$

**Options Framework:**

Option $o = \langle I_o, \pi_o, \beta_o \rangle$:
- $I_o$ = initiation set (when option available)
- $\pi_o$ = option policy
- $\beta_o$ = termination condition

### 11.4.4 Sequence Learning via SMA/Pre-SMA

**Chunking Mechanism:**

Frequently co-occurring actions $(a_1, a_2, ..., a_k)$ bind into chunk $C$:

$$P(C) = \prod_{i=1}^k P(a_i | a_{i-1}) \quad \text{if} \quad P > \theta_{\text{chunk}}$$

**Sequence Representation:**

Neurons encode ordinal position:

$$r_i(t) \propto \exp\left(-\frac{(t - t_i)^2}{2\sigma_t^2}\right)$$

Where $t_i$ = preferred time in sequence.

### 11.4.5 Parameters

| Parameter | Symbol | Value | Range | Units |
|-----------|--------|-------|-------|-------|
| Planning depth | $d$ | 4 | 2-6 | steps |
| Discount factor | $\gamma$ | 0.95 | 0.9-0.99 | - |
| Control cost weight | $\lambda$ | 0.01 | 0.001-0.1 | - |
| Chunk threshold | $\theta_{\text{chunk}}$ | 0.8 | 0.6-0.95 | probability |
| Sequence time width | $\sigma_t$ | 100 | 50-200 | ms |

---

# LAYER 12: METACOGNITIVE/INTROSPECTION LAYER

## Overview

The Metacognitive Layer monitors and controls the cognitive system itself: detecting errors, estimating confidence, predicting performance, and adapting learning strategies. This is "thinking about thinking."

---

## 12.1 Error Monitoring

### 12.1.1 Prediction Error Signals

**Hierarchical Prediction Errors:**

At each level $l$:

$$e_l(t) = x_l(t) - \hat{x}_l(t|h_{l-1})$$

Where:
- $x_l$ = actual representation at level $l$
- $\hat{x}_l$ = prediction from level $l-1$

**Precision-Weighted Errors:**

$$\epsilon_l = \Pi_l \cdot e_l$$

Where $\Pi_l$ = precision (inverse variance) of prediction at level $l$

### 12.1.2 Anterior Cingulate Error Detection

**Conflict Monitoring Theory:**

$$\text{Conflict} = \sum_{i \neq j} a_i \cdot a_j$$

High conflict when multiple responses co-activated.

**Error-Related Negativity (ERN):**

$$\text{ERN}(t) = k \cdot |r_{\text{correct}} - r_{\text{chosen}}|$$

Appears ~50-100ms after error commission.

**Error Likelihood:**

$$P(\text{error} | \text{conflict}, RT, \text{confidence}) = \sigma(w_1 \cdot \text{conflict} - w_2 \cdot \text{confidence} + w_3 / RT)$$

### 12.1.3 Adaptive Control

**Post-Error Slowing:**

$$RT_{n+1} = RT_n + \Delta RT_{\text{error}}$$

Where $\Delta RT_{\text{error}} \approx 50-200$ ms

**Error-Triggered Learning Rate Increase:**

$$\alpha_{n+1} = \min(\alpha_n \cdot (1 + k_{\text{error}}), \alpha_{\max})$$

### 12.1.4 Parameters

| Parameter | Symbol | Value | Range | Units |
|-----------|--------|-------|-------|-------|
| Error boost factor | $k_{\text{error}}$ | 2.0 | 1.5-5.0 | - |
| Post-error slowing | $\Delta RT_{\text{error}}$ | 100 | 50-300 | ms |
| Conflict weight | $w_1$ | 1.5 | 1.0-3.0 | - |
| Confidence weight | $w_2$ | 2.0 | 1.0-4.0 | - |
| ERN latency | - | 75 | 50-120 | ms |

---

## 12.2 Confidence Estimation

### 12.2.1 Evidence-Based Confidence

**Decision Variable Distance:**

$$\text{Confidence} = \frac{|DV_{\text{chosen}} - DV_{\text{alternative}}|}{DV_{\text{chosen}} + DV_{\text{alternative}}}$$

Where $DV$ = decision variable (accumulated evidence)

**Probability Correct:**

$$P(\text{correct}) = \Phi\left(\frac{\mu \cdot T}{\sigma \sqrt{T}}\right)$$

Where:
- $\Phi$ = cumulative normal distribution
- $T$ = decision time
- $\mu, \sigma$ from drift-diffusion

### 12.2.2 Balance of Evidence Model

**Log Posterior Ratio:**

$$\log \frac{P(H_1|x)}{P(H_2|x)} = \log \frac{P(H_1)}{P(H_2)} + \sum_t \log \frac{P(x_t|H_1)}{P(x_t|H_2)}$$

Confidence = absolute value of log posterior ratio.

### 12.2.3 Metacognitive Sensitivity

**Meta-d' (Metacognitive Efficiency):**

$$\text{meta-d'} = \Phi^{-1}(\text{Hit rate}) - \Phi^{-1}(\text{FA rate})$$

For confidence ratings predicting accuracy.

**Metacognitive Efficiency:**

$$\text{M-ratio} = \frac{\text{meta-d'}}{\text{d'}}$$

Perfect metacognition: M-ratio = 1.0

### 12.2.4 Parameters

| Parameter | Symbol | Value | Range | Units |
|-----------|--------|-------|-------|-------|
| Confidence slope | - | 0.5 | 0.3-1.0 | - |
| Metacognitive noise | $\sigma_{\text{meta}}$ | 0.2 | 0.1-0.5 | - |
| M-ratio (typical) | - | 0.7 | 0.5-1.0 | - |

---

## 12.3 Performance Prediction

### 12.3.1 Forward Model of Learning

**Predicted Learning Curve:**

$$\hat{P}(n) = P_\infty - (P_\infty - P_0) e^{-n/\tau_{\text{learn}}}$$

Where:
- $\hat{P}(n)$ = predicted performance after $n$ trials
- $P_\infty$ = asymptotic performance
- $\tau_{\text{learn}}$ = learning time constant

**Uncertainty:**

$$\sigma_{\hat{P}}^2(n) = \sigma_0^2 e^{-n/\tau_{\text{uncertainty}}}$$

Uncertainty decreases with experience.

### 12.3.2 Resource-Performance Mapping

**Performance as Function of Resources:**

$$P = f(T_{\text{time}}, E_{\text{effort}}, A_{\text{ability}})$$

Often modeled as:

$$P = A \cdot (1 - e^{-\lambda T}) \cdot g(E)$$

Where:
- $g(E) = \frac{E}{E + \sigma_E}$ (saturating function of effort)

### 12.3.3 Difficulty Estimation

**Subjective Difficulty:**

$$D = w_1 \cdot \text{RT} + w_2 \cdot (1 - \text{Confidence}) + w_3 \cdot \text{Errors}$$

**Optimal Difficulty (Flow State):**

$$D^* = C + \epsilon$$

Where:
- $C$ = current competence
- $\epsilon$ = small challenge margin

### 12.3.4 Parameters

| Parameter | Symbol | Value | Range | Units |
|-----------|--------|-------|-------|-------|
| Learning time constant | $\tau_{\text{learn}}$ | 50 | 20-200 | trials |
| Uncertainty decay | $\tau_{\text{uncertainty}}$ | 100 | 50-300 | trials |
| Effort weight | $\lambda$ | 0.1 | 0.05-0.5 | 1/min |
| Flow margin | $\epsilon$ | 0.1 | 0.05-0.2 | normalized |

---

## 12.4 Self-Modification Algorithms

### 12.4.1 Meta-Learning (Learning to Learn)

**MAML (Model-Agnostic Meta-Learning):**

$$\theta^* = \theta - \alpha \nabla_\theta \mathcal{L}_{\mathcal{T}_i}(f_\theta)$$

Meta-objective:

$$\min_\theta \sum_{\mathcal{T}_i} \mathcal{L}_{\mathcal{T}_i}(f_{\theta^*})$$

Learns initial parameters $\theta$ that adapt quickly to new tasks.

**Reptile (First-Order Approximation):**

$$\theta \leftarrow \theta + \beta (\theta^* - \theta)$$

Where $\theta^*$ = parameters after task-specific training.

### 12.4.2 Neural Architecture Search

**Strategy Adaptation:**

System learns which architectural components to activate:

$$a_{\text{component}}(t) = \sigma\left(\sum_k w_k \cdot p_k(t)\right)$$

Where:
- $p_k(t)$ = performance metrics
- $w_k$ = learned weights
- $a$ = activation/allocation to component

### 12.4.3 Hyperparameter Optimization

**Learning Rate Adaptation:**

$$\alpha(t) = \alpha_0 \cdot f(\nabla \mathcal{L}, \text{progress}, \text{stability})$$

Common forms:
- Exponential decay: $\alpha(t) = \alpha_0 e^{-\lambda t}$
- Step decay: $\alpha(t) = \alpha_0 \cdot 0.1^{\lfloor t / T_{\text{step}} \rfloor}$
- Adaptive (Adam-like): $\alpha_t = \alpha_0 / \sqrt{v_t + \epsilon}$

### 12.4.4 Curriculum Learning

**Difficulty Scheduling:**

Start with easy examples, gradually increase:

$$D(t) = D_{\min} + (D_{\max} - D_{\min}) \cdot s(t)$$

Where $s(t)$ = scheduling function (e.g., $s(t) = t/T$ for linear)

**Performance-Based Pacing:**

$$D(t+1) = \begin{cases}
D(t) + \Delta D & \text{if } P(t) > \theta_{\text{progress}} \\
D(t) - \Delta D & \text{if } P(t) < \theta_{\text{regress}} \\
D(t) & \text{otherwise}
\end{cases}$$

### 12.4.5 Parameters

| Parameter | Symbol | Value | Range | Units |
|-----------|--------|-------|-------|-------|
| Meta-learning rate | $\beta$ | 0.1 | 0.01-0.5 | - |
| Adaptation steps | $K$ | 5 | 3-10 | gradient steps |
| Initial learning rate | $\alpha_0$ | 0.001 | 0.0001-0.01 | - |
| LR decay rate | $\lambda$ | 0.0001 | 0.00001-0.001 | 1/iteration |
| Curriculum step size | $\Delta D$ | 0.1 | 0.05-0.2 | difficulty units |

---

## 12.5 Learning Rate Adaptation

### 12.5.1 Error-Driven Modulation

**Prediction Error Scaling:**

$$\alpha_{\text{effective}} = \alpha_{\text{base}} \cdot (1 + k \cdot |\text{PE}|)$$

Where:
- $\text{PE}$ = prediction error
- $k$ = error sensitivity (typically 1-5)

**Uncertainty Modulation:**

$$\alpha = \alpha_0 \cdot \frac{1}{\sigma^2 + \epsilon}$$

Higher uncertainty → higher learning rate.

### 12.5.2 Neuromodulatory Control

**Dopamine-Dependent Learning Rate:**

$$\alpha_{\text{DA}} = \alpha_0 \cdot (1 + \beta_{\text{DA}} \cdot [\text{DA}]_t)$$

Where $[\text{DA}]_t$ = dopamine concentration (reward prediction error signal)

**Norepinephrine (Unexpected Uncertainty):**

$$\alpha_{\text{NE}} = \alpha_0 \cdot (1 + \beta_{\text{NE}} \cdot [\text{NE}]_t)$$

High NE → reset learning, explore new strategies.

### 12.5.3 Context-Dependent Adaptation

**State-Dependent Learning Rates:**

$$\alpha(s) = \text{softmax}(\mathbf{w}^T \phi(s))$$

Where:
- $\phi(s)$ = state features
- $\mathbf{w}$ = learned mapping to learning rates

**Temporal Credit Assignment:**

Eligibility trace for delayed credit:

$$e_t = \gamma \lambda e_{t-1} + \nabla_\theta \log \pi(a_t|s_t)$$

Effective learning rate scaled by trace:

$$\Delta \theta = \alpha \cdot \delta_t \cdot e_t$$

### 12.5.4 Parameters

| Parameter | Symbol | Value | Range | Units |
|-----------|--------|-------|-------|-------|
| Error sensitivity | $k$ | 2.0 | 1.0-5.0 | - |
| DA modulation | $\beta_{\text{DA}}$ | 3.0 | 1.0-10.0 | - |
| NE modulation | $\beta_{\text{NE}}$ | 5.0 | 2.0-10.0 | - |
| Trace decay | $\lambda$ | 0.9 | 0.7-0.99 | - |

---

# INTEGRATION ACROSS LAYERS

## Hierarchical Information Flow

### Bottom-Up (Layers 9→12)

```
Regional Activity (Layer 9)
    ↓ (competition for broadcast)
Network Selection (Layer 10)
    ↓ (workspace contents → cognitive operations)
Cognitive Functions (Layer 11)
    ↓ (performance monitoring)
Metacognition (Layer 12)
    ↓ (adaptation signals)
    ↓
Back to Layers 9-11 (modulation)
```

### Top-Down (Layers 12→9)

```
Metacognitive Assessment (Layer 12)
    ↓ (learning rate, attention modulation)
Cognitive Control (Layer 11)
    ↓ (goal-directed attention, WM maintenance)
Network Gating (Layer 10)
    ↓ (pathway selection, broadcast control)
Regional Modulation (Layer 9)
    ↓
Modified Regional Dynamics
```

---

## Unified System Equations

**Complete System State:**

$$\mathbf{s}(t) = \begin{bmatrix}
\mathbf{r}_{\text{regional}}(t) \\
\mathbf{w}_{\text{workspace}}(t) \\
\mathbf{c}_{\text{cognitive}}(t) \\
\mathbf{m}_{\text{meta}}(t)
\end{bmatrix}$$

**Coupled Dynamics:**

$$\frac{d\mathbf{s}}{dt} = \mathbf{F}(\mathbf{s}, \mathbf{I}_{\text{ext}}, \mathbf{\theta}(t))$$

Where $\mathbf{\theta}(t)$ = time-varying parameters (learning rates, attention, etc.) controlled by Layer 12.

---

## Implementation Strategy

### Phase 1: Regional Specialization (Layer 9)
- Implement 3-5 specialized regions
- Self-organizing topographic maps
- Dynamic routing between regions
- **Timeline:** 4 weeks

### Phase 2: Global Workspace (Layer 10)
- Winner-take-all network
- Broadcast mechanism
- Gamma-band synchronization
- **Timeline:** 3 weeks

### Phase 3: Cognitive Functions (Layer 11)
- Working memory (attractor dynamics)
- Attention (biased competition)
- Decision-making (drift-diffusion)
- **Timeline:** 4 weeks

### Phase 4: Metacognition (Layer 12)
- Error monitoring
- Confidence estimation
- Adaptive learning rates
- **Timeline:** 3 weeks

### Phase 5: Integration
- Hierarchical coupling
- End-to-end testing
- **Timeline:** 2 weeks

**Total:** ~16 weeks for complete Layers 9-12 implementation

---

## Validation Metrics

### Layer 9 (Regional)
- ✓ Regions develop distinct selectivity profiles
- ✓ Topographic maps preserve neighborhood structure
- ✓ Routing adapts to task demands
- ✓ Pathway delays match biological values (10-100ms)

### Layer 10 (Network)
- ✓ Global workspace holds 4-7 items
- ✓ Broadcast amplifies by 10-100×
- ✓ Gamma coherence increases during binding
- ✓ Switching time: 100-500ms

### Layer 11 (Cognitive)
- ✓ WM persists for 1-5 seconds
- ✓ Attention increases gain by 1.5-3×
- ✓ DDM predicts RT distributions
- ✓ Planning depth: 3-5 steps

### Layer 12 (Metacognitive)
- ✓ ERN appears 50-100ms after errors
- ✓ Confidence correlates with accuracy (r > 0.6)
- ✓ Learning rate adapts to error magnitude
- ✓ M-ratio > 0.5

---

## References

### Layer 9 (Regional)
1. Kohonen, T. (1990). "The self-organizing map." *Proceedings of the IEEE*
2. Van Essen, D.C. (1997). "A tension-based theory of morphogenesis and compact wiring in the central nervous system." *Nature*
3. Breakspear, M. (2017). "Dynamic models of large-scale brain activity." *Nature Neuroscience*

### Layer 10 (Network)
4. Dehaene, S., Changeux, J.P. (2011). "Experimental and theoretical approaches to conscious processing." *Neuron*
5. Fries, P. (2015). "Rhythms for cognition: communication through coherence." *Neuron*
6. Buzsáki, G., Draguhn, A. (2004). "Neuronal oscillations in cortical networks." *Science*

### Layer 11 (Cognitive)
7. Compte, A. (2000). "Synaptic mechanisms and network dynamics underlying spatial working memory in a cortical network model." *Cerebral Cortex*
8. Ratcliff, R., McKoon, G. (2008). "The diffusion decision model." *Neural Computation*
9. Reynolds, J.H., Heeger, D.J. (2009). "The normalization model of attention." *Neuron*

### Layer 12 (Metacognitive)
10. Fleming, S.M., Dolan, R.J. (2012). "The neural basis of metacognitive ability." *Philosophical Transactions of the Royal Society B*
11. Ridderinkhof, K.R. (2004). "The role of the medial frontal cortex in cognitive control." *Science*
12. Finn, C., Abbeel, P., Levine, S. (2017). "Model-agnostic meta-learning for fast adaptation of deep networks." *ICML*

---

**END OF DOCUMENT**

*This reference provides complete mathematical formulations for implementing biological Layers 9-12. All equations are implementation-ready with specified parameters based on neuroscience literature and computational modeling.*
