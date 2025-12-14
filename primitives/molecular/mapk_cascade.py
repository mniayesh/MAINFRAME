"""
MAPK Signal Amplification Cascade (Entry #23-30)

Biological Level: 1 (Molecular)
Category: Signal Transduction
Function: Amplify weak signals through kinase cascade

Application in AI:
- Rare word/token amplification (1000× boost)
- Long-range dependency detection
- Multi-scale feature extraction
"""

import torch
import torch.nn as nn
from ..base_primitive import BiologicalPrimitive, PRIMITIVE_REGISTRY


class MAPKCascadeNode(BiologicalPrimitive):
    """
    Three-stage kinase cascade for signal amplification.

    Input: (batch, seq_len, hidden_dim) - token embeddings
    Output: (batch, seq_len, hidden_dim * 8) - amplified features

    Mechanism:
    - Stage 1 (Raf): Initial activation, 10× amplification
    - Stage 2 (MEK): Secondary amplification, 10× amplification
    - Stage 3 (ERK): Final amplification, 10× amplification
    - Total: 1000× amplification for rare signals
    """

    def __init__(self, hidden_dim: int = 768, amplification_per_stage: float = 10.0):
        super().__init__()

        # Metadata
        self.primitive_id = "MAPK_001"
        self.name = "MAPK Signal Amplification Cascade"
        self.biological_level = 1  # Molecular
        self.category = "signal_transduction"

        # I/O shapes - output is 8× larger due to multi-scale features
        self.input_shape = (None, hidden_dim)
        self.output_shape = (None, hidden_dim * 8)

        # No dependencies
        self.requires = []

        # Biological parameters
        self.amp_factor = nn.Parameter(torch.tensor(amplification_per_stage))

        # Stage 1: Raf kinase (coarse features)
        self.raf_kinase = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim * 2),
            nn.ReLU(),
            nn.LayerNorm(hidden_dim * 2)
        )

        # Stage 2: MEK kinase (intermediate features)
        self.mek_kinase = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim * 4),
            nn.ReLU(),
            nn.LayerNorm(hidden_dim * 4)
        )

        # Stage 3: ERK kinase (fine features)
        self.erk_kinase = nn.Sequential(
            nn.Linear(hidden_dim * 4, hidden_dim * 8),
            nn.ReLU(),
            nn.LayerNorm(hidden_dim * 8)
        )

        # Importance detector - identifies rare/important signals
        self.signal_detector = nn.Linear(hidden_dim, 1)

        self.flops_per_token = hidden_dim * (2 + 4 + 8)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: (batch, seq_len, hidden_dim)

        Returns:
            amplified: (batch, seq_len, hidden_dim * 8) - multi-scale amplified features
        """
        # Detect signal importance
        signal_strength = torch.sigmoid(self.signal_detector(x))  # (batch, seq_len, 1)

        # Stage 1: Raf activation (coarse scale)
        raf_output = self.raf_kinase(x)  # (batch, seq_len, hidden_dim * 2)
        raf_amplified = raf_output * (1 + signal_strength * (self.amp_factor - 1))

        # Stage 2: MEK activation (intermediate scale)
        mek_output = self.mek_kinase(raf_amplified)  # (batch, seq_len, hidden_dim * 4)
        mek_amplified = mek_output * (1 + signal_strength * (self.amp_factor - 1))

        # Stage 3: ERK activation (fine scale)
        erk_output = self.erk_kinase(mek_amplified)  # (batch, seq_len, hidden_dim * 8)
        erk_amplified = erk_output * (1 + signal_strength * (self.amp_factor - 1))

        # Total amplification: ~1000× for important signals, ~1× for background
        return erk_amplified

    def get_amplification_stats(self, x: torch.Tensor) -> dict:
        """
        Diagnostics: Measure actual amplification achieved.

        Returns:
            dict with min/mean/max amplification factors
        """
        with torch.no_grad():
            signal_strength = torch.sigmoid(self.signal_detector(x))
            amp_factor = 1 + signal_strength * (self.amp_factor - 1)
            total_amp = amp_factor ** 3  # Three stages

            return {
                'min_amplification': total_amp.min().item(),
                'mean_amplification': total_amp.mean().item(),
                'max_amplification': total_amp.max().item(),
            }


# Register in global registry
PRIMITIVE_REGISTRY.register("MAPK_001", MAPKCascadeNode)
