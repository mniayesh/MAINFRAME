# Biological Learning Rules: Complete Analysis

This directory contains a comprehensive extraction and analysis of **how biology actually implements learning**, extracted from 90,313 biological formulas.

---

## 📁 Files in This Analysis

### 📊 Data Files
- **`bioformulas.db`** - SQLite database with 90,313 biological formulas
- **`learning_rules.json`** - Machine-readable export of 9 learning rules with full metadata

### 📄 Documentation
- **`BIOLOGICAL_LEARNING_SUMMARY.md`** - ⭐ **START HERE** - Executive summary
- **`BIOLOGICAL_LEARNING_RULES_ANALYSIS.md`** - Detailed technical analysis

### 🐍 Python Tools
- **`extract_learning_rules.py`** - Query and analyze learning rules from database
- **`compare_bio_vs_ai_learning.py`** - Compare biological vs. AI learning algorithms

### 📈 Visualizations
- **`stdp_window.png`** - STDP temporal learning window
- **`calcium_plasticity.png`** - Calcium-dependent plasticity zones
- **`bcm_rule.png`** - BCM sliding threshold mechanism

---

## 🚀 Quick Start

### 1. Read the Executive Summary
```bash
cat BIOLOGICAL_LEARNING_SUMMARY.md
```
**Time:** 10 minutes
**Outcome:** Understand biology's key learning principles

### 2. View the Visualizations
```bash
# Open the PNG files to see:
# - How STDP uses timing for credit assignment
# - How calcium concentration determines LTP/LTD
# - How BCM implements sliding threshold plasticity
```

### 3. Explore the Database
```bash
python3 extract_learning_rules.py
```
**Output:** Complete list of all 9 learning rules with formulas

### 4. Run Comparisons
```bash
python3 compare_bio_vs_ai_learning.py
```
**Output:**
- Comparison table (biology vs. AI)
- STDP, calcium, and BCM visualizations
- Demonstration that Oja's rule performs PCA

---

## 🧠 The 9 Learning Rules Extracted

| # | Rule | Type | Key Property |
|---|------|------|--------------|
| 1 | **Pair-Based STDP** | Temporal | Causality detection via spike timing |
| 2 | **Triplet STDP** | Temporal | Frequency-dependent plasticity |
| 3 | **BCM Rule** | Homeostatic | Sliding threshold prevents runaway |
| 4 | **Oja's Rule** | Normalization | Performs PCA, prevents weight explosion |
| 5 | **Calcium Plasticity** | Biochemical | The molecular substrate of learning |
| 6 | Symmetric STDP | Temporal | Magnitude-based, not direction |
| 7 | Asymmetric STDP | Temporal | Classic Hebbian timing |
| 8 | Anti-Hebbian STDP | Temporal | Decorrelation (inhibitory) |
| 9 | Mexican Hat STDP | Temporal | Difference of Gaussians window |

---

## 🔬 Key Findings

### Biology vs. Backpropagation

| Feature | Biology | Backprop |
|---------|---------|----------|
| **Locality** | ✅ 100% local | ❌ Global error |
| **Labels** | ✅ Unsupervised | ❌ Needs labels |
| **Timing** | ✅ Millisecond precision | ❌ Time-agnostic |
| **Stability** | ✅ Homeostatic | ❌ Needs regularization |
| **Biological** | ✅ Real neurons | ❌ Implausible |

### What AI Can Learn From Biology

1. **Local Learning Is Possible** - No global error signals needed
2. **Time Is a Learning Signal** - STDP uses precise timing (±20ms)
3. **Homeostasis Prevents Instability** - BCM threshold, Oja normalization
4. **Calcium = Computation** - Multi-purpose biochemical signal
5. **Unsupervised ≠ Useless** - Visual cortex self-organizes without labels

---

## 📐 Mathematical Formulas

### STDP (Spike-Timing Dependent Plasticity)
```
Δw = A₊ exp(-Δt/τ₊)    if Δt > 0  (pre before post → LTP)
     -A₋ exp(Δt/τ₋)    if Δt < 0  (post before pre → LTD)
```
**Time window:** ±20ms
**Meaning:** If pre-spike causes post-spike, strengthen synapse

### BCM Rule (Bienenstock-Cooper-Munro)
```
dw/dt = η · φ(c) · c_pre
where φ(c) = c(c - θᵖ)
```
**Key:** Threshold θ adapts to activity history
**Meaning:** Implements homeostatic plasticity

### Oja's Rule
```
Δwᵢ = η · y · (xᵢ - y·wᵢ)
```
**Property:** Performs Principal Component Analysis (PCA)
**Meaning:** Hebbian learning with automatic normalization

### Calcium-Based Plasticity
```
dw/dt = γₚΩ([Ca²⁺]) - γ_dΩ([Ca²⁺])·w
```
**Three zones:**
- Low [Ca²⁺] → LTD (depression)
- Medium [Ca²⁺] → No change
- High [Ca²⁺] → LTP (potentiation)

---

## 🔧 Using the Python Tools

### Extract Learning Rules
```python
from extract_learning_rules import LearningRuleExtractor

with LearningRuleExtractor("bioformulas.db") as extractor:
    # Get all learning rules
    all_rules = extractor.get_all_plasticity_rules()

    # Get STDP rules only
    stdp_rules = extractor.get_stdp_rules()

    # Get calcium-dependent rules
    calcium_rules = extractor.get_calcium_rules()

    # Search for specific formulas
    ltp_formulas = extractor.search_formulas("LTP")

    # Export to JSON
    extractor.export_to_json("my_learning_rules.json")
```

### Implement Learning Rules
```python
from compare_bio_vs_ai_learning import BiologicalLearningRules

# STDP
dt = 10  # ms, pre before post
dw = BiologicalLearningRules.pair_stdp(dt)  # Returns positive (LTP)

# BCM
c_post = 2.0  # High activity
c_pre = 1.0
dw = BiologicalLearningRules.bcm_rule(c_post, c_pre, theta=1.5)

# Oja's rule
import numpy as np
x = np.array([1.0, 0.5])  # Input
y = 0.8  # Output
w = np.array([0.7, 0.3])  # Weights
dw = BiologicalLearningRules.oja_rule(x, y, w)
```

---

## 🎯 Actionable Insights for AI Research

### For Neuromorphic Computing
- Implement STDP in spiking neural networks
- Use calcium-like integration for multi-signal processing
- Add BCM sliding thresholds for stability

### For Deep Learning
- Explore local learning alternatives (e.g., Equilibrium Propagation)
- Add temporal credit assignment without backprop
- Implement adaptive thresholds (BCM-inspired)

### For Continual Learning
- Add homeostatic mechanisms (BCM, synaptic scaling)
- Use Oja-style weight normalization
- Prevent catastrophic forgetting with metaplasticity

### For Unsupervised Learning
- Study biological development patterns
- Implement covariance-based learning
- Use temporal coherence (STDP-like)

---

## 📚 Deep Dive Topics

### 1. NMDA Receptors: Biology's Coincidence Detector
The NMDA receptor is a molecular AND gate that requires **both**:
- Pre-synaptic glutamate release
- Post-synaptic depolarization

This implements Hebbian learning at the molecular level.

**Formula:**
```
I_NMDA = g·s·B(V)·(V - E)
where B(V) = 1/(1 + [Mg²⁺]·exp(-0.062V))
```

### 2. The Credit Assignment Problem
**AI approach:** Backpropagate errors from output
**Biology's approach:** Use local temporal correlations

STDP solves credit assignment using only:
- Local spike timing (±20ms window)
- Pre-synaptic activity
- Post-synaptic activity

No global error signal needed.

### 3. Why Backprop Is Biologically Implausible
1. **Weight Transport Problem:** Requires symmetric weights
2. **Non-local:** Needs error from distant layers
3. **Supervised:** Requires labels (most brain learning is unsupervised)
4. **Synchronous:** Requires separate forward/backward phases

Biology solves all these with local, asynchronous, unsupervised rules.

---

## 🔬 Database Schema

The bioformulas database contains:
- **90,313 total formulas**
- **10 plasticity rules** (9 extracted, 1 Shouval-Ca not detailed)
- **4 synapse models**
- **34 neuron models**

### Key Tables
- `formulas` - All biological formulas
- `plasticity_rules` - Learning rule metadata
- `parameters` - Formula parameters
- `synapses` - Synaptic transmission models
- `neuron_models` - Neuron dynamics

### Example Query
```sql
SELECT f.name, f.latex, pr.rule_type
FROM formulas f
JOIN plasticity_rules pr ON f.formula_id = pr.formula_id
WHERE pr.calcium_dependent = 1;
```

---

## 🌟 Key Takeaways

1. **Biology uses fundamentally different learning than AI**
   - Local vs. global
   - Unsupervised vs. supervised
   - Temporal vs. time-agnostic

2. **STDP implements temporal credit assignment**
   - ±20ms window
   - Causality detection
   - No labels needed

3. **Calcium is the computational currency**
   - Low → LTD
   - High → LTP
   - Integrates multiple signals

4. **Homeostasis is essential for stability**
   - BCM sliding threshold
   - Oja normalization
   - Prevents catastrophic forgetting

5. **The future of AI may be hybrid**
   - Biological rules for unsupervised learning
   - Backprop for supervised fine-tuning
   - Best of both worlds

---

## 📖 Recommended Reading Order

1. **Quick overview (15 min):**
   - `BIOLOGICAL_LEARNING_SUMMARY.md`
   - View the 3 PNG visualizations

2. **Technical details (1 hour):**
   - `BIOLOGICAL_LEARNING_RULES_ANALYSIS.md`
   - Run `extract_learning_rules.py`

3. **Hands-on experimentation (2 hours):**
   - Run `compare_bio_vs_ai_learning.py`
   - Modify parameters and see effects
   - Implement STDP in your own network

4. **Deep exploration (ongoing):**
   - Query the database directly
   - Read referenced papers
   - Implement in neuromorphic hardware

---

## 🤝 Contributing

Ideas for extending this analysis:
- [ ] Add dopamine-modulated learning (reward-based)
- [ ] Include eligibility traces (long-term credit assignment)
- [ ] Extract metaplasticity rules (plasticity of plasticity)
- [ ] Add energy efficiency comparisons
- [ ] Implement in spiking neural network simulators (Brian2, NEST)

---

## 📞 Questions?

For questions about:
- **The database:** See `bioformulas.db` schema
- **Learning rules:** See `BIOLOGICAL_LEARNING_RULES_ANALYSIS.md`
- **Python tools:** Check docstrings in `.py` files
- **Biological background:** See references in analysis document

---

## 🎓 Citation

If you use this analysis in your research:

```bibtex
@misc{bioformulas_learning_rules_2025,
  title={Biological Learning Rules: How Biology Actually Implements Learning},
  author={Extracted from bioformulas database},
  year={2025},
  note={90,313 biological formulas, 9 plasticity rules extracted}
}
```

---

**Remember:** Biology had 500 million years to optimize these algorithms. We've only had 70 years with neural networks. There's much to learn.
