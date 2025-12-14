"""
Dynamic Primitive Loader and Architecture Assembly

Loads only the primitives needed for a specific task, chains them together,
and creates a complete architecture from biological building blocks.

Usage:
    loader = PrimitiveLoader()

    # Load specific primitives for rare word detection task
    arch = loader.compose([
        "MAPK_001",  # Amplify rare words
        "HH_001",    # Gate by importance
        "PC_001",    # Hierarchical processing
    ])

    output = arch(input_tokens)
"""

import torch
import torch.nn as nn
from typing import List, Dict, Optional
from pathlib import Path
import importlib
import inspect

from .base_primitive import BiologicalPrimitive, PRIMITIVE_REGISTRY


class PrimitiveLoader:
    """
    Dynamically loads and instantiates primitive nodes.

    Features:
    - Auto-discovery: Scans primitives/ directory for all nodes
    - Lazy loading: Only imports when needed
    - Dependency resolution: Loads required primitives automatically
    - Metadata search: Find primitives by biological level, category, etc.
    """

    def __init__(self, primitives_dir: Optional[Path] = None):
        self.primitives_dir = primitives_dir or Path(__file__).parent
        self._discovered = False

    def discover_primitives(self) -> Dict[str, str]:
        """
        Scan primitives directory and build registry.

        Returns:
            dict mapping primitive_id -> module path
        """
        primitive_map = {}

        # Scan all Python files in primitives/
        for py_file in self.primitives_dir.rglob("*.py"):
            if py_file.name.startswith("_"):
                continue  # Skip __init__.py, _private.py, etc.

            # Convert path to module name
            rel_path = py_file.relative_to(self.primitives_dir.parent)
            module_name = str(rel_path.with_suffix("")).replace("/", ".")

            try:
                # Import module to trigger registration
                importlib.import_module(module_name)
            except Exception as e:
                print(f"Warning: Failed to import {module_name}: {e}")

        self._discovered = True
        return primitive_map

    def load(self, primitive_id: str, **kwargs) -> BiologicalPrimitive:
        """
        Load a single primitive by ID.

        Args:
            primitive_id: e.g., "HH_001", "MAPK_001"
            **kwargs: Constructor arguments for the primitive

        Returns:
            Instantiated primitive node
        """
        if not self._discovered:
            self.discover_primitives()

        return PRIMITIVE_REGISTRY.load(primitive_id)

    def load_batch(self, primitive_ids: List[str]) -> List[BiologicalPrimitive]:
        """Load multiple primitives at once."""
        if not self._discovered:
            self.discover_primitives()

        return [self.load(pid) for pid in primitive_ids]

    def compose(self, primitive_ids: List[str],
                connection_mode: str = "sequential") -> nn.Module:
        """
        Compose multiple primitives into a complete architecture.

        Args:
            primitive_ids: List of primitive IDs to chain together
            connection_mode: How to connect them:
                - "sequential": Output of one feeds into next
                - "parallel": All receive same input, outputs concatenated
                - "residual": Sequential with skip connections

        Returns:
            Composed architecture (nn.Module)
        """
        primitives = self.load_batch(primitive_ids)

        if connection_mode == "sequential":
            return SequentialComposition(primitives)
        elif connection_mode == "parallel":
            return ParallelComposition(primitives)
        elif connection_mode == "residual":
            return ResidualComposition(primitives)
        else:
            raise ValueError(f"Unknown connection mode: {connection_mode}")

    def search(self, biological_level: Optional[int] = None,
               category: Optional[str] = None,
               max_flops: Optional[int] = None) -> List[str]:
        """
        Search for primitives matching criteria.

        Example:
            # Find all molecular-level primitives
            loader.search(biological_level=1)

            # Find efficient ion channel mechanisms
            loader.search(category="ion_channel", max_flops=1000)
        """
        if not self._discovered:
            self.discover_primitives()

        filters = {}
        if biological_level is not None:
            filters['biological_level'] = biological_level
        if category is not None:
            filters['category'] = category

        results = PRIMITIVE_REGISTRY.search(**filters)

        # Additional filtering by FLOPs
        if max_flops is not None:
            filtered = []
            for pid in results:
                prim = self.load(pid)
                if prim.flops_per_token <= max_flops:
                    filtered.append(pid)
            results = filtered

        return results


class SequentialComposition(nn.Module):
    """Chain primitives sequentially: out = p3(p2(p1(x)))"""

    def __init__(self, primitives: List[BiologicalPrimitive]):
        super().__init__()
        self.primitives = nn.ModuleList(primitives)

        # Validate shapes are compatible
        for i in range(len(primitives) - 1):
            out_shape = primitives[i].output_shape
            in_shape = primitives[i + 1].input_shape
            # Note: (None, dim) matches any sequence length
            if out_shape[1] != in_shape[1]:
                raise ValueError(
                    f"Shape mismatch: {primitives[i].name} outputs {out_shape}, "
                    f"but {primitives[i+1].name} expects {in_shape}"
                )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for primitive in self.primitives:
            x = primitive(x)
        return x


class ParallelComposition(nn.Module):
    """Run primitives in parallel, concatenate outputs."""

    def __init__(self, primitives: List[BiologicalPrimitive]):
        super().__init__()
        self.primitives = nn.ModuleList(primitives)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        outputs = [primitive(x) for primitive in self.primitives]
        return torch.cat(outputs, dim=-1)


class ResidualComposition(nn.Module):
    """Sequential with skip connections: out = x + p3(p2(p1(x)))"""

    def __init__(self, primitives: List[BiologicalPrimitive]):
        super().__init__()
        self.primitives = nn.ModuleList(primitives)

        # Projection layers to match dimensions for skip connections
        self.skip_projections = nn.ModuleList()
        for i, prim in enumerate(primitives):
            if prim.input_shape != prim.output_shape:
                # Need projection for skip connection
                in_dim = prim.input_shape[1]
                out_dim = prim.output_shape[1]
                self.skip_projections.append(nn.Linear(in_dim, out_dim))
            else:
                self.skip_projections.append(nn.Identity())

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for primitive, projection in zip(self.primitives, self.skip_projections):
            identity = projection(x)
            x = primitive(x) + identity
        return x


# Convenience function for quick architecture creation
def quick_arch(task: str, constraints: Optional[Dict] = None) -> nn.Module:
    """
    Generate architecture for common tasks.

    Args:
        task: "rare_word_detection", "hierarchical_nlp", "efficient_inference"
        constraints: {"max_flops": 10000, "max_memory_mb": 500}

    Returns:
        Composed architecture ready for training
    """
    loader = PrimitiveLoader()

    task_templates = {
        'rare_word_detection': [
            "MAPK_001",  # Amplify rare signals
            "HH_001",    # Gate by importance
        ],
        'hierarchical_nlp': [
            "PC_001",    # Predictive coding
            "HH_001",    # Selective gating
        ],
        'efficient_inference': [
            "HH_001",    # Skip unimportant tokens
        ],
    }

    if task not in task_templates:
        raise ValueError(f"Unknown task: {task}. Available: {list(task_templates.keys())}")

    primitive_ids = task_templates[task]
    return loader.compose(primitive_ids, connection_mode="sequential")
