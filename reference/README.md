# Biological Database Extraction Framework

A production-ready Python framework for extracting architectural primitives from biological databases.

## Overview

This framework provides a modular, scalable solution for extracting biological mechanisms, processes, and architectural patterns from major biological databases including GO, Reactome, KEGG, UniProt, ChEBI, Allen Brain Atlas, and more.

### Key Features

- **Modular Architecture**: Each database has its own extractor module
- **Rate Limiting**: Respects API limits (e.g., KEGG's 3 requests/second)
- **Intelligent Caching**: 15-minute cache with automatic expiration
- **Retry Logic**: Exponential backoff for failed requests
- **Parallel Extraction**: Extract from multiple databases simultaneously
- **Progress Tracking**: Detailed logging and statistics
- **Error Recovery**: Graceful handling of failures
- **Schema Integration**: Direct integration with bio_architecture_schema.sql

## Installation

```bash
# Clone repository or navigate to directory
cd /home/user/MAINFRAME/bio_extractors

# Install dependencies
pip install -r requirements.txt
```

### Requirements

- Python 3.8+
- SQLite3
- Internet connection for API access

## Quick Start

### 1. Basic Extraction

Extract from all enabled databases with default settings:

```bash
python extract_all.py
```

### 2. Extract Specific Databases

Extract only from GO and Reactome:

```bash
python extract_all.py --databases GO,Reactome
```

### 3. Custom Configuration

Create your own config file and use it:

```bash
python extract_all.py --config my_config.yaml
```

### 4. Dry Run

Preview what will be extracted without actually executing:

```bash
python extract_all.py --dry-run
```

## Configuration

Edit `config/extraction_config.yaml` to customize extraction:

```yaml
extraction:
  max_items_per_database: 500
  parallel: true
  max_workers: 4

databases:
  GO:
    enabled: true
    priority: 1
    extraction_params:
      max_terms: 500
```

### Database Priorities

Lower priority numbers are extracted first:

- **Priority 1**: Core mechanisms (GO, Reactome, KEGG)
- **Priority 2**: Neuroscience (Allen Brain, NeuroMorpho, Cell Ontology)
- **Priority 3**: Proteins (UniProt, InterPro, BRENDA)
- **Priority 4**: Metabolic (ChEBI, eQuilibrator)
- **Priority 5**: Cognitive (Cognitive Atlas, CogPO, MFO)

### Authentication

Some databases require authentication. Add credentials to config:

```yaml
credentials:
  brenda_email: "your@email.com"
  brenda_password: "yourpassword"
  bioportal_api_key: "your-api-key"
```

**SECURITY**: Never commit real credentials! Use environment variables:

```bash
export BRENDA_EMAIL="your@email.com"
export BRENDA_PASSWORD="yourpassword"
```

## Usage Examples

### Python API

```python
from bio_extractors import GOExtractor, ReactomeExtractor

# Extract GO terms
with GOExtractor() as extractor:
    go_terms = extractor.extract(max_terms=100)
    extractor.print_stats()

# Extract Reactome pathways
with ReactomeExtractor() as extractor:
    pathways = extractor.extract(species='9606')  # Homo sapiens
```

### Command Line

```bash
# Extract with custom output directory
python extract_all.py --output results/batch1/

# Extract without saving to database
python extract_all.py --skip-db-save

# Sequential extraction (no parallelization)
python extract_all.py --no-parallel

# Specify database path
python extract_all.py --db-path custom_bio_arch.db
```

## Architecture

### Module Structure

```
bio_extractors/
├── __init__.py                    # Package initialization
├── base.py                        # Base extractor with caching, rate limiting
├── mechanisms_extractors.py       # GO, Reactome, KEGG
├── neuroscience_extractors.py     # Allen Brain, NeuroMorpho, Cell Ontology
├── protein_extractors.py          # UniProt, InterPro, BRENDA
├── metabolic_extractors.py        # ChEBI, eQuilibrator
├── cognitive_extractors.py        # Cognitive Atlas, CogPO, MFO
├── extract_all.py                 # Orchestration script
├── config/
│   └── extraction_config.yaml     # Configuration file
└── requirements.txt               # Dependencies
```

### Base Extractor Features

All extractors inherit from `BaseExtractor`:

- **Rate Limiting**: Token bucket algorithm
- **Caching**: File-based cache with TTL
- **Retry Logic**: Exponential backoff (3 attempts by default)
- **Pagination**: Automatic pagination handling
- **Session Management**: Connection pooling
- **Statistics**: Request counts, cache hit rates, errors

### Data Flow

```
1. Load Configuration → 2. Initialize Extractors → 3. Extract Data
                                                         ↓
4. Save to Files ← 5. Transform to Schema Format ← Extract Data
     ↓
6. Save to Database → 7. Generate Report
```

## Extractors

### Mechanisms & Processes

#### GOExtractor
- **Source**: Gene Ontology
- **Extracts**: Biological processes, molecular functions
- **Format**: OBO parsing, API queries
- **Rate**: 10 requests/second

```python
extractor = GOExtractor()
terms = extractor.extract(aspect='biological_process', max_terms=500)
```

#### ReactomeExtractor
- **Source**: Reactome Pathway Database
- **Extracts**: Pathways, reactions
- **Format**: JSON API
- **Rate**: 10 requests/second

```python
extractor = ReactomeExtractor()
pathways = extractor.extract(species='9606')
```

#### KEGGExtractor
- **Source**: KEGG
- **Extracts**: Metabolic/signaling pathways
- **Format**: KEGG flat file
- **Rate**: **3 requests/second** (strict limit)

```python
extractor = KEGGExtractor()  # Automatically rate-limited to 3/sec
pathways = extractor.extract(organism='hsa')
```

### Neuroscience

#### AllenBrainExtractor
- **Source**: Allen Brain Atlas
- **Extracts**: Brain structures, connectivity
- **Format**: JSON API

#### NeuroMorphoExtractor
- **Source**: NeuroMorpho.org
- **Extracts**: Neuronal morphologies, cell types
- **Format**: JSON API

#### CellOntologyExtractor
- **Source**: Cell Ontology (via OLS)
- **Extracts**: Cell type classifications
- **Format**: OLS JSON API

### Proteins & Enzymes

#### UniProtExtractor
- **Source**: UniProt
- **Extracts**: Protein families, domains
- **Format**: REST API, JSON
- **Focus**: Family-level, not individual sequences

#### InterProExtractor
- **Source**: InterPro
- **Extracts**: Protein domain architectures
- **Format**: REST API, JSON

#### BRENDAExtractor
- **Source**: BRENDA
- **Extracts**: Enzyme catalytic mechanisms
- **Format**: SOAP API
- **Auth**: Required (email + password)

### Metabolic

#### ChEBIExtractor
- **Source**: ChEBI
- **Extracts**: Chemical entities, biological roles
- **Format**: SOAP API, REST API

#### EQuilibratorExtractor
- **Source**: eQuilibrator
- **Extracts**: Thermodynamic parameters
- **Format**: REST API

### Cognitive

#### CognitiveAtlasExtractor
- **Source**: Cognitive Atlas
- **Extracts**: Cognitive concepts, tasks
- **Format**: REST API, JSON

#### CogPOExtractor
- **Source**: Cognitive Paradigm Ontology (BioPortal)
- **Extracts**: Experimental paradigms
- **Format**: BioPortal API
- **Auth**: API key required

#### MFOExtractor
- **Source**: Mental Functioning Ontology (BioPortal)
- **Extracts**: Mental states, processes
- **Format**: BioPortal API
- **Auth**: API key required

## Output

### File Output

Results are saved to `extraction_results/` by default:

```
extraction_results/
├── GO_extracted.json
├── Reactome_extracted.json
├── KEGG_extracted.json
├── ...
└── extraction_report.json
```

### Database Output

Entities are inserted into `bio_architecture.db` using the schema from `bio_architecture_schema.sql`.

### Report Format

```json
{
  "extraction_summary": {
    "total_databases": 10,
    "total_items_extracted": 4523,
    "total_errors": 2,
    "duration_seconds": 342.5
  },
  "database_breakdown": {
    "GO": {
      "item_count": 500,
      "entity_types": {
        "process": 320,
        "mechanism": 180
      }
    }
  }
}
```

## Performance

### Benchmarks

Typical extraction performance (with caching):

- **GO**: ~500 terms in 30-60 seconds
- **Reactome**: ~300 pathways in 45-90 seconds
- **KEGG**: ~300 pathways in 100-120 seconds (rate limited)
- **Total**: ~3000-5000 entities in 5-10 minutes

### Optimization Tips

1. **Enable Caching**: Reduces redundant API calls
2. **Parallel Extraction**: Set `max_workers: 4` or higher
3. **Focus on High-Value Terms**: Use filters in config
4. **Batch Processing**: Extract in batches for large datasets

## Error Handling

The framework handles various error scenarios:

- **Network Errors**: Automatic retry with exponential backoff
- **Rate Limits**: Automatic throttling and waiting
- **Invalid Data**: Logged and skipped, extraction continues
- **Authentication Failures**: Clear error messages

## Logging

Logs are written to both console and `extraction.log`:

```
2025-12-10 10:30:45 - GOExtractor - INFO - Starting GO extraction...
2025-12-10 10:30:50 - GOExtractor - INFO - Parsed 500 GO terms from OBO file
2025-12-10 10:31:00 - BaseExtractor - INFO - Cache hit rate: 85.3%
```

## Development

### Adding a New Extractor

1. Create extractor class inheriting from `BaseExtractor`
2. Implement `extract()` method
3. Add to `__init__.py`
4. Add configuration to `extraction_config.yaml`
5. Add to `extract_all.py` orchestrator

Example:

```python
from .base import BaseExtractor

class MyDatabaseExtractor(BaseExtractor):
    def __init__(self, **kwargs):
        super().__init__(rate_limit_calls=10, **kwargs)
        self.base_url = "https://api.mydatabase.org"

    def extract(self, max_items=500):
        data = self.get_json(f"{self.base_url}/data")
        return [self._transform(item) for item in data]

    def _transform(self, item):
        return {
            'identifier': item['id'],
            'name': item['name'],
            'entity_type': 'process'
        }
```

### Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=bio_extractors tests/

# Test specific extractor
pytest tests/test_go_extractor.py
```

### Code Quality

```bash
# Format code
black bio_extractors/

# Lint
flake8 bio_extractors/

# Type check
mypy bio_extractors/
```

## Troubleshooting

### Common Issues

**Problem**: "Rate limit exceeded"
**Solution**: Increase `rate_limit_period` in config

**Problem**: "Authentication failed"
**Solution**: Check credentials in config file

**Problem**: "Connection timeout"
**Solution**: Increase `request_timeout` in config

**Problem**: "Cache corruption"
**Solution**: Clear cache directory: `rm -rf .cache/`

### Debug Mode

Enable debug logging:

```bash
python extract_all.py --config config/extraction_config.yaml
```

Edit config:
```yaml
logging:
  level: "DEBUG"
```

## API Documentation

See individual extractor modules for detailed API documentation:

- [Base Extractor](base.py)
- [Mechanisms Extractors](mechanisms_extractors.py)
- [Neuroscience Extractors](neuroscience_extractors.py)
- [Protein Extractors](protein_extractors.py)
- [Metabolic Extractors](metabolic_extractors.py)
- [Cognitive Extractors](cognitive_extractors.py)

## License

This framework is part of the BioArchitecture project. See main repository for license information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Support

For issues, questions, or contributions:
- GitHub Issues: [link]
- Documentation: [link]
- Contact: [email]

## Version History

- **1.0.0** (2025-12-10): Initial release
  - Base infrastructure
  - 14 database extractors
  - Orchestration framework
  - Configuration system

## Acknowledgments

- Gene Ontology Consortium
- Reactome Team
- KEGG Database
- Allen Institute for Brain Science
- NeuroMorpho.org
- UniProt Consortium
- BRENDA Enzyme Database
- ChEBI Team
- Cognitive Atlas Project
- BioPortal Team
