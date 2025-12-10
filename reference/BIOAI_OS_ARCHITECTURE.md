# BIOAI OS: Complete Architecture from Bare Metal to Thought

**Version:** 1.0
**Status:** Full Specification + Implementation Blueprint
**Goal:** A new operating system paradigm built on biological principles, with 16 layers from physical hardware to conscious thought.

---

## Executive Summary

This document specifies a complete OS for biological AI: a system that:
- Starts at bare metal (CPU/GPU/RAM)
- Builds upward through 16 layers
- Reaches full cognitive competence (learning, planning, self-awareness)
- Treats biology not as metaphor, but as executable specification

**Key principle:** Each layer is defined by its API boundary. What's below is opaque. What's above depends only on the interface.

---

## Layer 0: Physical Hardware (Reality)

**What it is:**
- CPU: ISA, registers, cache, ALUs, SIMD
- GPU / NPU / ANE with compute units
- RAM: addressable byte array
- Storage: blocks, sectors, LBAs
- NIC: packet I/O
- Clocks and interrupts

**What it knows:**
- Execute bytes as machine instructions
- Move bits between registers, memory, devices

**What it doesn't know:**
- Values, types, neurons, APIs
- Any semantics beyond "instruction format"

**API upward:** None—Layer 1 reaches down directly.

---

## Layer 1: Hardware Bridge (Fixed Platform Layer)

**Purpose:**
The single hardcoded software layer that knows how to talk to this specific hardware box optimally. Once written for a platform, this layer is frozen forever.

**What it defines:**
1. **CPU initialization & execution context**
   - CPU mode setup (kernel/user, privilege levels)
   - Exception/interrupt handlers
   - Stack and call frame management
   - Register allocation conventions

2. **Memory management**
   - Virtual → physical address translation
   - TLB/paging setup
   - Heap allocation, free lists, garbage collection interface
   - Cache-aware layout hints

3. **Device drivers (hand-tuned for this box)**
   - MMIO addresses and register offsets
   - DMA queues, doorbells, signaling protocols
   - Interrupt service routines for each device

4. **Core primitives** (the only things Layer 1 exports)

```python
# CPU execution
def cpu_exec(code_ptr: uint64, arg_ptr: uint64) -> uint64:
    """Execute machine code at code_ptr with args at arg_ptr.
    Returns result in processor register."""
    # Opaque: machine code execution
    pass

# Memory operations
def mem_alloc(size: uint64) -> uint64:
    """Allocate size bytes, return base pointer."""
    pass

def mem_free(ptr: uint64) -> None:
    """Release allocated memory."""
    pass

def mem_read(ptr: uint64, len: uint64) -> bytes:
    """Read len bytes from ptr."""
    pass

def mem_write(ptr: uint64, data: bytes) -> None:
    """Write data to ptr."""
    pass

# GPU/accelerator operations
def gpu_run(kernel_id: uint32, buffers: list[uint64], params: dict) -> None:
    """Execute GPU kernel kernel_id.
    buffers: list of GPU memory pointers.
    params: scalar arguments (learning rates, thresholds, etc.)."""
    pass

def gpu_alloc(size_bytes: uint64) -> uint64:
    """Allocate GPU memory."""
    pass

def gpu_read(gpu_ptr: uint64, len: uint64) -> bytes:
    """Copy from GPU to CPU."""
    pass

def gpu_write(gpu_ptr: uint64, data: bytes) -> None:
    """Copy from CPU to GPU."""
    pass

def npu_run(graph_id: uint32, tensors: list[uint64]) -> None:
    """Run NPU inference graph."""
    pass

# Disk I/O
def disk_read(lba: uint64, count: uint32, dst_ptr: uint64) -> None:
    """Read count sectors from LBA into memory at dst_ptr."""
    pass

def disk_write(lba: uint64, count: uint32, src_ptr: uint64) -> None:
    """Write count sectors from src_ptr to LBA."""
    pass

# Timing
def get_timestamp() -> uint64:
    """Return nanoseconds since boot."""
    pass

def sleep_ns(ns: uint64) -> None:
    """Sleep for at least ns nanoseconds."""
    pass

# Sensor/actuator I/O (if robot)
def read_sensor(sensor_id: uint32) -> bytes:
    """Read sensor data."""
    pass

def write_actuator(actuator_id: uint32, command: bytes) -> None:
    """Send command to actuator."""
    pass
```

**Properties:**
- **Completeness:** Every operation that touches hardware goes through these functions.
- **Simplicity:** No semantics, no state machines, no buffering policies. Just translation.
- **Determinism:** Same input → same output.
- **Portability:** Everything above Layer 1 is identical across platforms. Swap Layer 1, run same code on different hardware.

**Example:** One Layer 1 for x86 + NVIDIA GPU. Different Layer 1 for ARM + Mali GPU. Everything else unchanged.

---

## Layer 2: Math / Compute Layer

**Purpose:**
Convert hardware primitives into a universe of mathematical operations. This layer answers: "How do I make the hardware compute what I want?"

**Built on:** Layer 1 only.

**What it provides:**

### 2a. Scalar Operations
```python
def add(a: float, b: float) -> float:
    """a + b."""
    pass

def mul(a: float, b: float) -> float:
    """a * b."""
    pass

def exp(x: float) -> float:
    """e^x."""
    pass

def tanh(x: float) -> float:
    """tanh(x)."""
    pass

def sigmoid(x: float) -> float:
    """1 / (1 + e^-x)."""
    pass

def relu(x: float) -> float:
    """max(0, x)."""
    pass
```

### 2b. Tensor Operations

Tensors are n-dimensional arrays in device memory (CPU RAM or GPU VRAM).

```python
class Tensor:
    """Handle to a chunk of memory, with shape and dtype metadata."""
    ptr: uint64         # Pointer (CPU or GPU)
    shape: tuple[int]   # e.g., (batch, height, width, channels)
    dtype: str          # 'float32', 'float16', 'int32', etc.
    device: str         # 'cpu', 'gpu', 'npu'

def tensor_alloc(shape: tuple[int], dtype: str, device: str) -> Tensor:
    """Allocate tensor on device."""
    pass

def tensor_read(t: Tensor) -> numpy.ndarray:
    """Copy tensor from device to CPU numpy array."""
    pass

def tensor_write(t: Tensor, data: numpy.ndarray) -> None:
    """Copy numpy array to tensor on device."""
    pass

def add(a: Tensor, b: Tensor) -> Tensor:
    """Element-wise a + b. Returns new tensor."""
    pass

def mul(a: Tensor, b: Tensor) -> Tensor:
    """Element-wise a * b."""
    pass

def matmul(A: Tensor, B: Tensor) -> Tensor:
    """Matrix multiply A @ B."""
    pass

def conv2d(X: Tensor, K: Tensor, stride: int, padding: int) -> Tensor:
    """2D convolution."""
    pass

def softmax(X: Tensor, axis: int) -> Tensor:
    """Softmax normalization along axis."""
    pass

def norm(X: Tensor, p: float = 2.0) -> float:
    """L-p norm of tensor."""
    pass

def relu(X: Tensor) -> Tensor:
    """Apply ReLU element-wise."""
    pass

def tanh(X: Tensor) -> Tensor:
    """Apply tanh element-wise."""
    pass

def outer(u: Tensor, v: Tensor) -> Tensor:
    """Outer product: u[i] * v[j]."""
    pass
```

### 2c. Kernel / JIT System

The Layer 2 runtime can:
- Detect chains of operations
- Fuse them into single GPU kernels
- Choose CPU vs GPU vs NPU based on size
- Manage buffer layouts and memory efficiency

```python
class KernelCache:
    """JIT compilation cache."""
    def compile_op_chain(ops: list[str], shapes: list[tuple]) -> kernel_id:
        """Compile sequence of ops into single kernel."""
        pass

def fused_op(ops_and_args: list[tuple], use_device: str = 'auto') -> Tensor:
    """Execute fused operation sequence, auto-choosing device."""
    pass
```

**API upward:**
Layers 3+ never think about hardware. They just call `add()`, `matmul()`, `relu()`, etc., and Layer 2 handles whether it's CPU, GPU, or split across devices.

---

## Layer 3: State / Time / Graph Engine

**Purpose:**
A generic dynamical systems simulator. Defines stateful units, connections between them, time evolution, and scheduling.

**Built on:** Layers 1–2.

**Core concepts:**

### 3a. Unit (Stateful Computation Node)

A **Unit** is:
- Some **state** (a set of Tensors)
- An **update function** that takes state + inputs → new state + outputs
- No predefined semantics (could be neuron, integrate-and-fire, Hodgkin-Huxley, etc.)

```python
class Unit:
    """Base class for any stateful computational node."""

    def __init__(self, unit_type: str, params: dict):
        self.unit_type = unit_type
        self.state = {}  # Dict of Tensors (neuron_id -> voltage, etc.)
        self.params = params

    def update(self, dt: float, inputs: dict[str, Tensor]) -> dict[str, Tensor]:
        """Advance state by dt.
        inputs: dict of signal names → values from connected units.
        returns: dict of output names → output values."""
        pass
```

### 3b. Connection (Signal Routing)

A **Connection** links one unit's outputs to another unit's inputs.

```python
class Connection:
    """Directed link from source unit to target unit."""

    def __init__(self, source_unit: Unit, target_unit: Unit,
                 source_output: str, target_input: str,
                 weight_matrix: Tensor = None):
        self.source = source_unit
        self.target = target_unit
        self.source_output = source_output
        self.target_input = target_input
        self.weights = weight_matrix  # Optional synaptic weight

    def transmit(self) -> Tensor:
        """Get output from source, apply weight, return."""
        output = self.source.state[self.source_output]
        if self.weights is not None:
            output = matmul(output, self.weights)
        return output
```

### 3c. Graph (Collection of Units + Connections)

```python
class Graph:
    """A dynamical system: units + connections + scheduler."""

    def __init__(self):
        self.units = {}  # unit_id -> Unit
        self.connections = []  # List of Connection
        self.time = 0.0
        self.history = []  # Optional: record trajectory

    def add_unit(self, unit_id: str, unit: Unit) -> None:
        self.units[unit_id] = unit

    def add_connection(self, conn: Connection) -> None:
        self.connections.append(conn)

    def step(self, dt: float, external_inputs: dict = None) -> None:
        """Update all units once by dt.
        external_inputs: dict of unit_id -> {input_name -> value}."""

        if external_inputs is None:
            external_inputs = {}

        # Gather inputs to each unit from connections
        unit_inputs = {uid: {} for uid in self.units}
        for conn in self.connections:
            signal = conn.transmit()
            unit_inputs[conn.target.id][conn.target_input] = signal

        # Merge external inputs
        for uid, ext_in in external_inputs.items():
            unit_inputs[uid].update(ext_in)

        # Update all units
        for uid, unit in self.units.items():
            unit.update(dt, unit_inputs[uid])

        self.time += dt

    def get_state(self, unit_id: str, state_var: str) -> Tensor:
        """Read a unit's state variable."""
        return self.units[unit_id].state[state_var]

    def set_state(self, unit_id: str, state_var: str, value: Tensor) -> None:
        """Manually set a unit's state."""
        self.units[unit_id].state[state_var] = value
```

**Why this layer is generic:**
- It knows nothing about neurons, spikes, or dendrites.
- Any system of ODEs → Graph.
- Neuromorphic, dynamical, recurrent, differentiable, spiking—all expressible as Units and Connections.

**API upward:**
Layers 4+ build specific unit types and networks on top of this.

---

## Layer 4: Genome / Development Specification

**Purpose:**
Define the blueprint for the brain structure—not the dynamics, but the shape, wiring, and initial parameters.

**Conceptually:** This is "DNA" for the brain.

**Built on:** Layers 1–3 (mainly 3).

**What it specifies:**

### 4a. Brain Anatomy

```yaml
# Pseudocode: YAML-like genome file
brain:
  areas:
    visual_cortex:
      subregions:
        - name: V1
          layers: 6  # Standard cortical layers 1-6
          size: 256  # neurons per layer per "hypercolumn"

        - name: V2
          layers: 6
          size: 128

    language:
      subregions:
        - name: pSTG
          layers: 6
          size: 512

        - name: MTG
          layers: 6
          size: 512

        - name: STS
          layers: 6
          size: 512
```

### 4b. Neuron Type Distribution

```yaml
  neuron_types:
    pyramidal:
      fraction: 0.8
      params:
        soma_capacitance: 100.0  # pF
        soma_leak: 0.1  # nS
        num_dendritic_branches: 5

    parvalbumin_interneuron:
      fraction: 0.15
      params:
        soma_capacitance: 50.0
        num_dendritic_branches: 3

    somatostatin_interneuron:
      fraction: 0.04
      params:
        soma_capacitance: 75.0
        dendritic_target: "apical"  # Targets apical dendrites

    vip_interneuron:
      fraction: 0.01
      params:
        soma_capacitance: 60.0
        axonal_target: "sst_soma"  # Disinhibits by targeting SST
```

### 4c. Microcircuit Motifs (Templates)

```yaml
  motifs:
    canonical_thalamocortical:
      description: "Classic feedforward + recurrent motif"
      neurons:
        - type: pyramidal
          count: 100

        - type: parvalbumin_interneuron
          count: 20

        - type: somatostatin_interneuron
          count: 5

      connections:
        - from: "thalamic_input"
          to: "pyramidal"
          weight_dist: "normal(0.5, 0.1)"
          synapse_type: "AMPA"

        - from: "pyramidal"
          to: "pyramidal"
          weight_dist: "normal(0.3, 0.15)"
          synapse_type: "NMDA+AMPA"

        - from: "pyramidal"
          to: "pv_interneuron"
          weight_dist: "normal(0.8, 0.1)"
          synapse_type: "AMPA"

        - from: "pv_interneuron"
          to: "pyramidal"
          weight_dist: "normal(-1.0, 0.1)"  # Negative = inhibitory
          synapse_type: "GABA"
```

### 4d. Growth Rules (Connectivity Generation)

```yaml
  growth_rules:

    # Connection probability based on distance
    distance_dependent:
      formula: "p(distance) = exp(-distance^2 / lambda^2)"
      lambda: 0.5  # mm, characteristic length
      max_distance: 5.0  # mm

    # Laminar specificity
    laminar_targets:
      layer_4:
        receives_from: ["thalamus"]
        projects_to: ["layer_2_3"]

      layer_2_3:
        receives_from: ["layer_4", "layer_2_3"]
        projects_to: ["layer_5", "layer_1"]

      layer_5:
        receives_from: ["layer_2_3", "layer_5"]
        projects_to: ["subcortical", "layer_6"]

      layer_6:
        receives_from: ["layer_5"]
        projects_to: ["thalamus"]
```

### 4e. Plasticity Defaults

```yaml
  plasticity:
    stdp:
      tau_plus: 20.0  # ms
      tau_minus: 20.0  # ms
      a_plus: 0.01
      a_minus: -0.01

    dopamine_modulation:
      learning_rate_scale: 0.1  # If dopamine > baseline

    hebbian:
      learning_rate: 0.001
```

### 4f. API

```python
class Genome:
    """Load and manage the brain blueprint."""

    def __init__(self, genome_file: str):
        self.data = load_yaml(genome_file)  # Or JSON

    def get_area_spec(self, area_name: str) -> dict:
        """Return spec for an area."""
        pass

    def get_subregion_spec(self, area: str, subregion: str) -> dict:
        """Return spec for a subregion."""
        pass

    def get_neuron_distribution(self, region: str) -> dict:
        """Return neuron type mix for region."""
        pass

    def get_motif_template(self, motif_name: str) -> dict:
        """Return template for a microcircuit motif."""
        pass

    def get_connectivity_rule(self, source_region: str, target_region: str) -> callable:
        """Return a function(source_locs, target_locs) -> connection_list."""
        pass
```

**Why Layer 4 is separate:**
- Specifies structure, not dynamics.
- Can be evolved, regenerated, or replaced.
- Decouples "what should the brain look like" from "how does it run".

---

## Layer 5: Dendritic Subunit Model

**Purpose:**
The smallest local computing units: nonlinear functions on dendritic branches.

**Built on:** Layers 1–4 (mainly 3: uses Graph/Unit).

**What it is:**

A single dendritic subunit is a **Unit** (Layer 3) with:
- Local inputs (synapses on one branch)
- A nonlinear integration function
- Local plasticity rule
- Output to soma

### 5a. Subunit Types

```python
class DendriticSubunit(Unit):
    """A dendritic branch or compartment."""

    def __init__(self, unit_type: str, num_synapses: int, params: dict):
        super().__init__(unit_type, params)

        # State variables
        self.state['voltage'] = tensor([0.0] * num_synapses)  # Synaptic inputs
        self.state['Ca'] = tensor([0.0])  # Calcium for plasticity

        # Synaptic weights
        self.weights = tensor_alloc((num_synapses,), 'float32', 'cpu')
        tensor_write(self.weights, numpy.ones(num_synapses) * 0.5)

    def update(self, dt, inputs):
        """Integration rule for this branch."""

        if self.unit_type == 'excitatory_feedforward':
            # Simple: weighted sum + ReLU
            input_signals = inputs['synaptic_input']  # [num_synapses]
            weighted = mul(input_signals, self.weights)
            output = relu(sum(weighted))

        elif self.unit_type == 'saturating':
            # Sublinear: divides by norm (models voltage ceiling)
            input_signals = inputs['synaptic_input']
            weighted = mul(input_signals, self.weights)
            norm_val = norm(weighted)
            output = weighted / (1.0 + 0.1 * norm_val)

        elif self.unit_type == 'multiplicative_gate':
            # Signal * gate
            signal = inputs['signal']  # Feedforward
            gate = inputs['gate']  # Modulating input
            gate_out = sigmoid(gate)  # Gate to [0, 1]
            output = mul(signal, gate_out)

        elif self.unit_type == 'predictive':
            # Top-down prediction error
            prediction = inputs['prediction']
            reality = inputs['bottom_up']
            output = prediction - reality  # Signed error

        self.state['voltage'] = output

        # Calcium accumulation (for plasticity)
        self.state['Ca'] = output  # Simplified: Ca follows voltage

        return {'output': output}
```

### 5b. Plasticity Rules (Local)

```python
def hebbian_update(subunit: DendriticSubunit, learning_rate: float):
    """Strengthens weights that co-activate with output."""
    output = subunit.state['voltage']
    inputs = subunit.state['synaptic_input']  # [num_synapses]

    # dW ∝ output * input
    dW = learning_rate * outer(output, inputs)
    subunit.weights += dW

def predictive_error_update(subunit: DendriticSubunit, learning_rate: float):
    """Adjusts weights to minimize prediction error."""
    output = subunit.state['voltage']  # error signal
    inputs = subunit.state['synaptic_input']

    dW = learning_rate * output * inputs
    subunit.weights += dW

def stdp_update(subunit: DendriticSubunit, presynaptic_spikes: Tensor,
                postsynaptic_voltage: float, tau_plus: float, tau_minus: float):
    """STDP: weight change depends on timing between pre and post."""
    # Simplified: if pre before post, strengthen; if after, weaken
    delta_t = postsynaptic_voltage - presynaptic_spikes  # Approximation

    ltp = exp(-abs(delta_t) / tau_plus) * (delta_t > 0)
    ltd = exp(-abs(delta_t) / tau_minus) * (delta_t < 0)

    dW = (ltp - ltd) * presynaptic_spikes
    subunit.weights += dW
```

**Key insight:** Dendritic subunits are composable, reusable, locally plastic Units.

---

## Layer 6: Neuron Type Layer

**Purpose:**
Compose dendritic subunits into specific neuron types (pyramidal, PV+, SST+, VIP+, etc.).

**Built on:** Layers 3–5.

**What it is:**

A neuron is a Graph (Layer 3) containing:
- Multiple dendritic subunits (Layer 5)
- A soma (integration unit)
- An axon (firing logic)

### 6a. Neuron Class

```python
class NeuronType(Unit):
    """Composite unit: dendrites + soma + axon."""

    def __init__(self, neuron_type_id: str, morphology: dict, plasticity_rules: list):
        super().__init__(f"neuron_{neuron_type_id}", {})

        self.neuron_type = neuron_type_id
        self.morphology = morphology  # Number of branches, type, etc.
        self.plasticity_rules = plasticity_rules

        # Build internal graph
        self.internal_graph = Graph()
        self._build_dendritic_tree()

    def _build_dendritic_tree(self):
        """Instantiate dendritic subunits based on morphology."""

        num_branches = self.morphology.get('num_branches', 5)

        # Create dendritic subunits
        for i in range(num_branches):
            subunit = DendriticSubunit(
                unit_type='excitatory_feedforward',
                num_synapses=50,
                params=self.morphology
            )
            self.internal_graph.add_unit(f'dend_{i}', subunit)

        # Create soma (integration unit)
        soma = Unit('soma', {})
        soma.state['voltage'] = tensor([0.0])
        soma.update = self._soma_integrate
        self.internal_graph.add_unit('soma', soma)

        # Create axon (firing)
        axon = Unit('axon', {})
        axon.state['spike'] = tensor([0.0])
        axon.update = self._axon_fire
        self.internal_graph.add_unit('axon', axon)

        # Wire dendrites → soma
        for i in range(num_branches):
            conn = Connection(
                source_unit=self.internal_graph.units[f'dend_{i}'],
                target_unit=self.internal_graph.units['soma'],
                source_output='output',
                target_input=f'dend_input_{i}'
            )
            self.internal_graph.add_connection(conn)

        # Wire soma → axon
        conn = Connection(
            source_unit=self.internal_graph.units['soma'],
            target_unit=self.internal_graph.units['axon'],
            source_output='voltage',
            target_input='soma_voltage'
        )
        self.internal_graph.add_connection(conn)

    def _soma_integrate(self, dt, inputs):
        """Integration rule for soma."""
        # Collect dendritic inputs
        total = tensor([0.0])
        for i in range(self.morphology['num_branches']):
            key = f'dend_input_{i}'
            if key in inputs:
                total += inputs[key]

        # Leaky integration
        tau = 10.0  # ms
        self.state['voltage'] += dt / tau * (total - self.state['voltage'])

        return {'voltage': self.state['voltage']}

    def _axon_fire(self, dt, inputs):
        """Firing rule for axon."""
        soma_voltage = inputs.get('soma_voltage', tensor([0.0]))
        threshold = 20.0

        # Generate spike if threshold exceeded
        if soma_voltage > threshold:
            self.state['spike'] = tensor([1.0])
        else:
            self.state['spike'] = tensor([0.0])

        return {'spike': self.state['spike']}

    def update(self, dt, external_inputs):
        """Step the neuron: update internal dynamics."""

        # Prepare inputs for dendritic subunits
        internal_inputs = {}
        for i in range(self.morphology['num_branches']):
            internal_inputs[f'dend_{i}'] = {
                'synaptic_input': external_inputs.get(f'syn_{i}', tensor([0.0]))
            }

        # Add soma inputs (will be filled by connections)
        internal_inputs['soma'] = {}
        internal_inputs['axon'] = {}

        # Step internal graph
        self.internal_graph.step(dt, internal_inputs)

        # Copy state from internal graph
        self.state['voltage'] = self.internal_graph.get_state('soma', 'voltage')
        self.state['spike'] = self.internal_graph.get_state('axon', 'spike')

        # Apply plasticity rules
        for rule_type in self.plasticity_rules:
            if rule_type == 'hebbian':
                for i in range(self.morphology['num_branches']):
                    dend = self.internal_graph.units[f'dend_{i}']
                    hebbian_update(dend, learning_rate=0.001)

        return {
            'spike': self.state['spike'],
            'voltage': self.state['voltage']
        }

# Specific neuron type implementations

class PyramidalNeuron(NeuronType):
    def __init__(self):
        super().__init__(
            neuron_type_id='pyramidal',
            morphology={
                'num_branches': 5,
                'soma_capacitance': 100.0,
                'soma_leak': 0.1
            },
            plasticity_rules=['hebbian', 'stdp']
        )

class ParvalbumiInterneuron(NeuronType):
    def __init__(self):
        super().__init__(
            neuron_type_id='pv_interneuron',
            morphology={
                'num_branches': 3,
                'soma_capacitance': 50.0,
                'fast_kinetics': True
            },
            plasticity_rules=['stdp']
        )

class SomatostatinInterneuron(NeuronType):
    def __init__(self):
        super().__init__(
            neuron_type_id='sst_interneuron',
            morphology={
                'num_branches': 4,
                'dendritic_target': 'apical'
            },
            plasticity_rules=['hebbian']
        )
```

**Key:** Each neuron type is composed of subunits + integration logic, all expressible in the Layer 3 Graph/Unit formalism.

---

## Layer 7: Microcircuit Motif Layer

**Purpose:**
Define reusable "algorithms" built from neuron types.

**Built on:** Layers 3–6.

**What they are:**

Motifs are small graph templates: a stereotyped wiring pattern with specific neuron types.

### 7a. Motif Examples

```python
class Motif(Graph):
    """Base class for microcircuit motifs."""

    def __init__(self, motif_type: str, params: dict):
        super().__init__()
        self.motif_type = motif_type
        self.params = params
        self._instantiate()

    def _instantiate(self):
        """Override in subclass to build the motif."""
        pass

class CanonicalThalamocortical(Motif):
    """Classic E→I→E feedforward + recurrent motif."""

    def _instantiate(self):
        num_exc = self.params.get('num_excitatory', 100)
        num_inh = self.params.get('num_inhibitory', 20)

        # Create excitatory neurons
        for i in range(num_exc):
            neuron = PyramidalNeuron()
            self.add_unit(f'exc_{i}', neuron)

        # Create inhibitory neurons
        for i in range(num_inh):
            neuron = ParvalbumiInterneuron()
            self.add_unit(f'inh_{i}', neuron)

        # E ← thalamic input
        for i in range(num_exc):
            # External connection (filled during step)
            pass

        # E → E (recurrent, weak)
        for i in range(num_exc):
            for j in range(num_exc):
                if i != j and random.random() < 0.1:
                    weight = tensor_alloc((1,), 'float32', 'cpu')
                    tensor_write(weight, numpy.array([0.3]))
                    conn = Connection(
                        self.units[f'exc_{i}'],
                        self.units[f'exc_{j}'],
                        'spike',
                        'syn_excitatory',
                        weight
                    )
                    self.add_connection(conn)

        # E → I (strong)
        for i in range(num_exc):
            for j in range(num_inh):
                if random.random() < 0.3:
                    weight = tensor_alloc((1,), 'float32', 'cpu')
                    tensor_write(weight, numpy.array([0.8]))
                    conn = Connection(
                        self.units[f'exc_{i}'],
                        self.units[f'inh_{j}'],
                        'spike',
                        'syn_excitatory',
                        weight
                    )
                    self.add_connection(conn)

        # I → E (strong inhibition)
        for i in range(num_inh):
            for j in range(num_exc):
                if random.random() < 0.5:
                    weight = tensor_alloc((1,), 'float32', 'cpu')
                    tensor_write(weight, numpy.array([-1.0]))
                    conn = Connection(
                        self.units[f'inh_{i}'],
                        self.units[f'exc_{j}'],
                        'spike',
                        'syn_inhibitory',
                        weight
                    )
                    self.add_connection(conn)

class WinnerTakeAll(Motif):
    """Competitive dynamics: strongest input wins."""

    def _instantiate(self):
        num_units = self.params.get('num_units', 10)

        # Create excitatory neurons
        for i in range(num_units):
            neuron = PyramidalNeuron()
            self.add_unit(f'unit_{i}', neuron)

        # All-to-all inhibition (strong)
        for i in range(num_units):
            for j in range(num_units):
                if i != j:
                    weight = tensor_alloc((1,), 'float32', 'cpu')
                    tensor_write(weight, numpy.array([-2.0]))
                    conn = Connection(
                        self.units[f'unit_{i}'],
                        self.units[f'unit_{j}'],
                        'spike',
                        'syn_inhibitory',
                        weight
                    )
                    self.add_connection(conn)

class PredictiveCodingLoop(Motif):
    """Feedforward + feedback for error correction."""

    def _instantiate(self):
        # Feedforward layer
        ff_neurons = [PyramidalNeuron() for _ in range(50)]
        for i, n in enumerate(ff_neurons):
            self.add_unit(f'ff_{i}', n)

        # Feedback layer
        fb_neurons = [PyramidalNeuron() for _ in range(50)]
        for i, n in enumerate(fb_neurons):
            self.add_unit(f'fb_{i}', n)

        # FF → FB (prediction)
        for i in range(50):
            for j in range(50):
                weight = tensor_alloc((1,), 'float32', 'cpu')
                tensor_write(weight, numpy.random.randn(1) * 0.1)
                conn = Connection(
                    self.units[f'ff_{i}'],
                    self.units[f'fb_{j}'],
                    'voltage',
                    'syn_predicted',
                    weight
                )
                self.add_connection(conn)

class AttractorPool(Motif):
    """Recurrent network that settles to learned patterns."""

    def _instantiate(self):
        # All excitatory, all-to-all with learned weights
        num_neurons = self.params.get('num_neurons', 100)

        for i in range(num_neurons):
            neuron = PyramidalNeuron()
            self.add_unit(f'neuron_{i}', neuron)

        # Dense recurrent connectivity
        for i in range(num_neurons):
            for j in range(num_neurons):
                weight = tensor_alloc((1,), 'float32', 'cpu')
                # Initialized from learned Hopfield-like weights
                init_val = 0.05 if i != j else 0.0
                tensor_write(weight, numpy.array([init_val]))
                conn = Connection(
                    self.units[f'neuron_{i}'],
                    self.units[f'neuron_{j}'],
                    'spike',
                    'syn_recurrent',
                    weight
                )
                self.add_connection(conn)
```

**Key library of motifs:**
- Feedforward + inhibition
- Winner-take-all
- Attractor networks
- Predictive coding loops
- Lateral inhibition
- Thalamocortical relay
- And more (customizable)

---

## Layer 8: Cortical Layer (1–6) / Laminar Structure

**Purpose:**
Assemble microcircuit motifs into a full 6-layer cortical stack within a subregion.

**Built on:** Layers 3–7.

**What it does:**

Each cortical layer (L1–L6) has:
- Specific neuron type mix (from Genome, Layer 4)
- Specific microcircuits (from motifs, Layer 7)
- Specific connectivity between layers

### 8a. Layer Class

```python
class CorticalLayer(Graph):
    """A single cortical layer within a subregion."""

    def __init__(self, layer_id: int, subregion: str, neuron_counts: dict,
                 motif_config: dict):
        super().__init__()

        self.layer_id = layer_id
        self.subregion = subregion
        self.neuron_counts = neuron_counts
        self.motif_config = motif_config

        self._build_layer()

    def _build_layer(self):
        """Instantiate neurons and microcircuits for this layer."""

        # Layer 1: Mostly inhibitory, sparse
        if self.layer_id == 1:
            self._build_layer_1()

        # Layer 2/3: Main computation, pyramidal cells
        elif self.layer_id in [2, 3]:
            self._build_layer_23()

        # Layer 4: Thalamic input relay
        elif self.layer_id == 4:
            self._build_layer_4()

        # Layer 5: Large pyramidals, subcortical output
        elif self.layer_id == 5:
            self._build_layer_5()

        # Layer 6: Thalamic feedback
        elif self.layer_id == 6:
            self._build_layer_6()

    def _build_layer_1(self):
        """Layer 1: sparse, mostly inhibitory."""
        num_vip = self.neuron_counts.get('vip', 5)

        for i in range(num_vip):
            neuron = VIPInterneuron()
            self.add_unit(f'vip_{i}', neuron)

    def _build_layer_23(self):
        """Layer 2/3: main pyramidal computation + local inhibition."""
        num_pyr = self.neuron_counts.get('pyramidal', 100)
        num_pv = self.neuron_counts.get('pv', 20)
        num_sst = self.neuron_counts.get('sst', 5)

        # Pyramidal neurons
        for i in range(num_pyr):
            neuron = PyramidalNeuron()
            self.add_unit(f'pyr_{i}', neuron)

        # PV+ interneurons (fast somatic inhibition)
        for i in range(num_pv):
            neuron = ParvalbumiInterneuron()
            self.add_unit(f'pv_{i}', neuron)

        # SST+ interneurons (dendritic inhibition)
        for i in range(num_sst):
            neuron = SomatostatinInterneuron()
            self.add_unit(f'sst_{i}', neuron)

        # Canonical microcircuit: E→I→E
        motif = CanonicalThalamocortical({
            'num_excitatory': num_pyr,
            'num_inhibitory': num_pv + num_sst
        })
        # Merge motif into this layer
        self._merge_motif(motif)

    def _build_layer_4(self):
        """Layer 4: thalamic input, relay through stellate."""
        num_stellate = self.neuron_counts.get('stellate', 50)

        for i in range(num_stellate):
            neuron = PyramidalNeuron()  # Simplified: use pyramidal
            self.add_unit(f'stellate_{i}', neuron)

    def _build_layer_5(self):
        """Layer 5: large pyramidals, projects to subcortical regions."""
        num_large_pyr = self.neuron_counts.get('pyramidal', 80)

        for i in range(num_large_pyr):
            neuron = PyramidalNeuron()
            self.add_unit(f'pyr_5_{i}', neuron)

    def _build_layer_6(self):
        """Layer 6: projects back to thalamus."""
        num_pyr_6 = self.neuron_counts.get('pyramidal', 60)

        for i in range(num_pyr_6):
            neuron = PyramidalNeuron()
            self.add_unit(f'pyr_6_{i}', neuron)

    def _merge_motif(self, motif: Motif):
        """Integrate a motif's units and connections into this layer."""
        for uid, unit in motif.units.items():
            self.add_unit(uid, unit)
        for conn in motif.connections:
            self.add_connection(conn)

    def connect_to_layer(self, pre_layer: 'CorticalLayer', rule: dict):
        """Connect this layer to another layer."""
        # rule specifies probability, weight distribution, etc.

        pre_neurons = list(pre_layer.units.keys())
        post_neurons = list(self.units.keys())

        for pre_id in pre_neurons:
            for post_id in post_neurons:
                if random.random() < rule.get('connection_probability', 0.1):
                    weight = tensor_alloc((1,), 'float32', 'cpu')
                    weight_val = numpy.random.normal(
                        rule.get('mean_weight', 0.3),
                        rule.get('std_weight', 0.1)
                    )
                    tensor_write(weight, numpy.array([weight_val]))

                    conn = Connection(
                        pre_layer.units[pre_id],
                        self.units[post_id],
                        'spike',
                        'syn_external',
                        weight
                    )
                    self.add_connection(conn)
```

**API:**
```python
# Create a full 6-layer stack
layers = []
for layer_id in range(1, 7):
    layer = CorticalLayer(
        layer_id=layer_id,
        subregion='pSTG',
        neuron_counts=genome.get_neuron_distribution('pSTG'),
        motif_config={'type': 'canonical_thalamocortical'}
    )
    layers.append(layer)

# Connect layers
for i in range(len(layers) - 1):
    layers[i].connect_to_layer(layers[i+1], rule={'connection_probability': 0.2})
```

---

## Layer 9: Subregion Layer (pSTG, MTG, STS, etc.)

**Purpose:**
Combine laminar stacks into functionally distinct subregions.

**Built on:** Layers 3–8.

### 9a. Subregion Class

```python
class Subregion(Graph):
    """A distinct subregion (pSTG, MTG, V1, etc.)."""

    def __init__(self, name: str, area: str, genome: Genome):
        super().__init__()

        self.name = name
        self.area = area
        self.genome = genome

        self.layers = []
        self._build_subregion()

    def _build_subregion(self):
        """Instantiate 6 layers + inter-layer connectivity."""

        spec = self.genome.get_subregion_spec(self.area, self.name)
        neuron_dist = self.genome.get_neuron_distribution(self.name)

        # Build layers 1–6
        for layer_id in range(1, 7):
            layer = CorticalLayer(
                layer_id=layer_id,
                subregion=self.name,
                neuron_counts=neuron_dist.get(f'layer_{layer_id}', {}),
                motif_config=spec.get(f'layer_{layer_id}_motifs', {})
            )
            self.layers.append(layer)

            # Merge layer into subregion graph
            for uid, unit in layer.units.items():
                self.add_unit(f'L{layer_id}_{uid}', unit)
            for conn in layer.connections:
                self.add_connection(conn)

        # Connect layers to each other
        # Standard: L4 ← thalamus, L4 → L2/3, L2/3 → L5, L5 → L6, L6 → thalamus

        # L4 → L2/3
        self.layers[1].connect_to_layer(self.layers[3], {
            'connection_probability': 0.3,
            'mean_weight': 0.5
        })

        # L2/3 → L5
        self.layers[1].connect_to_layer(self.layers[4], {
            'connection_probability': 0.2,
            'mean_weight': 0.4
        })

        # L5 → L6
        self.layers[4].connect_to_layer(self.layers[5], {
            'connection_probability': 0.25,
            'mean_weight': 0.3
        })
```

---

## Layer 10: Brain Area Layer (V1, Broca, Wernicke, etc.)

**Purpose:**
Group subregions into named anatomical/functional areas.

**Built on:** Layers 3–9.

### 10a. Area Class

```python
class BrainArea(Graph):
    """A complete brain area (V1, Wernicke, etc.)."""

    def __init__(self, name: str, genome: Genome):
        super().__init__()

        self.name = name
        self.genome = genome
        self.subregions = {}

        self._build_area()

    def _build_area(self):
        """Build all subregions within this area."""
        area_spec = self.genome.get_area_spec(self.name)

        for subregion_name in area_spec.get('subregions', []):
            subregion = Subregion(subregion_name, self.name, self.genome)
            self.subregions[subregion_name] = subregion

            # Merge into area
            for uid, unit in subregion.units.items():
                self.add_unit(f'{subregion_name}_{uid}', unit)
            for conn in subregion.connections:
                self.add_connection(conn)
```

---

## Layer 11: Pathway / Network Layer

**Purpose:**
Wire brain areas into systems (visual stream, language pathway, motor control, etc.).

**Built on:** Layers 3–10.

### 11a. Pathway Class

```python
class Pathway(Graph):
    """A network of connected brain areas."""

    def __init__(self, name: str, areas: list[BrainArea], routing_rules: dict):
        super().__init__()

        self.name = name
        self.areas = {area.name: area for area in areas}
        self.routing_rules = routing_rules

        # Merge all areas into pathway
        for area in areas:
            for uid, unit in area.units.items():
                self.add_unit(f'{area.name}_{uid}', unit)
            for conn in area.connections:
                self.add_connection(conn)

        # Apply inter-area connections
        self._wire_areas()

    def _wire_areas(self):
        """Create connections between areas based on routing rules."""

        for (source_area, target_area), rule in self.routing_rules.items():
            source = self.areas[source_area]
            target = self.areas[target_area]

            # Connect output neurons of source to input neurons of target
            # (Simplified: probabilistic all-to-all)

            source_neurons = list(source.units.keys())
            target_neurons = list(target.units.keys())

            for src_id in source_neurons[:min(100, len(source_neurons))]:
                for tgt_id in target_neurons[:min(100, len(target_neurons))]:
                    if random.random() < rule.get('connection_probability', 0.05):
                        weight = tensor_alloc((1,), 'float32', 'cpu')
                        weight_val = numpy.random.normal(0.2, 0.1)
                        tensor_write(weight, numpy.array([weight_val]))

                        conn = Connection(
                            source.units[src_id],
                            target.units[tgt_id],
                            'spike',
                            'syn_pathway',
                            weight
                        )
                        self.add_connection(conn)
```

---

## Layer 12: Global Workspace / Attention

**Purpose:**
Provide a shared "board" where selected information is integrated and broadcast.

**Built on:** Layers 3–11.

### 12a. GlobalWorkspace Class

```python
class GlobalWorkspace(Graph):
    """Central attentional hub: competition + broadcast."""

    def __init__(self, capacity: int = 10):
        super().__init__()

        self.capacity = capacity
        self.sources = {}  # source_id -> (area, neurons)
        self.current_focus = None
        self.broadcast_state = {}

        # Create workspace neurons (one per content item)
        for i in range(capacity):
            neuron = PyramidalNeuron()
            self.add_unit(f'workspace_{i}', neuron)

    def register_source(self, source_id: str, area: BrainArea, neurons: list):
        """Register a source of information."""
        self.sources[source_id] = {'area': area, 'neurons': neurons}

    def update(self, dt, external_inputs):
        """Update workspace: competition + broadcast."""

        # Read activations from registered sources
        activations = {}
        for source_id, spec in self.sources.items():
            neuron_activities = [
                spec['area'].units[nid].state.get('spike', tensor([0.0]))
                for nid in spec['neurons']
            ]
            activations[source_id] = sum(neuron_activities) / len(spec['neurons'])

        # Winner-take-all: highest activation broadcasts
        if activations:
            self.current_focus = max(activations, key=activations.get)
            self.broadcast_state = activations[self.current_focus]

        # Broadcast to all areas
        # (In full implementation, this would modulate learning rates, attention, etc.)

        super().update(dt, external_inputs)
```

---

## Layer 13: Executive / Controller

**Purpose:**
High-level decision-making, goal-setting, planning.

**Built on:** Layers 3–12.

### 13a. ExecutiveController Class

```python
class ExecutiveController(Graph):
    """Decision-making and task control."""

    def __init__(self, prefrontal: BrainArea, basal_ganglia: BrainArea,
                 workspace: GlobalWorkspace):
        super().__init__()

        self.prefrontal = prefrontal
        self.basal_ganglia = basal_ganglia
        self.workspace = workspace

        self.current_goal = None
        self.working_memory = {}
        self.task_representation = None

    def set_goal(self, goal_repr: Tensor):
        """Set a high-level goal."""
        self.current_goal = goal_repr
        self.task_representation = goal_repr

    def propose_action(self) -> Tensor:
        """Propose next action based on goal + workspace content."""

        if self.current_goal is None:
            return tensor([0.0])  # No action

        # Simplified: use workspace focus + goal to select action
        workspace_content = self.workspace.broadcast_state
        action = matmul(self.task_representation, workspace_content)

        return action

    def update(self, dt, external_inputs):
        """Update executive state."""

        # Merge prefrontal + basal ganglia updates
        # (In full implementation, this would include working memory updates,
        #  reward prediction, action selection, etc.)

        super().update(dt, external_inputs)
```

---

## Layer 14: Meta-Cognition / Self-Model

**Purpose:**
Think about itself: introspect, adjust strategies, build self-model.

**Built on:** Layers 3–13.

### 14a. MetaCognition Class

```python
class MetaCognition(Graph):
    """Self-awareness and strategy adjustment."""

    def __init__(self, controller: ExecutiveController, workspace: GlobalWorkspace):
        super().__init__()

        self.controller = controller
        self.workspace = workspace

        self.internal_model = {}
        self.performance_history = []
        self.error_signals = []

    def introspect(self) -> dict:
        """Summarize internal state."""
        return {
            'current_goal': self.controller.current_goal,
            'workspace_focus': self.workspace.current_focus,
            'recent_errors': self.error_signals[-10:],
            'task_performance': self._compute_performance()
        }

    def adjust_policies(self, meta_info: dict):
        """Adjust learning rates, exploration, etc. based on performance."""

        performance = meta_info.get('performance', 0.5)

        if performance < 0.3:
            # Struggling: increase exploration
            print("Meta-cognition: increasing exploration")
        elif performance > 0.8:
            # Succeeding: reduce exploration, refine
            print("Meta-cognition: reducing exploration, refining")

    def _compute_performance(self) -> float:
        """Aggregate performance measure."""
        if not self.performance_history:
            return 0.5
        return sum(self.performance_history[-10:]) / min(10, len(self.performance_history))

    def log_error(self, error: float):
        """Log an error signal."""
        self.error_signals.append(error)

    def update(self, dt, external_inputs):
        """Update self-model."""

        meta_info = self.introspect()
        self.adjust_policies(meta_info)

        super().update(dt, external_inputs)
```

---

## Layer 15: Cognitive / Behavioral Loop

**Purpose:**
The top-level loop that runs the organism.

**Built on:** Layers 0–14.

### 15a. Main Loop

```python
class BioAISystem:
    """Complete cognitive system from sensor to motor."""

    def __init__(self, hardware_bridge, genome_file: str):
        self.hardware = hardware_bridge
        self.genome = Genome(genome_file)

        # Build all layers
        print("Building brain...")

        # Layers 5–11: Build neural systems
        self.visual_area = BrainArea('V1', self.genome)
        self.language_area = BrainArea('Wernicke', self.genome)
        self.prefrontal = BrainArea('PFC', self.genome)
        self.basal_ganglia = BrainArea('BG', self.genome)

        # Layer 11: Wire into pathways
        self.visual_pathway = Pathway('visual', [self.visual_area], {})
        self.language_pathway = Pathway(
            'language',
            [self.language_area],
            {}
        )

        # Layer 12: Global workspace
        self.workspace = GlobalWorkspace(capacity=20)

        # Layer 13: Executive
        self.executive = ExecutiveController(
            self.prefrontal,
            self.basal_ganglia,
            self.workspace
        )

        # Layer 14: Meta-cognition
        self.meta = MetaCognition(self.executive, self.workspace)

        # Merge all into one big graph
        self.brain = Graph()
        for area in [self.visual_area, self.language_area, self.prefrontal, self.basal_ganglia]:
            for uid, unit in area.units.items():
                self.brain.add_unit(f'area_{uid}', unit)
            for conn in area.connections:
                self.brain.add_connection(conn)

        print(f"Brain built: {len(self.brain.units)} neurons")

    def run(self, max_steps: int = 10000):
        """Main cognitive loop."""

        for step in range(max_steps):
            # 1. Read sensory inputs
            sensory_data = self.hardware.read_sensors()  # bytes
            sensory_vector = self._encode_sensory(sensory_data)

            # 2. Inject into brain regions
            self._inject_sensory(sensory_vector)

            # 3. Step all dynamics
            dt = 0.001  # 1 ms
            self.brain.step(dt)
            self.workspace.update(dt, {})
            self.executive.update(dt, {})
            self.meta.update(dt, {})

            # 4. Read motor outputs
            motor_outputs = self._read_motor_outputs()

            # 5. Send to actuators
            self.hardware.write_actuators(motor_outputs)

            # 6. Optional: print progress
            if step % 100 == 0:
                print(f"Step {step}: focus={self.workspace.current_focus}, "
                      f"goal={self.executive.current_goal}")

    def _encode_sensory(self, raw_bytes: bytes) -> Tensor:
        """Convert raw sensor data to tensor."""
        # Placeholder: parse raw sensor data
        data_array = numpy.frombuffer(raw_bytes, dtype=numpy.float32)
        sensory_tensor = tensor_alloc((len(data_array),), 'float32', 'cpu')
        tensor_write(sensory_tensor, data_array)
        return sensory_tensor

    def _inject_sensory(self, sensory: Tensor):
        """Inject sensory input into appropriate brain regions."""
        # Route to visual, auditory, proprioceptive areas
        # (Simplified: just broadcast to all areas)
        self.visual_area.step(0.001, {'sensory': sensory})

    def _read_motor_outputs(self) -> bytes:
        """Read motor commands from motor areas."""
        # Collect spikes from motor neurons
        motor_neurons = [uid for uid in self.brain.units.keys() if 'motor' in uid]
        motor_spikes = [
            self.brain.get_state(uid, 'spike') for uid in motor_neurons
        ]

        # Convert to bytes
        motor_array = numpy.array(motor_spikes, dtype=numpy.float32)
        return motor_array.tobytes()

# Example: instantiate and run
if __name__ == '__main__':
    from layer_1_hardware_bridge import HardwareBridge

    bridge = HardwareBridge()  # Your hardware implementation
    system = BioAISystem(bridge, 'genome.yaml')

    print("Boot complete.")
    system.run(max_steps=10000)
```

**Pseudocode for the main loop:**

```
while alive:
    # Layer 1: Read sensors
    sensory = hardware_bridge.read_sensors()

    # Layers 5–11: Neural dynamics
    inject_into_areas(sensory)
    step_all_neurons_and_circuits(dt)

    # Layer 12: Global attention
    update_workspace(dt)

    # Layer 13: Decision-making
    action = executive.propose_action()

    # Layer 14: Self-reflection
    meta_cognition.update(dt)

    # Layer 1: Send action
    hardware_bridge.write_actuators(action)

    time += dt
```

---

## Complete Hierarchy (Summary Table)

| Layer | Name | Role | Built On | Key Classes |
|-------|------|------|----------|-------------|
| 0 | Physical Hardware | CPU, GPU, RAM, devices | Reality | None (physics) |
| 1 | Hardware Bridge | Fixed platform layer | Layer 0 | `cpu_exec`, `mem_alloc`, `gpu_run` |
| 2 | Math / Compute | Scalar & tensor ops | Layer 1 | `add`, `matmul`, `relu`, `Tensor` |
| 3 | State / Time / Graph | Generic dynamical systems | Layers 1–2 | `Unit`, `Connection`, `Graph` |
| 4 | Genome / Development | Brain blueprint (structure) | Layers 1–3 | `Genome` |
| 5 | Dendritic Subunits | Local nonlinear branches | Layers 1–4 | `DendriticSubunit` |
| 6 | Neuron Types | Composite neurons | Layers 3–5 | `PyramidalNeuron`, `ParvalbumiInterneuron` |
| 7 | Microcircuit Motifs | Reusable algorithms | Layers 3–6 | `CanonicalThalamocortical`, `WTA`, `AttractorPool` |
| 8 | Cortical Layers (1–6) | Laminar stacks | Layers 3–7 | `CorticalLayer` |
| 9 | Subregions | Functionally distinct regions | Layers 3–8 | `Subregion` |
| 10 | Brain Areas | Named regions (V1, Wernicke) | Layers 3–9 | `BrainArea` |
| 11 | Pathways / Networks | Connected area systems | Layers 3–10 | `Pathway` |
| 12 | Global Workspace | Attentional hub | Layers 3–11 | `GlobalWorkspace` |
| 13 | Executive / Controller | Decision-making | Layers 3–12 | `ExecutiveController` |
| 14 | Meta-Cognition | Self-awareness | Layers 3–13 | `MetaCognition` |
| 15 | Cognitive / Behavioral Loop | Top-level main loop | Layers 0–14 | `BioAISystem` |

---

## Design Principles

### 1. Layering
- Each layer has well-defined API boundaries.
- Upper layers depend only on the layer below's interface.
- Lower layers don't know about higher layers.

### 2. Composability
- Subunits compose into neurons.
- Neurons compose into motifs.
- Motifs compose into layers.
- Layers compose into subregions.
- Subregions compose into areas.
- Areas compose into pathways.

### 3. Flexibility
- Swap Layer 1 → run on different hardware.
- Swap Layer 4 → regenerate brain structure.
- Swap Layer 5–6 → change neuron models.
- Everything else unchanged.

### 4. Interpretability
- Each unit, synapse, connection is inspectable.
- Can read internal state, weights, error signals.
- Can visualize what each region is doing.

### 5. Biological Grounding
- Based on known anatomy (areas, layers, neuron types, microcircuits).
- Uses biologically plausible learning rules (STDP, Hebbian, neuromodulation).
- Respects constraints (compartmentalization, local plasticity, no global backprop).

---

## Next Steps

1. **Implement Layer 1** (Hardware Bridge for your specific hardware)
2. **Implement Layer 2** (Math operations, tensor backend)
3. **Implement Layer 3** (Graph Engine, Unit, Connection, Graph classes)
4. **Implement Layer 4** (Genome loader from YAML/JSON specification)
5. **Implement Layers 5–6** (Dendritic subunits and neuron types)
6. **Test with small brain** (1 area, 1 subregion, 1,000 neurons)
7. **Scale up** (Add more areas, implement full pathways)
8. **Add Layer 12+** (Workspace, executive, meta-cognition)
9. **Deploy** (Run on hardware, test real sensorimotor tasks)

---

**This is a complete operating system specification. Everything above is pseudocode/specification. Implementation follows the blueprint.**

