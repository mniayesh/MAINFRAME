# TOP-TIER BIOLOGICAL DATABASE APIs
## Comprehensive API Documentation and Access Methods

**Document Version:** 1.0
**Date:** 2025-12-10
**Purpose:** Research documentation for extracting mechanisms, processes, molecular functions, pathways, and quantitative parameters from major biological databases.

---

## Table of Contents

1. [Gene Ontology (GO)](#1-gene-ontology-go)
2. [Reactome](#2-reactome)
3. [KEGG](#3-kegg)
4. [IUPHAR/BPS Guide to Pharmacology](#4-iupharbps-guide-to-pharmacology)
5. [Comparative Analysis](#5-comparative-analysis)
6. [Computational/Architectural Value Assessment](#6-computationalarchitectural-value-assessment)

---

## 1. Gene Ontology (GO)

### Primary API Endpoint
- **Base URL:** `http://api.geneontology.org/api/`
- **Swagger Documentation:** `http://api.geneontology.org/`
- **Alternative SPARQL Endpoint:** `https://rdf.geneontology.org/blazegraph/sparql` (DEPRECATED - being phased out as of 2024)

### Authentication Requirements
- **API Key:** Not required for public access
- **Rate Limits:** Not explicitly documented
- **Academic Use:** Freely available for research

### Available Data Formats
- **OBO Format:** `http://purl.obolibrary.org/obo/go.obo`
- **OWL Format:** `http://purl.obolibrary.org/obo/go.owl`
- **JSON Format:** `http://purl.obolibrary.org/obo/go.json`
- **RDF/XML & Turtle:** For GO-CAMs (Gene Ontology Causal Activity Models)

### Key Entity Types and IDs

#### GO Term Structure
- **GO ID Format:** `GO:NNNNNNN` (e.g., `GO:0006915` for apoptotic process)
- **Three Ontology Aspects:**
  - **Biological Process (BP):** Larger biological programs (e.g., signal transduction, synaptic transmission)
  - **Molecular Function (MF):** Molecular-level activities (e.g., catalysis, binding, gating)
  - **Cellular Component (CC):** Cellular locations and structures

#### Hierarchical Relationships
- **is_a:** Sub-class relationship (e.g., glucose transport is_a monosaccharide transport)
- **part_of:** Component relationship (e.g., mitochondrial membrane part_of mitochondrial envelope)

### Example API Calls

#### 1. Get GO Term Metadata and Annotations
```bash
# Retrieve function data for apoptotic process
curl http://api.geneontology.org/api/bioentity/function/GO:0006915?start=0&rows=100

# Returns JSON with term definition, relationships, and annotations
```

#### 2. Get GO Terms for a Specific Gene
```bash
# Get all GO annotations for human gene NCBIGene:1493 (CTLA4)
curl http://api.geneontology.org/api/bioentity/gene/NCBIGene:1493/function

# Returns all molecular functions, biological processes, and cellular components
```

#### 3. Query Hierarchical Relationships
```bash
# Get all child terms (more specific) of a GO term
curl http://api.geneontology.org/api/bioentity/function/GO:0006915/subterms

# Get all parent terms (more general)
curl http://api.geneontology.org/api/bioentity/function/GO:0006915/superterms
```

#### 4. GOLr Search Query (Alternative SOLR-based)
```bash
# Search annotations for specific entity
curl "http://golr-aux.geneontology.io/solr/select?fq=document_category:annotation&q=*:*&fq=bioentity:RGD:3889&wt=json"
```

#### 5. Cross-References
```bash
# GO extensively cross-references to UniProt, NCBI, Ensembl, etc.
# Cross-references embedded in term metadata responses
```

### Bulk Download Options

#### Monthly Releases (Recommended)
- **Current Release:** `http://current.geneontology.org`
- **Archive Access:** `http://release.geneontology.org`
- **Historical Archive:** Available from March 2004 onwards

#### File Downloads
```bash
# Complete ontology in OBO format
wget http://purl.obolibrary.org/obo/go.obo

# Complete ontology in OWL format
wget http://purl.obolibrary.org/obo/go.owl

# Complete ontology in JSON format
wget http://purl.obolibrary.org/obo/go.json
```

### Update Frequency and Versioning
- **Official Releases:** Monthly (with persistent DOIs)
- **Snapshot Releases:** Weekly (for internal/testing use)
- **Versioning:** Each release has unique DOI for reproducibility
- **Format Version:** OBO 1.4 (latest), OBO 1.2 supported

### Computational/Architectural Value

#### High-Value Mechanisms & Processes
- **Predictive Coding-Related Terms:**
  - GO:0007601 (visual perception)
  - GO:0050896 (response to stimulus)
  - GO:0007611 (learning or memory)

- **Hebbian Learning & Synaptic Plasticity:**
  - GO:0048167 (regulation of synaptic plasticity)
  - GO:0048168 (regulation of neuronal synaptic plasticity)
  - GO:0099560 (synaptic membrane adhesion)

- **Signal Transduction:**
  - GO:0007165 (signal transduction)
  - GO:0023052 (signaling)
  - GO:0035556 (intracellular signal transduction)

#### High-Value Molecular Functions
- **Catalytic Activity:** GO:0003824
- **Binding Functions:** GO:0005488
- **Transporter Activity:** GO:0005215
- **Molecular Function Regulator:** GO:0098772
- **Ion Channel Activity:** GO:0005216
- **Gating Functions:** GO:0022836

---

## 2. Reactome

### Primary API Endpoint
- **Content Service:** `https://reactome.org/ContentService/`
- **Analysis Service:** `https://reactome.org/AnalysisService/`
- **API Documentation:** `https://reactome.org/dev/content-service`
- **Interactive Swagger:** `https://reactome.org/ContentService/#/`

### Authentication Requirements
- **API Key:** NOT required - public access
- **Rate Limits:** None documented
- **Token-Based Analysis:** Analysis Service uses tokens (valid for 7 days)
- **Academic Use:** Freely available under Creative Commons licenses

### Available Data Formats
- **JSON:** Primary format for all API responses
- **BioPAX Level 2 & 3:** Biological pathway exchange format
- **SBML Level 2.3:** Systems Biology Markup Language
- **PSI-MITAB:** Molecular interaction format
- **SBGN:** Systems Biology Graphical Notation
- **MySQL Dumps:** Complete database downloads
- **Neo4j GraphDB:** Graph database format

### Key Entity Types and IDs

#### Reactome Identifier Structure
- **Pathway ID Format:** `R-HSA-NNNNNN` (e.g., `R-HSA-69278`)
- **Reaction ID Format:** `R-HSA-NNNNNN` (e.g., `R-HSA-141409`)
- **Entity Formats:**
  - R-HSA = Homo sapiens
  - R-MMU = Mus musculus
  - Species-specific prefixes for other organisms

#### Entity Types
- **Pathways:** Hierarchical biological pathways
- **Reactions:** Individual biochemical reactions with stoichiometry
- **PhysicalEntities:** Proteins, complexes, small molecules
- **Events:** General term for pathways and reactions

### Example API Calls

#### 1. Get All Pathways Hierarchy for Species
```bash
# Get complete pathway hierarchy for humans (Homo sapiens = 48887)
curl -X GET --header 'Accept: application/json' \
  'https://reactome.org/ContentService/data/eventsHierarchy/9606'

# Returns nested JSON with all top-level pathways and their children
```

#### 2. Get Specific Pathway Details
```bash
# Get detailed information about a pathway
curl -X GET --header 'Accept: application/json' \
  'https://reactome.org/ContentService/data/query/R-HSA-69278'

# Returns pathway name, description, participants, reactions, cross-references
```

#### 3. Get Reaction Details with Stoichiometry
```bash
# Retrieve reaction "Mad1 binds kinetochore"
curl -X GET --header 'Accept: application/json' \
  'https://reactome.org/ContentService/data/query/R-HSA-141409'

# Returns:
# - Input entities with stoichiometry
# - Output entities with stoichiometry
# - Catalysts and regulators
# - Compartment information
# - Cross-references
```

#### 4. Get All Participants in a Pathway/Reaction
```bash
# Get all PhysicalEntities in an event
curl -X GET --header 'Accept: application/json' \
  'https://reactome.org/ContentService/data/participants/R-HSA-5576891'

# Returns complete list of proteins, complexes, small molecules involved
```

#### 5. Cross-References to Other Databases
```bash
# Get cross-references for an entity
curl -X GET --header 'Accept: application/json' \
  'https://reactome.org/ContentService/data/entity/R-HSA-2318524/crossReference'

# Returns links to NCBI, Ensembl, UniProt, KEGG, ChEBI, PubMed, GO
```

#### 6. Search for Pathways by Name/Term
```bash
# Search for pathways containing "apoptosis"
curl -X GET --header 'Accept: application/json' \
  'https://reactome.org/ContentService/search/query?query=apoptosis&species=9606'
```

#### 7. Get Pathway Topology (Diagram)
```bash
# Get pathway diagram layout and topology
curl -X GET --header 'Accept: application/json' \
  'https://reactome.org/ContentService/data/pathway/R-HSA-69278/containedEvents'

# Returns hierarchical structure of sub-pathways and reactions
```

### Bulk Download Options

#### Download Page
**URL:** `https://reactome.org/download-data`

#### Available Bulk Formats
```bash
# BioPAX Level 3 (complete human reactions)
wget https://reactome.org/download/current/biopax.zip

# BioPAX Level 2
wget https://reactome.org/download/current/biopax2.zip

# SBML Level 2.3
wget https://reactome.org/download/current/homo_sapiens.2.sbml.tgz

# MySQL Database Dump (complete database)
wget https://reactome.org/download/current/databases/gk_current.sql.gz

# Neo4j Graph Database
wget https://reactome.org/download/current/reactome.graphdb.tgz

# Mapping files (pathway-gene-reaction associations)
wget https://reactome.org/download/current/NCBI2Reactome_All_Levels.txt
```

#### Historical Versions
```bash
# Access specific version (e.g., Version 80)
wget https://download.reactome.org/80/databases/gk_current.sql.gz

# Versions 60, 65, 70+ available
```

### Update Frequency and Versioning
- **Release Schedule:** Quarterly
- **Current Version (Dec 2025):** Version 82+
- **Versioning Format:** Simple incrementing numbers (80, 81, 82...)
- **Archive Access:** All releases from Version 60 onwards preserved
- **Content Updates:** Continuously curated by expert biologists

### Computational/Architectural Value

#### High-Value Pathway Topology
- **Signal Transduction Networks:** Complete wiring diagrams
- **Feedback Loops:** Regulatory circuits clearly annotated
- **Pathway Dynamics:** Temporal ordering of reactions
- **Compartmentalization:** Subcellular localization critical for dynamics

#### Quantitative Parameters Available
- **Reaction Stoichiometry:** All input/output coefficients
- **Catalysts and Regulators:** Positive/negative regulation
- **Disease Variants:** Mutations affecting pathways
- **Drug Targets:** Therapeutic intervention points

---

## 3. KEGG

### Primary API Endpoint
- **Base URL:** `https://rest.kegg.jp/`
- **API Documentation:** `https://www.kegg.jp/kegg/rest/keggapi.html`
- **Format:** REST-style API

### Authentication Requirements
- **API Key:** NOT required
- **Rate Limits:** **3 requests per second maximum** (STRICT - access will be blocked if exceeded)
- **Academic Use Only:** KEGG API available only for academic users
- **Non-Academic Use:** Requires license - see KEGG website

### Available Data Formats
- **JSON:** Supported via `/json` option
- **KGML:** KEGG Markup Language (XML-based pathway format)
- **KGML+SVG:** Enhanced pathway graphics
- **Text/Flat File:** Default format for most queries
- **Image Formats:** PNG pathway maps available

### Key Entity Types and IDs

#### KEGG Identifier Structure
- **Pathway IDs:**
  - Reference pathways: `map#####` (e.g., `map00010` for glycolysis)
  - Organism-specific: `org#####` (e.g., `hsa00010` for human glycolysis)
  - hsa = Homo sapiens, mmu = Mus musculus, etc.

- **Compound IDs:** `C#####` (e.g., `C00031` for D-Glucose)
- **Reaction IDs:** `R#####` (e.g., `R00299` for hexokinase reaction)
- **Enzyme IDs:** `EC #.#.#.#` (e.g., `EC 2.7.1.1` for hexokinase)
- **Gene IDs:** `org:gene_id` (e.g., `hsa:3098` for human HK1 gene)
- **Module IDs:** `M#####` (e.g., `M00001` for glycolysis core module)
- **Glycan IDs:** `G#####` (e.g., `G00001`)

#### Database Prefixes
- **pathway:** KEGG pathway maps
- **compound:** Chemical compounds
- **reaction:** Biochemical reactions
- **enzyme:** Enzyme nomenclature
- **genes:** Gene catalogs for organisms
- **module:** Functional units/modules
- **disease:** Disease entries
- **drug:** Drug entries

### Example API Calls

#### 1. List All Pathways
```bash
# Get list of all reference pathways
curl https://rest.kegg.jp/list/pathway

# Get human-specific pathways
curl https://rest.kegg.jp/list/pathway/hsa

# Returns: pathway_id<TAB>pathway_name
```

#### 2. Get Specific Pathway Details
```bash
# Get human glycolysis pathway in text format
curl https://rest.kegg.jp/get/hsa00010

# Get pathway in JSON format
curl https://rest.kegg.jp/get/hsa00010/json

# Get KGML (XML pathway topology)
curl https://rest.kegg.jp/get/hsa00010/kgml

# Get pathway as PNG image
curl https://rest.kegg.jp/get/hsa00010/image
```

#### 3. Get Reaction Details with Stoichiometry
```bash
# Get reaction R00299 (hexokinase: ATP + D-Glucose -> ADP + D-Glucose 6-phosphate)
curl https://rest.kegg.jp/get/R00299

# Returns:
# - Reaction equation with stoichiometry
# - Enzyme(s) catalyzing reaction (EC numbers)
# - Pathways containing reaction
# - Compound IDs for substrates/products
```

#### 4. Get Compound/Metabolite Information
```bash
# Get D-Glucose information
curl https://rest.kegg.jp/get/C00031

# Returns:
# - Chemical formula
# - Exact mass, molecular weight
# - Chemical structure data
# - Pathways containing compound
# - Reactions involving compound
```

#### 5. Find Operations (Search)
```bash
# Find pathways containing "glycolysis"
curl https://rest.kegg.jp/find/pathway/glycolysis

# Find compounds by exact mass (180.0634 +/- 0.01)
curl https://rest.kegg.jp/find/compound/180.0634/exact_mass

# Find compounds by molecular formula
curl https://rest.kegg.jp/find/compound/C6H12O6/formula
```

#### 6. Link Operations (Cross-References)
```bash
# Get all pathways for a specific gene
curl https://rest.kegg.jp/link/pathway/hsa:3098

# Get all genes in a pathway
curl https://rest.kegg.jp/link/genes/hsa00010

# Get PubMed cross-references
curl https://rest.kegg.jp/link/pubmed/hsa:3098

# Cross-reference to external databases
curl https://rest.kegg.jp/conv/ncbi-geneid/hsa:3098
curl https://rest.kegg.jp/conv/uniprot/hsa:3098
```

#### 7. Get Hierarchical Relationships
```bash
# Get all reactions in a pathway
curl https://rest.kegg.jp/link/reaction/pathway:hsa00010

# Get module composition
curl https://rest.kegg.jp/get/M00001

# Returns module definition with gene requirements
```

#### 8. Get Modules (Functional Units)
```bash
# Get glycolysis core module
curl https://rest.kegg.jp/get/M00001

# List all modules
curl https://rest.kegg.jp/list/module

# Returns functional module definitions with gene composition
```

### Bulk Download Options

#### KEGG FTP Service (Subscription Required)
- **Academic FTP:** Available for academic users with subscription
- **URL:** `https://www.kegg.jp/kegg/download/`
- **Contents:**
  - Complete KGML files for all pathways
  - KGML+SVG files
  - Database flat files
  - Complete pathway maps

#### Important Notes
- KEGG licensing prevents redistribution of downloaded data
- API access (`https://rest.kegg.jp`) always returns latest data
- Bulk downloads require FTP subscription (separate from API access)

### Update Frequency and Versioning
- **Update Frequency:** Continuous updates (near real-time)
- **Release Notes:** Available at `https://www.genome.jp/kegg/docs/relnote.html`
- **30th Anniversary:** December 2025 marked KEGG's 30th anniversary
- **Historical Updates:** Previously quarterly/semi-annual releases
- **Current Data:** API always serves most current version
- **KGML Versions:** v0.3 (2003) → v0.4 (2004) → KGML+SVG (2010)

### Computational/Architectural Value

#### High-Value Metabolic Pathways
- **hsa00010:** Glycolysis/Gluconeogenesis (core energy metabolism)
- **hsa00020:** Citrate cycle (TCA cycle)
- **hsa00190:** Oxidative phosphorylation
- **hsa01100:** Metabolic pathways (overview map)

#### High-Value Signaling Pathways
- **hsa04010:** MAPK signaling pathway (architectural computation)
- **hsa04020:** Calcium signaling
- **hsa04024:** cAMP signaling
- **hsa04151:** PI3K-Akt signaling

#### Neural & Synaptic Pathways
- **hsa04724:** Glutamatergic synapse
- **hsa04727:** GABAergic synapse
- **hsa04728:** Dopaminergic synapse
- **hsa04720:** Long-term potentiation (Hebbian learning)
- **hsa04725:** Cholinergic synapse

#### Quantitative Parameters
- **Reaction Equations:** Complete stoichiometry for all reactions
- **Enzyme Kinetics:** Links to BRENDA database for Km, Vmax values
- **Thermodynamics:** Standard Gibbs free energies (via external links)
- **Rate Constants:** Limited direct data, but extensive enzyme characterization

---

## 4. IUPHAR/BPS Guide to Pharmacology

### Primary API Endpoint
- **Base URL:** `https://www.guidetopharmacology.org/services/`
- **Web Services Page:** `https://www.guidetopharmacology.org/webServices.jsp`
- **Main Website:** `https://www.guidetopharmacology.org/`

### Authentication Requirements
- **API Key:** NOT required - open access
- **Rate Limits:** Not documented (reasonable use expected)
- **License:** Open Database License (ODbL) + CC BY-SA 4.0
- **Academic & Commercial:** Free for all users

### Available Data Formats
- **JSON:** Primary API format (lightweight data interchange)
- **CSV/TSV:** Bulk downloads of targets, ligands, interactions
- **RDF/N3:** Linked data format (Notation3)
  - All data RDF file
  - Targets-only RDF
  - Ligands-only RDF
  - Interactions-only RDF
- **PostgreSQL Dump:** Complete relational database (PostgreSQL 12.20)

### Key Entity Types and IDs

#### GtoPdb Identifier Structure
- **Target IDs:** Numeric (e.g., `221` for GPER)
- **Ligand IDs:** Numeric (e.g., `1016` for tamoxifen)
- **Family IDs:** Numeric groupings of related targets
- **Interaction IDs:** Internal identifiers

#### External Identifiers
- **Targets:** UniProtKB IDs
- **Ligands:** PubChem Compound IDs (CIDs)
- **Genes:** HGNC symbols, Ensembl IDs
- **Diseases:** Disease Ontology IDs

#### Target Categories
- **GPCRs:** G protein-coupled receptors
- **Ion Channels:** Voltage-gated, ligand-gated channels
- **Enzymes:** Kinases, phosphatases, proteases
- **Nuclear Receptors:** Transcription factors
- **Transporters:** Active and passive transporters
- **Catalytic Receptors:** Receptor tyrosine kinases

### Example API Calls

#### 1. Get All Targets
```bash
# Retrieve all pharmacological targets
curl 'https://www.guidetopharmacology.org/services/targets'

# Filter by target type (GPCR)
curl 'https://www.guidetopharmacology.org/services/targets?type=GPCR'

# Returns JSON array of all targets with IDs and basic info
```

#### 2. Get Specific Target Details
```bash
# Get GPER (G protein-coupled estrogen receptor 1) - Target ID 221
curl 'https://www.guidetopharmacology.org/services/targets/221'

# Returns:
# - Target name, type, family
# - Gene information (HGNC, UniProt)
# - Functional annotations
# - Links to interactions
```

#### 3. Get All Ligands
```bash
# Retrieve all ligands
curl 'https://www.guidetopharmacology.org/services/ligands'

# Get only approved drugs
curl 'https://www.guidetopharmacology.org/services/ligands?type=Approved'

# Returns ligand IDs, names, types, approval status
```

#### 4. Get Specific Ligand Details
```bash
# Get tamoxifen (ligand ID 1016)
curl 'https://www.guidetopharmacology.org/services/ligands/1016'

# Get synonyms for tamoxifen
curl 'https://www.guidetopharmacology.org/services/ligands/1016/synonyms'

# Returns:
# - Chemical structure (SMILES, InChI)
# - PubChem CID
# - Drug approval status
# - Synonyms and trade names
```

#### 5. Get Target-Ligand Interactions (Quantitative)
```bash
# Find agonists of GPER (target 221) with pKi >= 7
curl 'https://www.guidetopharmacology.org/services/targets/221/interactions?type=Agonist&affinityType=pKi&affinity=7'

# Get all interactions for approved drugs at GPCRs with pKi data
curl 'https://www.guidetopharmacology.org/services/interactions?affinityType=pKi&approved=true&targetType=GPCR'

# Returns:
# - Ligand ID and target ID
# - Interaction type (agonist, antagonist, etc.)
# - Quantitative affinity (pKi, pIC50, pEC50, pKd)
# - Reference citations
```

#### 6. Get Interactions by Affinity Type
```bash
# Get all pKi interactions
curl 'https://www.guidetopharmacology.org/services/interactions?affinityType=pKi'

# Get high-affinity antagonists (pKi >= 8)
curl 'https://www.guidetopharmacology.org/services/interactions?type=Antagonist&affinityType=pKi&affinity=8'
```

#### 7. Get Family Information
```bash
# Get all target families
curl 'https://www.guidetopharmacology.org/services/families'

# Get targets in a specific family
curl 'https://www.guidetopharmacology.org/services/families/{family_id}/targets'
```

#### 8. Search Operations
```bash
# Search for targets/ligands by name
curl 'https://www.guidetopharmacology.org/services/ligands?name=dopamine'

# Complex queries with multiple filters
curl 'https://www.guidetopharmacology.org/services/interactions?targetType=Ion_channel&affinityType=pIC50&affinity=6'
```

### Bulk Download Options

#### Download Page
**URL:** `https://www.guidetopharmacology.org/download.jsp`

#### Available Downloads (Version 2025.3, Released Sept 10, 2025)

```bash
# Complete PostgreSQL database dump
wget https://www.guidetopharmacology.org/DATA/public_iuphardb_v2025.3.sql

# Targets CSV
wget https://www.guidetopharmacology.org/DATA/targets_and_families.csv

# Ligands CSV
wget https://www.guidetopharmacology.org/DATA/ligands.csv

# Interactions CSV (main data file)
wget https://www.guidetopharmacology.org/DATA/interactions.csv

# RDF Linked Data (all data in N3 format)
wget https://www.guidetopharmacology.org/DATA/public_iuphardb_v2025.3_all.n3

# RDF Targets only
wget https://www.guidetopharmacology.org/DATA/public_iuphardb_v2025.3_targets.n3

# RDF Ligands only
wget https://www.guidetopharmacology.org/DATA/public_iuphardb_v2025.3_ligands.n3

# RDF Interactions only
wget https://www.guidetopharmacology.org/DATA/public_iuphardb_v2025.3_interactions.n3
```

### Update Frequency and Versioning
- **Release Schedule:** Quarterly (4 releases per year)
- **Version Format:** YYYY.Q (e.g., 2025.3 for Q3 2025)
- **Recent Versions:**
  - 2025.3 (September 10, 2025)
  - 2025.2 (June 18, 2025)
  - 2025.1 (April 2, 2025)
  - 2023.2 (August 7, 2023)
- **Continuous Curation:** Expert-driven updates between releases
- **Persistent Versioning:** All previous versions archived

### Database Scale (Sept 2025)
- **Protein Targets:** 3,112 human targets
  - 1,790 with curated quantitative ligand interactions
- **Ligands:** 13,503 molecules
  - 9,758 with curated quantitative target interactions
- **Interactions:** 24,207 curated interactions
  - 21,968 quantitative (with affinity data)

### Computational/Architectural Value

#### High-Value Target Categories for Neural Architecture

##### Ion Channels (Critical for Neural Dynamics)
- **Voltage-gated sodium channels:** Action potential generation
- **Voltage-gated potassium channels:** Repolarization and oscillations
- **Voltage-gated calcium channels:** Synaptic transmission, plasticity
- **Ligand-gated ion channels:** Fast synaptic transmission
  - NMDA receptors (plasticity, learning)
  - AMPA receptors (excitatory transmission)
  - GABA-A receptors (inhibitory transmission)

##### GPCRs (Neuromodulation)
- **Dopamine receptors:** Reward learning, predictive coding
- **Serotonin receptors:** Mood, precision weighting
- **Adrenergic receptors:** Attention, arousal
- **Metabotropic glutamate receptors:** Synaptic plasticity modulation

##### Enzymes (Synaptic Computation)
- **Kinases:** Phosphorylation-based memory
- **Phosphatases:** Synaptic depression
- **Proteases:** Structural plasticity
- **Cyclases:** Second messenger systems

##### Transporters (Neurotransmitter Recycling)
- **Monoamine transporters:** Synaptic concentration control
- **Glutamate transporters:** Excitotoxicity prevention
- **GABA transporters:** Inhibitory tone regulation

#### Quantitative Parameters Available
- **Binding Affinities:** pKi, pKd (equilibrium dissociation constants)
- **Functional Potencies:** pEC50 (agonist potency), pIC50 (antagonist potency)
- **Selectivity Data:** Cross-target binding profiles
- **Kinetic Parameters:** kon, koff rates (limited but growing)
- **Voltage Dependence:** For ion channels
- **Allosteric Modulation:** PAM/NAM effects

#### Mechanistic Annotations
- **Receptor Gating:** Open/closed kinetics
- **Desensitization:** Receptor inactivation dynamics
- **Biased Signaling:** Pathway-selective activation
- **Receptor Oligomerization:** Functional assemblies

---

## 5. Comparative Analysis

### API Accessibility Summary

| Database | Auth Required | Rate Limits | Best Format | Ease of Use |
|----------|---------------|-------------|-------------|-------------|
| **GO** | No | None stated | JSON, OWL | Moderate |
| **Reactome** | No | None | JSON | Easy |
| **KEGG** | No | **3/sec STRICT** | JSON, KGML | Easy |
| **IUPHAR** | No | None stated | JSON, CSV | Easy |

### Data Completeness for Computational Modeling

| Feature | GO | Reactome | KEGG | IUPHAR |
|---------|----|----|------|--------|
| **Hierarchical Structures** | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★☆☆ |
| **Quantitative Parameters** | ☆☆☆☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★★★ |
| **Pathway Topology** | ☆☆☆☆☆ | ★★★★★ | ★★★★★ | ★☆☆☆☆ |
| **Reaction Stoichiometry** | ☆☆☆☆☆ | ★★★★★ | ★★★★★ | ★☆☆☆☆ |
| **Cross-References** | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★★☆ |
| **Molecular Mechanisms** | ★★★☆☆ | ★★★★☆ | ★★★★☆ | ★★★★★ |
| **Update Frequency** | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★☆ |

### Complementary Nature

The four databases are **highly complementary**:

1. **GO** provides the conceptual framework (what biological functions exist)
2. **Reactome** provides pathway mechanisms (how functions are implemented)
3. **KEGG** provides metabolic/signaling networks (system-level organization)
4. **IUPHAR** provides molecular pharmacology (precise quantitative parameters)

### Recommended Integration Strategy

```
┌─────────────────────────────────────────────────┐
│  Integration Flow for Computational Modeling   │
└─────────────────────────────────────────────────┘

1. START WITH GO
   ↓
   Identify relevant biological processes/functions
   (e.g., GO:0048167 - regulation of synaptic plasticity)

2. MAP TO REACTOME
   ↓
   Get detailed pathway implementations
   Extract reaction networks and stoichiometry

3. CROSS-REFERENCE TO KEGG
   ↓
   Get broader metabolic/signaling context
   Retrieve pathway topology (KGML)
   Extract module structure

4. ENRICH WITH IUPHAR
   ↓
   Get precise binding affinities for targets
   Extract quantitative pharmacology
   Identify druggable nodes

5. SYNTHESIZE
   ↓
   Build computational model with:
   - GO concepts (semantic layer)
   - Reactome mechanisms (implementation)
   - KEGG connectivity (network topology)
   - IUPHAR kinetics (quantitative parameters)
```

---

## 6. Computational/Architectural Value Assessment

### Highest-Value Data for Neural Architecture Modeling

#### Tier 1: Critical Foundation (Must-Have)

##### From IUPHAR (Quantitative Molecular Mechanisms)
- **NMDA receptor gating:** Voltage-dependent Mg²⁺ block (critical for Hebbian learning)
- **AMPA receptor kinetics:** Fast synaptic transmission parameters
- **GABA-A receptor pharmacology:** Inhibitory dynamics
- **Voltage-gated channel kinetics:** Action potential generation and propagation
- **Neuromodulator receptor affinities:** Dopamine, serotonin, norepinephrine systems

**Computational Value:** Direct implementation of synaptic transfer functions, gating variables, and neuromodulation

##### From Reactome (Pathway Dynamics)
- **Synaptic vesicle cycle:** Complete reaction network for neurotransmitter release
- **Long-term potentiation/depression:** Plasticity mechanism implementations
- **Calcium signaling cascades:** Second messenger systems
- **MAPK/ERK signaling:** Long-term plasticity and gene expression
- **PI3K-Akt pathway:** Neuronal growth and survival

**Computational Value:** Multi-scale temporal dynamics from milliseconds (transmission) to hours (plasticity consolidation)

##### From KEGG (Network Architecture)
- **Glutamatergic synapse (hsa04724):** Complete excitatory synapse wiring
- **GABAergic synapse (hsa04727):** Complete inhibitory synapse wiring
- **Long-term potentiation (hsa04720):** Hebbian plasticity circuit
- **MAPK signaling (hsa04010):** Learning and memory cascades
- **Circadian rhythm (hsa04710):** Temporal gating mechanisms

**Computational Value:** Provides network topology and module boundaries for compartmentalized computation

##### From GO (Semantic Organization)
- **Synaptic plasticity hierarchy:** GO:0048167 and descendants
- **Learning/memory processes:** GO:0007611 and descendants
- **Ion channel activity:** GO:0005216 and descendants
- **Signal transduction:** GO:0007165 and descendants

**Computational Value:** Ontological structure for organizing computational primitives

#### Tier 2: Enhanced Realism (Should-Have)

##### Metabolic Constraints (KEGG)
- **Glycolysis (hsa00010):** ATP production for synaptic function
- **Oxidative phosphorylation (hsa00190):** Neuronal energy budget
- **Neurotransmitter synthesis pathways:** Dopamine, serotonin, GABA synthesis
- **Lipid metabolism:** Membrane dynamics and myelination

**Computational Value:** Energetic constraints on neural computation, metabolic gating of plasticity

##### Receptor Desensitization (IUPHAR)
- **Desensitization kinetics:** Adaptation and gain control
- **Receptor recycling rates:** Dynamic range modulation
- **Allosteric modulation:** Context-dependent computation

**Computational Value:** Nonlinear gain control, adaptation, temporal filtering

##### Protein Complexes (Reactome)
- **Postsynaptic density composition:** Scaffold-based computation
- **Presynaptic active zone:** Release probability regulation
- **Receptor clustering:** Synaptic strength heterogeneity

**Computational Value:** Spatial organization and localized computation

#### Tier 3: Advanced Features (Nice-to-Have)

##### Disease Variants (Reactome, IUPHAR)
- **Channelopathies:** Altered excitability
- **Receptor mutations:** Modified pharmacology
- **Signaling pathway disruptions:** Circuit dysfunction

**Computational Value:** Perturbation studies, robustness analysis

##### Drug Modulation (IUPHAR, KEGG)
- **Psychoactive drug targets:** Neuromodulation mechanisms
- **Cognitive enhancers:** Performance optimization
- **Anesthetics:** Consciousness mechanisms

**Computational Value:** Understanding controllability and intervention points

### Specific Mechanisms for Predictive Coding Implementation

#### Prediction Error Computation

```
Required Data:
├── NMDA receptor kinetics (IUPHAR: Target 1479-1482)
│   └── Voltage-dependent gating → nonlinear integration
├── Layer-specific connectivity (GO: synaptic organization terms)
│   └── Feedforward vs. feedback distinction
├── Dendritic integration (Reactome: R-HSA-9619229)
│   └── Active dendrites with voltage-gated channels
└── Calcium-dependent plasticity (KEGG: hsa04020, hsa04720)
    └── Error-driven weight updates
```

#### Precision Weighting

```
Required Data:
├── Neuromodulator systems (IUPHAR: dopamine, serotonin, norepinephrine targets)
│   └── Gain modulation of prediction errors
├── GABA inhibition (IUPHAR: GABA-A receptor kinetics)
│   └── Precision-weighted inhibition
├── Astrocyte signaling (Reactome: gliotransmission)
│   └── Slow modulation of synaptic strength
└── Adenosine system (KEGG: purinergic signaling)
    └── Metabolic gating of precision
```

#### Hierarchical Message Passing

```
Required Data:
├── Layer-specific receptor expression (GO annotations + gene expression)
│   └── Different computational primitives per layer
├── Cortico-cortical pathways (Reactome: axon guidance)
│   └── Anatomical hierarchy
├── Thalamo-cortical loops (KEGG: sensory transduction pathways)
│   └── Feedforward sensory drive
└── Cortical microcircuits (Reactome: neuronal system)
    └── Canonical computation within layers
```

### Prioritized Extraction Roadmap

#### Phase 1: Core Synaptic Mechanisms (Weeks 1-2)
```
1. Extract from IUPHAR:
   - All NMDA, AMPA, GABA-A receptor parameters
   - Voltage-gated Na+, K+, Ca2+ channel kinetics
   - Neuromodulator receptor affinities (D1, D2, 5-HT1A, etc.)

2. Extract from KEGG:
   - hsa04724 (Glutamatergic synapse) - complete KGML
   - hsa04727 (GABAergic synapse) - complete KGML
   - hsa04720 (Long-term potentiation) - complete KGML

3. Cross-reference with GO:
   - Map all components to GO molecular functions
   - Identify hierarchical relationships
```

#### Phase 2: Signaling Cascades (Weeks 3-4)
```
4. Extract from Reactome:
   - Synaptic vesicle cycle (complete stoichiometry)
   - Calcium signaling (all reactions with kinetics)
   - MAPK/ERK pathway (complete network)
   - CaMKII activation (plasticity induction)

5. Extract from KEGG:
   - hsa04010 (MAPK signaling)
   - hsa04020 (Calcium signaling)
   - hsa04151 (PI3K-Akt signaling)

6. Cross-reference:
   - Reactome reactions → KEGG pathways
   - Time-scale separation (fast vs. slow processes)
```

#### Phase 3: Metabolic Constraints (Weeks 5-6)
```
7. Extract from KEGG:
   - hsa00010 (Glycolysis)
   - hsa00020 (TCA cycle)
   - hsa00190 (Oxidative phosphorylation)
   - Neurotransmitter synthesis pathways

8. Energy budget calculations:
   - ATP costs of synaptic transmission
   - Action potential metabolic load
   - Plasticity energy requirements
```

#### Phase 4: Integration and Validation (Weeks 7-8)
```
9. Build integrated dataset:
   - Link all entities across databases
   - Resolve conflicts in parameters
   - Create unified ID mapping

10. Validate completeness:
    - Check coverage of key mechanisms
    - Identify missing parameters
    - Document data quality issues

11. Create computational model templates:
    - ODE systems for signaling pathways
    - Channel gating equations
    - Plasticity rules from pathway data
```

### Key Metrics for Data Quality

| Metric | Target | Assessment Method |
|--------|--------|-------------------|
| **Parameter Coverage** | >80% for Tier 1 mechanisms | Count available kinetic constants |
| **Cross-Reference Completeness** | >90% entities linked | Check ID mapping success rate |
| **Temporal Range** | Microseconds to hours | Verify time-scale coverage |
| **Spatial Scales** | Molecular to network | Check compartmentalization |
| **Taxonomic Specificity** | Human > 90%, Rodent > 70% | Filter by organism |
| **Citation Recency** | Median < 5 years | Check PubMed dates |

---

## Appendix A: Quick Reference - Essential API Calls

### GO: Get Synaptic Plasticity Terms
```bash
curl http://api.geneontology.org/api/bioentity/function/GO:0048167
```

### Reactome: Get LTP Pathway
```bash
curl https://reactome.org/ContentService/data/query/R-HSA-3371556
```

### KEGG: Get Glutamatergic Synapse
```bash
curl https://rest.kegg.jp/get/hsa04724/json
curl https://rest.kegg.jp/get/hsa04724/kgml
```

### IUPHAR: Get NMDA Receptor Data
```bash
curl https://www.guidetopharmacology.org/services/targets/1479/interactions?affinityType=pKi
```

---

## Appendix B: Critical Missing Data

### Parameters Generally NOT Available
1. **Single-Channel Conductances:** Limited in IUPHAR, need patch-clamp literature
2. **Spatial Diffusion Constants:** Not in databases, need biophysics papers
3. **Protein Copy Numbers:** Limited annotations, need proteomics
4. **Receptor Trafficking Rates:** Sparse in Reactome, need live-cell imaging papers
5. **3D Structural Dynamics:** Not in scope for these databases, need MD simulations

### Workarounds
- **Supplement with BioNumbers database** for cellular concentrations
- **BRENDA enzyme database** for detailed kinetics (Km, kcat, Ki)
- **BindingDB, ChEMBL** for additional binding affinity data
- **Allen Brain Atlas** for spatial expression patterns
- **Literature mining** for missing quantitative parameters

---

## Appendix C: Useful External Tools

### API Clients and Libraries
- **Python:** `bioservices`, `requests`, `reactome2py`, `KEGGREST`
- **R:** `KEGGREST`, `reactome.db`, `GO.db`, `biomaRt`
- **JavaScript:** `fetch`, `axios` for direct REST calls

### Data Integration Frameworks
- **Bioconductor:** Comprehensive R framework for all databases
- **Biopython:** GO, KEGG parsers
- **SPARQL:** For RDF/linked data queries (GO, IUPHAR RDF)

### Visualization
- **Cytoscape:** Network visualization (import from Reactome, KEGG)
- **Pathway Commons:** Integrated pathway viewer
- **Escher:** Metabolic map builder (KEGG data)

---

## Document Sources

### Gene Ontology
- [Gene Ontology Resource](https://geneontology.org/)
- [Programmatic Access to Gene Ontology](https://geneontology.org/docs/tools-guide/)
- [GO API Documentation](http://api.geneontology.org/)
- [Download Ontology](https://geneontology.org/docs/download-ontology/)
- [Gene Ontology Relations](https://geneontology.org/docs/ontology-relations/)

### Reactome
- [Reactome Content Service](https://reactome.org/dev/content-service)
- [Reactome API Documentation](https://reactome.org/ContentService/)
- [Reactome Downloads](https://reactome.org/download-data)
- [Reactome Release Calendar](https://reactome.org/about/release-calendar)

### KEGG
- [KEGG API Manual](https://www.kegg.jp/kegg/rest/keggapi.html)
- [KEGG REST API](https://www.kegg.jp/kegg/rest/)
- [KEGG Pathway Database](https://www.genome.jp/kegg/pathway.html)
- [KEGG Release Notes](https://www.genome.jp/kegg/docs/relnote.html)

### IUPHAR/BPS Guide to Pharmacology
- [GtoPdb Web Services](https://www.guidetopharmacology.org/webServices.jsp)
- [GtoPdb Downloads](https://www.guidetopharmacology.org/download.jsp)
- [GtoPdb Home](https://www.guidetopharmacology.org/)
- [IUPHAR/BPS Guide to PHARMACOLOGY in 2024 - NAR](https://academic.oup.com/nar/article/52/D1/D1438/7332061)

---

**End of Document**

*Last Updated: 2025-12-10*
*Compiled by: Claude Code Research Assistant*
*For: BioFormulas Database Architecture Project*
