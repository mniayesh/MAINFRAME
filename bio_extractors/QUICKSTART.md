# Quick Start Guide

Get up and running with the BioExtractors framework in 5 minutes.

## Installation (60 seconds)

```bash
cd /home/user/MAINFRAME/bio_extractors

# Run automated setup
./setup.sh

# Or manual setup:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Your First Extraction (2 minutes)

### Option 1: Run Examples

```bash
# Run all examples
python example_usage.py

# Run specific example
python example_usage.py 1  # Simple GO extraction
python example_usage.py 8  # Parallel extraction
```

### Option 2: Quick Extraction

```bash
# Preview what will be extracted
python extract_all.py --dry-run

# Extract from GO and Reactome
python extract_all.py --databases GO,Reactome

# Full extraction (all enabled databases)
python extract_all.py
```

## Output

Results are saved to:
- **Files**: `extraction_results/*.json`
- **Database**: `bio_architecture.db`
- **Report**: `extraction_results/extraction_report.json`
- **Logs**: `extraction.log`

## Python API (30 seconds)

```python
from bio_extractors import GOExtractor

# Extract GO terms
with GOExtractor() as extractor:
    terms = extractor.extract(max_terms=100)
    print(f"Extracted {len(terms)} GO terms")
    extractor.print_stats()
```

## Configuration (Optional)

Edit `config/extraction_config.yaml`:

```yaml
extraction:
  max_items_per_database: 500  # Adjust as needed

databases:
  GO:
    enabled: true
    extraction_params:
      max_terms: 1000  # Increase limit
```

## Authentication (For BRENDA, BioPortal)

Add to `config/extraction_config.yaml`:

```yaml
credentials:
  brenda_email: "your@email.com"
  brenda_password: "yourpassword"
  bioportal_api_key: "your-api-key"

databases:
  BRENDA:
    enabled: true  # Enable after adding credentials
```

**Get credentials**:
- BRENDA: https://www.brenda-enzymes.org/ (register)
- BioPortal: https://bioportal.bioontology.org/account (get API key)

## Common Commands

```bash
# Extract specific databases
python extract_all.py --databases GO,Reactome,KEGG

# Change output directory
python extract_all.py --output results/batch1/

# Skip database save (JSON only)
python extract_all.py --skip-db-save

# Sequential extraction (no parallel)
python extract_all.py --no-parallel

# Custom config
python extract_all.py --config my_config.yaml
```

## Verification

Check if extraction worked:

```bash
# List extracted files
ls -lh extraction_results/

# View report
cat extraction_results/extraction_report.json | python -m json.tool

# Check database
sqlite3 bio_architecture.db "SELECT COUNT(*) FROM entities;"
```

## Troubleshooting

**Problem**: Import error
```bash
# Solution: Activate virtual environment
source venv/bin/activate
```

**Problem**: Rate limit errors
```bash
# Solution: Increase delay in config
# Edit config/extraction_config.yaml:
rate_limits:
  default_period: 2.0  # Increase from 1.0
```

**Problem**: Authentication failed
```bash
# Solution: Check credentials in config
# Ensure BRENDA/BioPortal credentials are correct
```

**Problem**: Memory issues with large extractions
```bash
# Solution: Extract in batches
python extract_all.py --databases GO
python extract_all.py --databases Reactome,KEGG
python extract_all.py --databases UniProt,ChEBI
```

## Next Steps

1. **Read the full README**: `README.md`
2. **Explore examples**: `example_usage.py`
3. **Customize config**: `config/extraction_config.yaml`
4. **View extractors**: Individual `*_extractors.py` files
5. **Database schema**: `../bio_architecture_schema.sql`

## Support

- Documentation: See `README.md`
- Examples: Run `python example_usage.py`
- Logs: Check `extraction.log` for detailed info

## Cheat Sheet

```bash
# Setup
./setup.sh

# Quick test
python example_usage.py 1

# Preview extraction
python extract_all.py --dry-run

# Extract all
python extract_all.py

# Extract specific
python extract_all.py --databases GO,Reactome

# Custom output
python extract_all.py --output my_results/

# View results
cat extraction_results/extraction_report.json | python -m json.tool
```

---

**Time to first extraction**: < 5 minutes

**Default extraction**: ~3000-5000 entities in 5-10 minutes

**Databases supported**: 14 (GO, Reactome, KEGG, UniProt, ChEBI, Allen Brain, NeuroMorpho, Cell Ontology, InterPro, BRENDA, eQuilibrator, Cognitive Atlas, CogPO, MFO)
