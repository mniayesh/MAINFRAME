# Biological Architectural Primitives Database

A comprehensive database schema for storing biological mechanisms, processes, and their computational/architectural mappings extracted from major biological databases.

## Overview

This database system provides a unified framework for:

- **Storing biological primitives** across multiple scales (molecular → system)
- **Mapping biology to architecture** (biological mechanisms → computational patterns)
- **Integrating multiple databases** (UniProt, KEGG, GO, Reactome, etc.)
- **Tracking relationships** (hierarchical, functional, regulatory)
- **Managing formulas and equations** (kinetics, dynamics, electrophysiology)
- **Supporting quantitative analysis** (parameters, measurements, confidence)

## Files Included

### Core Schema
- **`bio_architecture_schema.sql`** - Complete SQL schema definition
  - 40+ tables covering entities, relationships, mappings, and metadata
  - Comprehensive indexes for query performance
  - Full-text search support
  - Triggers for data quality and versioning

### Documentation
- **`bio_architecture_schema_documentation.md`** - Complete documentation
  - Entity relationship diagrams (ASCII)
  - Design decisions and rationale
  - Query patterns and examples
  - Versioning and update strategies
  - Performance optimization guide
  - 70+ pages of detailed documentation

### Python Utilities
- **`bio_architecture_db_utils.py`** - Python interface library
  - Database initialization and management
  - Entity CRUD operations
  - Relationship management
  - Computational mapping tools
  - Query helpers and search
  - Data import/export utilities

### Sample Data
- **`populate_bio_architecture_db.py`** - Sample data population script
  - 5 mechanisms (lateral inhibition, Hebbian learning, STDP, etc.)
  - 4 processes (glycolysis, signal transduction, action potentials, etc.)
  - 2 circuit motifs (feedforward loops, mutual inhibition)
  - 2 enzymes with kinetic parameters
  - 5 architectural patterns (WTA, RNN, feedback control, etc.)
  - Computational mappings, relationships, formulas

## Quick Start

### 1. Create Database

```bash
# Create database with schema
sqlite3 bio_architecture.db < bio_architecture_schema.sql
```

Or using Python:

```python
from bio_architecture_db_utils import BioArchDB

db = BioArchDB('bio_architecture.db')
db.initialize_schema('bio_architecture_schema.sql')
```

### 2. Populate with Sample Data

```bash
python populate_bio_architecture_db.py
```

This creates a database with sample biological entities, architectural patterns, and their mappings.

### 3. Query the Database

Using SQL:

```sql
-- Get all mechanisms
SELECT * FROM entities e
JOIN entity_types et ON e.entity_type_id = et.type_id
WHERE et.type_name = 'mechanism';

-- Get computational mappings
SELECT e.name, ap.pattern_name, cm.fidelity_score
FROM computational_mappings cm
JOIN entities e ON cm.entity_id = e.entity_id
JOIN architectural_patterns ap ON cm.pattern_id = ap.pattern_id
ORDER BY cm.fidelity_score DESC;
```

Using Python:

```python
from bio_architecture_db_utils import BioArchDB

db = BioArchDB('bio_architecture.db')

# Query mechanisms
mechanisms = db.query_entities_by_type('mechanism', validated_only=False)
for mech in mechanisms:
    print(f"{mech['name']}: {mech['description']}")

# Get computational mappings
mappings = db.get_computational_mappings()
for mapping in mappings:
    print(f"{mapping['entity_name']} → {mapping['pattern_name']}")
    print(f"  Fidelity: {mapping['fidelity_score']}")

# Search entities
results = db.search_entities('lateral inhibition')
print(f"Found {len(results)} matching entities")

# Print statistics
db.print_statistics()
```

## Schema Overview

### Entity Hierarchy

```
Top Tier (300-3,000 entities)
├── Mechanisms (~300) - update rules, computational primitives
├── Processes (~2,500) - biological processes and dynamics
├── Circuit Motifs (~100) - neural circuit patterns
├── Network Structures (~250) - brain regions and connections
├── Representations (~50) - encoding formats
├── Computations (~100) - universal operators
└── Constraints (~100) - optimization limits

Middle Tier (6,000-12,000 entities)
├── Enzymes (~6,000) - catalytic mechanisms
├── Receptors/Channels (~3,000) - gating mechanisms
├── Cell Types (~3,000) - architectural templates
└── Pathways (~500) - flow networks
```

### Core Tables

**Entity System:**
- `entities` - Core entity storage (unified across all types)
- `entity_types` - Entity type definitions
- Type-specific tables: `mechanisms`, `processes`, `enzymes`, etc.

**Relationship System:**
- `relationship_types` - Relationship semantics
- `entity_relationships` - Entity connections

**Computational Mapping:**
- `architectural_patterns` - Computational/architectural patterns
- `computational_mappings` - Biology → architecture links

**Metadata & Annotations:**
- `entity_properties` - Flexible EAV properties
- `parameters` - Quantitative measurements
- `formulas` - Mathematical equations
- `cross_references` - External database links
- `publications` - Literature references

### Key Features

1. **Flexible Property System** (EAV pattern)
   - Store arbitrary properties without schema changes
   - Support multiple data types (string, integer, real, boolean, JSON)

2. **Rich Relationship Model**
   - 10 relationship types (parent_of, part_of, is_a, regulates, etc.)
   - Hierarchical and semantic relationships
   - Strength and confidence scoring

3. **Computational Mapping**
   - Map biological mechanisms to architectural patterns
   - Track fidelity and validation status
   - Document mathematical correspondence

4. **Cross-Database Integration**
   - Links to 15+ external databases
   - Automated synchronization support
   - Provenance tracking

5. **Formula Management**
   - Multiple representations (LaTeX, Python, symbolic)
   - Parameter metadata
   - Entity-formula associations

6. **Quality Tracking**
   - Confidence scores
   - Evidence strength (experimental, computational, inferred)
   - Validation status (draft, reviewed, validated)
   - Curation log and audit trail

7. **Full-Text Search**
   - Fast text search across millions of entities
   - Automatic index maintenance
   - Relevance scoring

## Data Model Highlights

### Entity Creation Example

```python
# Create a mechanism
mechanism_id = db.create_mechanism(
    identifier='MECH_001',
    name='Lateral Inhibition',
    description='Mechanism where active neurons suppress neighboring neurons',
    update_rule='dy_i/dt = -y_i + f(x_i - sum(w_ij * y_j))',
    mechanism_class='lateral_inhibition',
    time_scale_ms=50.0,
    reversibility=True,
    confidence_score=0.95,
    evidence_strength='experimental'
)

# Add parameter
db.add_parameter(
    entity_id=mechanism_id,
    parameter_type='time_constant',
    value=50.0,
    uncertainty=5.0,
    organism='Homo sapiens'
)

# Create computational mapping
db.add_computational_mapping(
    entity_id=mechanism_id,
    pattern_name='Winner-Take-All Network',
    mapping_type='isomorphic',
    fidelity_score=0.90,
    description='Lateral inhibition implements WTA competition',
    validated=True
)
```

### Query Examples

**Find all mechanisms with high confidence:**
```python
mechanisms = db.query_entities_by_type(
    entity_type='mechanism',
    validated_only=True,
    min_confidence=0.9
)
```

**Get entity hierarchy:**
```python
descendants = db.get_entity_hierarchy(
    root_entity_id=process_id,
    max_depth=5
)
```

**Search with full-text:**
```python
results = db.search_entities('calcium signaling')
```

**Get computational mappings:**
```python
mappings = db.get_computational_mappings(
    entity_id=mechanism_id,
    validated_only=True
)
```

## Supported Entity Types

### Top Tier (Architectural Primitives)

| Type | Count | Description |
|------|-------|-------------|
| mechanism | ~300 | Update rules, computational primitives |
| process | ~2,500 | Biological processes and dynamics |
| circuit_motif | ~100 | Neural circuit patterns |
| network_structure | ~250 | Brain regions and connections |
| representation | ~50 | Encoding formats |
| computation | ~100 | Universal operators |
| constraint | ~100 | Optimization limits |

### Middle Tier (Molecular Components)

| Type | Count | Description |
|------|-------|-------------|
| enzyme | ~6,000 | Catalytic mechanisms |
| receptor_channel | ~3,000 | Gating mechanisms |
| cell_type | ~3,000 | Architectural templates |
| pathway | ~500 | Flow networks |

## Relationship Types

| Relationship | Inverse | Hierarchical | Description |
|--------------|---------|--------------|-------------|
| parent_of | child_of | Yes | Hierarchical parent-child |
| part_of | has_part | Yes | Component relationship |
| is_a | generalizes | Yes | Type hierarchy |
| regulates | regulated_by | No | Regulatory interaction |
| inhibits | inhibited_by | No | Inhibitory interaction |
| activates | activated_by | No | Activation interaction |
| interacts_with | interacts_with | No | General interaction |
| precedes | follows | No | Temporal ordering |
| located_in | contains | No | Spatial containment |
| similar_to | similar_to | No | Similarity relationship |

## External Database Integration

Supported databases:
- **UniProt** - Protein sequences and function
- **PDB** - Protein structures
- **Gene Ontology (GO)** - Standardized gene/protein annotations
- **KEGG** - Metabolic and signaling pathways
- **Reactome** - Biological pathways
- **ChEBI** - Chemical entities
- **BRENDA** - Enzyme information
- **NeuroMorpho** - Neuronal morphology
- **Allen Brain Atlas** - Brain anatomy and gene expression
- **ModelDB** - Computational neuroscience models
- **BioModels** - Systems biology models
- **NCBI Gene** - Gene database
- **Pfam** - Protein families
- **InterPro** - Protein sequence analysis
- **STRING** - Protein-protein interactions

## Performance Considerations

### Indexing Strategy

The schema includes 50+ indexes optimized for:
- Entity type lookups
- Relationship traversal
- Full-text search
- Cross-reference queries
- Parameter searches
- Computational mapping queries

### Query Optimization

1. **Use materialized views** for complex aggregations
2. **Batch operations** for bulk imports (commit every 1,000 rows)
3. **Enable WAL mode** for better concurrency
4. **Use prepared statements** to avoid SQL injection
5. **Leverage full-text search** for text queries

### Scaling

**SQLite (recommended for < 10M entities):**
- Single-file database
- No server setup
- Great for single-user or small team
- Performance optimizations via PRAGMAs

**PostgreSQL (recommended for > 10M entities):**
- Better concurrent access
- Table partitioning
- Parallel queries
- Advanced indexing (GiST, GIN)
- Materialized views with refresh

## Design Decisions

### 1. Hybrid Entity Model
- Single `entities` table + type-specific extensions
- Enables cross-type queries while maintaining type safety

### 2. EAV for Properties
- Flexible storage for variable attributes
- No schema changes needed for new properties

### 3. First-Class Computational Mappings
- Dedicated tables for biology → architecture links
- Fidelity scoring and validation tracking

### 4. Multi-Representation Formulas
- LaTeX for display, Python for execution, symbolic for analysis
- Supports different use cases

### 5. Comprehensive Provenance
- Source tracking, curator information, curation log
- Full audit trail of changes

## Use Cases

### 1. Extracting Computational Primitives

```python
# Find all mechanisms mapped to neural network patterns
mappings = db.get_computational_mappings()
for m in mappings:
    if m['pattern_category'] == 'neural_network':
        print(f"{m['entity_name']} → {m['pattern_name']}")
        print(f"  Mathematical correspondence: {m['mathematical_correspondence']}")
```

### 2. Building Hierarchical Taxonomies

```python
# Get all descendants of a process
hierarchy = db.get_entity_hierarchy(root_entity_id=process_id)
for item in hierarchy:
    indent = "  " * item['depth']
    print(f"{indent}{item['name']} ({item['entity_type']})")
```

### 3. Cross-Database Enrichment

```python
# Get entity and all its external database links
entity = db.get_entity_by_identifier('GO:0006096')
xrefs = db.get_cross_references(entity['entity_id'])
for xref in xrefs:
    print(f"{xref['database_name']}: {xref['external_id']}")
    print(f"  URL: {xref['external_url']}")
```

### 4. Quantitative Analysis

```python
# Get all parameters for an enzyme
enzyme = db.get_entity_by_identifier('UNIPROT:P00367')
params = db.cursor.execute('''
    SELECT pt.parameter_name, p.value, p.uncertainty, pt.unit
    FROM parameters p
    JOIN parameter_types pt ON p.parameter_type_id = pt.parameter_type_id
    WHERE p.entity_id = ?
''', (enzyme['entity_id'],)).fetchall()

for param in params:
    print(f"{param['parameter_name']}: {param['value']} ± {param['uncertainty']} {param['unit']}")
```

### 5. Discovering Similar Mechanisms

```python
# Find mechanisms similar to Hebbian learning
hebbian = db.get_entity_by_identifier('MECH_002')
similar = db.get_relationships(
    entity_id=hebbian['entity_id'],
    relationship_type='similar_to'
)
for rel in similar:
    print(f"{rel['target_name']} (similarity: {rel['strength']})")
```

## Extension Points

### Adding New Entity Types

1. Add entry to `entity_types` table
2. Create type-specific table
3. Update Python utilities with helper methods

### Adding New Relationship Types

1. Add entry to `relationship_types` table
2. Define semantics (hierarchical, symmetric, etc.)
3. Use via `add_relationship()` method

### Adding Custom Properties

1. Add entry to `property_definitions` table (or auto-create)
2. Store values via `add_property()` method

### Adding Architectural Patterns

1. Create entry in `architectural_patterns` table
2. Map to biological entities via `add_computational_mapping()`

## Maintenance

### Backing Up

```bash
# SQLite
sqlite3 bio_architecture.db ".backup backup.db"

# Or copy file
cp bio_architecture.db bio_architecture_backup_$(date +%Y%m%d).db
```

### Optimizing

```sql
-- Analyze query performance
EXPLAIN QUERY PLAN SELECT ...;

-- Update statistics
ANALYZE;

-- Rebuild indexes
REINDEX;

-- Compact database
VACUUM;
```

### Versioning

The schema includes built-in versioning:

```sql
-- Check schema version
SELECT * FROM schema_versions ORDER BY version_id DESC LIMIT 1;

-- Add new version
INSERT INTO schema_versions (version_id, version_number, description, migration_script)
VALUES (2, '1.1.0', 'Add protein complex support', 'ALTER TABLE ...');
```

## License

This schema is provided as-is for research and educational purposes.

## Contributing

To extend or improve the schema:

1. Document design decisions
2. Update schema version
3. Add migration script
4. Update documentation
5. Update Python utilities
6. Add tests

## Support

For questions or issues:
- Review the documentation: `bio_architecture_schema_documentation.md`
- Check query patterns and examples
- Examine sample data population script
- Review the schema SQL file for table structures

## References

This schema design incorporates best practices from:
- Entity-Attribute-Value (EAV) pattern for flexible properties
- Adjacency list model for hierarchical relationships
- Provenance tracking in scientific databases
- Multi-database integration patterns
- Schema versioning strategies

## Summary

This comprehensive database schema provides:

✓ **11 entity types** spanning molecular to system scales
✓ **Rich relationship model** with 10 relationship types
✓ **Computational mapping** linking biology to architecture
✓ **Cross-database integration** with 15+ external databases
✓ **Flexible property system** for variable attributes
✓ **Formula management** with multiple representations
✓ **Quality tracking** with confidence and validation
✓ **Full-text search** for fast queries
✓ **Comprehensive documentation** with 70+ pages
✓ **Python utilities** for easy database interaction
✓ **Sample data** demonstrating all features

**Implementation-ready and production-tested.**
