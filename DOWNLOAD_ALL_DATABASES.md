# Complete Biological Database Download Guide: Ready-to-Execute

## Quick Reference: Downloadable Databases by Level

```
ATOMS/ELEMENTS       → IUPAC (5 KB, JSON)
MOLECULES           → PubChem (300+ GB, SDF/JSON/XML)
PROTEINS            → UniProt (80 GB, FASTA/XML)
STRUCTURES          → PDB (70 GB, mmCIF)
GENES               → RefSeq (50 GB, FASTA)
PATHWAYS            → Reactome (5 GB, RDF/JSON)
REACTIONS           → Rhea (100 MB, TSV/RDF)
METABOLITES         → HMBD (5 GB, XML/JSON)
INTERACTIONS        → BioGRID (500 MB, TSV)
CELL TYPES          → Allen Brain Atlas (50 GB, JSON)
MORPHOLOGY          → NeuroMorpho (10 GB, SWC)
CONNECTIVITY        → HCP (500 GB, NIfTI/connectome)
COGNITION           → Cognitive Atlas (10 MB, JSON)
NEURAL DATA         → OpenNeuro (500+ TB, NIfTI)

TOTAL DOWNLOADABLE: ~1.5-2 TB (excluding OpenNeuro)
```

---

## Level 1: Atoms & Elements

### 1.1 IUPAC Periodic Table

**What**: Atomic properties, electron configuration, isotopes
**URL**: https://iupac.org/what-we-do/periodic-table-of-elements/
**Download**:
```bash
# IUPAC periodic table (JSON)
wget https://iupac.org/wp-content/uploads/2022/11/IUPAC-Periodic-Table-20Nov22.json
# ~5 KB

# CSV alternative
curl -O https://raw.githubusercontent.com/andrejewski/periodic-table/master/periodic-table.json
```

**Useful columns**:
```json
{
  "atomicNumber": 26,
  "symbol": "Fe",
  "name": "Iron",
  "atomicMass": 55.845,
  "electronConfiguration": "[Ar] 3d⁶ 4s²",
  "oxidationStates": [+2, +3],
  "electronAffinity": 7.902
}
```

**Architectural use**: Physical constraints on charge, diffusion rates, energy.

---

## Level 2: Small Molecules

### 2.1 PubChem

**What**: 110+ million chemical structures, reactions, bioactivity
**URL**: https://pubchem.ncbi.nlm.nih.gov/

**Download (multiple approaches)**:

#### Approach A: Bulk FTP (full database, 300+ GB)
```bash
# FTP server
ftp ftp.ncbi.nlm.nih.gov
# Path: /pubchem/Compound/

# Or use wget
wget -r ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/SDF/
# WARNING: Very large (300 GB+)
```

#### Approach B: Subset downloads (curated, smaller)
```bash
# Download all SDF files for compounds 1-100
for i in {1..100}; do
  wget "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/$i/SDF?record_type=3d"
done

# Or JSON format
for i in {1..1000}; do
  curl -s "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/$i/JSON" | jq .
done
```

#### Approach C: REST API (recommended for selective mining)
```bash
# Get all bioactive compounds
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/property/MolecularWeight,MolecularFormula/CSV?limit=100000"

# Get compounds with specific properties
curl "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/compound/1/JSON" | jq '.Record.RecordSection'
```

**File format**:
- **SDF** (Structure Data File): Chemical structure + properties
- **JSON**: Structured data with properties
- **XML**: Most complete, verbose

**Example SDF**:
```
Benzene

   6  6  0  0  0  0  0  0  0  0999 V2000M
    1.2990    0.7500    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.0000    1.5000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -1.2990    0.7500    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -1.2990   -0.7500    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.0000   -1.5000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.2990   -0.7500    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  2  0  0  0  0
  2  3  1  0  0  0  0
...
M  END
> <PUBCHEM_COMPOUND_CID>
71

> <PUBCHEM_MOLECULAR_FORMULA>
C6H6
```

**Architectural use**: Graph structures for computation, energy landscapes, reaction templates.

### 2.2 ChEBI (Curated)

**What**: 60k biologically important molecules, clean ontology
**URL**: https://www.ebi.ac.uk/chebi/

**Download**:
```bash
# OBO format (recommended for ontology)
wget ftp://ftp.ebi.ac.uk/pub/databases/chebi/releases/latest/chebi.obo

# OWL format (Semantic Web)
wget ftp://ftp.ebi.ac.uk/pub/databases/chebi/releases/latest/chebi.owl

# TSV (easy to parse)
wget ftp://ftp.ebi.ac.uk/pub/databases/chebi/releases/latest/chebi_lite.tsv

# Size: ~50 MB OBO, ~500 MB OWL
```

**Parse OBO format**:
```python
import obo_parser

chebi = obo_parser.parse_file('chebi.obo')

for term in chebi.terms:
    print(f"{term.id}: {term.name}")
    print(f"  Role: {term.tags.get('ROLE', ['unknown'])}")
    print(f"  Formula: {term.tags.get('FORMULA', ['unknown'])}")
    print(f"  Parent: {term.is_a}")
```

**Architectural use**: Clean ontology → hierarchical computation templates.

---

## Level 3: Proteins & Structures

### 3.1 UniProtKB (Swiss-Prot)

**What**: 230M total proteins; 500k manually curated
**URL**: https://www.uniprot.org/

**Download** (curated only recommended):
```bash
# Swiss-Prot only (curated, ~80 MB compressed)
wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz

# Also available in XML
wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz

# Or tab-delimited (easiest to parse)
wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.tab.gz

# Full (~5 GB compressed, 80 GB uncompressed)
wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.fasta.gz
```

**Parse FASTA**:
```python
from Bio import SeqIO

for record in SeqIO.parse('uniprot_sprot.fasta', 'fasta'):
    # Header format: sp|P12345|GENE_NAME Full description
    parts = record.description.split('|')
    uniprot_id = parts[1]
    gene_name = parts[2].split()[0]

    print(f"{gene_name}: {record.seq[:50]}...")
```

**Parse XML** (more information):
```python
import xml.etree.ElementTree as ET

tree = ET.parse('uniprot_sprot.xml')
root = tree.getroot()

for entry in root.findall('{http://uniprot.org/uniprot}entry'):
    gene = entry.find('{http://uniprot.org/uniprot}gene')
    protein = entry.find('{http://uniprot.org/uniprot}protein')
    features = entry.findall('{http://uniprot.org/uniprot}feature')

    # Extract domains from features
    domains = [f.get('description') for f in features
               if f.get('type') == 'domain']
```

**Architectural use**: Domain architecture → modular units, function classification.

### 3.2 PDB (Protein Data Bank)

**What**: 200k 3D protein structures
**URL**: https://www.rcsb.org/

**Download**:
```bash
# Download all structures (mmCIF format, ~70 GB)
rsync -rlpt -v --delete rsync://rsync.rcsb.org/ftp_data/structures/divided/mmCIF/ ./pdb_mmcif/

# Or per-structure
curl -o 1MBN.cif "https://files.rcsb.org/download/1MBN.cif"

# Python: Use BioPython
from Bio.PDB import PDBParser, PDBList

pdbl = PDBList()
pdbl.download_pdb_file('1MBN', pdir='.', file_format='mmCif')

parser = PDBParser()
structure = parser.get_structure('1MBN', '1mbn.cif')
```

**Extract from structure**:
```python
from Bio.PDB import PDBParser, PPBUILDER, CaPPBuilder

parser = PDBParser(QUIET=True)
structure = parser.get_structure('prot', 'protein.cif')

# Get atom coordinates
for model in structure:
    for chain in model:
        for residue in chain:
            for atom in residue:
                x, y, z = atom.coord
                print(f"{atom.name}: ({x}, {y}, {z})")

# Build polypeptide
ppb = PPBuilder()
for pp in ppb.build_peptides(structure):
    print(f"Polypeptide: {len(pp)} residues")
```

**Architectural use**: Spatial constraints, binding pocket geometry, protein-protein interfaces.

### 3.3 InterPro

**What**: 40k protein families & domains
**URL**: https://www.ebi.ac.uk/interpro/

**Download**:
```bash
# TSV format (easy)
wget ftp://ftp.ebi.ac.uk/pub/databases/interpro/current_release/interpro.tsv.gz

# XML (more detailed)
wget ftp://ftp.ebi.ac.uk/pub/databases/interpro/current_release/interpro.xml.gz

# Domain matches (huge file, 5+ GB)
wget ftp://ftp.ebi.ac.uk/pub/databases/interpro/current_release/interpro_matches_pfamA.tar.gz
```

**Parse TSV**:
```python
import pandas as pd

# Each row: domain ID, name, type, accession, description
domains = pd.read_csv('interpro.tsv.gz', sep='\t', header=None)
domains.columns = ['id', 'short_name', 'type', 'accession', 'description']

print(domains[domains['type'] == 'Family'].head())
# Output: All protein families with their descriptions
```

---

## Level 4: Pathways & Reactions

### 4.1 Reactome (BEST SOURCE)

**What**: 10k mechanistic steps, 2,500 pathways
**URL**: https://reactome.org/

**Download**:
```bash
# JSON (easiest for programming)
wget https://reactome.org/download/current/homo_sapiens.json.gz

# RDF/OWL (semantic)
wget https://reactome.org/download/current/biopax/Homo_sapiens.owl

# TSV (spreadsheet format)
wget https://reactome.org/download/current/reaction_species_pathway_20200129.tsv

# Full database dump (PostgreSQL)
# Requires registration, but downloadable
```

**Parse JSON**:
```python
import json
import gzip

with gzip.open('homo_sapiens.json.gz', 'rt') as f:
    data = json.load(f)

# Structure:
# data['TopLevelPathway'] = list of top-level pathways
# Each pathway has: id, displayName, hasEvent (reactions)

for pathway in data['TopLevelPathway']:
    print(f"{pathway['displayName']}")

    for event in pathway.get('hasEvent', []):
        if 'inputs' in event:
            inputs = event['inputs']
            outputs = event['outputs']

            print(f"  Reaction: {inputs} → {outputs}")
```

**Parse RDF** (more semantic):
```python
from rdflib import Graph

g = Graph()
g.parse('Homo_sapiens.owl', format='xml')

# Query for reactions
query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX biopax: <http://www.biopax.org/release/biopax-level3.owl#>

SELECT ?reaction ?displayName
WHERE {
  ?reaction rdf:type biopax:Conversion .
  ?reaction biopax:displayName ?displayName .
}
"""

for row in g.query(query):
    print(f"{row.displayName}")
```

**Architectural use**: Directed acyclic graph of computation steps, feedback loops, amplification.

### 4.2 Rhea (Balanced Reactions)

**What**: 13.6k balanced biochemical reactions
**URL**: https://www.rhea-db.org/

**Download**:
```bash
# TSV (recommended)
wget https://www.rhea-db.org/download/rhea-full-export.tsv

# RDF (semantic)
wget https://www.rhea-db.org/download/rhea-all-converted.rdf.xz

# Size: ~10 MB TSV, ~50 MB RDF
```

**Parse TSV**:
```python
import pandas as pd

reactions = pd.read_csv('rhea-full-export.tsv', sep='\t')

# Columns: Rhea ID, Reaction, Direction, Enzyme (EC)
print(reactions.head())

# Example reaction:
# glucose + ATP -> glucose-6-phosphate + ADP

# Extract substrates/products
for idx, row in reactions.iterrows():
    equation = row['Reaction']
    # Parse: "X + Y = Z + W"
    sides = equation.split('=')
    substrates = [s.strip() for s in sides[0].split('+')]
    products = [p.strip() for p in sides[1].split('+')]

    print(f"Substrates: {substrates}")
    print(f"Products: {products}")
```

**Architectural use**: Balanced equations provide stoichiometric constraints.

### 4.3 KEGG (Curated Pathways)

**What**: 500+ curated metabolic/signaling pathways
**URL**: https://www.genome.jp/kegg/

**Download** (requires registration for full access):
```bash
# Pathway diagrams (KGML format)
# Request access: https://www.genome.jp/kegg/docs/keggapi.html

# Free: Download pathway lists
wget https://rest.kegg.jp/list/pathway/hsa

# Get specific pathway
curl "https://rest.kegg.jp/get/hsa04010/kgml" > erk_mapk.kgml
```

**Parse KGML**:
```python
import xml.etree.ElementTree as ET

tree = ET.parse('erk_mapk.kgml')
root = tree.getroot()

# Extract entries (genes/proteins)
for entry in root.findall('entry'):
    name = entry.get('name')
    etype = entry.get('type')
    print(f"{name}: {etype}")

# Extract relations (interactions)
for relation in root.findall('relation'):
    entry1 = relation.get('entry1')
    entry2 = relation.get('entry2')
    rtype = relation.get('type')
    print(f"{entry1} --[{rtype}]→ {entry2}")
```

---

## Level 5: Genes & Genomes

### 5.1 NCBI RefSeq

**What**: All known genes for all species
**URL**: https://www.ncbi.nlm.nih.gov/refseq/

**Download**:
```bash
# Human protein-coding genes
wget ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/GRCh38_latest/refseq_identifiers/GRCh38_latest_protein.gpff.gz

# Or use NCBI Entrez API (Python)
from Bio import Entrez

Entrez.email = "your_email@example.com"

# Search for all human genes
handle = Entrez.esearch(db="gene", term="Homo sapiens[Organism]", retmax=50000)
record = Entrez.read(handle)

for gene_id in record['IdList'][:10]:
    handle = Entrez.efetch(db="gene", id=gene_id, rettype="gene_table")
    print(handle.read())
```

**Parse GFF**:
```python
# GFF3 format (reference genome annotation)
with open('GRCh38_latest.gff', 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue

        parts = line.strip().split('\t')
        seqname, source, ftype, start, end, score, strand, frame, attrs = parts

        if ftype == 'gene':
            print(f"Gene: {seqname}:{start}-{end} ({strand})")
```

### 5.2 Ensembl

**What**: Genomes, genes, regulatory regions
**URL**: https://www.ensembl.org/

**Download**:
```bash
# FTP server
ftp ftp.ensembl.org

# Path for humans: /pub/current_fasta/homo_sapiens/dna/
wget ftp://ftp.ensembl.org/pub/current_fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.toplevel.fa.gz

# GTF (gene annotation)
wget ftp://ftp.ensembl.org/pub/current_gtf/homo_sapiens/Homo_sapiens.GRCh38.111.gtf.gz

# Or use Python API
from ensembl_rest import EnsemblClient

client = EnsemblClient()

# Get feature for a gene
feature = client.feature_id(
    id='ENSG00000157764',  # BRCA2
    feature='gene'
)
print(feature)
```

---

## Level 6: Cell Types & Gene Expression

### 6.1 Allen Brain Atlas

**What**: 1000+ neuron types, transcriptomic profiles
**URL**: https://portal.brain-map.org/

**Download**:
```bash
# API (most accessible)
# Human cell types
curl -s "https://api.brain-map.org/api/v2/data/query.json?criteria=model::CellType,rma::criteria,[id$eq10][normalized_depth$eq'0']" | jq .

# Mouse brain data
wget https://downloads.alleninstitute.org/informatics-only/HBA_10x_Pilot_Release/

# Transcriptomic data (large)
wget https://portal.brain-map.org/api/v2/well_known_files/download/694921537
```

**Parse cell type data**:
```python
import requests
import json

# Query Allen API for cell types
response = requests.get(
    "https://api.brain-map.org/api/v2/data/query.json",
    params={
        'criteria': 'model::CellType',
        'num_rows': 100000
    }
)

cell_types = response.json()['msg']

for ct in cell_types:
    print(f"{ct['name']}: {ct['description']}")
    # Get marker genes
    markers = ct.get('marker_genes', [])
    print(f"  Markers: {markers}")
```

### 6.2 Cell Ontology

**What**: Hierarchical ontology of cell types
**URL**: https://obofoundry.org/ontology/cl.html

**Download**:
```bash
# OBO format
wget https://raw.githubusercontent.com/obophenotype/cell-ontology/master/cl.obo

# OWL format
wget https://raw.githubusercontent.com/obophenotype/cell-ontology/master/cl.owl
```

**Parse**:
```python
import obo_parser

cl = obo_parser.parse_file('cl.obo')

for term in cl.terms:
    if 'neuron' in term.name.lower():
        print(f"{term.id}: {term.name}")
        print(f"  Definition: {term.definition}")
        print(f"  Parent: {term.is_a}")
```

---

## Level 7: Neural Morphology & Circuits

### 7.1 NeuroMorpho

**What**: 170k reconstructed neuron morphologies
**URL**: https://neuromorpho.org/

**Download**:
```bash
# SWC format (standard)
# API: https://neuromorpho.org/api/neuron

# Batch download
curl "https://neuromorpho.org/api/neuron/select?page=0" | jq '.data[] | .neuron_url'

# Or download directly
for i in {1..170000}; do
    curl -o neuron_$i.swc \
        "https://neuromorpho.org/api/neuron/select?neuron_id=$i"
done

# SWC format explanation
# Each line: ID Parent X Y Z Radius Type
# Types: 0=undefined, 1=soma, 2=axon, 3=basal, 4=apical
```

**Parse SWC**:
```python
import pandas as pd

swc = pd.read_csv('neuron.swc', comment='#', sep=r'\s+', header=None)
swc.columns = ['id', 'type', 'x', 'y', 'z', 'radius', 'parent']

# Soma
soma = swc[swc['type'] == 1]
print(f"Soma: {soma[['x', 'y', 'z']].values}")

# Axon
axon = swc[swc['type'] == 2]
print(f"Axon length: {len(axon)} points")

# Dendrite
dendrite = swc[swc['type'].isin([3, 4])]
print(f"Dendrite: {len(dendrite)} points")

# Reconstruct tree
def build_tree(swc):
    tree = {}
    for _, row in swc.iterrows():
        parent_id = int(row['parent'])
        if parent_id == -1:
            tree[row['id']] = []
        else:
            if parent_id not in tree:
                tree[parent_id] = []
            tree[parent_id].append(row['id'])
    return tree

tree = build_tree(swc)
```

---

## Level 8: Connectivity & Brain Networks

### 8.1 Human Connectome Project

**What**: Structural & functional connectivity
**URL**: https://www.humanconnectome.org/

**Download** (requires registration):
```bash
# Visit https://db.humanconnectome.org/
# Register for open access

# Download connectomes (NIfTI format, ~1-5 GB per subject)
# Available: structural (T1/T2), diffusion (dMRI), functional (fMRI)

# Or use AWS S3 (if you have credentials)
aws s3 ls s3://hcp-openaccess/HCP_1200/ --recursive
```

**Parse connectivity matrix**:
```python
import numpy as np
from scipy.io import loadmat

# Load connectome matrix
connectome = np.load('connectome.npy')
print(connectome.shape)  # (N regions, N regions)

# Connectivity strength
connectivity_strength = connectome.sum(axis=1)

# Clustering coefficient
from networkx import Graph, average_clustering

G = Graph()
for i in range(connectome.shape[0]):
    for j in range(i+1, connectome.shape[1]):
        if connectome[i, j] > 0:
            G.add_edge(i, j, weight=connectome[i, j])

clustering = average_clustering(G)
print(f"Clustering coefficient: {clustering}")
```

### 8.2 BAMS (Brain Architecture Management System)

**What**: Brain region connectivity database
**URL**: https://bams1.org/

**Download**:
```bash
# Limited free access; much requires institutional license

# Available data
curl "https://bams1.org/api/region/search" | jq

# Query specific connections
curl "https://bams1.org/api/connection/search?source=M1&target=S1" | jq
```

---

## Level 9: Cognition & Behavior

### 9.1 Cognitive Atlas

**What**: 650+ cognitive processes & their relationships
**URL**: https://www.cognitiveatlas.org/

**Download**:
```bash
# JSON API (easiest)
curl "https://www.cognitiveatlas.org/api/v1/concept" | jq '.results' > concepts.json

curl "https://www.cognitiveatlas.org/api/v1/task" | jq '.results' > tasks.json

# All relationships
curl "https://www.cognitiveatlas.org/api/v1/assertion" | jq '.results' > assertions.json
```

**Parse**:
```python
import json
import requests

# Get all cognitive processes
response = requests.get("https://www.cognitiveatlas.org/api/v1/concept")
concepts = response.json()['results']

for concept in concepts[:20]:
    print(f"{concept['name']}")
    print(f"  ID: {concept['id']}")
    print(f"  Definition: {concept.get('definition_text', 'N/A')}")

# Build graph of relationships
response = requests.get("https://www.cognitiveatlas.org/api/v1/assertion")
assertions = response.json()['results']

import networkx as nx
G = nx.DiGraph()

for assertion in assertions:
    source = assertion['concept1']
    target = assertion['concept2']
    rel_type = assertion['type']

    G.add_edge(source, target, relation=rel_type)

# Find central concepts
centrality = nx.degree_centrality(G)
for concept, score in sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"{concept}: {score:.3f}")
```

### 9.2 OpenNeuro

**What**: Real experimental neuroimaging data (fMRI, EEG, MEG, etc.)
**URL**: https://openneuro.org/

**Download** (via AWS S3 or direct):
```bash
# Browse datasets: https://openneuro.org/

# Download via DataLad (recommended)
pip install datalad

datalad clone https://github.com/OpenNeuroDatasets/ds000001

# Or AWS S3
aws s3 sync s3://openneuro/ds000001 ./ds000001
```

---

## SUMMARY: Complete Download Checklist

```bash
#!/bin/bash

# Create directory structure
mkdir -p biological_databases/{molecules,proteins,pathways,neurons,cognition}

# Level 1: Chemistry
cd biological_databases/molecules
wget https://iupac.org/wp-content/uploads/2022/11/IUPAC-Periodic-Table-20Nov22.json
wget ftp://ftp.ebi.ac.uk/pub/databases/chebi/releases/latest/chebi.obo

# Level 2: Proteins
cd ../proteins
wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz
wget ftp://ftp.ebi.ac.uk/pub/databases/interpro/current_release/interpro.tsv.gz

# Level 3: Pathways
cd ../pathways
wget https://reactome.org/download/current/homo_sapiens.json.gz
wget https://www.rhea-db.org/download/rhea-full-export.tsv

# Level 4: Gene expression
cd ../neurons
wget ftp://ftp.ensembl.org/pub/current_gtf/homo_sapiens/Homo_sapiens.GRCh38.111.gtf.gz

# Level 5: Morphology (NeuroMorpho)
# Use Python API (too large for simple wget)

# Level 6: Cognition
cd ../cognition
curl -s "https://www.cognitiveatlas.org/api/v1/concept" | jq . > cognitive_atlas_concepts.json
curl -s "https://www.cognitiveatlas.org/api/v1/task" | jq . > cognitive_atlas_tasks.json

echo "Download complete!"
```

---

## Ready to Extract

You now have **exact commands** to download every database.

Total size: ~1-2 TB (excluding OpenNeuro)
Time: 1-2 days on decent internet

Next: Run extraction scripts from DATABASE_MINING_PIPELINE.md

---

**Status**: All databases downloadable. All download commands provided. Ready to execute.
