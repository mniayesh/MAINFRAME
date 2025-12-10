# Complete Brain-Region Implementation Roadmap

**Purpose:** Define the complete system architecture, dependencies, and implementation timeline for building a full biological AI brain from dendrites upward.

**Scope:** Cortex → Hippocampus → Basal Ganglia → Cerebellum → Thalamus → Amygdala → Integration

**Total Timeline:** 12-18 months, 5 phases, ~50,000 lines of code

---

## 🧠 System Architecture Overview

```
                            ╔════════════════════╗
                            ║   THALAMUS ROUTER  ║
                            ║  (attention control)║
                            ╚════════════════════╝
                                      △
                ┌─────────────────────┼─────────────────────┐
                │                     │                     │
                ▼                     ▼                     ▼
        ╔═══════════════╗     ╔═══════════════╗     ╔═══════════════╗
        ║    CORTEX     ║     ║  HIPPOCAMPUS  ║     ║ BASAL GANGLIA ║
        ║ (reasoning)   ║◄────►(memory)       ║◄────►(action)       ║
        ╚═══════════════╝     ╚═══════════════╝     ╚═══════════════╝
                △                     △                     △
                │                     │                     │
        ┌───────┴──────┬──────────────┼──────────────┬──────┴──────┐
        ▼              ▼              ▼              ▼             ▼
   ╔────────╗   ╔─────────╗   ╔──────────╗   ╔──────────╗   ╔──────────╗
   │AMYGDALA│   │CEREBEL  │   │NEUROMOD  │   │Error     │   │Working   │
   │(salience) │   │LUM      │   │(modes)   │   │Correction│   │Memory    │
   ╚────────╝   ╚─────────┘   ╚──────────┘   ╚──────────┘   ╚──────────┘
        △           △              △              △             △
        └───────────┴──────────────┴──────────────┴─────────────┘
                        Foundation: Dendritic Neurons
```

---

## 📋 Phase 0: Foundation (Weeks 1-4)

### Core Libraries & Infrastructure

**Goal:** Build the computational primitives that everything else uses.

#### 0.1 Dendritic Neuron Module
```
Status: DOCUMENTED (DENDRITIC_NEURON_MODULE.md)
Tasks:
  [ ] Implement DendriticNeuron class (5 branch types)
  [ ] Implement DendriticLayer (N neurons with shared plasticity)
  [ ] Unit tests (XOR problem, temporal integration)
  [ ] GPU acceleration (CuPy / PyTorch kernels)

Dependencies: None (foundation)
Deliverable: dendritic_core.py (~500 lines)
```

#### 0.2 Synaptic Plasticity Library
```
Status: DESIGNED
Tasks:
  [ ] Hebbian learning (local correlation)
  [ ] Predictive error learning (cortical)
  [ ] Reward-modulated learning (dopaminergic)
  [ ] STDP (spike-timing dependent plasticity)
  [ ] Eligibility traces (for credit assignment)

Dependencies: DendriticNeuron
Deliverable: plasticity.py (~300 lines)
```

#### 0.3 Microcircuit Templates
```
Status: DESIGNED
Tasks:
  [ ] Attractor pool (recurrent memory)
  [ ] Pattern separator (decorrelation)
  [ ] Winner-take-all (competition)
  [ ] Predictive coding loop (error minimization)
  [ ] Disinhibition gate (conditional routing)

Dependencies: DendriticLayer + Plasticity
Deliverable: microcircuits.py (~800 lines)
```

---

## 📋 Phase 1: Language Comprehension (Weeks 5-12)

### Wernicke Module (Reading & Understanding)

**Goal:** Build a functional language comprehension system.

#### 1.1 Phonological Parsing (pSTG)
```
Status: DOCUMENTED (WERNICKE_COMPREHENSION_MODULE.md)
Architecture:
  - Input: text tokens (one-hot or embeddings)
  - Output: [256,] phoneme-encoded hidden state
  - 256 dendritic neurons, 5 branches each

Tasks:
  [ ] Phoneme feature extraction (voicing, place, manner)
  [ ] Predictive coding layer for phoneme prediction
  [ ] Recurrent state update with error feedback
  [ ] Learning from phoneme prediction errors

Microcircuits used: Predictive-coding loop
Dependencies: Phase 0 (core + plasticity)
Deliverable: pstg_layer.py (~300 lines)
Evaluation: Phoneme recognition task
```

#### 1.2 Lexical Retrieval (MTG)
```
Status: DOCUMENTED
Architecture:
  - Input: [256,] from pSTG
  - Output: [512,] word embedding + semantic features
  - Hopfield-like attractor memory
  - 512 dendritic neurons, gated branches

Tasks:
  [ ] Word embedding layer (learned from corpus)
  [ ] Associative retrieval (softmax attention over vocabulary)
  [ ] Semantic feature integration
  [ ] Competing word candidates via dendritic gating

Microcircuits used: Attractor pool, WTA
Dependencies: 1.1 (pSTG)
Deliverable: mtg_layer.py (~400 lines)
Evaluation: Word sense disambiguation task
```

#### 1.3 Sentence Integration (STS)
```
Status: DOCUMENTED
Architecture:
  - Input: [512,] word meanings across sequence
  - Output: [512,] accumulated sentence context
  - Recurrent predictive-coding layer
  - 512 dendritic neurons, 8 branches each

Tasks:
  [ ] Predict next word's semantic representation
  [ ] Compute prediction errors at token level
  [ ] Maintain context across sentence
  [ ] Learn from sentence-level errors

Microcircuits used: Predictive-coding loop, recurrent attractor
Dependencies: 1.2 (MTG)
Deliverable: sts_layer.py (~300 lines)
Evaluation: Cloze task (predict missing words)
```

#### 1.4 Semantic Composition (Angular Gyrus)
```
Status: DOCUMENTED
Architecture:
  - Input: [512,] × T (sequence of word meanings)
  - Output: [512,] final compositional meaning
  - Cross-attention over sequence with role assignment
  - 512 dendritic neurons, 5 branches (semantic roles)

Tasks:
  [ ] Semantic role assignment (Agent, Patient, Action, Mod, Negation)
  [ ] Cross-attention over word sequence
  [ ] Compositional binding via dendritic integration
  [ ] Learn role assignments from context

Microcircuits used: Attention-based retrieval, role-based WTA
Dependencies: 1.3 (STS)
Deliverable: ag_layer.py (~350 lines)
Evaluation: Semantic role labeling, sentence similarity
```

#### 1.5 Wernicke Integration & Learning
```
Status: DESIGNED
Architecture: Full forward pass from text → meaning

Tasks:
  [ ] Integrate all 4 layers with shared learning
  [ ] Implement online learning curriculum
  [ ] Loss functions for each layer
  [ ] End-to-end gradient flow (local rules, no backprop)

Dependencies: 1.1-1.4
Deliverable: wernicke_module.py (~400 lines)
Evaluation: Language understanding benchmark (SQuAD-like)
```

---

## 📋 Phase 2: Language Production (Weeks 13-20)

### Broca Module (Writing & Speaking)

**Goal:** Complement comprehension with generation capability.

#### 2.1 Semantic → Grammatical Mapping
```
Status: DESIGNED
Architecture:
  - Input: [512,] semantic representation
  - Output: [512,] grammatical structure codes
  - Reverses Wernicke semantic structure
  - 512 dendritic neurons

Tasks:
  [ ] Learn inverse mapping (semantic → grammar)
  [ ] Extract subject/verb/object slots
  [ ] Plan syntactic structure
  [ ] Predict next word given grammar + semantics

Dependencies: Phase 1 (Wernicke)
Deliverable: broca_semantic_layer.py (~300 lines)
Evaluation: Grammaticality judgments
```

#### 2.2 Motor Planning (Articulatory)
```
Status: DESIGNED
Architecture:
  - Input: [512,] grammatical codes
  - Output: [128,] phoneme/motor sequences
  - Cerebellar-like error correction
  - Temporal planning for sequences

Tasks:
  [ ] Convert grammar to phoneme sequences
  [ ] Temporal planning (when to produce each phoneme)
  [ ] Motor error prediction
  [ ] Online correction during generation

Dependencies: 2.1 (semantic mapping)
Deliverable: broca_motor_layer.py (~350 lines)
Evaluation: Grammatical fluency, error rates
```

#### 2.3 Broca Integration
```
Status: DESIGNED
Architecture: Full semantic → text pipeline

Tasks:
  [ ] Integrate semantic input with grammar + motor
  [ ] Interactive learning with comprehension module
  [ ] Feedback from correctness signals

Dependencies: 2.1-2.2
Deliverable: broca_module.py (~300 lines)
Evaluation: Text generation quality
```

---

## 📋 Phase 3: Memory & Learning (Weeks 21-28)

### Hippocampus Module (Episodic Memory & Consolidation)

#### 3.1 Hippocampal Encoding
```
Status: DESIGNED
Architecture:
  - Input: [512,] semantic state from cortex
  - Output: Sparse hippocampal engram
  - Pattern separation via expansion
  - Rapid encoding (1-2 trials)

Tasks:
  [ ] Dense → sparse transformation
  [ ] Pattern separation (orthogonalization)
  [ ] Fast, plastic weights
  [ ] Novelty detection (hippocampal tagging)

Dependencies: Phase 1-2 (Wernicke + Broca)
Deliverable: hippocampus_encode.py (~300 lines)
Evaluation: One-shot memory task
```

#### 3.2 Hippocampal Retrieval
```
Status: DESIGNED
Architecture:
  - Input: [512,] cue (partial memory)
  - Output: [512,] retrieved memory
  - Autoassociative retrieval (Hopfield-like)
  - O(1) lookup time

Tasks:
  [ ] Implement improved Hopfield network
  [ ] Fast retrieval with softmax attention
  [ ] Handle partial/noisy cues
  [ ] Scale to millions of memories

Dependencies: 3.1 (encoding)
Deliverable: hippocampus_retrieve.py (~400 lines)
Evaluation: Memory capacity test
```

#### 3.3 Memory Consolidation
```
Status: DESIGNED
Architecture:
  - Input: Hippocampal memories
  - Output: Integrated cortical knowledge
  - Replay during "sleep"
  - Slow, structured learning

Tasks:
  [ ] Sample hippocampal memories
  [ ] Replay through cortex
  [ ] Integrate new knowledge with old
  [ ] Prevent catastrophic forgetting

Dependencies: 3.1-3.2 + Phase 1 (Wernicke)
Deliverable: hippocampus_consolidation.py (~350 lines)
Evaluation: Continual learning benchmark
```

---

## 📋 Phase 4: Action & Motivation (Weeks 29-36)

### Basal Ganglia Module (Action Selection & RL)

#### 4.1 Value Functions
```
Status: DESIGNED
Architecture:
  - Input: [512,] cortical state
  - Output: Q-values for each action
  - Deep Q-learning with dendritic neurons
  - Temporal difference learning

Tasks:
  [ ] Implement action representation
  [ ] Q-network with dendritic neurons
  [ ] TD error computation
  [ ] Dopamine signal (reward prediction error)

Dependencies: Phase 1-2 (perception)
Deliverable: basal_ganglia_value.py (~400 lines)
Evaluation: RL task (maze, goal-reaching)
```

#### 4.2 Action Selection (Direct/Indirect Pathways)
```
Status: DESIGNED
Architecture:
  - Input: Q-values [num_actions,]
  - Output: Selected action (softmax + sampling)
  - Go pathway (push) vs Stop pathway (inhibit)
  - Exploration-exploitation tradeoff

Tasks:
  [ ] Separate direct (go) and indirect (no-go) pathways
  [ ] Inhibitory competition
  [ ] Temperature-based exploration
  [ ] Learn pathway strengths

Dependencies: 4.1 (value functions)
Deliverable: basal_ganglia_action.py (~300 lines)
Evaluation: Action selection accuracy
```

#### 4.3 Motivation & Reward
```
Status: DESIGNED
Architecture:
  - Input: External reward signal
  - Output: Dopamine modulation (global neuromodulator)
  - Reward prediction + error
  - Goal-directed vs habitual learning

Tasks:
  [ ] Predict future reward
  [ ] Compute dopamine signal
  [ ] Modulate learning rates globally
  [ ] Switch between goal-directed + habitual modes

Dependencies: 4.1-4.2 + Phase 0 (neuromodulation)
Deliverable: basal_ganglia_motivation.py (~350 lines)
Evaluation: Multi-step RL task
```

---

## 📋 Phase 5: Integration & Specialization (Weeks 37-52)

### Thalamus, Cerebellum, Amygdala, & Full System

#### 5.1 Thalamic Router
```
Status: DESIGNED
Architecture:
  - Input: Outputs from all regions
  - Output: Dynamic routing decisions
  - Learned routing policy
  - Bandwidth control

Tasks:
  [ ] Routing network (which region talks to which)
  [ ] Attention gating (how much bandwidth)
  [ ] Mode-dependent routing
  [ ] Oscillatory synchronization

Dependencies: All phases (routes between all modules)
Deliverable: thalamus_router.py (~400 lines)
Evaluation: Information bottleneck test
```

#### 5.2 Cerebellar Learning & Prediction
```
Status: DESIGNED
Architecture:
  - Input: Proposed action + context
  - Output: Error prediction + correction
  - Very fast, lightweight predictor
  - One-trial learning

Tasks:
  [ ] Predict action outcome quality
  [ ] Suggest minimal corrections
  [ ] Extremely high learning rate
  [ ] Integrate feedback within action

Dependencies: Phase 4 (actions)
Deliverable: cerebellum_critic.py (~300 lines)
Evaluation: Online error correction task
```

#### 5.3 Amygdala (Salience & Risk)
```
Status: DESIGNED
Architecture:
  - Input: Any cortical state
  - Output: Salience, risk, novelty scores
  - Modulates all learning rates
  - Tags memories for prioritized consolidation

Tasks:
  [ ] Estimate salience (importance)
  [ ] Estimate risk (threat level)
  [ ] Novelty detection
  [ ] Modulate learning globally
  [ ] Tag memories with priority

Dependencies: All phases (evaluates everything)
Deliverable: amygdala_salience.py (~300 lines)
Evaluation: Attention capture task
```

#### 5.4 Neuromodulation Controller
```
Status: DESIGNED
Architecture:
  - Input: Cortical + limbic activity
  - Output: Global mode vector [dopamine, serotonin, NE, ACh]
  - Controls brain-wide parameters
  - Learns mode transitions

Tasks:
  [ ] Implement mode RNN
  [ ] Map modes → parameter multipliers
  [ ] Learn mode transitions from success
  [ ] Smooth mode switching (no jumps)

Dependencies: All phases (modulates all)
Deliverable: neuromodulation_controller.py (~300 lines)
Evaluation: Behavioral mode task
```

#### 5.5 Full System Integration
```
Status: DESIGNED
Architecture: Complete brain with all regions communicating

Tasks:
  [ ] Unified message-passing protocol
  [ ] Shared loss functions (no global backprop)
  [ ] Curriculum learning (learning order)
  [ ] Multi-region learning synchronization
  [ ] Energy efficiency optimization

Deliverable: brain_system.py (~600 lines)
Evaluation: Complex language + reasoning + RL task
```

---

## 🗺️ Dependency Graph

```
Phase 0 (Foundation)
├─ Dendritic Neurons
├─ Plasticity Rules
└─ Microcircuits
    │
    ▼
Phase 1 (Comprehension)
├─ pSTG (Phonological)
├─ MTG (Lexical)
├─ STS (Sentence)
└─ Angular Gyrus (Semantics)
    │
    ├─→ Phase 2 (Production)
    │   ├─ Broca Semantic
    │   ├─ Broca Motor
    │   └─ Broca Integration
    │
    ├─→ Phase 3 (Memory)
    │   ├─ Hippocampal Encoding
    │   ├─ Hippocampal Retrieval
    │   └─ Consolidation
    │
    └─→ Phase 4 (Action)
        ├─ Value Functions
        ├─ Action Selection
        └─ Motivation/Reward
            │
            ▼
        Phase 5 (Full Integration)
        ├─ Thalamus Router
        ├─ Cerebellum Critic
        ├─ Amygdala (Salience)
        ├─ Neuromodulation
        └─ System Integration
```

---

## 📊 Implementation Statistics

| Phase | Timeline | Modules | Code | Neurons | Complexity |
|-------|----------|---------|------|---------|------------|
| 0 | 4w | 3 | 1.6K | - | Low |
| 1 | 8w | 5 | 1.7K | 1.5K | Medium |
| 2 | 8w | 3 | 950 | 1.0K | Medium |
| 3 | 8w | 3 | 1.0K | 2.0K | Medium |
| 4 | 8w | 3 | 1.0K | 2.0K | Medium |
| 5 | 16w | 5 | 2.0K | 5.0K | High |
| **Total** | **52w** | **22** | **~8.2K** | **~11.5K** | **Med-High** |

---

## 🎯 Milestones & Evaluation

### Milestone 1 (Week 4): Foundation Ready
- [ ] Dendritic neuron tests pass
- [ ] Microcircuits functional
- [ ] GPU acceleration working
- **Metric:** 10ms inference per neuron layer on GPU

### Milestone 2 (Week 12): Language Comprehension
- [ ] Wernicke module reads English text
- [ ] Extracts semantic meaning
- [ ] Learns from feedback
- **Metric:** >80% accuracy on word sense disambiguation

### Milestone 3 (Week 20): Bidirectional Language
- [ ] Broca module generates grammatical text
- [ ] End-to-end comprehension + production
- [ ] Online learning works
- **Metric:** BLEU score > 0.7 on generation task

### Milestone 4 (Week 28): Continual Learning
- [ ] Hippocampus + consolidation working
- [ ] No catastrophic forgetting on new tasks
- [ ] Memory capacity > 100K facts
- **Metric:** Continual learning benchmark >0.8 accuracy

### Milestone 5 (Week 36): Reinforcement Learning
- [ ] Basal ganglia RL agent learns tasks
- [ ] Adaptive exploration-exploitation
- [ ] Multi-step reasoning works
- **Metric:** Average reward > baseline on 3+ RL tasks

### Milestone 6 (Week 52): Full System
- [ ] All regions integrated and communicating
- [ ] Solves complex multi-modal tasks
- [ ] Energy efficient (adaptive compute)
- [ ] Continual learning enabled
- **Metric:** Multi-task performance > 0.8 across 5+ domains

---

## 💻 Technology Stack

### Core Languages
- **Python 3.10+** (main implementation)
- **JAX / PyTorch** (numerical backend)
- **Cython** (performance-critical paths)
- **CUDA / HIP** (GPU kernels)

### Libraries
```
numpy>=1.21
scipy>=1.7
jax>=0.3
torch>=1.10
optuna>=2.10  # for hyperparameter tuning
wandb>=0.12   # experiment tracking
pytest>=6.2   # testing
```

### Hardware Requirements

**Minimal (laptop):**
- CPU: i7 or equivalent
- RAM: 16GB
- Training: ~1 day per phase

**Recommended (small cluster):**
- GPU: 2× A100 80GB
- CPU: 32 cores
- RAM: 256GB
- Training: ~1 week per phase

**Ideal (research cluster):**
- GPU: 8× A100 80GB (distributed)
- CPU: 128+ cores
- RAM: 1TB+
- Training: ~2-3 days per phase

---

## 🚀 How to Start

### Week 1: Get Dendritic Neurons Running

```bash
# Clone repository
git clone https://github.com/yourname/biological-ai-brain.git
cd biological-ai-brain

# Set up environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run Phase 0 tests
pytest tests/test_dendritic_neurons.py -v

# Try a simple example
python examples/xor_dendritic.py
```

### Week 2-4: Implement Foundation

- Read DENDRITIC_NEURON_MODULE.md
- Implement DendriticNeuron class
- Implement DendriticLayer class
- Write unit tests
- Optimize for GPU

### Week 5: Start Wernicke

- Read WERNICKE_COMPREHENSION_MODULE.md
- Implement pSTG layer
- Connect to dendritic foundation
- Test phoneme parsing

### ...and so on, following the roadmap.

---

## 📈 Success Metrics

**Phase 0:**
- All dendritic tests pass
- GPU kernel efficiency >80%
- Microcircuits show expected behavior

**Phase 1:**
- Wernicke understands SQuAD-like questions
- Learning curves show improvement
- Interpretability: can read attention weights

**Phase 2:**
- Broca generates fluent English
- Semantic ↔ text bidirectional
- BLEU score competitive with small LLMs

**Phase 3:**
- No catastrophic forgetting
- Memory retrieval works (>90% accuracy)
- Consolidation improves long-term learning

**Phase 4:**
- RL agent solves 3+ environments
- Adaptive exploration working
- Dopamine modulation visible in learning

**Phase 5:**
- Multi-task learning (5+ tasks simultaneously)
- Energy efficient (can reduce to 10% compute when appropriate)
- Matches transformer performance on language benchmarks

---

## 🏁 Summary

This roadmap takes you from **mathematical specifications to working code** in **52 weeks**.

By the end:
- You have a **complete, functional AI brain** built from dendritic neurons up
- **No catastrophic forgetting** (unlike Transformers)
- **Continual online learning** capability
- **Explainable** (attention patterns, roles, modes visible)
- **Modular** (can add new regions easily)
- **Biologically grounded** (matches known neuroscience)

Start with Phase 0. Everything else builds on it.

