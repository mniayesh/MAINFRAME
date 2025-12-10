# BioAI: Descriptor-Based Graph Model & Stage-1 Introspection Kernel

## Executive Summary

The real foundation of the BioAI OS is not a language, not a bootloader, not an ISA.

It is a **descriptor-based graph model** that can be instantiated identically on:
- Hosted simulation (Python/Linux)
- Bare metal hardware
- Any architecture in between

And a **Stage-1 introspection kernel** that:
- Parses descriptors
- Builds the capability graph
- Exposes it for debugging/modification
- Supports hot-reload as a first-class operation
- Enables the same code to run hosted or bare-metal

**Why this matters:** Debugging and hot-reload are not separate tools. They are the same mechanism the system uses to modify and learn about itself (metacognition).

---

## Part 1: The Descriptor Format

### Core Concept

A descriptor is **data that describes a node in the computation graph**.

It answers:
- **What am I?** (type: hardware_device, math_op, neuron, circuit, etc.)
- **What can I do?** (capabilities list)
- **Who am I connected to?** (input/output edges)
- **What is my current state?** (values, parameters, learning state)
- **How do I compute?** (operation, update rule, nonlinearity type)

### Node Descriptor Format

```
Node:
  id: str                          // Unique identifier
  type: str                        // "cpu", "gpu", "neuron", "dendrite", "circuit", etc.
  version: str                     // Allows updating node implementations

  // What this node provides
  capabilities: List[str]
    // Examples:
    // - "compute.matmul"
    // - "compute.sigmoid"
    // - "spike.threshold_based"
    // - "learn.stdp"
    // - "learn.hebbian"
    // - "integrate.leaky_iaf"

  // Connectivity
  inputs: List[InputPort]
    port_name: str                 // "dendrite_0", "soma", "external", etc.
    expected_type: str             // "spike", "analog", "signal", etc.
    expected_shape: str            // "scalar", "vector[100]", "matrix[32x32]", etc.
    optional: bool                 // Can this port be omitted?

  outputs: List[OutputPort]
    port_name: str                 // "spike", "voltage", "error", etc.
    output_type: str               // What does this port emit?
    output_shape: str              // Dimensionality

  // State (the actual values)
  state: Dict[str, Value]
    // Examples for a neuron:
    voltage: f32                   // Current membrane potential
    calcium: f32                   // Calcium concentration
    refractory_timer: i32          // Time since last spike

    // Examples for synaptic weights:
    weights: Array[f32]            // Synaptic weights
    plasticity_history: Array[f32] // STDP/Hebbian trace

  // Parameters (how to compute)
  parameters: Dict[str, Value]
    // Examples for a neuron:
    tau: f32                       // Time constant
    threshold: f32                 // Spike threshold
    reset_voltage: f32
    leak_conductance: f32

    // Examples for a learning rule:
    learning_rate: f32
    stdp_window: f32
    eligibility_trace_decay: f32

  // Operation definition
  operation:
    type: str                      // "integrate", "spike", "learn", "route", etc.
    implementation_id: str         // Which version of the operation to use

    // For stateful operations, how to update
    update_rule: str               // "dv/dt = leak + input"
                                   // "w' = w + α * pre * post"
                                   // "spike = v > theta"

  // Metadata
  metadata:
    category: str                  // "hardware", "math", "neuron", "circuit", "cognitive"
    created_at: timestamp
    last_modified: timestamp

    // For debugging
    human_readable_name: str       // "Neocortex Layer V Pyramidal Cell #42"
    tags: List[str]                // ["learning_enabled", "plastic", "sparse"]
    owner_region: str              // Which brain region/module owns this?
```

### Edge Descriptor Format

```
Edge:
  id: str                          // Unique identifier
  source_node: str                 // ID of source node
  source_port: str                 // Output port name from source
  target_node: str                 // ID of target node
  target_port: str                 // Input port name on target

  // Connection properties
  weight: f32                      // Synaptic strength (0.0-1.0, can be negative)
  type: str                        // "excitatory", "inhibitory", "modulatory"

  // Guarantees
  latency: f32                     // Expected propagation delay (ms)
  bandwidth: f32                   // Max signals/second allowed

  // Learning state
  plasticity_rule: str             // "stdp", "hebbian", "homeostatic", "dopamine_modulated"
  last_spike_time: f32             // For STDP calculations

  metadata:
    created_at: timestamp
    tags: List[str]                // ["critical", "debugging_only", "plastic"]
```

### Full Graph Descriptor

```
Graph:
  nodes: List[Node]
  edges: List[Edge]

  // Metadata about the graph
  metadata:
    timestamp: timestamp
    version: str                   // "1.0", "1.1", allows incremental updates

  // What operations are valid?
  allowed_operations:
    inspect_node: true
    modify_node_state: true
    modify_node_parameters: true
    modify_edge_weight: true
    add_node: restricted          // Only certain types allowed
    remove_node: restricted       // Can't remove hardware nodes
    rewire_edges: true
    hot_reload_implementation: true

  // Constraints
  constraints:
    max_nodes: int                // Memory bound
    max_edges: int                // Wiring bound
    max_firing_rate: f32          // Frequency bound
    energy_budget: f32            // Total ATP available
```

---

## Part 2: Stage-1 Introspection Kernel

### Purpose

The Stage-1 kernel is a **tiny OS that does one thing:**
- Parse hardware descriptors
- Build the graph representation
- Expose it for inspection and modification
- Load/reload higher layers on demand

It is:
- **Minimal** (< 10KB of code)
- **Hardware-agnostic** (same code on different architectures)
- **Debuggable** (everything is introspectable)
- **Hot-reloadable** (can replace its own modules)

### Core Operations

```
API Surface (all operations are graph edits):

1. INSPECT OPERATIONS
  ─────────────────
  dump_graph() → Graph
    Returns complete current state of all nodes and edges

  dump_node(node_id) → Node
    Returns descriptor for single node

  dump_edges_for_node(node_id) → List[Edge]
    Returns all edges connected to this node

  inspect_state(node_id, field) → Value
    Get current state value (voltage, weight, etc.)

  list_nodes_by_type(type) → List[Node]
    Find all nodes of a type ("neuron", "circuit", etc.)

  list_nodes_by_tag(tag) → List[Node]
    Find all nodes with a tag ("learning_enabled", etc.)

  list_capabilities() → List[str]
    What operations are available in the system?

  trace_path(from_node, to_node) → List[Edge]
    Find connectivity path between two nodes

  measure_connectivity_distance(node_a, node_b) → int
    Shortest path distance in steps

2. MODIFY OPERATIONS
  ──────────────────
  set_state(node_id, field, value) → Status
    Update a node's state (voltage, weight, etc.)
    Returns: {success: bool, reason?: str}

  set_parameter(node_id, param_name, value) → Status
    Update a node's parameters (learning_rate, threshold, etc.)

  modify_edge_weight(edge_id, new_weight) → Status
    Adjust synaptic strength

  modify_edge_tag(edge_id, tag) → Status
    Mark edges for special handling (debugging_only, plastic, etc.)

3. STRUCTURAL OPERATIONS
  ──────────────────────
  add_node(node_descriptor) → node_id
    Create a new node (neuron, circuit, etc.)
    Returns assigned ID
    Fails if it would exceed constraints (max_nodes, energy_budget, etc.)

  remove_node(node_id) → Status
    Delete a node
    Fails if it's hardware or has critical incoming connections

  add_edge(source_id, source_port, target_id, target_port, weight) → edge_id
    Create a new connection

  remove_edge(edge_id) → Status
    Delete a connection

  rewire_edge(edge_id, new_target_id, new_target_port) → Status
    Redirect an edge to a different target (hot-reload compatible)

4. HOT-RELOAD OPERATIONS
  ──────────────────────
  deploy_shadow_module(module_descriptor) → module_id
    Create new module running in parallel with old one
    Returns ID of shadow module

  compare_outputs(old_module_id, shadow_module_id, num_samples) → Difference
    Run both modules on same inputs, compare outputs
    Returns: mean_error, max_error, behavior_similarity

  flip_routing(old_module_id, shadow_module_id) → Status
    Atomically redirect all incoming edges from old to new
    Old module gets no new inputs after this point
    New module takes over

  retire_module(module_id) → Status
    After flip_routing, gracefully shut down old module
    Wait for active computations to complete

5. CHECKPOINT/RESTORE
  ───────────────────
  snapshot_state() → Checkpoint
    Save entire graph state to a blob
    Includes all node states and edge weights
    Can be serialized to disk

  restore_from_checkpoint(checkpoint) → Status
    Load graph state from checkpoint
    Resets all node states, edge weights

  diff_checkpoints(checkpoint_a, checkpoint_b) → Diff
    Compute delta between two graph states
    Shows which nodes changed state, which edges changed weight

6. DEBUGGING OPERATIONS
  ────────────────────
  set_breakpoint(node_id, condition) → breakpoint_id
    Pause execution when condition is met
    condition: "spike_detected", "weight_changed", "state > 0.5", etc.

  trace_signal(from_node, to_node) → SignalTrace
    Record all activations on path between two nodes
    Returns time-series of values

  inject_signal(target_node, port_name, value) → Status
    Force a signal into a node (for testing)
    Useful for "what-if" scenarios

  force_spike(neuron_id) → Status
    Manually trigger a spike (for testing learning)

  inhibit_spikes(neuron_id, duration) → Status
    Prevent a neuron from spiking (for testing circuits)

  measure_energy_cost(operation) → f32
    Estimate ATP consumption for operation
```

### Return Values (All Standardized)

```
Status:
  success: bool
  message: str
  details: Dict[str, Value]  // For debugging

Example:
  {
    "success": false,
    "message": "Cannot add node: would exceed max_nodes constraint",
    "details": {
      "current_nodes": 1024,
      "max_nodes": 1024,
      "requested_nodes": 1
    }
  }
```

---

## Part 3: How This Works in Practice

### Scenario 1: Debugging a Neuron's Behavior

```
User (via REPL):
  > dump_node("neuron_42")
  {
    "id": "neuron_42",
    "type": "neuron",
    "state": {
      "voltage": -0.045,
      "calcium": 0.2
    },
    "parameters": {
      "threshold": -0.040,
      "tau": 0.02
    }
  }

  > trace_signal("synapse_100", "neuron_42")
  [
    {"timestamp": 0.0, "value": 0.1},
    {"timestamp": 0.5, "value": 0.15},
    {"timestamp": 1.0, "value": 0.18},
    ...
    {"timestamp": 50.0, "value": -0.041}  // Crosses threshold!
  ]

  > inject_signal("neuron_42", "soma", -0.041)
  {"success": true, "message": "Signal injected"}

  > set_state("neuron_42", "voltage", -0.030)
  {"success": true, "message": "Voltage set to -0.030V"}

Result: Neuron spikes immediately (crossed threshold).
```

### Scenario 2: Hot-Reloading a Learning Rule

```
User discovers STDP window is too short. Instead of recompiling:

  > get_edges_with_plasticity("neuron_42", "stdp")
  [edge_100, edge_101, edge_102]

  > new_rule = {
      "type": "stdp",
      "learning_rate": 0.01,
      "window": 0.10  // Was 0.05, now longer
    }

  > deploy_shadow_module({
      "type": "synapse",
      "plasticity_rule": new_rule
    })
  "synapse_shadow_100"

  > compare_outputs("edge_100", "synapse_shadow_100", 1000)
  {
    "mean_error": 0.002,  // Very small difference
    "similarity": 0.998   // 99.8% same behavior
  }

  > flip_routing("edge_100", "synapse_shadow_100")
  {"success": true}

  > retire_module("edge_100")
  {"success": true}

Result: STDP window changed, no restart, no recompilation.
```

### Scenario 3: Discovering Hardware Capabilities

```
Stage 1 boots on new hardware.

Hardware descriptor (provided by bootloader):
  {
    "nodes": [
      {"id": "cpu_0", "type": "cpu", "capabilities": [
        "compute.add",
        "compute.mul",
        "compute.matmul"
      ]},
      {"id": "gpu_0", "type": "gpu", "capabilities": [
        "compute.matmul_large",  // 1000×1000 and above
        "compute.conv2d"
      ]},
      {"id": "ane_0", "type": "ane", "capabilities": [
        "compute.neural_ops",
        "compute.matmul_specialized"
      ]}
    ]
  }

Stage 1 calls:
  > list_capabilities()
  [
    "compute.add",
    "compute.mul",
    "compute.matmul",
    "compute.matmul_large",
    "compute.conv2d",
    "compute.neural_ops",
    "compute.matmul_specialized"
  ]

Later, Layer 2 (biological substrate) queries:
  > list_capabilities()
  > // Same result, doesn't need to know where they come from
  > // Chooses matmul_specialized for dendritic computation
  > // Uses matmul_large for circuit-level matrix operations
  > // Uses add/mul for single-neuron thresholds

Result: Same code runs identically on different hardware.
```

---

## Part 4: How Debugging/Hot-Reload Enables Metacognition

### The Key Insight

The mechanism you use to **debug the system** is the same mechanism the **system uses to modify itself**.

#### Example 1: Synaptic Plasticity IS Hot-Reload

Traditional view:
```
Learning = weights change via backprop
Debugging = I inspect/modify weights manually
These are different processes.
```

BioAI view:
```
Learning = STDP rule updates weights (graph operation: modify_edge_weight)
Debugging = I modify weights manually (graph operation: modify_edge_weight)
Metacognition = System inspects/modifies its own weights (graph operation: modify_edge_weight)

All the same operation. Just triggered by different signals.
```

#### Example 2: Structural Learning IS Node Creation

```
You (human): "Let me add a new microcircuit"
  > add_node(microcircuit_descriptor)

System (learning): "I should specialize this region"
  > add_node(microcircuit_descriptor)  // Same operation!

The system learns to add new structures using the same API.
```

#### Example 3: Circuit Rewiring IS Hot-Reload

```
You: "Let me change which neurons feed into this attractor"
  > rewire_edge(edge_old, new_target)

System (reorganizing): "This pathway is inefficient"
  > rewire_edge(edge_old, new_target)  // Same operation!

Self-optimization happens through graph edits, like debugging.
```

### Why This Matters for Real AI

A system that **debugs itself** is a system that **learns at multiple levels**:

1. **Level 1:** Synaptic weights change (traditional learning)
2. **Level 2:** Network wiring changes (structural learning)
3. **Level 3:** Nodes are added/removed (growing/pruning learning)
4. **Level 4:** Computation rules change (metarule learning)
5. **Level 5:** The system inspects and modifies Level 4 (metacognition)

All through the same operation API.

---

## Part 5: Hosted vs. Bare Metal

### Hosted Mode (Simulation on Linux/macOS)

```
Hardware descriptor (simulated):
  {
    "nodes": [
      {"id": "cpu_0", "type": "cpu", "capabilities": ["compute.add", "compute.mul", ...]},
      {"id": "ram_0", "type": "memory", "capacity": 16GB},
      {"id": "disk_0", "type": "storage", "capacity": 1TB}
    ]
  }

Stage 1 (Python/C):
  - Parses descriptor
  - Maps "compute.matmul" → NumPy matmul
  - Maps "ram_0.allocate" → malloc
  - Maps "disk_0.read" → fopen/fread
  - Builds graph, exposes REPL over socket

Layer 2+:
  - Same code as bare metal
  - Doesn't know it's simulated
  - Can hot-reload, debug, introspect identically
```

### Bare Metal Mode

```
Bootloader:
  - Detects actual hardware (CPU, GPU, ANE, RAM, storage)
  - Builds hardware descriptor from actual devices
  - Jumps into Stage 1

Stage 1 (bare metal kernel):
  - Parses descriptor (same code as hosted!)
  - Maps "compute.matmul" → GPU driver call
  - Maps "ram_0.allocate" → physical memory allocation
  - Maps "disk_0.read" → disk controller command
  - Builds graph, exposes REPL over serial/USB/network

Layer 2+:
  - Same code as hosted
  - Runs identically
  - Can hot-reload, debug, introspect identically
```

### The Migration Path

```
Stage 1:
  Week 1: Implement in Python (hosted mode)
    - Parse descriptor
    - Provide REPL
    - Expose graph operations
    - Test on simulated hardware

  Week 2-3: Implement in C (still hosted)
    - Same logic, compiled version
    - Prepare for bare metal

  Week 4: Create minimal bootloader
    - Hardware detection
    - Build real descriptor
    - Jump into Stage 1 (C version, now bare metal)

Result: NO CODE CHANGES in Layer 2+
        Only the descriptor source changes (simulated vs. real hardware)
```

---

## Part 6: Why This Solves the "No Hardcoded APIs" Problem

### Traditional Problem

```
How do you build a system with ZERO hardcoded types/interfaces?

Answer: You can't (in traditional systems).

The type system will leak from the OS into your application.
Python's int will contaminate everything.
```

### BioAI Solution

```
You DON'T hardcode types. You hardcode the DESCRIPTOR FORMAT.

That's it.

Everything else is a node in the graph.

- Math ops? Nodes with capabilities.
- Neurons? Nodes with parameters.
- Learning rules? Nodes with state.
- Cognition? Nodes with inputs/outputs.

The descriptor format is the ONLY hardcoded thing.

Everything above it is data-driven, not code-driven.
```

### Why This Works

```
Descriptor Format: Fixed (the ABI)
  └─ Graph Structure: Dynamic (data-driven)
    └─ Layer 0 (hardware ops): Discovered from descriptor
      └─ Layer 1 (math): Discovered from Layer 0
        └─ Layer 2+ (biology): Discovered from Layer 1

No hardcoded types.
No hardcoded interfaces.
Everything discovered at boot.
```

---

## Part 7: Implementation Order

### Phase 0: Design (Complete)
- ✅ Descriptor format specification
- ✅ Graph model specification
- ✅ Stage-1 operations specification

### Phase 1: Hosted Implementation (2-3 weeks)

**In Python:**

```python
class Descriptor:
    def __init__(self, json_spec):
        self.id = json_spec["id"]
        self.type = json_spec["type"]
        self.capabilities = json_spec["capabilities"]
        # ... load all fields from JSON

class Graph:
    def __init__(self, descriptor_list):
        self.nodes = {d.id: Descriptor(d) for d in descriptor_list}
        self.edges = {}

class Stage1Kernel:
    def __init__(self, hardware_descriptor):
        self.graph = Graph(hardware_descriptor["nodes"])
        self.repl = REPL(self)

    def dump_graph(self):
        return self.graph

    def set_state(self, node_id, field, value):
        self.graph.nodes[node_id].state[field] = value
        return {"success": True}

    # ... implement all operations

kernel = Stage1Kernel(hardware_descriptor)
kernel.repl.start()  # Python REPL connected to graph
```

**Result:** A working introspection system in ~1000 lines of Python.

### Phase 2: Add Simulated Hardware Descriptor

```python
hardware_descriptor = {
    "nodes": [
        {
            "id": "cpu_0",
            "type": "cpu",
            "capabilities": ["compute.add", "compute.mul", "compute.matmul"]
        },
        {
            "id": "gpu_0",
            "type": "gpu",
            "capabilities": ["compute.matmul_large"]
        },
        {
            "id": "ram_0",
            "type": "memory",
            "capacity": 16 * 1024 * 1024 * 1024
        }
    ]
}

kernel = Stage1Kernel(hardware_descriptor)
```

**Result:** Stage 1 can introspect "hardware" (simulated).

### Phase 3: Add Layer 0-1 Operations

```python
# Layer 0: CPU operations
class CPUOp:
    def add(a, b):
        return a + b

# Layer 1: Math dispatch
class MathDispatcher:
    def dispatch(operation_name, args):
        if operation_name == "add":
            return CPUOp.add(*args)

# In Stage 1:
kernel.math_dispatcher = MathDispatcher()
```

**Result:** Stage 1 can dispatch to math operations based on capability query.

### Phase 4: Add Layer 2 (Biological Substrate)

```python
# Create nodes for dendritic units
dendrite_descriptor = {
    "id": "dendrite_0",
    "type": "dendritic_branch",
    "capabilities": ["integrate.nonlinear", "learn.stdp"],
    "inputs": [{"name": "synapse_0", "type": "spike"}],
    "outputs": [{"name": "voltage", "type": "analog"}],
    "state": {"weights": [0.1, 0.2, ...]},
    "parameters": {"learning_rate": 0.01}
}

kernel.add_node(dendrite_descriptor)
```

**Result:** Biological nodes living in the same graph as hardware descriptors.

### Phase 5: Connect It All

```
User (REPL) → Stage 1 Kernel → Graph
                              ├─ Hardware Descriptor (CPU, GPU, RAM)
                              ├─ Math Ops (ADD, MUL, MATMUL)
                              └─ Biological Nodes (dendrites, neurons, circuits)

All introspectable. All modifiable. All hot-reloadable.
```

---

## Conclusion

The descriptor-based graph model is the **real OS**.

It is:
- **Minimal** (100 lines to parse a descriptor)
- **Hardware-agnostic** (works hosted or bare metal)
- **Self-introspectable** (you can read/modify the running graph)
- **Debuggable** (every operation is a graph edit)
- **Self-modifying** (learning = graph modifications)
- **Metacognitive** (the system can introspect/modify itself)

Everything above it (Layer 0, 1, 2+, cognition) is just:
- **Descriptors** (data describing what you want)
- **Operations** (graph edits that make it happen)
- **Introspection** (reading back what happened)

No bootloader complexity needed first.
No language needed first.
No new hardware needed first.

Just: descriptors + graph operations + a REPL.

Start there. Build everything else from it.

And when you're ready, the same code runs on bare metal.
