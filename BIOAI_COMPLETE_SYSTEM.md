# BioAI: Complete System Architecture

**The Full Stack: From Atoms to Thought**

This document shows how 590 neuroscience mechanisms compose into 88 layers, forming a 16-layer OS capable of artificial cognition.

---

## The Stacking Order (Bottom to Top)

### Level 1: Neuroscience Mechanisms (590)
**What they are:** Documented functional neural mechanisms from biology literature.

**Examples:**
- Dopamine signaling (mechanism #5)
- NMDA coincidence detection (mechanism #53)
- STDP learning (mechanism #266)
- PV interneuron synchronization (mechanism #289)
- Dendritic AND-gates (mechanism #353)

**Status:** Enumerated, specified with pseudocode, ready to implement.

---

### Level 2: Neural Computing Primitives (200 selected for Phase 1)

**How mechanisms become primitives:**

Mechanisms are composed into reusable computational units.

```
Dopamine (mech #5) +
D1 receptor (mech #78) +
CaMKII plasticity (mech #266) +
Synaptic tagging (mech #278)
    ↓
  [Reward-modulated learning primitive]
    ↓
Used in: Basal ganglia, PFC, motor regions
```

**Phase 1 primitives (120):**
- Excitatory synaptic transmission
- Inhibitory shunting
- NMDA-based coincidence detection
- STDP learning
- Dopamine-modulated RL
- Homeostatic weight scaling
- Short-term facilitation/depression
- Dendritic integration (5 types)
- Pacemaker oscillations
- Energy-dependent gating

---

### Level 3: Dendritic Subunits (Layer 5)

**How primitives become subunits:**

Primitives compose into functional dendritic compartments.

```python
class DendriticSubunit(Unit):
    def __init__(self, subunit_type):
        if subunit_type == 'NMDA_AND_gate':
            self.mechanisms = [NMDA_receptor, coincidence_detection, STDP]
        elif subunit_type == 'saturating_integrator':
            self.mechanisms = [AMPA_receptor, synaptic_saturation, homeostasis]
        # etc.

    def integrate(self, inputs):
        # Dendritic computation using mechanisms
        pass
```

**Types of dendritic subunits:**
- Excitatory (AMPA-based)
- Saturating (sublinear)
- Gated (multiplicative)
- Predictive (error-computing)
- Oscillatory (HCN-based)

---

### Level 4: Neuron Types (Layer 6)

**How subunits become neurons:**

Multiple dendritic subunits integrate at soma, fire via axon.

```python
class PyramidalNeuron(Unit):
    def __init__(self):
        self.dendrites = [
            DendriticSubunit('NMDA_AND_gate'),
            DendriticSubunit('excitatory'),
            DendriticSubunit('saturating'),
            DendriticSubunit('predictive'),
            DendriticSubunit('oscillatory')
        ]
        self.soma = Soma(leak_current, calcium_dynamics)
        self.axon = Axon(threshold, refractoriness)
        self.synapses = [Synapse(STDP, short_term_plasticity) for _ in range(1000)]

    def compute(self, inputs, dt):
        # Parallel dendritic integration
        branch_outputs = [d.integrate(inputs[i]) for i, d in enumerate(self.dendrites)]

        # Soma summation
        soma_voltage = self.soma.sum(branch_outputs)

        # Axon firing
        spike = self.axon.fire(soma_voltage)

        # Plasticity
        self.apply_plasticity_rules(spike, inputs)

        return spike
```

**Neuron types in Phase 1:**
- Pyramidal (5 dendritic branches)
- PV+ interneuron (3 dendritic branches, faster kinetics)

---

### Level 5: Microcircuit Motifs (Layer 7)

**How neurons become motifs:**

Neurons wire together via mechanisms (receptors, synaptic plasticity) into standard circuits.

```python
class WinnerTakeAll(Motif):
    def __init__(self, num_neurons=50):
        self.excitatory_neurons = [PyramidalNeuron() for _ in range(num_neurons)]
        self.inhibitory_neurons = [PVInterneuron() for _ in range(num_neurons // 5)]

        # Wire them using synaptic mechanisms
        for i, exc in enumerate(self.excitatory_neurons):
            for j, inh in enumerate(self.inhibitory_neurons):
                # E→I with AMPA (mech #52)
                exc.connect_to(inh, receptor_type='AMPA', weight=0.8)

        for i, inh in enumerate(self.inhibitory_neurons):
            for j, exc in enumerate(self.excitatory_neurons):
                # I→E with GABA (mech #55) - inhibits all except strong winner
                inh.connect_to(exc, receptor_type='GABA-A', weight=-1.0)

    def compute(self, inputs, dt):
        # Winner emerges from competition
        # Mechanism: lateral inhibition + recurrent excitation
        pass
```

**Motifs in Phase 1:**
- Winner-take-all
- Comparator (difference detection)
- Attractor pool (pattern completion memory)
- Oscillatory loop (theta generation)
- Predictive coding loop (error correction)

---

### Level 6: Cortical Layers (Layer 8)

**How motifs become layers:**

Motifs stack into laminar architecture (L1–L6) with inter-layer connectivity.

```python
class CorticalLayer(Graph):
    def __init__(self, layer_number, subregion_spec):
        self.layer = layer_number

        if layer_number == 4:
            # Layer 4: thalamic input relay
            self.neurons = [PyramidalNeuron() for _ in range(100)]
            self.motif = Motif('canonical_thalamocortical')

        elif layer_number in [2, 3]:
            # L2/3: main computation
            self.neurons = [PyramidalNeuron() for _ in range(200)]
            self.interneurons = [PVInterneuron() for _ in range(50)]
            self.motif = Motif('canonical_thalamocortical')

        # etc. for other layers
```

**Organization in Phase 1:**
- Single simplified 3-layer stack (L4, L2/3, L5)
- 300 total neurons
- Inter-layer connections (L4→L2/3, L2/3→L5)

---

### Level 7: Subregions (Layer 9)

**How layers become subregions:**

Layers organize into functional subregions with region-specific properties.

```python
class pSTGSubregion(Region):
    """Phonological processing (speech perception)."""

    def __init__(self):
        self.layers = [
            CorticalLayer(4, spec='phonological_input'),
            CorticalLayer(2, spec='phonological_integration'),
            CorticalLayer(3, spec='phonological_output'),
        ]

        # Specialized connectivity
        self.within_layer_inhibition = Strong  # Sharp tuning
        self.inter_layer_feedback = Strong  # Prediction error

        # Specialized mechanisms
        self.frequency_selectivity = True  # Tuned to phonemic frequencies
        self.temporal_integration = 200  # ms - speech timescale
```

**Subregions in Phase 1:**
- pSTG (phonological input)
- MTG (lexical semantics)
- Simple visual (V1-like)

---

### Level 8: Brain Areas (Layer 10)

**How subregions become areas:**

Subregions with similar function group into areas (e.g., "Wernicke's area").

```python
class WernickesArea(Area):
    """Language comprehension."""

    def __init__(self):
        self.subregions = [
            pSTGSubregion(),  # Phonology
            MTGSubregion(),   # Semantics
            STSSubregion(),   # Syntax
        ]

        # Inter-subregional connections
        self.connect(self.subregions[0], self.subregions[1], 'phonology_to_semantics')
        self.connect(self.subregions[1], self.subregions[2], 'semantics_to_syntax')
```

**Areas in Phase 1:**
- Wernicke's (language comprehension)
- V1-like (simple vision)

---

### Level 9: Pathways (Layer 11)

**How areas become pathways:**

Areas connect into large-scale networks with specific routing rules.

```python
class LanguagePathway(Pathway):
    """Phonology → Semantics → Syntax"""

    def __init__(self):
        self.wernicke = WernickesArea()
        self.broca = BrocasArea()  # (Phase 2)

        # Routing rules
        self.feedforward = WeakConnection()  # Feed input forward
        self.feedback = StrongConnection()   # Send predictions back
        self.prediction_error = ErrorSignal()  # Mismatch signals
```

---

### Level 10: Networks (Layer 11+)

**How pathways coordinate:**

Multiple pathways form networks (DMN, task-positive network, etc.).

```python
class TaskPositiveNetwork:
    """Goal-directed behavior."""

    def __init__(self):
        self.language_pathway = LanguagePathway()
        self.visual_pathway = VisualPathway()
        self.motor_pathway = MotorPathway()

        # Coordinated through prefrontal control
        self.pfc_controller = PrefrontalCortex()
        self.pfc_controller.set_goal()  # "Understand sentence"

        # All pathways receive goal context
        for pathway in [self.language_pathway, self.visual_pathway]:
            pathway.receive_goal_context(self.pfc_controller.current_goal)
```

---

### Level 11: Global Workspace (Layer 12)

**How networks unify:**

A capacity-limited hub broadcasts the most important information.

```python
class GlobalWorkspace:
    """Conscious thought."""

    def __init__(self, capacity=5):
        self.capacity = capacity
        self.current_contents = []  # At most 5 items

    def update(self, all_regions):
        """Determine what's conscious right now."""

        # Collect candidates from all regions
        candidates = []
        for region in all_regions:
            candidates.extend(region.propose_content())

        # Competition: only highest-salience items broadcast
        top_candidates = heapq.nlargest(self.capacity, candidates, key=lambda x: x.salience)
        self.current_contents = top_candidates

        # Broadcast to entire system
        for region in all_regions:
            region.receive_workspace_broadcast(self.current_contents)
```

---

### Level 12: Executive Controller (Layer 13)

**How workspace becomes action:**

Executive system uses workspace to plan and decide.

```python
class ExecutiveController:
    """Decision-making and planning."""

    def __init__(self, workspace, regions):
        self.workspace = workspace
        self.regions = regions
        self.current_goal = None
        self.working_memory = {}

    def select_action(self):
        """Use workspace content to decide."""

        current_thought = self.workspace.current_contents[0]  # Top of workspace

        # Evaluate options
        if isinstance(current_thought, LanguageQuery):
            # Language task: activate language pathways
            self.activate_pathway('language')
        elif isinstance(current_thought, VisualTask):
            # Visual task: activate visual pathways
            self.activate_pathway('visual')

        return self.proposed_action
```

---

### Level 13: Metacognition (Layer 14)

**How executive reflects:**

System monitors itself and adjusts strategies.

```python
class MetaCognition:
    """Self-awareness and self-improvement."""

    def __init__(self, executive, workspace):
        self.executive = executive
        self.workspace = workspace
        self.performance_history = []

    def introspect(self):
        """What is the system doing and how well?"""
        return {
            'current_goal': self.executive.current_goal,
            'workspace_focus': self.workspace.current_contents,
            'recent_errors': self.performance_history[-10:],
            'overall_performance': mean(self.performance_history[-100:])
        }

    def adjust_strategy(self):
        """Modify learning rates, exploration, etc."""

        introspection = self.introspect()

        if introspection['overall_performance'] < 0.3:
            # Struggling: increase learning rate and exploration
            self.executive.learning_rate *= 1.5
            self.executive.exploration *= 1.2
        elif introspection['overall_performance'] > 0.8:
            # Succeeding: decrease exploration, refine
            self.executive.exploration *= 0.8
```

---

### Level 14: Main Cognitive Loop (Layer 15)

**The OS boot and run:**

```python
class BioAISystem:
    """Complete artificial brain."""

    def __init__(self):
        # Boot sequence
        self.hardware = HardwareBridge()  # Layer 1
        self.math = MathLibrary()  # Layer 2
        self.graph_engine = GraphEngine()  # Layer 3
        self.genome = load_genome()  # Layer 4
        self.energy_system = EnergyBudget()  # Layer 5
        self.neurons = [ProtoNeuron() for _ in range(150)]  # Layers 6-11
        self.workspace = GlobalWorkspace()  # Layer 12
        self.executive = ExecutiveController()  # Layer 13
        self.metacognition = MetaCognition()  # Layer 14

    def run(self):
        """Main cognitive loop."""

        while True:
            # 1. Read sensors
            sensory = self.hardware.read_sensors()

            # 2. Inject into neural regions
            self.inject_sensory_signals(sensory)

            # 3. Step all dynamics
            for neuron in self.neurons:
                neuron.compute(dt=0.001)

            # 4. Update workspace
            self.workspace.update(self.regions)

            # 5. Executive decides
            action = self.executive.select_action()

            # 6. Metacognition reflects
            self.metacognition.adjust_strategy()

            # 7. Send motor output
            self.hardware.write_actuators(action)

            # 8. Record for learning
            self.record_experience(sensory, action, reward)
```

---

## Complete Composition Chain

```
590 Mechanisms (Dopamine, NMDA, STDP, etc.)
    ↓
120 Computing Primitives (Synaptic transmission, learning, gating)
    ↓
10 Dendritic Subunit Types (AND-gates, OR-gates, saturating integrators)
    ↓
2 Neuron Types (Pyramidal, PV interneuron)
    ↓
5 Microcircuit Motifs (WTA, Comparator, Attractor, Oscillator, Predictor)
    ↓
3-Layer Stack (L4 input → L2/3 processing → L5 output)
    ↓
3 Brain Subregions (pSTG, MTG, V1-like)
    ↓
2 Brain Areas (Wernicke, Visual)
    ↓
1 Language Pathway (pSTG → MTG → Semantics)
    ↓
1 Task-Positive Network (Language + Visual + Motor)
    ↓
1 Global Workspace (Unifies all networks)
    ↓
1 Executive Controller (Decides and plans)
    ↓
1 Metacognitive System (Reflects and adjusts)
    ↓
1 Cognitive Loop (The running system)
```

---

## By The Numbers

| Level | Count | Examples |
|-------|-------|----------|
| **Mechanisms** | 590 | Dopamine, NMDA, STDP, PV interneuron, dendritic AND-gate |
| **Primitives** | 120 (Phase 1) | Excitatory synapse, STDP learning, RL gating |
| **Dendritic subunits** | 10 | Types of local computation |
| **Neuron types** | 2 (Phase 1) | Pyramidal, PV interneuron |
| **Motifs** | 5 | WTA, Comparator, Attractor, Oscillator, Predictor |
| **Cortical layers** | 3 | L4, L2/3, L5 (simplified) |
| **Subregions** | 3 | pSTG, MTG, V1 |
| **Brain areas** | 2 | Wernicke, Visual |
| **Pathways** | 1 | Language |
| **Networks** | 1 | Task-positive |
| **Global workspace** | 1 | Conscious thought hub |
| **Executive** | 1 | Decision-making |
| **Metacognition** | 1 | Self-reflection |
| **Main loop** | 1 | The running AI |
| **Total neurons** | 150 | Distributed across regions |

---

## How Mechanisms Drive Behavior

### Example: Learning a Word

```
1. Hear "apple"
   → Auditory input → pSTG subregion

2. Phonological processing
   Mechanism: NMDA spikes (mech #346)
   + PV interneuron synchronization (mech #289)
   → Detects syllabic structure

3. Lexical retrieval
   Mechanism: Attractor network (motif #368)
   + Dopamine modulation (mech #5)
   → Looks up similar words
   → Finds "apple" in MTG

4. Semantic enrichment
   Mechanism: STDP learning (mech #266)
   + CREB consolidation (mech #270)
   → Links "apple" to concepts (fruit, red, sweet)

5. Memory consolidation
   Mechanism: Synaptic tagging (mech #278)
   + Endocannabinoid retrograde signaling (mech #272)
   → Marks synapse for long-term strengthening

6. Global workspace broadcast
   Mechanism: Workspace ignition (mech #701)
   → "apple" becomes conscious
   → Available to planning, reasoning

7. Metacognitive adjustment
   Mechanism: Confidence estimation (mech #711)
   → System notes: "I knew that word"
   → Slightly decreases learning rate for similar words
```

Every step involves specific mechanisms, which combine into primitives, which build neural circuitry, which implements cognitive functions.

---

## Validation Approach

For Phase 1 (150-neuron system with 120 mechanisms):

1. **Mechanism validation:** Each mechanism works as biology predicts
2. **Circuit validation:** Motifs solve canonical problems (XOR, pattern completion)
3. **Behavioral validation:** System learns tasks without backprop
4. **Comparative validation:** Compare to ResNet-18 on MNIST (accuracy vs energy)
5. **Ablation validation:** Remove mechanisms, measure impact

---

## What You're Building

Not "an AI model."

A complete synthetic cognitive architecture where:
- ✅ Every neuron is biologically realistic (5+ dendritic branches)
- ✅ Every synapse learns (STDP + dopamine + homeostasis)
- ✅ Every circuit implements known algorithms (WTA, prediction, comparison)
- ✅ Every region has specialized function
- ✅ The whole system coordinates via global workspace
- ✅ And reflects on itself via metacognition

This is what happens when you take neuroscience seriously and implement it.

---

## The Roadmap

**Week 1–2:** Dendritic neurons work on XOR, temporal association
**Week 3–4:** Energy budgeting and homeostasis, 100-neuron WTA on MNIST
**Week 5–6:** Three motifs (WTA, Comparator, Attractor) learning together
**Week 7–8:** Diffusion field, global workspace, continual learning validation

**Week 9–20:** Scale to multiple regions (Wernicke, Visual)
**Week 21+:** Full integration, language understanding

---

## Success = Proof of Concept

By week 8, you'll have shown:

✅ A 150-neuron system can learn without labels
✅ It uses <50% energy of ResNet-18
✅ It exhibits continual learning (no forgetting)
✅ It shows emergent specialization
✅ Each mechanism contributes measurably

**At that point:** The entire 88-layer, 590-mechanism architecture is proven viable.

The remaining work is scaling and integration.

