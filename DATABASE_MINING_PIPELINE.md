# Biological Database Mining Pipeline: From Atoms to Cognition

## Executive Summary

This document describes the **complete data extraction strategy** for building the mechanism library that powers biomimetic AI.

**Goal**: Extract ~5,000+ unique computational mechanisms from authoritative biological databases, organized by computational level.

**Timeline**: 8-12 weeks to complete first pass.

---

## Architecture: Database Hierarchy by Computational Level

```
┌─────────────────────────────────────────────────────────────────┐
│                    COGNITION LEVEL                              │
│  Cognitive Atlas (650 processes)  ← OpenNeuro (fMRI dynamics)   │
└──────────────────────┬──────────────────────────────────────────┘
                       │ (How cognition emerges from circuits)
┌──────────────────────▼──────────────────────────────────────────┐
│                    CIRCUIT LEVEL                                │
│  NeuroMorpho (170k morphologies)  ← Human Connectome (routing)  │
│  BAMS (connectivity)              ← Allen Brain (neuron types)  │
└──────────────────────┬──────────────────────────────────────────┘
                       │ (How circuits emerge from neurons)
┌──────────────────────▼──────────────────────────────────────────┐
│                    NEURON LEVEL                                 │
│  Channelpedia (ion kinetics)      ← IUPHAR (receptors)         │
│  Synapse Ontology (plasticity)    ← Spike mechanisms            │
└──────────────────────┬──────────────────────────────────────────┘
                       │ (How neurons emerge from molecules)
┌──────────────────────▼──────────────────────────────────────────┐
│                    PATHWAY LEVEL                                │
│  Reactome (10k steps)             ← KEGG (signaling)            │
│  BioCyc (enzyme mechanisms)       ← Rhea (balanced reactions)   │
└──────────────────────┬──────────────────────────────────────────┘
                       │ (How pathways emerge from reactions)
┌──────────────────────▼──────────────────────────────────────────┐
│                    MOLECULAR LEVEL                              │
│  UniProt (230M proteins)          ← InterPro (domains)          │
│  PDB (200k structures)            ← BioGRID (interactions)      │
└──────────────────────┬──────────────────────────────────────────┘
                       │ (How molecules emerge from chemistry)
┌──────────────────────▼──────────────────────────────────────────┐
│                    CHEMISTRY LEVEL                              │
│  PubChem (110M molecules)         ← ChEBI (ontology)            │
│  IUPAC (elements)                 ← Gene Ontology (mechanisms)  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Chemical & Molecular Level (Week 1-2)

### 1.1 Extract from ChEBI

**Goal**: Get the authoritative list of small molecules in biology.

```bash
# Download ChEBI OBO format
wget https://ftp.ebi.ac.uk/pub/databases/chebi/releases/latest/chebi.obo

# Parse
python parse_chebi.py → extract:
  - Molecule names
  - SMILES strings
  - Inchikeys
  - Biological roles (neurotransmitter, cofactor, etc.)
  - Ontological parents

Output: molecules.tsv (60k rows)
Fields: chebi_id, name, role, formula, parent_ids
```

### 1.2 Extract from Gene Ontology

**Goal**: Get biological process & molecular function terms.

```bash
# Download GO OBO
wget http://purl.obolibrary.org/obo/go.obo

# Parse for mechanistic terms
python parse_go.py → extract:
  - All "molecular function" terms (20k+)
  - "Biological process" terms (15k+)
  - "Cellular component" (10k+)
  - Relationships (is_a, part_of, regulates)

Output: go_mechanisms.tsv (45k rows)
Fields: go_id, name, type, definition, parents
```

**Example GO mechanisms relevant to AI**:
- GO:0005215 — "transporter activity" (gating)
- GO:0004930 — "G-protein coupled receptor activity" (signal routing)
- GO:0008152 — "metabolic process" (energy constraints)
- GO:0050849 — "diurnal rhythm process" (internal clocks)

---

## Phase 2: Protein & Interaction Level (Week 3-4)

### 2.1 Extract from UniProtKB

**Goal**: Get protein domain architecture and functional annotations.

```bash
# Download Swiss-Prot (curated only, 500k proteins)
wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz

# Parse for:
python parse_uniprot.py → extract:
  - Domain architecture (Pfam IDs)
  - Function (from comment section)
  - Subcellular localization
  - Tissue specificity
  - Biological role

Output: proteins_with_domains.tsv (500k rows)
Fields: uniprot_id, name, domains, function, localization, tissue
```

### 2.2 Extract from InterPro

**Goal**: Get functional domains and families.

```bash
# Download InterPro matches
wget ftp://ftp.ebi.ac.uk/pub/databases/interpro/releases/latest/interpro.xml.gz

# Parse
python parse_interpro.py → extract:
  - Domain names (Pfam, SMART, ProSite)
  - Domain boundaries
  - Functional descriptions
  - Family relationships

Output: protein_domains.tsv (40k domains)
Fields: domain_id, name, family, description, function_class
```

**Example domains relevant to computation**:
- PF00001: TM 7-transmembrane receptor (channel-like)
- PF00001: GPCR (signal routing)
- PF00010: Helix-turn-helix (binding / recognition)
- PF02931: Kinase (state change)

### 2.3 Extract from BioGRID

**Goal**: Get interaction networks and modularity.

```bash
# Download BioGRID
wget https://downloads.thebiogrid.org/BioGRID/Release-Archive/BIOGRID-4.4.227/BIOGRID-ALL-4.4.227.tab3.zip

# Parse
python parse_biogrid.py → extract:
  - Protein pairs
  - Interaction type
  - Experimental evidence
  - Confidence scores

Output: interaction_network.tsv (2.1M interactions)
Fields: protein_a, protein_b, interaction_type, confidence, evidence
```

---

## Phase 3: Reaction & Pathway Level (Week 5-6)

### 3.1 Extract from Reactome (THE BEST SOURCE)

**Goal**: Get the most mechanistically detailed pathway database.

```bash
# Download Reactome JSON
wget https://reactome.org/download/current/homo_sapiens.json.gz

# Parse
python parse_reactome.py → extract:
  - Pathways (2,500+)
  - Reactions (10,000+ mechanistic steps)
  - Reaction type (synthesis, degradation, binding, etc.)
  - Input/output compounds
  - Catalysts & regulators
  - Reaction formulas (where available)

# Reactome is hierarchical:
#   Top-level: Metabolism, Signal Transduction, Development, etc.
#   Mid-level: Specific pathways (e.g., "MAPK signaling")
#   Leaf: Individual reactions (e.g., "ERK phosphorylation by MEK")

Output: reactome_reactions.tsv (10k reactions)
Fields: reaction_id, pathway, reaction_type, inputs, outputs, catalysts, regulation
```

**Example Reactome reaction types** (directly useful for architecture):
- Binding (→ gating, routing)
- Phosphorylation (→ state change, gate)
- Degradation (→ decay, forgetting)
- Positive regulation (→ facilitation)
- Negative regulation (→ inhibition)
- Compartmentalization (→ isolation, modularity)

### 3.2 Extract from Rhea

**Goal**: Get balanced biochemical equations.

```bash
# Download Rhea
wget https://ftp.expasy.org/databases/rhea/rhea_complete.tsv

# Parse
python parse_rhea.py → extract:
  - Balanced equations
  - Substrates/products (with stoichiometry)
  - Enzyme (EC number)
  - Chemical transformations

Output: balanced_reactions.tsv (13.6k reactions)
Fields: rhea_id, equation, direction, ec_number, enzyme_name, substrates, products
```

**Why balanced reactions matter**:
- Stoichiometry is a computational constraint
- Can extract reaction rate structures from enzyme kinetics

### 3.3 Extract from KEGG Pathways

**Goal**: Get high-level pathway maps.

```bash
# KEGG is partly proprietary, but "pathway graphs" are available:
wget https://www.genome.jp/kegg-bin/get_htext?ko00000.kgml  # Pathway hierarchy

# Parse KGML (KEGG Markup Language)
python parse_kegg.py → extract:
  - Pathway hierarchy
  - Module decomposition
  - High-level signal flow

Output: kegg_pathway_structure.tsv
Fields: pathway_id, name, modules, signal_flows, type
```

---

## Phase 4: Ion Channel & Electrophysiology (Week 7)

### 4.1 Extract from Channelpedia / IUPHAR

**Goal**: Get electrical primitives (gating, kinetics, conductance).

```bash
# Channelpedia
wget http://channelpedia.epfl.ch/

# Parse channel data
python parse_channelpedia.py → extract:
  - Channel type (Na, K, Ca, Cl, etc.)
  - Gating mechanisms (Hodgkin-Huxley, Markov models)
  - Kinetic equations (α/β rates)
  - Voltage dependence
  - Temperature dependence
  - Reversal potentials

Output: ion_channels.tsv (1000+ channels)
Fields: channel_id, type, kinetics_type, alpha_formula, beta_formula,
        voltage_sensitivity, reversal_potential
```

**Example channel kinetics** (directly usable as primitives):
```
Sodium channel activation (m):
  α_m(V) = 0.1(V+40) / (1 - exp(-(V+40)/10))
  β_m(V) = 4 exp(-(V+65)/18)
```

### 4.2 Extract from IUPHAR Guide to Pharmacology

```bash
wget https://www.guidetopharmacology.org/DATA/

python parse_iuphar.py → extract:
  - Ion channels
  - GPCRs (G-protein coupled receptors)
  - Nuclear receptors
  - Ligand-gated channels
  - Voltage-gated channels
  - Channel states & transitions
  - Selectivity filters

Output: receptor_mechanisms.tsv (10k+ receptors)
Fields: receptor_id, type, subtype, ligands, modulators, channel_props
```

---

## Phase 5: Neuron Morphology & Types (Week 8)

### 5.1 Extract from Allen Brain Atlas

**Goal**: Get neuron types and their molecular profiles.

```bash
# Allen Brain Atlas transcriptomics
wget http://api.brain-map.org/api/v2/data/download/

# Query for:
python query_allen_brain.py:
  - List all neuron clusters (1000+)
  - For each cluster:
    - Morphological type
    - Electrophysiological properties
    - Marker genes (transcriptomic signature)
    - Brain region distribution
    - Connectivity partners

Output: neuron_types.tsv (1000+ types)
Fields: cluster_id, morphology, e_phys_props, markers, region, connectivity
```

### 5.2 Extract from NeuroMorpho

**Goal**: Get spatial morphologies for dendritic computation.

```bash
# NeuroMorpho API
python query_neuromorpho.py → extract:
  - All 170k morphologies in .swc format
  - Neuron type (pyramidal, basket, Purkinje, etc.)
  - Brain region
  - Species
  - Branching statistics (# branches, depth, angles)

# Compute from morphologies:
  - Dendritic surface area
  - Axon length
  - Number of potential synaptic sites
  - Branching complexity (fractal dimension)

Output: morphology_features.tsv (170k neurons)
Fields: neuron_id, type, region, n_branches, surface_area, complexity_index
```

---

## Phase 6: Synaptic Plasticity (Week 9)

### 6.1 Synapse Ontology

```bash
# Synapse ontology
wget https://github.com/SynO/SynO/raw/master/synaptic-ontology.owl

python parse_synapse_ontology.py → extract:
  - Synaptic proteins (presynaptic, postsynaptic, adhesion)
  - Vesicle cycle stages
  - Neurotransmitter receptors
  - Plasticity-related proteins
  - Scaffolding proteins
  - Kinase cascades

Output: synapse_proteome.tsv (2000+ proteins)
Fields: protein_id, location, function, pathway_role, plasticity_involvement
```

### 6.2 Plasticity Mechanisms from Literature

**Goal**: Extract STDP, LTP, LTD, BCM rules from peer-reviewed papers.

This requires **manual curation** (can't fully automate), but structure as:

```tsv
# plasticity_rules.tsv
rule_id	rule_name	equation	pre_factor	post_factor	time_window	learning_direction	reference_doi
STDP_001	Pair-based STDP	Δw(Δt)=A_+·e^(-Δt/τ+)	spike	spike	[-100,+100] ms	bidirectional	10.1523/JNEUROSCI.18-24-10464.1998
BCM_001	BCM rule	dw/dt=η·y·(y-θ)·x	firing_rate	firing_rate	[1,10] s	threshold-dependent	10.1523/JNEUROSCI.02-01-00032.1982
```

Sources:
- ModelDB (computational neuroscience models)
- Literature (Google Scholar searches for "STDP", "LTP", "BCM", "Oja", etc.)

---

## Phase 7: Circuit Connectivity (Week 10)

### 7.1 Extract from Human Connectome Project

```bash
# HCP structural connectomes (diffusion MRI)
wget https://db.humanconnectome.org/

# For each subject:
python parse_hcp_connectome.py → extract:
  - White matter bundles
  - Connection strength (fiber count / FA)
  - Path length
  - Region pairs

# Aggregate across 1000+ subjects:
  - Average connection probability
  - Connection weight distribution
  - Graph statistics (clustering, path length, modularity)

Output: connectivity_matrix.npy + connectivity_stats.tsv
```

### 7.2 Extract from BAMS

```bash
# Brain Architecture Management System
wget https://bams1.org/api/

python query_bams.py → extract:
  - Anatomical connections between brain regions
  - Connection strength (projection density)
  - Layer specificity (where connections originate/terminate)
  - Species specificity

Output: region_connectivity.tsv (1000+ regions)
Fields: source_region, target_region, strength, layer_source, layer_target
```

---

## Phase 8: Cognitive Processes (Week 11)

### 8.1 Extract from Cognitive Atlas

```bash
# Cognitive Atlas
wget https://www.cognitiveatlas.org/api/v1/

python query_cognitive_atlas.py → extract:
  - All 650+ cognitive processes
  - Definitions
  - Task relationships
  - Brain region involvement
  - Subprocess decomposition

Output: cognitive_processes.tsv (650 processes)
Fields: process_id, name, definition, parent_process, child_processes, brain_regions
```

**Example cognitive processes** (map to AI modules):
- GO:0007623 — "Working memory" → Attractor networks
- GO:0007624 — "Decision making" → Drift-diffusion + Bayesian
- GO:0007625 — "Language" → Sequence learning + semantics
- GO:0007626 — "Learning & memory" → Multiple plasticity rules

### 8.2 Extract from OpenNeuro

```bash
# OpenNeuro fMRI/EEG datasets
# Meta-analysis: extract typical activations for cognitive tasks

python meta_analyze_openneuro.py → extract:
  - Which brain regions activate for which cognitive tasks
  - Activation timescales (slow cortical dynamics)
  - Connectivity changes during tasks
  - Individual differences

Output: cognitive_task_signatures.tsv
Fields: task, brain_region, activation_level, timescale_ms
```

---

## Phase 9: Integration & Deduplication (Week 12)

### 9.1 Cross-Database Linking

Create a unified ID space:

```python
def link_across_databases():
    """
    Map entities across databases:
    - UniProt ID ↔ Ensemble Gene ID ↔ GO ID
    - EC number ↔ Reactome reaction ↔ KEGG enzyme
    - Brain region (Allen) ↔ Anatomist (BAMS)
    - Ion channel (IUPHAR) ↔ Gene (Ensemble) ↔ Protein (UniProt)
    """

    links = {}

    # Load all databases
    uniprot_data = load_uniprot()
    reactome_data = load_reactome()
    kegg_data = load_kegg()
    go_data = load_go()

    # Cross-references already embedded in databases
    for protein in uniprot_data:
        links[protein.id] = {
            'uniprot': protein.id,
            'gene': protein.gene_id,  # Ensemble
            'go_terms': protein.go_annotations,
            'domains': protein.interpro_domains,
        }

    return links
```

### 9.2 Deduplication

Some mechanisms appear in multiple databases with different names:

```python
def deduplicate_mechanisms():
    """
    Identify duplicate mechanisms across databases.

    Example:
    - Reactome: "ERK phosphorylation by MEK"
    - KEGG: "MAPK cascade - ERK phosphorylation"
    - Literature: "STDP potentiation window"

    Map to canonical mechanism.
    """

    canonical = {}

    for mech in all_mechanisms:
        # Signature: what does it do?
        signature = (mech.input_types, mech.output_types, mech.operation)

        if signature not in canonical:
            canonical[signature] = mech
        else:
            # Link variant to canonical form
            canonical[signature].add_alias(mech)

    return canonical
```

### 9.3 Formalization

Convert each mechanism to a **canonical formula**:

```python
class CanonicalMechanism:
    """
    Unified representation across all databases.
    """

    def __init__(self):
        self.name = ""              # E.g., "STDP potentiation"
        self.formula = ""           # LaTeX
        self.formula_code = ""      # Python/SymPy
        self.parameters = {}        # Parameter dict
        self.inputs = []            # What it depends on
        self.outputs = []           # What it produces
        self.timescale = 0.0        # milliseconds
        self.sources = []           # Where it came from
        self.aliases = []           # Other names for it
        self.validation = {}        # Experimental evidence
```

---

## Output: The Mechanism Database

### Structure

```
mechanisms/
├── molecules/
│   ├── neurotransmitters.tsv      (100+ entries)
│   ├── signaling_molecules.tsv    (500+ entries)
│   └── cofactors.tsv              (200+ entries)
│
├── reactions/
│   ├── metabolic_reactions.tsv    (10k entries)
│   ├── signaling_reactions.tsv    (5k entries)
│   └── plasticity_reactions.tsv   (500+ entries)
│
├── pathways/
│   ├── signal_transduction/       (100+ pathways)
│   ├── gene_regulation/           (50+ pathways)
│   └── metabolism/                (200+ pathways)
│
├── neurons/
│   ├── neuron_types.tsv           (1000+ types)
│   ├── ion_channels.tsv           (1000+ channels)
│   └── morphologies/              (170k morphologies)
│
├── circuits/
│   ├── microcircuits.tsv          (50+ canonical circuits)
│   ├── connectivity.tsv           (Brain region connections)
│   └── oscillations.tsv           (Rhythm mechanisms)
│
├── cognition/
│   ├── cognitive_processes.tsv    (650+ processes)
│   ├── task_signatures.tsv        (Brain activations)
│   └── learning_rules.tsv         (Plasticity rules)
│
└── formulas/
    ├── ode_mechanisms.tsv         (2000+ ODEs)
    ├── algebraic_mechanisms.tsv   (1000+ algebraic)
    ├── stochastic_mechanisms.tsv  (500+ SDEs)
    └── discrete_mechanisms.tsv    (300+ discrete maps)
```

### Total Coverage

| Category | Count | Source |
|----------|-------|--------|
| Molecules | 60k+ | ChEBI + PubChem |
| Proteins | 500k | UniProt (curated) |
| Protein domains | 40k | InterPro |
| Gene regulatory mechanisms | 45k | Gene Ontology |
| Pathways | 2,500 | Reactome |
| Mechanistic steps | 10k+ | Reactome reactions |
| Balanced reactions | 13.6k | Rhea |
| Ion channels | 1,000+ | IUPHAR + Channelpedia |
| Neuron types | 1,000+ | Allen Brain Atlas |
| Neuron morphologies | 170k | NeuroMorpho |
| Brain region connections | 1,000+ | HCP + BAMS |
| Cognitive processes | 650+ | Cognitive Atlas |
| Plasticity rules | 50+ | Literature + databases |
| **TOTAL UNIQUE MECHANISMS** | **~5,000-10,000** | All sources |

---

## Extraction Code Template

Here's the skeleton for extracting from any database:

```python
class DatabaseExtractor:
    """
    Generic extractor for biological databases.

    Each database inherits and implements extract().
    """

    def __init__(self, database_name, url, format='json'):
        self.name = database_name
        self.url = url
        self.format = format
        self.data = None

    def download(self):
        """Fetch data from source."""
        print(f"Downloading {self.name}...")
        response = requests.get(self.url)
        self.data = response.json() if self.format == 'json' else response.text
        return self.data

    def extract_mechanisms(self):
        """
        Override in subclasses.

        Should return:
        List[Mechanism] where each Mechanism has:
        - name: str
        - formula: str (LaTeX)
        - input: List[str]
        - output: List[str]
        - parameters: Dict[str, float]
        - source: str
        """
        raise NotImplementedError

    def save_tsv(self, mechanisms, filename):
        """Save to TSV."""
        df = pd.DataFrame([
            {
                'name': m.name,
                'formula': m.formula,
                'inputs': ';'.join(m.inputs),
                'outputs': ';'.join(m.outputs),
                'source': self.name,
            }
            for m in mechanisms
        ])
        df.to_csv(filename, sep='\t', index=False)


# Specific implementations
class ReactomeExtractor(DatabaseExtractor):
    def extract_mechanisms(self):
        mechanisms = []
        for reaction in self.data['reactions']:
            mech = Mechanism(
                name=reaction['displayName'],
                formula=reaction.get('formula', ''),
                inputs=[c['displayName'] for c in reaction['input']],
                outputs=[c['displayName'] for c in reaction['output']],
                parameters={},
            )
            mechanisms.append(mech)
        return mechanisms


class UniProtExtractor(DatabaseExtractor):
    def extract_mechanisms(self):
        mechanisms = []
        for protein in self.parse_fasta(self.data):
            # Protein domains are functional mechanisms
            for domain in protein.domains:
                mech = Mechanism(
                    name=f"{protein.name} - {domain.name}",
                    formula=domain.model if domain.model else '',
                    inputs=domain.substrates,
                    outputs=domain.products,
                    parameters=domain.kinetics if hasattr(domain, 'kinetics') else {},
                )
                mechanisms.append(mech)
        return mechanisms
```

---

## Timeline & Effort

| Phase | Task | Weeks | Effort | Output |
|-------|------|-------|--------|--------|
| 1 | Chemicals | 1-2 | 1 person | 60k molecules, 45k GO terms |
| 2 | Proteins | 3-4 | 1 person | 500k proteins, 40k domains, 2.1M interactions |
| 3 | Reactions | 5-6 | 1 person | 13.6k balanced reactions, 10k pathways |
| 4 | Electrophysiology | 7 | 0.5 person | 1000+ ion channels, kinetics |
| 5 | Neuron morphology | 8 | 0.5 person | 1000+ types, 170k morphologies |
| 6 | Synaptic plasticity | 9 | 1 person (manual) | 50+ plasticity rules from literature |
| 7 | Connectivity | 10 | 0.5 person | Brain connectome, region connections |
| 8 | Cognition | 11 | 0.5 person | 650 cognitive processes, task signatures |
| 9 | Integration | 12 | 1 person | Cross-linked unified database |
| **TOTAL** | | **12 weeks** | **~6 FTE** | **5,000-10,000 mechanisms** |

---

## Quality Control

### Validation Checks

```python
def validate_mechanism_library():
    """
    QA on extracted mechanisms.
    """

    checks = {
        'completeness': lambda m: bool(m.name and m.formula),
        'consistency': lambda m: len(m.inputs) > 0 or len(m.outputs) > 0,
        'parsability': lambda m: can_parse_latex(m.formula),
        'coverage': lambda m: m.source in AUTHORITATIVE_SOURCES,
    }

    for mechanism in all_mechanisms:
        for check_name, check_func in checks.items():
            if not check_func(mechanism):
                print(f"FAIL: {mechanism.name} - {check_name}")

    return sum(1 for m in all_mechanisms if all(
        check(m) for check in checks.values()
    )) / len(all_mechanisms)
```

### Benchmarking

Once extracted, validate against:
1. **Published parameter ranges** (are extracted parameters realistic?)
2. **Known biological dynamics** (can mechanisms be composed to recreate known behaviors?)
3. **Completeness** (have we captured the major computational motifs?)

---

## Next Steps

1. **Set up infrastructure** (PostgreSQL database, ETL pipeline)
2. **Begin Phase 1** (ChEBI + GO extraction)
3. **Validate early** (spot-check extracted mechanisms against literature)
4. **Parallelize** (phases 2-8 can run in parallel)
5. **Integrate** (link across databases, deduplicate, formalize)

---

## Success Criteria

✅ 5,000+ unique mechanisms extracted and validated
✅ Each mechanism has: name, formula (LaTeX), inputs, outputs, source
✅ Cross-database linking complete (UniProt ↔ Gene ↔ Pathway, etc.)
✅ Can compose mechanisms to recreate known biological processes
✅ Documentation complete for all data sources

---

**This is your complete mining strategy. Ready to execute.**
