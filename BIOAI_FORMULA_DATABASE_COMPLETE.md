# BioAI Formula Database - Complete Reference

**Total Formulas:** 295

**Organization:** By category, with full mathematical and implementation details.

---


## Biochemistry

### Hopfield Energy Function
**ID:** 246

**Description:** Energy of a memory state in Hopfield network

**Domain:** memory

**Origin:** hopfield-networks

**Mathematical Form:**
```latex
E(x) = -\frac{1}{2} x^T W x + b^T x
```

**Implementation:**
```python
energy = -0.5 * x.T @ W @ x + b.T @ x
```

**Reference:** DOI PNAS:79(8) (1982)

---

### Improved Hopfield Retrieval
**ID:** 247

**Description:** Attention-based memory retrieval from partial cue

**Domain:** memory

**Origin:** modern-hopfield-networks

**Mathematical Form:**
```latex
M(x) = \mathrm{softmax}(x^T K^T) V
```

**Implementation:**
```python
retrieved = softmax(x @ K.T) @ V
```

**Reference:** DOI arXiv:2008.02217 (2020)

---

### Memory Consolidation via Replay
**ID:** 250

**Description:** Replay sampled memories through cortex for consolidation

**Domain:** memory

**Origin:** systems-consolidation

**Mathematical Form:**
```latex
\Delta W_{cortex} += \sum_{t \in replay} e_t \cdot h_t^T
```

**Implementation:**
```python
dW_cortex += sum(e_t * h_t.T for e_t, h_t in replay_buffer)
```

**Reference:** DOI Neuron:44(1) (2004)

---

### Pattern Separation (Dentate Gyrus)
**ID:** 249

**Description:** Expand and decorrelate input patterns to prevent interference

**Domain:** memory

**Origin:** hippocampal-circuit

**Mathematical Form:**
```latex
m_{dg} = \text{ReLU}(E \cdot m_{input})
```

**Implementation:**
```python
m_dg = relu(E @ m_input)
```

**Reference:** DOI Neuron:50(3) (2006)

---

### Sparse Memory Encoding
**ID:** 248

**Description:** Encode experience as sparse vector for storage

**Domain:** memory

**Origin:** sparse-coding

**Mathematical Form:**
```latex
m = \text{top-k}(\text{embed}(experience))
```

**Implementation:**
```python
m = top_k_sparse(embed(exp), k=sparsity)
```

**Reference:** DOI arXiv:1908.01264 (2019)

---


## Cell Signaling

### Calcium Release from ER (IP3R)
**ID:** 53

**Description:** IP3 receptor-mediated calcium release

**Domain:** calcium-signaling

**Origin:** IP3R

**Mathematical Form:**
```latex
\frac{d[Ca^{2+}]_{cyt}}{dt} = v_{IP3R} m_\infty^3 h^3 ([Ca^{2+}]_{ER} - [Ca^{2+}]_{cyt})
```

---

### Calcium Release from ER (IP3R)
**ID:** 130

**Description:** IP3 receptor-mediated calcium release

**Domain:** calcium-signaling

**Origin:** IP3R

**Mathematical Form:**
```latex
\frac{d[Ca^{2+}]_{cyt}}{dt} = v_{IP3R} m_\infty^3 h^3 ([Ca^{2+}]_{ER} - [Ca^{2+}]_{cyt})
```

---

### Goldbeter-Koshland Ultrasensitivity
**ID:** 51

**Description:** Zero-order ultrasensitivity in phosphorylation cycles

**Domain:** cell-signaling

**Origin:** goldbeter-koshland

**Mathematical Form:**
```latex
[W^*] = G(v_1, v_2, J_1, J_2) = \frac{2v_1 J_2}{B + \sqrt{B^2 - 4(v_2 - v_1)v_1 J_2}}
```

**Reference:** DOI 10.1073/pnas.78.11.6840 (1981)

---

### Goldbeter-Koshland Ultrasensitivity
**ID:** 128

**Description:** Zero-order ultrasensitivity in phosphorylation cycles

**Domain:** cell-signaling

**Origin:** goldbeter-koshland

**Mathematical Form:**
```latex
[W^*] = G(v_1, v_2, J_1, J_2) = \frac{2v_1 J_2}{B + \sqrt{B^2 - 4(v_2 - v_1)v_1 J_2}}
```

**Reference:** DOI 10.1073/pnas.78.11.6840 (1981)

---

### MAPK Cascade Layer 1 (MAPKKK)
**ID:** 52

**Description:** MAPK cascade - MAPKKK activation/deactivation

**Domain:** cell-signaling

**Origin:** MAPK

**Mathematical Form:**
```latex
\frac{d[MAPKKK^*]}{dt} = \frac{k_1 [Signal][MAPKKK]}{K_{m1} + [MAPKKK]} - \frac{k_2 [MAPKKK^*]}{K_{m2} + [MAPKKK^*]}
```

**Reference:** DOI 10.1016/S0955-0674(97)80066-0 (1997)

---

### MAPK Cascade Layer 1 (MAPKKK)
**ID:** 129

**Description:** MAPK cascade - MAPKKK activation/deactivation

**Domain:** cell-signaling

**Origin:** MAPK

**Mathematical Form:**
```latex
\frac{d[MAPKKK^*]}{dt} = \frac{k_1 [Signal][MAPKKK]}{K_{m1} + [MAPKKK]} - \frac{k_2 [MAPKKK^*]}{K_{m2} + [MAPKKK^*]}
```

**Reference:** DOI 10.1016/S0955-0674(97)80066-0 (1997)

---

### SERCA Pump
**ID:** 54

**Description:** SERCA calcium pump flux into ER

**Domain:** calcium-signaling

**Origin:** SERCA

**Mathematical Form:**
```latex
J_{SERCA} = V_{SERCA} \frac{[Ca^{2+}]_{cyt}^2}{K_{SERCA}^2 + [Ca^{2+}]_{cyt}^2}
```

**Implementation:**
```python
J_SERCA = V_SERCA * Ca_cyt**2 / (K_SERCA**2 + Ca_cyt**2)
```

---

### SERCA Pump
**ID:** 131

**Description:** SERCA calcium pump flux into ER

**Domain:** calcium-signaling

**Origin:** SERCA

**Mathematical Form:**
```latex
J_{SERCA} = V_{SERCA} \frac{[Ca^{2+}]_{cyt}^2}{K_{SERCA}^2 + [Ca^{2+}]_{cyt}^2}
```

**Implementation:**
```python
J_SERCA = V_SERCA * Ca_cyt**2 / (K_SERCA**2 + Ca_cyt**2)
```

---


## Dendritic Computation

### Cable Equation (Dendrite)
**ID:** 161

**Description:** Passive signal propagation in dendrites

**Domain:** dendritic-computation

**Mathematical Form:**
```latex
\lambda^2 \frac{\partial^2 V}{\partial x^2} = \tau \frac{\partial V}{\partial t} + V - V_{rest}
```

---

### Coincidence Detection (AND Gate)
**ID:** 166

**Description:** Detect synchronous input from multiple sources

**Domain:** dendritic-computation

**Mathematical Form:**
```latex
Output = 1 \text{ if } (|t_1 - t_2| < \Delta t_{window})
```

**Implementation:**
```python
output = 1 if abs(t1 - t2) < dt_window else 0
```

---

### Compartmental Membrane Equation
**ID:** 162

**Description:** Compartmental neuron model with coupled segments

**Domain:** dendritic-computation

**Mathematical Form:**
```latex
C \frac{dV_i}{dt} = \sum(g_{ij}(V_j - V_i)) + I_{syn} - I_{leak}
```

**Implementation:**
```python
dV_dt = (sum(g[i,j]*(V[j]-V[i]) for j) + I_syn - I_leak) / C
```

---

### Exponential Decay (Temporal Integration)
**ID:** 164

**Description:** Exponential decay of voltage over time

**Domain:** dendritic-computation

**Mathematical Form:**
```latex
V(t) = V_0 \exp(-t/\tau)
```

**Implementation:**
```python
V = V_0 * np.exp(-t / tau)
```

---

### Integrate-and-Fire
**ID:** 163

**Description:** Simple neuron model: integrate input, fire when threshold crossed

**Domain:** dendritic-computation

**Mathematical Form:**
```latex
\tau \frac{dV}{dt} = -(V - V_{rest}) + R I
```

**Implementation:**
```python
dV_dt = (-(V - V_rest) + R * I) / tau
```

---

### Leaky Integration
**ID:** 165

**Description:** Leaky temporal integration of input

**Domain:** dendritic-computation

**Mathematical Form:**
```latex
V(t) = (R I)(1 - \exp(-t/\tau))
```

**Implementation:**
```python
V = (R * I) * (1 - np.exp(-t / tau))
```

---

### NMDA Voltage Dependence
**ID:** 167

**Description:** Voltage-dependent Mg2+ block of NMDA receptors

**Domain:** dendritic-computation

**Mathematical Form:**
```latex
g = \frac{g_{max}}{1 + [Mg^{2+}] \exp(-0.062 V)/3.57}
```

**Implementation:**
```python
g = g_max / (1 + (Mg / 3.57) * np.exp(-0.062 * V))
```

---


## Enzyme Kinetics

### Competitive Inhibition
**ID:** 38

**Description:** Enzyme kinetics with competitive inhibitor

**Domain:** enzyme-kinetics

**Origin:** competitive-inhibition

**Mathematical Form:**
```latex
v = \frac{V_{max} [S]}{K_m \left(1 + \frac{[I]}{K_i}\right) + [S]}
```

**Implementation:**
```python
v = V_max * S / (K_m * (1 + I/K_i) + S)
```

---

### Competitive Inhibition
**ID:** 115

**Description:** Enzyme kinetics with competitive inhibitor

**Domain:** enzyme-kinetics

**Origin:** competitive-inhibition

**Mathematical Form:**
```latex
v = \frac{V_{max} [S]}{K_m \left(1 + \frac{[I]}{K_i}\right) + [S]}
```

**Implementation:**
```python
v = V_max * S / (K_m * (1 + I/K_i) + S)
```

---

### Hill Equation
**ID:** 41

**Description:** Cooperative binding with Hill coefficient

**Domain:** enzyme-kinetics

**Origin:** hill

**Mathematical Form:**
```latex
v = \frac{V_{max} [S]^n}{K_{0.5}^n + [S]^n}
```

**Implementation:**
```python
v = V_max * S**n / (K_half**n + S**n)
```

---

### Hill Equation
**ID:** 118

**Description:** Cooperative binding with Hill coefficient

**Domain:** enzyme-kinetics

**Origin:** hill

**Mathematical Form:**
```latex
v = \frac{V_{max} [S]^n}{K_{0.5}^n + [S]^n}
```

**Implementation:**
```python
v = V_max * S**n / (K_half**n + S**n)
```

---

### KNF Sequential Model
**ID:** 50

**Description:** Koshland-Némethy-Filmer sequential binding model

**Domain:** enzyme-kinetics

**Origin:** KNF

**Mathematical Form:**
```latex
Y = \frac{[S](K_1 + 2K_1K_2[S] + 3K_1K_2K_3[S]^2 + 4K_1K_2K_3K_4[S]^3)}{4(1 + K_1[S] + K_1K_2[S]^2 + K_1K_2K_3[S]^3 + K_1K_2K_3K_4[S]^4)}
```

---

### KNF Sequential Model
**ID:** 127

**Description:** Koshland-Némethy-Filmer sequential binding model

**Domain:** enzyme-kinetics

**Origin:** KNF

**Mathematical Form:**
```latex
Y = \frac{[S](K_1 + 2K_1K_2[S] + 3K_1K_2K_3[S]^2 + 4K_1K_2K_3K_4[S]^3)}{4(1 + K_1[S] + K_1K_2[S]^2 + K_1K_2K_3[S]^3 + K_1K_2K_3K_4[S]^4)}
```

---

### Lineweaver-Burk Equation
**ID:** 37

**Description:** Double-reciprocal linearization of Michaelis-Menten

**Domain:** enzyme-kinetics

**Origin:** lineweaver-burk

**Mathematical Form:**
```latex
\frac{1}{v} = \frac{K_m}{V_{max}} \cdot \frac{1}{[S]} + \frac{1}{V_{max}}
```

**Implementation:**
```python
inv_v = (K_m / V_max) * (1 / S) + (1 / V_max)
```

---

### Lineweaver-Burk Equation
**ID:** 114

**Description:** Double-reciprocal linearization of Michaelis-Menten

**Domain:** enzyme-kinetics

**Origin:** lineweaver-burk

**Mathematical Form:**
```latex
\frac{1}{v} = \frac{K_m}{V_{max}} \cdot \frac{1}{[S]} + \frac{1}{V_{max}}
```

**Implementation:**
```python
inv_v = (K_m / V_max) * (1 / S) + (1 / V_max)
```

---

### Michaelis-Menten Kinetics
**ID:** 35

**Description:** Classic enzyme kinetics with substrate saturation

**Domain:** enzyme-kinetics

**Origin:** michaelis-menten

**Mathematical Form:**
```latex
v = \frac{V_{max} [S]}{K_m + [S]}
```

**Implementation:**
```python
v = V_max * S / (K_m + S)
```

---

### Michaelis-Menten Kinetics
**ID:** 112

**Description:** Classic enzyme kinetics with substrate saturation

**Domain:** enzyme-kinetics

**Origin:** michaelis-menten

**Mathematical Form:**
```latex
v = \frac{V_{max} [S]}{K_m + [S]}
```

**Implementation:**
```python
v = V_max * S / (K_m + S)
```

---

### Michaelis-Menten Substrate Dynamics
**ID:** 36

**Description:** Substrate consumption under Michaelis-Menten kinetics

**Domain:** enzyme-kinetics

**Origin:** michaelis-menten

**Mathematical Form:**
```latex
\frac{d[S]}{dt} = -\frac{V_{max} [S]}{K_m + [S]}
```

**Implementation:**
```python
dS_dt = -V_max * S / (K_m + S)
```

---

### Michaelis-Menten Substrate Dynamics
**ID:** 113

**Description:** Substrate consumption under Michaelis-Menten kinetics

**Domain:** enzyme-kinetics

**Origin:** michaelis-menten

**Mathematical Form:**
```latex
\frac{d[S]}{dt} = -\frac{V_{max} [S]}{K_m + [S]}
```

**Implementation:**
```python
dS_dt = -V_max * S / (K_m + S)
```

---

### Monod-Wyman-Changeux (MWC) Model
**ID:** 49

**Description:** Concerted allosteric transition model

**Domain:** enzyme-kinetics

**Origin:** MWC

**Mathematical Form:**
```latex
Y = \frac{\alpha(1+\alpha)^{n-1} + Lc\alpha(1+c\alpha)^{n-1}}{(1+\alpha)^n + L(1+c\alpha)^n}
```

**Reference:** DOI 10.1016/S0022-2836(65)80285-6 (1965)

---

### Monod-Wyman-Changeux (MWC) Model
**ID:** 126

**Description:** Concerted allosteric transition model

**Domain:** enzyme-kinetics

**Origin:** MWC

**Mathematical Form:**
```latex
Y = \frac{\alpha(1+\alpha)^{n-1} + Lc\alpha(1+c\alpha)^{n-1}}{(1+\alpha)^n + L(1+c\alpha)^n}
```

**Reference:** DOI 10.1016/S0022-2836(65)80285-6 (1965)

---

### Non-competitive Inhibition
**ID:** 39

**Description:** Enzyme kinetics with non-competitive inhibitor

**Domain:** enzyme-kinetics

**Origin:** non-competitive-inhibition

**Mathematical Form:**
```latex
v = \frac{V_{max} [S]}{(K_m + [S])\left(1 + \frac{[I]}{K_i}\right)}
```

**Implementation:**
```python
v = V_max * S / ((K_m + S) * (1 + I/K_i))
```

---

### Non-competitive Inhibition
**ID:** 116

**Description:** Enzyme kinetics with non-competitive inhibitor

**Domain:** enzyme-kinetics

**Origin:** non-competitive-inhibition

**Mathematical Form:**
```latex
v = \frac{V_{max} [S]}{(K_m + [S])\left(1 + \frac{[I]}{K_i}\right)}
```

**Implementation:**
```python
v = V_max * S / ((K_m + S) * (1 + I/K_i))
```

---

### Ordered Bi-Bi Mechanism
**ID:** 43

**Description:** Two-substrate ordered sequential mechanism

**Domain:** enzyme-kinetics

**Origin:** ordered-bi-bi

**Mathematical Form:**
```latex
v = \frac{V_{max} [A][B]}{K_{iA}K_B + K_B[A] + K_A[B] + [A][B]}
```

**Implementation:**
```python
v = V_max * A * B / (K_iA * K_B + K_B * A + K_A * B + A * B)
```

---

### Ordered Bi-Bi Mechanism
**ID:** 120

**Description:** Two-substrate ordered sequential mechanism

**Domain:** enzyme-kinetics

**Origin:** ordered-bi-bi

**Mathematical Form:**
```latex
v = \frac{V_{max} [A][B]}{K_{iA}K_B + K_B[A] + K_A[B] + [A][B]}
```

**Implementation:**
```python
v = V_max * A * B / (K_iA * K_B + K_B * A + K_A * B + A * B)
```

---

### Ping-Pong Bi-Bi Mechanism
**ID:** 44

**Description:** Two-substrate ping-pong mechanism

**Domain:** enzyme-kinetics

**Origin:** ping-pong

**Mathematical Form:**
```latex
v = \frac{V_{max} [A][B]}{K_A[B] + K_B[A] + [A][B]}
```

**Implementation:**
```python
v = V_max * A * B / (K_A * B + K_B * A + A * B)
```

---

### Ping-Pong Bi-Bi Mechanism
**ID:** 121

**Description:** Two-substrate ping-pong mechanism

**Domain:** enzyme-kinetics

**Origin:** ping-pong

**Mathematical Form:**
```latex
v = \frac{V_{max} [A][B]}{K_A[B] + K_B[A] + [A][B]}
```

**Implementation:**
```python
v = V_max * A * B / (K_A * B + K_B * A + A * B)
```

---

### Substrate Inhibition
**ID:** 42

**Description:** Enzyme kinetics with excess substrate inhibition

**Domain:** enzyme-kinetics

**Origin:** substrate-inhibition

**Mathematical Form:**
```latex
v = \frac{V_{max} [S]}{K_m + [S] + \frac{[S]^2}{K_{si}}}
```

**Implementation:**
```python
v = V_max * S / (K_m + S + S**2/K_si)
```

---

### Substrate Inhibition
**ID:** 119

**Description:** Enzyme kinetics with excess substrate inhibition

**Domain:** enzyme-kinetics

**Origin:** substrate-inhibition

**Mathematical Form:**
```latex
v = \frac{V_{max} [S]}{K_m + [S] + \frac{[S]^2}{K_{si}}}
```

**Implementation:**
```python
v = V_max * S / (K_m + S + S**2/K_si)
```

---

### Uncompetitive Inhibition
**ID:** 40

**Description:** Enzyme kinetics with uncompetitive inhibitor

**Domain:** enzyme-kinetics

**Origin:** uncompetitive-inhibition

**Mathematical Form:**
```latex
v = \frac{V_{max} [S]}{K_m + [S]\left(1 + \frac{[I]}{K_i}\right)}
```

**Implementation:**
```python
v = V_max * S / (K_m + S * (1 + I/K_i))
```

---

### Uncompetitive Inhibition
**ID:** 117

**Description:** Enzyme kinetics with uncompetitive inhibitor

**Domain:** enzyme-kinetics

**Origin:** uncompetitive-inhibition

**Mathematical Form:**
```latex
v = \frac{V_{max} [S]}{K_m + [S]\left(1 + \frac{[I]}{K_i}\right)}
```

**Implementation:**
```python
v = V_max * S / (K_m + S * (1 + I/K_i))
```

---


## Gene Regulation

### Activated Transcription (Hill)
**ID:** 56

**Description:** Transcription activated by transcription factor

**Domain:** gene-regulation

**Origin:** hill-activation

**Mathematical Form:**
```latex
\frac{d[mRNA]}{dt} = \beta \frac{[TF]^n}{K^n + [TF]^n} - \delta [mRNA]
```

**Implementation:**
```python
dmRNA_dt = beta * TF**n / (K**n + TF**n) - delta * mRNA
```

---

### Activated Transcription (Hill)
**ID:** 133

**Description:** Transcription activated by transcription factor

**Domain:** gene-regulation

**Origin:** hill-activation

**Mathematical Form:**
```latex
\frac{d[mRNA]}{dt} = \beta \frac{[TF]^n}{K^n + [TF]^n} - \delta [mRNA]
```

**Implementation:**
```python
dmRNA_dt = beta * TF**n / (K**n + TF**n) - delta * mRNA
```

---

### Dopamine-Modulated Learning
**ID:** 255

**Description:** Learning rate multiplied by dopamine (TD error)

**Domain:** synaptic-plasticity

**Origin:** reinforcement-learning

**Mathematical Form:**
```latex
\Delta W \propto \delta_t \cdot x_t
```

**Implementation:**
```python
dW = dopamine_signal * x
```

**Reference:** DOI Nature:521(7553) (2015)

---

### Inhibitory Competition (Direct vs Indirect)
**ID:** 254

**Description:** Net action tendency from competing pathways

**Domain:** decision-making

**Origin:** basal-ganglia-circuit

**Mathematical Form:**
```latex
a_{net} = Q_{direct} - Q_{indirect}
```

**Implementation:**
```python
action_net = Q_go - Q_stop
```

**Reference:** DOI Neuron:60(6) (2008)

---

### Negative Autoregulation
**ID:** 63

**Description:** Gene with negative autoregulation (speeds response)

**Domain:** gene-regulation

**Origin:** negative-autoregulation

**Mathematical Form:**
```latex
\frac{d[X]}{dt} = \beta \frac{K^n}{K^n + [X]^n} - \alpha [X]
```

**Implementation:**
```python
dX_dt = beta * K**n / (K**n + X**n) - alpha * X
```

---

### Negative Autoregulation
**ID:** 140

**Description:** Gene with negative autoregulation (speeds response)

**Domain:** gene-regulation

**Origin:** negative-autoregulation

**Mathematical Form:**
```latex
\frac{d[X]}{dt} = \beta \frac{K^n}{K^n + [X]^n} - \alpha [X]
```

**Implementation:**
```python
dX_dt = beta * K**n / (K**n + X**n) - alpha * X
```

---

### Positive Autoregulation
**ID:** 62

**Description:** Gene with positive autoregulation

**Domain:** gene-regulation

**Origin:** positive-autoregulation

**Mathematical Form:**
```latex
\frac{d[X]}{dt} = \beta_0 + \beta \frac{[X]^n}{K^n + [X]^n} - \alpha [X]
```

**Implementation:**
```python
dX_dt = beta0 + beta * X**n / (K**n + X**n) - alpha * X
```

---

### Positive Autoregulation
**ID:** 139

**Description:** Gene with positive autoregulation

**Domain:** gene-regulation

**Origin:** positive-autoregulation

**Mathematical Form:**
```latex
\frac{d[X]}{dt} = \beta_0 + \beta \frac{[X]^n}{K^n + [X]^n} - \alpha [X]
```

**Implementation:**
```python
dX_dt = beta0 + beta * X**n / (K**n + X**n) - alpha * X
```

---

### Q-Function (Action Value)
**ID:** 251

**Description:** Expected cumulative reward for state-action pair

**Domain:** reinforcement-learning

**Origin:** reinforcement-learning

**Mathematical Form:**
```latex
Q(s, a) = \mathbb{E}[R_t + \gamma Q(s_{t+1}, a\')]
```

**Implementation:**
```python
Q = R + gamma * Q_next
```

**Reference:** DOI IEEE:12(4) (1992)

---

### Repressed Transcription (Hill)
**ID:** 57

**Description:** Transcription repressed by repressor

**Domain:** gene-regulation

**Origin:** hill-repression

**Mathematical Form:**
```latex
\frac{d[mRNA]}{dt} = \beta \frac{K^n}{K^n + [R]^n} - \delta [mRNA]
```

**Implementation:**
```python
dmRNA_dt = beta * K**n / (K**n + R**n) - delta * mRNA
```

---

### Repressed Transcription (Hill)
**ID:** 134

**Description:** Transcription repressed by repressor

**Domain:** gene-regulation

**Origin:** hill-repression

**Mathematical Form:**
```latex
\frac{d[mRNA]}{dt} = \beta \frac{K^n}{K^n + [R]^n} - \delta [mRNA]
```

**Implementation:**
```python
dmRNA_dt = beta * K**n / (K**n + R**n) - delta * mRNA
```

---

### Repressilator Gene 1
**ID:** 59

**Description:** Repressilator mRNA dynamics - gene 1

**Domain:** synthetic-biology

**Origin:** repressilator

**Mathematical Form:**
```latex
\frac{dm_1}{dt} = -m_1 + \frac{\alpha}{1 + p_3^n} + \alpha_0
```

**Implementation:**
```python
dm1_dt = -m1 + alpha / (1 + p3**n) + alpha0
```

**Reference:** DOI 10.1038/35002125 (2000)

---

### Repressilator Gene 1
**ID:** 136

**Description:** Repressilator mRNA dynamics - gene 1

**Domain:** synthetic-biology

**Origin:** repressilator

**Mathematical Form:**
```latex
\frac{dm_1}{dt} = -m_1 + \frac{\alpha}{1 + p_3^n} + \alpha_0
```

**Implementation:**
```python
dm1_dt = -m1 + alpha / (1 + p3**n) + alpha0
```

**Reference:** DOI 10.1038/35002125 (2000)

---

### Simple Gene Expression
**ID:** 55

**Description:** Basic protein synthesis and degradation

**Domain:** gene-expression

**Origin:** gene-expression

**Mathematical Form:**
```latex
\frac{d[P]}{dt} = k_s - k_d [P]
```

**Implementation:**
```python
dP_dt = k_s - k_d * P
```

---

### Simple Gene Expression
**ID:** 132

**Description:** Basic protein synthesis and degradation

**Domain:** gene-expression

**Origin:** gene-expression

**Mathematical Form:**
```latex
\frac{d[P]}{dt} = k_s - k_d [P]
```

**Implementation:**
```python
dP_dt = k_s - k_d * P
```

---

### Softmax Action Selection
**ID:** 253

**Description:** Probabilistic action selection with exploration

**Domain:** decision-making

**Origin:** basal-ganglia-model

**Mathematical Form:**
```latex
\pi(a|s) = \frac{\exp(Q(s,a)/\tau)}{\sum_{a\'} \exp(Q(s,a\')/\tau)}
```

**Implementation:**
```python
probs = softmax(Q / temperature)
```

**Reference:** DOI Neuron:36(2) (2002)

---

### Temporal Difference Error (Dopamine)
**ID:** 252

**Description:** TD error signal corresponding to dopamine release

**Domain:** reinforcement-learning

**Origin:** temporal-difference-learning

**Mathematical Form:**
```latex
\delta_t = R_t + \gamma V(s_{t+1}) - V(s_t)
```

**Implementation:**
```python
delta = R + gamma * V_next - V
```

**Reference:** DOI Science:275(5307) (1997)

---

### Toggle Switch Gene 1
**ID:** 60

**Description:** Genetic toggle switch - gene u dynamics

**Domain:** synthetic-biology

**Origin:** toggle-switch

**Mathematical Form:**
```latex
\frac{du}{dt} = \frac{\alpha_1}{1 + v^\beta} - u
```

**Implementation:**
```python
du_dt = alpha1 / (1 + v**beta) - u
```

**Reference:** DOI 10.1038/35002131 (2000)

---

### Toggle Switch Gene 1
**ID:** 137

**Description:** Genetic toggle switch - gene u dynamics

**Domain:** synthetic-biology

**Origin:** toggle-switch

**Mathematical Form:**
```latex
\frac{du}{dt} = \frac{\alpha_1}{1 + v^\beta} - u
```

**Implementation:**
```python
du_dt = alpha1 / (1 + v**beta) - u
```

**Reference:** DOI 10.1038/35002131 (2000)

---

### Toggle Switch Gene 2
**ID:** 61

**Description:** Genetic toggle switch - gene v dynamics

**Domain:** synthetic-biology

**Origin:** toggle-switch

**Mathematical Form:**
```latex
\frac{dv}{dt} = \frac{\alpha_2}{1 + u^\gamma} - v
```

**Implementation:**
```python
dv_dt = alpha2 / (1 + u**gamma) - v
```

---

### Toggle Switch Gene 2
**ID:** 138

**Description:** Genetic toggle switch - gene v dynamics

**Domain:** synthetic-biology

**Origin:** toggle-switch

**Mathematical Form:**
```latex
\frac{dv}{dt} = \frac{\alpha_2}{1 + u^\gamma} - v
```

**Implementation:**
```python
dv_dt = alpha2 / (1 + u**gamma) - v
```

---

### Translation
**ID:** 58

**Description:** Protein translation from mRNA

**Domain:** gene-expression

**Origin:** translation

**Mathematical Form:**
```latex
\frac{d[P]}{dt} = k_{tl} [mRNA] - \gamma [P]
```

**Implementation:**
```python
dP_dt = k_tl * mRNA - gamma * P
```

---

### Translation
**ID:** 135

**Description:** Protein translation from mRNA

**Domain:** gene-expression

**Origin:** translation

**Mathematical Form:**
```latex
\frac{d[P]}{dt} = k_{tl} [mRNA] - \gamma [P]
```

**Implementation:**
```python
dP_dt = k_tl * mRNA - gamma * P
```

---


## Ion Channels

### HH Alpha_m Rate
**ID:** 3

**Description:** Forward rate constant for sodium activation

**Domain:** electrophysiology

**Origin:** hodgkin-huxley

**Mathematical Form:**
```latex
\alpha_m(V) = \frac{0.1(V+40)}{1 - \exp(-(V+40)/10)}
```

**Implementation:**
```python
alpha_m = 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))
```

---

### HH Alpha_m Rate
**ID:** 80

**Description:** Forward rate constant for sodium activation

**Domain:** electrophysiology

**Origin:** hodgkin-huxley

**Mathematical Form:**
```latex
\alpha_m(V) = \frac{0.1(V+40)}{1 - \exp(-(V+40)/10)}
```

**Implementation:**
```python
alpha_m = 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))
```

---

### HH Alpha_n Rate
**ID:** 7

**Description:** Forward rate constant for potassium activation

**Domain:** electrophysiology

**Origin:** hodgkin-huxley

**Mathematical Form:**
```latex
\alpha_n(V) = \frac{0.01(V+55)}{1 - \exp(-(V+55)/10)}
```

**Implementation:**
```python
alpha_n = 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10))
```

---

### HH Alpha_n Rate
**ID:** 84

**Description:** Forward rate constant for potassium activation

**Domain:** electrophysiology

**Origin:** hodgkin-huxley

**Mathematical Form:**
```latex
\alpha_n(V) = \frac{0.01(V+55)}{1 - \exp(-(V+55)/10)}
```

**Implementation:**
```python
alpha_n = 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10))
```

---

### HH Beta_m Rate
**ID:** 4

**Description:** Backward rate constant for sodium activation

**Domain:** electrophysiology

**Origin:** hodgkin-huxley

**Mathematical Form:**
```latex
\beta_m(V) = 4 \exp(-(V+65)/18)
```

**Implementation:**
```python
beta_m = 4 * np.exp(-(V + 65) / 18)
```

---

### HH Beta_m Rate
**ID:** 81

**Description:** Backward rate constant for sodium activation

**Domain:** electrophysiology

**Origin:** hodgkin-huxley

**Mathematical Form:**
```latex
\beta_m(V) = 4 \exp(-(V+65)/18)
```

**Implementation:**
```python
beta_m = 4 * np.exp(-(V + 65) / 18)
```

---

### HH Beta_n Rate
**ID:** 8

**Description:** Backward rate constant for potassium activation

**Domain:** electrophysiology

**Origin:** hodgkin-huxley

**Mathematical Form:**
```latex
\beta_n(V) = 0.125 \exp(-(V+65)/80)
```

**Implementation:**
```python
beta_n = 0.125 * np.exp(-(V + 65) / 80)
```

---

### HH Beta_n Rate
**ID:** 85

**Description:** Backward rate constant for potassium activation

**Domain:** electrophysiology

**Origin:** hodgkin-huxley

**Mathematical Form:**
```latex
\beta_n(V) = 0.125 \exp(-(V+65)/80)
```

**Implementation:**
```python
beta_n = 0.125 * np.exp(-(V + 65) / 80)
```

---

### HH Potassium Activation (n)
**ID:** 6

**Description:** Potassium channel activation gating variable dynamics

**Domain:** electrophysiology

**Origin:** hodgkin-huxley

**Mathematical Form:**
```latex
\frac{dn}{dt} = \alpha_n(V)(1-n) - \beta_n(V)n
```

**Implementation:**
```python
dn_dt = alpha_n(V) * (1 - n) - beta_n(V) * n
```

---

### HH Potassium Activation (n)
**ID:** 83

**Description:** Potassium channel activation gating variable dynamics

**Domain:** electrophysiology

**Origin:** hodgkin-huxley

**Mathematical Form:**
```latex
\frac{dn}{dt} = \alpha_n(V)(1-n) - \beta_n(V)n
```

**Implementation:**
```python
dn_dt = alpha_n(V) * (1 - n) - beta_n(V) * n
```

---

### HH Sodium Activation (m)
**ID:** 2

**Description:** Sodium channel activation gating variable dynamics

**Domain:** electrophysiology

**Origin:** hodgkin-huxley

**Mathematical Form:**
```latex
\frac{dm}{dt} = \alpha_m(V)(1-m) - \beta_m(V)m
```

**Implementation:**
```python
dm_dt = alpha_m(V) * (1 - m) - beta_m(V) * m
```

---

### HH Sodium Activation (m)
**ID:** 79

**Description:** Sodium channel activation gating variable dynamics

**Domain:** electrophysiology

**Origin:** hodgkin-huxley

**Mathematical Form:**
```latex
\frac{dm}{dt} = \alpha_m(V)(1-m) - \beta_m(V)m
```

**Implementation:**
```python
dm_dt = alpha_m(V) * (1 - m) - beta_m(V) * m
```

---

### HH Sodium Inactivation (h)
**ID:** 5

**Description:** Sodium channel inactivation gating variable dynamics

**Domain:** electrophysiology

**Origin:** hodgkin-huxley

**Mathematical Form:**
```latex
\frac{dh}{dt} = \alpha_h(V)(1-h) - \beta_h(V)h
```

**Implementation:**
```python
dh_dt = alpha_h(V) * (1 - h) - beta_h(V) * h
```

---

### HH Sodium Inactivation (h)
**ID:** 82

**Description:** Sodium channel inactivation gating variable dynamics

**Domain:** electrophysiology

**Origin:** hodgkin-huxley

**Mathematical Form:**
```latex
\frac{dh}{dt} = \alpha_h(V)(1-h) - \beta_h(V)h
```

**Implementation:**
```python
dh_dt = alpha_h(V) * (1 - h) - beta_h(V) * h
```

---

### Memory Priority Tagging
**ID:** 268

**Description:** Priority for memory consolidation based on salience

**Domain:** memory

**Origin:** amygdala-model

**Mathematical Form:**
```latex
priority = s_t + r_t + 0.1 \cdot novelty_t
```

**Implementation:**
```python
priority = s + r + 0.1*novelty
```

**Reference:** DOI Neuron:25(1) (2000)

---

### Novelty Detection
**ID:** 266

**Description:** Deviation from recent input distribution

**Domain:** computational-neuroscience

**Origin:** amygdala-model

**Mathematical Form:**
```latex
novelty_t = ||x_t - \mu_{recent}||
```

**Implementation:**
```python
novelty = norm(x - mean_recent)
```

**Reference:** DOI Neuron:25(1) (2000)

---

### Risk/Threat Assessment
**ID:** 265

**Description:** Estimate danger level and threat from current state

**Domain:** computational-neuroscience

**Origin:** amygdala-model

**Mathematical Form:**
```latex
r_t = \sigma(f_{risk}(x_t))
```

**Implementation:**
```python
r = sigmoid(risk_net(x))
```

**Reference:** DOI Neuron:25(1) (2000)

---

### Salience Estimation
**ID:** 264

**Description:** Importance score for current experience

**Domain:** computational-neuroscience

**Origin:** amygdala-model

**Mathematical Form:**
```latex
s_t = \sigma(f_{salience}(x_t))
```

**Implementation:**
```python
s = sigmoid(salience_net(x))
```

**Reference:** DOI Neuron:25(1) (2000)

---

### Salience-Modulated Learning Rate
**ID:** 267

**Description:** Increase learning rate for important and risky events

**Domain:** learning

**Origin:** amygdala-model

**Mathematical Form:**
```latex
\alpha_t = \alpha_0 + \beta_s \cdot s_t + \beta_r \cdot r_t
```

**Implementation:**
```python
alpha = alpha_0 + beta_s * s + beta_r * r
```

**Reference:** DOI Neuron:25(1) (2000)

---


## Language & Cognition

### Circular Convolution
**ID:** 212

**Description:** Bind vectors for structured representation

**Domain:** semantic-composition

**Mathematical Form:**
```latex
v_1 \star v_2 = \mathcal{F}^{-1}(\mathcal{F}(v_1) \cdot \mathcal{F}(v_2))
```

---

### Modus Ponens
**ID:** 214

**Description:** Logical inference rule

**Domain:** logical-inference

**Mathematical Form:**
```latex
(A \to B) \land A \Rightarrow B
```

---

### Proportional Analogy
**ID:** 213

**Description:** Solve analogy relations

**Domain:** semantic-composition

**Mathematical Form:**
```latex
a : b :: c : ? \rightarrow d = b - a + c
```

**Implementation:**
```python
d = b - a + c
```

---

### Shift-Reduce Parser
**ID:** 209

**Description:** Syntactic parsing rule

**Domain:** language-parsing

**Mathematical Form:**
```latex
\text{If } A \to BC \text{ matches: reduce}(B,C) \to A; \text{ Else: shift}
```

---

### Tensor Product Composition
**ID:** 211

**Description:** Tensor product for structured composition

**Domain:** semantic-composition

**Mathematical Form:**
```latex
T_{phrase} = v_1 \otimes v_2
```

**Implementation:**
```python
T = np.outer(v1, v2)
```

---

### Vector Composition (Addition)
**ID:** 210

**Description:** Simple additive semantic composition

**Domain:** semantic-composition

**Mathematical Form:**
```latex
v_{phrase} = v_1 + v_2
```

**Implementation:**
```python
v_phrase = v1 + v2
```

---


## Layer 0: Physical Substrate

### Boltzmann Distribution (Equilibrium)
**ID:** 278

**Description:** Equilibrium probability distribution in energy landscape. States with lower energy are exponentially more probable.

**Domain:** statistical_mechanics

**Origin:** Layer 0: Physical Substrate

**Mathematical Form:**
```latex
\rho_{eq}(x) \propto \exp\left(-\frac{U(x)}{k_B T}\right)
```

**Implementation:**
```python
def boltzmann_distribution(x, U, kB, T):
    return np.exp(-U(x) / (kB * T))
```

---

### Diffusion Equation (Fick's Second Law)
**ID:** 279

**Description:** Describes spreading of concentration through diffusion. Fundamental equation for molecular transport.

**Domain:** transport

**Origin:** Layer 0: Physical Substrate

**Mathematical Form:**
```latex
\frac{\partial c}{\partial t} = D\nabla^2 c
```

**Implementation:**
```python
def diffusion_step(c, dx, dt, D):
    laplacian = (np.roll(c,1) - 2*c + np.roll(c,-1)) / dx**2
    return c + D * laplacian * dt
```

---

### Einstein Relation (Mean Squared Displacement)
**ID:** 280

**Description:** Mean-squared displacement grows linearly with time in free diffusion. Used to extract diffusion coefficient from experiments.

**Domain:** transport

**Origin:** Layer 0: Physical Substrate

**Mathematical Form:**
```latex
\langle x^2(t) \rangle = 2Dt
```

**Implementation:**
```python
def msd_theory(t, D):
    return 2 * D * t
```

**Reference:** DOI 10.1002/andp.19053220806 (1905)

---

### Fluctuation-Dissipation Theorem
**ID:** 282

**Description:** Relates spontaneous fluctuations to dissipation (friction). Fundamental theorem connecting equilibrium fluctuations to transport coefficients.

**Domain:** statistical_mechanics

**Origin:** Layer 0: Physical Substrate

**Mathematical Form:**
```latex
\langle x(0) \cdot x(t) \rangle = \frac{k_B T}{\gamma}e^{-\gamma t/m}
```

**Implementation:**
```python
def autocorrelation(t, kB, T, gamma, m):
    return (kB * T / gamma) * np.exp(-gamma * t / m)
```

---

### Fokker-Planck Equation
**ID:** 277

**Description:** Evolution equation for probability density in Langevin dynamics. Gives ensemble behavior from single-particle stochastic equation.

**Domain:** statistical_mechanics

**Origin:** Layer 0: Physical Substrate

**Mathematical Form:**
```latex
\frac{\partial\rho}{\partial t} = \frac{1}{\gamma}\nabla\cdot[\nabla U(x)\rho] + D\nabla^2\rho
```

**Implementation:**
```python
def fokker_planck_step(rho, dx, dt, gamma, D, U_grad):
    # Drift term
    drift = divergence(U_grad * rho) / gamma
    # Diffusion term
    diffusion = D * laplacian(rho, dx)
    return rho + (drift + diffusion) * dt
```

**Reference:** DOI 10.1007/978-3-642-61544-3 (1996)

---

### Kramers Rate (Barrier Crossing)
**ID:** 281

**Description:** Rate of escape over energy barrier by thermal activation. Critical for protein folding, chemical reactions, state transitions.

**Domain:** kinetics

**Origin:** Layer 0: Physical Substrate

**Mathematical Form:**
```latex
k = \frac{\omega_0\omega_b}{2\pi\gamma}\exp\left(-\frac{\Delta U}{k_B T}\right)
```

**Implementation:**
```python
def kramers_rate(omega_0, omega_b, gamma, Delta_U, kB, T):
    prefactor = (omega_0 * omega_b) / (2 * np.pi * gamma)
    boltzmann = np.exp(-Delta_U / (kB * T))
    return prefactor * boltzmann
```

---

### Langevin Equation (Overdamped)
**ID:** 275

**Description:** Overdamped Langevin equation describing motion of particles in viscous medium with thermal fluctuations. Used for molecular dynamics, protein folding, Brownian motion.

**Domain:** statistical_mechanics

**Origin:** Layer 0: Physical Substrate

**Mathematical Form:**
```latex
\frac{dx}{dt} = -\frac{1}{\gamma}\nabla U(x) + \sqrt{2D}\eta(t)
```

**Implementation:**
```python
def langevin_step(x, dt, U_grad, gamma, D):
    drift = -(1/gamma) * U_grad(x)
    noise = np.sqrt(2*D*dt) * np.random.randn(*x.shape)
    return x + drift*dt + noise
```

**Reference:** DOI 10.1007/978-3-642-61544-3 (1996)

---

### Langevin Equation (Underdamped)
**ID:** 276

**Description:** Underdamped Langevin equation with inertial effects. Includes momentum term for systems where mass matters.

**Domain:** statistical_mechanics

**Origin:** Layer 0: Physical Substrate

**Mathematical Form:**
```latex
m\frac{d^2x}{dt^2} = -\gamma\frac{dx}{dt} - \nabla U(x) + \sqrt{2\gamma k_B T}\eta(t)
```

**Implementation:**
```python
def underdamped_langevin_step(x, v, dt, m, gamma, U_grad, kB, T):
    force = -gamma*v - U_grad(x) + np.sqrt(2*gamma*kB*T/dt)*np.random.randn(*x.shape)
    v_new = v + (force/m)*dt
    x_new = x + v_new*dt
    return x_new, v_new
```

---


## Layer 1: Capability Graph

### Clustering Coefficient
**ID:** 288

**Description:** Measures local clustering in networks. High C indicates community structure.

**Domain:** graph_theory

**Origin:** Layer 1: Capability Graph

**Mathematical Form:**
```latex
C = \frac{3 \times \text{number of triangles}}{\text{number of connected triples}}
```

**Implementation:**
```python
def clustering_coefficient(adjacency):
    import networkx as nx
    G = nx.from_numpy_array(adjacency)
    return nx.average_clustering(G)
```

---

### Graph Convolutional Network (GCN) Layer
**ID:** 286

**Description:** Graph convolutional layer for learning on graph-structured data. Aggregates neighbor features with learned weights.

**Domain:** machine_learning

**Origin:** Layer 1: Capability Graph

**Mathematical Form:**
```latex
H^{(l+1)} = \sigma(\tilde{D}^{-1/2}\tilde{A}\tilde{D}^{-1/2}H^{(l)}W^{(l)})
```

**Implementation:**
```python
def gcn_layer(H, adjacency, W, activation=np.tanh):
    # Add self-loops
    A_hat = adjacency + np.eye(len(adjacency))
    # Normalize
    D_hat = np.diag(np.sum(A_hat, axis=1))
    D_inv_sqrt = np.diag(1.0 / np.sqrt(np.diag(D_hat)))
    norm_adj = D_inv_sqrt @ A_hat @ D_inv_sqrt
    # Propagate
    return activation(norm_adj @ H @ W)
```

**Reference:** DOI 10.48550/arXiv.1609.02907 (2017)

---

### Graph Laplacian
**ID:** 283

**Description:** Graph Laplacian matrix governing diffusion on graphs. Eigenvalues encode connectivity structure.

**Domain:** graph_theory

**Origin:** Layer 1: Capability Graph

**Mathematical Form:**
```latex
L = D - A
```

**Implementation:**
```python
def graph_laplacian(adjacency):
    degree = np.diag(np.sum(adjacency, axis=1))
    return degree - adjacency
```

---

### Heat Equation on Graph
**ID:** 285

**Description:** Diffusion of signal on graph. Solution: s(t) = exp(-Lt)·s(0). Converges to uniform distribution.

**Domain:** graph_theory

**Origin:** Layer 1: Capability Graph

**Mathematical Form:**
```latex
\frac{\partial s}{\partial t} = -Ls
```

**Implementation:**
```python
def graph_diffusion_step(s, L, dt):
    return s - L @ s * dt
```

---

### Message Passing Neural Network (MPNN)
**ID:** 287

**Description:** General framework for graph neural networks. Nodes aggregate messages from neighbors and update states.

**Domain:** machine_learning

**Origin:** Layer 1: Capability Graph

**Mathematical Form:**
```latex
m_v^{(t)} = \sum_{u \in \mathcal{N}(v)} M_t(h_v^{(t-1)}, h_u^{(t-1)}, e_{uv})
```

**Implementation:**
```python
def message_passing_step(node_states, adjacency, message_fn, update_fn):
    messages = np.zeros_like(node_states)
    for i in range(len(node_states)):
        for j in range(len(node_states)):
            if adjacency[j, i] > 0:
                messages[i] += message_fn(node_states[i], node_states[j], adjacency[j,i])
    return update_fn(node_states, messages)
```

---

### Normalized Graph Laplacian
**ID:** 284

**Description:** Normalized Laplacian with eigenvalues in [0,2]. Better numerical properties than unnormalized version.

**Domain:** graph_theory

**Origin:** Layer 1: Capability Graph

**Mathematical Form:**
```latex
\mathcal{L} = I - D^{-1/2}AD^{-1/2}
```

**Implementation:**
```python
def normalized_laplacian(adjacency):
    degree = np.sum(adjacency, axis=1)
    D_inv_sqrt = np.diag(1.0 / np.sqrt(degree + 1e-10))
    return np.eye(len(adjacency)) - D_inv_sqrt @ adjacency @ D_inv_sqrt
```

---


## Layer 2: Morphogenesis

### Conway's Game of Life Rule
**ID:** 294

**Description:** Cellular automaton rule producing complex emergent behavior from simple local rules. B3/S23 notation.

**Domain:** cellular_automata

**Origin:** Layer 2: Morphogenesis

**Mathematical Form:**
```latex
s_{i,j}^{t+1} = \begin{cases} 1 & \text{if } N=3 \text{ or } (s_{i,j}^t=1 \text{ and } N \in \{2,3\}) \\ 0 & \text{otherwise} \end{cases}
```

**Implementation:**
```python
def game_of_life_rule(state, neighbors):
    if state == 1:
        return 1 if neighbors in [2, 3] else 0
    else:
        return 1 if neighbors == 3 else 0
```

---

### Elementary Cellular Automaton (1D)
**ID:** 295

**Description:** 1D cellular automaton with 256 possible rules (Wolfram classification). Rule 110 is Turing-complete.

**Domain:** cellular_automata

**Origin:** Layer 2: Morphogenesis

**Mathematical Form:**
```latex
s_i^{t+1} = f(s_{i-1}^t, s_i^t, s_{i+1}^t)
```

**Implementation:**
```python
def elementary_ca_step(state, rule_number):
    rule = {k: int(b) for k, b in zip(['111','110','101','100','011','010','001','000'],
                                       format(rule_number, '08b'))}
    new_state = np.zeros_like(state)
    for i in range(len(state)):
        config = f'{state[i-1]}{state[i]}{state[(i+1)%len(state)]}'
        new_state[i] = rule[config]
    return new_state
```

---

### Gierer-Meinhardt (Activator-Inhibitor)
**ID:** 291

**Description:** Activator-inhibitor model: short-range activation, long-range inhibition. Produces periodic patterns, segments.

**Domain:** morphogenesis

**Origin:** Layer 2: Morphogenesis

**Mathematical Form:**
```latex
\frac{\partial a}{\partial t} = c_a\left(\frac{a^2}{h} - \mu_a a + \rho_a\right) + D_a\nabla^2 a
```

**Implementation:**
```python
def gierer_meinhardt_step(a, h, dx, dt, D_a=0.01, D_h=1.0, c_a=0.01, mu_a=0.01):
    lap_a = laplacian(a, dx)
    lap_h = laplacian(h, dx)
    da = c_a*(a**2/(h+1e-10) - mu_a*a + rho_a) + D_a*lap_a
    dh = c_h*(a**2 - mu_h*h + rho_h) + D_h*lap_h
    return a + da*dt, h + dh*dt
```

---

### Gray-Scott Model
**ID:** 290

**Description:** Autocatalytic reaction-diffusion producing spots, stripes, spirals. Parameters F,k control pattern type.

**Domain:** morphogenesis

**Origin:** Layer 2: Morphogenesis

**Mathematical Form:**
```latex
\frac{\partial u}{\partial t} = D_u\nabla^2 u - uv^2 + F(1-u), \quad \frac{\partial v}{\partial t} = D_v\nabla^2 v + uv^2 - (F+k)v
```

**Implementation:**
```python
def gray_scott_step(u, v, dx, dt, D_u=0.16, D_v=0.08, F=0.060, k=0.062):
    lap_u = laplacian(u, dx)
    lap_v = laplacian(v, dx)
    uvv = u * v * v
    du = D_u*lap_u - uvv + F*(1-u)
    dv = D_v*lap_v + uvv - (F+k)*v
    return u + du*dt, v + dv*dt
```

**Reference:** DOI 10.1126/science.261.5118.189 (1993)

---

### Morphogen Diffusion-Degradation Equation
**ID:** 293

**Description:** Time evolution of morphogen with production, diffusion, and degradation. Steady state gives exponential gradient.

**Domain:** morphogenesis

**Origin:** Layer 2: Morphogenesis

**Mathematical Form:**
```latex
\frac{\partial c}{\partial t} = D\nabla^2 c - kc + S(x)
```

**Implementation:**
```python
def morphogen_evolution_step(c, dx, dt, D, k, source):
    lap_c = laplacian(c, dx)
    dc = D*lap_c - k*c + source
    return c + dc*dt
```

---

### Morphogen Gradient (Steady State)
**ID:** 292

**Description:** Exponential morphogen gradient from source. Length scale λ = √(D/k) sets spatial extent. Basis of positional information.

**Domain:** morphogenesis

**Origin:** Layer 2: Morphogenesis

**Mathematical Form:**
```latex
c(x) = c_0 e^{-x/\lambda}, \quad \lambda = \sqrt{D/k}
```

**Implementation:**
```python
def morphogen_gradient(x, c_0, D, k):
    lambda_decay = np.sqrt(D / k)
    return c_0 * np.exp(-x / lambda_decay)
```

**Reference:** DOI 10.1016/0022-5193(69)90079-9 (1969)

---

### Turing Reaction-Diffusion System
**ID:** 289

**Description:** General form of Turing reaction-diffusion system. Local reaction + differential diffusion → spatial patterns.

**Domain:** morphogenesis

**Origin:** Layer 2: Morphogenesis

**Mathematical Form:**
```latex
\frac{\partial u}{\partial t} = D_u\nabla^2 u + f(u,v), \quad \frac{\partial v}{\partial t} = D_v\nabla^2 v + g(u,v)
```

**Implementation:**
```python
def reaction_diffusion_step(u, v, dx, dt, D_u, D_v, f, g):
    lap_u = laplacian(u, dx)
    lap_v = laplacian(v, dx)
    u_new = u + (D_u*lap_u + f(u,v)) * dt
    v_new = v + (D_v*lap_v + g(u,v)) * dt
    return u_new, v_new
```

**Reference:** DOI 10.1098/rstb.1952.0012 (1952)

---


## Metabolic Pathways

### Arrhenius Equation
**ID:** 47

**Description:** Temperature dependence of rate constants

**Domain:** reaction-kinetics

**Origin:** arrhenius

**Mathematical Form:**
```latex
k = A \exp\left(-\frac{E_a}{RT}\right)
```

**Implementation:**
```python
k = A * np.exp(-E_a / (R * T))
```

---

### Arrhenius Equation
**ID:** 124

**Description:** Temperature dependence of rate constants

**Domain:** reaction-kinetics

**Origin:** arrhenius

**Mathematical Form:**
```latex
k = A \exp\left(-\frac{E_a}{RT}\right)
```

**Implementation:**
```python
k = A * np.exp(-E_a / (R * T))
```

---

### Mass Action (Irreversible)
**ID:** 45

**Description:** Irreversible mass action kinetics

**Domain:** reaction-kinetics

**Origin:** mass-action

**Mathematical Form:**
```latex
v = k [A]^a [B]^b
```

**Implementation:**
```python
v = k * A**a * B**b
```

---

### Mass Action (Irreversible)
**ID:** 122

**Description:** Irreversible mass action kinetics

**Domain:** reaction-kinetics

**Origin:** mass-action

**Mathematical Form:**
```latex
v = k [A]^a [B]^b
```

**Implementation:**
```python
v = k * A**a * B**b
```

---

### Mass Action (Reversible)
**ID:** 46

**Description:** Reversible mass action kinetics

**Domain:** reaction-kinetics

**Origin:** mass-action

**Mathematical Form:**
```latex
v = k_f [A][B] - k_r [C][D]
```

**Implementation:**
```python
v = k_f * A * B - k_r * C * D
```

---

### Mass Action (Reversible)
**ID:** 123

**Description:** Reversible mass action kinetics

**Domain:** reaction-kinetics

**Origin:** mass-action

**Mathematical Form:**
```latex
v = k_f [A][B] - k_r [C][D]
```

**Implementation:**
```python
v = k_f * A * B - k_r * C * D
```

---

### Q10 Temperature Coefficient
**ID:** 48

**Description:** Temperature dependence using Q10 factor

**Domain:** reaction-kinetics

**Origin:** Q10

**Mathematical Form:**
```latex
k(T) = k(T_0) Q_{10}^{(T-T_0)/10}
```

**Implementation:**
```python
k_T = k_T0 * Q10 ** ((T - T0) / 10)
```

---

### Q10 Temperature Coefficient
**ID:** 125

**Description:** Temperature dependence using Q10 factor

**Domain:** reaction-kinetics

**Origin:** Q10

**Mathematical Form:**
```latex
k(T) = k(T_0) Q_{10}^{(T-T_0)/10}
```

**Implementation:**
```python
k_T = k_T0 * Q10 ** ((T - T0) / 10)
```

---


## Molecular/Cellular Level

### Hill Equation (Gene Regulation)
**ID:** 157

**Description:** Gene regulatory output with Hill coefficient

**Domain:** molecular-cellular

**Mathematical Form:**
```latex
Output = \frac{V_{max} [Input]^n}{K^n + [Input]^n}
```

**Implementation:**
```python
output = V_max * (Input**n) / (K**n + Input**n)
```

---

### Linear Signal Summation
**ID:** 159

**Description:** Linear summation of weighted inputs

**Domain:** molecular-cellular

**Mathematical Form:**
```latex
S = \sum w_i I_i
```

**Implementation:**
```python
S = sum(w[i] * I[i] for i in range(n))
```

---

### Michaelis-Menten Kinetics (Cognitive Context)
**ID:** 160

**Description:** Enzyme kinetics in protein-protein interactions

**Domain:** molecular-cellular

**Mathematical Form:**
```latex
v = \frac{V_{max} [S]}{K_m + [S]}
```

**Implementation:**
```python
v = V_max * S / (K_m + S)
```

---

### Repressilator
**ID:** 158

**Description:** Repressilator genetic oscillator dynamics

**Domain:** molecular-cellular

**Mathematical Form:**
```latex
\frac{dx_i}{dt} = \frac{\alpha}{1 + x_j^n} - x_i
```

**Implementation:**
```python
dx_dt = alpha / (1 + x_j**n) - x
```

---

### Transcription Rate
**ID:** 155

**Description:** Transcription rate with Hill coefficient

**Domain:** molecular-cellular

**Mathematical Form:**
```latex
\frac{dR}{dt} = \frac{k_{tx} [TF]^n}{K_d^n + [TF]^n} - \gamma_R R
```

**Implementation:**
```python
dR_dt = (k_tx * TF**n / (K_d**n + TF**n)) - gamma_R * R
```

---

### Translation Rate
**ID:** 156

**Description:** Protein translation rate from mRNA

**Domain:** molecular-cellular

**Mathematical Form:**
```latex
\frac{dP}{dt} = k_{tl} R - \gamma_P P
```

**Implementation:**
```python
dP_dt = k_tl * R - gamma_P * P
```

---


## Motivation & Action

### Action-Value Function
**ID:** 219

**Description:** Expected return for action in state

**Domain:** action-selection

**Mathematical Form:**
```latex
Q(s,a) = E[R | s,a]
```

---

### Expected Value
**ID:** 218

**Description:** Expected value computation

**Domain:** motivation

**Mathematical Form:**
```latex
EV = \sum P(outcome_i) \cdot value(outcome_i)
```

**Implementation:**
```python
EV = sum(p[i] * v[i] for i)
```

---

### Habit Formation (Model-Free)
**ID:** 220

**Description:** Habitual action values from TD learning

**Domain:** learning

**Mathematical Form:**
```latex
Q_{MF}(s,a) \leftarrow Q_{MF} + \alpha \delta
```

---

### Model-Based Value
**ID:** 221

**Description:** Goal-directed planning-based value

**Domain:** planning

**Mathematical Form:**
```latex
Q_{MB}(s,a) = \sum P(s'|s,a) \max_a' Q(s',a')
```

**Implementation:**
```python
Q_MB = sum(p_trans * max_Q_next)
```

---

### Temporal Difference Error
**ID:** 215

**Description:** Reward prediction error (dopamine signal)

**Domain:** reward-prediction

**Mathematical Form:**
```latex
\delta(t) = r(t) + \gamma V(s_{t+1}) - V(s_t)
```

**Implementation:**
```python
delta = r + gamma * V_next - V
```

**Reference:** DOI 10.1016/0166-2236(93)90090-C (1993)

---

### Temporal Discounting (Hyperbolic)
**ID:** 217

**Description:** Value decrease over time

**Domain:** motivation

**Mathematical Form:**
```latex
V(t) = \frac{V_0}{1 + kt}
```

**Implementation:**
```python
V = V_0 / (1 + k * t)
```

---

### Threat-Based Urgency
**ID:** 216

**Description:** Threat evaluation for action urgency

**Domain:** motivation

**Mathematical Form:**
```latex
Risk = P(threat) \cdot magnitude(harm)
```

**Implementation:**
```python
risk = p_threat * harm_magnitude
```

---


## Network Dynamics

### Divisive Normalization
**ID:** 178

**Description:** Divisive inhibition for gain control

**Domain:** network-dynamics

**Mathematical Form:**
```latex
y_i = \frac{x_i}{\sigma + \sum_j x_j}
```

**Implementation:**
```python
y = x / (sigma + np.sum(x))
```

---

### Fisher Information (Population Coding)
**ID:** 181

**Description:** Information encoded by neural population

**Domain:** network-dynamics

**Mathematical Form:**
```latex
I(s) = \sum_i \frac{[df_i/ds]^2}{f_i(s)}
```

---

### Hopfield Network Energy
**ID:** 179

**Description:** Energy function for Hopfield attractor networks

**Domain:** network-dynamics

**Mathematical Form:**
```latex
E = -\frac{1}{2} \sum_{ij} w_{ij} s_i s_j - \sum_i \theta_i s_i
```

**Implementation:**
```python
E = -0.5 * np.dot(s, np.dot(w, s)) - np.dot(theta, s)
```

---

### LSTM Cell State
**ID:** 188

**Description:** LSTM cell state update

**Domain:** network-dynamics

**Mathematical Form:**
```latex
C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t
```

**Implementation:**
```python
C_t = f_t * C_prev + i_t * C_tilde
```

---

### LSTM Forget Gate
**ID:** 186

**Description:** LSTM forget gate dynamics

**Domain:** network-dynamics

**Mathematical Form:**
```latex
f_t = \sigma(W_f [h_{t-1}, x_t] + b_f)
```

**Implementation:**
```python
f_t = sigmoid(W_f @ np.hstack([h_prev, x]) + b_f)
```

---

### LSTM Input Gate
**ID:** 187

**Description:** LSTM input gate dynamics

**Domain:** network-dynamics

**Mathematical Form:**
```latex
i_t = \sigma(W_i [h_{t-1}, x_t] + b_i)
```

**Implementation:**
```python
i_t = sigmoid(W_i @ np.hstack([h_prev, x]) + b_i)
```

---

### Pattern Completion (Autoassociative)
**ID:** 184

**Description:** Retrieve full pattern from partial cue

**Domain:** network-dynamics

**Mathematical Form:**
```latex
y = Wx
```

**Implementation:**
```python
y = np.dot(W, x)
```

---

### Phase Oscillator
**ID:** 189

**Description:** Coupled phase oscillators for synchronization

**Domain:** network-dynamics

**Mathematical Form:**
```latex
\frac{d\theta}{dt} = \omega + K \sin(\theta_j - \theta_i)
```

**Implementation:**
```python
dtheta_dt = omega + K * np.sin(theta_j - theta)
```

---

### Population Vector Decoding
**ID:** 180

**Description:** Decode stimulus from population response

**Domain:** network-dynamics

**Mathematical Form:**
```latex
v_{pop} = \frac{\sum_i r_i d_i}{\sum_i r_i}
```

**Implementation:**
```python
v_pop = np.sum(r * d) / np.sum(r)
```

---

### Prediction Error (Predictive Coding)
**ID:** 192

**Description:** Mismatch between observation and prediction

**Domain:** network-dynamics

**Mathematical Form:**
```latex
\varepsilon_l = x_l - \mu_l
```

**Implementation:**
```python
epsilon = x - mu
```

---

### Predictive Coding Hierarchy
**ID:** 191

**Description:** Hierarchical prediction in predictive coding

**Domain:** network-dynamics

**Mathematical Form:**
```latex
\mu_l = f(\mu_{l+1})
```

**Implementation:**
```python
mu_l = f(mu_next)
```

---

### Principal Component Analysis
**ID:** 182

**Description:** Dimensionality reduction via PCA

**Domain:** network-dynamics

**Mathematical Form:**
```latex
x_{reduced} = W^T (x - \mu)
```

**Implementation:**
```python
x_red = np.dot(W.T, x - mu)
```

---

### Recurrent Neural Network
**ID:** 185

**Description:** Continuous recurrent neural network dynamics

**Domain:** network-dynamics

**Mathematical Form:**
```latex
\tau \frac{dy}{dt} = -y + f(W_{rec} y + W_{in} x + b)
```

**Implementation:**
```python
dy_dt = (-y + f(W_rec @ y + W_in @ x + b)) / tau
```

---

### Softmax Normalization
**ID:** 177

**Description:** Probability distribution from scores

**Domain:** network-dynamics

**Mathematical Form:**
```latex
y_i = \frac{\exp(x_i)}{\sum_j \exp(x_j)}
```

**Implementation:**
```python
y = np.exp(x) / np.sum(np.exp(x))
```

---

### Sparse Coding
**ID:** 183

**Description:** Sparse representation learning

**Domain:** network-dynamics

**Mathematical Form:**
```latex
minimize ||x - W s||^2 + \lambda ||s||_1
```

**Implementation:**
```python
minimize squared_error(x, W @ s) + lambda * L1_norm(s)
```

---

### Wilson-Cowan Equations
**ID:** 190

**Description:** Population rate model with excitation/inhibition

**Domain:** network-dynamics

**Mathematical Form:**
```latex
\tau_E \frac{dE}{dt} = -E + f_E(w_{EE}E - w_{EI}I + I_{ext})
```

**Implementation:**
```python
dE_dt = (-E + f_E(w_EE*E - w_EI*I + I_ext)) / tau_E
```

---


## Neural Networks

### Mean-Field Firing Rate
**ID:** 34

**Description:** Mean-field firing rate for LIF neurons with noise

**Domain:** mean-field

**Origin:** mean-field

**Mathematical Form:**
```latex
\nu = \phi(\mu, \sigma) = \left( \tau_{ref} + \tau_m \sqrt{\pi} \int_{(V_{reset}-\mu)/\sigma}^{(V_{th}-\mu)/\sigma} e^{u^2}(1+\text{erf}(u)) du \right)^{-1}
```

---

### Mean-Field Firing Rate
**ID:** 111

**Description:** Mean-field firing rate for LIF neurons with noise

**Domain:** mean-field

**Origin:** mean-field

**Mathematical Form:**
```latex
\nu = \phi(\mu, \sigma) = \left( \tau_{ref} + \tau_m \sqrt{\pi} \int_{(V_{reset}-\mu)/\sigma}^{(V_{th}-\mu)/\sigma} e^{u^2}(1+\text{erf}(u)) du \right)^{-1}
```

---

### Neural Sigmoid Activation
**ID:** 33

**Description:** Sigmoidal firing rate function

**Domain:** neural-networks

**Origin:** activation-function

**Mathematical Form:**
```latex
S(x) = \frac{1}{1 + \exp(-\beta(x - \theta))}
```

**Implementation:**
```python
S = 1 / (1 + np.exp(-beta * (x - theta)))
```

---

### Neural Sigmoid Activation
**ID:** 110

**Description:** Sigmoidal firing rate function

**Domain:** neural-networks

**Origin:** activation-function

**Mathematical Form:**
```latex
S(x) = \frac{1}{1 + \exp(-\beta(x - \theta))}
```

**Implementation:**
```python
S = 1 / (1 + np.exp(-beta * (x - theta)))
```

---

### Wilson-Cowan Excitatory
**ID:** 31

**Description:** Wilson-Cowan excitatory population rate equation

**Domain:** neural-networks

**Origin:** wilson-cowan

**Mathematical Form:**
```latex
\tau_E \frac{dE}{dt} = -E + S_E(w_{EE}E - w_{EI}I + I_{ext})
```

**Implementation:**
```python
dE_dt = (-E + S_E(w_EE*E - w_EI*I + I_ext)) / tau_E
```

**Reference:** DOI 10.1016/S0006-3495(72)86068-5 (1972)

---

### Wilson-Cowan Excitatory
**ID:** 108

**Description:** Wilson-Cowan excitatory population rate equation

**Domain:** neural-networks

**Origin:** wilson-cowan

**Mathematical Form:**
```latex
\tau_E \frac{dE}{dt} = -E + S_E(w_{EE}E - w_{EI}I + I_{ext})
```

**Implementation:**
```python
dE_dt = (-E + S_E(w_EE*E - w_EI*I + I_ext)) / tau_E
```

**Reference:** DOI 10.1016/S0006-3495(72)86068-5 (1972)

---

### Wilson-Cowan Inhibitory
**ID:** 32

**Description:** Wilson-Cowan inhibitory population rate equation

**Domain:** neural-networks

**Origin:** wilson-cowan

**Mathematical Form:**
```latex
\tau_I \frac{dI}{dt} = -I + S_I(w_{IE}E - w_{II}I)
```

**Implementation:**
```python
dI_dt = (-I + S_I(w_IE*E - w_II*I)) / tau_I
```

---

### Wilson-Cowan Inhibitory
**ID:** 109

**Description:** Wilson-Cowan inhibitory population rate equation

**Domain:** neural-networks

**Origin:** wilson-cowan

**Mathematical Form:**
```latex
\tau_I \frac{dI}{dt} = -I + S_I(w_{IE}E - w_{II}I)
```

**Implementation:**
```python
dI_dt = (-I + S_I(w_IE*E - w_II*I)) / tau_I
```

---


## Neuron Models

### AdEx Adaptation Current
**ID:** 11

**Description:** Adaptation current dynamics in AdEx model

**Domain:** computational-neuroscience

**Origin:** adaptive-exponential

**Mathematical Form:**
```latex
\tau_w \frac{dw}{dt} = a(V - V_{rest}) - w
```

**Implementation:**
```python
dw_dt = (a * (V - V_rest) - w) / tau_w
```

---

### AdEx Adaptation Current
**ID:** 88

**Description:** Adaptation current dynamics in AdEx model

**Domain:** computational-neuroscience

**Origin:** adaptive-exponential

**Mathematical Form:**
```latex
\tau_w \frac{dw}{dt} = a(V - V_{rest}) - w
```

**Implementation:**
```python
dw_dt = (a * (V - V_rest) - w) / tau_w
```

---

### Cable Equation
**ID:** 74

**Description:** Passive signal propagation in dendrites

**Domain:** electrophysiology

**Origin:** cable-theory

**Mathematical Form:**
```latex
\lambda^2 \frac{\partial^2 V}{\partial x^2} = \tau_m \frac{\partial V}{\partial t} + V
```

---

### Cable Equation
**ID:** 151

**Description:** Passive signal propagation in dendrites

**Domain:** electrophysiology

**Origin:** cable-theory

**Mathematical Form:**
```latex
\lambda^2 \frac{\partial^2 V}{\partial x^2} = \tau_m \frac{\partial V}{\partial t} + V
```

---

### Exponential Integrate-and-Fire
**ID:** 10

**Description:** LIF with exponential spike initiation for more realistic dynamics

**Domain:** computational-neuroscience

**Origin:** exponential-integrate-fire

**Mathematical Form:**
```latex
\tau_m \frac{dV}{dt} = -(V - V_{rest}) + \Delta_T \exp\left(\frac{V - V_T}{\Delta_T}\right) + R_m I_{ext}
```

**Implementation:**
```python
dV_dt = (-(V - V_rest) + Delta_T * np.exp((V - V_T) / Delta_T) + R_m * I_ext) / tau_m
```

---

### Exponential Integrate-and-Fire
**ID:** 87

**Description:** LIF with exponential spike initiation for more realistic dynamics

**Domain:** computational-neuroscience

**Origin:** exponential-integrate-fire

**Mathematical Form:**
```latex
\tau_m \frac{dV}{dt} = -(V - V_{rest}) + \Delta_T \exp\left(\frac{V - V_T}{\Delta_T}\right) + R_m I_{ext}
```

**Implementation:**
```python
dV_dt = (-(V - V_rest) + Delta_T * np.exp((V - V_T) / Delta_T) + R_m * I_ext) / tau_m
```

---

### FitzHugh-Nagumo Recovery
**ID:** 15

**Description:** FitzHugh-Nagumo recovery variable

**Domain:** computational-neuroscience

**Origin:** fitzhugh-nagumo

**Mathematical Form:**
```latex
\frac{dw}{dt} = \epsilon(v + a - bw)
```

**Implementation:**
```python
dw_dt = epsilon * (v + a - b * w)
```

---

### FitzHugh-Nagumo Recovery
**ID:** 92

**Description:** FitzHugh-Nagumo recovery variable

**Domain:** computational-neuroscience

**Origin:** fitzhugh-nagumo

**Mathematical Form:**
```latex
\frac{dw}{dt} = \epsilon(v + a - bw)
```

**Implementation:**
```python
dw_dt = epsilon * (v + a - b * w)
```

---

### FitzHugh-Nagumo Voltage
**ID:** 14

**Description:** FitzHugh-Nagumo model - simplified HH capturing excitability

**Domain:** computational-neuroscience

**Origin:** fitzhugh-nagumo

**Mathematical Form:**
```latex
\frac{dv}{dt} = v - \frac{v^3}{3} - w + I_{ext}
```

**Implementation:**
```python
dv_dt = v - v**3/3 - w + I_ext
```

---

### FitzHugh-Nagumo Voltage
**ID:** 91

**Description:** FitzHugh-Nagumo model - simplified HH capturing excitability

**Domain:** computational-neuroscience

**Origin:** fitzhugh-nagumo

**Mathematical Form:**
```latex
\frac{dv}{dt} = v - \frac{v^3}{3} - w + I_{ext}
```

**Implementation:**
```python
dv_dt = v - v**3/3 - w + I_ext
```

---

### Hodgkin-Huxley Membrane Equation
**ID:** 1

**Description:** Main membrane potential equation from the Hodgkin-Huxley model describing action potential generation

**Domain:** electrophysiology

**Origin:** hodgkin-huxley

**Mathematical Form:**
```latex
C_m \frac{dV}{dt} = -g_{Na} m^3 h (V - E_{Na}) - g_K n^4 (V - E_K) - g_L (V - E_L) + I_{ext}
```

**Implementation:**
```python
dV_dt = (I_ext - g_Na * m**3 * h * (V - E_Na) - g_K * n**4 * (V - E_K) - g_L * (V - E_L)) / C_m
```

**Reference:** DOI 10.1113/jphysiol.1952.sp004764 (1952)

---

### Hodgkin-Huxley Membrane Equation
**ID:** 78

**Description:** Main membrane potential equation from the Hodgkin-Huxley model describing action potential generation

**Domain:** electrophysiology

**Origin:** hodgkin-huxley

**Mathematical Form:**
```latex
C_m \frac{dV}{dt} = -g_{Na} m^3 h (V - E_{Na}) - g_K n^4 (V - E_K) - g_L (V - E_L) + I_{ext}
```

**Implementation:**
```python
dV_dt = (I_ext - g_Na * m**3 * h * (V - E_Na) - g_K * n**4 * (V - E_K) - g_L * (V - E_L)) / C_m
```

**Reference:** DOI 10.1113/jphysiol.1952.sp004764 (1952)

---

### Izhikevich Membrane Equation
**ID:** 12

**Description:** Izhikevich model membrane potential dynamics

**Domain:** computational-neuroscience

**Origin:** izhikevich

**Mathematical Form:**
```latex
\frac{dv}{dt} = 0.04v^2 + 5v + 140 - u + I
```

**Implementation:**
```python
dv_dt = 0.04 * v**2 + 5 * v + 140 - u + I
```

**Reference:** DOI 10.1109/TNN.2004.832719 (2003)

---

### Izhikevich Membrane Equation
**ID:** 89

**Description:** Izhikevich model membrane potential dynamics

**Domain:** computational-neuroscience

**Origin:** izhikevich

**Mathematical Form:**
```latex
\frac{dv}{dt} = 0.04v^2 + 5v + 140 - u + I
```

**Implementation:**
```python
dv_dt = 0.04 * v**2 + 5 * v + 140 - u + I
```

**Reference:** DOI 10.1109/TNN.2004.832719 (2003)

---

### Izhikevich Recovery Variable
**ID:** 13

**Description:** Izhikevich model recovery variable dynamics

**Domain:** computational-neuroscience

**Origin:** izhikevich

**Mathematical Form:**
```latex
\frac{du}{dt} = a(bv - u)
```

**Implementation:**
```python
du_dt = a * (b * v - u)
```

---

### Izhikevich Recovery Variable
**ID:** 90

**Description:** Izhikevich model recovery variable dynamics

**Domain:** computational-neuroscience

**Origin:** izhikevich

**Mathematical Form:**
```latex
\frac{du}{dt} = a(bv - u)
```

**Implementation:**
```python
du_dt = a * (b * v - u)
```

---

### Leaky Integrate-and-Fire
**ID:** 9

**Description:** Simple neuron model with passive leak current and threshold-based spiking

**Domain:** computational-neuroscience

**Origin:** integrate-and-fire

**Mathematical Form:**
```latex
\tau_m \frac{dV}{dt} = -(V - V_{rest}) + R_m I_{ext}
```

**Implementation:**
```python
dV_dt = (-(V - V_rest) + R_m * I_ext) / tau_m
```

---

### Leaky Integrate-and-Fire
**ID:** 86

**Description:** Simple neuron model with passive leak current and threshold-based spiking

**Domain:** computational-neuroscience

**Origin:** integrate-and-fire

**Mathematical Form:**
```latex
\tau_m \frac{dV}{dt} = -(V - V_{rest}) + R_m I_{ext}
```

**Implementation:**
```python
dV_dt = (-(V - V_rest) + R_m * I_ext) / tau_m
```

---

### Morris-Lecar Membrane
**ID:** 16

**Description:** Morris-Lecar model - 2D reduction of HH for barnacle muscle

**Domain:** electrophysiology

**Origin:** morris-lecar

**Mathematical Form:**
```latex
C \frac{dV}{dt} = I - g_L(V-V_L) - g_{Ca}m_\infty(V)(V-V_{Ca}) - g_K w(V-V_K)
```

**Implementation:**
```python
dV_dt = (I - g_L*(V-V_L) - g_Ca*m_inf(V)*(V-V_Ca) - g_K*w*(V-V_K)) / C
```

---

### Morris-Lecar Membrane
**ID:** 93

**Description:** Morris-Lecar model - 2D reduction of HH for barnacle muscle

**Domain:** electrophysiology

**Origin:** morris-lecar

**Mathematical Form:**
```latex
C \frac{dV}{dt} = I - g_L(V-V_L) - g_{Ca}m_\infty(V)(V-V_{Ca}) - g_K w(V-V_K)
```

**Implementation:**
```python
dV_dt = (I - g_L*(V-V_L) - g_Ca*m_inf(V)*(V-V_Ca) - g_K*w*(V-V_K)) / C
```

---


## Neuroscience

### Cortical Hebbian Learning
**ID:** 244

**Description:** Local Hebbian-like learning from prediction error

**Domain:** synaptic-plasticity

**Origin:** predictive-coding

**Mathematical Form:**
```latex
\Delta W_i = -\alpha \cdot e_i^{(t)} \cdot h_{i-1}^{(t)T}
```

**Implementation:**
```python
dW = -alpha * outer(error, h_prev)
```

**Reference:** DOI arXiv:1511.06701 (2015)

---

### Cortical Recurrence
**ID:** 245

**Description:** Recurrent refinement of hidden state through iterations

**Domain:** network-dynamics

**Origin:** predictive-coding

**Mathematical Form:**
```latex
h_i^{(t)} = \tanh(W_i \cdot h_{i-1}^{(t)} + U_i \cdot h_i^{(t-1)} + b_i)
```

**Implementation:**
```python
h = tanh(W @ h_prev_layer + U @ h_prev_time + b)
```

**Reference:** DOI arXiv:1511.06701 (2015)

---

### Error Backpropagation in Cortex
**ID:** 243

**Description:** Propagate error signal to lower layers

**Domain:** predictive-coding

**Origin:** predictive-coding

**Mathematical Form:**
```latex
e_{i-1}^{(t)} = W_i^T e_i^{(t)}
```

**Implementation:**
```python
error_lower = W.T @ error_upper
```

**Reference:** DOI arXiv:1511.06701 (2015)

---

### Goldman-Hodgkin-Katz Voltage Equation
**ID:** 73

**Description:** Resting membrane potential from multiple ions

**Domain:** electrophysiology

**Origin:** GHK

**Mathematical Form:**
```latex
V_m = \frac{RT}{F} \ln \frac{P_K[K^+]_o + P_{Na}[Na^+]_o + P_{Cl}[Cl^-]_i}{P_K[K^+]_i + P_{Na}[Na^+]_i + P_{Cl}[Cl^-]_o}
```

---

### Goldman-Hodgkin-Katz Voltage Equation
**ID:** 150

**Description:** Resting membrane potential from multiple ions

**Domain:** electrophysiology

**Origin:** GHK

**Mathematical Form:**
```latex
V_m = \frac{RT}{F} \ln \frac{P_K[K^+]_o + P_{Na}[Na^+]_o + P_{Cl}[Cl^-]_i}{P_K[K^+]_i + P_{Na}[Na^+]_i + P_{Cl}[Cl^-]_o}
```

---

### Nernst Equation
**ID:** 72

**Description:** Equilibrium potential for an ion

**Domain:** electrophysiology

**Origin:** nernst

**Mathematical Form:**
```latex
E = \frac{RT}{zF} \ln \frac{[ion]_{out}}{[ion]_{in}}
```

**Implementation:**
```python
E = (R * T) / (z * F) * np.log(ion_out / ion_in)
```

---

### Nernst Equation
**ID:** 149

**Description:** Equilibrium potential for an ion

**Domain:** electrophysiology

**Origin:** nernst

**Mathematical Form:**
```latex
E = \frac{RT}{zF} \ln \frac{[ion]_{out}}{[ion]_{in}}
```

**Implementation:**
```python
E = (R * T) / (z * F) * np.log(ion_out / ion_in)
```

---

### Prediction Error
**ID:** 242

**Description:** Difference between actual input and prediction

**Domain:** predictive-coding

**Origin:** predictive-coding

**Mathematical Form:**
```latex
e_i^{(t)} = x_i^{(t)} - \hat{x}_i^{(t)}
```

**Implementation:**
```python
error = x - x_hat
```

**Reference:** DOI arXiv:1511.06701 (2015)

---

### Predictive Coding Forward Pass
**ID:** 241

**Description:** Prediction of next layer input from current hidden state

**Domain:** predictive-coding

**Origin:** predictive-coding

**Mathematical Form:**
```latex
\hat{x}_i^{(t)} = f_\theta(h_{i-1}^{(t)})
```

**Implementation:**
```python
x_hat = activation(W @ h_prev + b)
```

**Reference:** DOI arXiv:1511.06701 (2015)

---


## Optimization

### Adam: First Moment
**ID:** 230

**Description:** Adam exponential moving average of gradients

**Domain:** optimization

**Mathematical Form:**
```latex
m \leftarrow \beta_1 m + (1-\beta_1) \nabla L
```

---

### Adam: Second Moment
**ID:** 231

**Description:** Adam exponential moving average of squared gradients

**Domain:** optimization

**Mathematical Form:**
```latex
v \leftarrow \beta_2 v + (1-\beta_2) (\nabla L)^2
```

---

### EM Algorithm: E-Step
**ID:** 238

**Description:** Expectation step of EM algorithm

**Domain:** unsupervised-learning

**Mathematical Form:**
```latex
Q(\theta|\theta_{old}) = E_Z[\log P(X,Z|\theta) | X, \theta_{old}]
```

---

### Fuzzy Logic AND
**ID:** 236

**Description:** Min t-norm for fuzzy AND

**Domain:** fuzzy-logic

**Mathematical Form:**
```latex
\mu_{AND} = \min(\mu_A, \mu_B)
```

**Implementation:**
```python
fuzzy_and = min(mu_A, mu_B)
```

---

### Fuzzy Logic OR
**ID:** 237

**Description:** Max t-conorm for fuzzy OR

**Domain:** fuzzy-logic

**Mathematical Form:**
```latex
\mu_{OR} = \max(\mu_A, \mu_B)
```

**Implementation:**
```python
fuzzy_or = max(mu_A, mu_B)
```

---

### Gradient Descent
**ID:** 228

**Description:** Basic gradient descent update

**Domain:** optimization

**Mathematical Form:**
```latex
\theta \leftarrow \theta - \eta \nabla L(\theta)
```

**Implementation:**
```python
theta = theta - eta * gradient
```

---

### Graph Attention
**ID:** 235

**Description:** Attention mechanism for graphs

**Domain:** graph-neural-networks

**Mathematical Form:**
```latex
\alpha_{ij} = softmax(LeakyReLU(a^T[W h_i || W h_j]))
```

---

### Graph Convolutional Layer
**ID:** 234

**Description:** Graph convolution for relational data

**Domain:** graph-neural-networks

**Mathematical Form:**
```latex
H^{(l+1)} = \sigma(D^{-1/2} A D^{-1/2} H^{(l)} W^{(l)})
```

---

### Matrix Multiplication
**ID:** 233

**Description:** Bilinear tensor contraction

**Domain:** tensor-operations

**Mathematical Form:**
```latex
C_{ij} = \sum_k A_{ik} B_{kj}
```

**Implementation:**
```python
C = np.dot(A, B)
```

---

### RMSprop Optimizer
**ID:** 232

**Description:** Root mean square propagation optimizer

**Domain:** optimization

**Mathematical Form:**
```latex
E[g^2]_t = \beta E[g^2]_{t-1} + (1-\beta) g_t^2, \theta \leftarrow \theta - \eta g_t/\sqrt{E[g^2]_t + \epsilon}
```

---

### SGD with Momentum
**ID:** 229

**Description:** Stochastic gradient descent with momentum

**Domain:** optimization

**Mathematical Form:**
```latex
v \leftarrow \beta v + \nabla L, \theta \leftarrow \theta - \eta v
```

**Implementation:**
```python
v = beta * v + grad; theta = theta - eta * v
```

---

### VAE ELBO Loss
**ID:** 240

**Description:** Evidence lower bound for VAE

**Domain:** generative-models

**Mathematical Form:**
```latex
L = -E_q[\log p_\theta(x|z)] + KL(q_\phi(z|x) || p(z))
```

---

### VAE Encoder
**ID:** 239

**Description:** Variational autoencoder inference network

**Domain:** generative-models

**Mathematical Form:**
```latex
q_\phi(z|x) = \mathcal{N}(\mu_\phi(x), \sigma^2_\phi(x))
```

---


## Population Dynamics

### Competitive Lotka-Volterra (Species 1)
**ID:** 68

**Description:** Competition between two species - species 1

**Domain:** ecology

**Origin:** competitive-lotka-volterra

**Mathematical Form:**
```latex
\frac{dN_1}{dt} = r_1 N_1 \left(1 - \frac{N_1 + \alpha_{12} N_2}{K_1}\right)
```

**Implementation:**
```python
dN1_dt = r1 * N1 * (1 - (N1 + alpha12 * N2) / K1)
```

---

### Competitive Lotka-Volterra (Species 1)
**ID:** 145

**Description:** Competition between two species - species 1

**Domain:** ecology

**Origin:** competitive-lotka-volterra

**Mathematical Form:**
```latex
\frac{dN_1}{dt} = r_1 N_1 \left(1 - \frac{N_1 + \alpha_{12} N_2}{K_1}\right)
```

**Implementation:**
```python
dN1_dt = r1 * N1 * (1 - (N1 + alpha12 * N2) / K1)
```

---

### Exponential Growth
**ID:** 64

**Description:** Unlimited exponential population growth

**Domain:** population-dynamics

**Origin:** exponential-growth

**Mathematical Form:**
```latex
\frac{dN}{dt} = rN
```

**Implementation:**
```python
dN_dt = r * N
```

---

### Exponential Growth
**ID:** 141

**Description:** Unlimited exponential population growth

**Domain:** population-dynamics

**Origin:** exponential-growth

**Mathematical Form:**
```latex
\frac{dN}{dt} = rN
```

**Implementation:**
```python
dN_dt = r * N
```

---

### Logistic Growth
**ID:** 65

**Description:** Density-dependent population growth

**Domain:** population-dynamics

**Origin:** logistic-growth

**Mathematical Form:**
```latex
\frac{dN}{dt} = rN\left(1 - \frac{N}{K}\right)
```

**Implementation:**
```python
dN_dt = r * N * (1 - N / K)
```

---

### Logistic Growth
**ID:** 142

**Description:** Density-dependent population growth

**Domain:** population-dynamics

**Origin:** logistic-growth

**Mathematical Form:**
```latex
\frac{dN}{dt} = rN\left(1 - \frac{N}{K}\right)
```

**Implementation:**
```python
dN_dt = r * N * (1 - N / K)
```

---

### Lotka-Volterra Predator
**ID:** 66

**Description:** Predator population dynamics

**Domain:** ecology

**Origin:** lotka-volterra

**Mathematical Form:**
```latex
\frac{dP}{dt} = -dP + \beta NP
```

**Implementation:**
```python
dP_dt = -d * P + beta * N * P
```

---

### Lotka-Volterra Predator
**ID:** 143

**Description:** Predator population dynamics

**Domain:** ecology

**Origin:** lotka-volterra

**Mathematical Form:**
```latex
\frac{dP}{dt} = -dP + \beta NP
```

**Implementation:**
```python
dP_dt = -d * P + beta * N * P
```

---

### Lotka-Volterra Prey
**ID:** 67

**Description:** Prey population dynamics

**Domain:** ecology

**Origin:** lotka-volterra

**Mathematical Form:**
```latex
\frac{dN}{dt} = rN - \alpha NP
```

**Implementation:**
```python
dN_dt = r * N - alpha * N * P
```

---

### Lotka-Volterra Prey
**ID:** 144

**Description:** Prey population dynamics

**Domain:** ecology

**Origin:** lotka-volterra

**Mathematical Form:**
```latex
\frac{dN}{dt} = rN - \alpha NP
```

**Implementation:**
```python
dN_dt = r * N - alpha * N * P
```

---

### Oscillatory Synchronization
**ID:** 263

**Description:** Phase-locking of oscillations for coordinated communication

**Domain:** network-dynamics

**Origin:** kuramoto-model

**Mathematical Form:**
```latex
\dot{\phi}_i = \omega_i + K \sum_j \sin(\phi_j - \phi_i)
```

**Implementation:**
```python
dphi = omega + K * sum(sin(phi_j - phi_i) for j)
```

**Reference:** DOI Nature:355(6359) (1992)

---

### Routed Signal
**ID:** 261

**Description:** Information flow from source region through router to target

**Domain:** computational-neuroscience

**Origin:** thalamic-gating

**Mathematical Form:**
```latex
y_j = \sum_i R_{ij} \cdot \mathrm{project}_j(x_i)
```

**Implementation:**
```python
y = sum(R[i,j] * project_j(x_i) for i in sources)
```

**Reference:** DOI Neuroscience:23(3) (2020)

---

### Thalamic Bandwidth Control
**ID:** 262

**Description:** Capacity limit on each communication channel

**Domain:** computational-neuroscience

**Origin:** thalamic-gating

**Mathematical Form:**
```latex
y_j = \text{capacity}_{ij} \cdot y_j, \quad \text{capacity} \in [0,1]
```

**Implementation:**
```python
y = capacity * y
```

**Reference:** DOI Neuroscience:23(3) (2020)

---

### Thalamic Routing Gate
**ID:** 260

**Description:** Learned gating matrix determining information flow

**Domain:** computational-neuroscience

**Origin:** thalamic-gating

**Mathematical Form:**
```latex
R_{ij} = \mathrm{softmax}(\text{policy}(x_i))
```

**Implementation:**
```python
R = softmax(policy_net(x))
```

**Reference:** DOI Neuroscience:23(3) (2020)

---


## Probabilistic Inference

### Bayes' Rule
**ID:** 222

**Description:** Posterior from likelihood and prior

**Domain:** bayesian-inference

**Mathematical Form:**
```latex
P(\theta|D) = \frac{P(D|\theta) P(\theta)}{P(D)}
```

**Implementation:**
```python
posterior = likelihood * prior / evidence
```

---

### Belief Propagation (Sum-Product)
**ID:** 226

**Description:** Message passing for probabilistic inference

**Domain:** graphical-models

**Mathematical Form:**
```latex
m_{ij}(x_j) = \sum_{x_i} \psi(x_i,x_j) \phi(x_i) \prod_{k \in N(i)\j} m_{ki}(x_i)
```

---

### Kalman Filter: Predict
**ID:** 224

**Description:** Kalman filter prediction step

**Domain:** filtering

**Mathematical Form:**
```latex
\hat{x}_{t|t-1} = F \hat{x}_{t-1|t-1}, P_{t|t-1} = F P_{t-1|t-1} F^T + Q
```

---

### Kalman Filter: Update
**ID:** 225

**Description:** Kalman gain computation

**Domain:** filtering

**Mathematical Form:**
```latex
K_t = P_{t|t-1} H^T (H P_{t|t-1} H^T + R)^{-1}
```

---

### Log Odds Update
**ID:** 223

**Description:** Logarithmic odds update rule

**Domain:** bayesian-inference

**Mathematical Form:**
```latex
\log\frac{P(A|D)}{P(\neg A|D)} = \log\frac{P(D|A)}{P(D|\neg A)} + \log\frac{P(A)}{P(\neg A)}
```

---

### Max-Product Algorithm
**ID:** 227

**Description:** Max-product (Viterbi) for MAP inference

**Domain:** graphical-models

**Mathematical Form:**
```latex
m_{ij}(x_j) = \max_{x_i} \psi(x_i,x_j) \phi(x_i) \prod_{k \in N(i)\j} m_{ki}(x_i)
```

---


## Sensory Computations

### Cochlear Filterbank
**ID:** 197

**Description:** Frequency analysis in auditory system

**Domain:** sensory-computation

**Mathematical Form:**
```latex
H_i(f) = \frac{(f/f_i)^p}{(f/f_i)^p + q}
```

---

### Complex Cell Response
**ID:** 196

**Description:** Orientation-selective response with phase invariance

**Domain:** sensory-computation

**Mathematical Form:**
```latex
C = \sqrt{S_{even}^2 + S_{odd}^2}
```

**Implementation:**
```python
C = np.sqrt(S_even**2 + S_odd**2)
```

---

### Convolutional Filtering (V1)
**ID:** 193

**Description:** Receptive field computation via convolution

**Domain:** sensory-computation

**Mathematical Form:**
```latex
r(x,y) = \sum_{ij} w(i,j) I(x+i, y+j)
```

**Implementation:**
```python
r = convolve2d(I, w)
```

---

### Edge Detection (Sensory)
**ID:** 195

**Description:** Spatial gradient for edge detection

**Domain:** sensory-computation

**Mathematical Form:**
```latex
I_{edge} = [\partial I/\partial x, \partial I/\partial y]
```

**Implementation:**
```python
I_edge = np.gradient(I)
```

---

### Gabor Filter
**ID:** 194

**Description:** Oriented frequency-selective filter

**Domain:** sensory-computation

**Mathematical Form:**
```latex
G(x,y) = \exp(-(x'^2 + \gamma^2 y'^2)/(2\sigma^2)) \cos(2\pi x'/\lambda + \psi)
```

---

### Gammatone Filter
**ID:** 198

**Description:** Auditory filter approximation

**Domain:** sensory-computation

**Mathematical Form:**
```latex
g(t) = t^{n-1} \exp(-2\pi b t) \cos(2\pi f_c t + \phi)
```

---


## Synaptic Plasticity

### BCM Learning Rule
**ID:** 168

**Description:** Bienenstock-Cooper-Munro rule with sliding threshold

**Domain:** synaptic-plasticity

**Mathematical Form:**
```latex
\frac{dw}{dt} = \eta y (y - \theta) x
```

**Implementation:**
```python
dw_dt = eta * y * (y - theta) * x
```

**Reference:** DOI 10.1523/JNEUROSCI.02-01-00032.1982 (1982)

---

### BCM Phi Function
**ID:** 28

**Description:** BCM selectivity function

**Domain:** synaptic-plasticity

**Origin:** BCM

**Mathematical Form:**
```latex
\phi(c) = c(c - \theta_m)
```

**Implementation:**
```python
phi = c * (c - theta_m)
```

---

### BCM Phi Function
**ID:** 105

**Description:** BCM selectivity function

**Domain:** synaptic-plasticity

**Origin:** BCM

**Mathematical Form:**
```latex
\phi(c) = c(c - \theta_m)
```

**Implementation:**
```python
phi = c * (c - theta_m)
```

---

### BCM Plasticity Rule
**ID:** 27

**Description:** Bienenstock-Cooper-Munro rule with sliding threshold

**Domain:** synaptic-plasticity

**Origin:** BCM

**Mathematical Form:**
```latex
\frac{dw}{dt} = \eta \phi(c) c_{pre}
```

**Implementation:**
```python
dw_dt = eta * phi(c) * c_pre
```

**Reference:** DOI 10.1523/JNEUROSCI.02-01-00032.1982 (1982)

---

### BCM Plasticity Rule
**ID:** 104

**Description:** Bienenstock-Cooper-Munro rule with sliding threshold

**Domain:** synaptic-plasticity

**Origin:** BCM

**Mathematical Form:**
```latex
\frac{dw}{dt} = \eta \phi(c) c_{pre}
```

**Implementation:**
```python
dw_dt = eta * phi(c) * c_pre
```

**Reference:** DOI 10.1523/JNEUROSCI.02-01-00032.1982 (1982)

---

### BCM Threshold
**ID:** 169

**Description:** Sliding modification threshold in BCM rule

**Domain:** synaptic-plasticity

**Mathematical Form:**
```latex
\theta = \langle y^2 \rangle
```

**Implementation:**
```python
theta = mean(y**2)
```

---

### Calcium-Based Plasticity
**ID:** 30

**Description:** Plasticity driven by calcium concentration levels

**Domain:** synaptic-plasticity

**Origin:** calcium-based

**Mathematical Form:**
```latex
\frac{dw}{dt} = \gamma_p \Omega([Ca^{2+}]) - \gamma_d \Omega([Ca^{2+}]) w
```

**Implementation:**
```python
dw_dt = gamma_p * Omega_p(Ca) - gamma_d * Omega_d(Ca) * w
```

---

### Calcium-Based Plasticity
**ID:** 107

**Description:** Plasticity driven by calcium concentration levels

**Domain:** synaptic-plasticity

**Origin:** calcium-based

**Mathematical Form:**
```latex
\frac{dw}{dt} = \gamma_p \Omega([Ca^{2+}]) - \gamma_d \Omega([Ca^{2+}]) w
```

**Implementation:**
```python
dw_dt = gamma_p * Omega_p(Ca) - gamma_d * Omega_d(Ca) * w
```

---

### Covariance Learning
**ID:** 171

**Description:** Covariance-based Hebbian rule

**Domain:** synaptic-plasticity

**Mathematical Form:**
```latex
\Delta w = \eta (x - \langle x \rangle)(y - \langle y \rangle)
```

**Implementation:**
```python
dw = eta * (x - mean_x) * (y - mean_y)
```

---

### Hebbian Learning
**ID:** 170

**Description:** Basic Hebbian learning rule

**Domain:** synaptic-plasticity

**Mathematical Form:**
```latex
\Delta w = \eta x y
```

**Implementation:**
```python
dw = eta * x * y
```

---

### Oja's Learning Rule
**ID:** 29

**Description:** Hebbian rule with weight normalization (PCA)

**Domain:** synaptic-plasticity

**Origin:** Oja

**Mathematical Form:**
```latex
\Delta w_i = \eta y (x_i - y w_i)
```

**Implementation:**
```python
dw = eta * y * (x - y * w)
```

---

### Oja's Learning Rule
**ID:** 106

**Description:** Hebbian rule with weight normalization (PCA)

**Domain:** synaptic-plasticity

**Origin:** Oja

**Mathematical Form:**
```latex
\Delta w_i = \eta y (x_i - y w_i)
```

**Implementation:**
```python
dw = eta * y * (x - y * w)
```

---

### Oja's Learning Rule (Cognitive)
**ID:** 172

**Description:** Hebbian rule with weight normalization (PCA)

**Domain:** synaptic-plasticity

**Mathematical Form:**
```latex
\Delta w = \eta y (x - w y)
```

**Implementation:**
```python
dw = eta * y * (x - w * y)
```

---

### Pair-Based STDP
**ID:** 25

**Description:** Classic spike-timing dependent plasticity rule

**Domain:** synaptic-plasticity

**Origin:** STDP

**Mathematical Form:**
```latex
\Delta w = \begin{cases} A_+ \exp(-\Delta t / \tau_+) & \text{if } \Delta t > 0 \\ -A_- \exp(\Delta t / \tau_-) & \text{if } \Delta t < 0 \end{cases}
```

**Implementation:**
```python
dw = A_plus * np.exp(-dt/tau_plus) if dt > 0 else -A_minus * np.exp(dt/tau_minus)
```

**Reference:** DOI 10.1523/JNEUROSCI.18-24-10464.1998 (1998)

---

### Pair-Based STDP
**ID:** 102

**Description:** Classic spike-timing dependent plasticity rule

**Domain:** synaptic-plasticity

**Origin:** STDP

**Mathematical Form:**
```latex
\Delta w = \begin{cases} A_+ \exp(-\Delta t / \tau_+) & \text{if } \Delta t > 0 \\ -A_- \exp(\Delta t / \tau_-) & \text{if } \Delta t < 0 \end{cases}
```

**Implementation:**
```python
dw = A_plus * np.exp(-dt/tau_plus) if dt > 0 else -A_minus * np.exp(dt/tau_minus)
```

**Reference:** DOI 10.1523/JNEUROSCI.18-24-10464.1998 (1998)

---

### Short-Term Depression
**ID:** 175

**Description:** Resource depletion in short-term plasticity

**Domain:** synaptic-plasticity

**Mathematical Form:**
```latex
\frac{dx}{dt} = \frac{1-x}{\tau_{rec}}
```

**Implementation:**
```python
dx_dt = (1 - x) / tau_rec
```

---

### Short-Term Facilitation
**ID:** 176

**Description:** Increased release probability in short-term plasticity

**Domain:** synaptic-plasticity

**Mathematical Form:**
```latex
\frac{du}{dt} = \frac{U-u}{\tau_{fac}}
```

**Implementation:**
```python
du_dt = (U - u) / tau_fac
```

---

### Spike-Timing Dependent Plasticity (STDP)
**ID:** 173

**Description:** STDP: potentiation if presynaptic fires before postsynaptic

**Domain:** synaptic-plasticity

**Mathematical Form:**
```latex
\Delta w(\Delta t) = \begin{cases} A_+ \exp(-\Delta t/\tau_+) & \text{if } \Delta t > 0 \\ -A_- \exp(\Delta t/\tau_-) & \text{if } \Delta t < 0 \end{cases}
```

**Implementation:**
```python
dw = A_plus * np.exp(-dt/tau_plus) if dt > 0 else -A_minus * np.exp(dt/tau_minus)
```

**Reference:** DOI 10.1523/JNEUROSCI.18-24-10464.1998 (1998)

---

### Triplet STDP
**ID:** 174

**Description:** Triplet STDP capturing frequency dependence

**Domain:** synaptic-plasticity

**Mathematical Form:**
```latex
\Delta w = r_1(t)(A_2^+ + A_3^+ r_2(t-\epsilon)) - o_1(t)(A_2^- + A_3^- o_2(t-\epsilon))
```

---

### Triplet STDP Rule
**ID:** 26

**Description:** Triplet STDP capturing frequency dependence

**Domain:** synaptic-plasticity

**Origin:** triplet-STDP

**Mathematical Form:**
```latex
\Delta w = r_1(t) \left( A_2^+ + A_3^+ r_2(t-\epsilon) \right) - o_1(t) \left( A_2^- + A_3^- o_2(t-\epsilon) \right)
```

**Reference:** DOI 10.1523/JNEUROSCI.1425-06.2006 (2006)

---

### Triplet STDP Rule
**ID:** 103

**Description:** Triplet STDP capturing frequency dependence

**Domain:** synaptic-plasticity

**Origin:** triplet-STDP

**Mathematical Form:**
```latex
\Delta w = r_1(t) \left( A_2^+ + A_3^+ r_2(t-\epsilon) \right) - o_1(t) \left( A_2^- + A_3^- o_2(t-\epsilon) \right)
```

**Reference:** DOI 10.1523/JNEUROSCI.1425-06.2006 (2006)

---


## Synaptic Transmission

### AMPA Gating Dynamics
**ID:** 18

**Description:** AMPA receptor gating variable dynamics

**Domain:** synaptic-transmission

**Origin:** AMPA

**Mathematical Form:**
```latex
\frac{ds}{dt} = \alpha [T](1-s) - \beta s
```

**Implementation:**
```python
ds_dt = alpha * T * (1 - s) - beta * s
```

---

### AMPA Gating Dynamics
**ID:** 95

**Description:** AMPA receptor gating variable dynamics

**Domain:** synaptic-transmission

**Origin:** AMPA

**Mathematical Form:**
```latex
\frac{ds}{dt} = \alpha [T](1-s) - \beta s
```

**Implementation:**
```python
ds_dt = alpha * T * (1 - s) - beta * s
```

---

### AMPA Synaptic Current
**ID:** 17

**Description:** AMPA receptor-mediated excitatory synaptic current

**Domain:** synaptic-transmission

**Origin:** AMPA

**Mathematical Form:**
```latex
I_{AMPA} = g_{AMPA} s (V - E_{AMPA})
```

**Implementation:**
```python
I_AMPA = g_AMPA * s * (V - E_AMPA)
```

---

### AMPA Synaptic Current
**ID:** 94

**Description:** AMPA receptor-mediated excitatory synaptic current

**Domain:** synaptic-transmission

**Origin:** AMPA

**Mathematical Form:**
```latex
I_{AMPA} = g_{AMPA} s (V - E_{AMPA})
```

**Implementation:**
```python
I_AMPA = g_AMPA * s * (V - E_AMPA)
```

---

### Acetylcholine-Modulated Recurrence
**ID:** 272

**Description:** Thinking depth (recurrence iterations) controlled by acetylcholine

**Domain:** network-dynamics

**Origin:** neuromodulation

**Mathematical Form:**
```latex
D_t = D_0 \cdot (1 + m_{acetylcholine})
```

**Implementation:**
```python
D = D_0 * (1 + m_acetylcholine)
```

**Reference:** DOI Nature:317(6036) (1985)

---

### Alpha Function Synapse
**ID:** 23

**Description:** Alpha function for synaptic conductance time course

**Domain:** synaptic-transmission

**Origin:** alpha-function

**Mathematical Form:**
```latex
g(t) = g_{max} \frac{t-t_0}{\tau} \exp\left(1 - \frac{t-t_0}{\tau}\right)
```

**Implementation:**
```python
g = g_max * (t - t0) / tau * np.exp(1 - (t - t0) / tau)
```

---

### Alpha Function Synapse
**ID:** 100

**Description:** Alpha function for synaptic conductance time course

**Domain:** synaptic-transmission

**Origin:** alpha-function

**Mathematical Form:**
```latex
g(t) = g_{max} \frac{t-t_0}{\tau} \exp\left(1 - \frac{t-t_0}{\tau}\right)
```

**Implementation:**
```python
g = g_max * (t - t0) / tau * np.exp(1 - (t - t0) / tau)
```

---

### Dopamine-Modulated Learning Rate
**ID:** 271

**Description:** Global learning rate modulation by dopamine signal

**Domain:** learning

**Origin:** neuromodulation

**Mathematical Form:**
```latex
\alpha_t = \alpha_0 \cdot (1 + m_{dopamine})
```

**Implementation:**
```python
alpha = alpha_0 * (1 + m_dopamine)
```

**Reference:** DOI Nature:317(6036) (1985)

---

### Double Exponential Synapse
**ID:** 24

**Description:** Bi-exponential synaptic conductance with rise and decay

**Domain:** synaptic-transmission

**Origin:** double-exponential

**Mathematical Form:**
```latex
g(t) = g_{max} \frac{\tau_d \tau_r}{\tau_d - \tau_r} \left( \exp\left(-\frac{t}{\tau_d}\right) - \exp\left(-\frac{t}{\tau_r}\right) \right)
```

**Implementation:**
```python
g = g_max * tau_d * tau_r / (tau_d - tau_r) * (np.exp(-t/tau_d) - np.exp(-t/tau_r))
```

---

### Double Exponential Synapse
**ID:** 101

**Description:** Bi-exponential synaptic conductance with rise and decay

**Domain:** synaptic-transmission

**Origin:** double-exponential

**Mathematical Form:**
```latex
g(t) = g_{max} \frac{\tau_d \tau_r}{\tau_d - \tau_r} \left( \exp\left(-\frac{t}{\tau_d}\right) - \exp\left(-\frac{t}{\tau_r}\right) \right)
```

**Implementation:**
```python
g = g_max * tau_d * tau_r / (tau_d - tau_r) * (np.exp(-t/tau_d) - np.exp(-t/tau_r))
```

---

### GABA-A Synaptic Current
**ID:** 21

**Description:** GABA-A receptor-mediated inhibitory synaptic current

**Domain:** synaptic-transmission

**Origin:** GABA-A

**Mathematical Form:**
```latex
I_{GABA_A} = g_{GABA_A} s (V - E_{Cl})
```

**Implementation:**
```python
I_GABA_A = g_GABA_A * s * (V - E_Cl)
```

---

### GABA-A Synaptic Current
**ID:** 98

**Description:** GABA-A receptor-mediated inhibitory synaptic current

**Domain:** synaptic-transmission

**Origin:** GABA-A

**Mathematical Form:**
```latex
I_{GABA_A} = g_{GABA_A} s (V - E_{Cl})
```

**Implementation:**
```python
I_GABA_A = g_GABA_A * s * (V - E_Cl)
```

---

### GABA-B Synaptic Current
**ID:** 22

**Description:** GABA-B receptor current via G-protein activation

**Domain:** synaptic-transmission

**Origin:** GABA-B

**Mathematical Form:**
```latex
I_{GABA_B} = g_{GABA_B} \frac{[G]^n}{[G]^n + K_d} (V - E_K)
```

**Implementation:**
```python
I_GABA_B = g_GABA_B * (G**n / (G**n + Kd)) * (V - E_K)
```

---

### GABA-B Synaptic Current
**ID:** 99

**Description:** GABA-B receptor current via G-protein activation

**Domain:** synaptic-transmission

**Origin:** GABA-B

**Mathematical Form:**
```latex
I_{GABA_B} = g_{GABA_B} \frac{[G]^n}{[G]^n + K_d} (V - E_K)
```

**Implementation:**
```python
I_GABA_B = g_GABA_B * (G**n / (G**n + Kd)) * (V - E_K)
```

---

### NMDA Magnesium Block
**ID:** 20

**Description:** Voltage-dependent magnesium block of NMDA receptors

**Domain:** synaptic-transmission

**Origin:** NMDA

**Mathematical Form:**
```latex
B(V) = \frac{1}{1 + \frac{[Mg^{2+}]}{3.57} \exp(-0.062 V)}
```

**Implementation:**
```python
B = 1 / (1 + (Mg / 3.57) * np.exp(-0.062 * V))
```

---

### NMDA Magnesium Block
**ID:** 97

**Description:** Voltage-dependent magnesium block of NMDA receptors

**Domain:** synaptic-transmission

**Origin:** NMDA

**Mathematical Form:**
```latex
B(V) = \frac{1}{1 + \frac{[Mg^{2+}]}{3.57} \exp(-0.062 V)}
```

**Implementation:**
```python
B = 1 / (1 + (Mg / 3.57) * np.exp(-0.062 * V))
```

---

### NMDA Synaptic Current
**ID:** 19

**Description:** NMDA receptor current with voltage-dependent Mg2+ block

**Domain:** synaptic-transmission

**Origin:** NMDA

**Mathematical Form:**
```latex
I_{NMDA} = g_{NMDA} s B(V) (V - E_{NMDA})
```

**Implementation:**
```python
I_NMDA = g_NMDA * s * B(V) * (V - E_NMDA)
```

---

### NMDA Synaptic Current
**ID:** 96

**Description:** NMDA receptor current with voltage-dependent Mg2+ block

**Domain:** synaptic-transmission

**Origin:** NMDA

**Mathematical Form:**
```latex
I_{NMDA} = g_{NMDA} s B(V) (V - E_{NMDA})
```

**Implementation:**
```python
I_NMDA = g_NMDA * s * B(V) * (V - E_NMDA)
```

---

### Neuromodulatory Mode Dynamics
**ID:** 270

**Description:** RNN governing transitions between neuromodulatory modes

**Domain:** network-dynamics

**Origin:** neuromodulation

**Mathematical Form:**
```latex
\mathbf{m}_{t+1} = \mathrm{RNN}(\mathbf{m}_t, observations_t, internal\_state_t)
```

**Implementation:**
```python
m_next = mode_rnn(m, obs, internal_state)
```

**Reference:** DOI Nature:317(6036) (1985)

---

### Neuromodulatory Mode Vector
**ID:** 269

**Description:** Global state vector controlling brain-wide parameters

**Domain:** network-dynamics

**Origin:** neuromodulation

**Mathematical Form:**
```latex
\mathbf{m}_t = [m_{dopamine}, m_{serotonin}, m_{norepinephrine}, m_{acetylcholine}]
```

**Implementation:**
```python
m = [m_dopamine, m_serotonin, m_norepinephrine, m_acetylcholine]
```

**Reference:** DOI Nature:317(6036) (1985)

---

### Norepinephrine-Modulated Dropout
**ID:** 273

**Description:** Noise/exploration controlled by norepinephrine (arousal)

**Domain:** network-dynamics

**Origin:** neuromodulation

**Mathematical Form:**
```latex
p_{drop}(t) = p_0 + m_{norepinephrine} \cdot 0.3
```

**Implementation:**
```python
p_drop = p_0 + m_norepinephrine * 0.3
```

**Reference:** DOI Nature:317(6036) (1985)

---

### Serotonin-Modulated Memory Consolidation
**ID:** 274

**Description:** Strength of memory replay controlled by serotonin (calmness)

**Domain:** memory

**Origin:** neuromodulation

**Mathematical Form:**
```latex
replay\_weight_t = m_{serotonin}
```

**Implementation:**
```python
replay_weight = m_serotonin
```

**Reference:** DOI Nature:317(6036) (1985)

---


## Systems Biology

### Cerebellar Error Signal
**ID:** 257

**Description:** Error between actual and desired outcome

**Domain:** computational-neuroscience

**Origin:** cerebellum-model

**Mathematical Form:**
```latex
e_{predicted} = ||y_{actual} - y_{desired}||
```

**Implementation:**
```python
error = norm(y_actual - y_desired)
```

**Reference:** DOI Neuron:7(4) (1991)

---

### Cerebellar Fast Learning
**ID:** 259

**Description:** One-trial learning with high learning rate

**Domain:** synaptic-plasticity

**Origin:** cerebellum-learning

**Mathematical Form:**
```latex
W(t+1) = W(t) - \alpha \cdot e_t \cdot x_t^T, \quad \alpha >> 0.01
```

**Implementation:**
```python
W += high_alpha * error * x.T  # typically high_alpha=0.1-1.0
```

**Reference:** DOI Neuron:7(4) (1991)

---

### Cerebellar Prediction
**ID:** 256

**Description:** Fast prediction of outcome quality from proposed action

**Domain:** computational-neuroscience

**Origin:** cerebellum-model

**Mathematical Form:**
```latex
\hat{y}_t = f_{cerebellum}(x_t, a_t)
```

**Implementation:**
```python
y_pred = f_cerebellum(x, a)
```

**Reference:** DOI Neuron:7(4) (1991)

---

### Circadian PER Protein
**ID:** 71

**Description:** Circadian clock PER protein dynamics

**Domain:** circadian

**Origin:** circadian

**Mathematical Form:**
```latex
\frac{d[PER]}{dt} = v_s \frac{K_I^n}{K_I^n + [CN]^n} - v_m \frac{[PER]}{K_m + [PER]} - k_d [PER]
```

---

### Circadian PER Protein
**ID:** 148

**Description:** Circadian clock PER protein dynamics

**Domain:** circadian

**Origin:** circadian

**Mathematical Form:**
```latex
\frac{d[PER]}{dt} = v_s \frac{K_I^n}{K_I^n + [CN]^n} - v_m \frac{[PER]}{K_m + [PER]} - k_d [PER]
```

---

### Fick's Law of Diffusion
**ID:** 75

**Description:** Concentration changes due to diffusion

**Domain:** diffusion

**Origin:** fick

**Mathematical Form:**
```latex
\frac{\partial C}{\partial t} = D \nabla^2 C
```

**Implementation:**
```python
dC_dt = D * laplacian(C)
```

---

### Fick's Law of Diffusion
**ID:** 152

**Description:** Concentration changes due to diffusion

**Domain:** diffusion

**Origin:** fick

**Mathematical Form:**
```latex
\frac{\partial C}{\partial t} = D \nabla^2 C
```

**Implementation:**
```python
dC_dt = D * laplacian(C)
```

---

### Goodwin Oscillator (mRNA)
**ID:** 69

**Description:** Goodwin negative feedback oscillator - mRNA

**Domain:** circadian

**Origin:** goodwin

**Mathematical Form:**
```latex
\frac{dM}{dt} = \frac{v_1 K_1^n}{K_1^n + P_n^n} - v_2 \frac{M}{K_2 + M}
```

**Implementation:**
```python
dM_dt = v1 * K1**n / (K1**n + Pn**n) - v2 * M / (K2 + M)
```

**Reference:** DOI 10.1016/0065-2571(65)90067-1 (1965)

---

### Goodwin Oscillator (mRNA)
**ID:** 146

**Description:** Goodwin negative feedback oscillator - mRNA

**Domain:** circadian

**Origin:** goodwin

**Mathematical Form:**
```latex
\frac{dM}{dt} = \frac{v_1 K_1^n}{K_1^n + P_n^n} - v_2 \frac{M}{K_2 + M}
```

**Implementation:**
```python
dM_dt = v1 * K1**n / (K1**n + Pn**n) - v2 * M / (K2 + M)
```

**Reference:** DOI 10.1016/0065-2571(65)90067-1 (1965)

---

### Reaction-Diffusion Equation
**ID:** 76

**Description:** Diffusion with local reaction dynamics

**Domain:** pattern-formation

**Origin:** reaction-diffusion

**Mathematical Form:**
```latex
\frac{\partial u}{\partial t} = D \nabla^2 u + f(u)
```

---

### Reaction-Diffusion Equation
**ID:** 153

**Description:** Diffusion with local reaction dynamics

**Domain:** pattern-formation

**Origin:** reaction-diffusion

**Mathematical Form:**
```latex
\frac{\partial u}{\partial t} = D \nabla^2 u + f(u)
```

---

### Suggested Correction
**ID:** 258

**Description:** Minimal correction to action based on error gradient

**Domain:** computational-neuroscience

**Origin:** cerebellum-model

**Mathematical Form:**
```latex
\Delta a = -\eta \nabla_a e_{predicted}
```

**Implementation:**
```python
delta_a = -eta * grad(error, a)
```

**Reference:** DOI Neuron:7(4) (1991)

---

### Turing Activator
**ID:** 77

**Description:** Activator in Turing pattern formation

**Domain:** pattern-formation

**Origin:** turing

**Mathematical Form:**
```latex
\frac{\partial a}{\partial t} = D_a \nabla^2 a + \rho_a \frac{a^2}{h} - \mu_a a + \rho_0
```

---

### Turing Activator
**ID:** 154

**Description:** Activator in Turing pattern formation

**Domain:** pattern-formation

**Origin:** turing

**Mathematical Form:**
```latex
\frac{\partial a}{\partial t} = D_a \nabla^2 a + \rho_a \frac{a^2}{h} - \mu_a a + \rho_0
```

---

### Van der Pol Oscillator
**ID:** 70

**Description:** Classic relaxation oscillator

**Domain:** oscillators

**Origin:** van-der-pol

**Mathematical Form:**
```latex
\frac{d^2x}{dt^2} - \mu(1-x^2)\frac{dx}{dt} + x = 0
```

---

### Van der Pol Oscillator
**ID:** 147

**Description:** Classic relaxation oscillator

**Domain:** oscillators

**Origin:** van-der-pol

**Mathematical Form:**
```latex
\frac{d^2x}{dt^2} - \mu(1-x^2)\frac{dx}{dt} + x = 0
```

---


## Working Memory & Decision

### Actor-Critic TD Error
**ID:** 205

**Description:** Temporal difference error for actor-critic

**Domain:** reinforcement-learning

**Mathematical Form:**
```latex
\delta = r + \gamma V(s') - V(s)
```

**Implementation:**
```python
delta = r + gamma * V[s_next] - V[s]
```

---

### Bayesian Confidence
**ID:** 208

**Description:** Confidence from posterior probability

**Domain:** decision-making

**Mathematical Form:**
```latex
confidence \propto P(hypothesis|data)
```

---

### Drift-Diffusion Model
**ID:** 201

**Description:** Decision variable accumulation with noise

**Domain:** decision-making

**Mathematical Form:**
```latex
\frac{dx}{dt} = \mu I + \sigma \xi(t)
```

**Implementation:**
```python
dx_dt = mu * I + sigma * noise
```

---

### Q-Learning
**ID:** 203

**Description:** Value-based reinforcement learning

**Domain:** reinforcement-learning

**Mathematical Form:**
```latex
Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma \max_a' Q(s',a') - Q(s,a)]
```

**Implementation:**
```python
Q[s,a] = Q[s,a] + alpha * (r + gamma * max(Q[s_next]) - Q[s,a])
```

---

### Race Model (Decision)
**ID:** 202

**Description:** Competing accumulators for decision

**Domain:** decision-making

**Mathematical Form:**
```latex
\frac{dx_i}{dt} = I_i + noise
```

**Implementation:**
```python
dx_dt = I + np.random.normal()
```

---

### SARSA Algorithm
**ID:** 204

**Description:** On-policy temporal difference learning

**Domain:** reinforcement-learning

**Mathematical Form:**
```latex
Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma Q(s',a') - Q(s,a)]
```

**Implementation:**
```python
Q[s,a] = Q[s,a] + alpha * (r + gamma * Q[s_next,a_next] - Q[s,a])
```

---

### Softmax Policy (Boltzmann)
**ID:** 207

**Description:** Stochastic action selection from Q-values

**Domain:** reinforcement-learning

**Mathematical Form:**
```latex
P(a|s) = \frac{\exp(Q(s,a)/\tau)}{\sum_a' \exp(Q(s,a')/\tau)}
```

**Implementation:**
```python
p = np.exp(Q / tau) / np.sum(np.exp(Q / tau))
```

---

### Value Function
**ID:** 206

**Description:** Expected discounted future reward

**Domain:** reinforcement-learning

**Mathematical Form:**
```latex
V(s) = E[\sum \gamma^t r_t | s_0 = s]
```

---

### Working Memory Gating
**ID:** 200

**Description:** Gate for updating working memory

**Domain:** working-memory

**Mathematical Form:**
```latex
x_{new} = g x_{input} + (1-g) x_{old}
```

**Implementation:**
```python
x_new = g * x_in + (1 - g) * x_old
```

---

### Working Memory Maintenance
**ID:** 199

**Description:** Persistent activity for working memory

**Domain:** working-memory

**Mathematical Form:**
```latex
\tau \frac{dx}{dt} = -x + f(W x + I_{input})
```

**Implementation:**
```python
dx_dt = (-x + f(W @ x + I)) / tau
```

---

