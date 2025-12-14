#!/usr/bin/env python3
"""
Working Database Downloader - Uses APIs that actually work

Many databases changed their access methods, so we use a combination of:
1. Direct HTTP downloads (where available)
2. REST APIs
3. Python library extractors

Expected yield: ~3,000 primitives from direct downloads + API extraction
"""

import os
import sys
import requests
import json
import time
from pathlib import Path
from urllib.request import urlretrieve

# Color output
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'biology_data'

def print_header(text):
    print(f"\n{BLUE}{'='*80}{NC}")
    print(f"{BLUE}{text}{NC}")
    print(f"{BLUE}{'='*80}{NC}\n")

def download_file(url, output_path, description):
    """Download a file with progress"""
    print(f"{YELLOW}[DOWNLOAD]{NC} {description}")
    print(f"  {BLUE}URL:{NC} {url}")
    print(f"  {BLUE}Output:{NC} {output_path}")

    if output_path.exists():
        print(f"  {GREEN}✓ Already exists, skipping{NC}")
        return True

    try:
        print(f"  {YELLOW}Downloading...{NC}")

        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        downloaded = 0

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(block_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        pct = (downloaded / total_size) * 100
                        print(f"\r  Progress: {downloaded/1024/1024:.1f}/{total_size/1024/1024:.1f} MB ({pct:.0f}%)", end='')

        print(f"\n  {GREEN}✓ Download complete{NC}")
        return True

    except Exception as e:
        print(f"\n  {RED}✗ Failed: {e}{NC}")
        if output_path.exists():
            output_path.unlink()
        return False

def fetch_kegg_pathways():
    """Fetch KEGG pathways via REST API"""
    print(f"\n{YELLOW}[API]{NC} Fetching KEGG pathways...")

    output_file = DATA_DIR / 'pathways' / 'kegg_pathways.txt'

    if output_file.exists():
        print(f"  {GREEN}✓ Already exists{NC}")
        return True

    try:
        url = "http://rest.kegg.jp/list/pathway"
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(response.text)

        count = len(response.text.strip().split('\n'))
        print(f"  {GREEN}✓ Downloaded {count} pathways{NC}")
        return True

    except Exception as e:
        print(f"  {RED}✗ Failed: {e}{NC}")
        return False

def fetch_cognitive_atlas():
    """Fetch Cognitive Atlas via API"""
    print(f"\n{YELLOW}[API]{NC} Fetching Cognitive Atlas...")

    output_file = DATA_DIR / 'cognition' / 'cognitive_atlas.json'

    if output_file.exists():
        print(f"  {GREEN}✓ Already exists{NC}")
        return True

    try:
        # Try the GitHub raw URL
        url = "https://raw.githubusercontent.com/CognitiveAtlas/cogat/master/cogat.json"
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(response.text)

        data = json.loads(response.text)
        count = len(data.get('concepts', []))
        print(f"  {GREEN}✓ Downloaded {count} cognitive concepts{NC}")
        return True

    except Exception as e:
        print(f"  {RED}✗ Failed: {e}{NC}")
        return False

def main():
    print_header("Working Database Downloader")

    print(f"{GREEN}Strategy:{NC} Download what works, use APIs for the rest")
    print(f"{GREEN}Expected:{NC} ~3,000 primitives from accessible sources\n")

    stats = {
        'attempted': 0,
        'successful': 0,
        'failed': 0
    }

    # Phase 1: Direct HTTP downloads
    print_header("PHASE 1: Direct Downloads")

    downloads = [
        ("https://purl.obolibrary.org/obo/go.obo",
         DATA_DIR / "chemistry" / "gene_ontology.obo",
         "Gene Ontology (45,000 terms)"),

        ("https://purl.obolibrary.org/obo/sao.owl",
         DATA_DIR / "plasticity" / "synapse_ontology.owl",
         "Synapse Ontology (2,500 terms)"),

        ("https://ftp.expasy.org/databases/rhea/tsv/rhea2ec.tsv",
         DATA_DIR / "chemistry" / "rhea2ec.tsv",
         "Rhea EC Classifications"),

        ("https://reactome.org/download/current/ReactomePathways.txt",
         DATA_DIR / "pathways" / "reactome_pathways.txt",
         "Reactome Pathways"),

        ("https://reactome.org/download/current/ReactomePathwaysRelation.txt",
         DATA_DIR / "pathways" / "reactome_relations.txt",
         "Reactome Hierarchy"),

        ("https://www.guidetopharmacology.org/DATA/targets_and_families.csv",
         DATA_DIR / "electrophysiology" / "iuphar_targets.csv",
         "IUPHAR Targets"),
    ]

    for url, output, desc in downloads:
        stats['attempted'] += 1
        if download_file(url, output, desc):
            stats['successful'] += 1
        else:
            stats['failed'] += 1

    # Phase 2: REST API calls
    print_header("PHASE 2: REST API Fetches")

    stats['attempted'] += 1
    if fetch_kegg_pathways():
        stats['successful'] += 1
    else:
        stats['failed'] += 1

    stats['attempted'] += 1
    if fetch_cognitive_atlas():
        stats['successful'] += 1
    else:
        stats['failed'] += 1

    # Phase 3: Summary
    print_header("DOWNLOAD SUMMARY")

    print(f"  {GREEN}Successful:{NC} {stats['successful']}/{stats['attempted']}")
    print(f"  {RED}Failed:{NC} {stats['failed']}/{stats['attempted']}")

    # Check what we got
    total_size = 0
    file_count = 0

    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            if file not in ['.gitkeep', 'download_manifest.json']:
                file_path = Path(root) / file
                size = file_path.stat().st_size
                total_size += size
                file_count += 1

    print(f"\n  {BLUE}Total files:{NC} {file_count}")
    print(f"  {BLUE}Total size:{NC} {total_size / 1024 / 1024:.1f} MB")

    print(f"\n{BLUE}{'='*80}{NC}")
    print(f"{YELLOW}Next steps:{NC}")
    print(f"  1. For large databases (UniProt, Allen, etc.), use:")
    print(f"     {BLUE}python3 bio_extractors/extract_all.py{NC}")
    print(f"  2. Extract primitives from downloaded files:")
    print(f"     {BLUE}python3 scripts/extract_primitives.py{NC}")
    print(f"{BLUE}{'='*80}{NC}")

if __name__ == '__main__':
    main()
