# Biological Architectural Primitives Database - Quick Reference

## Table Summary

### Core Entity Tables (3)
```
entities              - Core entity storage (all types unified)
entity_types          - Entity type definitions (11 types)
curators              - Curator information
```

### Type-Specific Tables (11)
```
mechanisms            - Update rules, computational primitives (~300)
processes             - Biological processes and dynamics (~2.5k)
circuit_motifs        - Neural circuit patterns (~100)
network_structures    - Brain regions and connections (~250)
representations       - Encoding formats (~50)
computations          - Universal operators (~100)
constraints           - Optimization limits (~100)
enzymes               - Catalytic mechanisms (~6k)
receptors_channels    - Gating mechanisms (~3k)
cell_types            - Architectural templates (~3k)
pathways              - Flow networks (~500)
```

### Relationship Tables (2)
```
relationship_types     - Relationship semantics (10 types)
entity_relationships   - Entity connections (source → target)
```

### Property & Parameter Tables (4)
```
property_definitions   - Define flexible properties
entity_properties      - EAV storage for properties
parameter_types        - Quantitative parameter types
parameters             - Measured values with uncertainty
```

### Computational Mapping (2)
```
architectural_patterns - Computational/architectural patterns
computational_mappings - Biology → architecture links
```

### Formula Tables (3)
```
formula_categories     - Formula classifications
formulas               - Mathematical equations (multi-format)
entity_formulas        - Link entities to formulas
```

### Cross-Reference Tables (3)
```
external_databases     - External database registry (15+ databases)
cross_references       - Links to external IDs
publications           - Literature references
entity_publications    - Entity-publication links
```

### Taxonomy & Annotation (5)
```
organisms              - Species/organism information
entity_organisms       - Entity-organism associations
tags                   - Flexible categorization
entity_tags            - Entity-tag associations
entity_notes           - Comments and curation notes
```

### Audit & Versioning (2)
```
curation_log          - Full audit trail
schema_versions       - Schema version tracking
```

### Views (3)
```
v_architectural_primitives - Top-tier entities with mappings
v_entity_hierarchy         - Hierarchical relationships
v_entity_completeness      - Data completeness scores
```

### Full-Text Search (1)
```
entities_fts          - FTS5 virtual table for search
```

**Total: 40+ tables + 3 views + 50+ indexes**

---

## Entity Type Reference

| ID | Type Name | Category | Est. Count | Description |
|----|-----------|----------|------------|-------------|
| 1 | mechanism | top_tier | 300 | Update rules and computational primitives |
| 2 | process | top_tier | 2,500 | Biological processes and their dynamics |
| 3 | circuit_motif | top_tier | 100 | Neural circuit patterns |
| 4 | network_structure | top_tier | 250 | Brain regions and connections |
| 5 | representation | top_tier | 50 | Encoding formats |
| 6 | computation | top_tier | 100 | Universal operators |
| 7 | constraint | top_tier | 100 | Optimization limits |
| 8 | enzyme | middle_tier | 6,000 | Catalytic mechanisms |
| 9 | receptor_channel | middle_tier | 3,000 | Gating mechanisms |
| 10 | cell_type | middle_tier | 3,000 | Architectural templates |
| 11 | pathway | middle_tier | 500 | Flow networks |

---

## Relationship Type Reference

| ID | Type | Inverse | Hierarchical | Symmetric | Usage |
|----|------|---------|--------------|-----------|-------|
| 1 | parent_of | child_of | ✓ | ✗ | Hierarchy |
| 2 | part_of | has_part | ✓ | ✗ | Composition |
| 3 | is_a | generalizes | ✓ | ✗ | Taxonomy |
| 4 | regulates | regulated_by | ✗ | ✗ | Regulation |
| 5 | inhibits | inhibited_by | ✗ | ✗ | Inhibition |
| 6 | activates | activated_by | ✗ | ✗ | Activation |
| 7 | interacts_with | interacts_with | ✗ | ✓ | Interaction |
| 8 | precedes | follows | ✗ | ✗ | Temporal |
| 9 | located_in | contains | ✗ | ✗ | Spatial |
| 10 | similar_to | similar_to | ✗ | ✓ | Similarity |

---

## Parameter Type Reference

| ID | Name | Unit | Description |
|----|------|------|-------------|
| 1 | rate_constant | s^-1 | Kinetic rate constant |
| 2 | binding_affinity | M | Binding affinity (Kd) |
| 3 | time_constant | ms | Characteristic time constant |
| 4 | energy | kJ/mol | Free energy change |
| 5 | voltage | mV | Membrane potential |
| 6 | current | pA | Ionic current |
| 7 | concentration | M | Molecular concentration |
| 8 | flux | mmol/s | Metabolic flux |
| 9 | distance | um | Spatial distance |
| 10 | frequency | Hz | Oscillation frequency |

---

## External Database Reference

| ID | Database | URL | Type |
|----|----------|-----|------|
| 1 | UniProt | uniprot.org | Proteins |
| 2 | PDB | rcsb.org | Structures |
| 3 | GO | geneontology.org | Ontology |
| 4 | KEGG | kegg.jp | Pathways |
| 5 | Reactome | reactome.org | Pathways |
| 6 | ChEBI | ebi.ac.uk/chebi | Chemicals |
| 7 | BRENDA | brenda-enzymes.org | Enzymes |
| 8 | NeuroMorpho | neuromorpho.org | Morphology |
| 9 | Allen Brain Atlas | brain-map.org | Brain |
| 10 | ModelDB | modeldb.science | Models |
| 11 | BioModels | ebi.ac.uk/biomodels | Models |
| 12 | NCBI Gene | ncbi.nlm.nih.gov/gene | Genes |
| 13 | Pfam | pfam.xfam.org | Families |
| 14 | InterPro | ebi.ac.uk/interpro | Proteins |
| 15 | STRING | string-db.org | Networks |

---

## Common Query Patterns

### 1. Find Entity by Identifier
```sql
SELECT * FROM entities WHERE identifier = 'GO:0006096';
```

### 2. Get All Entities of Type
```sql
SELECT e.* FROM entities e
JOIN entity_types et ON e.entity_type_id = et.type_id
WHERE et.type_name = 'mechanism';
```

### 3. Get Entity with Type-Specific Data
```sql
SELECT e.*, m.* FROM entities e
JOIN mechanisms m ON e.entity_id = m.entity_id
WHERE e.entity_id = ?;
```

### 4. Get Entity Relationships
```sql
SELECT er.*, e.name as related_entity
FROM entity_relationships er
JOIN entities e ON er.target_entity_id = e.entity_id
WHERE er.source_entity_id = ?;
```

### 5. Get Computational Mappings
```sql
SELECT e.name, ap.pattern_name, cm.fidelity_score
FROM computational_mappings cm
JOIN entities e ON cm.entity_id = e.entity_id
JOIN architectural_patterns ap ON cm.pattern_id = ap.pattern_id
WHERE cm.validated = 1
ORDER BY cm.fidelity_score DESC;
```

### 6. Get Entity Hierarchy (Recursive)
```sql
WITH RECURSIVE descendants AS (
    SELECT entity_id, 0 as depth FROM entities WHERE entity_id = ?
    UNION ALL
    SELECT er.target_entity_id, d.depth + 1
    FROM entity_relationships er
    JOIN descendants d ON er.source_entity_id = d.entity_id
    JOIN relationship_types rt ON er.relationship_type_id = rt.relationship_type_id
    WHERE rt.is_hierarchical = 1
)
SELECT * FROM descendants;
```

### 7. Full-Text Search
```sql
SELECT e.* FROM entities_fts fts
JOIN entities e ON fts.entity_id = e.entity_id
WHERE entities_fts MATCH 'calcium AND signaling'
ORDER BY rank;
```

### 8. Get Cross-References
```sql
SELECT db.database_name, xr.external_id, xr.external_url
FROM cross_references xr
JOIN external_databases db ON xr.database_id = db.database_id
WHERE xr.entity_id = ?;
```

### 9. Get Parameters
```sql
SELECT pt.parameter_name, p.value, p.uncertainty, pt.unit
FROM parameters p
JOIN parameter_types pt ON p.parameter_type_id = pt.parameter_type_id
WHERE p.entity_id = ?;
```

### 10. Get Formulas
```sql
SELECT f.name, f.latex_notation, f.python_code
FROM entity_formulas ef
JOIN formulas f ON ef.formula_id = f.formula_id
WHERE ef.entity_id = ?;
```

---

## Python Quick Reference

### Initialize Database
```python
from bio_architecture_db_utils import BioArchDB
db = BioArchDB('bio_architecture.db')
db.initialize_schema('bio_architecture_schema.sql')
```

### Create Entities
```python
# Mechanism
mechanism_id = db.create_mechanism(
    identifier='MECH_001',
    name='Lateral Inhibition',
    update_rule='dy_i/dt = -y_i + f(x_i - sum(w_ij * y_j))',
    mechanism_class='lateral_inhibition',
    time_scale_ms=50.0
)

# Process
process_id = db.create_process(
    identifier='GO:0006096',
    name='Glycolysis',
    process_category='metabolic',
    spatial_scale='cellular'
)

# Enzyme
enzyme_id = db.create_enzyme(
    identifier='UNIPROT:P00367',
    name='Alcohol dehydrogenase 1A',
    ec_number='EC 1.1.1.1',
    km_value=0.8,
    kcat_value=350.0
)
```

### Add Relationships
```python
db.add_relationship(
    source_entity_id=parent_id,
    target_entity_id=child_id,
    relationship_type='parent_of',
    strength=0.9,
    confidence=0.95
)
```

### Add Computational Mapping
```python
db.add_computational_mapping(
    entity_id=mechanism_id,
    pattern_name='Winner-Take-All Network',
    mapping_type='isomorphic',
    fidelity_score=0.90,
    validated=True
)
```

### Query Entities
```python
# By type
mechanisms = db.query_entities_by_type('mechanism', validated_only=True)

# By ID
entity = db.get_entity_by_id(entity_id)

# By identifier
entity = db.get_entity_by_identifier('GO:0006096')

# Full-text search
results = db.search_entities('calcium signaling')
```

### Get Related Data
```python
# Relationships
relationships = db.get_relationships(entity_id, direction='both')

# Computational mappings
mappings = db.get_computational_mappings(entity_id=entity_id)

# Cross-references
xrefs = db.get_cross_references(entity_id)

# Hierarchy
hierarchy = db.get_entity_hierarchy(root_entity_id, max_depth=5)
```

### Add Metadata
```python
# Parameter
db.add_parameter(
    entity_id=entity_id,
    parameter_type='time_constant',
    value=50.0,
    uncertainty=5.0
)

# Property
db.add_property(
    entity_id=entity_id,
    property_name='substrate_specificity',
    value='alcohol',
    confidence=0.95
)

# Cross-reference
db.add_cross_reference(
    entity_id=entity_id,
    database_name='UniProt',
    external_id='P00367',
    external_url='https://www.uniprot.org/uniprot/P00367'
)
```

### Statistics
```python
stats = db.get_statistics()
db.print_statistics()
```

---

## Field Reference

### entities Table
```
entity_id              INTEGER PRIMARY KEY
entity_type_id         INTEGER (FK → entity_types)
identifier             VARCHAR(100) UNIQUE
name                   VARCHAR(500)
common_name            VARCHAR(500)
description            TEXT
mathematical_formulation TEXT
complexity_level       VARCHAR(20)
confidence_score       REAL (0-1)
evidence_strength      VARCHAR(20)
validation_status      VARCHAR(20)
created_at            TIMESTAMP
updated_at            TIMESTAMP
version               INTEGER
source_database       VARCHAR(100)
curator               VARCHAR(200)
```

### entity_relationships Table
```
relationship_id       INTEGER PRIMARY KEY
source_entity_id      INTEGER (FK → entities)
target_entity_id      INTEGER (FK → entities)
relationship_type_id  INTEGER (FK → relationship_types)
strength              REAL (0-1)
confidence            REAL (0-1)
context               TEXT
evidence              TEXT
created_at           TIMESTAMP
source_database      VARCHAR(100)
```

### computational_mappings Table
```
mapping_id                   INTEGER PRIMARY KEY
entity_id                    INTEGER (FK → entities)
pattern_id                   INTEGER (FK → architectural_patterns)
mapping_type                 VARCHAR(50)
fidelity_score              REAL (0-1)
description                 TEXT
mathematical_correspondence TEXT
implementation_notes        TEXT
code_example                TEXT
abstraction_level           VARCHAR(50)
validated                   BOOLEAN
created_at                  TIMESTAMP
created_by                  VARCHAR(200)
```

---

## Validation Status Values

```
draft      - Initial entry, not yet reviewed
reviewed   - Peer-reviewed, awaiting final validation
validated  - Fully validated and approved
deprecated - No longer current, kept for reference
```

## Evidence Strength Values

```
experimental  - Direct experimental evidence
computational - Computational/simulation evidence
inferred      - Inferred from related data
predicted     - Predicted by model/algorithm
```

## Complexity Level Values

```
simple    - Basic, well-understood
moderate  - Intermediate complexity
complex   - Highly complex or poorly understood
```

## Mapping Type Values

```
isomorphic   - One-to-one mathematical correspondence
analogous    - Similar but not identical
approximates - Rough approximation
```

---

## Index Reference

### Primary Indexes
- All primary keys (automatic)
- All foreign keys

### Lookup Indexes
```
idx_entities_type          - entities(entity_type_id)
idx_entities_identifier    - entities(identifier)
idx_entities_name          - entities(name)
idx_entities_validation    - entities(validation_status)
```

### Relationship Indexes
```
idx_relationships_source   - entity_relationships(source_entity_id)
idx_relationships_target   - entity_relationships(target_entity_id)
idx_relationships_type     - entity_relationships(relationship_type_id)
```

### Composite Indexes
```
idx_composite_entity_type_status    - entities(entity_type_id, validation_status)
idx_composite_entity_type_confidence - entities(entity_type_id, confidence_score)
idx_composite_params_entity_type     - parameters(entity_id, parameter_type_id)
idx_composite_xref_db_id             - cross_references(database_id, external_id)
```

### Type-Specific Indexes
```
idx_mechanisms_class       - mechanisms(mechanism_class)
idx_processes_category     - processes(process_category)
idx_enzymes_ec            - enzymes(ec_number)
idx_pathways_category     - pathways(pathway_category)
```

---

## Performance Tips

1. **Use prepared statements** for repeated queries
2. **Batch commits** for bulk inserts (every 1000 rows)
3. **Use indexes** for WHERE/JOIN clauses
4. **Limit result sets** with LIMIT/OFFSET
5. **Use views** for complex queries
6. **Enable WAL mode** for better concurrency
7. **Run ANALYZE** periodically
8. **Use full-text search** for text queries

## Maintenance Commands

```sql
-- Analyze tables for query optimization
ANALYZE;

-- Rebuild indexes
REINDEX;

-- Compact database
VACUUM;

-- Check integrity
PRAGMA integrity_check;

-- View schema
.schema entities

-- Export to CSV
.mode csv
.output entities.csv
SELECT * FROM entities;
.output stdout
```

---

## Quick Start Checklist

- [ ] Create database: `sqlite3 bio_architecture.db`
- [ ] Load schema: `.read bio_architecture_schema.sql`
- [ ] Populate sample data: `python populate_bio_architecture_db.py`
- [ ] Verify: `SELECT COUNT(*) FROM entities;`
- [ ] Query mechanisms: `SELECT * FROM v_architectural_primitives;`
- [ ] Test search: `SELECT * FROM entities_fts WHERE entities_fts MATCH 'inhibition';`
- [ ] Check stats: Python: `db.print_statistics()`

---

## Schema Version

**Current Version:** 1.0.0
**Date:** 2025-12-10
**Total Tables:** 40+
**Total Indexes:** 50+
**Total Views:** 3

---

## Support Files

1. `bio_architecture_schema.sql` - Full schema definition
2. `bio_architecture_schema_documentation.md` - Complete documentation
3. `bio_architecture_db_utils.py` - Python utilities
4. `populate_bio_architecture_db.py` - Sample data script
5. `BIO_ARCHITECTURE_SCHEMA_README.md` - Overview and guide
6. `schema_quick_reference.md` - This file

---

**For detailed documentation, see `bio_architecture_schema_documentation.md`**
