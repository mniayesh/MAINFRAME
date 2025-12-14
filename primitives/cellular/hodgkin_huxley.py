"""
Hodgkin-Huxley Ion Channel Dynamics (Entry #61-75)

Biological Level: 2 (Cellular)
Category: Ion Channel
Function: Selective signal gating based on membrane potential

Application in AI:
- Token importance filtering
- Selective attention mechanisms
- Adaptive computation (skip unimportant tokens)
"""

import torch
import torch.nn as nn
from ..base_primitive import BiologicalPrimitive, PRIMITIVE_REGISTRY


class HodgkinHuxleyNode(BiologicalPrimitive):
    """
    Ion channel gating mechanism for selective processing.

    Input: (batch, seq_len, hidden_dim) - token embeddings
    Output: (batch, seq_len, hidden_dim) - gated embeddings + mask

    Mechanism:
    - Membrane potential increases with token importance
    - Fires (deep process) when V_mem > threshold
    - Skips expensive operations for unimportant tokens
    """

    def __init__(self, hidden_dim: int = 768, threshold: float = -55.0):
        super().__init__()

        # Metadata
        self.primitive_id = "HH_001"
        self.name = "Hodgkin-Huxley Ion Channel Dynamics"
        self.biological_level = 2  # Cellular
        self.category = "ion_channel"

        # I/O shapes
        self.input_shape = (None, hidden_dim)  # (seq_len, hidden_dim)
        self.output_shape = (None, hidden_dim)

        # Dependencies
        self.requires = []  # No dependencies, fundamental primitive

        # Biological parameters
        self.threshold = nn.Parameter(torch.tensor(threshold))
        self.V_rest = nn.Parameter(torch.tensor(-70.0))
        self.leak_rate = nn.Parameter(torch.tensor(0.1))

        # Learnable importance estimator
        self.importance_net = nn.Linear(hidden_dim, 1)

        # Gating network (used when above threshold)
        self.gate = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim)
        )

        self.flops_per_token = hidden_dim * 3  # Approximate

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: (batch, seq_len, hidden_dim)

        Returns:
            gated_x: (batch, seq_len, hidden_dim) - selectively processed
        """
        batch, seq_len, hidden_dim = x.shape

        # Calculate token importance (analogous to depolarization)
        importance = self.importance_net(x).squeeze(-1)  # (batch, seq_len)

        # Membrane potential dynamics
        V_mem = self.V_rest + importance * 30.0  # Scale to mV range

        # Apply leak (return to resting potential)
        V_mem = V_mem * (1 - self.leak_rate) + self.V_rest * self.leak_rate

        # Generate action potential (1 if above threshold, 0 otherwise)
        firing_mask = (V_mem > self.threshold).float()  # (batch, seq_len)

        # Selective processing:
        # - Above threshold: Deep processing with gate network
        # - Below threshold: Pass through with minimal computation
        gated = self.gate(x) * firing_mask.unsqueeze(-1) + x * (1 - firing_mask.unsqueeze(-1))

        return gated

    def get_firing_rate(self, x: torch.Tensor) -> float:
        """
        Diagnostics: What percentage of tokens fire?

        Useful for monitoring computational efficiency.
        """
        with torch.no_grad():
            importance = self.importance_net(x).squeeze(-1)
            V_mem = self.V_rest + importance * 30.0
            firing_mask = (V_mem > self.threshold).float()
            return firing_mask.mean().item()


# Register in global registry
PRIMITIVE_REGISTRY.register("HH_001", HodgkinHuxleyNode)
