-- BioFormulas Database Schema
-- Stores mathematical formulas from biological modeling databases

PRAGMA foreign_keys = ON;

-- ============================================
-- CORE TABLES
-- ============================================

-- Sources: BioModels, ModelDB, NeuroML, etc.
CREATE TABLE IF NOT EXISTS sources (
    source_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    url TEXT,
    description TEXT,
    formula_count INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories of formulas
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    parent_category_id INTEGER REFERENCES categories(category_id),
    description TEXT
);

-- Main formulas table
CREATE TABLE IF NOT EXISTS formulas (
    formula_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER REFERENCES sources(source_id),
    category_id INTEGER REFERENCES categories(category_id),
    name TEXT NOT NULL,
    description TEXT,
    latex TEXT,                          -- LaTeX representation
    mathml TEXT,                         -- MathML representation
    symbolic TEXT,                       -- SymPy-compatible string
    python_code TEXT,                    -- Python implementation
    formula_type TEXT NOT NULL,          -- ODE, algebraic, kinetic, stochastic, etc.
    domain TEXT,                         -- biochemistry, neuroscience, genetics, etc.
    model_origin TEXT,                   -- Original model name/ID
    publication_doi TEXT,
    publication_year INTEGER,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Variables used in formulas
CREATE TABLE IF NOT EXISTS variables (
    variable_id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    name TEXT,
    description TEXT,
    typical_unit TEXT,
    typical_range_min REAL,
    typical_range_max REAL,
    variable_type TEXT,                  -- state, parameter, constant, input, output
    domain TEXT
);

-- Junction table: formulas <-> variables
CREATE TABLE IF NOT EXISTS formula_variables (
    formula_id INTEGER REFERENCES formulas(formula_id) ON DELETE CASCADE,
    variable_id INTEGER REFERENCES variables(variable_id) ON DELETE CASCADE,
    role TEXT,                           -- dependent, independent, parameter, constant
    PRIMARY KEY (formula_id, variable_id)
);

-- Parameters with typical values
CREATE TABLE IF NOT EXISTS parameters (
    parameter_id INTEGER PRIMARY KEY AUTOINCREMENT,
    formula_id INTEGER REFERENCES formulas(formula_id) ON DELETE CASCADE,
    symbol TEXT NOT NULL,
    name TEXT,
    value REAL,
    unit TEXT,
    source_organism TEXT,
    temperature_celsius REAL,
    ph REAL,
    notes TEXT
);

-- ============================================
-- SPECIALIZED TABLES BY DOMAIN
-- ============================================

-- Ion channel models (HH-style)
CREATE TABLE IF NOT EXISTS ion_channels (
    channel_id INTEGER PRIMARY KEY AUTOINCREMENT,
    formula_id INTEGER REFERENCES formulas(formula_id) ON DELETE CASCADE,
    channel_type TEXT,                   -- Na, K, Ca, Cl, nonspecific
    gating_type TEXT,                    -- HH, Markov, GHK
    num_gates INTEGER,
    activation_var TEXT,                 -- m, n, etc.
    inactivation_var TEXT,               -- h, etc.
    reversal_potential REAL,
    max_conductance REAL,
    conductance_unit TEXT
);

-- Synapse models
CREATE TABLE IF NOT EXISTS synapses (
    synapse_id INTEGER PRIMARY KEY AUTOINCREMENT,
    formula_id INTEGER REFERENCES formulas(formula_id) ON DELETE CASCADE,
    synapse_type TEXT,                   -- AMPA, NMDA, GABA_A, GABA_B, etc.
    plasticity_type TEXT,                -- none, STDP, BCM, Oja, etc.
    transmission_type TEXT,              -- chemical, electrical, mixed
    time_constant_rise REAL,
    time_constant_decay REAL,
    reversal_potential REAL
);

-- Enzyme kinetics
CREATE TABLE IF NOT EXISTS enzyme_kinetics (
    kinetics_id INTEGER PRIMARY KEY AUTOINCREMENT,
    formula_id INTEGER REFERENCES formulas(formula_id) ON DELETE CASCADE,
    enzyme_name TEXT,
    ec_number TEXT,                      -- Enzyme Commission number
    kinetics_type TEXT,                  -- Michaelis-Menten, Hill, ping-pong, etc.
    km REAL,                             -- Michaelis constant
    vmax REAL,                           -- Maximum velocity
    kcat REAL,                           -- Turnover number
    ki REAL,                             -- Inhibition constant
    hill_coefficient REAL,
    substrate TEXT,
    product TEXT,
    inhibitor TEXT,
    activator TEXT
);

-- Reaction networks (stoichiometry)
CREATE TABLE IF NOT EXISTS reactions (
    reaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    formula_id INTEGER REFERENCES formulas(formula_id) ON DELETE CASCADE,
    reaction_name TEXT,
    reactants TEXT,                      -- JSON array
    products TEXT,                       -- JSON array
    stoichiometry TEXT,                  -- JSON object
    rate_law TEXT,
    reversible BOOLEAN DEFAULT FALSE,
    compartment TEXT
);

-- Plasticity rules (STDP, etc.)
CREATE TABLE IF NOT EXISTS plasticity_rules (
    plasticity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    formula_id INTEGER REFERENCES formulas(formula_id) ON DELETE CASCADE,
    rule_type TEXT,                      -- STDP, BCM, Oja, covariance, etc.
    time_window_pre REAL,                -- ms
    time_window_post REAL,               -- ms
    learning_rate REAL,
    weight_dependence TEXT,              -- additive, multiplicative, soft-bound
    calcium_dependent BOOLEAN DEFAULT FALSE
);

-- Oscillator models
CREATE TABLE IF NOT EXISTS oscillators (
    oscillator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    formula_id INTEGER REFERENCES formulas(formula_id) ON DELETE CASCADE,
    oscillator_type TEXT,                -- limit cycle, relaxation, coupled, etc.
    frequency_hz REAL,
    amplitude REAL,
    biological_system TEXT               -- circadian, cardiac, neural, etc.
);

-- Neuron models
CREATE TABLE IF NOT EXISTS neuron_models (
    neuron_id INTEGER PRIMARY KEY AUTOINCREMENT,
    formula_id INTEGER REFERENCES formulas(formula_id) ON DELETE CASCADE,
    model_type TEXT,                     -- HH, LIF, Izhikevich, AdEx, etc.
    num_compartments INTEGER DEFAULT 1,
    threshold_mv REAL,
    resting_potential_mv REAL,
    membrane_capacitance REAL,
    membrane_resistance REAL,
    refractory_period_ms REAL
);

-- Gene regulatory networks
CREATE TABLE IF NOT EXISTS gene_regulation (
    regulation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    formula_id INTEGER REFERENCES formulas(formula_id) ON DELETE CASCADE,
    gene_name TEXT,
    regulation_type TEXT,                -- activation, repression, mixed
    transcription_factor TEXT,
    binding_affinity REAL,
    hill_coefficient REAL,
    basal_rate REAL,
    max_rate REAL
);

-- Signaling cascades
CREATE TABLE IF NOT EXISTS signaling_cascades (
    cascade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    formula_id INTEGER REFERENCES formulas(formula_id) ON DELETE CASCADE,
    pathway_name TEXT,                   -- MAPK, PI3K-Akt, Wnt, etc.
    cascade_level INTEGER,               -- position in cascade
    activation_type TEXT,                -- phosphorylation, binding, etc.
    upstream_component TEXT,
    downstream_component TEXT
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

CREATE INDEX IF NOT EXISTS idx_formulas_source ON formulas(source_id);
CREATE INDEX IF NOT EXISTS idx_formulas_category ON formulas(category_id);
CREATE INDEX IF NOT EXISTS idx_formulas_type ON formulas(formula_type);
CREATE INDEX IF NOT EXISTS idx_formulas_domain ON formulas(domain);
CREATE INDEX IF NOT EXISTS idx_variables_symbol ON variables(symbol);
CREATE INDEX IF NOT EXISTS idx_parameters_symbol ON parameters(symbol);

-- Full-text search on formula descriptions and names
CREATE VIRTUAL TABLE IF NOT EXISTS formulas_fts USING fts5(
    name, description, latex, symbolic, content=formulas, content_rowid=formula_id
);

-- Trigger to keep FTS in sync
CREATE TRIGGER IF NOT EXISTS formulas_ai AFTER INSERT ON formulas BEGIN
    INSERT INTO formulas_fts(rowid, name, description, latex, symbolic)
    VALUES (new.formula_id, new.name, new.description, new.latex, new.symbolic);
END;

CREATE TRIGGER IF NOT EXISTS formulas_ad AFTER DELETE ON formulas BEGIN
    INSERT INTO formulas_fts(formulas_fts, rowid, name, description, latex, symbolic)
    VALUES('delete', old.formula_id, old.name, old.description, old.latex, old.symbolic);
END;

CREATE TRIGGER IF NOT EXISTS formulas_au AFTER UPDATE ON formulas BEGIN
    INSERT INTO formulas_fts(formulas_fts, rowid, name, description, latex, symbolic)
    VALUES('delete', old.formula_id, old.name, old.description, old.latex, old.symbolic);
    INSERT INTO formulas_fts(rowid, name, description, latex, symbolic)
    VALUES (new.formula_id, new.name, new.description, new.latex, new.symbolic);
END;

-- ============================================
-- VIEWS FOR COMMON QUERIES
-- ============================================

CREATE VIEW IF NOT EXISTS v_formulas_full AS
SELECT
    f.formula_id,
    f.name,
    f.description,
    f.latex,
    f.symbolic,
    f.formula_type,
    f.domain,
    s.name as source_name,
    c.name as category_name,
    f.model_origin,
    f.publication_doi
FROM formulas f
LEFT JOIN sources s ON f.source_id = s.source_id
LEFT JOIN categories c ON f.category_id = c.category_id;

CREATE VIEW IF NOT EXISTS v_neuroscience_formulas AS
SELECT * FROM v_formulas_full WHERE domain = 'neuroscience';

CREATE VIEW IF NOT EXISTS v_biochemistry_formulas AS
SELECT * FROM v_formulas_full WHERE domain = 'biochemistry';

CREATE VIEW IF NOT EXISTS v_ode_formulas AS
SELECT * FROM v_formulas_full WHERE formula_type = 'ODE';
