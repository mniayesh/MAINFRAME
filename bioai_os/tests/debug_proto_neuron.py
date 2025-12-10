"""Debug ProtoNeuron signal flow."""

import numpy as np
import sys
sys.path.insert(0, '/home/user/MAINFRAME')

from bioai_os.layer_5_proto_neuron import ProtoNeuron

# Create a simple test neuron
neuron = ProtoNeuron(num_dendritic_branches=2, inputs_per_branch=5)

# Test with a strong sustained input
inputs = np.ones(10) * 0.5  # 10 elements for 2 branches × 5 inputs

print("Debug: ProtoNeuron Signal Flow")
print("="*60)
print(f"Input: {inputs}")
print(f"Initial soma voltage: {neuron.soma.voltage:.4f}")
print(f"Initial weights branch 0: {neuron.dendritic_branches[0].weights}")
print(f"Initial weights branch 1: {neuron.dendritic_branches[1].weights}")
print()

# Run for 100 timesteps
for t in range(100):
    spike, output = neuron.compute(inputs, dt=0.001)

    if t % 10 == 0:
        branch_outputs = [b.voltage for b in neuron.dendritic_branches]
        dendritic_sum = sum(branch_outputs)
        print(f"T={t:3d}: Dendritic=[{', '.join(f'{b:.4f}' for b in branch_outputs)}], " +
              f"Sum={dendritic_sum:.4f}, Soma={neuron.soma.voltage:.4f}, " +
              f"Spike={spike}, Threshold={neuron.soma.config.threshold:.4f}")

print()
print("="*60)
print(f"Final soma voltage: {neuron.soma.voltage:.4f}")
print(f"Firing threshold: {neuron.soma.config.threshold:.4f}")
print(f"Final weights branch 0: {neuron.dendritic_branches[0].weights}")
print(f"Final weights branch 1: {neuron.dendritic_branches[1].weights}")
print(f"Total spikes: {sum(neuron.spike_history)}")
