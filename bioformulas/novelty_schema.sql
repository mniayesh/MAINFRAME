-- NOVELTY Database Schema
-- Stores novel biological → computational architecture mappings
-- Extracted from biological databases with fidelity scores

PRAGMA foreign_keys = ON;

-- ============================================
-- BIOLOGICAL ENTITIES
-- ============================================

CREATE TABLE IF NOT EXISTS biological_entities (
    entity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    identifier TEXT UNIQUE NOT NULL,      -- e.g., COGAT:trm_xxx, ABA:123, hsa01100
    name TEXT NOT NULL,
    description TEXT,
    entity_type TEXT NOT NULL,            -- computation, network_structure, pathway, enzyme
    source_database TEXT NOT NULL,        -- CognitiveAtlas, AllenBrain, KEGG, InterPro, etc.
    confidence_score REAL DEFAULT 0.85,
    evidence_strength TEXT,               -- experimental, computational, curated
    extraction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT                         -- JSON for additional fields
);

-- ============================================
-- COMPUTATIONAL PRIMITIVES
-- ============================================

CREATE TABLE IF NOT EXISTS computational_primitives (
    primitive_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,            -- e.g., "Interrupt Handler / Process Scheduler"
    category TEXT NOT NULL,               -- os_primitive, architecture_pattern, system_pattern
    description TEXT,
    application_domains TEXT,             -- e.g., "OS kernel design, real-time systems"
    related_technologies TEXT             -- e.g., "Linux scheduler, RTOS"
);

-- ============================================
-- BIOLOGICAL → COMPUTATIONAL MAPPINGS
-- ============================================

CREATE TABLE IF NOT EXISTS bio_comp_mappings (
    mapping_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id INTEGER REFERENCES biological_entities(entity_id) ON DELETE CASCADE,
    primitive_id INTEGER REFERENCES computational_primitives(primitive_id) ON DELETE CASCADE,
    fidelity_score REAL NOT NULL,        -- 0.0 to 1.0
    mapping_type TEXT NOT NULL,          -- cognitive_to_os, structure_to_arch, pathway_to_system
    description TEXT,                     -- Explanation of the mapping
    examples TEXT,                        -- Specific examples (JSON array)
    discovered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified BOOLEAN DEFAULT FALSE,
    UNIQUE(entity_id, primitive_id)
);

-- ============================================
-- ARCHITECTURAL PATTERNS
-- ============================================

CREATE TABLE IF NOT EXISTS architecture_patterns (
    pattern_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,           -- e.g., "Hierarchical Processing Pipeline"
    category TEXT,                       -- network, memory, processing, control
    description TEXT,
    biological_examples INTEGER DEFAULT 0,
    computational_examples TEXT,         -- JSON array of systems using this pattern
    scalability TEXT,                    -- how pattern scales
    tradeoffs TEXT                       -- performance vs accuracy, etc.
);

-- Junction table: patterns <-> biological entities
CREATE TABLE IF NOT EXISTS entity_patterns (
    entity_id INTEGER REFERENCES biological_entities(entity_id) ON DELETE CASCADE,
    pattern_id INTEGER REFERENCES architecture_patterns(pattern_id) ON DELETE CASCADE,
    PRIMARY KEY (entity_id, pattern_id)
);

-- ============================================
-- KEY INSIGHTS
-- ============================================

CREATE TABLE IF NOT EXISTS insights (
    insight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT,                       -- abstraction, memory, scheduling, error_correction, etc.
    description TEXT,
    evidence TEXT,                       -- Supporting evidence
    implications TEXT,                   -- What this enables
    related_mappings TEXT,               -- JSON array of mapping_ids
    impact_score REAL DEFAULT 0.5,       -- 0.0 to 1.0
    discovered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- EXTRACTION STATISTICS
-- ============================================

CREATE TABLE IF NOT EXISTS extraction_stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    database_name TEXT NOT NULL,
    entities_extracted INTEGER DEFAULT 0,
    extraction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success_rate REAL,                   -- 0.0 to 1.0
    avg_confidence REAL,
    validation_failures INTEGER DEFAULT 0,
    duration_seconds REAL,
    notes TEXT
);

-- ============================================
-- INDEXES
-- ============================================

CREATE INDEX IF NOT EXISTS idx_entities_type ON biological_entities(entity_type);
CREATE INDEX IF NOT EXISTS idx_entities_source ON biological_entities(source_database);
CREATE INDEX IF NOT EXISTS idx_entities_identifier ON biological_entities(identifier);
CREATE INDEX IF NOT EXISTS idx_mappings_fidelity ON bio_comp_mappings(fidelity_score);
CREATE INDEX IF NOT EXISTS idx_mappings_type ON bio_comp_mappings(mapping_type);
CREATE INDEX IF NOT EXISTS idx_patterns_category ON architecture_patterns(category);

-- ============================================
-- FULL-TEXT SEARCH
-- ============================================

CREATE VIRTUAL TABLE IF NOT EXISTS entities_fts USING fts5(
    name, description, content=biological_entities, content_rowid=entity_id
);

CREATE VIRTUAL TABLE IF NOT EXISTS insights_fts USING fts5(
    title, description, evidence, content=insights, content_rowid=insight_id
);

-- ============================================
-- VIEWS
-- ============================================

CREATE VIEW IF NOT EXISTS v_high_fidelity_mappings AS
SELECT
    be.name as biological_entity,
    be.entity_type,
    be.source_database,
    cp.name as computational_primitive,
    bcm.fidelity_score,
    bcm.description,
    bcm.mapping_type
FROM bio_comp_mappings bcm
JOIN biological_entities be ON bcm.entity_id = be.entity_id
JOIN computational_primitives cp ON bcm.primitive_id = cp.primitive_id
WHERE bcm.fidelity_score >= 0.90
ORDER BY bcm.fidelity_score DESC;

CREATE VIEW IF NOT EXISTS v_entities_by_database AS
SELECT
    source_database,
    entity_type,
    COUNT(*) as count,
    AVG(confidence_score) as avg_confidence
FROM biological_entities
GROUP BY source_database, entity_type;

CREATE VIEW IF NOT EXISTS v_pattern_implementations AS
SELECT
    ap.name as pattern_name,
    ap.category,
    COUNT(ep.entity_id) as biological_implementations,
    GROUP_CONCAT(be.name, '; ') as example_entities
FROM architecture_patterns ap
LEFT JOIN entity_patterns ep ON ap.pattern_id = ep.pattern_id
LEFT JOIN biological_entities be ON ep.entity_id = be.entity_id
GROUP BY ap.pattern_id;

CREATE VIEW IF NOT EXISTS v_mapping_statistics AS
SELECT
    mapping_type,
    COUNT(*) as total_mappings,
    AVG(fidelity_score) as avg_fidelity,
    MIN(fidelity_score) as min_fidelity,
    MAX(fidelity_score) as max_fidelity,
    COUNT(CASE WHEN fidelity_score >= 0.90 THEN 1 END) as high_fidelity_count
FROM bio_comp_mappings
GROUP BY mapping_type;
