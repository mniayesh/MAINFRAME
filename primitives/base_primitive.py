"""
Base Primitive Node - Standardized interface for all biological primitives.

All 5,000 primitives inherit from this base class, ensuring:
- Fixed input/output tensor interface
- Biological metadata (level, category, dependencies)
- Automatic shape validation
- Dynamic loading compatibility
"""

import torch
import torch.nn as nn
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional


class BiologicalPrimitive(nn.Module, ABC):
    """
    Base class for all biological primitive nodes.

    Each primitive must define:
    - input_shape: Expected input tensor shape (excluding batch)
    - output_shape: Output tensor shape (excluding batch)
    - biological_level: Which level of hierarchy (1-7)
    - category: Type of computation (e.g., "ion_channel", "metabolic")
    - forward(): The actual computation
    """

    def __init__(self):
        super().__init__()

        # Metadata - Must be set by subclass
        self.primitive_id: str = ""           # e.g., "HH_001"
        self.name: str = ""                   # e.g., "Hodgkin-Huxley Dynamics"
        self.biological_level: int = 0        # 1-7 hierarchy level
        self.category: str = ""               # e.g., "cellular", "molecular"

        # Interface specification
        self.input_shape: Tuple[int, ...] = None   # Expected input shape
        self.output_shape: Tuple[int, ...] = None  # Output shape

        # Dependencies - Other primitives this requires
        self.requires: List[str] = []         # List of primitive IDs

        # Computational cost (FLOPs estimate)
        self.flops_per_token: int = 0

    @abstractmethod
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass - must be implemented by each primitive.

        Args:
            x: Input tensor of shape (batch, *input_shape)

        Returns:
            Output tensor of shape (batch, *output_shape)
        """
        pass

    def validate_input(self, x: torch.Tensor) -> None:
        """Validate input tensor shape matches specification."""
        expected = (x.shape[0],) + self.input_shape  # Add batch dimension
        if x.shape != expected:
            raise ValueError(
                f"{self.name} expected input shape {expected}, "
                f"got {x.shape}"
            )

    def get_metadata(self) -> Dict:
        """Return primitive metadata for assembly system."""
        return {
            'id': self.primitive_id,
            'name': self.name,
            'biological_level': self.biological_level,
            'category': self.category,
            'input_shape': self.input_shape,
            'output_shape': self.output_shape,
            'requires': self.requires,
            'flops_per_token': self.flops_per_token,
        }

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.primitive_id}, "
            f"level={self.biological_level}, "
            f"in={self.input_shape}, "
            f"out={self.output_shape})"
        )


class PrimitiveRegistry:
    """
    Registry for dynamically loading primitive nodes.

    Usage:
        registry = PrimitiveRegistry()
        registry.register("HH_001", HodgkinHuxleyNode)
        node = registry.load("HH_001")  # Instantiates the primitive
    """

    def __init__(self):
        self._primitives: Dict[str, type] = {}

    def register(self, primitive_id: str, primitive_class: type):
        """Register a primitive class."""
        self._primitives[primitive_id] = primitive_class

    def load(self, primitive_id: str) -> BiologicalPrimitive:
        """Dynamically instantiate a primitive by ID."""
        if primitive_id not in self._primitives:
            raise ValueError(f"Primitive {primitive_id} not found in registry")
        return self._primitives[primitive_id]()

    def load_batch(self, primitive_ids: List[str]) -> List[BiologicalPrimitive]:
        """Load multiple primitives at once."""
        return [self.load(pid) for pid in primitive_ids]

    def search(self, **filters) -> List[str]:
        """
        Search for primitives matching criteria.

        Example:
            registry.search(biological_level=2, category="cellular")
        """
        results = []
        for pid, cls in self._primitives.items():
            instance = cls()
            metadata = instance.get_metadata()

            # Check if all filters match
            if all(metadata.get(k) == v for k, v in filters.items()):
                results.append(pid)

        return results


# Global registry instance
PRIMITIVE_REGISTRY = PrimitiveRegistry()
