"""
Predictive Coding Hierarchy (Entry #145)

Biological Level: 4 (Systems)
Category: Hierarchical Processing
Function: Predict next level, learn from prediction errors

Application in AI:
- Self-supervised learning
- Hierarchical representations
- Efficient credit assignment
"""

import torch
import torch.nn as nn
from ..base_primitive import BiologicalPrimitive, PRIMITIVE_REGISTRY


class PredictiveCodingNode(BiologicalPrimitive):
    """
    Hierarchical predictive coding with error correction.

    Input: (batch, seq_len, hidden_dim) - bottom-up sensory input
    Output: (batch, seq_len, hidden_dim) - top-down prediction + error

    Mechanism:
    - Maintain internal prediction (μ)
    - Compare with bottom-up input (x)
    - Update prediction based on error
    - Pass error signal upward
    """

    def __init__(self, hidden_dim: int = 768, num_layers: int = 3, learning_rate: float = 0.01):
        super().__init__()

        # Metadata
        self.primitive_id = "PC_001"
        self.name = "Predictive Coding Hierarchy"
        self.biological_level = 4  # Systems
        self.category = "hierarchical_processing"

        # I/O shapes
        self.input_shape = (None, hidden_dim)
        self.output_shape = (None, hidden_dim)

        # May depend on lower-level primitives
        self.requires = []  # Can work standalone

        # Biological parameters
        self.num_layers = num_layers
        self.learning_rate = nn.Parameter(torch.tensor(learning_rate))

        # Prediction state (μ) - learnable initial state
        self.register_buffer('mu', torch.zeros(1, 1, hidden_dim))

        # Generative model (top-down prediction)
        self.W_gen = nn.Parameter(torch.randn(hidden_dim, hidden_dim) * 0.02)

        # Recognition model (bottom-up error propagation)
        self.W_rec = nn.Parameter(torch.randn(hidden_dim, hidden_dim) * 0.02)

        # Precision (confidence in prediction vs. input)
        self.precision = nn.Parameter(torch.ones(1))

        self.flops_per_token = hidden_dim * hidden_dim * 2

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: (batch, seq_len, hidden_dim) - bottom-up input

        Returns:
            output: (batch, seq_len, hidden_dim) - refined representation
        """
        batch, seq_len, hidden_dim = x.shape

        # Expand mu to match batch/sequence
        mu = self.mu.expand(batch, seq_len, hidden_dim).clone()

        # Iterative prediction refinement (biological cortex does ~10 iterations)
        num_iterations = 3  # Reduced for efficiency

        for _ in range(num_iterations):
            # Top-down prediction
            prediction = mu @ self.W_gen

            # Prediction error (bottom-up input - top-down prediction)
            error = x - prediction

            # Precision-weighted error (trust input more if precision is high)
            weighted_error = error * self.precision

            # Update internal state (gradient descent on prediction error)
            mu = mu + self.learning_rate * (weighted_error @ self.W_gen.T)

        # Output refined representation (prediction + residual error)
        output = mu + error * 0.1  # Small residual for flexibility

        # Update stored state for next timestep (stateful processing)
        self.mu = mu[:, -1:, :].detach()

        return output

    def reset_state(self):
        """Reset internal prediction state (e.g., at start of new sequence)."""
        self.mu.zero_()

    def get_prediction_error(self, x: torch.Tensor) -> torch.Tensor:
        """
        Diagnostics: Measure prediction error magnitude.

        Lower error = better internal model of data.
        """
        with torch.no_grad():
            mu = self.mu.expand_as(x)
            prediction = mu @ self.W_gen
            error = (x - prediction).pow(2).mean()
            return error


# Register in global registry
PRIMITIVE_REGISTRY.register("PC_001", PredictiveCodingNode)
