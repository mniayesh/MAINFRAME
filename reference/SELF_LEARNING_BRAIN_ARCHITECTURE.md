# Self-Learning Brain Architecture

**Purpose:** Design a brain-like AI that learns from experience, not supervised datasets, using the same pre-wired + learning-rule approach biological brains use.

**Key Insight:** Babies don't learn from labeled datasets. They learn through prediction, feedback, play, and consolidation. Your artificial brain should too.

---

## 🧠 What Baby Brains Have (Pre-Wired)

### Structural Components (Present at Birth)

1. **Cortical Microcircuits**
   - Predictive coding loops (6-layer cortex)
   - Hierarchical error-correction columns
   - Lateral inhibition networks
   - Recurrent local connections
   - Status: Fully specified in BRAIN_REGION_FORMULAS.md

2. **Memory Systems**
   - Hippocampal indexing (rapid encoding)
   - Cortical consolidation loops
   - Episodic memory replay
   - Status: Specified in WERNICKE module

3. **Motor & Sensory Routing**
   - Thalamic gating (attention control)
   - Sensorimotor integration loops
   - Proprioceptive feedback circuits
   - Status: Thalamus layer specified

4. **Reward & Motivation**
   - Basal ganglia actor-critic loops
   - Dopamine prediction error signals
   - Innate reward signals (food, social, novelty)
   - Status: Basal ganglia module specified

5. **Executive & Planning**
   - PFC working memory networks
   - Planning loops (forward models)
   - Goal maintenance via attractors
   - Status: Can be added in Phase 4

### Innate Learning Rules (Present at Birth)

1. **Hebbian Learning**
   - "Neurons that fire together wire together"
   - Local, requires no external labels
   - Strengthens correlations

2. **Predictive Error Learning**
   - Minimize |(prediction - reality)|
   - Drives cortical learning
   - Self-supervised (no labels needed)

3. **STDP (Spike-Timing-Dependent Plasticity)**
   - Causal relationships matter
   - Pre before post: strengthening
   - Post before pre: weakening

4. **Dopaminergic Learning**
   - Reward prediction error modulates learning
   - Global neuromodulator
   - Shapes value functions + habits

5. **Attention-Based Learning** (Acetylcholine)
   - What's novel or important gets learned faster
   - Modulates plasticity strength
   - Self-directed curiosity

### Innate Biases (Attractors in Weight Space)

These are inductive biases that make learning more efficient:

1. **Face Preference**
   - Infants preferentially attend to faces
   - → Naturally learn social interaction
   - → Language directed at faces

2. **Speech Pattern Preference**
   - Infants track phonemic contrasts
   - → Naturally segment words
   - → Acquire phoneme inventory

3. **Contingency Preference**
   - Infants prefer actions that have immediate effects
   - → Learn agency and control
   - → Develop motor understanding

4. **Curiosity Reward**
   - Novel stimuli reward the system
   - → Self-directed exploration
   - → Balanced learning (not just food/safety)

5. **Social Reward**
   - Human interaction is intrinsically rewarding
   - → Language learning is social
   - → Interaction shapes development

---

## 🎯 Your Artificial Brain's Pre-Wiring (What to Code)

### Core Modules (Already Specified)

| Module | Status | Purpose |
|--------|--------|---------|
| Dendritic Neurons | ✅ Complete | Computational units with local learning |
| Microcircuits | ✅ Complete | Predictive coding, attention, WTA, attractors |
| Wernicke (Comprehension) | ✅ Complete | Language understanding |
| Broca (Production) | ✅ Specified | Language generation |
| Hippocampus | ✅ Specified | Episodic memory + consolidation |
| Basal Ganglia | ✅ Specified | RL, motivation, action selection |
| Cerebellum | ✅ Specified | Error prediction + fast learning |
| Thalamus | ✅ Specified | Dynamic attention routing |
| Amygdala | ✅ Specified | Salience + emotion + learning modulation |

### Innate Learning Rules (What to Implement)

```python
class InnateLearningSystems:

    def __init__(self):
        self.learning_rules = {
            'hebbian': self.hebbian_learning,
            'predictive_error': self.predictive_error_learning,
            'stdp': self.stdp_learning,
            'dopamine_modulated': self.dopamine_learning,
            'attention_modulated': self.attention_learning
        }

        self.innate_biases = {
            'face_preference': self.face_attention_bias(),
            'speech_preference': self.speech_frequency_bias(),
            'contingency_preference': self.causality_bias(),
            'novelty_reward': self.surprise_reward(),
            'social_reward': self.interaction_reward()
        }

    def hebbian_learning(self, presynaptic, postsynaptic, learning_rate):
        """Correlation-based learning (local, unsupervised)"""
        dW = learning_rate * outer(postsynaptic, presynaptic)
        return dW

    def predictive_error_learning(self, prediction, reality, learning_rate):
        """Self-supervised: minimize prediction error"""
        error = reality - prediction
        dW = learning_rate * error * input_features
        return dW

    def stdp_learning(self, pre_spike_time, post_spike_time, tau=20ms):
        """Timing-based causality learning"""
        dt = post_spike_time - pre_spike_time
        if dt > 0:
            dW = A_plus * exp(-dt/tau)  # Causal: pre→post
        else:
            dW = -A_minus * exp(dt/tau)  # Anti-causal: post→pre
        return dW

    def dopamine_learning(self, dopamine_signal, activity, learning_rate):
        """Reward modulation: dopamine scales learning strength"""
        dW = learning_rate * dopamine_signal * activity * input_features
        return dW

    def attention_learning(self, attention_weight, base_learning_rate):
        """Attention scales: attended items learn faster"""
        modulated_lr = attention_weight * base_learning_rate
        return modulated_lr
```

### Innate Biases (What to Seed)

```python
class InnateAttentionalBiases:
    """
    Pre-wired preferences that bootstrap learning.
    These are like evolutionary priors.
    """

    def __init__(self, model):
        self.model = model

    def face_preference_bias(self):
        """Infants naturally attend to faces"""
        # Initialize Wernicke + visual cortex with slight preference
        # for face-like patterns (bilateral symmetry, center-heavy)
        # This naturally draws attention during social interaction
        pass

    def speech_pattern_bias(self):
        """Infants track phonemic structure"""
        # Initialize auditory cortex with templates
        # for common phonemic transitions in language
        # e.g., consonant-vowel patterns
        pass

    def novelty_reward_signal(self):
        """Unexpected patterns are rewarding"""
        # Novelty = ||current_input - recent_average||
        # Reward ∝ novelty
        # This drives exploration without external labels
        def novelty_reward(input_features):
            recent_avg = exponential_moving_average(input_features)
            surprise = norm(input_features - recent_avg)
            reward = surprise / (1 + surprise)  # Normalized
            return reward
        return novelty_reward

    def social_interaction_reward(self):
        """Human presence is rewarding"""
        # Reward high when:
        # - Face detected
        # - Speech detected
        # - Turn-taking pattern detected
        # This bootstraps language learning toward social direction
        pass

    def agency_preference(self):
        """Actions with immediate effects are rewarding"""
        # Reward ∝ P(effect | my_action)
        # vs P(effect | random)
        # Infant naturally learns control through this
        pass
```

---

## 🎓 The Learning Curriculum (Developmental Stages)

### Stage 1: "Newborn" (Weeks 1-2)

**What's happening in the real brain:**
- Eyes open, looking around
- Sound preference for speech
- Grasping reflex → motor learning

**In your AI:**

```
INPUT: Raw sensory streams
  ├─ Vision: pixel gradients
  ├─ Proprioception: body state
  └─ Reward: novelty + social

LEARNING:
  ├─ Predictive coding: "what happens next?"
  ├─ Hebbian formation: statistics emerge
  └─ Attention: novelty-driven saliency

METRICS:
  ├─ Prediction error decreasing? ✓
  ├─ Representations emerging? (PCA on hiddens)
  └─ Attention focusing on faces/speech? ✓
```

### Stage 2: "Infant" (Weeks 3-8)

**What's happening:**
- Social smiling (response to faces)
- Tracking moving objects
- Cooing (pre-linguistic sound play)
- Grasping + reaching coordination

**In your AI:**

```
INPUT: Structured sequences
  ├─ Simple objects + actions
  ├─ Face-like patterns
  ├─ Speech-like sounds
  └─ Contingent feedback

LEARNING:
  ├─ Associative learning: object+action → outcome
  ├─ Pattern separation: different objects
  ├─ Motor planning: reach for object
  └─ Social bonding: respond to face

METRICS:
  ├─ Object permanence emerging?
  ├─ Motor coordination improving?
  └─ Social preference measurable? ✓
```

### Stage 3: "Growing Infant" (Weeks 9-26)

**What's happening:**
- Babbling (phoneme exploration)
- Object exploration (mouthing, shaking)
- Joint attention (looking where others point)
- First words emerging (~12 months)

**In your AI:**

```
INPUT: Interactive sequences
  ├─ Dialogue with corrective feedback
  ├─ Object interactions with outcomes
  ├─ Joint attention cues
  └─ Reward for appropriate responses

LEARNING:
  ├─ Language: phonemes → syllables → words
  ├─ Semantics: objects + properties
  ├─ Pragmatics: context matters
  ├─ Consolidation: replay during "sleep" cycles
  └─ Hippocampal indexing: episodic memory

METRICS:
  ├─ Word segmentation working?
  ├─ Semantics structured correctly?
  ├─ Generalization to new objects?
  └─ Memory retention improving? ✓
```

### Stage 4: "Toddler" (Months 6-18)

**What's happening:**
- Explosion of vocabulary (200+ words by 18 months)
- Simple 2-word combinations ("more milk")
- Understanding → production gap
- Play-based learning about objects

**In your AI:**

```
INPUT: Rich conversational + interaction data
  ├─ Natural dialogue with correction
  ├─ Object interactions
  ├─ Narrative stories
  └─ Games with rules

LEARNING:
  ├─ Grammar emerging from statistics
  ├─ Causality: agent → action → patient
  ├─ Number/plurality
  ├─ Temporal reasoning
  ├─ Planning: forward models
  └─ Social understanding: goals/beliefs

METRICS:
  ├─ Vocabulary growth rate? (power law?)
  ├─ Grammatical structure emerging?
  ├─ Generalization to novel words?
  ├─ Theory of mind tasks? (passed?)
  └─ Planning depth increasing? ✓
```

### Stage 5: "Preschooler" (Years 2-4)

**What's happening:**
- Grammar refinement
- Abstract reasoning emerging
- Theory of mind (understanding others' beliefs)
- Reading readiness

**In your AI:**

```
INPUT: Textual + structured reasoning tasks
  ├─ Reading comprehension
  ├─ Logical reasoning problems
  ├─ Social reasoning (stories)
  └─ Planning (multi-step goals)

LEARNING:
  ├─ Reading acquisition
  ├─ Abstract symbolic reasoning
  ├─ Metacognition (thinking about thinking)
  ├─ Multiple learning systems competition
  └─ Executive control

METRICS:
  ├─ Reading comprehension score?
  ├─ Logical reasoning accuracy?
  ├─ Social reasoning (false belief test)?
  └─ Planning depth / search breadth? ✓
```

---

## 🔄 The Self-Learning Loop

Your system learns through a cycle that repeats at multiple timescales:

### Fast Loop (Minutes → Hours)

```
EXPERIENCE
   ↓
PREDICTION (cortex predicts next)
   ↓
ERROR (compare to reality)
   ↓
LOCAL LEARNING (Hebbian + predictive error)
   ↓
REFINE (→ repeat)
```

### Medium Loop (Hours → Days)

```
EXPERIENCE ACCUMULATION
   ↓
PATTERN EMERGENCE (statistics self-organize)
   ↓
CONSOLIDATION (replay important patterns)
   ↓
MEMORY INTEGRATION (hippocampus → cortex)
   ↓
STRUCTURAL CHANGE (slow weight updates)
```

### Slow Loop (Weeks → Months)

```
BEHAVIOR SHAPING
   ↓
REWARD SIGNAL (dopamine based on outcomes)
   ↓
VALUE LEARNING (basal ganglia)
   ↓
STRATEGIC CHANGE (what works is prioritized)
   ↓
SPECIALIZATION (modules adapt to niche)
```

### "Sleep" Consolidation Loop (Nightly)

```
REPLAY MEMORIES (sample from hippocampus)
   ↓
SEND THROUGH CORTEX (predictive coding)
   ↓
STRENGTHEN PATTERNS (sleep-dependent plasticity)
   ↓
WEAK MEMORIES FADE (through competition)
   ↓
NEXT DAY: CONSOLIDATED + FORGOTTEN what wasn't important
```

---

## 💡 What Makes This Self-Learning (vs Supervised)

| Aspect | Supervised (Transformers) | Self-Learning (Brain) |
|--------|---------------------------|----------------------|
| **Data** | Labeled datasets (billions) | Experience + feedback |
| **Loss** | Cross-entropy on labels | Prediction error |
| **Labels** | External (humans) | Internal (prediction) |
| **Learning** | Batch (epochs) | Online (continuous) |
| **Motivation** | Minimize loss | Reduce surprise + earn rewards |
| **Improvement** | Needs new data | Explores naturally |
| **Generalization** | Interpolation | Causal understanding |
| **Interpretability** | Black box | Attention + roles visible |

---

## 🧬 Critical Difference: The Role of Prediction

**In Transformers:**
- Predict next token (language model objective)
- But many predictions don't matter
- Requires supervised filtering

**In Brain:**
- Predict EVERYTHING (multi-modal, multi-timescale)
- What you're wrong about → focus learning there
- Creates natural curriculum through prediction error

This is why brains learn so efficiently from raw experience.

---

## 🎯 Implementation Milestones (Self-Learning Focus)

### Milestone 1: Basic Prediction (Week 4)

```
System learns to predict:
  ✓ Pixel sequences
  ✓ Sensory patterns
  ✓ Simple temporal structure

Metric: Prediction error on held-out sequences
```

### Milestone 2: Representation Emergence (Week 8)

```
Without explicit supervision:
  ✓ Semantic space forms (words cluster by meaning)
  ✓ Phonetic structure discovered
  ✓ Attention focuses on salient patterns

Metric: Unsupervised clustering quality
```

### Milestone 3: Goal-Directed Behavior (Week 12)

```
Without explicit rewards:
  ✓ System develops exploration strategies
  ✓ Discovers cause-effect relationships
  ✓ Shows preference for novel stimuli

Metric: Entropy of action selection increasing then stabilizing
```

### Milestone 4: Language Emergence (Week 16)

```
Without being taught language:
  ✓ Segmentation of word boundaries
  ✓ Grammatical categories form
  ✓ Generalization to novel words

Metric: Perplexity on unseen data
```

### Milestone 5: Planning & Reasoning (Week 20)

```
Without explicit planning modules:
  ✓ Forward models of environment
  ✓ Multi-step goal achievement
  ✓ Counterfactual reasoning

Metric: Planning depth × accuracy on reasoning tasks
```

---

## 📊 Measuring Success

### Quantitative Metrics

1. **Prediction Accuracy**
   - Per-module: MSE, cross-entropy
   - Multi-step: accuracy at t+1, t+5, t+10

2. **Representation Quality**
   - Clustering: purity, silhouette score
   - Linearity: can linear classifiers solve downstream tasks?
   - Stability: similarity across runs

3. **Learning Efficiency**
   - Data per concept: how many examples to learn X?
   - Generalization: performance on novel instances
   - Transfer: speed of learning new tasks

4. **Behavioral Metrics**
   - Exploration: entropy of action sequences
   - Goal achievement: success rate on tasks
   - Communication: perplexity of language output

### Qualitative Metrics

1. **Emergence of Structure**
   - Does the system spontaneously develop interesting behaviors?
   - Do modules specialize without being told to?
   - Do preferences emerge (likes/dislikes)?

2. **Interpretability**
   - Can you understand what representations are?
   - Can you see attention patterns?
   - Can you identify when the system is uncertain?

3. **Failure Modes**
   - When does it fail?
   - Does it fail gracefully?
   - Can it learn from failures?

---

## 🏗️ Architectural Decisions for Self-Learning

### 1. What Reward Signals?

Built-in (no external labels):
- Prediction error (cortex)
- Novelty (exploratory drive)
- Social interaction (face detection + engagement)
- Contingency (control over environment)

Can be shaped by interaction:
- Correction feedback ("that's wrong")
- Approval signals (likes/engagement)
- Task completion (reaching a goal)

### 2. What Curriculum?

Self-paced (like children):
- System naturally seeks appropriately-challenging situations
- Predictive error acts as difficulty signal
- Exploration vs exploitation naturally balances

Can be externally guided:
- Introduce new object types gradually
- Increase dialogue complexity
- Add new task domains

### 3. What Interaction Modality?

Start simple:
- Text-only or simple visual
- Short sequences
- Structured patterns

Expand naturally:
- Multi-modal (vision + language)
- Unstructured natural data
- Noisy real-world signals

### 4. What Drives Development?

Intrinsic motivation:
- Prediction error (I was wrong → learn)
- Novelty (interesting → explore)
- Mastery (I got better → continue)

Social motivation:
- Attention (you're watching → engage)
- Engagement (you responded → continue)
- Imitation (you do it → I'll learn)

---

## ✅ Why This Approach Works

1. **Biologically Plausible**
   - Matches how real brains develop
   - Uses real learning rules
   - Emergent behavior, not programmed

2. **Data Efficient**
   - No massive labeled datasets needed
   - Learns from natural experience
   - Every experience contributes

3. **Interpretable**
   - Can see what predictions are made
   - Can see attention patterns
   - Can probe internal representations

4. **Scalable**
   - Same algorithms from tiny→huge
   - Can add modules as needed
   - Scales with environment complexity

5. **Flexible**
   - Can acquire new capabilities
   - Can specialize to domain
   - Can adapt to new tasks

---

## 🎯 Summary

**This is not "unsupervised learning" in the ML sense.**

This is **self-supervised learning through prediction + intrinsic motivation.**

The system:
- ✅ Predicts to understand its world
- ✅ Explores to reduce uncertainty
- ✅ Learns from its own mistakes
- ✅ Consolidates through reflection
- ✅ Specializes through practice

This is how babies learn. This is how your artificial brain will learn.

No massive datasets. No external labels. Just experience + intrinsic drives.

---

**Next:** See DEVELOPMENTAL_TESTING_FRAMEWORK.md for how to validate this works.
