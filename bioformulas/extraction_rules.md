
# Mechanism Extraction Rules from Biological Databases

## Phase 1: Chemistry Databases
### Gene Ontology → Cellular Processes
Extract GO terms related to:
- Molecular function (GO:0003674) → Mechanism signatures
- Biological process (GO:0008150) → System-level rules
- Cellular component (GO:0005575) → Structural constraints

### ChEBI → Molecular Properties
Extract from ChEBI entries:
- InChI strings → Structural fingerprints
- Charge/pKa → Electrostatic interactions
- Molecular weight → Scaling constraints
- Role classifications → Functional categories

## Phase 2: Protein Databases
### UniProt → Protein Mechanisms
- Post-translational modifications (phosphorylation sites) → learning rules
- Protein domains (InterPro) → computational modules
- Protein-protein interactions (BioGRID) → network motifs
- Subcellular localization → architectural constraints

## Phase 3: Pathways
### Reactome → Biochemical Motifs
Extract:
- Enzymatic reaction steps (substrates → products)
- Regulatory relationships (inhibition, activation)
- Pathway hierarchies (meta-level organization)

### Rhea → Reaction Kinetics
Extract:
- Forward/reverse rates
- Cofactor requirements
- EC number classifications

## Phase 4: Electrophysiology
### Channelpedia → Ion Channel Models
Extract:
- Conductance-voltage relationships
- Inactivation kinetics
- Pharmacological modulation
- Expression levels

### Allen Cell Types → Electrophysiological Features
Extract:
- Action potential shapes
- Firing patterns
- Intrinsic membrane properties

## Phase 5: Morphology
### NeuroMorpho → Dendritic Computation
Extract from neuron reconstructions:
- Branching patterns (fractal dimension)
- Compartment sizes (for cable equations)
- Spine densities (synaptic capacity)

### Allen Brain Atlas → Volumetric Organization
Extract:
- Layer thickness and composition
- Cell density distributions
- Projection patterns

## Phase 6: Plasticity
### Synapse Ontology → Learning Mechanisms
Extract:
- Presynaptic factors (release probability)
- Postsynaptic factors (receptor sensitivity)
- Plasticity induction rules (Hebbian, etc.)

### PhosphoSite → Biochemical Cascades
Extract:
- Kinase-substrate relationships
- Phosphorylation cascades
- Signaling thresholds

## Phase 7: Connectivity
### HCP/BAMS → Network Topology
Extract:
- Connection strengths (white matter tract FA)
- Network hubs and clusters
- Long-range vs local connectivity ratios

### C. elegans Connectome → Complete Circuits
Extract:
- Gap junction strength distributions
- Chemical synapse types and counts
- Network motifs (feedforward, feedback loops)

## Phase 8: Cognition
### Cognitive Atlas → Computational Processes
Extract:
- Process definitions (behavioral signatures)
- Task paradigms (input-output mappings)
- Individual differences (parameters)

### OpenNeuro → Empirical fMRI Patterns
Extract:
- Activation patterns (distributed representations)
- Timing relationships (network dynamics)
- Subject variability (parameter ranges)

## Cross-Database Linking Rules

1. **ChEBI ID ↔ Reactome Reactions**: Map molecular entities to biochemical steps
2. **UniProt IDs ↔ Gene Ontology**: Link protein functions to biological processes
3. **Channelpedia ↔ Gene names**: Map electrophysiological properties to genes
4. **NeuroMorpho ↔ Cell type**: Link morphologies to electrophysiological types
5. **Allen Atlas ↔ Cognitive Atlas**: Bridge anatomy to cognitive functions

## Output Schema

Each extracted mechanism becomes a formula record:
{
    "name": "Mechanism_Name",
    "domain": "extracted_from_database",
    "category": "mechanism_type",
    "latex": "Mathematical_Equation",
    "python_code": "implementation",
    "biological_origin": "database_source",
    "parameters": ["param1", "param2"],
    "constraints": ["constraint1"],
    "references": ["DOI", "URL"]
}
