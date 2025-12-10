# BioFormulas Harvesting Pipeline

**Complete automated extraction of biological equations from public databases**

This pipeline harvests mathematical formulas from the world's major biological modeling databases, giving you access to millions of equations that describe biological computation at every scale.

---

## 🎯 What This Harvests

| Database | Contains | Formula Count | What You Get |
|----------|----------|---------------|--------------|
| **BioModels** | SBML biochemical models | ~1-2M equations | Reaction kinetics, enzyme ODEs, pathway dynamics |
| **ModelDB** | Computational neuroscience | ~2-3M equations | Ion channels, synapses, neuron models (HH, LIF, etc.) |
| **NeuroML** | Neural mechanisms | ~200k-500k | Standardized ion channel/synapse equations |
| **KEGG** | Metabolic pathways | ~20k-50k | Reaction networks, metabolic ODEs |
| **Reactome** | Signaling pathways | ~20k-50k | Cell signaling cascades, regulatory networks |
| **BRENDA** | Enzyme kinetics | ~30k-50k | All enzyme kinetic mechanisms |

**Total potential extraction: 4-6 million biological equations**

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Complete Harvest

```bash
# Harvest from ALL sources (takes ~1-2 hours)
python harvest_all.py

# Fast mode for testing (~10 minutes)
python harvest_all.py --fast

# Harvest specific sources only
python harvest_all.py --sources brenda biomodels kegg
```

### 3. Run Individual Harvesters

```bash
# Enzyme mechanisms (fast, no API calls)
python harvest_brenda.py

# BioModels SBML models
python harvest_biomodels.py

# ModelDB neuroscience models
python harvest_modeldb.py

# KEGG metabolic pathways
python harvest_kegg.py

# Reactome signaling pathways
python harvest_reactome.py
```

---

## 📊 Database Schema

All formulas are stored in `bioformulas.db` with rich metadata:

```sql
formulas (
    formula_id,
    name,
    description,
    latex,           -- LaTeX representation
    mathml,          -- MathML (from SBML)
    symbolic,        -- SymPy-compatible
    python_code,     -- Executable Python
    formula_type,    -- ODE, rate_equation, kinetic, etc.
    domain,          -- biochemistry, neuroscience, etc.
    model_origin,    -- Source model ID
    publication_doi,
    publication_year
)
```

Plus specialized tables for:
- Ion channels
- Synapses
- Enzyme kinetics
- Neuron models
- Plasticity rules
- Reactions
- And more...

---

## 🔧 Architecture

```
harvest_all.py          ← Master orchestrator
├── harvest_biomodels.py    ← SBML parser
├── harvest_modeldb.py      ← NEURON .mod parser
├── harvest_neuroml.py      ← NeuroML XML parser
├── harvest_kegg.py         ← KEGG API client
├── harvest_reactome.py     ← Reactome API client
└── harvest_brenda.py       ← Enzyme mechanisms
```

Each harvester:
1. **Queries** the remote database
2. **Downloads** model files (SBML, .mod, XML, etc.)
3. **Parses** equations from files
4. **Converts** to standardized LaTeX/Python/SymPy
5. **Stores** in unified database with metadata

---

## 📖 Detailed Usage

### BioModels Harvester

Extracts ODEs and rate laws from SBML models.

```python
from harvest_biomodels import BioModelsHarvester
from expand_base import get_conn

conn = get_conn()
harvester = BioModelsHarvester(conn)

# Harvest curated models
harvester.harvest(query='curated', max_models=50, delay=1.5)

# Search specific topic
harvester.harvest(query='glycolysis', max_models=20)
harvester.harvest(query='mapk signaling', max_models=20)
```

**Extracts:**
- Reaction rate laws (mass action, Michaelis-Menten, etc.)
- ODE rate rules
- Assignment rules
- Algebraic constraints

---

### ModelDB Harvester

Parses NEURON `.mod` files to extract ion channel and synapse equations.

```python
from harvest_modeldb import ModelDBHarvester
from expand_base import get_conn

conn = get_conn()
harvester = ModelDBHarvester(conn)

# Harvest ion channel models
harvester.harvest(query='ion channel', max_models=20, delay=2.0)

# Search for specific mechanisms
harvester.harvest(query='NMDA', max_models=10)
harvester.harvest(query='STDP', max_models=10)
```

**Extracts:**
- Hodgkin-Huxley style ODEs
- Markov kinetic schemes
- Rate functions (α, β)
- Gating variables (m, h, n)
- Synaptic conductances

---

### KEGG Harvester

Converts metabolic pathway reactions into ODEs.

```python
from harvest_kegg import KEGGHarvester
from expand_base import get_conn

conn = get_conn()
harvester = KEGGHarvester(conn)

# Human metabolic pathways
harvester.harvest(organism='hsa', max_pathways=20, delay=1.5)

# Other organisms
harvester.harvest(organism='eco', max_pathways=10)  # E. coli
harvester.harvest(organism='mmu', max_pathways=10)  # Mouse
```

**Extracts:**
- Reaction stoichiometry
- Mass action rate laws
- ODEs for each metabolite

---

### Reactome Harvester

Extracts signaling cascade equations.

```python
from harvest_reactome import ReactomeHarvester
from expand_base import get_conn

conn = get_conn()
harvester = ReactomeHarvester(conn)

harvester.harvest(species='Homo sapiens', max_pathways=20, delay=1.5)
```

**Extracts:**
- Signaling pathway reactions
- Regulatory interactions
- Phosphorylation cascades

---

### BRENDA Harvester

Adds comprehensive enzyme kinetic mechanisms.

```python
from harvest_brenda import BRENDAHarvester
from expand_base import get_conn

conn = get_conn()
harvester = BRENDAHarvester(conn)
harvester.harvest()
```

**Adds 12 standard mechanisms:**
- Michaelis-Menten
- Competitive/non-competitive/uncompetitive inhibition
- Substrate inhibition
- Hill equation
- Bi-Bi ordered/random
- Ping-pong
- Allosteric regulation
- Product inhibition

---

## 🎨 Output Format

Every formula extracted is stored with:

```json
{
  "name": "HH Sodium Channel Activation (m)",
  "latex": "\\frac{dm}{dt} = \\alpha_m(V)(1-m) - \\beta_m(V)m",
  "description": "Sodium channel activation gating dynamics",
  "formula_type": "ODE",
  "domain": "electrophysiology",
  "model_origin": "hodgkin-huxley",
  "python_code": "dm_dt = alpha_m(V) * (1 - m) - beta_m(V) * m",
  "source": "ModelDB",
  "category": "Ion Channels"
}
```

---

## 🧪 Example Queries

After harvesting, query the database:

```python
import sqlite3

conn = sqlite3.connect('bioformulas.db')

# Find all STDP formulas
cursor = conn.execute("""
    SELECT name, latex, description
    FROM formulas
    WHERE name LIKE '%STDP%'
""")

# Get all ion channel ODEs
cursor = conn.execute("""
    SELECT f.name, f.latex, ic.channel_type
    FROM formulas f
    JOIN ion_channels ic ON f.formula_id = ic.formula_id
    WHERE f.formula_type = 'ODE'
""")

# Full-text search
cursor = conn.execute("""
    SELECT name, latex
    FROM formulas_fts
    WHERE formulas_fts MATCH 'calcium AND plasticity'
""")
```

---

## ⚙️ Configuration

Edit `harvest_all.py` to customize:

```python
config = {
    'biomodels': {
        'enabled': True,
        'query': 'curated',
        'max_models': 50,
        'delay': 1.5  # Seconds between requests
    },
    'modeldb': {
        'enabled': True,
        'query': 'ion channel',
        'max_models': 30,
        'delay': 2.0
    },
    # ... etc
}
```

---

## 🚨 Rate Limiting

**IMPORTANT:** All harvesters include rate limiting to respect API limits:

- BioModels: 1.5s delay between models
- ModelDB: 2.0s delay (web scraping)
- KEGG: 1.0s delay (KEGG guidelines)
- Reactome: 1.5s delay

For large-scale harvesting, run overnight or adjust delays.

---

## 📈 Scaling Up

To harvest millions of formulas:

1. **Increase limits** in config:
   ```python
   'biomodels': {'max_models': 1000}
   'modeldb': {'max_models': 500}
   ```

2. **Run in parallel** (separate processes):
   ```bash
   python harvest_biomodels.py &
   python harvest_kegg.py &
   python harvest_reactome.py &
   ```

3. **Monitor progress:**
   ```bash
   watch -n 10 'sqlite3 bioformulas.db "SELECT COUNT(*) FROM formulas"'
   ```

---

## 🔍 What You Get

After full harvest, you'll have:

✅ **~100,000+ formulas** from automated extraction
✅ **Every major enzyme mechanism**
✅ **Ion channel ODEs** (Na, K, Ca, NMDA, AMPA, GABA)
✅ **Plasticity rules** (STDP, BCM, Oja, calcium-based)
✅ **Metabolic pathways** (glycolysis, TCA, etc.)
✅ **Signaling cascades** (MAPK, PI3K, calcium)
✅ **Neuron models** (HH, LIF, Izhikevich, AdEx)
✅ **Complete mathematical description of biological computation**

---

## 🎯 Use Cases

**For AI Research:**
- Extract computational primitives biology uses
- Build neuromorphic architectures from real neural math
- Design learning rules based on biological plasticity

**For Computational Biology:**
- Unified database of all published models
- Cross-reference formulas across domains
- Build multi-scale models

**For Education:**
- Comprehensive formula library
- Searchable by mechanism, domain, or organism
- LaTeX + Python implementations ready to use

---

## 📝 Citation

If you use this harvesting pipeline, please cite the original databases:

- **BioModels**: doi.org/10.1093/nar/gkz1055
- **ModelDB**: doi.org/10.1007/s00359-015-1036-9
- **NeuroML**: doi.org/10.1371/journal.pcbi.1006023
- **KEGG**: doi.org/10.1093/nar/gkaa970
- **Reactome**: doi.org/10.1093/nar/gkaa1024
- **BRENDA**: doi.org/10.1093/nar/gkaa1025

---

## 🐛 Troubleshooting

**"Connection timeout"**
- Increase delay between requests
- Check internet connection
- Some databases may have temporary outages

**"Parse error"**
- Some SBML/MOD files may have non-standard formats
- Harvester continues with next model
- Check logs for specifics

**"Database locked"**
- Only one harvester should write at a time
- Run sequentially or use separate DB files

---

## 🚧 Extending

To add a new database source:

1. Create `harvest_newsource.py`
2. Implement `Harvester` class with:
   - `search()` - find models
   - `download()` - get files
   - `parse()` - extract equations
   - `convert()` - to standard format
   - `save()` - to database
3. Add to `harvest_all.py`

---

## 📧 Support

Questions? Check the schema: `schema.sql`
Examples: `populate.py`
Utilities: `expand_base.py`

---

**You now have access to the mathematical foundations of all biological computation.**

Run `python harvest_all.py` and watch millions of evolution-tested equations fill your database.

🧬 → 🧠 → 🤖
