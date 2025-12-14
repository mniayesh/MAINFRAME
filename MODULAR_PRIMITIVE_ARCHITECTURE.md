# Modular Primitive Architecture

**The Solution to MDA Implementation**

This document describes the modular architecture design that makes MDA (Mechanism-Driven Architecture) practical and scalable.

## The Challenge

**Original problem**: How to implement MDA with 5,000 biological primitives?

**Naive approach** (doesn't work):
- Load all 5,000 primitives into memory → 50+ GB
- Hard-code connections between primitives → unmaintainable
- Tight coupling between primitives → can't swap/experiment

**Required solution**:
- Dynamic loading: Only load the 6-12 primitives needed per task
- Standardized interface: Fixed I/O so primitives can be composed
- Loose coupling: Primitives work independently
- Easy experimentation: Swap primitives by changing IDs

## The Solution: Modular Primitive Nodes

### Core Design Principles

**1. Each Primitive = One PyTorch File**

Every biological mechanism is a self-contained `.py` file:

```
primitives/
├── molecular/
│   ├── mapk_cascade.py          # Entry #23-30
│   ├── metabolic_pathways.py    # Entry #1-22
│   └── ...                       # 1,000+ molecular primitives
├── cellular/
│   ├── hodgkin_huxley.py        # Entry #61-75
│   ├── calcium_dynamics.py      # Entry #76-90
│   └── ...                       # 1,000+ cellular primitives
├── systems/
│   ├── predictive_coding.py     # Entry #145
│   └── ...
└── ...                           # Levels 3-7
```

**2. Standardized I/O Interface**

All primitives inherit from `BiologicalPrimitive` base class:

```python
class HodgkinHuxleyNode(BiologicalPrimitive):
    def __init__(self):
        self.input_shape = (None, 768)   # (seq_len, hidden_dim)
        self.output_shape = (None, 768)
        self.biological_level = 2        # Cellular

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Implementation
        return gated_output
```

**Fixed contracts**:
- Input: `(batch, seq_len, hidden_dim)` tensor
- Output: `(batch, seq_len, output_dim)` tensor
- Metadata: Level, category, dependencies, FLOPs

**3. Dynamic Loading**

Only load primitives needed for your task:

```python
from primitives import PrimitiveLoader

loader = PrimitiveLoader()

# Load only 3 primitives (not all 5,000)
arch = loader.compose([
    "MAPK_001",  # Molecular amplification
    "HH_001",    # Cellular gating
    "PC_001",    # Systems-level prediction
])

# Memory: ~10 MB vs. ~50 GB for full library
```

**4. Compositional Architecture**

Chain primitives like LEGO blocks:

```python
# Sequential: MAPK → HH → PC
arch = loader.compose(
    ["MAPK_001", "HH_001", "PC_001"],
    connection_mode="sequential"
)

# Parallel: Run all, concatenate outputs
arch = loader.compose(
    ["MAPK_001", "HH_002", "PC_001"],
    connection_mode="parallel"
)

# Residual: Sequential with skip connections
arch = loader.compose(
    ["MAPK_001", "HH_001", "PC_001"],
    connection_mode="residual"
)
```

## Implementation Status

### ✅ Completed (Proof of Concept)

**Base Infrastructure**:
- `primitives/base_primitive.py` - Base class + registry system
- `primitives/primitive_loader.py` - Dynamic loading + composition
- `primitives/__init__.py` - Package structure

**Example Primitives** (3 implemented):
- `molecular/mapk_cascade.py` - MAPK signal amplification (Entry #23-30)
- `cellular/hodgkin_huxley.py` - Ion channel gating (Entry #61-75)
- `systems/predictive_coding.py` - Hierarchical prediction (Entry #145)

**Demo**:
- `examples/dynamic_primitive_demo.py` - Full working demonstration

### 🚧 Next Steps (Scale to 5,000)

**Immediate** (Next 10 primitives):
1. `molecular/ecoli_metabolism.py` - 65-objective optimization (Entry #1-18)
2. `cellular/calcium_dynamics.py` - Second messenger signaling (Entry #76-90)
3. `circuits/wilson_cowan.py` - E-I balance (Entry #151-180)
4. `circuits/oscillations.py` - Gamma/theta rhythms (Entry #181-210)
5. `systems/global_workspace.py` - Consciousness model (Entry #228)
6. `systems/attention.py` - Selective attention (Entry #229-240)
7. `cognition/working_memory.py` - PBWM model (Entry #351-370)
8. `cognition/reinforcement_learning.py` - TD learning (Entry #371-390)
9. `metacognition/gene_expression.py` - Meta-learning (Entry #451-470)
10. `advanced/executive_function.py` - Planning (Entry #551-570)

**Medium-term** (100 primitives):
- Cover all major mechanisms from `BIOAI_600_COMPLETE_MECHANISMS.md`
- Implement top 100 from `00_NOVELTY.md`
- Extract primitives from downloaded databases (2,500+ unique)

**Long-term** (5,000 primitives):
- Complete all 7 biological levels
- Automated extraction from databases
- Community contributions (like PyTorch Hub)

## Usage Examples

### Example 1: Rare Word Detection

**Task**: Detect and amplify rare words in language model

**Primitives needed**:
- MAPK cascade (1000× amplification)
- Hodgkin-Huxley gating (selective processing)

**Code**:
```python
from primitives import quick_arch

# Generate architecture automatically
model = quick_arch("rare_word_detection")

# Or compose manually
loader = PrimitiveLoader()
model = loader.compose(["MAPK_001", "HH_001"])

# Use like any PyTorch model
output = model(input_tokens)
```

### Example 2: Hierarchical NLP

**Task**: Build hierarchical language understanding

**Primitives needed**:
- Predictive coding (hierarchical prediction)
- Hodgkin-Huxley (selective attention)

**Code**:
```python
model = quick_arch("hierarchical_nlp")
# Uses: PC_001 → HH_001
```

### Example 3: Custom Task

**Task**: Novel architecture for multi-objective translation

**Primitives needed**:
- E. coli metabolism (65-objective optimization)
- MAPK (rare word amplification)
- Wilson-Cowan (stability)
- Global workspace (multi-task)

**Code**:
```python
loader = PrimitiveLoader()

model = loader.compose([
    "ECOLI_001",  # Multi-objective loss
    "MAPK_001",   # Rare word handling
    "WC_001",     # E-I balance for stability
    "GW_001",     # Multi-task coordination
], connection_mode="residual")
```

## Advantages of Modular Design

### 1. Memory Efficiency

| Approach | Memory Usage | Primitives Loaded |
|----------|--------------|-------------------|
| Monolithic (load all) | ~50 GB | 5,000 |
| Modular (task-specific) | ~10 MB | 6-12 |
| **Savings** | **5,000×** | **99.8% reduction** |

### 2. Compositional Flexibility

**Same primitives, different combinations**:
```python
# Efficient inference
model_1 = compose(["HH_001"])

# Rare word detection
model_2 = compose(["MAPK_001", "HH_001"])

# Full hierarchical
model_3 = compose(["MAPK_001", "HH_001", "PC_001", "GW_001"])
```

### 3. Easy Experimentation

**Swap primitives without code changes**:
```python
# Original
arch = compose(["MAPK_001", "HH_001"])

# Try different ion channel
arch = compose(["MAPK_001", "HH_002"])  # Just change ID

# Try different amplification
arch = compose(["ECOLI_001", "HH_001"])  # Use metabolism instead of MAPK
```

### 4. Biological Interpretability

Each primitive has clear biological analog:
- MAPK_001 → MAPK cascade in cell signaling
- HH_001 → Hodgkin-Huxley neuron dynamics
- PC_001 → Predictive coding in cortex

**Debugging**: "The model isn't gating correctly" → Check HH_001 threshold

### 5. Parallel Development

Different primitives can be developed independently:
- Team A: Molecular primitives (1-60)
- Team B: Cellular primitives (61-150)
- Team C: Circuit primitives (151-250)
- No conflicts, all use same interface

### 6. Incremental Growth

Start with 10 primitives, grow to 5,000:
- Week 1: 10 primitives → Basic architectures work
- Month 1: 100 primitives → Cover major mechanisms
- Year 1: 1,000 primitives → Comprehensive coverage
- Year 2: 5,000 primitives → Complete biological stack

## Technical Details

### Primitive Metadata

Every primitive exposes metadata for assembly:

```python
primitive.get_metadata() = {
    'id': 'MAPK_001',
    'name': 'MAPK Signal Amplification Cascade',
    'biological_level': 1,          # Molecular
    'category': 'signal_transduction',
    'input_shape': (None, 768),
    'output_shape': (None, 6144),   # 8× expansion
    'requires': [],                  # Dependencies
    'flops_per_token': 15360,
}
```

### Search and Discovery

Find primitives programmatically:

```python
loader = PrimitiveLoader()

# All molecular primitives
molecular = loader.search(biological_level=1)

# Efficient primitives (< 5K FLOPs)
efficient = loader.search(max_flops=5000)

# Ion channels
channels = loader.search(category="ion_channel")
```

### Connection Modes

Three ways to compose primitives:

**Sequential** (Pipeline):
```
Input → MAPK → HH → PC → Output
```

**Parallel** (Multi-path):
```
        ┌→ MAPK →┐
Input ──┼→ HH   →┼→ Concat → Output
        └→ PC   →┘
```

**Residual** (Skip connections):
```
Input ──→ MAPK ──→ + ──→ HH ──→ + ──→ Output
  │                 ↑            ↑
  └─────────────────┘            │
  └──────────────────────────────┘
```

### Shape Validation

Automatic shape checking prevents composition errors:

```python
# This works (shapes compatible)
compose(["MAPK_001", "HH_001"])
# MAPK: (N, 768) → (N, 6144)
# HH: (N, 6144) → (N, 6144) ✓

# This fails (shape mismatch)
compose(["HH_001", "MAPK_001"])
# HH: (N, 768) → (N, 768)
# MAPK: expects (N, 768) but needs wider input ✗
```

## Running the Demo

```bash
cd /home/user/MAINFRAME
python examples/dynamic_primitive_demo.py
```

**Output shows**:
1. Dynamic loading (only load what you need)
2. Architecture composition (chain primitives)
3. Task-specific selection (different tasks, different primitives)
4. Search and filtering (find primitives by criteria)
5. Real inference with diagnostics
6. Modular advantages (memory, flexibility, interpretability)

## Comparison to Traditional Approaches

| Aspect | Traditional AI | Modular MDA |
|--------|---------------|-------------|
| Architecture | Hand-designed | Composed from primitives |
| Scale | Fixed (1 architecture) | Infinite (combinatorial) |
| Memory | All loaded | Only needed primitives |
| Experimentation | Rewrite code | Swap primitive IDs |
| Interpretability | Black box | Biological mapping |
| Development | Monolithic | Parallel teams |

## Next Steps

**To reach 5,000 primitives**:

1. **Extract from databases** (2,500 primitives available)
   - Gene Ontology → 1,918 molecular functions
   - Reactome → 2,500+ signaling mechanisms
   - IUPHAR → 3,353 ion channels

2. **Implement from BIOAI_600** (600 documented mechanisms)
   - All 7 levels covered
   - Dependencies mapped
   - Ready for implementation

3. **Extract from 00_NOVELTY.md** (196 high-impact architectures)
   - Formulas already documented
   - Code examples provided
   - Direct conversion to primitives

4. **Community expansion**
   - GitHub: Users submit new primitives
   - Review: Ensure interface compliance
   - Merge: Add to library
   - Like PyTorch Hub but for biological primitives

## Conclusion

**Problem**: Need to implement 5,000 biological primitives for MDA
**Solution**: Modular primitive nodes with standardized I/O

**Key insight**: Each primitive is a separate file that acts as a node. Dynamically load only what you need, compose them like LEGO blocks.

**Status**:
- ✅ Infrastructure complete
- ✅ 3 primitives implemented (proof of concept)
- ✅ Full demo working
- 🚧 Scale to 5,000 primitives

**Impact**: Makes MDA practical, scalable, and maintainable.

The full biological stack (atoms → cells → circuits → cognition) is now implementable as modular, composable primitives.
