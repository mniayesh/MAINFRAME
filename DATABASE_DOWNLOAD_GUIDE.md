# Smart Database Download Guide

**Strategy**: Download all useful databases, skip wasteful ones
**Total Size**: ~24 GB (saves 121 GB vs. full download)
**Expected Primitives**: ~5,000 core types
**Time Required**: 6-12 hours (download + extraction)

---

## Quick Start

```bash
# 1. Download all useful databases (~24 GB)
./scripts/download_databases.sh

# 2. Extract primitives (processes downloaded files)
python3 scripts/extract_primitives.py --parallel 8

# 3. View results
sqlite3 bio_architecture.db "SELECT COUNT(*) FROM mechanisms"
```

---

## What Gets Downloaded (25/28 databases)

### ✅ TIER 1: Core Primitives (~8 GB)

| Database | Size | Items | Primitives |
|----------|------|-------|------------|
| **Gene Ontology** | 35 MB | 45,000 terms | Functional annotations |
| **ChEBI** | 1.2 GB | 200,000 compounds | Chemical mechanisms |
| **Reactome** | 400 MB | 10,500 pathways | Signaling cascades |
| **KEGG** | 1 MB | 500+ pathways | Metabolic pathways |
| **Rhea** | 150 MB | 13,600 reactions | Biochemical reactions |
| **IUPHAR** | 500 MB | 11,000 targets | Ion channels, receptors |
| **Synapse Ontology** | 50 MB | 2,500 terms | Synaptic mechanisms |
| **Cognitive Atlas** | 50 MB | 650 concepts | Cognitive functions |
| **C. elegans** | 50 MB | 7,000 synapses | Complete connectome |

**Subtotal**: ~2.4 GB, ~3,000 primitive types

### ✅ TIER 2: Molecular Detail (~4 GB)

| Database | Size | Items | Primitives |
|----------|------|-------|------------|
| **UniProt Swiss-Prot** | 800 MB | 569,000 proteins | Curated protein functions |
| **InterPro** | 1.2 GB | 40,000 domains | Protein domain families |
| **BioGRID** | 2 GB | 900,000 interactions | Protein interaction networks |
| **PDB Index** | 2 MB | 200,000 structures | Structural templates |

**Subtotal**: ~4 GB, +1,000 primitive types

### ✅ TIER 3: Structural/Network (~0.5 GB)

| Database | Size | Items | Primitives |
|----------|------|-------|------------|
| **Drosophila Brain** | 50 MB | Connectome | Circuit motifs |

**Subtotal**: ~0.5 GB, +500 circuit patterns

### 🔌 API-Based (Require Extraction Scripts)

These databases require API calls and are handled by Python extractors:

| Database | Size | Items | Script |
|----------|------|-------|--------|
| **Channelpedia** | ~100 MB | 500 channels | `AllenBrainExtractor` |
| **Allen Cell Types** | ~5 GB | 1,800 neuron models | `AllenBrainExtractor` |
| **NeuroMorpho** | ~500 MB | 170,000 neurons | `NeuroMorphoExtractor` |
| **Allen Brain Atlas** | ~10 GB | Gene expression | `AllenBrainExtractor` |
| **BAMS** | ~200 MB | 50,000 connections | API extraction |

**Subtotal**: ~16 GB, API-extracted

---

## What Gets Skipped (3/28 databases, saves 121 GB)

### ❌ UniProt TrEMBL - 68.4 GB

**Why skip**: 230 million unreviewed protein sequences (raw data, not computational mechanisms)

**What we use instead**: UniProt Swiss-Prot (800 MB, curated proteins only)

**Savings**: 68.4 GB

### ❌ Human Connectome Project - 48.8 GB

**Why skip**: Raw fMRI imaging data from 1,200 subjects (not primitives)

**What we use instead**: BAMS connectivity (200 MB, actual connections)

**Savings**: 48.8 GB

### ❌ PubChem 10M Sample - 2.4 GB

**Why skip**: 10 million compound structures (ChEBI is sufficient for mechanisms)

**What we use instead**: ChEBI (1.2 GB, biological compounds only)

**Savings**: 2.4 GB

**Total savings**: 121 GB (82% reduction)

---

## Download Time Estimates

### By Internet Speed

| Speed | Download Time | Extraction Time | Total |
|-------|---------------|-----------------|-------|
| **100 Mbps (fast)** | 0.5 hours | 3-6 hours | ~6 hours |
| **50 Mbps (good)** | 1 hour | 3-6 hours | ~7 hours |
| **10 Mbps (slow)** | 5 hours | 3-6 hours | ~11 hours |

### By Phase

| Phase | Size | Files | Time (50 Mbps) |
|-------|------|-------|----------------|
| Chemistry | 1.7 GB | 3 | 5 min |
| Proteins | 4 GB | 4 | 10 min |
| Pathways | 0.6 GB | 4 | 2 min |
| Electrophysiology | 0.5 GB | 1 | 1 min |
| Morphology | 0.05 GB | 1 | <1 min |
| Plasticity | 0.05 GB | 1 | <1 min |
| Connectivity | 0.05 GB | 1 | <1 min |
| Cognition | 0.01 GB | 2 | <1 min |
| **Subtotal (direct)** | **~7 GB** | **17** | **~20 min** |
| **API-based** | **~16 GB** | **~8** | **~40 min** |
| **Total** | **~24 GB** | **25** | **~1 hour** |

---

## Expected Primitive Counts

### After Full Extraction

| Category | Primitive Types | Source Databases |
|----------|----------------|------------------|
| **Ion Channels** | ~500 | Channelpedia, IUPHAR |
| **Signaling Pathways** | ~2,000 | Reactome, KEGG |
| **Biochemical Reactions** | ~13,600 | Rhea |
| **Protein Domains** | ~40,000 | InterPro |
| **Synaptic Mechanisms** | ~2,500 | Synapse Ontology, PhosphoSite |
| **Neuron Models** | ~1,800 | Allen Cell Types |
| **Circuit Patterns** | ~500 | NeuroMorpho, connectomes |
| **Cognitive Functions** | ~650 | Cognitive Atlas |
| **Brain Connections** | ~50,000 | BAMS, C. elegans |

**Raw items**: ~111,550

**Deduplicated core types**: ~5,000 (after removing variants and duplicates)

---

## Storage Requirements

### Disk Space Needed

```
Downloaded files:     ~24 GB
Extracted database:   ~2 GB (SQLite)
Working directory:    ~5 GB (temp files)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total required:       ~31 GB
Recommended:          ~50 GB (with buffer)
```

### By Directory

```
biology_data/
├── chemistry/          ~1.4 GB (ChEBI, GO)
├── proteins/           ~4.0 GB (UniProt, InterPro, BioGRID)
├── pathways/           ~0.6 GB (Reactome, KEGG, Rhea)
├── electrophysiology/  ~5.6 GB (Allen, IUPHAR)
├── morphology/         ~10.5 GB (Allen Atlas, NeuroMorpho)
├── plasticity/         ~0.85 GB (Synapse Ontology, PhosphoSite)
├── connectivity/       ~0.25 GB (C. elegans, BAMS)
└── cognition/          ~0.25 GB (Cognitive Atlas)
```

---

## Manual Steps Required

Some databases require manual intervention:

### 1. PhosphoSite Plus (Phosphorylation Sites)

**Why**: Requires free registration
**Size**: ~300 MB
**Items**: 100,000+ phosphorylation sites

**Steps**:
1. Visit https://www.phosphosite.org/staticDownloads
2. Create free account
3. Download "Phosphorylation_site_dataset.gz"
4. Place in `biology_data/plasticity/`

### 2. Allen Brain Institute (API Key)

**Why**: Large downloads benefit from API key
**Size**: ~15 GB total
**Items**: Cell types, morphologies, gene expression

**Steps**:
1. Visit http://www.brain-map.org/
2. Create free account (optional but recommended)
3. Use Python extractors (automatic)

---

## Verification

### Check Downloaded Files

```bash
# List all downloaded files with sizes
find biology_data -type f -exec ls -lh {} \; | awk '{print $5, $9}'

# Count files per directory
for dir in biology_data/*/; do
    echo "$dir: $(find "$dir" -type f | wc -l) files"
done

# Total size
du -sh biology_data/
```

### Expected Output

```
biology_data/chemistry:         3 files
biology_data/proteins:          4 files
biology_data/pathways:          4 files
biology_data/electrophysiology: 1 file
biology_data/morphology:        1 file
biology_data/plasticity:        1 file
biology_data/connectivity:      1 file
biology_data/cognition:         2 files

Total: 17 files, ~7 GB (direct downloads)
```

---

## Troubleshooting

### Download Failures

**Problem**: wget/curl not found
**Solution**: Install with `apt-get install wget curl` or `brew install wget`

**Problem**: Connection timeout
**Solution**: Script auto-retries. For persistent issues, download manually and place in correct directory.

**Problem**: FTP access blocked
**Solution**: Some networks block FTP. Use alternative HTTP URLs in script.

### Extraction Issues

**Problem**: "Module not found"
**Solution**: Install dependencies: `pip install -r requirements.txt`

**Problem**: Out of memory
**Solution**: Reduce parallel workers: `--parallel 2`

**Problem**: Slow extraction
**Solution**: Increase workers: `--parallel 8` (requires 16+ GB RAM)

---

## Next Steps After Download

1. **Extract primitives**:
   ```bash
   python3 scripts/extract_primitives.py --parallel 8
   ```

2. **Verify extraction**:
   ```bash
   sqlite3 bio_architecture.db "
   SELECT
       mechanism_class,
       COUNT(*) as count
   FROM mechanisms
   GROUP BY mechanism_class
   ORDER BY count DESC
   "
   ```

3. **Generate analysis**:
   ```bash
   python3 scripts/analyze_primitives.py
   ```

4. **Update inventory**:
   ```bash
   python3 scripts/update_inventory.py
   ```

---

## Comparison: Smart vs. Full Download

| Metric | Smart (This Guide) | Full (Everything) | Savings |
|--------|-------------------|-------------------|---------|
| **Databases** | 25/28 (89%) | 28/28 (100%) | -3 wasteful DBs |
| **Storage** | 24 GB | 145 GB | 121 GB (82%) |
| **Download Time** | 1 hour | 3-33 hours | 2-32 hours |
| **Core Primitives** | ~5,000 types | ~5,000 types | Same! |
| **Usefulness** | 100% useful | 82% waste | - |

**Conclusion**: Get 100% of the primitives with 16% of the storage.

---

## References

- Full database manifest: `biology_data/download_manifest.json`
- Extraction framework: `bio_extractors/`
- Database schema: `bio_architecture_schema.sql`
- Current inventory: `PRIMITIVES_INVENTORY.md`

---

**Last Updated**: 2025-12-12
**Estimated Completion**: 6-12 hours total
**Expected Result**: ~5,000 biological computational primitives
