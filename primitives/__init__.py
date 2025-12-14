"""
Biological Primitives Package

Modular primitive nodes with standardized I/O interface.
Each primitive is a self-contained PyTorch module that can be
dynamically loaded and composed into complete architectures.

Organization:
  primitives/
    ├── base_primitive.py          # Base class and registry
    ├── primitive_loader.py        # Dynamic loading system
    ├── molecular/                 # Level 1: Molecular primitives
    │   └── mapk_cascade.py
    ├── cellular/                  # Level 2: Cellular primitives
    │   └── hodgkin_huxley.py
    ├── circuits/                  # Level 3: Circuit primitives
    ├── systems/                   # Level 4: Systems primitives
    │   └── predictive_coding.py
    └── ...                        # Levels 5-7

Usage:
    from primitives import PrimitiveLoader

    loader = PrimitiveLoader()
    arch = loader.compose(["MAPK_001", "HH_001", "PC_001"])
    output = arch(input_tensor)
"""

from .base_primitive import BiologicalPrimitive, PrimitiveRegistry, PRIMITIVE_REGISTRY
from .primitive_loader import PrimitiveLoader, quick_arch

__all__ = [
    'BiologicalPrimitive',
    'PrimitiveRegistry',
    'PRIMITIVE_REGISTRY',
    'PrimitiveLoader',
    'quick_arch',
]
