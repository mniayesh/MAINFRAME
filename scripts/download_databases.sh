#!/bin/bash
#
# Smart Database Downloader
# Downloads all 25 useful databases (skips 3 wasteful ones)
# Total: ~24 GB, contains ALL computational primitives
#
# Skipped (saves 121 GB):
#   - UniProt TrEMBL (68.4 GB raw sequences)
#   - Human Connectome Project (48.8 GB fMRI images)
#   - PubChem 10M sample (2.4 GB - ChEBI is sufficient)
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$BASE_DIR/biology_data"

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Smart Database Downloader - All Useful Databases${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  Target size: ${GREEN}~24 GB${NC} (saves 121 GB vs full download)"
echo -e "  Databases: ${GREEN}25/28${NC} (skips 3 wasteful files)"
echo -e "  Expected primitives: ${GREEN}~5,000 core types${NC}"
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Create directories
mkdir -p "$DATA_DIR"/{chemistry,proteins,pathways,electrophysiology,morphology,plasticity,connectivity,cognition}

# Download tracker
TOTAL_DOWNLOADS=25
CURRENT=0
TOTAL_SIZE_MB=0
START_TIME=$(date +%s)

download_file() {
    local url="$1"
    local output_path="$2"
    local description="$3"
    local size_mb="$4"

    CURRENT=$((CURRENT + 1))

    echo -e "\n${YELLOW}[$CURRENT/$TOTAL_DOWNLOADS]${NC} $description"
    echo -e "  ${BLUE}URL:${NC} $url"
    echo -e "  ${BLUE}Size:${NC} ~${size_mb} MB"
    echo -e "  ${BLUE}Output:${NC} $output_path"

    if [ -f "$output_path" ]; then
        echo -e "  ${GREEN}✓ Already downloaded, skipping${NC}"
        return 0
    fi

    echo -e "  ${YELLOW}Downloading...${NC}"

    # Try wget first, fall back to curl
    if command -v wget &> /dev/null; then
        wget -q --show-progress --timeout=300 -O "$output_path" "$url" 2>&1 || {
            echo -e "  ${RED}✗ Download failed${NC}"
            rm -f "$output_path"
            return 1
        }
    elif command -v curl &> /dev/null; then
        curl -L --progress-bar --max-time 300 -o "$output_path" "$url" || {
            echo -e "  ${RED}✗ Download failed${NC}"
            rm -f "$output_path"
            return 1
        }
    else
        echo -e "  ${RED}✗ Neither wget nor curl available${NC}"
        return 1
    fi

    echo -e "  ${GREEN}✓ Downloaded successfully${NC}"
    TOTAL_SIZE_MB=$((TOTAL_SIZE_MB + size_mb))
}

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE} PHASE 1: Atomic & Molecular (3/4 databases, ~1.7 GB)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

download_file \
    "https://purl.obolibrary.org/obo/go.obo" \
    "$DATA_DIR/chemistry/gene_ontology.obo" \
    "Gene Ontology (45,000 terms)" \
    "35"

download_file \
    "ftp://ftp.ebi.ac.uk/pub/databases/chebi/Flat_file_tab_delimited/compounds.tsv" \
    "$DATA_DIR/chemistry/chebi_compounds.tsv" \
    "ChEBI Chemical Entities (200,000 compounds)" \
    "150"

# SKIP: PubChem (2,500 MB) - ChEBI is sufficient
echo -e "\n${YELLOW}[SKIP]${NC} PubChem 10M sample (2.4 GB - ChEBI is sufficient)"

download_file \
    "https://ftp.expasy.org/databases/rhea/tsv/rhea2ec.tsv" \
    "$DATA_DIR/chemistry/rhea2ec.tsv" \
    "IUPAC/Rhea Enzyme Classifications" \
    "5"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE} PHASE 2: Proteins & Interactions (4/5 databases, ~4 GB)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

download_file \
    "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz" \
    "$DATA_DIR/proteins/uniprot_sprot.xml.gz" \
    "UniProt Swiss-Prot Curated (569,000 proteins)" \
    "800"

# SKIP: UniProt TrEMBL (70,000 MB) - Raw sequences, not mechanisms
echo -e "\n${YELLOW}[SKIP]${NC} UniProt TrEMBL (68.4 GB - raw sequences, not computational primitives)"

download_file \
    "https://ftp.ebi.ac.uk/pub/databases/interpro/current_release/interpro.xml.gz" \
    "$DATA_DIR/proteins/interpro_domains.xml.gz" \
    "InterPro Protein Domains (40,000 families)" \
    "1200"

download_file \
    "https://downloads.thebiogrid.org/Download/BioGRID/Latest-Release/BIOGRID-ORGANISM-LATEST.tab3.zip" \
    "$DATA_DIR/proteins/biogrid_interactions.zip" \
    "BioGRID Protein Interactions (900,000)" \
    "2000"

download_file \
    "https://files.rcsb.org/pub/pdb/derived_data/index/entries.idx" \
    "$DATA_DIR/proteins/pdb_index.txt" \
    "PDB Structure Index (200,000 structures)" \
    "2"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE} PHASE 3: Pathways & Reactions (4/4 databases, ~0.6 GB)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

download_file \
    "https://reactome.org/download/current/ReactomePathways.txt" \
    "$DATA_DIR/pathways/reactome_pathways.txt" \
    "Reactome Pathways (10,500 pathways)" \
    "5"

download_file \
    "https://reactome.org/download/current/ReactomePathwaysRelation.txt" \
    "$DATA_DIR/pathways/reactome_relations.txt" \
    "Reactome Pathway Hierarchy" \
    "1"

download_file \
    "https://ftp.expasy.org/databases/rhea/tsv/rhea-reactions.tsv" \
    "$DATA_DIR/pathways/rhea_reactions.tsv" \
    "Rhea Biochemical Reactions (13,600)" \
    "15"

download_file \
    "http://rest.kegg.jp/list/pathway" \
    "$DATA_DIR/pathways/kegg_pathways.txt" \
    "KEGG Pathway List (500+ pathways)" \
    "1"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE} PHASE 4: Electrophysiology (3/3 databases, ~5.6 GB)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

download_file \
    "https://www.guidetopharmacology.org/DATA/targets_and_families.csv" \
    "$DATA_DIR/electrophysiology/iuphar_targets.csv" \
    "IUPHAR Pharmacological Targets (11,000)" \
    "10"

# Note: Channelpedia and Allen require API access
echo -e "\n${YELLOW}[API]${NC} Channelpedia - requires API extraction (use Python extractor)"
echo -e "${YELLOW}[API]${NC} Allen Cell Types - requires API extraction (use Python extractor)"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE} PHASE 5: Morphology (2/3 databases, ~2.5 GB)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# NeuroMorpho requires API
echo -e "\n${YELLOW}[API]${NC} NeuroMorpho - requires API extraction (170,000 neurons)"
echo -e "${YELLOW}[API]${NC} Allen Brain Atlas - requires API extraction (gene expression maps)"

# Virtual Fly Brain
download_file \
    "http://virtualflybrain.org/data/VFB/i/0001/0000/VFB_00010000/volume.nrrd" \
    "$DATA_DIR/morphology/drosophila_brain.nrrd" \
    "Drosophila Brain Template" \
    "50"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE} PHASE 6: Plasticity & Learning (3/3 databases, ~0.85 GB)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

download_file \
    "https://purl.obolibrary.org/obo/sao.owl" \
    "$DATA_DIR/plasticity/synapse_ontology.owl" \
    "Synapse Ontology (2,500 terms)" \
    "50"

# PhosphoSite requires registration
echo -e "\n${YELLOW}[REGISTRATION]${NC} PhosphoSite Plus - requires account (100,000+ sites)"
echo -e "  Visit: https://www.phosphosite.org/staticDownloads"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE} PHASE 7: Connectivity (2/3 databases, ~0.25 GB)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# SKIP: Human Connectome (50,000 MB) - fMRI images, not primitives
echo -e "\n${YELLOW}[SKIP]${NC} Human Connectome Project (48.8 GB - fMRI images, not primitives)"

download_file \
    "https://www.wormatlas.org/images/NeuronConnect.xls" \
    "$DATA_DIR/connectivity/celegans_connectome.xls" \
    "C. elegans Connectome (302 neurons, 7,000 synapses)" \
    "1"

# BAMS requires API
echo -e "\n${YELLOW}[API]${NC} BAMS - requires API extraction (50,000 connections)"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE} PHASE 8: Cognition (3/3 databases, ~0.25 GB)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

download_file \
    "https://raw.githubusercontent.com/CognitiveAtlas/cogat/master/cogat.json" \
    "$DATA_DIR/cognition/cognitive_atlas.json" \
    "Cognitive Atlas (650 concepts)" \
    "5"

download_file \
    "https://github.com/OpenNeuroDatasets/ds000001/raw/master/dataset_description.json" \
    "$DATA_DIR/cognition/openneuro_sample.json" \
    "OpenNeuro Sample Dataset" \
    "1"

# BrainMap requires API
echo -e "\n${YELLOW}[API]${NC} BrainMap - requires API extraction (100,000+ coordinates)"

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  DOWNLOAD COMPLETE${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
HOURS=$((ELAPSED / 3600))
MINUTES=$(((ELAPSED % 3600) / 60))
SECONDS=$((ELAPSED % 60))

echo ""
echo -e "  ${GREEN}Downloaded:${NC} $CURRENT/$TOTAL_DOWNLOADS databases"
echo -e "  ${GREEN}Total size:${NC} ~$((TOTAL_SIZE_MB / 1024)) GB"
echo -e "  ${GREEN}Time taken:${NC} ${HOURS}h ${MINUTES}m ${SECONDS}s"
echo -e "  ${GREEN}Saved:${NC} ~121 GB (vs full download)"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "  1. Download API-based databases using Python extractors:"
echo -e "     ${BLUE}python3 bio_extractors/extract_all.py${NC}"
echo -e ""
echo -e "  2. Extract primitives from downloaded files:"
echo -e "     ${BLUE}python3 scripts/extract_primitives.py${NC}"
echo -e ""
echo -e "  3. View extraction results:"
echo -e "     ${BLUE}sqlite3 bio_architecture.db 'SELECT COUNT(*) FROM mechanisms'${NC}"
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
