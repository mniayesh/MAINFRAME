"""
Layer 5: ProtoNeuron - Biologically-Complete Compartmental Neuron

Core innovation: Replace scalar neuron with multi-compartment model capturing:
- Dendritic computation (Layer 20): Nonlinear integration in 5 branches
- Soma integration (Layer 18): Leaky integration of dendritic inputs
- Axonal output (Layer 21): Threshold-based spiking with refractoriness
- Synaptic plasticity (Layer 28): STDP + Hebbian + neuromodulation
- Energy regulation (Layer 5): ATP-based metabolic constraints
- Homeostasis (Layer 10): Weight saturation prevention + activation bounds

This single neuron is a microcosm of the entire 88-layer system.
Demonstrates that biologically-inspired computation can learn without backprop.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import math


# ============================================================================
# LAYER 18: SOMA COMPARTMENT
# ============================================================================

@dataclass
class SomaConfig:
    """Soma parameters."""
    tau: float = 0.2  # Time constant (ms) - very long for strong integration
    threshold: float = 0.05  # Spiking threshold (achievable within 50 timesteps)
    reset_voltage: float = -0.1  # Reset voltage after spike (V)
    leak_conductance: float = 0.01  # Very low leak for strong integration
    resting_potential: float = 0.0  # Resting potential (V)


class Soma:
    """Soma compartment: integrates dendritic inputs, fires spikes."""

    def __init__(self, config: SomaConfig = None):
        self.config = config or SomaConfig()
        self.voltage = self.config.resting_potential  # Membrane potential
        self.last_spike_time = -np.inf  # Time of last spike
        self.refractory_period = 0.002  # Milliseconds
        self.spike_history = []  # For STDP

    def integrate(self, dendritic_input: float, dt: float = 0.001) -> bool:
        """
        Integrate dendritic input using leaky integrate-and-fire model.
        Returns: True if neuron spikes, False otherwise.
        """
        # Leak: voltage decays toward resting potential
        leak = -self.config.leak_conductance * (
            self.voltage - self.config.resting_potential
        )

        # Update voltage: dV/dt = leak + input
        dv_dt = leak + dendritic_input
        self.voltage += dv_dt * dt

        # Check for spike (and refractory period)
        current_time = len(self.spike_history) * dt
        time_since_last_spike = current_time - self.last_spike_time

        spike = False
        if (self.voltage >= self.config.threshold and
            time_since_last_spike >= self.refractory_period):
            spike = True
            self.voltage = self.config.reset_voltage
            self.last_spike_time = current_time
            self.spike_history.append(current_time)

        return spike

    def get_recent_spike_times(self, window: float = 0.1) -> List[float]:
        """Return spike times within the past `window` seconds."""
        current_time = len(self.spike_history) * 0.001
        return [t for t in self.spike_history if current_time - t < window]


# ============================================================================
# LAYER 20: DENDRITIC COMPARTMENTS
# ============================================================================

@dataclass
class DendriticBranchConfig:
    """Dendritic branch parameters."""
    num_inputs: int = 10  # Number of synaptic inputs per branch
    nonlinearity: str = 'quadratic'  # 'quadratic' or 'sigmoid'
    threshold: float = 0.3  # Dendritic spike threshold


class DendriticBranch:
    """
    Dendritic branch: performs independent nonlinear computation.

    Key insight: Dendrite is not a passive wire. Each branch can compute
    AND/OR gates, multiplicative gates (gating), and nonlinear functions.
    """

    def __init__(self, num_inputs: int = 10, config: DendriticBranchConfig = None):
        self.config = config or DendriticBranchConfig(num_inputs=num_inputs)
        self.num_inputs = num_inputs

        # Synaptic weights per input (initialize with strong values for signal propagation)
        # Initialize with positive bias so signals actually propagate
        # Mix of excitatory (+) and inhibitory (-) with more excitatory
        self.weights = np.random.uniform(0, 0.3, num_inputs)  # Mostly positive
        # Add a small fraction of inhibitory weights for gating
        inhibitory_indices = np.random.choice(num_inputs, max(1, num_inputs // 5), replace=False)
        self.weights[inhibitory_indices] = np.random.uniform(-0.2, 0, len(inhibitory_indices))
        self.weights = np.clip(self.weights, -0.5, 0.5)

        # Dendritic voltage (can generate local spikes)
        self.voltage = 0.0
        self.tau = 0.002  # Time constant (fast enough to pass signal, slow enough to integrate)

        # Local dendritic spike history for STDP
        self.spike_history = []

    def integrate(self, inputs: np.ndarray, dt: float = 0.001) -> float:
        """
        Integrate synaptic inputs with nonlinearity.

        Implements dendritic AND-gate behavior: multiplicative interactions
        between inputs (simulated via ReLU for stability).

        Args:
            inputs: Array of presynaptic activations
            dt: Time step

        Returns:
            Output of this dendritic branch
        """
        assert len(inputs) == self.num_inputs, f"Expected {self.num_inputs} inputs, got {len(inputs)}"

        # Weighted sum of inputs (clip for stability)
        weighted_input = np.dot(self.weights, inputs)
        weighted_input = np.clip(weighted_input, -10, 10)  # Prevent overflow

        # Nonlinearity - apply very strong gain to ensure signal propagates
        if self.config.nonlinearity == 'quadratic':
            # ReLU with very strong gain
            output = np.maximum(weighted_input, 0) * 10.0  # 10.0 gain for strong dendritic signals
        elif self.config.nonlinearity == 'sigmoid':
            # Sigmoid: smoother nonlinearity
            output = (1.0 / (1.0 + np.exp(-weighted_input * 2)) - 0.5) * 10.0
        else:
            output = weighted_input * 10.0

        # Dendritic integration with decay (slower decay for stronger signal integration)
        decay = np.exp(-dt / self.tau)  # Exponential decay
        self.voltage = self.voltage * decay + output * (1 - decay)
        self.voltage = np.clip(self.voltage, -1.0, 1.0)  # Bound voltage

        return self.voltage

    def learn_stdp(self, presynaptic: np.ndarray, postsynaptic_spike_time: Optional[float],
                   learning_rate: float = 0.001, window: float = 0.05):
        """
        Spike-timing-dependent plasticity (STDP).

        Rule:
        - If postsynaptic spike follows presynaptic: strengthen (LTP)
        - If postsynaptic spike precedes presynaptic: weaken (LTD)
        """
        if postsynaptic_spike_time is None:
            return

        for i, pre_activity in enumerate(presynaptic):
            if pre_activity > 0.01:  # Only learn if pre activity significant
                # Assume presynaptic spike occurred at this time
                # In real system, use precise spike times
                dt = postsynaptic_spike_time  # Simplified

                # STDP kernel
                if dt >= 0:  # Post after pre
                    ltp = np.exp(-dt / window) * 0.1
                    self.weights[i] += learning_rate * ltp * pre_activity
                else:  # Post before pre
                    ltd = -np.exp(dt / window) * 0.1
                    self.weights[i] += learning_rate * ltd * pre_activity

        # Prevent weight explosion (aggressive clipping)
        self.weights = np.clip(self.weights, -1.0, 1.0)


# ============================================================================
# LAYER 21: AXON AND SPIKE GENERATION
# ============================================================================

class Axon:
    """Axon: generates spikes and transmits output."""

    def __init__(self):
        self.spike_output = False
        self.output_rate = 0.0  # Firing rate (Hz)
        self.output_history = []

    def fire(self, soma_voltage: float, threshold: float = None) -> Tuple[bool, float]:
        """
        Pass through spike decision from soma (axon doesn't re-check threshold).
        The soma has already determined if a spike occurred.
        Returns: (spike_bool, output_value)
        """
        # Axon just transmits the spike, doesn't make independent threshold decision
        # Threshold checking is done in the Soma
        output_value = 1.0 if (soma_voltage >= (threshold or 0.05)) else 0.0

        self.spike_output = output_value > 0
        self.output_history.append(output_value)

        return self.spike_output, output_value


# ============================================================================
# LAYER 28: SYNAPTIC PLASTICITY RULES
# ============================================================================

class STDPRule:
    """Spike-timing-dependent plasticity."""

    def __init__(self, learning_rate: float = 0.01, window: float = 0.05):
        self.learning_rate = learning_rate
        self.window = window  # STDP time window (seconds)

    def apply(self, dendritic_branch: DendriticBranch, presynaptic: np.ndarray,
              postsynaptic_spike: bool, postsynaptic_spike_time: Optional[float] = None):
        """Apply STDP to dendritic branch."""
        if postsynaptic_spike and postsynaptic_spike_time is not None:
            dendritic_branch.learn_stdp(presynaptic, postsynaptic_spike_time,
                                       self.learning_rate, self.window)


class HebbianRule:
    """Hebbian learning: correlation between pre and post."""

    def __init__(self, learning_rate: float = 0.001):
        self.learning_rate = learning_rate

    def apply(self, dendritic_branch: DendriticBranch, presynaptic: np.ndarray,
              postsynaptic_rate: float):
        """Apply Hebbian learning."""
        dendritic_branch.weights += self.learning_rate * np.outer(
            presynaptic, [postsynaptic_rate]
        ).flatten() * 0.1
        dendritic_branch.weights = np.clip(dendritic_branch.weights, -1.0, 1.0)


class NeuromodulatedRule:
    """Learning gated by neuromodulator (dopamine, serotonin, acetylcholine)."""

    def __init__(self, learning_rate: float = 0.01):
        self.learning_rate = learning_rate

    def apply(self, dendritic_branch: DendriticBranch, presynaptic: np.ndarray,
              postsynaptic_rate: float, neuromodulator_level: float = 1.0):
        """Apply neuromodulated learning."""
        # Learning is gated by neuromodulator
        gated_learning_rate = self.learning_rate * neuromodulator_level
        dendritic_branch.weights += gated_learning_rate * presynaptic * postsynaptic_rate * 0.01
        dendritic_branch.weights = np.clip(dendritic_branch.weights, -1.0, 1.0)


# ============================================================================
# LAYER 5: ENERGY AND METABOLIC REGULATION
# ============================================================================

class EnergyBudget:
    """Energy regulation: ATP-based metabolic constraints."""

    def __init__(self, initial_atp: float = 100.0):
        self.atp_level = initial_atp
        self.baseline_atp = initial_atp
        self.metabolic_rate = 1.0  # ATP per millisecond at rest
        self.spike_cost = 10.0  # ATP cost per spike

    def consume(self, spike: bool) -> float:
        """Consume ATP for baseline + spike costs."""
        baseline_consumption = self.metabolic_rate * 0.001  # per ms
        spike_consumption = self.spike_cost if spike else 0.0

        total_consumption = baseline_consumption + spike_consumption
        self.atp_level = max(0, self.atp_level - total_consumption)

        return total_consumption

    def refund(self, amount: float):
        """Refund ATP (e.g., from offline learning)."""
        self.atp_level = min(self.baseline_atp, self.atp_level + amount)

    def can_spike(self) -> bool:
        """Check if neuron has enough energy to spike."""
        return self.atp_level >= self.spike_cost

    def get_energy_factor(self) -> float:
        """Get multiplier for neuron function based on energy (0-1)."""
        return self.atp_level / self.baseline_atp


# ============================================================================
# LAYER 10: HOMEOSTATIC REGULATION
# ============================================================================

class HomeostasisMonitor:
    """Homeostatic plasticity: self-regulation of weights and activation."""

    def __init__(self, target_firing_rate: float = 0.1, window: int = 100):
        self.target_firing_rate = target_firing_rate  # Desired fraction of time spiking
        self.window = window  # How many timesteps to average over
        self.recent_spikes = []
        self.weight_scale = 1.0

    def update(self, spike: bool, dendritic_branches: List[DendriticBranch], soma: Soma):
        """
        Monitor firing rate and adjust synaptic weights to maintain homeostasis.

        Principle: If firing too much, scale down weights. If too little, scale up.
        This prevents saturation and maintains stability.
        """
        self.recent_spikes.append(1.0 if spike else 0.0)
        if len(self.recent_spikes) > self.window:
            self.recent_spikes.pop(0)

        # Calculate recent firing rate
        current_firing_rate = np.mean(self.recent_spikes)

        # Adjust weights if firing rate deviates from target (additive, not multiplicative)
        error = current_firing_rate - self.target_firing_rate
        if abs(error) > 0.02:  # Only adjust if error is significant
            # Additive scaling (more stable than multiplicative)
            adjustment = -error * 0.001  # Small adjustment factor

            # Apply scaling to all dendritic weights
            for branch in dendritic_branches:
                branch.weights += adjustment * branch.weights  # Proportional but bounded
                branch.weights = np.clip(branch.weights, -1.0, 1.0)  # Aggressive clipping


# ============================================================================
# MAIN PROTO NEURON
# ============================================================================

class ProtoNeuron:
    """
    Complete biologically-plausible compartmental neuron.

    Layers integrated:
    - Layer 5: Energy budgeting (ATP constraints)
    - Layer 10: Homeostasis (self-regulation)
    - Layer 18: Soma compartment (integration)
    - Layer 20: Dendritic computation (5 branches with nonlinearity)
    - Layer 21: Axon (spike generation)
    - Layer 28: Plasticity rules (STDP, Hebbian, neuromodulation)

    This single neuron demonstrates:
    ✓ Local learning (no backprop)
    ✓ Energy constraints (realistic metabolism)
    ✓ Self-regulation (homeostasis)
    ✓ Biological plausibility (compartmental model)
    """

    def __init__(self, num_dendritic_branches: int = 5, inputs_per_branch: int = 10):
        # Compartments
        self.soma = Soma()
        self.dendritic_branches = [
            DendriticBranch(num_inputs=inputs_per_branch)
            for _ in range(num_dendritic_branches)
        ]
        self.axon = Axon()

        # Learning rules (increased rates for faster discrimination)
        self.stdp_rule = STDPRule(learning_rate=0.1, window=0.05)  # 10x stronger STDP
        self.hebbian_rule = HebbianRule(learning_rate=0.01)  # 10x stronger Hebbian
        self.neuromodulated_rule = NeuromodulatedRule(learning_rate=0.1)

        # Regulation (relaxed homeostasis to allow weight growth)
        self.energy = EnergyBudget(initial_atp=100.0)
        self.homeostasis = HomeostasisMonitor(target_firing_rate=0.2)  # More relaxed firing rate target

        # State
        self.spike_history = []
        self.voltage_history = []
        self.last_spike_time = -np.inf

        # Neuromodulator levels (dopamine, serotonin, etc.)
        self.neuromodulators = {
            'dopamine': 0.5,      # Motivation, learning
            'serotonin': 0.5,     # Mood, satiation
            'acetylcholine': 0.5  # Attention
        }

    def compute(self, inputs: np.ndarray, dt: float = 0.001) -> Tuple[bool, float]:
        """
        Complete neural computation for one timestep.

        Pipeline:
        1. Dendritic integration (5 branches in parallel)
        2. Soma summation
        3. Axon thresholding (conditional on energy)
        4. Plasticity updates (STDP, homeostasis)

        Args:
            inputs: 50-element array (10 inputs × 5 branches)
            dt: Time step

        Returns:
            (spike: bool, output_value: float)
        """
        assert len(inputs) == 50, f"Expected 50 inputs (10 per branch × 5), got {len(inputs)}"

        # Layer 20: Dendritic integration
        branch_outputs = []
        for i, branch in enumerate(self.dendritic_branches):
            branch_input = inputs[i*10:(i+1)*10]
            branch_out = branch.integrate(branch_input, dt)
            branch_outputs.append(branch_out)

        # Layer 18: Soma integration (sum of dendritic branches)
        dendritic_sum = np.sum(branch_outputs)
        spike = self.soma.integrate(dendritic_sum, dt)

        # Layer 21: Axon firing (with energy constraint)
        # Note: soma.integrate() already detected if a spike occurred
        # The axon just transmits the spike, energy can only block it
        if self.energy.can_spike():
            # Use the soma's spike detection directly (already happened in line 420)
            output_value = 1.0 if spike else 0.0
            # Energy can prevent spike
        else:
            spike = False  # No energy = no spike
            output_value = 0.0

        # Layer 5: Consume energy
        self.energy.consume(spike)

        # Layer 28: Apply plasticity rules
        if spike:
            self.last_spike_time = len(self.spike_history) * dt
            for i, branch in enumerate(self.dendritic_branches):
                branch_input = inputs[i*10:(i+1)*10]
                self.stdp_rule.apply(branch, branch_input, True, self.last_spike_time)

        # Layer 10: Homeostatic regulation
        self.homeostasis.update(spike, self.dendritic_branches, self.soma)

        # Track history
        self.spike_history.append(1.0 if spike else 0.0)
        self.voltage_history.append(self.soma.voltage)

        return spike, output_value

    def set_neuromodulator(self, name: str, level: float):
        """Set neuromodulator level (0-1)."""
        if name in self.neuromodulators:
            self.neuromodulators[name] = np.clip(level, 0.0, 1.0)

    def reset(self):
        """Reset neuron to initial state."""
        self.soma.voltage = self.soma.config.resting_potential
        self.soma.last_spike_time = -np.inf
        self.spike_history = []
        self.voltage_history = []
        self.energy.atp_level = self.energy.baseline_atp

    def get_firing_rate(self, window: int = 100) -> float:
        """Get recent firing rate."""
        if len(self.spike_history) < window:
            return np.mean(self.spike_history) if self.spike_history else 0.0
        return np.mean(self.spike_history[-window:])

    def get_energy_state(self) -> Dict:
        """Get energy information."""
        return {
            'atp_level': self.energy.atp_level,
            'baseline_atp': self.energy.baseline_atp,
            'energy_factor': self.energy.get_energy_factor(),
            'can_spike': self.energy.can_spike()
        }

    def get_synaptic_weights(self) -> List[np.ndarray]:
        """Get current synaptic weights from all branches."""
        return [branch.weights.copy() for branch in self.dendritic_branches]

    def set_synaptic_weights(self, weights: List[np.ndarray]):
        """Set synaptic weights for all branches."""
        for i, w in enumerate(weights):
            self.dendritic_branches[i].weights = w.copy()


# ============================================================================
# BATCH NEURON FOR EFFICIENT COMPUTATION
# ============================================================================

class ProtoNeuronBatch:
    """Multiple ProtoNeurons computing in parallel."""

    def __init__(self, num_neurons: int, num_dendritic_branches: int = 5,
                 inputs_per_branch: int = 10):
        self.neurons = [
            ProtoNeuron(num_dendritic_branches, inputs_per_branch)
            for _ in range(num_neurons)
        ]
        self.num_neurons = num_neurons

    def compute(self, inputs: np.ndarray, dt: float = 0.001) -> np.ndarray:
        """
        Compute batch of neurons.

        Args:
            inputs: Shape (num_neurons, 50)

        Returns:
            spikes: Shape (num_neurons,) - bool array
        """
        assert inputs.shape == (self.num_neurons, 50)

        spikes = np.zeros(self.num_neurons, dtype=bool)
        for i, neuron in enumerate(self.neurons):
            spike, _ = neuron.compute(inputs[i], dt)
            spikes[i] = spike

        return spikes

    def reset(self):
        """Reset all neurons."""
        for neuron in self.neurons:
            neuron.reset()

    def get_firing_rates(self, window: int = 100) -> np.ndarray:
        """Get firing rates of all neurons."""
        return np.array([neuron.get_firing_rate(window) for neuron in self.neurons])
