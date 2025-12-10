# Biological Architectural Primitives Database Schema Documentation

## Table of Contents
1. [Overview](#overview)
2. [Entity Relationship Diagram](#entity-relationship-diagram)
3. [Schema Design Decisions](#schema-design-decisions)
4. [Core Components](#core-components)
5. [Versioning and Updates](#versioning-and-updates)
6. [Query Patterns](#query-patterns)
7. [Data Import Strategies](#data-import-strategies)
8. [Performance Optimization](#performance-optimization)
9. [Extension Points](#extension-points)

---

## Overview

This schema stores biological architectural primitives extracted from major databases, supporting both **top-tier** entities (mechanisms, processes, circuit motifs, etc.) and **middle-tier** entities (enzymes, receptors, cell types, etc.) with rich metadata, relationships, and computational mappings.

### Design Philosophy

1. **Flexibility First**: Hybrid approach combining structured tables for core data with flexible EAV (Entity-Attribute-Value) pattern for variable properties
2. **Relationship-Centric**: Rich relationship system supporting hierarchies, interactions, and cross-references
3. **Computational Focus**: First-class support for mapping biological mechanisms to architectural patterns
4. **Provenance & Quality**: Built-in curation, versioning, and quality tracking
5. **Scalability**: Designed to handle millions of entities with efficient indexing

---

## Entity Relationship Diagram

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CORE ENTITY SYSTEM                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐   │
│  │ entity_types │────────>│   entities   │<────────│  curators    │   │
│  └──────────────┘         └──────────────┘         └──────────────┘   │
│         │                        │                                     │
│         v                        v                                     │
│  ┌──────────────────────────────────────────────┐                     │
│  │         TYPE-SPECIFIC TABLES                 │                     │
│  ├──────────────────────────────────────────────┤                     │
│  │ mechanisms | processes | circuit_motifs      │                     │
│  │ network_structures | representations         │                     │
│  │ computations | constraints                   │                     │
│  │ enzymes | receptors_channels | cell_types    │                     │
│  │ pathways                                     │                     │
│  └──────────────────────────────────────────────┘                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                  ┌───────────────┼───────────────┐
                  │               │               │
                  v               v               v
┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
│  RELATIONSHIPS      │ │   PROPERTIES    │ │   ANNOTATIONS       │
├─────────────────────┤ ├─────────────────┤ ├─────────────────────┤
│                     │ │                 │ │                     │
│ relationship_types  │ │ property_defs   │ │ tags                │
│        │            │ │        │        │ │   │                 │
│        v            │ │        v        │ │   v                 │
│ entity_relationships│ │ entity_props    │ │ entity_tags         │
│                     │ │                 │ │                     │
│ (hierarchical &     │ │ parameters      │ │ entity_notes        │
│  semantic links)    │ │                 │ │                     │
└─────────────────────┘ └─────────────────┘ └─────────────────────┘

                  ┌───────────────┼───────────────┐
                  │               │               │
                  v               v               v
┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
│  FORMULAS           │ │ COMPUTATIONAL   │ │ CROSS-REFERENCES    │
├─────────────────────┤ ├─────────────────┤ ├─────────────────────┤
│                     │ │                 │ │                     │
│ formula_categories  │ │ architectural_  │ │ external_databases  │
│        │            │ │   patterns      │ │        │            │
│        v            │ │        │        │ │        v            │
│ formulas            │ │        v        │ │ cross_references    │
│        │            │ │ computational_  │ │                     │
│        v            │ │   mappings      │ │ (UniProt, KEGG,     │
│ entity_formulas     │ │                 │ │  Reactome, etc.)    │
│                     │ │ (biology →      │ │                     │
│                     │ │  architecture)  │ │                     │
└─────────────────────┘ └─────────────────┘ └─────────────────────┘

                           │               │
                           v               v
                  ┌─────────────────┐ ┌─────────────────┐
                  │  PUBLICATIONS   │ │   ORGANISMS     │
                  ├─────────────────┤ ├─────────────────┤
                  │                 │ │                 │
                  │ publications    │ │ organisms       │
                  │        │        │ │        │        │
                  │        v        │ │        v        │
                  │ entity_pubs     │ │ entity_organisms│
                  │                 │ │                 │
                  │ (PMIDs, DOIs)   │ │ (taxonomy)      │
                  └─────────────────┘ └─────────────────┘
```

### Detailed Core Entity Model

```
┌────────────────────────────────────────────────────────────────┐
│                         entities                                │
├────────────────────────────────────────────────────────────────┤
│ PK: entity_id                                                  │
│ FK: entity_type_id → entity_types                              │
│                                                                │
│ Core Fields:                                                   │
│  - identifier (e.g., GO:0008150, EC 1.1.1.1)                  │
│  - name, common_name, description                              │
│  - mathematical_formulation                                    │
│  - complexity_level, confidence_score, evidence_strength       │
│  - validation_status, version                                  │
│  - created_at, updated_at                                      │
│  - source_database, curator                                    │
└────────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        v                  v                  v
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  mechanisms  │   │  processes   │   │circuit_motifs│
├──────────────┤   ├──────────────┤   ├──────────────┤
│ - mechanism_ │   │ - process_   │   │ - motif_     │
│   class      │   │   category   │   │   topology   │
│ - update_rule│   │ - temporal_  │   │ - node_count │
│ - time_scale │   │   dynamics   │   │ - connection_│
│ - reversibil-│   │ - spatial_   │   │   pattern    │
│   ity        │   │   scale      │   │ - transfer_  │
│              │   │ - rate_      │   │   function   │
│              │   │   equation   │   │              │
└──────────────┘   └──────────────┘   └──────────────┘

        ... (8 more type-specific tables)
```

### Relationship System

```
                    ┌─────────────────────────┐
                    │  relationship_types     │
                    ├─────────────────────────┤
                    │ - type_name             │
                    │ - inverse_type_name     │
                    │ - is_hierarchical       │
                    │ - is_symmetric          │
                    └─────────────────────────┘
                               │
                               v
     ┌──────────────────────────────────────────────────┐
     │        entity_relationships                      │
     ├──────────────────────────────────────────────────┤
     │ source_entity_id ──┐                             │
     │                    │  relationship_type_id       │
     │ target_entity_id ──┘                             │
     │                                                  │
     │ Properties:                                      │
     │  - strength (0-1)                                │
     │  - confidence (0-1)                              │
     │  - context                                       │
     │  - evidence                                      │
     └──────────────────────────────────────────────────┘

Supported Relationship Types:
  1. parent_of / child_of (hierarchical)
  2. part_of / has_part (compositional)
  3. is_a / generalizes (taxonomic)
  4. regulates / regulated_by (functional)
  5. inhibits / inhibited_by (functional)
  6. activates / activated_by (functional)
  7. interacts_with (symmetric)
  8. precedes / follows (temporal)
  9. located_in / contains (spatial)
  10. similar_to (symmetric)
```

### Computational Mapping System

```
┌─────────────────────────────────────────────────────────┐
│                 architectural_patterns                   │
├─────────────────────────────────────────────────────────┤
│ - pattern_name (e.g., "Winner-Take-All Network")        │
│ - pattern_category (control_flow, data_structure, ...)  │
│ - formal_description                                     │
│ - pseudocode                                             │
│ - complexity_class                                       │
│ - properties_json                                        │
└─────────────────────────────────────────────────────────┘
                           │
                           v
┌─────────────────────────────────────────────────────────┐
│              computational_mappings                      │
├─────────────────────────────────────────────────────────┤
│ entity_id ───> biological mechanism                     │
│ pattern_id ──> architectural pattern                    │
│                                                          │
│ Mapping Properties:                                      │
│  - mapping_type (isomorphic, analogous, approximates)   │
│  - fidelity_score (how well does it map?)               │
│  - description                                           │
│  - mathematical_correspondence                           │
│  - implementation_notes                                  │
│  - code_example                                          │
│  - abstraction_level (molecular → system)               │
│  - validated                                             │
└─────────────────────────────────────────────────────────┘
```

---

## Schema Design Decisions

### 1. Hybrid Entity Model (Unified + Type-Specific)

**Decision**: Use a single `entities` table for common fields, with type-specific extension tables for specialized attributes.

**Rationale**:
- **Unified queries**: Can query across all entity types easily
- **Type safety**: Specialized tables enforce domain-specific constraints
- **Performance**: Avoids sparse columns in single table
- **Extensibility**: Easy to add new entity types

**Trade-off**: Requires joins for complete entity data, but indexed properly this is performant.

### 2. EAV (Entity-Attribute-Value) for Properties

**Decision**: Use `property_definitions` + `entity_properties` for flexible attributes.

**Rationale**:
- Different entity types have vastly different properties
- Many properties are optional and domain-specific
- Allows adding new properties without schema changes
- Supports multiple value types (string, integer, real, boolean, text, JSON)

**Trade-off**: Slightly more complex queries, but provides maximum flexibility.

### 3. Relationship Types Table

**Decision**: Separate `relationship_types` table defining relationship semantics.

**Rationale**:
- Enforces relationship semantics (symmetric, hierarchical)
- Enables relationship-specific queries (e.g., "find all hierarchical relationships")
- Supports bidirectional relationships (parent_of ↔ child_of)
- Easy to add new relationship types

### 4. Computational Mapping as First-Class Concept

**Decision**: Dedicated `computational_mappings` table linking biology to architecture.

**Rationale**:
- Core purpose of the database
- Supports multiple mapping types (isomorphic, analogous, etc.)
- Includes fidelity scoring
- Separates biological description from computational interpretation

### 5. Formula Storage with Multiple Representations

**Decision**: Store formulas in LaTeX, Python, and symbolic forms.

**Rationale**:
- LaTeX for rendering/publication
- Python for execution/simulation
- Symbolic for analysis/transformation
- Different use cases require different representations

### 6. Comprehensive Cross-Referencing

**Decision**: Explicit `cross_references` table linking to external databases.

**Rationale**:
- Integrates with existing biological databases
- Supports data enrichment and updates
- Enables federated queries
- Maintains provenance

### 7. Full-Text Search Support

**Decision**: FTS5 virtual table for entity search with automatic sync triggers.

**Rationale**:
- Fast text search across millions of entities
- Automatic index maintenance
- Supports complex queries (phrase search, proximity)
- Database-agnostic (can port to PostgreSQL's tsvector)

### 8. Versioning at Entity Level

**Decision**: Version field in `entities` table, incremented on substantive changes.

**Rationale**:
- Simple to implement
- Tracks entity evolution
- Supports rollback via `curation_log`
- Lightweight compared to full temporal tables

**Alternative Considered**: Full temporal tables (SCD Type 2) - deemed too complex for initial implementation.

### 9. Quality and Confidence Tracking

**Decision**: Multiple quality indicators (confidence_score, evidence_strength, validation_status).

**Rationale**:
- Scientific data has varying quality
- Enables filtering by confidence
- Supports curation workflow (draft → reviewed → validated)
- Tracks evidence basis (experimental vs. computational)

### 10. Materialized Views for Common Queries

**Decision**: Views for architectural primitives, hierarchies, and completeness.

**Rationale**:
- Optimizes common query patterns
- Provides high-level abstractions
- Can be materialized in PostgreSQL for performance
- Easier to query than complex JOINs

---

## Core Components

### Entity System

The entity system is the foundation, storing all biological primitives in a unified structure:

```sql
-- Core entity with common fields
entities (
    entity_id, entity_type_id, identifier, name, description,
    mathematical_formulation, confidence_score, validation_status, ...
)

-- Type-specific extensions
mechanisms (mechanism_id, entity_id, mechanism_class, update_rule, ...)
processes (process_id, entity_id, process_category, temporal_dynamics, ...)
-- ... 9 more type tables
```

**Key Features**:
- Single point of reference for all entities
- Type discrimination via `entity_type_id`
- Extensible via type-specific tables

### Relationship System

Three-part relationship system:

1. **Relationship Types**: Define semantics
2. **Entity Relationships**: Store connections with properties
3. **Hierarchical Support**: Special handling for parent/child, part-of, is-a

**Example: Finding All Children**
```sql
SELECT e.name, rt.type_name
FROM entity_relationships er
JOIN entities e ON er.target_entity_id = e.entity_id
JOIN relationship_types rt ON er.relationship_type_id = rt.relationship_type_id
WHERE er.source_entity_id = ? AND rt.is_hierarchical = TRUE;
```

### Property System

Flexible EAV pattern for domain-specific properties:

1. **Property Definitions**: Define allowed properties
2. **Entity Properties**: Store actual values
3. **Type-Specific Value Fields**: Efficient storage

**Example: Finding Entities with High Km**
```sql
SELECT e.name, ep.value_real as km_value
FROM entities e
JOIN entity_properties ep ON e.entity_id = ep.entity_id
JOIN property_definitions pd ON ep.property_id = pd.property_id
WHERE pd.property_name = 'km_value' AND ep.value_real > 0.1;
```

### Computational Mapping

Links biological mechanisms to architectural patterns:

**Workflow**:
1. Define architectural pattern (pseudocode, complexity class)
2. Create mapping to biological entity
3. Specify mapping type and fidelity
4. Document mathematical correspondence
5. Validate mapping

**Example Mapping**:
- **Biological**: Lateral inhibition mechanism
- **Architectural**: Winner-take-all network
- **Mapping Type**: Isomorphic
- **Fidelity**: 0.90
- **Correspondence**: Inhibitory weights W_ij implement competitive suppression

### Formula System

Multi-representation formula storage:

```sql
formulas (
    formula_id, name, category_id,
    latex_notation,      -- For display
    python_code,         -- For execution
    symbolic_form,       -- For analysis
    variables_json,      -- Parameter metadata
    assumptions          -- When formula applies
)

entity_formulas (
    entity_id, formula_id,
    role,                -- governing_equation, constraint, etc.
    parameter_values     -- Specific values for this entity
)
```

### Cross-Reference System

Links to external databases (UniProt, KEGG, GO, etc.):

**Features**:
- Bidirectional links (internal ID ↔ external ID)
- Direct URLs to resources
- Confidence scoring
- Last verification timestamp

**Use Cases**:
- Data enrichment from external sources
- Synchronization with updates
- Provenance tracking
- Federated queries

---

## Versioning and Updates

### Schema Versioning

**Table**: `schema_versions`

**Purpose**: Track database schema evolution

**Workflow**:
1. Each schema change gets a version number (semantic versioning)
2. Migration script stored with version
3. Applied timestamp recorded
4. Supports rollback and forward migration

**Example**:
```sql
INSERT INTO schema_versions (version_id, version_number, description, migration_script)
VALUES (2, '1.1.0', 'Add support for protein complexes',
'ALTER TABLE entities ADD COLUMN complex_stoichiometry TEXT;');
```

### Entity Versioning

**Approach**: Optimistic versioning with audit trail

**Components**:
1. **Version field**: Integer counter in `entities` table
2. **Timestamps**: created_at, updated_at
3. **Curation log**: Full audit trail of changes

**Auto-increment trigger**:
```sql
CREATE TRIGGER increment_entity_version
AFTER UPDATE ON entities
FOR EACH ROW
WHEN OLD.description != NEW.description OR
     OLD.mathematical_formulation != NEW.mathematical_formulation
BEGIN
    UPDATE entities SET version = version + 1 WHERE entity_id = NEW.entity_id;
END;
```

### Update Strategies

#### Strategy 1: Incremental Updates
- Update individual entities as new data arrives
- Use `curation_log` to track changes
- Maintain version history

#### Strategy 2: Bulk Import with Conflict Resolution
```sql
-- On conflict, update if newer or higher confidence
INSERT INTO entities (entity_id, identifier, name, ...)
VALUES (?, ?, ?, ...)
ON CONFLICT(entity_type_id, identifier) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    updated_at = CURRENT_TIMESTAMP,
    version = version + 1
WHERE EXCLUDED.confidence_score > entities.confidence_score;
```

#### Strategy 3: Synchronization with External Databases
```sql
-- Record last sync time
UPDATE external_databases
SET last_sync = CURRENT_TIMESTAMP
WHERE database_id = ?;

-- Import new cross-references
INSERT INTO cross_references (entity_id, database_id, external_id, ...)
SELECT ... FROM external_api_results
ON CONFLICT DO NOTHING;
```

### Deprecation Workflow

1. Mark entity as deprecated:
```sql
UPDATE entities
SET validation_status = 'deprecated'
WHERE entity_id = ?;
```

2. Log deprecation reason:
```sql
INSERT INTO entity_notes (entity_id, note_type, content)
VALUES (?, 'deprecation', 'Replaced by entity X due to updated research');
```

3. Keep entity for historical reference (soft delete)

4. Update relationships to point to replacement entity

### Rollback Strategy

Use `curation_log` to reconstruct previous state:

```sql
-- Find changes to entity
SELECT field_changed, old_value, new_value, performed_at
FROM curation_log
WHERE entity_id = ? AND action_type = 'update'
ORDER BY performed_at DESC;

-- Restore specific field
UPDATE entities
SET description = (
    SELECT old_value FROM curation_log
    WHERE entity_id = ? AND field_changed = 'description'
    ORDER BY performed_at DESC LIMIT 1
)
WHERE entity_id = ?;
```

---

## Query Patterns

### Pattern 1: Find All Entities of a Type

```sql
-- Get all mechanisms with their details
SELECT
    e.entity_id,
    e.identifier,
    e.name,
    e.description,
    m.mechanism_class,
    m.update_rule,
    m.time_scale_ms
FROM entities e
JOIN mechanisms m ON e.entity_id = m.entity_id
WHERE e.entity_type_id = (SELECT type_id FROM entity_types WHERE type_name = 'mechanism')
  AND e.validation_status = 'validated'
ORDER BY e.confidence_score DESC;
```

### Pattern 2: Find Computational Mappings for an Entity

```sql
-- Get all architectural patterns for lateral inhibition
SELECT
    e.name as biological_entity,
    ap.pattern_name,
    ap.pattern_category,
    cm.mapping_type,
    cm.fidelity_score,
    cm.description,
    cm.mathematical_correspondence
FROM entities e
JOIN computational_mappings cm ON e.entity_id = cm.entity_id
JOIN architectural_patterns ap ON cm.pattern_id = ap.pattern_id
WHERE e.identifier = 'MECH_001'
ORDER BY cm.fidelity_score DESC;
```

### Pattern 3: Traverse Entity Hierarchy

```sql
-- Get all descendants of a process (recursive CTE)
WITH RECURSIVE descendants AS (
    -- Base case: start entity
    SELECT entity_id, name, 0 as depth
    FROM entities
    WHERE identifier = 'GO:0008150'

    UNION ALL

    -- Recursive case: find children
    SELECT e.entity_id, e.name, d.depth + 1
    FROM entities e
    JOIN entity_relationships er ON e.entity_id = er.target_entity_id
    JOIN descendants d ON er.source_entity_id = d.entity_id
    JOIN relationship_types rt ON er.relationship_type_id = rt.relationship_type_id
    WHERE rt.type_name IN ('parent_of', 'has_part')
)
SELECT * FROM descendants ORDER BY depth, name;
```

### Pattern 4: Find Entities with Specific Properties

```sql
-- Find all enzymes with Km < 0.1 mM and optimal pH between 6-8
SELECT
    e.name,
    enz.ec_number,
    enz.km_value,
    enz.optimal_ph
FROM entities e
JOIN enzymes enz ON e.entity_id = enz.entity_id
WHERE e.entity_type_id = (SELECT type_id FROM entity_types WHERE type_name = 'enzyme')
  AND enz.km_value < 0.1
  AND enz.optimal_ph BETWEEN 6.0 AND 8.0
ORDER BY enz.km_value;
```

### Pattern 5: Find Entities by Formula

```sql
-- Find all entities using Michaelis-Menten kinetics
SELECT
    e.name,
    e.description,
    f.latex_notation,
    ef.parameter_values
FROM entities e
JOIN entity_formulas ef ON e.entity_id = ef.entity_id
JOIN formulas f ON ef.formula_id = f.formula_id
WHERE f.name LIKE '%Michaelis-Menten%'
  AND ef.role = 'governing_equation';
```

### Pattern 6: Cross-Database Lookup

```sql
-- Find entity by UniProt ID and get all its cross-references
SELECT
    e.name,
    e.description,
    db.database_name,
    xr.external_id,
    xr.external_url
FROM cross_references xr
JOIN entities e ON xr.entity_id = e.entity_id
JOIN external_databases db ON xr.database_id = db.database_id
WHERE xr.external_id = 'P12345'  -- UniProt ID
  AND xr.database_id = (SELECT database_id FROM external_databases WHERE database_name = 'UniProt');
```

### Pattern 7: Find Similar Entities (by relationship)

```sql
-- Find entities similar to a given mechanism
SELECT
    e2.name as similar_entity,
    et.type_name,
    er.strength as similarity_score,
    er.context
FROM entities e1
JOIN entity_relationships er ON e1.entity_id = er.source_entity_id
JOIN entities e2 ON er.target_entity_id = e2.entity_id
JOIN entity_types et ON e2.entity_type_id = et.type_id
WHERE e1.identifier = 'MECH_001'
  AND er.relationship_type_id = (SELECT relationship_type_id FROM relationship_types WHERE type_name = 'similar_to')
ORDER BY er.strength DESC;
```

### Pattern 8: Full-Text Search

```sql
-- Search for entities mentioning "calcium" and "signaling"
SELECT
    e.entity_id,
    e.name,
    e.description,
    et.type_name
FROM entities_fts fts
JOIN entities e ON fts.entity_id = e.entity_id
JOIN entity_types et ON e.entity_type_id = et.type_id
WHERE entities_fts MATCH 'calcium AND signaling'
ORDER BY rank;
```

### Pattern 9: Aggregate Statistics

```sql
-- Count entities by type and validation status
SELECT
    et.type_name,
    e.validation_status,
    COUNT(*) as entity_count,
    AVG(e.confidence_score) as avg_confidence
FROM entities e
JOIN entity_types et ON e.entity_type_id = et.type_id
GROUP BY et.type_name, e.validation_status
ORDER BY et.type_name, e.validation_status;
```

### Pattern 10: Complex Multi-Join Query

```sql
-- Find top-tier computational primitives with high-confidence mappings,
-- formulas, and supporting publications
SELECT
    e.name,
    et.type_name,
    COUNT(DISTINCT cm.mapping_id) as mapping_count,
    COUNT(DISTINCT ef.formula_id) as formula_count,
    COUNT(DISTINCT ep.publication_id) as publication_count,
    AVG(cm.fidelity_score) as avg_fidelity,
    e.confidence_score
FROM entities e
JOIN entity_types et ON e.entity_type_id = et.type_id
LEFT JOIN computational_mappings cm ON e.entity_id = cm.entity_id
LEFT JOIN entity_formulas ef ON e.entity_id = ef.entity_id
LEFT JOIN entity_publications ep ON e.entity_id = ep.entity_id
WHERE et.type_category = 'top_tier'
  AND e.validation_status = 'validated'
  AND e.confidence_score > 0.8
GROUP BY e.entity_id, e.name, et.type_name, e.confidence_score
HAVING mapping_count > 0
ORDER BY e.confidence_score DESC, mapping_count DESC;
```

### Pattern 11: Find Architectural Patterns by Properties

```sql
-- Find all feedback mechanisms mapped to control flow patterns
SELECT
    e.name,
    m.mechanism_class,
    ap.pattern_name,
    ap.complexity_class,
    cm.fidelity_score
FROM mechanisms m
JOIN entities e ON m.entity_id = e.entity_id
JOIN computational_mappings cm ON e.entity_id = cm.entity_id
JOIN architectural_patterns ap ON cm.pattern_id = ap.pattern_id
WHERE m.mechanism_class LIKE '%feedback%'
  AND ap.pattern_category = 'control_flow'
  AND cm.validated = TRUE
ORDER BY cm.fidelity_score DESC;
```

### Pattern 12: Pathway Analysis

```sql
-- Find all pathways and their constituent molecules
SELECT
    e.name as pathway_name,
    p.pathway_category,
    p.input_molecules,
    p.output_molecules,
    p.intermediate_steps,
    COUNT(DISTINCT er.target_entity_id) as component_count
FROM pathways p
JOIN entities e ON p.entity_id = e.entity_id
LEFT JOIN entity_relationships er ON e.entity_id = er.source_entity_id
WHERE er.relationship_type_id = (SELECT relationship_type_id FROM relationship_types WHERE type_name = 'has_part')
GROUP BY e.entity_id, e.name, p.pathway_category, p.input_molecules, p.output_molecules, p.intermediate_steps
ORDER BY component_count DESC;
```

---

## Data Import Strategies

### Strategy 1: Batch Import from CSV/TSV

```python
import sqlite3
import csv

def import_entities_from_csv(csv_file, entity_type_id):
    conn = sqlite3.connect('bio_architecture.db')
    cursor = conn.cursor()

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Insert into entities table
            cursor.execute('''
                INSERT INTO entities (entity_type_id, identifier, name, description,
                                     confidence_score, source_database)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (entity_type_id, row['identifier'], row['name'], row['description'],
                  float(row.get('confidence', 0.8)), row.get('source', 'import')))

            entity_id = cursor.lastrowid

            # Insert into type-specific table (example: mechanisms)
            if entity_type_id == 1:  # mechanism
                cursor.execute('''
                    INSERT INTO mechanisms (mechanism_id, entity_id, mechanism_class, update_rule)
                    VALUES (?, ?, ?, ?)
                ''', (entity_id, entity_id, row['mechanism_class'], row['update_rule']))

    conn.commit()
    conn.close()
```

### Strategy 2: API Integration

```python
import requests

def import_from_uniprot(uniprot_id):
    # Fetch data from UniProt API
    url = f'https://www.uniprot.org/uniprot/{uniprot_id}.json'
    response = requests.get(url)
    data = response.json()

    # Extract relevant fields
    entity_data = {
        'identifier': uniprot_id,
        'name': data['protein']['recommendedName']['fullName']['value'],
        'description': data.get('comments', [{}])[0].get('text', [{}])[0].get('value', ''),
        'entity_type_id': 8,  # enzyme
        'source_database': 'UniProt'
    }

    # Insert into database
    cursor.execute('''
        INSERT INTO entities (entity_type_id, identifier, name, description, source_database)
        VALUES (?, ?, ?, ?, ?)
    ''', (entity_data['entity_type_id'], entity_data['identifier'],
          entity_data['name'], entity_data['description'], entity_data['source_database']))

    entity_id = cursor.lastrowid

    # Add cross-reference
    cursor.execute('''
        INSERT INTO cross_references (entity_id, database_id, external_id, external_url)
        VALUES (?, ?, ?, ?)
    ''', (entity_id, 1, uniprot_id, f'https://www.uniprot.org/uniprot/{uniprot_id}'))

    return entity_id
```

### Strategy 3: Database Dump Import

```sql
-- Import from another SQLite database
ATTACH DATABASE 'external_source.db' AS external;

INSERT INTO entities (entity_type_id, identifier, name, description, source_database)
SELECT type_id, ext_id, ext_name, ext_desc, 'external_source'
FROM external.entities_table
WHERE NOT EXISTS (
    SELECT 1 FROM entities WHERE identifier = ext_id
);

DETACH DATABASE external;
```

### Strategy 4: Incremental Sync with Deduplication

```python
def sync_with_deduplication(new_entities):
    """
    Import new entities, merging with existing ones based on identifier
    """
    for entity in new_entities:
        # Check if entity exists
        cursor.execute('''
            SELECT entity_id, confidence_score, version
            FROM entities
            WHERE identifier = ? AND entity_type_id = ?
        ''', (entity['identifier'], entity['entity_type_id']))

        existing = cursor.fetchone()

        if existing:
            entity_id, old_confidence, old_version = existing

            # Update if new data has higher confidence
            if entity['confidence_score'] > old_confidence:
                cursor.execute('''
                    UPDATE entities
                    SET name = ?, description = ?, confidence_score = ?,
                        updated_at = CURRENT_TIMESTAMP, version = ?
                    WHERE entity_id = ?
                ''', (entity['name'], entity['description'], entity['confidence_score'],
                      old_version + 1, entity_id))

                # Log the update
                cursor.execute('''
                    INSERT INTO curation_log (entity_id, action_type, reason)
                    VALUES (?, 'update', 'Sync with higher confidence data')
                ''', (entity_id,))
        else:
            # Insert new entity
            cursor.execute('''
                INSERT INTO entities (entity_type_id, identifier, name, description, confidence_score)
                VALUES (?, ?, ?, ?, ?)
            ''', (entity['entity_type_id'], entity['identifier'],
                  entity['name'], entity['description'], entity['confidence_score']))
```

---

## Performance Optimization

### Index Strategy

The schema includes comprehensive indexing:

1. **Primary Keys**: All tables (automatic)
2. **Foreign Keys**: All relationships (for join performance)
3. **Type Lookups**: `idx_entities_type`
4. **Identifier Lookups**: `idx_entities_identifier`
5. **Composite Indexes**: For common query patterns
   - `idx_composite_entity_type_status` for filtered type queries
   - `idx_composite_params_entity_type` for parameter searches
   - `idx_composite_mapping_validated` for computational mappings

### Query Optimization Tips

1. **Use EXPLAIN QUERY PLAN** to verify index usage:
```sql
EXPLAIN QUERY PLAN
SELECT * FROM entities WHERE entity_type_id = 1 AND validation_status = 'validated';
```

2. **Limit result sets** with pagination:
```sql
SELECT * FROM entities
WHERE entity_type_id = 1
ORDER BY confidence_score DESC
LIMIT 100 OFFSET 0;
```

3. **Use JOINs instead of subqueries** when possible
4. **Denormalize for read-heavy workloads** (use materialized views)
5. **Partition large tables** (for PostgreSQL)

### Caching Strategy

1. **Application-Level Cache**: Cache frequent queries (entity lookups by ID)
2. **Materialized Views**: Pre-compute expensive aggregations
3. **Read Replicas**: For high-volume read workloads (PostgreSQL)

### Scaling Considerations

#### For SQLite (< 10M entities):
- Works well for single-user or small team
- Consider PRAGMA optimizations:
```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = -64000;  -- 64MB
PRAGMA temp_store = MEMORY;
```

#### For PostgreSQL (> 10M entities):
- Better concurrent access
- Partitioning support
- Parallel query execution
- More sophisticated indexing (GiST, GIN for full-text)

**Migration to PostgreSQL**:
```sql
-- Convert SQLite schema to PostgreSQL
-- Replace INTEGER PRIMARY KEY with SERIAL
-- Replace REAL with DOUBLE PRECISION
-- Add proper CHECK constraints
-- Use tsvector for full-text search instead of FTS5
```

---

## Extension Points

### 1. Adding New Entity Types

```sql
-- Step 1: Add entity type
INSERT INTO entity_types (type_id, type_name, type_category, estimated_count, description)
VALUES (12, 'organelle', 'middle_tier', 100, 'Subcellular structures');

-- Step 2: Create type-specific table
CREATE TABLE organelles (
    organelle_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL UNIQUE,
    organelle_type VARCHAR(100),
    membrane_bound BOOLEAN,
    primary_function TEXT,
    volume_um3 REAL,
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

CREATE INDEX idx_organelles_type ON organelles(organelle_type);

-- Step 3: Insert entities
INSERT INTO entities (entity_id, entity_type_id, identifier, name, description)
VALUES (10001, 12, 'ORG_001', 'Mitochondrion', 'Powerhouse of the cell');

INSERT INTO organelles (organelle_id, entity_id, organelle_type, membrane_bound, primary_function)
VALUES (1, 10001, 'energy_production', TRUE, 'ATP synthesis via oxidative phosphorylation');
```

### 2. Adding New Relationship Types

```sql
INSERT INTO relationship_types (relationship_type_id, type_name, inverse_type_name,
                                is_hierarchical, is_symmetric, description)
VALUES (11, 'catalyzes', 'catalyzed_by', FALSE, FALSE,
        'Enzyme catalyzes reaction');

-- Use the new relationship
INSERT INTO entity_relationships (relationship_id, source_entity_id, target_entity_id,
                                 relationship_type_id, strength, confidence)
SELECT nextval('relationship_seq'), enz.entity_id, rxn.entity_id, 11, 1.0, 0.95
FROM entities enz
JOIN entities rxn ON rxn.identifier = 'RXN_001'
WHERE enz.identifier = 'EC:1.1.1.1';
```

### 3. Adding Custom Property Types

```sql
INSERT INTO property_definitions (property_id, property_name, data_type, unit, description)
VALUES (101, 'quantum_efficiency', 'real', 'dimensionless',
        'Quantum efficiency of photoreceptor');

-- Add property to entity
INSERT INTO entity_properties (property_instance_id, entity_id, property_id, value_real, confidence)
VALUES (5001, 1234, 101, 0.67, 0.90);
```

### 4. Custom Architectural Patterns

```sql
INSERT INTO architectural_patterns (pattern_id, pattern_name, pattern_category,
                                   formal_description, complexity_class)
VALUES (51, 'Leaky Integrate-and-Fire', 'neural_network',
        'Neuron model with capacitive integration and voltage reset',
        'O(1) per timestep');

-- Map to biological entity
INSERT INTO computational_mappings (mapping_id, entity_id, pattern_id, mapping_type,
                                   fidelity_score, description)
VALUES (1001, 2345, 51, 'approximates', 0.75,
        'Simplified model of biological neuron capturing essential dynamics');
```

### 5. Plugin System for Analysis

The schema supports external analysis tools via:

1. **Export Views**: Pre-defined views for common analyses
2. **JSON Properties**: Store complex structured data
3. **External Tool Integration**: Via cross_references table

Example plugin interface:
```python
class AnalysisPlugin:
    def analyze(self, entity_id):
        """Run analysis on entity and store results as JSON property"""
        # Fetch entity data
        entity = fetch_entity(entity_id)

        # Perform analysis
        results = self.run_analysis(entity)

        # Store results
        store_json_property(entity_id, 'analysis_results', results)
```

---

## Implementation Checklist

### Phase 1: Core Schema
- [ ] Create database file
- [ ] Execute schema SQL
- [ ] Verify all tables created
- [ ] Test basic CRUD operations
- [ ] Populate entity_types
- [ ] Populate relationship_types
- [ ] Populate external_databases

### Phase 2: Initial Data Import
- [ ] Import top-tier entities (mechanisms, processes, etc.)
- [ ] Import middle-tier entities (enzymes, receptors, etc.)
- [ ] Establish hierarchical relationships
- [ ] Add cross-references to external databases
- [ ] Import formulas
- [ ] Import publications

### Phase 3: Computational Mapping
- [ ] Define architectural patterns
- [ ] Create computational mappings
- [ ] Validate mappings
- [ ] Document correspondences

### Phase 4: Quality and Curation
- [ ] Add curator accounts
- [ ] Implement validation workflow
- [ ] Set up curation log
- [ ] Establish quality metrics
- [ ] Create review process

### Phase 5: Optimization
- [ ] Analyze query performance
- [ ] Add additional indexes as needed
- [ ] Create materialized views (if using PostgreSQL)
- [ ] Implement caching layer
- [ ] Set up monitoring

### Phase 6: Integration and API
- [ ] Build REST API
- [ ] Create query interface
- [ ] Implement export functionality
- [ ] Set up synchronization with external databases
- [ ] Document API endpoints

---

## Best Practices

### Data Entry
1. Always populate `identifier` with a unique, stable ID
2. Use consistent naming conventions
3. Include `source_database` for provenance
4. Set `confidence_score` based on evidence
5. Link to publications when available

### Relationship Management
1. Use appropriate relationship types (don't overuse `interacts_with`)
2. Set strength and confidence for weighted relationships
3. Document context for non-obvious relationships
4. Avoid circular dependencies in hierarchies

### Computational Mapping
1. Validate mappings with domain experts
2. Document mathematical correspondence clearly
3. Provide implementation examples
4. Rate fidelity honestly (avoid inflation)
5. Link to relevant publications

### Performance
1. Don't create indexes on every column (overhead)
2. Use batch inserts for large imports
3. Analyze query plans regularly
4. Monitor database size and growth
5. Archive deprecated entities (don't delete)

### Quality Control
1. Require validation for public-facing data
2. Use curation_log for all manual edits
3. Implement peer review for high-impact entities
4. Regular audits of cross-references
5. Monitor for duplicate entries

---

## Common Issues and Solutions

### Issue 1: Slow Hierarchical Queries

**Problem**: Recursive queries on deep hierarchies are slow.

**Solution**: Use materialized path or nested set model for read-heavy workloads:
```sql
-- Add path column to entities
ALTER TABLE entities ADD COLUMN hierarchy_path VARCHAR(500);

-- Update with materialized path (e.g., "/1/5/23/")
UPDATE entities SET hierarchy_path = compute_path(entity_id);

-- Query becomes simple string match
SELECT * FROM entities
WHERE hierarchy_path LIKE '/1/5/%';
```

### Issue 2: Property Query Performance

**Problem**: Querying EAV properties is slow.

**Solution**: Create indexed views for common properties:
```sql
CREATE INDEX idx_props_km ON entity_properties(property_id, value_real)
WHERE property_id = (SELECT property_id FROM property_definitions WHERE property_name = 'km_value');
```

### Issue 3: Full-Text Search Relevance

**Problem**: Full-text search returns too many irrelevant results.

**Solution**: Use BM25 ranking and filter by entity type:
```sql
SELECT e.*, bm25(entities_fts) as score
FROM entities_fts
JOIN entities e ON entities_fts.entity_id = e.entity_id
WHERE entities_fts MATCH 'calcium signaling'
  AND e.entity_type_id IN (1, 2, 3)  -- Only top-tier
ORDER BY score
LIMIT 50;
```

### Issue 4: Version Conflicts

**Problem**: Concurrent updates cause version conflicts.

**Solution**: Use optimistic locking:
```sql
UPDATE entities
SET description = ?, version = version + 1, updated_at = CURRENT_TIMESTAMP
WHERE entity_id = ? AND version = ?;

-- If rows affected = 0, conflict occurred
```

---

## Future Enhancements

1. **Graph Database Integration**: Use Neo4j for complex relationship queries
2. **Time-Series Data**: Add support for temporal dynamics (time-varying parameters)
3. **Spatial Data**: Store 3D structures (proteins, brain regions)
4. **Machine Learning Integration**: Auto-generate computational mappings
5. **Collaborative Features**: Real-time collaboration on curation
6. **API Gateway**: GraphQL interface for flexible queries
7. **Semantic Web**: RDF export for ontology integration
8. **Visualization**: Interactive network graphs and pathway diagrams

---

This documentation provides a complete guide to implementing and using the biological architectural primitives database. The schema is production-ready and can scale from thousands to millions of entities with appropriate database selection (SQLite → PostgreSQL) and optimization.
