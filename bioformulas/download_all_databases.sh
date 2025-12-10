#!/bin/bash
# Biological Database Download Script
# Generated: 2025-12-10T01:05:53.663820
# Run this script in an environment with internet access

set -e  # Exit on error
BASE_DIR="./biology_data"


# ========== PHASE 1: Atomic & Molecular Databases ==========

echo 'Downloading Gene Ontology (35MB, ~45,000 terms)...'
mkdir -p "$BASE_DIR/chemistry"
wget -c 'https://purl.obolibrary.org/obo/go.obo' -O "$BASE_DIR/chemistry/gene_ontology.obo"
echo '✅ Gene Ontology downloaded'

echo 'Downloading ChEBI (Chemical Entities of Biological Interest) (1,200MB, ~200,000 compounds)...'
mkdir -p "$BASE_DIR/chemistry"
wget -c 'ftp://ftp.ebi.ac.uk/pub/databases/chebi/archive/release-latest/Flat_file_formats/chebi_complete.sdf' -O "$BASE_DIR/chemistry/chebi_complete.sdf"
echo '✅ ChEBI (Chemical Entities of Biological Interest) downloaded'

echo 'Downloading PubChem Compounds (first 10M) (2,500MB, ~10,000,000 compounds (sample))...'
mkdir -p "$BASE_DIR/chemistry"
wget -c 'https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/SDF/pubchem_compounds_001_010.sdf.gz' -O "$BASE_DIR/chemistry/pubchem_compounds_sample.sdf.gz"
echo '✅ PubChem Compounds (first 10M) downloaded'

echo 'Downloading IUPAC InChI (500MB, Structure standardization)...'
mkdir -p "$BASE_DIR/chemistry"
wget -c 'https://www.inchi-trust.org/download/' -O "$BASE_DIR/chemistry/iupac_inchi.zip"
echo '✅ IUPAC InChI downloaded'

# ========== PHASE 2: Protein & Interaction Databases ==========

echo 'Downloading UniProt (SwissProt curated) (800MB, ~569,000 proteins (curated))...'
mkdir -p "$BASE_DIR/proteins"
wget -c 'https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz' -O "$BASE_DIR/proteins/uniprot_sprot.xml.gz"
echo '✅ UniProt (SwissProt curated) downloaded'

echo 'Downloading UniProt (TrEMBL all) (70,000MB, ~230,000,000 sequences (unreviewed))...'
mkdir -p "$BASE_DIR/proteins"
wget -c 'https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.xml.gz' -O "$BASE_DIR/proteins/uniprot_trembl.xml.gz"
echo '✅ UniProt (TrEMBL all) downloaded'

echo 'Downloading PDB (Protein Data Bank structures) (2MB, ~200,000 structures)...'
mkdir -p "$BASE_DIR/proteins"
wget -c 'https://www.wwpdb.org/ftp/pdb-files/divided/pdb/index.txt.Z' -O "$BASE_DIR/proteins/pdb_index.txt.Z"
uncompress "$BASE_DIR/proteins/pdb_index.txt.Z"
echo '✅ PDB (Protein Data Bank structures) downloaded'

echo 'Downloading InterPro Domains (1,200MB, ~40,000 protein domains)...'
mkdir -p "$BASE_DIR/proteins"
wget -c 'https://ftp.ebi.ac.uk/pub/databases/interpro/current/interpro.xml.gz' -O "$BASE_DIR/proteins/interpro_domains.xml.gz"
echo '✅ InterPro Domains downloaded'

echo 'Downloading BioGRID (Protein Interactions) (2,000MB, ~900,000 interactions)...'
mkdir -p "$BASE_DIR/proteins"
wget -c 'https://downloads.thebiogrid.org/Download/BioGRID/Latest-Release/BIOGRID-ALL-LATEST.psi25.zip' -O "$BASE_DIR/proteins/biogrid_interactions.zip"
unzip -d "$BASE_DIR/proteins" "$BASE_DIR/proteins/biogrid_interactions.zip"
echo '✅ BioGRID (Protein Interactions) downloaded'

# ========== PHASE 3: Pathway & Reaction Databases ==========

echo 'Downloading Reactome Pathways (400MB, ~10,500 pathways)...'
mkdir -p "$BASE_DIR/pathways"
wget -c 'https://reactome.org/download/current/reactome.owl' -O "$BASE_DIR/pathways/reactome.owl"
echo '✅ Reactome Pathways downloaded'

echo 'Downloading Rhea Reactions (ChEBI-based) (150MB, ~13,600 reactions)...'
mkdir -p "$BASE_DIR/pathways"
wget -c 'https://ftp.expasy.org/databases/rhea/tsv/rhea-reactions.tsv.gz' -O "$BASE_DIR/pathways/rhea_reactions.tsv.gz"
echo '✅ Rhea Reactions (ChEBI-based) downloaded'

echo 'Downloading KEGG Pathways (1MB, ~500+ pathways)...'
mkdir -p "$BASE_DIR/pathways"
wget -c 'http://rest.kegg.jp/list/pathway' -O "$BASE_DIR/pathways/kegg_pathways.txt"
echo '✅ KEGG Pathways downloaded'

echo 'Downloading MetaBoAnalyst Compounds (50MB, ~200,000 metabolites)...'
mkdir -p "$BASE_DIR/pathways"
wget -c 'https://www.metaboanalyst.ca/resources/databases/' -O "$BASE_DIR/pathways/metabolites.csv"
echo '✅ MetaBoAnalyst Compounds downloaded'

# ========== PHASE 4: Ion Channels & Electrophysiology ==========

echo 'Downloading Channelpedia (Ion Channel Properties) (100MB, ~500 channels)...'
mkdir -p "$BASE_DIR/electrophysiology"
wget -c 'https://channelpedia.epfl.ch/downloads/' -O "$BASE_DIR/electrophysiology/channelpedia.csv"
echo '✅ Channelpedia (Ion Channel Properties) downloaded'

echo 'Downloading IUPHAR/BPS Guide to Pharmacology (500MB, ~11,000 pharmacological targets)...'
mkdir -p "$BASE_DIR/electrophysiology"
wget -c 'https://www.guidetopharmacology.org/DATA/' -O "$BASE_DIR/electrophysiology/iuphar_targets.csv"
echo '✅ IUPHAR/BPS Guide to Pharmacology downloaded'

echo 'Downloading Allen Cell Types Database (5,000MB, ~1,800+ neuron types)...'
mkdir -p "$BASE_DIR/electrophysiology"
wget -c 'https://celltypes.brain-map.org/api/v1/cell_types/models/download' -O "$BASE_DIR/electrophysiology/allen_cell_types.json"
echo '✅ Allen Cell Types Database downloaded'

# ========== PHASE 5: Neuromorphology Databases ==========

echo 'Downloading Allen Brain Atlas (ISH data) (10,000MB, 3D brain anatomy + expression)...'
mkdir -p "$BASE_DIR/morphology"
wget -c 'https://mouse.brain-map.org/api/v2/data/download' -O "$BASE_DIR/morphology/allen_brain_atlas.nii.gz"
echo '✅ Allen Brain Atlas (ISH data) downloaded'

echo 'Downloading NeuroMorpho.Org Reconstructions (500MB, ~170,000 neuron reconstructions)...'
mkdir -p "$BASE_DIR/morphology"
wget -c 'http://neuromorpho.org/api/neuron/select?q=*' -O "$BASE_DIR/morphology/neuromorpho_catalog.json"
echo '✅ NeuroMorpho.Org Reconstructions downloaded'

echo 'Downloading Open Data for Structural Connectomics (2,000MB, Drosophila connectome)...'
mkdir -p "$BASE_DIR/morphology"
wget -c 'https://www.virtualflybrain.org/' -O "$BASE_DIR/morphology/connectome_structures.swc"
echo '✅ Open Data for Structural Connectomics downloaded'

# ========== PHASE 6: Synaptic Plasticity & Learning ==========

echo 'Downloading Synapse Ontology (50MB, ~2,500 synaptic terms)...'
mkdir -p "$BASE_DIR/plasticity"
wget -c 'https://purl.obolibrary.org/obo/snpo.owl' -O "$BASE_DIR/plasticity/synapse_ontology.owl"
echo '✅ Synapse Ontology downloaded'

echo 'Downloading SynapseHub (Synapse Properties) (500MB, ~2,000 plasticity proteins)...'
mkdir -p "$BASE_DIR/plasticity"
wget -c 'https://www.ncbi.nlm.nih.gov/gene/synaptic/' -O "$BASE_DIR/plasticity/synapse_hub.csv"
echo '✅ SynapseHub (Synapse Properties) downloaded'

echo 'Downloading Protein Phosphorylation Sites (300MB, ~100,000+ phosphorylation sites)...'
mkdir -p "$BASE_DIR/plasticity"
wget -c 'https://www.phosphosite.org/staticDownloads.action' -O "$BASE_DIR/plasticity/phosphosites.txt"
echo '✅ Protein Phosphorylation Sites downloaded'

# ========== PHASE 7: Brain Connectome & Network Data ==========

echo 'Downloading Human Connectome Project (HCP) (50,000MB, 1,200+ subjects)...'
mkdir -p "$BASE_DIR/connectivity"
wget -c 'https://db.humanconnectome.org/data/projects/HCP' -O "$BASE_DIR/connectivity/hcp_connectome.nii.gz"
echo '✅ Human Connectome Project (HCP) downloaded'

echo 'Downloading BAMS (Brain Architecture Management System) (200MB, ~50,000 connections)...'
mkdir -p "$BASE_DIR/connectivity"
wget -c 'http://www.bams.brain-map.org/' -O "$BASE_DIR/connectivity/bams_connections.json"
echo '✅ BAMS (Brain Architecture Management System) downloaded'

echo 'Downloading C. elegans Connectome (50MB, 302 neurons, ~7,000 synapses)...'
mkdir -p "$BASE_DIR/connectivity"
wget -c 'https://www.wormwiring.org/pages/data.html' -O "$BASE_DIR/connectivity/celegans_connectome.json"
echo '✅ C. elegans Connectome downloaded'

# ========== PHASE 8: Cognitive & Behavioral Ontologies ==========

echo 'Downloading Cognitive Atlas (50MB, ~650 cognitive concepts)...'
mkdir -p "$BASE_DIR/cognition"
wget -c 'https://www.cognitiveatlas.org/download/' -O "$BASE_DIR/cognition/cognitive_atlas.json"
echo '✅ Cognitive Atlas downloaded'

echo 'Downloading OpenNeuro (fMRI datasets) (100MB, ~300+ fMRI experiments)...'
mkdir -p "$BASE_DIR/cognition"
wget -c 'https://openneuro.org/' -O "$BASE_DIR/cognition/openneuro_metadata.json"
echo '✅ OpenNeuro (fMRI datasets) downloaded'

echo 'Downloading BrainMap (neuroimaging meta-analysis) (100MB, ~100,000+ peak coordinates)...'
mkdir -p "$BASE_DIR/cognition"
wget -c 'http://brainmap.org/' -O "$BASE_DIR/cognition/brainmap_coordinates.txt"
echo '✅ BrainMap (neuroimaging meta-analysis) downloaded'

echo ''
echo '========================================='
echo '✅ All databases downloaded successfully'
echo '========================================='
echo 'Next: Run parse_databases.py to extract mechanisms'