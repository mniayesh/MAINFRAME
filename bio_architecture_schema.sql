-- ============================================================================
-- BIOLOGICAL ARCHITECTURAL PRIMITIVES DATABASE SCHEMA
-- Version: 1.0.0
-- Description: Comprehensive schema for storing biological mechanisms,
--              processes, and their computational mappings
-- ============================================================================

-- ============================================================================
-- SCHEMA VERSIONING & METADATA
-- ============================================================================

CREATE TABLE schema_versions (
    version_id INTEGER PRIMARY KEY,
    version_number VARCHAR(20) NOT NULL UNIQUE,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    migration_script TEXT
);

-- Initial version entry
INSERT INTO schema_versions (version_id, version_number, description)
VALUES (1, '1.0.0', 'Initial schema for biological architectural primitives');

-- ============================================================================
-- CORE ENTITY SYSTEM
-- ============================================================================

-- Entity types enumeration
CREATE TABLE entity_types (
    type_id INTEGER PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL UNIQUE,
    type_category VARCHAR(20) NOT NULL CHECK (type_category IN ('top_tier', 'middle_tier')),
    estimated_count INTEGER,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO entity_types (type_id, type_name, type_category, estimated_count, description) VALUES
(1, 'mechanism', 'top_tier', 300, 'Update rules and computational primitives'),
(2, 'process', 'top_tier', 2500, 'Biological processes and their dynamics'),
(3, 'circuit_motif', 'top_tier', 100, 'Neural circuit patterns'),
(4, 'network_structure', 'top_tier', 250, 'Brain regions and connections'),
(5, 'representation', 'top_tier', 50, 'Encoding formats'),
(6, 'computation', 'top_tier', 100, 'Universal operators'),
(7, 'constraint', 'top_tier', 100, 'Optimization limits'),
(8, 'enzyme', 'middle_tier', 6000, 'Catalytic mechanisms'),
(9, 'receptor_channel', 'middle_tier', 3000, 'Gating mechanisms'),
(10, 'cell_type', 'middle_tier', 3000, 'Architectural templates'),
(11, 'pathway', 'middle_tier', 500, 'Flow networks');

-- Core entities table (unified storage for all entity types)
CREATE TABLE entities (
    entity_id INTEGER PRIMARY KEY,
    entity_type_id INTEGER NOT NULL,
    identifier VARCHAR(100) NOT NULL,  -- Unique identifier (e.g., EC number, GO ID)
    name VARCHAR(500) NOT NULL,
    common_name VARCHAR(500),
    description TEXT,
    mathematical_formulation TEXT,     -- Core equation/rule if applicable
    complexity_level VARCHAR(20) CHECK (complexity_level IN ('simple', 'moderate', 'complex')),

    -- Metadata
    confidence_score REAL CHECK (confidence_score >= 0 AND confidence_score <= 1),
    evidence_strength VARCHAR(20) CHECK (evidence_strength IN ('experimental', 'computational', 'inferred', 'predicted')),
    validation_status VARCHAR(20) DEFAULT 'draft' CHECK (validation_status IN ('draft', 'reviewed', 'validated', 'deprecated')),

    -- Timestamps and versioning
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version INTEGER DEFAULT 1,

    -- Provenance
    source_database VARCHAR(100),
    curator VARCHAR(200),

    FOREIGN KEY (entity_type_id) REFERENCES entity_types(type_id),
    UNIQUE (entity_type_id, identifier)
);

CREATE INDEX idx_entities_type ON entities(entity_type_id);
CREATE INDEX idx_entities_identifier ON entities(identifier);
CREATE INDEX idx_entities_name ON entities(name);
CREATE INDEX idx_entities_validation ON entities(validation_status);

-- ============================================================================
-- TYPE-SPECIFIC EXTENSION TABLES
-- ============================================================================

-- Mechanisms: Update rules and computational primitives
CREATE TABLE mechanisms (
    mechanism_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL UNIQUE,
    mechanism_class VARCHAR(100),      -- e.g., 'feedback', 'feedforward', 'lateral_inhibition'
    update_rule TEXT,                   -- Mathematical update rule
    time_scale_ms REAL,                 -- Characteristic timescale
    computational_complexity VARCHAR(50), -- O(n), O(n^2), etc.
    reversibility BOOLEAN,
    energy_requirement VARCHAR(50),     -- 'ATP-dependent', 'passive', etc.
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

CREATE INDEX idx_mechanisms_class ON mechanisms(mechanism_class);

-- Processes: Biological processes and dynamics
CREATE TABLE processes (
    process_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL UNIQUE,
    process_category VARCHAR(100),      -- 'metabolic', 'signaling', 'transport', etc.
    temporal_dynamics VARCHAR(50),      -- 'transient', 'sustained', 'oscillatory', 'bistable'
    spatial_scale VARCHAR(50),          -- 'molecular', 'cellular', 'tissue', 'organ', 'system'
    rate_equation TEXT,                 -- Differential equation or rate law
    equilibrium_state TEXT,             -- Description of steady state
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

CREATE INDEX idx_processes_category ON processes(process_category);
CREATE INDEX idx_processes_scale ON processes(spatial_scale);

-- Circuit motifs: Neural circuit patterns
CREATE TABLE circuit_motifs (
    motif_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL UNIQUE,
    motif_topology VARCHAR(100),        -- 'feedforward', 'recurrent', 'winner-take-all', etc.
    node_count INTEGER,                 -- Number of nodes in motif
    connection_pattern TEXT,            -- Graph representation
    transfer_function TEXT,             -- Input-output transformation
    stability_analysis TEXT,            -- Stability properties
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

CREATE INDEX idx_motifs_topology ON circuit_motifs(motif_topology);

-- Network structures: Brain regions and connections
CREATE TABLE network_structures (
    structure_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL UNIQUE,
    anatomical_location VARCHAR(200),
    network_topology VARCHAR(100),      -- 'hierarchical', 'small-world', 'scale-free', etc.
    node_count INTEGER,
    edge_count INTEGER,
    modularity_coefficient REAL,
    clustering_coefficient REAL,
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

CREATE INDEX idx_structures_location ON network_structures(anatomical_location);

-- Representations: Encoding formats
CREATE TABLE representations (
    representation_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL UNIQUE,
    encoding_type VARCHAR(100),         -- 'rate', 'temporal', 'population', 'sparse', etc.
    dimensionality INTEGER,
    information_capacity_bits REAL,
    noise_tolerance VARCHAR(50),
    decoding_method TEXT,
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

CREATE INDEX idx_representations_encoding ON representations(encoding_type);

-- Computations: Universal operators
CREATE TABLE computations (
    computation_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL UNIQUE,
    operation_type VARCHAR(100),        -- 'integration', 'differentiation', 'normalization', etc.
    input_dimensions INTEGER,
    output_dimensions INTEGER,
    computational_model TEXT,           -- Description or pseudocode
    biological_implementation TEXT,     -- How biology implements this
    universality_class VARCHAR(100),    -- Computational class
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

CREATE INDEX idx_computations_operation ON computations(operation_type);

-- Constraints: Optimization limits
CREATE TABLE constraints (
    constraint_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL UNIQUE,
    constraint_type VARCHAR(100),       -- 'metabolic', 'physical', 'information_theoretic', etc.
    constraint_equation TEXT,
    lower_bound REAL,
    upper_bound REAL,
    units VARCHAR(50),
    violation_consequence TEXT,
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

CREATE INDEX idx_constraints_type ON constraints(constraint_type);

-- Enzymes: Catalytic mechanisms
CREATE TABLE enzymes (
    enzyme_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL UNIQUE,
    ec_number VARCHAR(20),              -- Enzyme Commission number
    catalytic_mechanism VARCHAR(200),
    substrate_specificity TEXT,
    km_value REAL,                      -- Michaelis constant
    kcat_value REAL,                    -- Turnover number
    optimal_ph REAL,
    optimal_temperature_c REAL,
    cofactor_requirements TEXT,
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

CREATE INDEX idx_enzymes_ec ON enzymes(ec_number);

-- Receptors and channels: Gating mechanisms
CREATE TABLE receptors_channels (
    receptor_channel_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL UNIQUE,
    receptor_type VARCHAR(100),         -- 'GPCR', 'ion_channel', 'nuclear_receptor', etc.
    gating_mechanism VARCHAR(200),
    selectivity TEXT,                   -- Ion selectivity or ligand binding
    activation_threshold REAL,
    inactivation_kinetics TEXT,
    conductance_pS REAL,                -- Conductance in picosiemens
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

CREATE INDEX idx_receptors_type ON receptors_channels(receptor_type);

-- Cell types: Architectural templates
CREATE TABLE cell_types (
    cell_type_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL UNIQUE,
    tissue_origin VARCHAR(200),
    morphology_class VARCHAR(100),      -- 'pyramidal', 'stellate', 'granule', etc.
    electrophysiological_properties TEXT,
    marker_genes TEXT,                  -- Comma-separated list
    connectivity_pattern TEXT,
    functional_role TEXT,
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

CREATE INDEX idx_cell_types_tissue ON cell_types(tissue_origin);
CREATE INDEX idx_cell_types_morphology ON cell_types(morphology_class);

-- Pathways: Flow networks
CREATE TABLE pathways (
    pathway_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL UNIQUE,
    pathway_category VARCHAR(100),      -- 'metabolic', 'signaling', 'regulatory', etc.
    input_molecules TEXT,
    output_molecules TEXT,
    intermediate_steps INTEGER,
    flux_rate REAL,
    regulation_type VARCHAR(50),        -- 'feedback', 'feedforward', 'allosteric', etc.
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE
);

CREATE INDEX idx_pathways_category ON pathways(pathway_category);

-- ============================================================================
-- RELATIONSHIP SYSTEM
-- ============================================================================

-- Relationship types
CREATE TABLE relationship_types (
    relationship_type_id INTEGER PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL UNIQUE,
    inverse_type_name VARCHAR(50),      -- For bidirectional relationships
    is_hierarchical BOOLEAN DEFAULT FALSE,
    is_symmetric BOOLEAN DEFAULT FALSE,
    description TEXT
);

INSERT INTO relationship_types (relationship_type_id, type_name, inverse_type_name, is_hierarchical, is_symmetric, description) VALUES
(1, 'parent_of', 'child_of', TRUE, FALSE, 'Hierarchical parent-child relationship'),
(2, 'part_of', 'has_part', TRUE, FALSE, 'Component relationship'),
(3, 'is_a', 'generalizes', TRUE, FALSE, 'Type hierarchy (subclass relationship)'),
(4, 'regulates', 'regulated_by', FALSE, FALSE, 'Regulatory interaction'),
(5, 'inhibits', 'inhibited_by', FALSE, FALSE, 'Inhibitory interaction'),
(6, 'activates', 'activated_by', FALSE, FALSE, 'Activation interaction'),
(7, 'interacts_with', 'interacts_with', FALSE, TRUE, 'General interaction'),
(8, 'precedes', 'follows', FALSE, FALSE, 'Temporal ordering'),
(9, 'located_in', 'contains', FALSE, FALSE, 'Spatial containment'),
(10, 'similar_to', 'similar_to', FALSE, TRUE, 'Similarity relationship');

-- Entity relationships
CREATE TABLE entity_relationships (
    relationship_id INTEGER PRIMARY KEY,
    source_entity_id INTEGER NOT NULL,
    target_entity_id INTEGER NOT NULL,
    relationship_type_id INTEGER NOT NULL,

    -- Quantitative properties of relationship
    strength REAL CHECK (strength >= 0 AND strength <= 1),
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),

    -- Context
    context TEXT,                       -- Under what conditions this relationship holds
    evidence TEXT,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_database VARCHAR(100),

    FOREIGN KEY (source_entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE,
    FOREIGN KEY (target_entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE,
    FOREIGN KEY (relationship_type_id) REFERENCES relationship_types(relationship_type_id),

    -- Prevent self-loops in hierarchical relationships
    CHECK (
        (relationship_type_id NOT IN (SELECT relationship_type_id FROM relationship_types WHERE is_hierarchical = TRUE))
        OR (source_entity_id != target_entity_id)
    )
);

CREATE INDEX idx_relationships_source ON entity_relationships(source_entity_id);
CREATE INDEX idx_relationships_target ON entity_relationships(target_entity_id);
CREATE INDEX idx_relationships_type ON entity_relationships(relationship_type_id);
CREATE INDEX idx_relationships_source_type ON entity_relationships(source_entity_id, relationship_type_id);

-- ============================================================================
-- FLEXIBLE PROPERTY SYSTEM (EAV Pattern)
-- ============================================================================

-- Property definitions
CREATE TABLE property_definitions (
    property_id INTEGER PRIMARY KEY,
    property_name VARCHAR(100) NOT NULL UNIQUE,
    data_type VARCHAR(20) NOT NULL CHECK (data_type IN ('string', 'integer', 'real', 'boolean', 'text', 'json')),
    unit VARCHAR(50),                   -- For quantitative properties
    description TEXT,
    applicable_entity_types TEXT,       -- Comma-separated type IDs or 'all'
    validation_rule TEXT                -- Regular expression or constraint
);

-- Entity properties (flexible key-value storage)
CREATE TABLE entity_properties (
    property_instance_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL,
    property_id INTEGER NOT NULL,

    -- Value storage (only one should be populated)
    value_string VARCHAR(500),
    value_integer INTEGER,
    value_real REAL,
    value_boolean BOOLEAN,
    value_text TEXT,
    value_json TEXT,                    -- For complex structured data

    -- Metadata
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    source VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES property_definitions(property_id),

    UNIQUE (entity_id, property_id)
);

CREATE INDEX idx_properties_entity ON entity_properties(entity_id);
CREATE INDEX idx_properties_property ON entity_properties(property_id);

-- ============================================================================
-- QUANTITATIVE PARAMETERS
-- ============================================================================

-- Parameter types
CREATE TABLE parameter_types (
    parameter_type_id INTEGER PRIMARY KEY,
    parameter_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    unit VARCHAR(50),
    typical_range_min REAL,
    typical_range_max REAL,
    measurement_method TEXT
);

INSERT INTO parameter_types (parameter_type_id, parameter_name, description, unit) VALUES
(1, 'rate_constant', 'Kinetic rate constant', 's^-1'),
(2, 'binding_affinity', 'Binding affinity (Kd)', 'M'),
(3, 'time_constant', 'Characteristic time constant', 'ms'),
(4, 'energy', 'Free energy change', 'kJ/mol'),
(5, 'voltage', 'Membrane potential', 'mV'),
(6, 'current', 'Ionic current', 'pA'),
(7, 'concentration', 'Molecular concentration', 'M'),
(8, 'flux', 'Metabolic flux', 'mmol/s'),
(9, 'distance', 'Spatial distance', 'um'),
(10, 'frequency', 'Oscillation frequency', 'Hz');

-- Parameters table
CREATE TABLE parameters (
    parameter_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL,
    parameter_type_id INTEGER NOT NULL,

    -- Value with uncertainty
    value REAL NOT NULL,
    uncertainty REAL,                   -- Standard deviation or error
    value_min REAL,                     -- Range
    value_max REAL,

    -- Conditions under which parameter was measured
    temperature_c REAL,
    ph REAL,
    experimental_conditions TEXT,

    -- Metadata
    measurement_method VARCHAR(200),
    organism VARCHAR(200),
    tissue_type VARCHAR(200),

    -- Provenance
    source VARCHAR(200),
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE,
    FOREIGN KEY (parameter_type_id) REFERENCES parameter_types(parameter_type_id)
);

CREATE INDEX idx_parameters_entity ON parameters(entity_id);
CREATE INDEX idx_parameters_type ON parameters(parameter_type_id);

-- ============================================================================
-- FORMULAS AND EQUATIONS
-- ============================================================================

-- Formula categories
CREATE TABLE formula_categories (
    category_id INTEGER PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

INSERT INTO formula_categories (category_id, category_name, description) VALUES
(1, 'kinetics', 'Kinetic rate equations'),
(2, 'dynamics', 'Dynamical systems equations'),
(3, 'thermodynamics', 'Thermodynamic relations'),
(4, 'electrophysiology', 'Electrical properties and equations'),
(5, 'population_dynamics', 'Population-level dynamics'),
(6, 'information_theory', 'Information-theoretic measures'),
(7, 'optimization', 'Optimization objectives and constraints');

-- Formulas table
CREATE TABLE formulas (
    formula_id INTEGER PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category_id INTEGER,

    -- Formula representation
    latex_notation TEXT NOT NULL,       -- LaTeX format for rendering
    python_code TEXT,                   -- Python implementation
    symbolic_form TEXT,                 -- SymPy or similar

    -- Description
    description TEXT,
    assumptions TEXT,                   -- Under what assumptions formula holds

    -- Variables
    variables_json TEXT,                -- JSON array of {name, symbol, unit, description}
    parameters_json TEXT,               -- JSON array of parameters

    -- Classification
    formula_type VARCHAR(50),           -- 'differential', 'algebraic', 'integral', etc.
    dimensionality VARCHAR(50),         -- 'scalar', 'vector', 'matrix', 'tensor'

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    validated BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (category_id) REFERENCES formula_categories(category_id)
);

CREATE INDEX idx_formulas_category ON formulas(category_id);
CREATE INDEX idx_formulas_name ON formulas(name);

-- Link entities to formulas
CREATE TABLE entity_formulas (
    entity_formula_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL,
    formula_id INTEGER NOT NULL,

    -- How this formula applies to this entity
    role VARCHAR(100),                  -- 'governing_equation', 'constraint', 'objective', etc.
    parameter_values TEXT,              -- JSON of parameter values for this entity

    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE,
    FOREIGN KEY (formula_id) REFERENCES formulas(formula_id) ON DELETE CASCADE,

    UNIQUE (entity_id, formula_id, role)
);

CREATE INDEX idx_entity_formulas_entity ON entity_formulas(entity_id);
CREATE INDEX idx_entity_formulas_formula ON entity_formulas(formula_id);

-- ============================================================================
-- COMPUTATIONAL MAPPING SYSTEM
-- ============================================================================

-- Architectural pattern types
CREATE TABLE architectural_patterns (
    pattern_id INTEGER PRIMARY KEY,
    pattern_name VARCHAR(100) NOT NULL UNIQUE,
    pattern_category VARCHAR(50),       -- 'control_flow', 'data_structure', 'algorithm', etc.
    formal_description TEXT,
    pseudocode TEXT,
    complexity_class VARCHAR(50),
    properties_json TEXT                -- JSON of key properties
);

-- Map biological entities to computational/architectural patterns
CREATE TABLE computational_mappings (
    mapping_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL,
    pattern_id INTEGER NOT NULL,

    -- Mapping details
    mapping_type VARCHAR(50),           -- 'isomorphic', 'analogous', 'approximates', etc.
    fidelity_score REAL CHECK (fidelity_score >= 0 AND fidelity_score <= 1),

    -- Mapping description
    description TEXT,
    mathematical_correspondence TEXT,   -- How biological math maps to computational

    -- Implementation
    implementation_notes TEXT,
    code_example TEXT,                  -- Example implementation

    -- Abstraction level
    abstraction_level VARCHAR(50),      -- 'molecular', 'cellular', 'circuit', 'system'

    -- Validation
    validated BOOLEAN DEFAULT FALSE,
    validation_method TEXT,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(200),

    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE,
    FOREIGN KEY (pattern_id) REFERENCES architectural_patterns(pattern_id),

    UNIQUE (entity_id, pattern_id)
);

CREATE INDEX idx_mappings_entity ON computational_mappings(entity_id);
CREATE INDEX idx_mappings_pattern ON computational_mappings(pattern_id);
CREATE INDEX idx_mappings_type ON computational_mappings(mapping_type);

-- ============================================================================
-- CROSS-REFERENCE SYSTEM
-- ============================================================================

-- External database types
CREATE TABLE external_databases (
    database_id INTEGER PRIMARY KEY,
    database_name VARCHAR(100) NOT NULL UNIQUE,
    database_url VARCHAR(500),
    api_endpoint VARCHAR(500),
    description TEXT,
    last_sync TIMESTAMP
);

INSERT INTO external_databases (database_id, database_name, database_url, description) VALUES
(1, 'UniProt', 'https://www.uniprot.org/', 'Protein sequence and functional information'),
(2, 'PDB', 'https://www.rcsb.org/', 'Protein Data Bank - 3D structures'),
(3, 'GO', 'http://geneontology.org/', 'Gene Ontology'),
(4, 'KEGG', 'https://www.kegg.jp/', 'Kyoto Encyclopedia of Genes and Genomes'),
(5, 'Reactome', 'https://reactome.org/', 'Pathway database'),
(6, 'ChEBI', 'https://www.ebi.ac.uk/chebi/', 'Chemical Entities of Biological Interest'),
(7, 'BRENDA', 'https://www.brenda-enzymes.org/', 'Enzyme information'),
(8, 'NeuroMorpho', 'http://neuromorpho.org/', 'Neuronal morphology'),
(9, 'Allen Brain Atlas', 'https://brain-map.org/', 'Brain anatomy and gene expression'),
(10, 'ModelDB', 'https://modeldb.science/', 'Computational neuroscience models'),
(11, 'BioModels', 'https://www.ebi.ac.uk/biomodels/', 'Systems biology models'),
(12, 'NCBI Gene', 'https://www.ncbi.nlm.nih.gov/gene/', 'Gene database'),
(13, 'Pfam', 'https://pfam.xfam.org/', 'Protein families'),
(14, 'InterPro', 'https://www.ebi.ac.uk/interpro/', 'Protein sequence analysis'),
(15, 'STRING', 'https://string-db.org/', 'Protein-protein interaction networks');

-- Cross-references to external databases
CREATE TABLE cross_references (
    xref_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL,
    database_id INTEGER NOT NULL,

    -- External identifier
    external_id VARCHAR(200) NOT NULL,
    external_url VARCHAR(500),          -- Direct link to resource

    -- Metadata
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    mapping_method VARCHAR(100),        -- How the mapping was established
    last_verified TIMESTAMP,

    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE,
    FOREIGN KEY (database_id) REFERENCES external_databases(database_id),

    UNIQUE (entity_id, database_id, external_id)
);

CREATE INDEX idx_xrefs_entity ON cross_references(entity_id);
CREATE INDEX idx_xrefs_database ON cross_references(database_id);
CREATE INDEX idx_xrefs_external_id ON cross_references(external_id);

-- ============================================================================
-- LITERATURE REFERENCES
-- ============================================================================

-- Publications
CREATE TABLE publications (
    publication_id INTEGER PRIMARY KEY,

    -- Identifiers
    pmid VARCHAR(20),                   -- PubMed ID
    doi VARCHAR(200),
    pmcid VARCHAR(20),                  -- PubMed Central ID

    -- Citation details
    title TEXT NOT NULL,
    authors TEXT,
    journal VARCHAR(500),
    year INTEGER,
    volume VARCHAR(20),
    pages VARCHAR(50),

    -- Content
    abstract TEXT,
    keywords TEXT,

    -- Links
    url VARCHAR(500),
    pdf_url VARCHAR(500),

    -- Metadata
    citation_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (pmid),
    UNIQUE (doi)
);

CREATE INDEX idx_publications_pmid ON publications(pmid);
CREATE INDEX idx_publications_doi ON publications(doi);
CREATE INDEX idx_publications_year ON publications(year);

-- Link entities to publications
CREATE TABLE entity_publications (
    entity_publication_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL,
    publication_id INTEGER NOT NULL,

    -- Relationship details
    evidence_type VARCHAR(50),          -- 'primary', 'supporting', 'review', etc.
    relevance_score REAL CHECK (relevance_score >= 0 AND relevance_score <= 1),
    excerpt TEXT,                       -- Relevant quote from publication

    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE,
    FOREIGN KEY (publication_id) REFERENCES publications(publication_id) ON DELETE CASCADE,

    UNIQUE (entity_id, publication_id)
);

CREATE INDEX idx_entity_pubs_entity ON entity_publications(entity_id);
CREATE INDEX idx_entity_pubs_publication ON entity_publications(publication_id);

-- ============================================================================
-- ANNOTATION AND CURATION
-- ============================================================================

-- Curator information
CREATE TABLE curators (
    curator_id INTEGER PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(200),
    institution VARCHAR(300),
    orcid VARCHAR(20),
    expertise_areas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Curation activities (audit trail)
CREATE TABLE curation_log (
    log_id INTEGER PRIMARY KEY,
    entity_id INTEGER,
    curator_id INTEGER,

    -- Action details
    action_type VARCHAR(50),            -- 'create', 'update', 'validate', 'deprecate', etc.
    field_changed VARCHAR(100),
    old_value TEXT,
    new_value TEXT,

    -- Rationale
    reason TEXT,

    -- Timestamp
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE SET NULL,
    FOREIGN KEY (curator_id) REFERENCES curators(curator_id)
);

CREATE INDEX idx_curation_entity ON curation_log(entity_id);
CREATE INDEX idx_curation_curator ON curation_log(curator_id);
CREATE INDEX idx_curation_timestamp ON curation_log(performed_at);

-- Comments and notes
CREATE TABLE entity_notes (
    note_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL,
    curator_id INTEGER,

    -- Note content
    note_type VARCHAR(50),              -- 'general', 'issue', 'todo', 'question', etc.
    content TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'open',  -- 'open', 'resolved', 'wontfix'

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,

    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE,
    FOREIGN KEY (curator_id) REFERENCES curators(curator_id)
);

CREATE INDEX idx_notes_entity ON entity_notes(entity_id);
CREATE INDEX idx_notes_status ON entity_notes(status);

-- ============================================================================
-- TAXONOMY AND SPECIES SPECIFICITY
-- ============================================================================

-- Organisms/species
CREATE TABLE organisms (
    organism_id INTEGER PRIMARY KEY,
    scientific_name VARCHAR(200) NOT NULL UNIQUE,
    common_name VARCHAR(200),
    taxonomy_id INTEGER,                -- NCBI Taxonomy ID
    kingdom VARCHAR(50),
    phylum VARCHAR(50),
    class VARCHAR(50),
    order_name VARCHAR(50),             -- 'order' is SQL keyword
    family VARCHAR(50),
    genus VARCHAR(50),
    species VARCHAR(50)
);

CREATE INDEX idx_organisms_taxonomy ON organisms(taxonomy_id);

-- Entity-organism associations
CREATE TABLE entity_organisms (
    entity_organism_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL,
    organism_id INTEGER NOT NULL,

    -- Conservation
    is_conserved BOOLEAN,
    conservation_score REAL CHECK (conservation_score >= 0 AND conservation_score <= 1),

    -- Specificity
    specificity VARCHAR(50),            -- 'universal', 'conserved', 'species_specific', 'variant'

    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE,
    FOREIGN KEY (organism_id) REFERENCES organisms(organism_id),

    UNIQUE (entity_id, organism_id)
);

CREATE INDEX idx_entity_organisms_entity ON entity_organisms(entity_id);
CREATE INDEX idx_entity_organisms_organism ON entity_organisms(organism_id);

-- ============================================================================
-- SEARCH AND DISCOVERY
-- ============================================================================

-- Tags for flexible categorization
CREATE TABLE tags (
    tag_id INTEGER PRIMARY KEY,
    tag_name VARCHAR(100) NOT NULL UNIQUE,
    tag_category VARCHAR(50),           -- 'method', 'application', 'domain', etc.
    description TEXT
);

CREATE TABLE entity_tags (
    entity_tag_id INTEGER PRIMARY KEY,
    entity_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,

    FOREIGN KEY (entity_id) REFERENCES entities(entity_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE,

    UNIQUE (entity_id, tag_id)
);

CREATE INDEX idx_entity_tags_entity ON entity_tags(entity_id);
CREATE INDEX idx_entity_tags_tag ON entity_tags(tag_id);

-- Full-text search support (entity descriptions)
-- Note: Implementation depends on database system (SQLite FTS, PostgreSQL tsvector, etc.)
-- For SQLite:
CREATE VIRTUAL TABLE IF NOT EXISTS entities_fts USING fts5(
    entity_id,
    identifier,
    name,
    description,
    content='entities',
    content_rowid='entity_id'
);

-- Triggers to keep FTS index updated
CREATE TRIGGER entities_fts_insert AFTER INSERT ON entities BEGIN
    INSERT INTO entities_fts(entity_id, identifier, name, description)
    VALUES (new.entity_id, new.identifier, new.name, new.description);
END;

CREATE TRIGGER entities_fts_update AFTER UPDATE ON entities BEGIN
    UPDATE entities_fts SET
        identifier = new.identifier,
        name = new.name,
        description = new.description
    WHERE entity_id = new.entity_id;
END;

CREATE TRIGGER entities_fts_delete AFTER DELETE ON entities BEGIN
    DELETE FROM entities_fts WHERE entity_id = old.entity_id;
END;

-- ============================================================================
-- MATERIALIZED VIEWS FOR COMMON QUERIES
-- ============================================================================

-- Note: SQLite doesn't support materialized views natively,
-- so these are regular views. For PostgreSQL, use CREATE MATERIALIZED VIEW

-- All top-tier entities with their computational mappings
CREATE VIEW v_architectural_primitives AS
SELECT
    e.entity_id,
    et.type_name,
    e.identifier,
    e.name,
    e.description,
    COUNT(DISTINCT cm.mapping_id) as mapping_count,
    GROUP_CONCAT(DISTINCT ap.pattern_name) as patterns
FROM entities e
JOIN entity_types et ON e.entity_type_id = et.type_id
LEFT JOIN computational_mappings cm ON e.entity_id = cm.entity_id
LEFT JOIN architectural_patterns ap ON cm.pattern_id = ap.pattern_id
WHERE et.type_category = 'top_tier'
GROUP BY e.entity_id, et.type_name, e.identifier, e.name, e.description;

-- Entity hierarchy (transitive closure)
-- This is a simple view; for deep hierarchies, consider recursive CTEs
CREATE VIEW v_entity_hierarchy AS
SELECT
    er.source_entity_id as parent_id,
    e1.name as parent_name,
    et1.type_name as parent_type,
    er.target_entity_id as child_id,
    e2.name as child_name,
    et2.type_name as child_type,
    rt.type_name as relationship_type
FROM entity_relationships er
JOIN relationship_types rt ON er.relationship_type_id = rt.relationship_type_id
JOIN entities e1 ON er.source_entity_id = e1.entity_id
JOIN entities e2 ON er.target_entity_id = e2.entity_id
JOIN entity_types et1 ON e1.entity_type_id = et1.type_id
JOIN entity_types et2 ON e2.entity_type_id = et2.type_id
WHERE rt.is_hierarchical = TRUE;

-- Entity completeness score (how much data we have)
CREATE VIEW v_entity_completeness AS
SELECT
    e.entity_id,
    e.name,
    et.type_name,
    (CASE WHEN e.description IS NOT NULL THEN 1 ELSE 0 END +
     CASE WHEN e.mathematical_formulation IS NOT NULL THEN 1 ELSE 0 END +
     COUNT(DISTINCT ep.property_instance_id) +
     COUNT(DISTINCT p.parameter_id) +
     COUNT(DISTINCT ef.formula_id) +
     COUNT(DISTINCT xr.xref_id) +
     COUNT(DISTINCT epub.publication_id)) as completeness_score
FROM entities e
JOIN entity_types et ON e.entity_type_id = et.type_id
LEFT JOIN entity_properties ep ON e.entity_id = ep.entity_id
LEFT JOIN parameters p ON e.entity_id = p.entity_id
LEFT JOIN entity_formulas ef ON e.entity_id = ef.entity_id
LEFT JOIN cross_references xr ON e.entity_id = xr.entity_id
LEFT JOIN entity_publications epub ON e.entity_id = epub.entity_id
GROUP BY e.entity_id, e.name, et.type_name, e.description, e.mathematical_formulation;

-- ============================================================================
-- UTILITY FUNCTIONS AND STORED PROCEDURES
-- ============================================================================

-- Note: SQLite doesn't support stored procedures. These are example patterns.
-- For PostgreSQL, implement as functions.

-- Example: Get all descendants of an entity (recursive)
-- In PostgreSQL:
/*
CREATE OR REPLACE FUNCTION get_descendants(root_entity_id INTEGER)
RETURNS TABLE(entity_id INTEGER, depth INTEGER) AS $$
WITH RECURSIVE descendants AS (
    SELECT entity_id, 0 as depth
    FROM entities
    WHERE entity_id = root_entity_id

    UNION ALL

    SELECT er.target_entity_id, d.depth + 1
    FROM entity_relationships er
    JOIN descendants d ON er.source_entity_id = d.entity_id
    JOIN relationship_types rt ON er.relationship_type_id = rt.relationship_type_id
    WHERE rt.is_hierarchical = TRUE
)
SELECT entity_id, depth FROM descendants;
$$ LANGUAGE SQL;
*/

-- ============================================================================
-- PERFORMANCE INDEXES
-- ============================================================================

-- Additional composite indexes for common query patterns

-- Find all entities of a type with specific properties
CREATE INDEX idx_composite_entity_type_status ON entities(entity_type_id, validation_status);

-- Find entities by type and confidence
CREATE INDEX idx_composite_entity_type_confidence ON entities(entity_type_id, confidence_score);

-- Parameter queries
CREATE INDEX idx_composite_params_entity_type ON parameters(entity_id, parameter_type_id);

-- Relationship queries (both directions)
CREATE INDEX idx_composite_rel_types ON entity_relationships(relationship_type_id, source_entity_id, target_entity_id);

-- Cross-reference lookups
CREATE INDEX idx_composite_xref_db_id ON cross_references(database_id, external_id);

-- Computational mapping queries
CREATE INDEX idx_composite_mapping_validated ON computational_mappings(validated, fidelity_score);

-- ============================================================================
-- DATA QUALITY CONSTRAINTS
-- ============================================================================

-- Ensure at least one value is populated in entity_properties
CREATE TRIGGER check_property_value
BEFORE INSERT ON entity_properties
FOR EACH ROW
WHEN (
    NEW.value_string IS NULL AND
    NEW.value_integer IS NULL AND
    NEW.value_real IS NULL AND
    NEW.value_boolean IS NULL AND
    NEW.value_text IS NULL AND
    NEW.value_json IS NULL
)
BEGIN
    SELECT RAISE(ABORT, 'At least one value field must be populated');
END;

-- Update entity timestamp on modification
CREATE TRIGGER update_entity_timestamp
AFTER UPDATE ON entities
FOR EACH ROW
BEGIN
    UPDATE entities SET updated_at = CURRENT_TIMESTAMP WHERE entity_id = NEW.entity_id;
END;

-- Increment entity version on update
CREATE TRIGGER increment_entity_version
AFTER UPDATE ON entities
FOR EACH ROW
WHEN OLD.description != NEW.description OR
     OLD.mathematical_formulation != NEW.mathematical_formulation
BEGIN
    UPDATE entities SET version = version + 1 WHERE entity_id = NEW.entity_id;
END;

-- ============================================================================
-- SAMPLE DATA INSERTION TEMPLATES
-- ============================================================================

-- Example: Inserting a mechanism
/*
-- 1. Insert core entity
INSERT INTO entities (entity_id, entity_type_id, identifier, name, description,
                      mathematical_formulation, confidence_score, evidence_strength,
                      source_database, curator)
VALUES (1, 1, 'MECH_001', 'Lateral Inhibition',
        'Mechanism where active neurons suppress neighboring neurons',
        'dy_i/dt = -y_i + f(x_i - sum(w_ij * y_j))',
        0.95, 'experimental', 'NeuroML', 'John Doe');

-- 2. Insert mechanism-specific details
INSERT INTO mechanisms (mechanism_id, entity_id, mechanism_class, update_rule,
                        time_scale_ms, reversibility)
VALUES (1, 1, 'lateral_inhibition', 'dy_i/dt = -y_i + f(x_i - sum(w_ij * y_j))',
        50.0, TRUE);

-- 3. Add parameters
INSERT INTO parameters (parameter_id, entity_id, parameter_type_id, value,
                        uncertainty, organism)
VALUES (1, 1, 3, 50.0, 5.0, 'Homo sapiens');

-- 4. Add computational mapping
INSERT INTO architectural_patterns (pattern_id, pattern_name, pattern_category,
                                    formal_description)
VALUES (1, 'Winner-Take-All Network', 'neural_network',
        'Competitive network where strongest input suppresses others');

INSERT INTO computational_mappings (mapping_id, entity_id, pattern_id,
                                   mapping_type, fidelity_score, description)
VALUES (1, 1, 1, 'isomorphic', 0.90,
        'Lateral inhibition directly implements WTA competition');

-- 5. Add cross-references
INSERT INTO cross_references (xref_id, entity_id, database_id, external_id,
                             external_url)
VALUES (1, 1, 10, 'ModelDB:12345',
        'https://modeldb.science/12345');

-- 6. Add publication
INSERT INTO publications (publication_id, pmid, doi, title, authors, journal, year)
VALUES (1, '12345678', '10.1038/nature12345',
        'Lateral inhibition in sensory processing',
        'Smith J, Doe J', 'Nature', 2020);

INSERT INTO entity_publications (entity_publication_id, entity_id, publication_id,
                                evidence_type, relevance_score)
VALUES (1, 1, 1, 'primary', 1.0);
*/

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================

-- Summary statistics
SELECT '=== Schema Creation Complete ===' as status;
SELECT 'Total tables created: ' || COUNT(*) || ' tables' as summary
FROM sqlite_master WHERE type='table';

SELECT 'Total indexes created: ' || COUNT(*) || ' indexes' as summary
FROM sqlite_master WHERE type='index';

SELECT 'Total views created: ' || COUNT(*) || ' views' as summary
FROM sqlite_master WHERE type='view';
