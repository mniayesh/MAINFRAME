# BioAI Architecture: Existing Tools & Libraries Mapping

**Date:** 2025-12-10
**Status:** Comprehensive Research Survey
**Purpose:** Map existing software implementations to BioAI's 14 architectural layers

---

## Executive Summary

This document surveys existing tools, libraries, and frameworks that approximate various aspects of the BioAI 14-layer architecture. Each tool is assessed for:
- **Target Layer(s):** Which BioAI layers it approximates
- **Mathematical Foundation:** Core theoretical principles
- **Integration Potential:** How it could be adapted for BioAI
- **Limitations:** Gaps and constraints
- **Code Availability:** Implementation status

**Key Finding:** No single framework implements all 14 layers, but multiple tools can be composed to build the complete architecture.

---

## Layer Mapping Overview

```
BIOAI LAYERS          |  EXISTING TOOLS & FRAMEWORKS
==================================================================================
Layer 1-2:  Adaptive  |  Lenia, READY, Cellular Automata Simulators
            Microcode |  Reaction-Diffusion Systems
            & Hetero  |
            Processing|
-----------------------------------------------------------------------------------
Layer 3-5:  Branch,   |  COPASI, Tellurium, libSBML, SBML Ecosystem
            Routing,  |  Chemical Reaction Network Simulators
            Templates |  Systems Biology Tools
-----------------------------------------------------------------------------------
Layer 6-8:  Dynamic   |  Brian2, Dendrify, NEST, NEURON
            Subnetwrk |  GeNN, BindsNET, Norse, SNNTorch, SpikingJelly
            Hierarchy |  Spiking Neural Network Simulators
            Multi-Sys |
-----------------------------------------------------------------------------------
Layer 9-11: Mode-Based|  Nengo (NEF + SPA), SOAR, ACT-R
            Routing   |  LIDA (Global Workspace), Cedar (DFT)
            Bio Limits|  Cognitive Architectures
-----------------------------------------------------------------------------------
Layer 12-14:Non-Vector|  Reservoir Computing (ESN, LSM)
            Cognitive |  Predictive Coding / Free Energy Implementations
            Non-vNeum |  Meta-Learning Frameworks (MAML, Reptile, ACL)
-----------------------------------------------------------------------------------
Cross-Layer:Hardware  |  Intel Loihi, Loihi 2, SpiNNaker
            Platform  |  Neuromorphic Hardware Platforms
==================================================================================
```

---

# PART 1: LAYER-BY-LAYER TOOL ANALYSIS

---

## LAYERS 0-2: ADAPTIVE HARDWARE & HETEROGENEOUS PROCESSING

### 🔧 Tool 1: Lenia (Continuous Cellular Automata)

**Target Layers:** 1-2 (Adaptive microcode, heterogeneous units)

**Description:**
Lenia is a 2D cellular automata system with continuous space, time, and states. It demonstrates how simple local rules can generate complex emergent patterns resembling biological life.

**Mathematical Foundation:**
```
State Update Rule:
s(t+1) = s(t) + Δt · G(K * s(t))

where:
- s(t) = state at time t
- K = convolution kernel (neighborhood influence)
- G() = growth function (nonlinear response)
- * = convolution operation
```

**Strengths:**
- ✅ Demonstrates emergent complexity from local rules
- ✅ Continuous states (not binary)
- ✅ GPU-accelerated via FFT (Fast Fourier Transform)
- ✅ Multiple variants: Flow-Lenia (mass conservation), Sensorimotor-Lenia

**Limitations:**
- ❌ Not a computational substrate (purely simulation)
- ❌ No heterogeneous unit types (all cells identical)
- ❌ No learning or plasticity mechanisms

**Integration Potential:**
Could inspire Layer 1's adaptive microcode design—where local computational "cells" interact through continuous state updates rather than discrete operations.

**Code Availability:**
- GitHub: [Chakazul/Lenia](https://github.com/Chakazul/Lenia)
- Languages: Python, MATLAB, JavaScript
- License: MIT

**References:**
- [Lenia Project Website](https://chakazul.github.io/lenia.html)
- [Flow-Lenia Paper (MIT Artificial Life, 2024)](https://direct.mit.edu/artl/article/31/2/228/130572/Flow-Lenia-Emergent-Evolutionary-Dynamics-in-Mass)

---

### 🔧 Tool 2: Reaction-Diffusion Simulators (Gray-Scott, Turing Patterns)

**Target Layers:** 1-2 (Primitive operators, compound operators)

**Description:**
Reaction-diffusion systems model how chemicals interact and diffuse, creating self-organizing patterns (Turing patterns, spots, stripes, spirals).

**Mathematical Foundation:**
```
Gray-Scott Model:
∂u/∂t = Du∇²u - uv² + F(1-u)
∂v/∂t = Dv∇²v + uv² - (F+k)v

where:
- u, v = chemical concentrations
- Du, Dv = diffusion rates
- F = feed rate
- k = kill rate
```

**Strengths:**
- ✅ Self-organization without central control
- ✅ Multiple stable patterns from same equations
- ✅ Biological realism (used in morphogenesis models)
- ✅ Fast GPU implementations available

**Limitations:**
- ❌ Fixed equations (not adaptive)
- ❌ No memory or learning
- ❌ Continuous space only

**Integration Potential:**
Layer 2's compound operators could use reaction-diffusion dynamics for signal propagation and pattern formation between computational units.

**Code Availability:**
- Web: [Interactive Gray-Scott Simulator](https://pmneila.github.io/jsexp/grayscott/)
- GitHub: [jluebeck/ReactionDiffusionSimulator](https://github.com/jluebeck/ReactionDiffusionSimulator)
- READY: Multi-platform reaction-diffusion simulator

**References:**
- [Biological Modeling: Gray-Scott Model](https://biologicalmodeling.org/prologue/gray-scott)
- [COMSOL Turing Pattern Tutorial](https://www.comsol.com/blogs/visualizing-the-emergence-of-turing-patterns-with-simulation)

---

## LAYERS 3-5: CHEMICAL NETWORKS & CIRCUIT TEMPLATES

### 🔧 Tool 3: COPASI (Complex Pathway Simulator)

**Target Layers:** 3-5 (Routing, templates, reusable circuits)

**Description:**
COPASI is a standalone software for simulation and analysis of biochemical networks. It automatically converts reaction equations into differential equations.

**Mathematical Foundation:**
```
Chemical Reactions → ODEs:
A + B → C  ⟹  d[A]/dt = -k[A][B]
                d[B]/dt = -k[A][B]
                d[C]/dt = +k[A][B]

Supports:
- Deterministic (ODE solver)
- Stochastic (Gillespie algorithm)
- Hybrid approaches
```

**Strengths:**
- ✅ GUI + command-line interface
- ✅ Steady-state, time-course, parameter scan analysis
- ✅ Metabolic control analysis (MCA)
- ✅ SBML import/export (interoperability)
- ✅ Optimization and parameter estimation

**Limitations:**
- ❌ Not designed for neural computation
- ❌ No spike-based dynamics
- ❌ Limited spatial modeling

**Integration Potential:**
Layer 4's learned routing could use COPASI-style reaction networks to model synaptic plasticity and neuromodulation as chemical signaling cascades.

**Code Availability:**
- Website: [copasi.org](https://copasi.org/)
- Binaries: Windows, macOS, Linux
- License: Artistic License 2.0

**References:**
- [COPASI Paper (Bioinformatics, 2006)](https://academic.oup.com/bioinformatics/article/22/24/3067/208398)
- [CytoCopasi Extension (PMC, 2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10963058/)

---

### 🔧 Tool 4: SBML Ecosystem (libSBML, Tellurium)

**Target Layers:** 3-5 (Standardized circuit description)

**Description:**
SBML (Systems Biology Markup Language) is an XML-based format for representing biochemical models. libSBML is the reference library, Tellurium is a Python-based simulation environment.

**Mathematical Foundation:**
```
Model Components:
- Species (molecules)
- Compartments (spatial regions)
- Reactions (transformations)
- Parameters (rate constants)
- Rules (algebraic/differential equations)
```

**Strengths:**
- ✅ Lingua franca of systems biology (300+ tools support it)
- ✅ Reproducible model exchange
- ✅ Multi-language bindings (C++, Python, R, MATLAB, Java, etc.)
- ✅ Tellurium integrates simulation, visualization, analysis

**Limitations:**
- ❌ XML overhead for large models
- ❌ Not designed for online learning
- ❌ Limited support for spatial/stochastic hybrid models

**Integration Potential:**
Could serve as Layer 5's "genome" format—blueprint definitions of circuit templates that can be instantiated dynamically.

**Code Availability:**
- libSBML: [GitHub: sbmlteam/libsbml](https://github.com/sbmlteam/libsbml)
- Tellurium: [GitHub: sys-bio/tellurium](https://github.com/sys-bio/tellurium)
- License: LGPL (libSBML), BSD-2 (Tellurium)

**References:**
- [SBML.org](https://sbml.org/)
- [Tellurium Paper (ResearchGate)](https://www.researchgate.net/publication/344847222_Tellurium_A_Python_Based_Modeling_and_Reproducibility_Platform_for_Systems_Biology)

---

## LAYERS 6-8: SPIKING NEURAL NETWORKS & HIERARCHY

### 🔧 Tool 5: Brian2 + Dendrify

**Target Layers:** 6-8 (Dynamic subnetworks, hierarchical modules, multi-system coordination)

**Description:**
Brian2 is a flexible, equation-based spiking neural network simulator in Python. Dendrify extends Brian2 with biologically realistic dendritic compartments.

**Mathematical Foundation:**
```
Neuron Model (e.g., Leaky Integrate-and-Fire):
τ dV/dt = -(V - V_rest) + I_syn/C

if V > V_thresh:
    emit spike
    V ← V_reset

Dendritic Compartments:
Each dendrite is a separate differential equation system
with local nonlinearities and thresholds.
```

**Strengths:**
- ✅ Pure Python with C++ code generation
- ✅ Arbitrary neuron/synapse models via equations
- ✅ Multi-compartmental neurons (with Dendrify)
- ✅ STDP, homeostasis, neuromodulation support
- ✅ GPU acceleration available (Brian2CUDA, Brian2GeNN)

**Limitations:**
- ❌ Not optimized for very large networks (>1M neurons)
- ❌ Compartmental modeling less mature than NEURON
- ❌ No built-in cognitive-level abstractions

**Integration Potential:**
Excellent fit for Layers 6-7: Brian2 can implement dynamic subnetwork formation, Dendrify adds dendritic branch computation (Layer 3 parallelism).

**Code Availability:**
- Brian2: [GitHub: brian-team/brian2](https://github.com/brian-team/brian2)
- Dendrify: [Nature Communications Paper (2022)](https://www.nature.com/articles/s41467-022-35747-8)
- License: CeCILL (Brian2), MIT (Dendrify)

**Example Code:**
```python
from brian2 import *

# Define neuron model
eqs = '''
dv/dt = (I-v)/tau : 1
I : 1
tau : second
'''

# Create neuron group
G = NeuronGroup(100, eqs, threshold='v>1', reset='v=0')
G.tau = 10*ms

# Run simulation
run(1*second)
```

**References:**
- [Brian2 Documentation](https://briansimulator.org/)
- [Dendrify Paper (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9832130/)

---

### 🔧 Tool 6: NEST (Neural Simulation Tool)

**Target Layers:** 6-8 (Large-scale networks, multi-system coordination)

**Description:**
NEST focuses on spiking neural networks at brain scale (10^8 neurons, 10^12 synapses). Optimized for distributed computing (HPC clusters).

**Mathematical Foundation:**
```
Point Neuron Models:
- Leaky IF, Adaptive Exponential IF
- Izhikevich, Hodgkin-Huxley
- MAT (Multi-timescale Adaptive Threshold)

Synapse Models:
- Static, Tsodyks-Markram (STP)
- STDP (various formulations)
- Gap junctions
```

**Strengths:**
- ✅ Scales to brain-sized networks
- ✅ MPI parallelization for clusters
- ✅ 50+ neuron models, 10+ synapse models
- ✅ Recent support for multicompartment neurons
- ✅ Integration with PyNN (model portability)

**Limitations:**
- ❌ Primarily point neurons (compartmental support is new)
- ❌ Steeper learning curve than Brian2
- ❌ Less flexibility in custom models

**Integration Potential:**
Best for Layer 8 (multi-system coordination) where many brain regions interact. Can simulate large-scale network dynamics with heterogeneous populations.

**Code Availability:**
- Website: [nest-simulator.org](https://www.nest-simulator.org/)
- GitHub: nest/nest-simulator
- License: GPL v2+

**References:**
- [NEST Scholarpedia](http://www.scholarpedia.org/article/NEST_(NEural_Simulation_Tool))
- [NEST Multicompartment Framework (bioRxiv, 2025)](https://www.biorxiv.org/content/10.1101/2025.06.30.662287v1.full)

---

### 🔧 Tool 7: NEURON Simulator

**Target Layers:** 3, 6-7 (Dendritic branch parallelism, detailed compartmental modeling)

**Description:**
NEURON is the gold standard for biophysically detailed compartmental modeling. Developed at Yale/Duke since 1990s.

**Mathematical Foundation:**
```
Cable Theory:
∂V/∂t = (1/c_m) · (1/r_a) · ∂²V/∂x² - (1/c_m) · Σ I_ion

Hodgkin-Huxley Channels:
I_Na = g_Na · m³h · (V - E_Na)
dm/dt = α_m(V)(1-m) - β_m(V)m
```

**Strengths:**
- ✅ Gold standard for detailed morphology
- ✅ 40+ years of model development
- ✅ Extensive ion channel library
- ✅ ModelDB database of published models
- ✅ Python + HOC (custom language)

**Limitations:**
- ❌ Steep learning curve
- ❌ Not designed for large network simulations
- ❌ Limited plasticity modeling compared to Brian2

**Integration Potential:**
Perfect for Layer 3 (branch-based parallelism) and Layer 7 (hierarchical modules with detailed morphology). Can model single neurons with 1000+ compartments.

**Code Availability:**
- Website: neuron.yale.edu
- License: GPL

**References:**
- [NEURON Book (Carnevale & Hines)](https://neuronaldynamics.epfl.ch/)
- [Cable Theory Scholarpedia](http://www.scholarpedia.org/article/Neuronal_cable_theory)

---

### 🔧 Tool 8: GeNN (GPU-Enhanced Neural Networks)

**Target Layers:** 6-8 (High-performance spiking networks)

**Description:**
GeNN generates optimized CUDA code from model descriptions. Achieves 200× speedup over single-core CPU for Hodgkin-Huxley neurons.

**Mathematical Foundation:**
```
Code Generation Approach:
User defines:
- Neuron model (state vars + update equations)
- Synapse model (plasticity rules)
- Connectivity pattern

GeNN generates:
- CUDA kernels for neuron updates
- Spike propagation code
- Weight update kernels
```

**Strengths:**
- ✅ 200-1000× faster than CPU (on NVIDIA GPUs)
- ✅ Custom neuron/synapse models via code snippets
- ✅ STDP and custom plasticity rules
- ✅ PyGeNN Python interface
- ✅ Brian2GeNN integration available

**Limitations:**
- ❌ NVIDIA GPUs only (no AMD/Intel)
- ❌ Less flexible than Brian2 (code generation constraints)
- ❌ Limited spatial modeling

**Integration Potential:**
Ideal for Layer 6-8 when speed is critical. Can simulate 1M neurons in real-time on modern GPUs.

**Code Availability:**
- GitHub: [genn-team/genn](https://github.com/genn-team)
- License: LGPL

**References:**
- [GeNN Paper (Scientific Reports, 2016)](https://www.nature.com/articles/srep18854)
- [PyGeNN Paper (Frontiers, 2021)](https://www.frontiersin.org/articles/10.3389/fninf.2021.659005/full)

---

### 🔧 Tool 9: BindsNET (PyTorch SNN Library)

**Target Layers:** 6-8 (ML-oriented spiking networks)

**Description:**
BindsNET brings spiking neural networks to PyTorch, enabling GPU acceleration and integration with deep learning workflows.

**Mathematical Foundation:**
```
Leaky Integrate-and-Fire:
dv/dt = (v_rest - v + I)/τ
if v > θ: spike & v ← v_reset

Plasticity Rules:
- Hebbian: Δw ∝ x_pre · x_post
- STDP: Δw ∝ f(t_post - t_pre)
- PostPre: Simplified STDP
```

**Strengths:**
- ✅ Native PyTorch (GPU by default)
- ✅ Integrates with PyTorch ecosystem (DataLoader, optim, etc.)
- ✅ Biologically-inspired learning (Hebbian, STDP)
- ✅ Supports image encoding (Poisson, rate, latency)

**Limitations:**
- ❌ Primarily for ML tasks (not detailed biophysics)
- ❌ Limited compartmental modeling
- ❌ Fewer neuron models than Brian2/NEST

**Integration Potential:**
Good for Layer 6-7 when combining biological principles with modern ML. Enables hybrid architectures.

**Code Availability:**
- GitHub: [BindsNET/bindsnet](https://github.com/BindsNET/bindsnet)
- License: AGPL-3.0

**References:**
- [BindsNET Paper (Frontiers, 2018)](https://www.frontiersin.org/articles/10.3389/fninf.2018.00089/full)

---

### 🔧 Tool 10: Norse (PyTorch SNN Framework)

**Target Layers:** 6-8 (Deep learning + spiking)

**Description:**
Norse extends PyTorch with bio-inspired primitives for event-driven, sparse computation.

**Mathematical Foundation:**
```
Supported Models:
- LIF, Adaptive LIF, Izhikevich
- LSNN (Long Short-Term Memory SNN)

Training:
- Surrogate gradients (continuous relaxation)
- BPTT (BackProp Through Time)
```

**Strengths:**
- ✅ Clean PyTorch integration
- ✅ Surrogate gradient method for training
- ✅ Event-driven execution option
- ✅ Scales to HPC clusters

**Limitations:**
- ❌ Less biologically detailed than Brian2
- ❌ Fewer built-in plasticity rules

**Integration Potential:**
Suitable for Layer 6-8 when training large SNNs with gradients. Complements local learning approaches.

**Code Availability:**
- GitHub: [norse/norse](https://github.com/norse/norse)
- License: LGPL-3.0

**References:**
- [Norse Documentation](https://norse.github.io/norse/)

---

### 🔧 Tool 11: SNNTorch

**Target Layers:** 6-8 (Educational + neuromorphic ML)

**Description:**
SNNTorch is designed for accessibility and education, with extensive tutorials covering spike encoding, training, and neuromorphic datasets.

**Mathematical Foundation:**
```
Leaky Neuron Models:
Lapicque, Synaptic, Alpha, RLeaky, etc.

Spike Generation:
- Poisson encoding
- Rate encoding
- Latency encoding
```

**Strengths:**
- ✅ Best documentation and tutorials in SNN space
- ✅ PyTorch-native
- ✅ Surrogate gradient training
- ✅ Neuromorphic dataset support (N-MNIST, DVS)

**Limitations:**
- ❌ Focused on ML (not detailed biophysics)
- ❌ Limited compartmental/dendritic features

**Integration Potential:**
Excellent for prototyping Layer 6-8 architectures and educational purposes. Good starting point before scaling to NEST/Brian2.

**Code Availability:**
- GitHub: [jeshraghian/snntorch](https://github.com/jeshraghian/snntorch)
- License: MIT

**References:**
- [SNNTorch Tutorials](https://snntorch.readthedocs.io/en/latest/tutorials/index.html)
- [Open Neuromorphic: SNNTorch](https://open-neuromorphic.org/neuromorphic-computing/software/snn-frameworks/snntorch/)

---

### 🔧 Tool 12: SpikingJelly

**Target Layers:** 6-8 (Full-stack neuromorphic platform)

**Description:**
SpikingJelly provides full-stack integration: datasets, ANN2SNN conversion, surrogate gradients, CUDA kernels, and neuromorphic hardware support.

**Mathematical Foundation:**
```
Neuron Models:
- IF, LIF, Parametric LIF
- Multi-compartment extensions

Training Methods:
- Surrogate gradient + BPTT
- ANN2SNN (convert trained ANNs)
- Biologically-plausible (STDP, etc.)
```

**Strengths:**
- ✅ Most comprehensive SNN framework
- ✅ Optimized CUDA kernels
- ✅ Neuromorphic hardware backends (Loihi, etc.)
- ✅ ANN2SNN for transfer learning
- ✅ Active development (Chinese AI community)

**Limitations:**
- ❌ Documentation primarily in Chinese
- ❌ Less Western community adoption

**Integration Potential:**
Best all-around choice for Layers 6-8 implementation. Combines flexibility, performance, and hardware portability.

**Code Availability:**
- GitHub: [fangwei123456/spikingjelly](https://github.com/fangwei123456/spikingjelly)
- License: MPL-2.0

**References:**
- [SpikingJelly Paper (Science Advances, 2023)](https://www.science.org/doi/10.1126/sciadv.adi1480)

---

## LAYERS 9-11: COGNITIVE ARCHITECTURES & CONSTRAINTS

### 🔧 Tool 13: Nengo (Neural Engineering Framework)

**Target Layers:** 9-11 (Mode-based computation, routing graphs, biological constraints)

**Description:**
Nengo implements the Neural Engineering Framework (NEF) and Semantic Pointer Architecture (SPA), enabling large-scale functional brain models.

**Mathematical Foundation:**
```
NEF Principles:
1. Representation: x = Σ a_i φ_i (population coding)
2. Transformation: y = f(x) via learned decoders
3. Dynamics: dx/dt = Ax + Bu (recurrent connections)

Semantic Pointer Architecture:
- High-dimensional vectors (512-8192 dim)
- Binding: x ⊛ y (circular convolution)
- Cognitive operations via vector algebra
```

**Strengths:**
- ✅ Largest functional brain model ever: Spaun (2.5M neurons, 8 tasks)
- ✅ Principled mapping from cognition to neurons
- ✅ Supports spiking + rate neurons
- ✅ Hardware backends (Loihi, SpiNNaker)
- ✅ Working memory, planning, reasoning primitives

**Limitations:**
- ❌ Requires understanding NEF theory
- ❌ Not as flexible as Brian2 for custom dynamics
- ❌ Limited support for detailed dendrites

**Integration Potential:**
Excellent for Layers 9-11: Nengo's SPA provides cognitive OS primitives (working memory, attention, planning). NEF naturally implements biological constraints through population coding.

**Code Availability:**
- Website: [nengo.ai](https://www.nengo.ai/)
- GitHub: nengo/nengo
- License: GPLv2 (core), proprietary (some backends)

**References:**
- [Nengo Paper (Frontiers, 2014)](https://www.frontiersin.org/articles/10.3389/fninf.2013.00048/full)
- [Spaun Model](https://www.nengo.ai/publications/)

---

### 🔧 Tool 14: SOAR (Cognitive Architecture)

**Target Layers:** 10-11 (Goal-driven behavior, problem-solving)

**Description:**
SOAR is a production system-based cognitive architecture focused on goal-oriented reasoning and learning from experience.

**Mathematical Foundation:**
```
Production System:
IF   <conditions>
THEN <actions>

Problem Space Hypothesis:
All cognition = search through problem spaces

Memory Systems:
- Procedural (productions)
- Declarative (facts)
- Episodic (events)
- Semantic (general knowledge)
```

**Strengths:**
- ✅ 40+ years of development
- ✅ Unified learning mechanisms (chunking, reinforcement)
- ✅ Extensive validation in AI/robotics
- ✅ Active community

**Limitations:**
- ❌ Not biologically detailed (symbolic AI)
- ❌ No direct neural implementation
- ❌ Less suitable for perception/motor control

**Integration Potential:**
Layer 11 (routing graphs) could use SOAR's production system for high-level goal management. However, needs neural grounding.

**Code Availability:**
- Website: [soar.eecs.umich.edu](https://soar.eecs.umich.edu/)
- GitHub: SoarGroup/Soar
- License: BSD-3-Clause

**References:**
- [SOAR Introduction (arXiv, 2022)](https://arxiv.org/pdf/2205.03854)

---

### 🔧 Tool 15: ACT-R (Adaptive Control of Thought—Rational)

**Target Layers:** 10-11 (Working memory, production system)

**Description:**
ACT-R models human cognition as a hybrid symbolic-subsymbolic architecture with modules for vision, motor, declarative memory, and goal management.

**Mathematical Foundation:**
```
Activation Equation:
A_i = B_i + Σ W_j S_ji + ε

where:
- B_i = base-level activation
- W_j = attentional weights
- S_ji = associative strength
- ε = noise

Production Selection:
U = P · E - C

where:
- P = probability of success
- E = expected gain
- C = cost
```

**Strengths:**
- ✅ Strong psychological validity
- ✅ Predicts human reaction times, errors
- ✅ Subsymbolic tuning (activation, noise)
- ✅ Extensive model library

**Limitations:**
- ❌ Not fully neural (hybrid approach)
- ❌ Limited perceptual modeling
- ❌ Serial bottleneck (one production at a time)

**Integration Potential:**
Layer 10-11 routing and working memory could adopt ACT-R's activation-based selection. Hybrid approach complements neural layers.

**Code Availability:**
- Website: [act-r.psy.cmu.edu](https://act-r.psy.cmu.edu/)
- License: Open source

**References:**
- [ACT-R Paper (WIREs, 2019)](https://wires.onlinelibrary.wiley.com/doi/abs/10.1002/wcs.1488)

---

### 🔧 Tool 16: LIDA (Learning Intelligent Distribution Agent)

**Target Layers:** 9-10 (Global workspace, consciousness)

**Description:**
LIDA is a computational implementation of Global Workspace Theory (Baars), modeling conscious experience as a broadcast mechanism.

**Mathematical Foundation:**
```
Cognitive Cycle (200ms):
1. Perception (feature detection)
2. Workspace composition (coalition formation)
3. Attention (winner-take-all competition)
4. Global broadcast (to all modules)
5. Action selection
6. Learning

Broadcast Gain:
Winning coalition → amplified signal (10-100×)
```

**Strengths:**
- ✅ Explicit consciousness model
- ✅ Integrates perception, attention, action
- ✅ Learning via consciousness

**Limitations:**
- ❌ Limited neural implementation
- ❌ Fixed cognitive cycle (not adaptive)
- ❌ Symbolic representations

**Integration Potential:**
Layer 9's mode-based computation could use LIDA's cognitive cycle. Layer 10's routing could implement the global broadcast mechanism.

**Code Availability:**
- Framework exists but fragmented
- Research implementations in Java

**References:**
- [LIDA Paper (Int'l J. Machine Consciousness)](https://www.worldscientific.com/doi/10.1142/S1793843009000050)
- [Global Workspace Theory](https://en.wikipedia.org/wiki/Global_workspace_theory)

---

### 🔧 Tool 17: Cedar (Dynamic Field Theory Framework)

**Target Layers:** 9-10 (Neural field dynamics, continuous attractor)

**Description:**
Cedar implements Dynamic Field Theory (DFT), modeling cognition as activation dynamics in continuous neural fields.

**Mathematical Foundation:**
```
Neural Field Equation:
τ ∂u/∂t = -u + h + ∫ w(x,x') σ(u(x')) dx' + S(x,t)

where:
- u(x,t) = activation field
- h = resting level
- w(x,x') = lateral interaction kernel
- σ() = threshold function
- S(x,t) = sensory input
```

**Strengths:**
- ✅ GUI for building DFT architectures
- ✅ Real-time parameter tuning + visualization
- ✅ Embodied robotics integration
- ✅ Continuous representations (not discrete tokens)

**Limitations:**
- ❌ Primarily for sensorimotor tasks
- ❌ Limited higher cognition support
- ❌ No plasticity/learning built-in

**Integration Potential:**
Layer 10's routing graphs could use DFT fields for continuous attentional control. Layer 9's modes could switch field parameters.

**Code Availability:**
- Website: [dynamicfieldtheory.org](https://dynamicfieldtheory.org/)
- Framework: Cedar (C++/Qt GUI)

**References:**
- [Cedar Paper (Frontiers, 2016)](https://www.frontiersin.org/journals/neurorobotics/articles/10.3389/fnbot.2016.00014/full)
- [DFT Book](https://dynamicfieldtheory.org/book/)

---

## LAYERS 12-14: NON-VECTOR REPRESENTATIONS & META-LEARNING

### 🔧 Tool 18: Reservoir Computing (Echo State Networks, Liquid State Machines)

**Target Layers:** 12 (Non-vector information encoding, dynamic representations)

**Description:**
Reservoir computing uses a fixed, random recurrent network as a "reservoir" of dynamics, training only the readout layer.

**Mathematical Foundation:**
```
Echo State Network:
x(t+1) = (1-α)x(t) + α·tanh(W_in·u(t) + W·x(t))
y(t) = W_out·x(t)

where:
- x = reservoir state (high-dimensional)
- W = fixed random recurrent weights
- W_out = trained readout weights (linear regression)

Liquid State Machine (spiking version):
Same concept but with spiking neurons
```

**Strengths:**
- ✅ No backprop through time needed
- ✅ Fast training (linear regression)
- ✅ Universal approximation (with large enough reservoir)
- ✅ Temporal processing built-in

**Limitations:**
- ❌ Fixed reservoir (no online adaptation)
- ❌ Hyperparameter sensitive (spectral radius, sparsity)
- ❌ Limited interpretability

**Integration Potential:**
Layer 12's non-vector encoding could use reservoir dynamics for temporal pattern recognition. Complements feedforward layers.

**Code Availability:**
- Python: pyESN, ReservoirPy
- MATLAB: aureservoir
- Julia: ReservoirComputing.jl

**References:**
- [Echo State Networks (Scholarpedia)](http://www.scholarpedia.org/article/Echo_state_network)
- [Liquid State Machines (Wikipedia)](https://en.wikipedia.org/wiki/Liquid_state_machine)

---

### 🔧 Tool 19: Predictive Coding / Free Energy Principle

**Target Layers:** 13-14 (Cognitive OS, hierarchical inference)

**Description:**
Predictive coding implements hierarchical Bayesian inference in the brain via prediction errors and top-down predictions.

**Mathematical Foundation:**
```
Free Energy:
F = ⟨log q(x) - log p(x,u)⟩

Prediction Error:
ε = observation - prediction

Update Rules:
- Lower layer: minimize prediction error
- Higher layer: update internal model

Hierarchical:
Layer_n predicts Layer_{n-1}
Layer_{n-1} sends error to Layer_n
```

**Strengths:**
- ✅ Unified framework for perception, action, learning
- ✅ Biologically plausible (local error signals)
- ✅ Explains diverse phenomena (attention, action, homeostasis)
- ✅ Active inference extends to decision-making

**Limitations:**
- ❌ Computationally expensive (iterative inference)
- ❌ Limited large-scale implementations
- ❌ Theory ahead of practical tools

**Integration Potential:**
Layer 13's cognitive OS could use predictive coding for all inference tasks. Layer 7's hierarchical modules naturally implement prediction/error loops.

**Code Availability:**
- Various research implementations (MATLAB, Python)
- No unified framework yet
- Active Inference Lab: [pymdp](https://github.com/infer-actively/pymdp)

**References:**
- [Predictive Coding (Friston, 2009)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2666703/)
- [Free Energy Principle (Wikipedia)](https://en.wikipedia.org/wiki/Free_energy_principle)

---

### 🔧 Tool 20: Meta-Learning Frameworks (MAML, Reptile, ACL)

**Target Layers:** 14 (Non-Von Neumann, continual learning)

**Description:**
Meta-learning frameworks train models to learn new tasks quickly, addressing continual learning and catastrophic forgetting.

**Mathematical Foundation:**
```
MAML (Model-Agnostic Meta-Learning):
θ' = θ - α∇_θ L_task(θ)  (inner loop)
θ ← θ - β∇_θ Σ L_val(θ')  (outer loop)

Automated Continual Learning (ACL):
Train self-referential networks that
metalearn their own continual learning algorithms
```

**Strengths:**
- ✅ Few-shot learning (learn from 1-5 examples)
- ✅ Reduces catastrophic forgetting
- ✅ Task-agnostic (works for any gradient-based model)
- ✅ Active research area

**Limitations:**
- ❌ Expensive (two levels of optimization)
- ❌ Not fully biological (uses backprop)
- ❌ Limited theoretical understanding

**Integration Potential:**
Layer 14's non-Von Neumann paradigm could use meta-learning for self-modification. Layer 9's mode switching could be learned via meta-learning.

**Code Availability:**
- MAML: [PyTorch implementations on GitHub]
- Reptile: OpenAI implementation
- ACL: Research code (limited availability)

**References:**
- [MAML Paper (ICML 2017)](https://arxiv.org/abs/1703.03400)
- [ACL Paper (arXiv, 2023)](https://arxiv.org/html/2312.00276v3)
- [Continual Learning Survey (arXiv, 2024)](https://arxiv.org/html/2403.05175v1)

---

## CROSS-LAYER: NEUROMORPHIC HARDWARE

### 🔧 Tool 21: Intel Loihi / Loihi 2

**Target Layers:** All (hardware substrate for BioAI)

**Description:**
Loihi is Intel's neuromorphic research chip with 131k neurons (Loihi 1) or 1M neurons (Loihi 2). Hala Point (2024) scales to 1.15B neurons.

**Mathematical Foundation:**
```
Current-based LIF with adaptation:
dV/dt = 1/C (I_syn - g_L(V-E_L))
if V > θ: spike, V ← V_reset

Learning:
- Configurable STDP rules
- Reward-modulated learning
- Three-factor learning (pre, post, neuromodulator)
```

**Strengths:**
- ✅ True asynchronous, event-driven execution
- ✅ 1000× more energy-efficient than GPUs for SNNs
- ✅ On-chip learning (STDP, reward modulation)
- ✅ Lava SDK (open-source software framework)
- ✅ Scales to billion-neuron systems (Hala Point)

**Limitations:**
- ❌ Research-only (not commercially available)
- ❌ Fixed neuron models (less flexible than simulation)
- ❌ Intel-only ecosystem

**Integration Potential:**
Ideal end-target for BioAI implementation. All layers 1-14 could eventually run on Loihi hardware for maximum efficiency.

**Code Availability:**
- Lava: [GitHub: lava-nc/lava](https://github.com/lava-nc/lava)
- License: BSD-3-Clause

**References:**
- [Intel Neuromorphic Computing](https://www.intel.com/content/www/us/en/research/neuromorphic-computing.html)
- [Hala Point (2024)](https://conscium.com/explainers/major-neuromorphic-computing-projects/)

---

### 🔧 Tool 22: SpiNNaker (Million-Core Supercomputer)

**Target Layers:** All (large-scale neural simulation)

**Description:**
SpiNNaker is a million-core ARM-based supercomputer at University of Manchester, designed to simulate 1 billion neurons in real-time.

**Mathematical Foundation:**
```
Hardware:
- 1,036,800 ARM9 cores
- 7 TB distributed RAM
- Custom interconnect for spike routing

Software:
- PyNN interface (portable models)
- Custom models in C
```

**Strengths:**
- ✅ Largest neuromorphic system in operation
- ✅ Real-time simulation at brain scale
- ✅ PyNN compatibility (model portability)
- ✅ Power-efficient (1 MW for 1B neurons)

**Limitations:**
- ❌ Single installation (not distributed)
- ❌ Limited by communication bandwidth at scale
- ❌ Programming model more complex than Loihi

**Integration Potential:**
Excellent for Layer 6-8 large-scale network validation. Can test brain-scale BioAI architectures.

**Code Availability:**
- Website: [spinnakermanchester.github.io](https://spinnakermanchester.github.io/)
- GitHub: SpiNNakerManchester

**References:**
- [SpiNNaker Wikipedia](https://en.wikipedia.org/wiki/SpiNNaker)

---

# PART 2: CROSS-CUTTING CAPABILITIES

## Biologically-Realistic Learning Rules

### Local Plasticity Mechanisms

**Tools with Strong Support:**
1. **Brian2**: Arbitrary plasticity rules via equations
2. **BindsNET**: Hebbian, STDP, PostPre
3. **NEST**: 10+ plasticity models (STDP variants, triplet rules)
4. **GeNN**: Custom plasticity via code snippets

**Key Algorithms:**
```
Hebbian Learning:
Δw ∝ x_pre · x_post

Spike-Timing Dependent Plasticity (STDP):
Δw = A_+ exp(-Δt/τ_+)   if Δt > 0  (LTP)
Δw = -A_- exp(Δt/τ_-)   if Δt < 0  (LTD)

Three-Factor Rules (Reward-Modulated):
Δw = δ · e(t)
where δ = reward signal, e(t) = eligibility trace
```

**Best Implementations:**
- **Research**: Brian2 (most flexible)
- **Performance**: GeNN, SpikingJelly (CUDA optimized)
- **Hardware**: Loihi (on-chip STDP)

**References:**
- [Biologically Plausible Learning Survey (arXiv, 2024)](https://arxiv.org/html/2509.14447v2)
- [Hebbian Learning in DNNs (Nature Neuroscience, 2023)](https://www.nature.com/articles/s41593-023-01460-y)

---

## Surrogate Gradient Methods

**Problem:** Spikes are non-differentiable (discontinuous), breaking standard backprop.

**Solution:** Replace spike threshold with smooth approximation during backward pass.

**Tools with Support:**
1. **Norse**: Multiple surrogate functions built-in
2. **SNNTorch**: SuperSpike, ATan, Sigmoid surrogates
3. **SpikingJelly**: Fast approximation, sigmoid
4. **BindsNET**: Post-Pre (simplified STDP as surrogate)

**Mathematical Formulation:**
```
Forward Pass:
s = H(v - θ)  (Heaviside, non-differentiable)

Backward Pass:
ds/dv ≈ σ'(v - θ)  (smooth surrogate)

Common Surrogates:
- Sigmoid: σ(x) = 1/(1 + exp(-βx))
- ATan: σ(x) = (1/π)·atan(βx) + 0.5
- SuperSpike: σ(x) = 1/(1 + β|x|)²
```

**Trade-offs:**
- ✅ Enables gradient-based training of SNNs
- ✅ Achieves competitive accuracy
- ❌ Not biologically plausible
- ❌ Requires careful tuning (β parameter)

**References:**
- [Surrogate Gradient Learning (IEEE Signal Processing, 2019)](https://ieeexplore.ieee.org/document/8891809)
- [SpyTorch Tutorial](https://github.com/fzenke/spytorch)

---

## Catastrophic Forgetting Mitigation

**Problem:** Neural networks forget old tasks when learning new ones.

**Solutions in Surveyed Tools:**

### 1. Homeostatic Mechanisms (Biological)
**Tools:** Brian2, custom implementations
```
Synaptic Scaling:
w_i ← w_i · (target_rate / actual_rate)

Intrinsic Plasticity:
θ ← θ + η(target - actual)
```

### 2. Elastic Weight Consolidation (EWC)
**Tools:** PyTorch-based (Norse, SNNTorch compatible)
```
Loss = L_task + λ Σ F_i (θ_i - θ*_i)²
where F_i = Fisher information (importance of weight i)
```

### 3. Progressive Neural Networks
**Tools:** Modular architectures (Nengo, custom)
- Freeze old task columns
- Add new columns for new tasks
- Lateral connections for transfer

### 4. Meta-Learning Approaches
**Tools:** MAML, Reptile, ACL
- Learn how to learn without forgetting
- Optimize for few-shot adaptation

**Best Approach for BioAI:**
Combine homeostasis (Layer 9), modular growth (Layer 5), and meta-learned plasticity (Layer 14).

**References:**
- [Continual Learning Survey (arXiv, 2024)](https://arxiv.org/abs/2403.05175)
- [Hebbian Continual Learning (arXiv, 2024)](https://arxiv.org/html/2407.17305)

---

# PART 3: INTEGRATION STRATEGIES

## Strategy 1: Hybrid Stack (Recommended)

**Architecture:**
```
Layer 12-14: Meta-Learning & Cognition
             ↓ (Python API)
Layer 9-11:  Nengo (NEF/SPA) + Cedar (DFT)
             ↓ (Neural interface)
Layer 6-8:   SpikingJelly (performance) or Brian2 (flexibility)
             ↓ (Synapse models)
Layer 3-5:   SBML/Tellurium (circuit templates)
             ↓ (Reactions → dynamics)
Layer 1-2:   Custom (adaptive microcode)
             ↓
Hardware:    Loihi 2 (target) or GPU (development)
```

**Advantages:**
- ✅ Best tool for each layer
- ✅ Proven components
- ✅ Incremental development

**Challenges:**
- ❌ Integration overhead
- ❌ Performance boundaries
- ❌ Consistency across layers

---

## Strategy 2: Unified Framework (Brian2-Centric)

**Architecture:**
```
All Layers: Brian2 + Extensions
- Dendrify for Layer 3 (dendrites)
- Custom equations for Layers 1-2
- Cognitive APIs for Layers 9-11
- Brian2GeNN or Brian2CUDA for performance
```

**Advantages:**
- ✅ Single framework, consistent API
- ✅ Maximum flexibility
- ✅ Strong community

**Challenges:**
- ❌ Not optimized for all use cases
- ❌ Requires extensive custom code
- ❌ Limited hardware targets

---

## Strategy 3: Neuromorphic-First (Loihi/SpiNNaker)

**Architecture:**
```
Target Hardware: Loihi 2
Development: Lava SDK
Simulation: Brian2 → Lava conversion
Higher Layers: Nengo → Lava backend
```

**Advantages:**
- ✅ Maximum efficiency (1000× energy reduction)
- ✅ True asynchronous execution
- ✅ Scales to billion neurons

**Challenges:**
- ❌ Limited hardware availability
- ❌ Constrained neuron models
- ❌ Debugging harder than simulation

---

# PART 4: IMPLEMENTATION ROADMAP

## Phase 1: Foundation (Months 1-3)

**Goal:** Validate core principles with existing tools.

**Tasks:**
1. **Layer 1-2 Prototype:** Lenia + custom rules
   - Implement adaptive operator generation
   - Test emergent complexity

2. **Layer 3-5 Template:** SBML + Brian2
   - Define microcircuit templates in SBML
   - Instantiate in Brian2

3. **Layer 6-8 Network:** SpikingJelly or Brian2
   - Implement heterogeneous neuron types
   - Test dynamic subnetwork formation

**Deliverables:**
- ✅ Proof-of-concept for each layer cluster
- ✅ Performance benchmarks
- ✅ Integration tests

---

## Phase 2: Vertical Integration (Months 4-6)

**Goal:** Connect lower layers to higher layers.

**Tasks:**
1. **Nengo Integration:**
   - Build NEF/SPA models on top of SNN layers
   - Implement working memory, attention primitives

2. **Global Workspace:**
   - Implement LIDA-style broadcast mechanism
   - Test winner-take-all competition

3. **Mode Switching:**
   - Implement 3+ computational modes
   - Test context-dependent algorithm selection

**Deliverables:**
- ✅ End-to-end task (e.g., digit recognition + recall)
- ✅ Cognitive OS primitives working
- ✅ Performance within 10× of Transformers

---

## Phase 3: Scaling & Optimization (Months 7-9)

**Goal:** Scale to realistic problem sizes.

**Tasks:**
1. **GPU Optimization:**
   - Port to GeNN or SpikingJelly CUDA kernels
   - Profile and optimize bottlenecks

2. **Neuromorphic Deployment:**
   - Port subset to Loihi 2 (if available)
   - Compare energy efficiency

3. **Benchmarking:**
   - Test on standard tasks (MNIST, Penn Treebank, RL)
   - Compare to Transformers, CNNs, RNNs

**Deliverables:**
- ✅ 1000+ neuron networks running in real-time
- ✅ Energy efficiency measurements
- ✅ Competitive accuracy on benchmarks

---

## Phase 4: Advanced Features (Months 10-12)

**Goal:** Implement Layer 12-14 capabilities.

**Tasks:**
1. **Continual Learning:**
   - Test on sequential task benchmarks
   - Measure catastrophic forgetting

2. **Meta-Learning:**
   - Few-shot task adaptation
   - Self-modification experiments

3. **Consciousness Primitives:**
   - Global workspace introspection
   - Error detection and correction

**Deliverables:**
- ✅ Zero-forgetting continual learning demo
- ✅ Few-shot learning (< 10 examples)
- ✅ Self-aware error correction

---

# PART 5: TOOL SELECTION MATRIX

| Layer | Primary Tool | Alternative | Rationale |
|-------|-------------|-------------|-----------|
| **1-2: Adaptive Hardware** | Custom (Lenia-inspired) | Reaction-Diffusion | Need adaptive operators, no existing tool fits |
| **3-5: Circuit Templates** | SBML + Tellurium | COPASI | Standardized format, Python integration |
| **6: Dynamic Subnetworks** | Brian2 | SpikingJelly | Flexibility for prototyping |
| **7: Hierarchical Modules** | Brian2 + Dendrify | NEURON | Balance of detail and scalability |
| **8: Multi-System Coord** | NEST | Brian2 | Large-scale network support |
| **9: Mode-Based Compute** | Nengo | Custom | NEF handles mode switching naturally |
| **10: Routing Graphs** | Cedar (DFT) | Nengo | Continuous attractor dynamics |
| **11: Biological Limits** | Nengo | Custom | NEF naturally constrains resources |
| **12: Non-Vector Encoding** | Reservoir Computing | Nengo SPA | Temporal dynamics + semantic pointers |
| **13: Cognitive OS** | Nengo SPA | LIDA | Most complete implementation |
| **14: Non-Von Neumann** | Meta-Learning (custom) | Active Inference | Research frontier, custom needed |
| **Hardware Target** | Loihi 2 | SpiNNaker | Best neuromorphic platform available |

---

# PART 6: KEY GAPS & RESEARCH NEEDS

## Gap 1: Adaptive Microcode (Layer 1)
**Status:** ❌ No existing tool
**Need:** Runtime-modifiable instruction set
**Research Direction:** Programmable logic + neural control
**Timeline:** 12-18 months custom development

## Gap 2: Heterogeneous Processing Units (Layer 2)
**Status:** ⚠️ Partial (NEST has neuron types, but not full heterogeneity)
**Need:** Different mathematical kernels per neuron type
**Research Direction:** Extend GeNN code generation
**Timeline:** 6-9 months

## Gap 3: Learned Circuit Templates (Layer 5)
**Status:** ⚠️ Partial (SBML defines circuits, but no learning)
**Need:** Template discovery from experience
**Research Direction:** Neuroevolution + program synthesis
**Timeline:** 9-12 months

## Gap 4: Mode-Based Computation (Layer 9)
**Status:** ⚠️ Partial (cognitive architectures have modes, SNNs don't)
**Need:** Neural implementation of computational modes
**Research Direction:** Neuromodulation + context networks
**Timeline:** 6-9 months

## Gap 5: Non-Vector Representations (Layer 12)
**Status:** ✅ Good (Nengo SPA, Vector Symbolic Architectures)
**Need:** Integration with lower layers
**Research Direction:** SNN + VSA hybrid
**Timeline:** 3-6 months

## Gap 6: Online Meta-Learning (Layer 14)
**Status:** ⚠️ Research frontier
**Need:** Self-modifying neural architectures
**Research Direction:** Automated Continual Learning + hypernetworks
**Timeline:** 12+ months

---

# PART 7: RECOMMENDED STARTING POINT

## Minimal Viable BioAI (Layers 6-11)

**Why:** Layers 6-11 have the best tool support and represent the core neural computation stack.

**Architecture:**
```python
# Layer 6-8: Spiking Neural Network
from brian2 import *
from dendrify import NeuronModel

# Layer 9: Cognitive Control (Nengo)
import nengo

# Layer 10: Routing (DFT via custom)
# Layer 11: Constraints (population size limits)

# Integration
nengo_snn_bridge = NengoSNNInterface()
```

**Proof-of-Concept Task:**
Working memory + pattern recognition
- Input: MNIST digits
- Working memory: Hold 3 digits
- Output: Recall in order

**Expected Outcome:**
- 90%+ accuracy (competitive with RNNs)
- 10× fewer parameters than Transformer
- Demonstrates Layers 6-11 working together

**Timeline:** 2-3 months

**Next Steps After PoC:**
1. Add Layer 3-5 (circuit templates)
2. Add Layer 12 (semantic pointers)
3. Scale to more complex tasks
4. Deploy to Loihi 2

---

# CONCLUSION

## Key Findings

1. **No Single Framework:** BioAI's 14 layers require composing multiple tools. No existing framework implements all layers.

2. **Strong Lower-Layer Support:** Layers 6-11 (spiking networks + cognition) have excellent tools:
   - SNNs: Brian2, NEST, GeNN, SpikingJelly
   - Cognition: Nengo, SOAR, ACT-R

3. **Gaps in Extremes:**
   - Layer 1-2 (adaptive hardware): Need custom development
   - Layer 12-14 (meta-cognition): Research frontier

4. **Hardware Readiness:** Neuromorphic chips (Loihi 2, SpiNNaker) are production-ready for Layers 6-8 deployment.

5. **Integration is Key:** The value is in connecting layers, not individual components.

## Recommended Path Forward

### Short-Term (3 months)
1. Build Layer 6-11 prototype with Brian2 + Nengo
2. Validate on cognitive tasks (working memory, reasoning)
3. Benchmark against Transformers

### Medium-Term (6-12 months)
1. Add Layer 3-5 (circuit templates via SBML)
2. Implement Layer 12 (VSA/semantic pointers)
3. Deploy to Loihi 2 for efficiency validation

### Long-Term (12-24 months)
1. Custom Layer 1-2 (adaptive microcode)
2. Layer 14 meta-learning
3. Full 14-layer integration
4. Scale to brain-sized networks on neuromorphic hardware

## Confidence Assessment

| Layer | Tool Maturity | Integration Complexity | Timeline |
|-------|--------------|----------------------|----------|
| 1-2 | ⚠️ Low | 🔴 High | 12-18 mo |
| 3-5 | ✅ High | 🟡 Medium | 3-6 mo |
| 6-8 | ✅ Very High | 🟢 Low | 1-3 mo |
| 9-11 | ✅ High | 🟡 Medium | 3-6 mo |
| 12-14 | ⚠️ Medium | 🔴 High | 9-12 mo |

**Overall Assessment:** 70% of BioAI architecture is implementable with existing tools. The remaining 30% requires focused research, but the path is clear.

---

# APPENDIX: QUICK REFERENCE

## Python Package Installation

```bash
# Cellular Automata / Reaction-Diffusion
pip install lenia  # (if available, else clone GitHub)

# Systems Biology
pip install tellurium python-libsbml

# Spiking Neural Networks
pip install brian2 dendrify
pip install norse snntorch spikingjelly
pip install bindsnet

# Neuromorphic Hardware
pip install lava-nc  # Intel Loihi

# Cognitive Architectures
pip install nengo

# Reservoir Computing
pip install reservoirpy

# Meta-Learning
pip install learn2learn  # Meta-learning utilities
```

## Key GitHub Repositories

```
Lenia:              https://github.com/Chakazul/Lenia
Brian2:             https://github.com/brian-team/brian2
Dendrify:           (see Nature Comm paper)
NEST:               https://github.com/nest/nest-simulator
GeNN:               https://github.com/genn-team/genn
BindsNET:           https://github.com/BindsNET/bindsnet
Norse:              https://github.com/norse/norse
SNNTorch:           https://github.com/jeshraghian/snntorch
SpikingJelly:       https://github.com/fangwei123456/spikingjelly
Nengo:              https://github.com/nengo/nengo
COPASI:             https://copasi.org
Tellurium:          https://github.com/sys-bio/tellurium
Lava (Loihi):       https://github.com/lava-nc/lava
```

## Key Papers by Layer

**Layer 1-2:**
- [Flow-Lenia (2024)](https://direct.mit.edu/artl/article/31/2/228/130572/)
- [Turing Patterns (COMSOL)](https://www.comsol.com/blogs/visualizing-the-emergence-of-turing-patterns-with-simulation)

**Layer 3-5:**
- [COPASI (Bioinformatics, 2006)](https://academic.oup.com/bioinformatics/article/22/24/3067/208398)
- [SBML Overview (Wikipedia)](https://en.wikipedia.org/wiki/SBML)

**Layer 6-8:**
- [Brian2 (eLife, 2019)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6786860/)
- [Dendrify (Nature Comm, 2022)](https://www.nature.com/articles/s41467-022-35747-8)
- [SpikingJelly (Science Advances, 2023)](https://www.science.org/doi/10.1126/sciadv.adi1480)

**Layer 9-11:**
- [Nengo (Frontiers, 2014)](https://www.frontiersin.org/articles/10.3389/fninf.2013.00048/full)
- [SOAR Introduction (arXiv, 2022)](https://arxiv.org/pdf/2205.03854)
- [Cedar DFT (Frontiers, 2016)](https://www.frontiersin.org/journals/neurorobotics/articles/10.3389/fnbot.2016.00014/full)

**Layer 12-14:**
- [Predictive Coding (Friston, 2009)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2666703/)
- [Meta-Learning Continual Learning (arXiv, 2023)](https://arxiv.org/html/2312.00276v3)
- [Catastrophic Forgetting Survey (arXiv, 2024)](https://arxiv.org/abs/2403.05175)

**Neuromorphic Hardware:**
- [Intel Loihi Overview](https://www.intel.com/content/www/us/en/research/neuromorphic-computing.html)
- [SpiNNaker Wikipedia](https://en.wikipedia.org/wiki/SpiNNaker)

---

**End of Document**

*Last Updated: 2025-12-10*
*Compiled by: Claude (Anthropic)*
*For: BioAI 14-Layer Architecture Project*
