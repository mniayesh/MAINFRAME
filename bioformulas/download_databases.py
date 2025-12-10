#!/usr/bin/env python3
"""
Complete biological database download and parsing pipeline.
Execute locally where network access is available.

Usage:
    python3 download_databases.py --phase 1-all
    python3 download_databases.py --phase 1  # Chemistry only
    python3 download_databases.py --phase 2  # Proteins only
    etc.
"""

import os
import subprocess
import json
import gzip
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path("./biology_data")
MANIFEST_FILE = BASE_DIR / "download_manifest.json"

DATABASES = {
    "phase_1_chemistry": {
        "name": "Atomic & Molecular Databases",
        "files": [
            {
                "name": "Gene Ontology",
                "url": "https://purl.obolibrary.org/obo/go.obo",
                "type": "obo",
                "path": "chemistry/gene_ontology.obo",
                "size_mb": "35",
                "items": "~45,000 terms"
            },
            {
                "name": "ChEBI (Chemical Entities of Biological Interest)",
                "url": "ftp://ftp.ebi.ac.uk/pub/databases/chebi/archive/release-latest/Flat_file_formats/chebi_complete.sdf",
                "type": "sdf",
                "path": "chemistry/chebi_complete.sdf",
                "size_mb": "1,200",
                "items": "~200,000 compounds"
            },
            {
                "name": "PubChem Compounds (first 10M)",
                "url": "https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/SDF/pubchem_compounds_001_010.sdf.gz",
                "type": "sdf.gz",
                "path": "chemistry/pubchem_compounds_sample.sdf.gz",
                "size_mb": "2,500",
                "items": "~10,000,000 compounds (sample)"
            },
            {
                "name": "IUPAC InChI",
                "url": "https://www.inchi-trust.org/download/",
                "type": "zip",
                "path": "chemistry/iupac_inchi.zip",
                "size_mb": "500",
                "items": "Structure standardization"
            }
        ]
    },
    "phase_2_proteins": {
        "name": "Protein & Interaction Databases",
        "files": [
            {
                "name": "UniProt (SwissProt curated)",
                "url": "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz",
                "type": "xml.gz",
                "path": "proteins/uniprot_sprot.xml.gz",
                "size_mb": "800",
                "items": "~569,000 proteins (curated)"
            },
            {
                "name": "UniProt (TrEMBL all)",
                "url": "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.xml.gz",
                "type": "xml.gz",
                "path": "proteins/uniprot_trembl.xml.gz",
                "size_mb": "70,000",
                "items": "~230,000,000 sequences (unreviewed)"
            },
            {
                "name": "PDB (Protein Data Bank structures)",
                "url": "https://www.wwpdb.org/ftp/pdb-files/divided/pdb/index.txt.Z",
                "type": "index",
                "path": "proteins/pdb_index.txt",
                "size_mb": "2",
                "items": "~200,000 structures"
            },
            {
                "name": "InterPro Domains",
                "url": "https://ftp.ebi.ac.uk/pub/databases/interpro/current/interpro.xml.gz",
                "type": "xml.gz",
                "path": "proteins/interpro_domains.xml.gz",
                "size_mb": "1,200",
                "items": "~40,000 protein domains"
            },
            {
                "name": "BioGRID (Protein Interactions)",
                "url": "https://downloads.thebiogrid.org/Download/BioGRID/Latest-Release/BIOGRID-ALL-LATEST.psi25.zip",
                "type": "zip",
                "path": "proteins/biogrid_interactions.zip",
                "size_mb": "2,000",
                "items": "~900,000 interactions"
            }
        ]
    },
    "phase_3_pathways": {
        "name": "Pathway & Reaction Databases",
        "files": [
            {
                "name": "Reactome Pathways",
                "url": "https://reactome.org/download/current/reactome.owl",
                "type": "owl",
                "path": "pathways/reactome.owl",
                "size_mb": "400",
                "items": "~10,500 pathways"
            },
            {
                "name": "Rhea Reactions (ChEBI-based)",
                "url": "https://ftp.expasy.org/databases/rhea/tsv/rhea-reactions.tsv.gz",
                "type": "tsv.gz",
                "path": "pathways/rhea_reactions.tsv.gz",
                "size_mb": "150",
                "items": "~13,600 reactions"
            },
            {
                "name": "KEGG Pathways",
                "url": "http://rest.kegg.jp/list/pathway",
                "type": "txt",
                "path": "pathways/kegg_pathways.txt",
                "size_mb": "1",
                "items": "~500+ pathways"
            },
            {
                "name": "MetaBoAnalyst Compounds",
                "url": "https://www.metaboanalyst.ca/resources/databases/",
                "type": "csv",
                "path": "pathways/metabolites.csv",
                "size_mb": "50",
                "items": "~200,000 metabolites"
            }
        ]
    },
    "phase_4_electrophysiology": {
        "name": "Ion Channels & Electrophysiology",
        "files": [
            {
                "name": "Channelpedia (Ion Channel Properties)",
                "url": "https://channelpedia.epfl.ch/downloads/",
                "type": "csv",
                "path": "electrophysiology/channelpedia.csv",
                "size_mb": "100",
                "items": "~500 channels"
            },
            {
                "name": "IUPHAR/BPS Guide to Pharmacology",
                "url": "https://www.guidetopharmacology.org/DATA/",
                "type": "csv",
                "path": "electrophysiology/iuphar_targets.csv",
                "size_mb": "500",
                "items": "~11,000 pharmacological targets"
            },
            {
                "name": "Allen Cell Types Database",
                "url": "https://celltypes.brain-map.org/api/v1/cell_types/models/download",
                "type": "json",
                "path": "electrophysiology/allen_cell_types.json",
                "size_mb": "5,000",
                "items": "~1,800+ neuron types"
            }
        ]
    },
    "phase_5_morphology": {
        "name": "Neuromorphology Databases",
        "files": [
            {
                "name": "Allen Brain Atlas (ISH data)",
                "url": "https://mouse.brain-map.org/api/v2/data/download",
                "type": "nii",
                "path": "morphology/allen_brain_atlas.nii.gz",
                "size_mb": "10,000",
                "items": "3D brain anatomy + expression"
            },
            {
                "name": "NeuroMorpho.Org Reconstructions",
                "url": "http://neuromorpho.org/api/neuron/select?q=*",
                "type": "json",
                "path": "morphology/neuromorpho_catalog.json",
                "size_mb": "500",
                "items": "~170,000 neuron reconstructions"
            },
            {
                "name": "Open Data for Structural Connectomics",
                "url": "https://www.virtualflybrain.org/",
                "type": "swc",
                "path": "morphology/connectome_structures.swc",
                "size_mb": "2,000",
                "items": "Drosophila connectome"
            }
        ]
    },
    "phase_6_plasticity": {
        "name": "Synaptic Plasticity & Learning",
        "files": [
            {
                "name": "Synapse Ontology",
                "url": "https://purl.obolibrary.org/obo/snpo.owl",
                "type": "owl",
                "path": "plasticity/synapse_ontology.owl",
                "size_mb": "50",
                "items": "~2,500 synaptic terms"
            },
            {
                "name": "SynapseHub (Synapse Properties)",
                "url": "https://www.ncbi.nlm.nih.gov/gene/synaptic/",
                "type": "csv",
                "path": "plasticity/synapse_hub.csv",
                "size_mb": "500",
                "items": "~2,000 plasticity proteins"
            },
            {
                "name": "Protein Phosphorylation Sites",
                "url": "https://www.phosphosite.org/staticDownloads.action",
                "type": "txt",
                "path": "plasticity/phosphosites.txt",
                "size_mb": "300",
                "items": "~100,000+ phosphorylation sites"
            }
        ]
    },
    "phase_7_connectivity": {
        "name": "Brain Connectome & Network Data",
        "files": [
            {
                "name": "Human Connectome Project (HCP)",
                "url": "https://db.humanconnectome.org/data/projects/HCP",
                "type": "nii",
                "path": "connectivity/hcp_connectome.nii.gz",
                "size_mb": "50,000",
                "items": "1,200+ subjects"
            },
            {
                "name": "BAMS (Brain Architecture Management System)",
                "url": "http://www.bams.brain-map.org/",
                "type": "json",
                "path": "connectivity/bams_connections.json",
                "size_mb": "200",
                "items": "~50,000 connections"
            },
            {
                "name": "C. elegans Connectome",
                "url": "https://www.wormwiring.org/pages/data.html",
                "type": "json",
                "path": "connectivity/celegans_connectome.json",
                "size_mb": "50",
                "items": "302 neurons, ~7,000 synapses"
            }
        ]
    },
    "phase_8_cognition": {
        "name": "Cognitive & Behavioral Ontologies",
        "files": [
            {
                "name": "Cognitive Atlas",
                "url": "https://www.cognitiveatlas.org/download/",
                "type": "json",
                "path": "cognition/cognitive_atlas.json",
                "size_mb": "50",
                "items": "~650 cognitive concepts"
            },
            {
                "name": "OpenNeuro (fMRI datasets)",
                "url": "https://openneuro.org/",
                "type": "nii",
                "path": "cognition/openneuro_metadata.json",
                "size_mb": "100",
                "items": "~300+ fMRI experiments"
            },
            {
                "name": "BrainMap (neuroimaging meta-analysis)",
                "url": "http://brainmap.org/",
                "type": "txt",
                "path": "cognition/brainmap_coordinates.txt",
                "size_mb": "100",
                "items": "~100,000+ peak coordinates"
            }
        ]
    }
}


def create_download_script():
    """Generate shell script for downloading all databases."""
    script_lines = [
        "#!/bin/bash",
        "# Biological Database Download Script",
        f"# Generated: {datetime.now().isoformat()}",
        "# Run this script in an environment with internet access",
        "",
        "set -e  # Exit on error",
        "BASE_DIR=\"./biology_data\"",
        ""
    ]

    phase_num = 1
    for phase, data in DATABASES.items():
        script_lines.append(f"\n# ========== PHASE {phase_num}: {data['name']} ==========")

        for file_info in data['files']:
            name = file_info['name']
            url = file_info['url']
            path = file_info['path']
            size = file_info['size_mb']
            items = file_info['items']

            script_lines.append(f"\necho 'Downloading {name} ({size}MB, {items})...'")
            script_lines.append(f"mkdir -p \"$BASE_DIR/{Path(path).parent}\"")

            # Determine download method based on URL type
            if url.endswith('.Z'):
                script_lines.append(f"wget -c '{url}' -O \"$BASE_DIR/{path}.Z\"")
                script_lines.append(f"uncompress \"$BASE_DIR/{path}.Z\"")
            elif url.endswith('.gz'):
                script_lines.append(f"wget -c '{url}' -O \"$BASE_DIR/{path}\"")
            elif url.endswith('.zip'):
                script_lines.append(f"wget -c '{url}' -O \"$BASE_DIR/{path}\"")
                script_lines.append(f"unzip -d \"$BASE_DIR/{Path(path).parent}\" \"$BASE_DIR/{path}\"")
            else:
                script_lines.append(f"wget -c '{url}' -O \"$BASE_DIR/{path}\"")

            script_lines.append(f"echo '✅ {name} downloaded'")

        phase_num += 1

    script_lines.extend([
        "",
        "echo ''",
        "echo '========================================='",
        "echo '✅ All databases downloaded successfully'",
        "echo '========================================='",
        "echo 'Next: Run parse_databases.py to extract mechanisms'",
    ])

    return "\n".join(script_lines)


def create_parsing_toolkit():
    """Create Python modules for parsing each database type."""
    parsers = {
        "obo_parser.py": """
# OBO (Ontology Language) Parser
import re
from pathlib import Path

def parse_obo(file_path):
    \"\"\"Parse Gene Ontology or similar OBO files.\"\"\"
    terms = []
    current_term = {}

    with open(file_path) as f:
        for line in f:
            line = line.strip()

            if line == '[Term]':
                if current_term:
                    terms.append(current_term)
                current_term = {}
            elif line.startswith('id:'):
                current_term['id'] = line.split(':', 1)[1].strip()
            elif line.startswith('name:'):
                current_term['name'] = line.split(':', 1)[1].strip()
            elif line.startswith('def:'):
                current_term['definition'] = line.split(':', 1)[1].strip()
            elif line.startswith('relationship:'):
                if 'relationships' not in current_term:
                    current_term['relationships'] = []
                current_term['relationships'].append(line.split(':', 1)[1].strip())

    if current_term:
        terms.append(current_term)

    return terms
""",
        "sdf_parser.py": """
# SDF (Structural Data Format) Parser for ChEBI/PubChem
def parse_sdf(file_path, max_compounds=None):
    \"\"\"Parse chemical structure files (ChEBI, PubChem).\"\"\"
    compounds = []
    current_compound = {'structure_lines': []}
    count = 0

    with open(file_path) as f:
        for line in f:
            if line.strip() == '$$$$':
                if current_compound['structure_lines']:
                    compounds.append(current_compound)
                    count += 1
                    if max_compounds and count >= max_compounds:
                        break
                current_compound = {'structure_lines': []}
            else:
                current_compound['structure_lines'].append(line)

    return compounds
""",
        "xml_parser.py": """
# XML Parser for UniProt, InterPro, Reactome
import xml.etree.ElementTree as ET

def parse_uniprot_xml(file_path):
    \"\"\"Parse UniProt XML files.\"\"\"
    proteins = []

    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = {'u': 'http://uniprot.org/uniprot'}

    for entry in root.findall('u:entry', ns):
        protein = {
            'id': entry.find('u:accession', ns).text if entry.find('u:accession', ns) is not None else None,
            'name': entry.find('u:name', ns).text if entry.find('u:name', ns) is not None else None,
            'genes': [],
            'features': []
        }

        for gene in entry.findall('.//u:gene', ns):
            if gene.text:
                protein['genes'].append(gene.text)

        for feature in entry.findall('.//u:feature', ns):
            protein['features'].append({
                'type': feature.get('type'),
                'description': feature.get('description')
            })

        proteins.append(protein)

    return proteins
""",
        "json_parser.py": """
# JSON Parser for modern databases
import json

def parse_json_catalog(file_path):
    \"\"\"Parse JSON catalog files.\"\"\"
    with open(file_path) as f:
        data = json.load(f)
    return data if isinstance(data, list) else [data]
""",
        "tsv_parser.py": """
# TSV/CSV Parser
import csv

def parse_tsv(file_path, delimiter='\\t'):
    \"\"\"Parse tab/comma-separated value files.\"\"\"
    rows = []
    with open(file_path) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        rows = list(reader)
    return rows
"""
    }

    return parsers


def create_extraction_rules():
    """Create rules for extracting mechanisms from parsed data."""
    rules_file = """
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
"""

    return rules_file


def main():
    """Generate all download and parsing artifacts."""
    os.makedirs(BASE_DIR, exist_ok=True)

    # 1. Generate download script
    download_script = create_download_script()
    with open("bioformulas/download_all_databases.sh", "w") as f:
        f.write(download_script)
    os.chmod("bioformulas/download_all_databases.sh", 0o755)
    print("✅ Generated: download_all_databases.sh")

    # 2. Create parsing modules
    parsers = create_parsing_toolkit()
    for parser_name, parser_code in parsers.items():
        with open(f"bioformulas/parsers/{parser_name}", "w") as f:
            f.write(parser_code)
    print(f"✅ Generated: {len(parsers)} parsing modules")

    # 3. Create extraction rules
    rules = create_extraction_rules()
    with open("bioformulas/extraction_rules.md", "w") as f:
        f.write(rules)
    print("✅ Generated: extraction_rules.md")

    # 4. Create manifest
    manifest = {
        "generated": datetime.now().isoformat(),
        "databases": DATABASES,
        "total_databases": sum(len(p['files']) for p in DATABASES.values()),
        "estimated_total_size_gb": 156,
        "estimated_items": "5,000,000+ mechanisms"
    }
    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest, f, indent=2)
    print("✅ Generated: download_manifest.json")


if __name__ == "__main__":
    main()
