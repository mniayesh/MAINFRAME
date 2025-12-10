#!/usr/bin/env python3
"""
Populate BioFormulas database with biological modeling equations.

Sources represented:
- BioModels Database (SBML models - ODEs, reaction kinetics)
- ModelDB (computational neuroscience)
- NeuroML mechanisms
"""

import sqlite3
import logging
from datetime import datetime
from pathlib import Path

# Configure logging to show each formula as it's added
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent / 'bioformulas.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_source(conn, name, url, description):
    """Add a data source."""
    cur = conn.execute("""
        INSERT OR IGNORE INTO sources (name, url, description)
        VALUES (?, ?, ?)
    """, (name, url, description))
    conn.commit()
    if cur.rowcount > 0:
        log.info(f"📚 Added source: {name}")
    return conn.execute("SELECT source_id FROM sources WHERE name = ?", (name,)).fetchone()[0]

def add_category(conn, name, parent_id=None, description=None):
    """Add a category."""
    cur = conn.execute("""
        INSERT OR IGNORE INTO categories (name, parent_category_id, description)
        VALUES (?, ?, ?)
    """, (name, parent_id, description))
    conn.commit()
    if cur.rowcount > 0:
        log.info(f"📁 Added category: {name}")
    return conn.execute("SELECT category_id FROM categories WHERE name = ?", (name,)).fetchone()[0]

def add_formula(conn, name, latex, description, formula_type, category_id, source_id,
                mathml=None, symbolic=None, python_code=None,
                domain=None, model_origin=None, doi=None, year=None):
    """Add a formula and log it."""
    cur = conn.execute("""
        INSERT INTO formulas (name, latex, mathml, symbolic, python_code, description,
                              formula_type, domain, model_origin, source_id, category_id,
                              publication_doi, publication_year)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, latex, mathml, symbolic, python_code, description,
          formula_type, domain, model_origin, source_id, category_id,
          doi, year))
    conn.commit()
    formula_id = cur.lastrowid
    log.info(f"➕ [{formula_type}] {name}: {latex[:60]}{'...' if len(latex) > 60 else ''}")
    return formula_id

def add_variable(conn, symbol, name, description=None, typical_unit=None,
                 range_min=None, range_max=None, var_type=None, domain=None):
    """Add a variable."""
    cur = conn.execute("""
        INSERT OR IGNORE INTO variables (symbol, name, description, typical_unit,
                                         typical_range_min, typical_range_max, variable_type, domain)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (symbol, name, description, typical_unit, range_min, range_max, var_type, domain))
    conn.commit()
    return conn.execute("SELECT variable_id FROM variables WHERE symbol = ?", (symbol,)).fetchone()[0]

def link_formula_variable(conn, formula_id, variable_id, role):
    """Link a variable to a formula."""
    conn.execute("""
        INSERT OR IGNORE INTO formula_variables (formula_id, variable_id, role)
        VALUES (?, ?, ?)
    """, (formula_id, variable_id, role))
    conn.commit()

def add_ion_channel(conn, formula_id, channel_type, gating_type, num_gates=1,
                    activation_var=None, inactivation_var=None,
                    reversal_potential=None, max_conductance=None, cond_unit="mS/cm^2"):
    """Add ion channel details."""
    conn.execute("""
        INSERT INTO ion_channels (formula_id, channel_type, gating_type, num_gates,
                                  activation_var, inactivation_var, reversal_potential,
                                  max_conductance, conductance_unit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (formula_id, channel_type, gating_type, num_gates, activation_var, inactivation_var,
          reversal_potential, max_conductance, cond_unit))
    conn.commit()
    log.info(f"   ⚡ Ion channel: {channel_type} ({gating_type})")

def add_synapse(conn, formula_id, synapse_type, plasticity_type=None, transmission_type=None,
                tau_rise=None, tau_decay=None, reversal_potential=None):
    """Add synapse details."""
    conn.execute("""
        INSERT INTO synapses (formula_id, synapse_type, plasticity_type, transmission_type,
                              time_constant_rise, time_constant_decay, reversal_potential)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (formula_id, synapse_type, plasticity_type, transmission_type,
          tau_rise, tau_decay, reversal_potential))
    conn.commit()
    log.info(f"   🔗 Synapse: {synapse_type}")

def add_enzyme_kinetics(conn, formula_id, enzyme_name, kinetics_type, substrate=None, product=None,
                        km=None, vmax=None, kcat=None, ki=None, hill_coef=None,
                        ec_number=None, inhibitor=None, activator=None):
    """Add enzyme kinetics details."""
    conn.execute("""
        INSERT INTO enzyme_kinetics (formula_id, enzyme_name, ec_number, kinetics_type,
                                     km, vmax, kcat, ki, hill_coefficient,
                                     substrate, product, inhibitor, activator)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (formula_id, enzyme_name, ec_number, kinetics_type, km, vmax, kcat, ki, hill_coef,
          substrate, product, inhibitor, activator))
    conn.commit()
    log.info(f"   🧬 Enzyme: {enzyme_name} ({kinetics_type})")

def add_neuron_model(conn, formula_id, model_type, num_compartments=1,
                     threshold_mv=None, resting_mv=None, cap=None, res=None, refractory=None):
    """Add neuron model details."""
    conn.execute("""
        INSERT INTO neuron_models (formula_id, model_type, num_compartments,
                                   threshold_mv, resting_potential_mv, membrane_capacitance,
                                   membrane_resistance, refractory_period_ms)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (formula_id, model_type, num_compartments, threshold_mv, resting_mv, cap, res, refractory))
    conn.commit()
    log.info(f"   🧠 Neuron model: {model_type}")

def add_plasticity_rule(conn, formula_id, rule_type, tw_pre=None, tw_post=None,
                        learning_rate=None, weight_dependence=None, calcium_dep=False):
    """Add plasticity rule details."""
    conn.execute("""
        INSERT INTO plasticity_rules (formula_id, rule_type, time_window_pre, time_window_post,
                                      learning_rate, weight_dependence, calcium_dependent)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (formula_id, rule_type, tw_pre, tw_post, learning_rate, weight_dependence, calcium_dep))
    conn.commit()
    log.info(f"   📈 Plasticity: {rule_type}")

def populate_sources(conn):
    """Add data sources."""
    log.info("=" * 60)
    log.info("ADDING DATA SOURCES")
    log.info("=" * 60)

    sources = {}
    sources['biomodels'] = add_source(conn, 'BioModels Database',
        'https://www.ebi.ac.uk/biomodels/',
        'Repository of mathematical models of biological systems (SBML)')

    sources['modeldb'] = add_source(conn, 'ModelDB',
        'https://modeldb.yale.edu/',
        'Database of computational neuroscience models')

    sources['neuroml'] = add_source(conn, 'NeuroML',
        'https://neuroml.org/',
        'Standard format for neural model components')

    sources['literature'] = add_source(conn, 'Scientific Literature',
        None, 'Equations from peer-reviewed publications')

    return sources

def populate_categories(conn):
    """Add formula categories."""
    log.info("=" * 60)
    log.info("ADDING CATEGORIES")
    log.info("=" * 60)

    cats = {}

    # Top-level categories
    cats['neuro'] = add_category(conn, 'Neuroscience', None,
        'Neural and brain modeling equations')
    cats['biochem'] = add_category(conn, 'Biochemistry', None,
        'Enzyme kinetics and metabolic reactions')
    cats['genetics'] = add_category(conn, 'Gene Regulation', None,
        'Transcription, translation, and regulatory networks')
    cats['systems'] = add_category(conn, 'Systems Biology', None,
        'Whole-system and network models')
    cats['population'] = add_category(conn, 'Population Dynamics', None,
        'Growth, competition, and ecological models')

    # Neuroscience subcategories
    cats['ion_channels'] = add_category(conn, 'Ion Channels', cats['neuro'],
        'Voltage and ligand-gated channel kinetics')
    cats['synapses'] = add_category(conn, 'Synaptic Transmission', cats['neuro'],
        'Synapse models and neurotransmitter dynamics')
    cats['neurons'] = add_category(conn, 'Neuron Models', cats['neuro'],
        'Single neuron and compartmental models')
    cats['plasticity'] = add_category(conn, 'Synaptic Plasticity', cats['neuro'],
        'Learning rules and weight changes')
    cats['networks'] = add_category(conn, 'Neural Networks', cats['neuro'],
        'Population and network dynamics')

    # Biochemistry subcategories
    cats['enzyme'] = add_category(conn, 'Enzyme Kinetics', cats['biochem'],
        'Michaelis-Menten and enzyme mechanisms')
    cats['metabolic'] = add_category(conn, 'Metabolic Pathways', cats['biochem'],
        'Metabolic network dynamics')
    cats['signaling'] = add_category(conn, 'Cell Signaling', cats['biochem'],
        'Signal transduction cascades')

    return cats

def populate_neuroscience_formulas(conn, sources, cats):
    """Add neuroscience formulas."""
    log.info("=" * 60)
    log.info("ADDING NEUROSCIENCE FORMULAS")
    log.info("=" * 60)

    # =========================================================================
    # HODGKIN-HUXLEY MODEL
    # =========================================================================
    log.info("-" * 40)
    log.info("Hodgkin-Huxley Model")
    log.info("-" * 40)

    # Membrane equation
    fid = add_formula(conn,
        name="Hodgkin-Huxley Membrane Equation",
        latex=r"C_m \frac{dV}{dt} = -g_{Na} m^3 h (V - E_{Na}) - g_K n^4 (V - E_K) - g_L (V - E_L) + I_{ext}",
        description="Main membrane potential equation from the Hodgkin-Huxley model describing action potential generation",
        formula_type="ODE",
        category_id=cats['neurons'],
        source_id=sources['modeldb'],
        symbolic="C_m * Derivative(V, t) + g_Na * m**3 * h * (V - E_Na) + g_K * n**4 * (V - E_K) + g_L * (V - E_L) - I_ext",
        python_code="dV_dt = (I_ext - g_Na * m**3 * h * (V - E_Na) - g_K * n**4 * (V - E_K) - g_L * (V - E_L)) / C_m",
        domain="electrophysiology",
        model_origin="hodgkin-huxley",
        doi="10.1113/jphysiol.1952.sp004764",
        year=1952
    )
    add_neuron_model(conn, fid, "Hodgkin-Huxley", 1, -55.0, -65.0, 1.0, None, 2.0)

    # Na+ channel activation (m gate)
    fid = add_formula(conn,
        name="HH Sodium Activation (m)",
        latex=r"\frac{dm}{dt} = \alpha_m(V)(1-m) - \beta_m(V)m",
        description="Sodium channel activation gating variable dynamics",
        formula_type="ODE",
        category_id=cats['ion_channels'],
        source_id=sources['modeldb'],
        python_code="dm_dt = alpha_m(V) * (1 - m) - beta_m(V) * m",
        domain="electrophysiology",
        model_origin="hodgkin-huxley"
    )
    add_ion_channel(conn, fid, "Na_HH", "voltage-gated", 4, "m", "h", 50.0, 120.0)

    # Na+ alpha_m rate
    add_formula(conn,
        name="HH Alpha_m Rate",
        latex=r"\alpha_m(V) = \frac{0.1(V+40)}{1 - \exp(-(V+40)/10)}",
        description="Forward rate constant for sodium activation",
        formula_type="rate_equation",
        category_id=cats['ion_channels'],
        source_id=sources['modeldb'],
        python_code="alpha_m = 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))",
        domain="electrophysiology",
        model_origin="hodgkin-huxley"
    )

    # Na+ beta_m rate
    add_formula(conn,
        name="HH Beta_m Rate",
        latex=r"\beta_m(V) = 4 \exp(-(V+65)/18)",
        description="Backward rate constant for sodium activation",
        formula_type="rate_equation",
        category_id=cats['ion_channels'],
        source_id=sources['modeldb'],
        python_code="beta_m = 4 * np.exp(-(V + 65) / 18)",
        domain="electrophysiology",
        model_origin="hodgkin-huxley"
    )

    # Na+ channel inactivation (h gate)
    fid = add_formula(conn,
        name="HH Sodium Inactivation (h)",
        latex=r"\frac{dh}{dt} = \alpha_h(V)(1-h) - \beta_h(V)h",
        description="Sodium channel inactivation gating variable dynamics",
        formula_type="ODE",
        category_id=cats['ion_channels'],
        source_id=sources['modeldb'],
        python_code="dh_dt = alpha_h(V) * (1 - h) - beta_h(V) * h",
        domain="electrophysiology",
        model_origin="hodgkin-huxley"
    )
    add_ion_channel(conn, fid, "Na_HH_inact", "voltage-gated", 1, None, "h", 50.0, 120.0)

    # K+ channel activation (n gate)
    fid = add_formula(conn,
        name="HH Potassium Activation (n)",
        latex=r"\frac{dn}{dt} = \alpha_n(V)(1-n) - \beta_n(V)n",
        description="Potassium channel activation gating variable dynamics",
        formula_type="ODE",
        category_id=cats['ion_channels'],
        source_id=sources['modeldb'],
        python_code="dn_dt = alpha_n(V) * (1 - n) - beta_n(V) * n",
        domain="electrophysiology",
        model_origin="hodgkin-huxley"
    )
    add_ion_channel(conn, fid, "K_HH", "voltage-gated", 4, "n", None, -77.0, 36.0)

    # K+ alpha_n rate
    add_formula(conn,
        name="HH Alpha_n Rate",
        latex=r"\alpha_n(V) = \frac{0.01(V+55)}{1 - \exp(-(V+55)/10)}",
        description="Forward rate constant for potassium activation",
        formula_type="rate_equation",
        category_id=cats['ion_channels'],
        source_id=sources['modeldb'],
        python_code="alpha_n = 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10))",
        domain="electrophysiology",
        model_origin="hodgkin-huxley"
    )

    # K+ beta_n rate
    add_formula(conn,
        name="HH Beta_n Rate",
        latex=r"\beta_n(V) = 0.125 \exp(-(V+65)/80)",
        description="Backward rate constant for potassium activation",
        formula_type="rate_equation",
        category_id=cats['ion_channels'],
        source_id=sources['modeldb'],
        python_code="beta_n = 0.125 * np.exp(-(V + 65) / 80)",
        domain="electrophysiology",
        model_origin="hodgkin-huxley"
    )

    # =========================================================================
    # OTHER NEURON MODELS
    # =========================================================================
    log.info("-" * 40)
    log.info("Other Neuron Models")
    log.info("-" * 40)

    # Leaky Integrate-and-Fire
    fid = add_formula(conn,
        name="Leaky Integrate-and-Fire",
        latex=r"\tau_m \frac{dV}{dt} = -(V - V_{rest}) + R_m I_{ext}",
        description="Simple neuron model with passive leak current and threshold-based spiking",
        formula_type="ODE",
        category_id=cats['neurons'],
        source_id=sources['literature'],
        python_code="dV_dt = (-(V - V_rest) + R_m * I_ext) / tau_m",
        domain="computational-neuroscience",
        model_origin="integrate-and-fire"
    )
    add_neuron_model(conn, fid, "LIF", 1, -55.0, -70.0, 1.0, 10.0, 2.0)

    # Exponential Integrate-and-Fire
    fid = add_formula(conn,
        name="Exponential Integrate-and-Fire",
        latex=r"\tau_m \frac{dV}{dt} = -(V - V_{rest}) + \Delta_T \exp\left(\frac{V - V_T}{\Delta_T}\right) + R_m I_{ext}",
        description="LIF with exponential spike initiation for more realistic dynamics",
        formula_type="ODE",
        category_id=cats['neurons'],
        source_id=sources['literature'],
        python_code="dV_dt = (-(V - V_rest) + Delta_T * np.exp((V - V_T) / Delta_T) + R_m * I_ext) / tau_m",
        domain="computational-neuroscience",
        model_origin="exponential-integrate-fire"
    )
    add_neuron_model(conn, fid, "EIF", 1, -50.0, -70.0, 1.0, 10.0, 2.0)

    # AdEx - Adaptation current
    fid = add_formula(conn,
        name="AdEx Adaptation Current",
        latex=r"\tau_w \frac{dw}{dt} = a(V - V_{rest}) - w",
        description="Adaptation current dynamics in AdEx model",
        formula_type="ODE",
        category_id=cats['neurons'],
        source_id=sources['literature'],
        python_code="dw_dt = (a * (V - V_rest) - w) / tau_w",
        domain="computational-neuroscience",
        model_origin="adaptive-exponential"
    )
    add_neuron_model(conn, fid, "AdEx", 1, -50.0, -70.0, 1.0, 10.0, 2.0)

    # Izhikevich Model - Membrane
    fid = add_formula(conn,
        name="Izhikevich Membrane Equation",
        latex=r"\frac{dv}{dt} = 0.04v^2 + 5v + 140 - u + I",
        description="Izhikevich model membrane potential dynamics",
        formula_type="ODE",
        category_id=cats['neurons'],
        source_id=sources['literature'],
        python_code="dv_dt = 0.04 * v**2 + 5 * v + 140 - u + I",
        domain="computational-neuroscience",
        model_origin="izhikevich",
        doi="10.1109/TNN.2004.832719",
        year=2003
    )
    add_neuron_model(conn, fid, "Izhikevich", 1, 30.0, -65.0)

    # Izhikevich Model - Recovery
    add_formula(conn,
        name="Izhikevich Recovery Variable",
        latex=r"\frac{du}{dt} = a(bv - u)",
        description="Izhikevich model recovery variable dynamics",
        formula_type="ODE",
        category_id=cats['neurons'],
        source_id=sources['literature'],
        python_code="du_dt = a * (b * v - u)",
        domain="computational-neuroscience",
        model_origin="izhikevich"
    )

    # FitzHugh-Nagumo
    fid = add_formula(conn,
        name="FitzHugh-Nagumo Voltage",
        latex=r"\frac{dv}{dt} = v - \frac{v^3}{3} - w + I_{ext}",
        description="FitzHugh-Nagumo model - simplified HH capturing excitability",
        formula_type="ODE",
        category_id=cats['neurons'],
        source_id=sources['literature'],
        python_code="dv_dt = v - v**3/3 - w + I_ext",
        domain="computational-neuroscience",
        model_origin="fitzhugh-nagumo"
    )
    add_neuron_model(conn, fid, "FitzHugh-Nagumo", 1)

    add_formula(conn,
        name="FitzHugh-Nagumo Recovery",
        latex=r"\frac{dw}{dt} = \epsilon(v + a - bw)",
        description="FitzHugh-Nagumo recovery variable",
        formula_type="ODE",
        category_id=cats['neurons'],
        source_id=sources['literature'],
        python_code="dw_dt = epsilon * (v + a - b * w)",
        domain="computational-neuroscience",
        model_origin="fitzhugh-nagumo"
    )

    # Morris-Lecar
    fid = add_formula(conn,
        name="Morris-Lecar Membrane",
        latex=r"C \frac{dV}{dt} = I - g_L(V-V_L) - g_{Ca}m_\infty(V)(V-V_{Ca}) - g_K w(V-V_K)",
        description="Morris-Lecar model - 2D reduction of HH for barnacle muscle",
        formula_type="ODE",
        category_id=cats['neurons'],
        source_id=sources['literature'],
        python_code="dV_dt = (I - g_L*(V-V_L) - g_Ca*m_inf(V)*(V-V_Ca) - g_K*w*(V-V_K)) / C",
        domain="electrophysiology",
        model_origin="morris-lecar"
    )
    add_neuron_model(conn, fid, "Morris-Lecar", 1)

    # =========================================================================
    # SYNAPTIC MODELS
    # =========================================================================
    log.info("-" * 40)
    log.info("Synaptic Transmission")
    log.info("-" * 40)

    # AMPA synapse
    fid = add_formula(conn,
        name="AMPA Synaptic Current",
        latex=r"I_{AMPA} = g_{AMPA} s (V - E_{AMPA})",
        description="AMPA receptor-mediated excitatory synaptic current",
        formula_type="current_equation",
        category_id=cats['synapses'],
        source_id=sources['neuroml'],
        python_code="I_AMPA = g_AMPA * s * (V - E_AMPA)",
        domain="synaptic-transmission",
        model_origin="AMPA"
    )
    add_synapse(conn, fid, "AMPA", None, "glutamate", 0.5, 3.0, 0.0)

    # AMPA gating
    add_formula(conn,
        name="AMPA Gating Dynamics",
        latex=r"\frac{ds}{dt} = \alpha [T](1-s) - \beta s",
        description="AMPA receptor gating variable dynamics",
        formula_type="ODE",
        category_id=cats['synapses'],
        source_id=sources['neuroml'],
        python_code="ds_dt = alpha * T * (1 - s) - beta * s",
        domain="synaptic-transmission",
        model_origin="AMPA"
    )

    # NMDA synapse
    fid = add_formula(conn,
        name="NMDA Synaptic Current",
        latex=r"I_{NMDA} = g_{NMDA} s B(V) (V - E_{NMDA})",
        description="NMDA receptor current with voltage-dependent Mg2+ block",
        formula_type="current_equation",
        category_id=cats['synapses'],
        source_id=sources['neuroml'],
        python_code="I_NMDA = g_NMDA * s * B(V) * (V - E_NMDA)",
        domain="synaptic-transmission",
        model_origin="NMDA"
    )
    add_synapse(conn, fid, "NMDA", None, "glutamate", 2.0, 100.0, 0.0)

    # NMDA Mg block
    add_formula(conn,
        name="NMDA Magnesium Block",
        latex=r"B(V) = \frac{1}{1 + \frac{[Mg^{2+}]}{3.57} \exp(-0.062 V)}",
        description="Voltage-dependent magnesium block of NMDA receptors",
        formula_type="algebraic",
        category_id=cats['synapses'],
        source_id=sources['literature'],
        python_code="B = 1 / (1 + (Mg / 3.57) * np.exp(-0.062 * V))",
        domain="synaptic-transmission",
        model_origin="NMDA"
    )

    # GABA-A synapse
    fid = add_formula(conn,
        name="GABA-A Synaptic Current",
        latex=r"I_{GABA_A} = g_{GABA_A} s (V - E_{Cl})",
        description="GABA-A receptor-mediated inhibitory synaptic current",
        formula_type="current_equation",
        category_id=cats['synapses'],
        source_id=sources['neuroml'],
        python_code="I_GABA_A = g_GABA_A * s * (V - E_Cl)",
        domain="synaptic-transmission",
        model_origin="GABA-A"
    )
    add_synapse(conn, fid, "GABA-A", None, "GABAergic", 0.5, 6.0, -70.0)

    # GABA-B synapse
    fid = add_formula(conn,
        name="GABA-B Synaptic Current",
        latex=r"I_{GABA_B} = g_{GABA_B} \frac{[G]^n}{[G]^n + K_d} (V - E_K)",
        description="GABA-B receptor current via G-protein activation",
        formula_type="current_equation",
        category_id=cats['synapses'],
        source_id=sources['neuroml'],
        python_code="I_GABA_B = g_GABA_B * (G**n / (G**n + Kd)) * (V - E_K)",
        domain="synaptic-transmission",
        model_origin="GABA-B"
    )
    add_synapse(conn, fid, "GABA-B", None, "GABAergic", 50.0, 200.0, -90.0)

    # Alpha function synapse
    add_formula(conn,
        name="Alpha Function Synapse",
        latex=r"g(t) = g_{max} \frac{t-t_0}{\tau} \exp\left(1 - \frac{t-t_0}{\tau}\right)",
        description="Alpha function for synaptic conductance time course",
        formula_type="algebraic",
        category_id=cats['synapses'],
        source_id=sources['literature'],
        python_code="g = g_max * (t - t0) / tau * np.exp(1 - (t - t0) / tau)",
        domain="synaptic-transmission",
        model_origin="alpha-function"
    )

    # Double exponential synapse
    add_formula(conn,
        name="Double Exponential Synapse",
        latex=r"g(t) = g_{max} \frac{\tau_d \tau_r}{\tau_d - \tau_r} \left( \exp\left(-\frac{t}{\tau_d}\right) - \exp\left(-\frac{t}{\tau_r}\right) \right)",
        description="Bi-exponential synaptic conductance with rise and decay",
        formula_type="algebraic",
        category_id=cats['synapses'],
        source_id=sources['literature'],
        python_code="g = g_max * tau_d * tau_r / (tau_d - tau_r) * (np.exp(-t/tau_d) - np.exp(-t/tau_r))",
        domain="synaptic-transmission",
        model_origin="double-exponential"
    )

    # =========================================================================
    # SYNAPTIC PLASTICITY
    # =========================================================================
    log.info("-" * 40)
    log.info("Synaptic Plasticity")
    log.info("-" * 40)

    # Pair-based STDP
    fid = add_formula(conn,
        name="Pair-Based STDP",
        latex=r"\Delta w = \begin{cases} A_+ \exp(-\Delta t / \tau_+) & \text{if } \Delta t > 0 \\ -A_- \exp(\Delta t / \tau_-) & \text{if } \Delta t < 0 \end{cases}",
        description="Classic spike-timing dependent plasticity rule",
        formula_type="plasticity_rule",
        category_id=cats['plasticity'],
        source_id=sources['modeldb'],
        python_code="dw = A_plus * np.exp(-dt/tau_plus) if dt > 0 else -A_minus * np.exp(dt/tau_minus)",
        domain="synaptic-plasticity",
        model_origin="STDP",
        doi="10.1523/JNEUROSCI.18-24-10464.1998",
        year=1998
    )
    add_plasticity_rule(conn, fid, "pair-STDP", 20.0, 20.0, 0.01, "additive", False)

    # Triplet STDP
    fid = add_formula(conn,
        name="Triplet STDP Rule",
        latex=r"\Delta w = r_1(t) \left( A_2^+ + A_3^+ r_2(t-\epsilon) \right) - o_1(t) \left( A_2^- + A_3^- o_2(t-\epsilon) \right)",
        description="Triplet STDP capturing frequency dependence",
        formula_type="plasticity_rule",
        category_id=cats['plasticity'],
        source_id=sources['literature'],
        domain="synaptic-plasticity",
        model_origin="triplet-STDP",
        doi="10.1523/JNEUROSCI.1425-06.2006",
        year=2006
    )
    add_plasticity_rule(conn, fid, "triplet-STDP", 40.0, 40.0, 0.01, "multiplicative", False)

    # BCM rule
    fid = add_formula(conn,
        name="BCM Plasticity Rule",
        latex=r"\frac{dw}{dt} = \eta \phi(c) c_{pre}",
        description="Bienenstock-Cooper-Munro rule with sliding threshold",
        formula_type="ODE",
        category_id=cats['plasticity'],
        source_id=sources['literature'],
        python_code="dw_dt = eta * phi(c) * c_pre",
        domain="synaptic-plasticity",
        model_origin="BCM",
        doi="10.1523/JNEUROSCI.02-01-00032.1982",
        year=1982
    )
    add_plasticity_rule(conn, fid, "BCM", None, None, 0.001, "sliding-threshold", False)

    # BCM phi function
    add_formula(conn,
        name="BCM Phi Function",
        latex=r"\phi(c) = c(c - \theta_m)",
        description="BCM selectivity function",
        formula_type="algebraic",
        category_id=cats['plasticity'],
        source_id=sources['literature'],
        python_code="phi = c * (c - theta_m)",
        domain="synaptic-plasticity",
        model_origin="BCM"
    )

    # Oja's rule
    fid = add_formula(conn,
        name="Oja's Learning Rule",
        latex=r"\Delta w_i = \eta y (x_i - y w_i)",
        description="Hebbian rule with weight normalization (PCA)",
        formula_type="plasticity_rule",
        category_id=cats['plasticity'],
        source_id=sources['literature'],
        python_code="dw = eta * y * (x - y * w)",
        domain="synaptic-plasticity",
        model_origin="Oja"
    )
    add_plasticity_rule(conn, fid, "Oja", None, None, 0.01, "multiplicative", False)

    # Calcium-based plasticity
    fid = add_formula(conn,
        name="Calcium-Based Plasticity",
        latex=r"\frac{dw}{dt} = \gamma_p \Omega([Ca^{2+}]) - \gamma_d \Omega([Ca^{2+}]) w",
        description="Plasticity driven by calcium concentration levels",
        formula_type="ODE",
        category_id=cats['plasticity'],
        source_id=sources['literature'],
        python_code="dw_dt = gamma_p * Omega_p(Ca) - gamma_d * Omega_d(Ca) * w",
        domain="synaptic-plasticity",
        model_origin="calcium-based"
    )
    add_plasticity_rule(conn, fid, "calcium-based", 100.0, 100.0, 0.001, "multiplicative", True)

    # =========================================================================
    # NEURAL POPULATION MODELS
    # =========================================================================
    log.info("-" * 40)
    log.info("Neural Population Models")
    log.info("-" * 40)

    # Wilson-Cowan excitatory
    add_formula(conn,
        name="Wilson-Cowan Excitatory",
        latex=r"\tau_E \frac{dE}{dt} = -E + S_E(w_{EE}E - w_{EI}I + I_{ext})",
        description="Wilson-Cowan excitatory population rate equation",
        formula_type="ODE",
        category_id=cats['networks'],
        source_id=sources['literature'],
        python_code="dE_dt = (-E + S_E(w_EE*E - w_EI*I + I_ext)) / tau_E",
        domain="neural-networks",
        model_origin="wilson-cowan",
        doi="10.1016/S0006-3495(72)86068-5",
        year=1972
    )

    # Wilson-Cowan inhibitory
    add_formula(conn,
        name="Wilson-Cowan Inhibitory",
        latex=r"\tau_I \frac{dI}{dt} = -I + S_I(w_{IE}E - w_{II}I)",
        description="Wilson-Cowan inhibitory population rate equation",
        formula_type="ODE",
        category_id=cats['networks'],
        source_id=sources['literature'],
        python_code="dI_dt = (-I + S_I(w_IE*E - w_II*I)) / tau_I",
        domain="neural-networks",
        model_origin="wilson-cowan"
    )

    # Sigmoid activation function
    add_formula(conn,
        name="Neural Sigmoid Activation",
        latex=r"S(x) = \frac{1}{1 + \exp(-\beta(x - \theta))}",
        description="Sigmoidal firing rate function",
        formula_type="activation_function",
        category_id=cats['networks'],
        source_id=sources['literature'],
        python_code="S = 1 / (1 + np.exp(-beta * (x - theta)))",
        domain="neural-networks",
        model_origin="activation-function"
    )

    # Mean-field firing rate
    add_formula(conn,
        name="Mean-Field Firing Rate",
        latex=r"\nu = \phi(\mu, \sigma) = \left( \tau_{ref} + \tau_m \sqrt{\pi} \int_{(V_{reset}-\mu)/\sigma}^{(V_{th}-\mu)/\sigma} e^{u^2}(1+\text{erf}(u)) du \right)^{-1}",
        description="Mean-field firing rate for LIF neurons with noise",
        formula_type="algebraic",
        category_id=cats['networks'],
        source_id=sources['literature'],
        domain="mean-field",
        model_origin="mean-field"
    )

def populate_biochemistry_formulas(conn, sources, cats):
    """Add biochemistry formulas."""
    log.info("=" * 60)
    log.info("ADDING BIOCHEMISTRY FORMULAS")
    log.info("=" * 60)

    # =========================================================================
    # ENZYME KINETICS
    # =========================================================================
    log.info("-" * 40)
    log.info("Enzyme Kinetics")
    log.info("-" * 40)

    # Michaelis-Menten
    fid = add_formula(conn,
        name="Michaelis-Menten Kinetics",
        latex=r"v = \frac{V_{max} [S]}{K_m + [S]}",
        description="Classic enzyme kinetics with substrate saturation",
        formula_type="rate_equation",
        category_id=cats['enzyme'],
        source_id=sources['biomodels'],
        symbolic="V_max * S / (K_m + S)",
        python_code="v = V_max * S / (K_m + S)",
        domain="enzyme-kinetics",
        model_origin="michaelis-menten"
    )
    add_enzyme_kinetics(conn, fid, "generic enzyme", "michaelis-menten", "S", "P")

    # Michaelis-Menten substrate depletion
    add_formula(conn,
        name="Michaelis-Menten Substrate Dynamics",
        latex=r"\frac{d[S]}{dt} = -\frac{V_{max} [S]}{K_m + [S]}",
        description="Substrate consumption under Michaelis-Menten kinetics",
        formula_type="ODE",
        category_id=cats['enzyme'],
        source_id=sources['biomodels'],
        python_code="dS_dt = -V_max * S / (K_m + S)",
        domain="enzyme-kinetics",
        model_origin="michaelis-menten"
    )

    # Lineweaver-Burk
    add_formula(conn,
        name="Lineweaver-Burk Equation",
        latex=r"\frac{1}{v} = \frac{K_m}{V_{max}} \cdot \frac{1}{[S]} + \frac{1}{V_{max}}",
        description="Double-reciprocal linearization of Michaelis-Menten",
        formula_type="algebraic",
        category_id=cats['enzyme'],
        source_id=sources['biomodels'],
        python_code="inv_v = (K_m / V_max) * (1 / S) + (1 / V_max)",
        domain="enzyme-kinetics",
        model_origin="lineweaver-burk"
    )

    # Competitive inhibition
    fid = add_formula(conn,
        name="Competitive Inhibition",
        latex=r"v = \frac{V_{max} [S]}{K_m \left(1 + \frac{[I]}{K_i}\right) + [S]}",
        description="Enzyme kinetics with competitive inhibitor",
        formula_type="rate_equation",
        category_id=cats['enzyme'],
        source_id=sources['biomodels'],
        python_code="v = V_max * S / (K_m * (1 + I/K_i) + S)",
        domain="enzyme-kinetics",
        model_origin="competitive-inhibition"
    )
    add_enzyme_kinetics(conn, fid, "inhibited enzyme", "competitive", "S", "P", inhibitor="I")

    # Non-competitive inhibition
    fid = add_formula(conn,
        name="Non-competitive Inhibition",
        latex=r"v = \frac{V_{max} [S]}{(K_m + [S])\left(1 + \frac{[I]}{K_i}\right)}",
        description="Enzyme kinetics with non-competitive inhibitor",
        formula_type="rate_equation",
        category_id=cats['enzyme'],
        source_id=sources['biomodels'],
        python_code="v = V_max * S / ((K_m + S) * (1 + I/K_i))",
        domain="enzyme-kinetics",
        model_origin="non-competitive-inhibition"
    )
    add_enzyme_kinetics(conn, fid, "inhibited enzyme", "non-competitive", "S", "P", inhibitor="I")

    # Uncompetitive inhibition
    fid = add_formula(conn,
        name="Uncompetitive Inhibition",
        latex=r"v = \frac{V_{max} [S]}{K_m + [S]\left(1 + \frac{[I]}{K_i}\right)}",
        description="Enzyme kinetics with uncompetitive inhibitor",
        formula_type="rate_equation",
        category_id=cats['enzyme'],
        source_id=sources['biomodels'],
        python_code="v = V_max * S / (K_m + S * (1 + I/K_i))",
        domain="enzyme-kinetics",
        model_origin="uncompetitive-inhibition"
    )
    add_enzyme_kinetics(conn, fid, "inhibited enzyme", "uncompetitive", "S", "P", inhibitor="I")

    # Hill equation
    fid = add_formula(conn,
        name="Hill Equation",
        latex=r"v = \frac{V_{max} [S]^n}{K_{0.5}^n + [S]^n}",
        description="Cooperative binding with Hill coefficient",
        formula_type="rate_equation",
        category_id=cats['enzyme'],
        source_id=sources['biomodels'],
        symbolic="V_max * S**n / (K_half**n + S**n)",
        python_code="v = V_max * S**n / (K_half**n + S**n)",
        domain="enzyme-kinetics",
        model_origin="hill"
    )
    add_enzyme_kinetics(conn, fid, "cooperative enzyme", "hill", "S", "P", hill_coef=2.0)

    # Substrate inhibition
    fid = add_formula(conn,
        name="Substrate Inhibition",
        latex=r"v = \frac{V_{max} [S]}{K_m + [S] + \frac{[S]^2}{K_{si}}}",
        description="Enzyme kinetics with excess substrate inhibition",
        formula_type="rate_equation",
        category_id=cats['enzyme'],
        source_id=sources['biomodels'],
        python_code="v = V_max * S / (K_m + S + S**2/K_si)",
        domain="enzyme-kinetics",
        model_origin="substrate-inhibition"
    )
    add_enzyme_kinetics(conn, fid, "substrate-inhibited enzyme", "substrate-inhibition", "S", "P")

    # Bi-Bi ordered mechanism
    fid = add_formula(conn,
        name="Ordered Bi-Bi Mechanism",
        latex=r"v = \frac{V_{max} [A][B]}{K_{iA}K_B + K_B[A] + K_A[B] + [A][B]}",
        description="Two-substrate ordered sequential mechanism",
        formula_type="rate_equation",
        category_id=cats['enzyme'],
        source_id=sources['biomodels'],
        python_code="v = V_max * A * B / (K_iA * K_B + K_B * A + K_A * B + A * B)",
        domain="enzyme-kinetics",
        model_origin="ordered-bi-bi"
    )
    add_enzyme_kinetics(conn, fid, "two-substrate enzyme", "ordered-bi-bi", "A,B", "P,Q")

    # Ping-pong mechanism
    fid = add_formula(conn,
        name="Ping-Pong Bi-Bi Mechanism",
        latex=r"v = \frac{V_{max} [A][B]}{K_A[B] + K_B[A] + [A][B]}",
        description="Two-substrate ping-pong mechanism",
        formula_type="rate_equation",
        category_id=cats['enzyme'],
        source_id=sources['biomodels'],
        python_code="v = V_max * A * B / (K_A * B + K_B * A + A * B)",
        domain="enzyme-kinetics",
        model_origin="ping-pong"
    )
    add_enzyme_kinetics(conn, fid, "ping-pong enzyme", "ping-pong", "A,B", "P,Q")

    # =========================================================================
    # MASS ACTION KINETICS
    # =========================================================================
    log.info("-" * 40)
    log.info("Mass Action & Reaction Kinetics")
    log.info("-" * 40)

    # Mass action - irreversible
    add_formula(conn,
        name="Mass Action (Irreversible)",
        latex=r"v = k [A]^a [B]^b",
        description="Irreversible mass action kinetics",
        formula_type="rate_equation",
        category_id=cats['metabolic'],
        source_id=sources['biomodels'],
        python_code="v = k * A**a * B**b",
        domain="reaction-kinetics",
        model_origin="mass-action"
    )

    # Mass action - reversible
    add_formula(conn,
        name="Mass Action (Reversible)",
        latex=r"v = k_f [A][B] - k_r [C][D]",
        description="Reversible mass action kinetics",
        formula_type="rate_equation",
        category_id=cats['metabolic'],
        source_id=sources['biomodels'],
        python_code="v = k_f * A * B - k_r * C * D",
        domain="reaction-kinetics",
        model_origin="mass-action"
    )

    # Arrhenius equation
    add_formula(conn,
        name="Arrhenius Equation",
        latex=r"k = A \exp\left(-\frac{E_a}{RT}\right)",
        description="Temperature dependence of rate constants",
        formula_type="algebraic",
        category_id=cats['metabolic'],
        source_id=sources['biomodels'],
        python_code="k = A * np.exp(-E_a / (R * T))",
        domain="reaction-kinetics",
        model_origin="arrhenius"
    )

    # Q10 temperature coefficient
    add_formula(conn,
        name="Q10 Temperature Coefficient",
        latex=r"k(T) = k(T_0) Q_{10}^{(T-T_0)/10}",
        description="Temperature dependence using Q10 factor",
        formula_type="algebraic",
        category_id=cats['metabolic'],
        source_id=sources['biomodels'],
        python_code="k_T = k_T0 * Q10 ** ((T - T0) / 10)",
        domain="reaction-kinetics",
        model_origin="Q10"
    )

    # =========================================================================
    # ALLOSTERIC REGULATION
    # =========================================================================
    log.info("-" * 40)
    log.info("Allosteric Regulation")
    log.info("-" * 40)

    # MWC model
    add_formula(conn,
        name="Monod-Wyman-Changeux (MWC) Model",
        latex=r"Y = \frac{\alpha(1+\alpha)^{n-1} + Lc\alpha(1+c\alpha)^{n-1}}{(1+\alpha)^n + L(1+c\alpha)^n}",
        description="Concerted allosteric transition model",
        formula_type="algebraic",
        category_id=cats['enzyme'],
        source_id=sources['biomodels'],
        domain="enzyme-kinetics",
        model_origin="MWC",
        doi="10.1016/S0022-2836(65)80285-6",
        year=1965
    )

    # KNF model (sequential)
    add_formula(conn,
        name="KNF Sequential Model",
        latex=r"Y = \frac{[S](K_1 + 2K_1K_2[S] + 3K_1K_2K_3[S]^2 + 4K_1K_2K_3K_4[S]^3)}{4(1 + K_1[S] + K_1K_2[S]^2 + K_1K_2K_3[S]^3 + K_1K_2K_3K_4[S]^4)}",
        description="Koshland-Némethy-Filmer sequential binding model",
        formula_type="algebraic",
        category_id=cats['enzyme'],
        source_id=sources['biomodels'],
        domain="enzyme-kinetics",
        model_origin="KNF"
    )

    # =========================================================================
    # SIGNALING CASCADES
    # =========================================================================
    log.info("-" * 40)
    log.info("Cell Signaling")
    log.info("-" * 40)

    # Goldbeter-Koshland ultrasensitivity
    add_formula(conn,
        name="Goldbeter-Koshland Ultrasensitivity",
        latex=r"[W^*] = G(v_1, v_2, J_1, J_2) = \frac{2v_1 J_2}{B + \sqrt{B^2 - 4(v_2 - v_1)v_1 J_2}}",
        description="Zero-order ultrasensitivity in phosphorylation cycles",
        formula_type="algebraic",
        category_id=cats['signaling'],
        source_id=sources['biomodels'],
        domain="cell-signaling",
        model_origin="goldbeter-koshland",
        doi="10.1073/pnas.78.11.6840",
        year=1981
    )

    # MAPK cascade - first layer
    add_formula(conn,
        name="MAPK Cascade Layer 1 (MAPKKK)",
        latex=r"\frac{d[MAPKKK^*]}{dt} = \frac{k_1 [Signal][MAPKKK]}{K_{m1} + [MAPKKK]} - \frac{k_2 [MAPKKK^*]}{K_{m2} + [MAPKKK^*]}",
        description="MAPK cascade - MAPKKK activation/deactivation",
        formula_type="ODE",
        category_id=cats['signaling'],
        source_id=sources['biomodels'],
        domain="cell-signaling",
        model_origin="MAPK",
        doi="10.1016/S0955-0674(97)80066-0",
        year=1997
    )

    # Calcium dynamics - ER release
    add_formula(conn,
        name="Calcium Release from ER (IP3R)",
        latex=r"\frac{d[Ca^{2+}]_{cyt}}{dt} = v_{IP3R} m_\infty^3 h^3 ([Ca^{2+}]_{ER} - [Ca^{2+}]_{cyt})",
        description="IP3 receptor-mediated calcium release",
        formula_type="ODE",
        category_id=cats['signaling'],
        source_id=sources['biomodels'],
        domain="calcium-signaling",
        model_origin="IP3R"
    )

    # Calcium dynamics - SERCA pump
    add_formula(conn,
        name="SERCA Pump",
        latex=r"J_{SERCA} = V_{SERCA} \frac{[Ca^{2+}]_{cyt}^2}{K_{SERCA}^2 + [Ca^{2+}]_{cyt}^2}",
        description="SERCA calcium pump flux into ER",
        formula_type="algebraic",
        category_id=cats['signaling'],
        source_id=sources['biomodels'],
        python_code="J_SERCA = V_SERCA * Ca_cyt**2 / (K_SERCA**2 + Ca_cyt**2)",
        domain="calcium-signaling",
        model_origin="SERCA"
    )

def populate_gene_regulation_formulas(conn, sources, cats):
    """Add gene regulation formulas."""
    log.info("=" * 60)
    log.info("ADDING GENE REGULATION FORMULAS")
    log.info("=" * 60)

    log.info("-" * 40)
    log.info("Transcriptional Regulation")
    log.info("-" * 40)

    # Simple gene expression
    add_formula(conn,
        name="Simple Gene Expression",
        latex=r"\frac{d[P]}{dt} = k_s - k_d [P]",
        description="Basic protein synthesis and degradation",
        formula_type="ODE",
        category_id=cats['genetics'],
        source_id=sources['biomodels'],
        python_code="dP_dt = k_s - k_d * P",
        domain="gene-expression",
        model_origin="gene-expression"
    )

    # Activated transcription (Hill)
    add_formula(conn,
        name="Activated Transcription (Hill)",
        latex=r"\frac{d[mRNA]}{dt} = \beta \frac{[TF]^n}{K^n + [TF]^n} - \delta [mRNA]",
        description="Transcription activated by transcription factor",
        formula_type="ODE",
        category_id=cats['genetics'],
        source_id=sources['biomodels'],
        python_code="dmRNA_dt = beta * TF**n / (K**n + TF**n) - delta * mRNA",
        domain="gene-regulation",
        model_origin="hill-activation"
    )

    # Repressed transcription (Hill)
    add_formula(conn,
        name="Repressed Transcription (Hill)",
        latex=r"\frac{d[mRNA]}{dt} = \beta \frac{K^n}{K^n + [R]^n} - \delta [mRNA]",
        description="Transcription repressed by repressor",
        formula_type="ODE",
        category_id=cats['genetics'],
        source_id=sources['biomodels'],
        python_code="dmRNA_dt = beta * K**n / (K**n + R**n) - delta * mRNA",
        domain="gene-regulation",
        model_origin="hill-repression"
    )

    # Translation
    add_formula(conn,
        name="Translation",
        latex=r"\frac{d[P]}{dt} = k_{tl} [mRNA] - \gamma [P]",
        description="Protein translation from mRNA",
        formula_type="ODE",
        category_id=cats['genetics'],
        source_id=sources['biomodels'],
        python_code="dP_dt = k_tl * mRNA - gamma * P",
        domain="gene-expression",
        model_origin="translation"
    )

    # Repressilator - gene 1
    add_formula(conn,
        name="Repressilator Gene 1",
        latex=r"\frac{dm_1}{dt} = -m_1 + \frac{\alpha}{1 + p_3^n} + \alpha_0",
        description="Repressilator mRNA dynamics - gene 1",
        formula_type="ODE",
        category_id=cats['genetics'],
        source_id=sources['biomodels'],
        python_code="dm1_dt = -m1 + alpha / (1 + p3**n) + alpha0",
        domain="synthetic-biology",
        model_origin="repressilator",
        doi="10.1038/35002125",
        year=2000
    )

    # Toggle switch - gene 1
    add_formula(conn,
        name="Toggle Switch Gene 1",
        latex=r"\frac{du}{dt} = \frac{\alpha_1}{1 + v^\beta} - u",
        description="Genetic toggle switch - gene u dynamics",
        formula_type="ODE",
        category_id=cats['genetics'],
        source_id=sources['biomodels'],
        python_code="du_dt = alpha1 / (1 + v**beta) - u",
        domain="synthetic-biology",
        model_origin="toggle-switch",
        doi="10.1038/35002131",
        year=2000
    )

    # Toggle switch - gene 2
    add_formula(conn,
        name="Toggle Switch Gene 2",
        latex=r"\frac{dv}{dt} = \frac{\alpha_2}{1 + u^\gamma} - v",
        description="Genetic toggle switch - gene v dynamics",
        formula_type="ODE",
        category_id=cats['genetics'],
        source_id=sources['biomodels'],
        python_code="dv_dt = alpha2 / (1 + u**gamma) - v",
        domain="synthetic-biology",
        model_origin="toggle-switch"
    )

    # Autoactivation with positive feedback
    add_formula(conn,
        name="Positive Autoregulation",
        latex=r"\frac{d[X]}{dt} = \beta_0 + \beta \frac{[X]^n}{K^n + [X]^n} - \alpha [X]",
        description="Gene with positive autoregulation",
        formula_type="ODE",
        category_id=cats['genetics'],
        source_id=sources['biomodels'],
        python_code="dX_dt = beta0 + beta * X**n / (K**n + X**n) - alpha * X",
        domain="gene-regulation",
        model_origin="positive-autoregulation"
    )

    # Negative autoregulation
    add_formula(conn,
        name="Negative Autoregulation",
        latex=r"\frac{d[X]}{dt} = \beta \frac{K^n}{K^n + [X]^n} - \alpha [X]",
        description="Gene with negative autoregulation (speeds response)",
        formula_type="ODE",
        category_id=cats['genetics'],
        source_id=sources['biomodels'],
        python_code="dX_dt = beta * K**n / (K**n + X**n) - alpha * X",
        domain="gene-regulation",
        model_origin="negative-autoregulation"
    )

def populate_systems_biology_formulas(conn, sources, cats):
    """Add systems biology and population dynamics formulas."""
    log.info("=" * 60)
    log.info("ADDING SYSTEMS BIOLOGY FORMULAS")
    log.info("=" * 60)

    log.info("-" * 40)
    log.info("Population Dynamics")
    log.info("-" * 40)

    # Exponential growth
    add_formula(conn,
        name="Exponential Growth",
        latex=r"\frac{dN}{dt} = rN",
        description="Unlimited exponential population growth",
        formula_type="ODE",
        category_id=cats['population'],
        source_id=sources['literature'],
        python_code="dN_dt = r * N",
        domain="population-dynamics",
        model_origin="exponential-growth"
    )

    # Logistic growth
    add_formula(conn,
        name="Logistic Growth",
        latex=r"\frac{dN}{dt} = rN\left(1 - \frac{N}{K}\right)",
        description="Density-dependent population growth",
        formula_type="ODE",
        category_id=cats['population'],
        source_id=sources['literature'],
        python_code="dN_dt = r * N * (1 - N / K)",
        domain="population-dynamics",
        model_origin="logistic-growth"
    )

    # Lotka-Volterra predator
    add_formula(conn,
        name="Lotka-Volterra Predator",
        latex=r"\frac{dP}{dt} = -dP + \beta NP",
        description="Predator population dynamics",
        formula_type="ODE",
        category_id=cats['population'],
        source_id=sources['literature'],
        python_code="dP_dt = -d * P + beta * N * P",
        domain="ecology",
        model_origin="lotka-volterra"
    )

    # Lotka-Volterra prey
    add_formula(conn,
        name="Lotka-Volterra Prey",
        latex=r"\frac{dN}{dt} = rN - \alpha NP",
        description="Prey population dynamics",
        formula_type="ODE",
        category_id=cats['population'],
        source_id=sources['literature'],
        python_code="dN_dt = r * N - alpha * N * P",
        domain="ecology",
        model_origin="lotka-volterra"
    )

    # Competitive exclusion
    add_formula(conn,
        name="Competitive Lotka-Volterra (Species 1)",
        latex=r"\frac{dN_1}{dt} = r_1 N_1 \left(1 - \frac{N_1 + \alpha_{12} N_2}{K_1}\right)",
        description="Competition between two species - species 1",
        formula_type="ODE",
        category_id=cats['population'],
        source_id=sources['literature'],
        python_code="dN1_dt = r1 * N1 * (1 - (N1 + alpha12 * N2) / K1)",
        domain="ecology",
        model_origin="competitive-lotka-volterra"
    )

    log.info("-" * 40)
    log.info("Oscillators & Rhythms")
    log.info("-" * 40)

    # Goodwin oscillator - mRNA
    add_formula(conn,
        name="Goodwin Oscillator (mRNA)",
        latex=r"\frac{dM}{dt} = \frac{v_1 K_1^n}{K_1^n + P_n^n} - v_2 \frac{M}{K_2 + M}",
        description="Goodwin negative feedback oscillator - mRNA",
        formula_type="ODE",
        category_id=cats['systems'],
        source_id=sources['biomodels'],
        python_code="dM_dt = v1 * K1**n / (K1**n + Pn**n) - v2 * M / (K2 + M)",
        domain="circadian",
        model_origin="goodwin",
        doi="10.1016/0065-2571(65)90067-1",
        year=1965
    )

    # Van der Pol oscillator
    add_formula(conn,
        name="Van der Pol Oscillator",
        latex=r"\frac{d^2x}{dt^2} - \mu(1-x^2)\frac{dx}{dt} + x = 0",
        description="Classic relaxation oscillator",
        formula_type="ODE",
        category_id=cats['systems'],
        source_id=sources['literature'],
        domain="oscillators",
        model_origin="van-der-pol"
    )

    # Circadian PER protein
    add_formula(conn,
        name="Circadian PER Protein",
        latex=r"\frac{d[PER]}{dt} = v_s \frac{K_I^n}{K_I^n + [CN]^n} - v_m \frac{[PER]}{K_m + [PER]} - k_d [PER]",
        description="Circadian clock PER protein dynamics",
        formula_type="ODE",
        category_id=cats['systems'],
        source_id=sources['biomodels'],
        domain="circadian",
        model_origin="circadian"
    )

    log.info("-" * 40)
    log.info("Miscellaneous")
    log.info("-" * 40)

    # Nernst equation
    add_formula(conn,
        name="Nernst Equation",
        latex=r"E = \frac{RT}{zF} \ln \frac{[ion]_{out}}{[ion]_{in}}",
        description="Equilibrium potential for an ion",
        formula_type="algebraic",
        category_id=cats['neuro'],
        source_id=sources['literature'],
        python_code="E = (R * T) / (z * F) * np.log(ion_out / ion_in)",
        domain="electrophysiology",
        model_origin="nernst"
    )

    # Goldman-Hodgkin-Katz
    add_formula(conn,
        name="Goldman-Hodgkin-Katz Voltage Equation",
        latex=r"V_m = \frac{RT}{F} \ln \frac{P_K[K^+]_o + P_{Na}[Na^+]_o + P_{Cl}[Cl^-]_i}{P_K[K^+]_i + P_{Na}[Na^+]_i + P_{Cl}[Cl^-]_o}",
        description="Resting membrane potential from multiple ions",
        formula_type="algebraic",
        category_id=cats['neuro'],
        source_id=sources['literature'],
        domain="electrophysiology",
        model_origin="GHK"
    )

    # Cable equation
    add_formula(conn,
        name="Cable Equation",
        latex=r"\lambda^2 \frac{\partial^2 V}{\partial x^2} = \tau_m \frac{\partial V}{\partial t} + V",
        description="Passive signal propagation in dendrites",
        formula_type="PDE",
        category_id=cats['neurons'],
        source_id=sources['literature'],
        domain="electrophysiology",
        model_origin="cable-theory"
    )

    # Diffusion equation
    add_formula(conn,
        name="Fick's Law of Diffusion",
        latex=r"\frac{\partial C}{\partial t} = D \nabla^2 C",
        description="Concentration changes due to diffusion",
        formula_type="PDE",
        category_id=cats['systems'],
        source_id=sources['literature'],
        python_code="dC_dt = D * laplacian(C)",
        domain="diffusion",
        model_origin="fick"
    )

    # Reaction-diffusion
    add_formula(conn,
        name="Reaction-Diffusion Equation",
        latex=r"\frac{\partial u}{\partial t} = D \nabla^2 u + f(u)",
        description="Diffusion with local reaction dynamics",
        formula_type="PDE",
        category_id=cats['systems'],
        source_id=sources['literature'],
        domain="pattern-formation",
        model_origin="reaction-diffusion"
    )

    # Turing pattern - activator
    add_formula(conn,
        name="Turing Activator",
        latex=r"\frac{\partial a}{\partial t} = D_a \nabla^2 a + \rho_a \frac{a^2}{h} - \mu_a a + \rho_0",
        description="Activator in Turing pattern formation",
        formula_type="PDE",
        category_id=cats['systems'],
        source_id=sources['biomodels'],
        domain="pattern-formation",
        model_origin="turing"
    )

def populate_cognitive_formulas(conn, sources, cats):
    """Add brain-inspired cognitive computing formulas."""
    log.info("=" * 60)
    log.info("ADDING COGNITIVE COMPUTING FORMULAS")
    log.info("=" * 60)

    # Main cognitive category
    cats['cognitive'] = add_category(conn, 'Cognitive Computing', None,
        'Brain-inspired cognitive operating system formulas')

    # Subcategories
    cats['molecular'] = add_category(conn, 'Molecular/Cellular Level', cats['cognitive'],
        'Genetic encoding, gene regulation, signal integration')
    cats['dendritic'] = add_category(conn, 'Dendritic Computation', cats['cognitive'],
        'Cable equation, spike generation, temporal integration')
    cats['plasticity_cog'] = add_category(conn, 'Synaptic Plasticity', cats['cognitive'],
        'Calcium-based learning, STDP, Hebbian rules')
    cats['network_dyn'] = add_category(conn, 'Network Dynamics', cats['cognitive'],
        'Normalization, attractor dynamics, population coding')
    cats['sensory'] = add_category(conn, 'Sensory Computations', cats['cognitive'],
        'Visual, auditory, somatosensory processing')
    cats['working_mem'] = add_category(conn, 'Working Memory & Decision', cats['cognitive'],
        'Decision making, reinforcement learning, strategy selection')
    cats['language'] = add_category(conn, 'Language & Cognition', cats['cognitive'],
        'Language parsing, semantic composition, inference')
    cats['motivation'] = add_category(conn, 'Motivation & Action', cats['cognitive'],
        'Reward prediction, threat evaluation, action selection')
    cats['inference'] = add_category(conn, 'Probabilistic Inference', cats['cognitive'],
        'Bayesian inference, Kalman filtering, belief propagation')
    cats['optimization_cog'] = add_category(conn, 'Optimization', cats['cognitive'],
        'Gradient descent, tensor operations, graph propagation')

    log.info("-" * 40)
    log.info("Molecular/Cellular Level")
    log.info("-" * 40)

    # Transcription rate
    add_formula(conn,
        name="Transcription Rate",
        latex=r"\frac{dR}{dt} = \frac{k_{tx} [TF]^n}{K_d^n + [TF]^n} - \gamma_R R",
        description="Transcription rate with Hill coefficient",
        formula_type="ODE",
        category_id=cats['molecular'],
        source_id=sources['literature'],
        python_code="dR_dt = (k_tx * TF**n / (K_d**n + TF**n)) - gamma_R * R",
        domain="molecular-cellular"
    )

    # Translation rate
    add_formula(conn,
        name="Translation Rate",
        latex=r"\frac{dP}{dt} = k_{tl} R - \gamma_P P",
        description="Protein translation rate from mRNA",
        formula_type="ODE",
        category_id=cats['molecular'],
        source_id=sources['literature'],
        python_code="dP_dt = k_tl * R - gamma_P * P",
        domain="molecular-cellular"
    )

    # Hill equation
    add_formula(conn,
        name="Hill Equation (Gene Regulation)",
        latex=r"Output = \frac{V_{max} [Input]^n}{K^n + [Input]^n}",
        description="Gene regulatory output with Hill coefficient",
        formula_type="algebraic",
        category_id=cats['molecular'],
        source_id=sources['literature'],
        python_code="output = V_max * (Input**n) / (K**n + Input**n)",
        domain="molecular-cellular"
    )

    # Repressilator
    add_formula(conn,
        name="Repressilator",
        latex=r"\frac{dx_i}{dt} = \frac{\alpha}{1 + x_j^n} - x_i",
        description="Repressilator genetic oscillator dynamics",
        formula_type="ODE",
        category_id=cats['molecular'],
        source_id=sources['literature'],
        python_code="dx_dt = alpha / (1 + x_j**n) - x",
        domain="molecular-cellular"
    )

    # Linear summation
    add_formula(conn,
        name="Linear Signal Summation",
        latex=r"S = \sum w_i I_i",
        description="Linear summation of weighted inputs",
        formula_type="algebraic",
        category_id=cats['molecular'],
        source_id=sources['literature'],
        python_code="S = sum(w[i] * I[i] for i in range(n))",
        domain="molecular-cellular"
    )

    # Michaelis-Menten (repeated for context)
    add_formula(conn,
        name="Michaelis-Menten Kinetics (Cognitive Context)",
        latex=r"v = \frac{V_{max} [S]}{K_m + [S]}",
        description="Enzyme kinetics in protein-protein interactions",
        formula_type="rate_equation",
        category_id=cats['molecular'],
        source_id=sources['literature'],
        python_code="v = V_max * S / (K_m + S)",
        domain="molecular-cellular"
    )

    log.info("-" * 40)
    log.info("Dendritic Level")
    log.info("-" * 40)

    # Cable equation
    add_formula(conn,
        name="Cable Equation (Dendrite)",
        latex=r"\lambda^2 \frac{\partial^2 V}{\partial x^2} = \tau \frac{\partial V}{\partial t} + V - V_{rest}",
        description="Passive signal propagation in dendrites",
        formula_type="PDE",
        category_id=cats['dendritic'],
        source_id=sources['literature'],
        domain="dendritic-computation"
    )

    # Compartmental model
    add_formula(conn,
        name="Compartmental Membrane Equation",
        latex=r"C \frac{dV_i}{dt} = \sum(g_{ij}(V_j - V_i)) + I_{syn} - I_{leak}",
        description="Compartmental neuron model with coupled segments",
        formula_type="ODE",
        category_id=cats['dendritic'],
        source_id=sources['literature'],
        python_code="dV_dt = (sum(g[i,j]*(V[j]-V[i]) for j) + I_syn - I_leak) / C",
        domain="dendritic-computation"
    )

    # Integrate-and-fire
    add_formula(conn,
        name="Integrate-and-Fire",
        latex=r"\tau \frac{dV}{dt} = -(V - V_{rest}) + R I",
        description="Simple neuron model: integrate input, fire when threshold crossed",
        formula_type="ODE",
        category_id=cats['dendritic'],
        source_id=sources['literature'],
        python_code="dV_dt = (-(V - V_rest) + R * I) / tau",
        domain="dendritic-computation"
    )

    # Exponential decay
    add_formula(conn,
        name="Exponential Decay (Temporal Integration)",
        latex=r"V(t) = V_0 \exp(-t/\tau)",
        description="Exponential decay of voltage over time",
        formula_type="algebraic",
        category_id=cats['dendritic'],
        source_id=sources['literature'],
        python_code="V = V_0 * np.exp(-t / tau)",
        domain="dendritic-computation"
    )

    # Leaky integration
    add_formula(conn,
        name="Leaky Integration",
        latex=r"V(t) = (R I)(1 - \exp(-t/\tau))",
        description="Leaky temporal integration of input",
        formula_type="algebraic",
        category_id=cats['dendritic'],
        source_id=sources['literature'],
        python_code="V = (R * I) * (1 - np.exp(-t / tau))",
        domain="dendritic-computation"
    )

    # AND gate
    add_formula(conn,
        name="Coincidence Detection (AND Gate)",
        latex=r"Output = 1 \text{ if } (|t_1 - t_2| < \Delta t_{window})",
        description="Detect synchronous input from multiple sources",
        formula_type="boolean",
        category_id=cats['dendritic'],
        source_id=sources['literature'],
        python_code="output = 1 if abs(t1 - t2) < dt_window else 0",
        domain="dendritic-computation"
    )

    # NMDA voltage dependence
    add_formula(conn,
        name="NMDA Voltage Dependence",
        latex=r"g = \frac{g_{max}}{1 + [Mg^{2+}] \exp(-0.062 V)/3.57}",
        description="Voltage-dependent Mg2+ block of NMDA receptors",
        formula_type="algebraic",
        category_id=cats['dendritic'],
        source_id=sources['literature'],
        python_code="g = g_max / (1 + (Mg / 3.57) * np.exp(-0.062 * V))",
        domain="dendritic-computation"
    )

    log.info("-" * 40)
    log.info("Synaptic Plasticity (Cognitive)")
    log.info("-" * 40)

    # BCM rule
    add_formula(conn,
        name="BCM Learning Rule",
        latex=r"\frac{dw}{dt} = \eta y (y - \theta) x",
        description="Bienenstock-Cooper-Munro rule with sliding threshold",
        formula_type="ODE",
        category_id=cats['plasticity_cog'],
        source_id=sources['literature'],
        python_code="dw_dt = eta * y * (y - theta) * x",
        domain="synaptic-plasticity",
        doi="10.1523/JNEUROSCI.02-01-00032.1982",
        year=1982
    )

    # BCM threshold
    add_formula(conn,
        name="BCM Threshold",
        latex=r"\theta = \langle y^2 \rangle",
        description="Sliding modification threshold in BCM rule",
        formula_type="algebraic",
        category_id=cats['plasticity_cog'],
        source_id=sources['literature'],
        python_code="theta = mean(y**2)",
        domain="synaptic-plasticity"
    )

    # Hebbian
    add_formula(conn,
        name="Hebbian Learning",
        latex=r"\Delta w = \eta x y",
        description="Basic Hebbian learning rule",
        formula_type="plasticity_rule",
        category_id=cats['plasticity_cog'],
        source_id=sources['literature'],
        python_code="dw = eta * x * y",
        domain="synaptic-plasticity"
    )

    # Covariance
    add_formula(conn,
        name="Covariance Learning",
        latex=r"\Delta w = \eta (x - \langle x \rangle)(y - \langle y \rangle)",
        description="Covariance-based Hebbian rule",
        formula_type="plasticity_rule",
        category_id=cats['plasticity_cog'],
        source_id=sources['literature'],
        python_code="dw = eta * (x - mean_x) * (y - mean_y)",
        domain="synaptic-plasticity"
    )

    # Oja's rule
    add_formula(conn,
        name="Oja's Learning Rule (Cognitive)",
        latex=r"\Delta w = \eta y (x - w y)",
        description="Hebbian rule with weight normalization (PCA)",
        formula_type="plasticity_rule",
        category_id=cats['plasticity_cog'],
        source_id=sources['literature'],
        python_code="dw = eta * y * (x - w * y)",
        domain="synaptic-plasticity"
    )

    # STDP
    fid = add_formula(conn,
        name="Spike-Timing Dependent Plasticity (STDP)",
        latex=r"\Delta w(\Delta t) = \begin{cases} A_+ \exp(-\Delta t/\tau_+) & \text{if } \Delta t > 0 \\ -A_- \exp(\Delta t/\tau_-) & \text{if } \Delta t < 0 \end{cases}",
        description="STDP: potentiation if presynaptic fires before postsynaptic",
        formula_type="plasticity_rule",
        category_id=cats['plasticity_cog'],
        source_id=sources['literature'],
        python_code="dw = A_plus * np.exp(-dt/tau_plus) if dt > 0 else -A_minus * np.exp(dt/tau_minus)",
        domain="synaptic-plasticity",
        doi="10.1523/JNEUROSCI.18-24-10464.1998",
        year=1998
    )
    add_plasticity_rule(conn, fid, "STDP", 20.0, 20.0, 0.005, "additive", False)

    # Triplet STDP
    add_formula(conn,
        name="Triplet STDP",
        latex=r"\Delta w = r_1(t)(A_2^+ + A_3^+ r_2(t-\epsilon)) - o_1(t)(A_2^- + A_3^- o_2(t-\epsilon))",
        description="Triplet STDP capturing frequency dependence",
        formula_type="plasticity_rule",
        category_id=cats['plasticity_cog'],
        source_id=sources['literature'],
        domain="synaptic-plasticity"
    )

    # Short-term depression
    add_formula(conn,
        name="Short-Term Depression",
        latex=r"\frac{dx}{dt} = \frac{1-x}{\tau_{rec}}",
        description="Resource depletion in short-term plasticity",
        formula_type="ODE",
        category_id=cats['plasticity_cog'],
        source_id=sources['literature'],
        python_code="dx_dt = (1 - x) / tau_rec",
        domain="synaptic-plasticity"
    )

    # Short-term facilitation
    add_formula(conn,
        name="Short-Term Facilitation",
        latex=r"\frac{du}{dt} = \frac{U-u}{\tau_{fac}}",
        description="Increased release probability in short-term plasticity",
        formula_type="ODE",
        category_id=cats['plasticity_cog'],
        source_id=sources['literature'],
        python_code="du_dt = (U - u) / tau_fac",
        domain="synaptic-plasticity"
    )

    log.info("-" * 40)
    log.info("Network Dynamics")
    log.info("-" * 40)

    # Softmax
    add_formula(conn,
        name="Softmax Normalization",
        latex=r"y_i = \frac{\exp(x_i)}{\sum_j \exp(x_j)}",
        description="Probability distribution from scores",
        formula_type="algebraic",
        category_id=cats['network_dyn'],
        source_id=sources['literature'],
        python_code="y = np.exp(x) / np.sum(np.exp(x))",
        domain="network-dynamics"
    )

    # Divisive normalization
    add_formula(conn,
        name="Divisive Normalization",
        latex=r"y_i = \frac{x_i}{\sigma + \sum_j x_j}",
        description="Divisive inhibition for gain control",
        formula_type="algebraic",
        category_id=cats['network_dyn'],
        source_id=sources['literature'],
        python_code="y = x / (sigma + np.sum(x))",
        domain="network-dynamics"
    )

    # Hopfield energy
    add_formula(conn,
        name="Hopfield Network Energy",
        latex=r"E = -\frac{1}{2} \sum_{ij} w_{ij} s_i s_j - \sum_i \theta_i s_i",
        description="Energy function for Hopfield attractor networks",
        formula_type="algebraic",
        category_id=cats['network_dyn'],
        source_id=sources['literature'],
        python_code="E = -0.5 * np.dot(s, np.dot(w, s)) - np.dot(theta, s)",
        domain="network-dynamics"
    )

    # Population vector
    add_formula(conn,
        name="Population Vector Decoding",
        latex=r"v_{pop} = \frac{\sum_i r_i d_i}{\sum_i r_i}",
        description="Decode stimulus from population response",
        formula_type="algebraic",
        category_id=cats['network_dyn'],
        source_id=sources['literature'],
        python_code="v_pop = np.sum(r * d) / np.sum(r)",
        domain="network-dynamics"
    )

    # Fisher information
    add_formula(conn,
        name="Fisher Information (Population Coding)",
        latex=r"I(s) = \sum_i \frac{[df_i/ds]^2}{f_i(s)}",
        description="Information encoded by neural population",
        formula_type="algebraic",
        category_id=cats['network_dyn'],
        source_id=sources['literature'],
        domain="network-dynamics"
    )

    # PCA
    add_formula(conn,
        name="Principal Component Analysis",
        latex=r"x_{reduced} = W^T (x - \mu)",
        description="Dimensionality reduction via PCA",
        formula_type="algebraic",
        category_id=cats['network_dyn'],
        source_id=sources['literature'],
        python_code="x_red = np.dot(W.T, x - mu)",
        domain="network-dynamics"
    )

    # Sparse coding
    add_formula(conn,
        name="Sparse Coding",
        latex=r"minimize ||x - W s||^2 + \lambda ||s||_1",
        description="Sparse representation learning",
        formula_type="optimization",
        category_id=cats['network_dyn'],
        source_id=sources['literature'],
        python_code="minimize squared_error(x, W @ s) + lambda * L1_norm(s)",
        domain="network-dynamics"
    )

    # Pattern completion
    add_formula(conn,
        name="Pattern Completion (Autoassociative)",
        latex=r"y = Wx",
        description="Retrieve full pattern from partial cue",
        formula_type="algebraic",
        category_id=cats['network_dyn'],
        source_id=sources['literature'],
        python_code="y = np.dot(W, x)",
        domain="network-dynamics"
    )

    # Recurrent RNN
    add_formula(conn,
        name="Recurrent Neural Network",
        latex=r"\tau \frac{dy}{dt} = -y + f(W_{rec} y + W_{in} x + b)",
        description="Continuous recurrent neural network dynamics",
        formula_type="ODE",
        category_id=cats['network_dyn'],
        source_id=sources['literature'],
        python_code="dy_dt = (-y + f(W_rec @ y + W_in @ x + b)) / tau",
        domain="network-dynamics"
    )

    # LSTM forget gate
    add_formula(conn,
        name="LSTM Forget Gate",
        latex=r"f_t = \sigma(W_f [h_{t-1}, x_t] + b_f)",
        description="LSTM forget gate dynamics",
        formula_type="algebraic",
        category_id=cats['network_dyn'],
        source_id=sources['literature'],
        python_code="f_t = sigmoid(W_f @ np.hstack([h_prev, x]) + b_f)",
        domain="network-dynamics"
    )

    # LSTM input gate
    add_formula(conn,
        name="LSTM Input Gate",
        latex=r"i_t = \sigma(W_i [h_{t-1}, x_t] + b_i)",
        description="LSTM input gate dynamics",
        formula_type="algebraic",
        category_id=cats['network_dyn'],
        source_id=sources['literature'],
        python_code="i_t = sigmoid(W_i @ np.hstack([h_prev, x]) + b_i)",
        domain="network-dynamics"
    )

    # LSTM cell state
    add_formula(conn,
        name="LSTM Cell State",
        latex=r"C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t",
        description="LSTM cell state update",
        formula_type="algebraic",
        category_id=cats['network_dyn'],
        source_id=sources['literature'],
        python_code="C_t = f_t * C_prev + i_t * C_tilde",
        domain="network-dynamics"
    )

    # Phase oscillator
    add_formula(conn,
        name="Phase Oscillator",
        latex=r"\frac{d\theta}{dt} = \omega + K \sin(\theta_j - \theta_i)",
        description="Coupled phase oscillators for synchronization",
        formula_type="ODE",
        category_id=cats['network_dyn'],
        source_id=sources['literature'],
        python_code="dtheta_dt = omega + K * np.sin(theta_j - theta)",
        domain="network-dynamics"
    )

    # Wilson-Cowan
    add_formula(conn,
        name="Wilson-Cowan Equations",
        latex=r"\tau_E \frac{dE}{dt} = -E + f_E(w_{EE}E - w_{EI}I + I_{ext})",
        description="Population rate model with excitation/inhibition",
        formula_type="ODE",
        category_id=cats['network_dyn'],
        source_id=sources['literature'],
        python_code="dE_dt = (-E + f_E(w_EE*E - w_EI*I + I_ext)) / tau_E",
        domain="network-dynamics"
    )

    # Predictive coding
    add_formula(conn,
        name="Predictive Coding Hierarchy",
        latex=r"\mu_l = f(\mu_{l+1})",
        description="Hierarchical prediction in predictive coding",
        formula_type="algebraic",
        category_id=cats['network_dyn'],
        source_id=sources['literature'],
        python_code="mu_l = f(mu_next)",
        domain="network-dynamics"
    )

    # Prediction error
    add_formula(conn,
        name="Prediction Error (Predictive Coding)",
        latex=r"\varepsilon_l = x_l - \mu_l",
        description="Mismatch between observation and prediction",
        formula_type="algebraic",
        category_id=cats['network_dyn'],
        source_id=sources['literature'],
        python_code="epsilon = x - mu",
        domain="network-dynamics"
    )

    log.info("-" * 40)
    log.info("Sensory Computations")
    log.info("-" * 40)

    # Convolution
    add_formula(conn,
        name="Convolutional Filtering (V1)",
        latex=r"r(x,y) = \sum_{ij} w(i,j) I(x+i, y+j)",
        description="Receptive field computation via convolution",
        formula_type="algebraic",
        category_id=cats['sensory'],
        source_id=sources['literature'],
        python_code="r = convolve2d(I, w)",
        domain="sensory-computation"
    )

    # Gabor filter
    add_formula(conn,
        name="Gabor Filter",
        latex=r"G(x,y) = \exp(-(x'^2 + \gamma^2 y'^2)/(2\sigma^2)) \cos(2\pi x'/\lambda + \psi)",
        description="Oriented frequency-selective filter",
        formula_type="algebraic",
        category_id=cats['sensory'],
        source_id=sources['literature'],
        domain="sensory-computation"
    )

    # Edge detection
    add_formula(conn,
        name="Edge Detection (Sensory)",
        latex=r"I_{edge} = [\partial I/\partial x, \partial I/\partial y]",
        description="Spatial gradient for edge detection",
        formula_type="algebraic",
        category_id=cats['sensory'],
        source_id=sources['literature'],
        python_code="I_edge = np.gradient(I)",
        domain="sensory-computation"
    )

    # Complex cell
    add_formula(conn,
        name="Complex Cell Response",
        latex=r"C = \sqrt{S_{even}^2 + S_{odd}^2}",
        description="Orientation-selective response with phase invariance",
        formula_type="algebraic",
        category_id=cats['sensory'],
        source_id=sources['literature'],
        python_code="C = np.sqrt(S_even**2 + S_odd**2)",
        domain="sensory-computation"
    )

    # Cochlear filterbank
    add_formula(conn,
        name="Cochlear Filterbank",
        latex=r"H_i(f) = \frac{(f/f_i)^p}{(f/f_i)^p + q}",
        description="Frequency analysis in auditory system",
        formula_type="algebraic",
        category_id=cats['sensory'],
        source_id=sources['literature'],
        domain="sensory-computation"
    )

    # Gammatone filter
    add_formula(conn,
        name="Gammatone Filter",
        latex=r"g(t) = t^{n-1} \exp(-2\pi b t) \cos(2\pi f_c t + \phi)",
        description="Auditory filter approximation",
        formula_type="algebraic",
        category_id=cats['sensory'],
        source_id=sources['literature'],
        domain="sensory-computation"
    )

    log.info("-" * 40)
    log.info("Working Memory & Decision Making")
    log.info("-" * 40)

    # Working memory maintenance
    add_formula(conn,
        name="Working Memory Maintenance",
        latex=r"\tau \frac{dx}{dt} = -x + f(W x + I_{input})",
        description="Persistent activity for working memory",
        formula_type="ODE",
        category_id=cats['working_mem'],
        source_id=sources['literature'],
        python_code="dx_dt = (-x + f(W @ x + I)) / tau",
        domain="working-memory"
    )

    # Working memory gating
    add_formula(conn,
        name="Working Memory Gating",
        latex=r"x_{new} = g x_{input} + (1-g) x_{old}",
        description="Gate for updating working memory",
        formula_type="algebraic",
        category_id=cats['working_mem'],
        source_id=sources['literature'],
        python_code="x_new = g * x_in + (1 - g) * x_old",
        domain="working-memory"
    )

    # Drift-diffusion
    add_formula(conn,
        name="Drift-Diffusion Model",
        latex=r"\frac{dx}{dt} = \mu I + \sigma \xi(t)",
        description="Decision variable accumulation with noise",
        formula_type="SDE",
        category_id=cats['working_mem'],
        source_id=sources['literature'],
        python_code="dx_dt = mu * I + sigma * noise",
        domain="decision-making"
    )

    # Race model
    add_formula(conn,
        name="Race Model (Decision)",
        latex=r"\frac{dx_i}{dt} = I_i + noise",
        description="Competing accumulators for decision",
        formula_type="ODE",
        category_id=cats['working_mem'],
        source_id=sources['literature'],
        python_code="dx_dt = I + np.random.normal()",
        domain="decision-making"
    )

    # Q-learning
    add_formula(conn,
        name="Q-Learning",
        latex=r"Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma \max_a' Q(s',a') - Q(s,a)]",
        description="Value-based reinforcement learning",
        formula_type="update_rule",
        category_id=cats['working_mem'],
        source_id=sources['literature'],
        python_code="Q[s,a] = Q[s,a] + alpha * (r + gamma * max(Q[s_next]) - Q[s,a])",
        domain="reinforcement-learning"
    )

    # SARSA
    add_formula(conn,
        name="SARSA Algorithm",
        latex=r"Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma Q(s',a') - Q(s,a)]",
        description="On-policy temporal difference learning",
        formula_type="update_rule",
        category_id=cats['working_mem'],
        source_id=sources['literature'],
        python_code="Q[s,a] = Q[s,a] + alpha * (r + gamma * Q[s_next,a_next] - Q[s,a])",
        domain="reinforcement-learning"
    )

    # Actor-Critic TD error
    add_formula(conn,
        name="Actor-Critic TD Error",
        latex=r"\delta = r + \gamma V(s') - V(s)",
        description="Temporal difference error for actor-critic",
        formula_type="algebraic",
        category_id=cats['working_mem'],
        source_id=sources['literature'],
        python_code="delta = r + gamma * V[s_next] - V[s]",
        domain="reinforcement-learning"
    )

    # Value function
    add_formula(conn,
        name="Value Function",
        latex=r"V(s) = E[\sum \gamma^t r_t | s_0 = s]",
        description="Expected discounted future reward",
        formula_type="algebraic",
        category_id=cats['working_mem'],
        source_id=sources['literature'],
        domain="reinforcement-learning"
    )

    # Softmax policy
    add_formula(conn,
        name="Softmax Policy (Boltzmann)",
        latex=r"P(a|s) = \frac{\exp(Q(s,a)/\tau)}{\sum_a' \exp(Q(s,a')/\tau)}",
        description="Stochastic action selection from Q-values",
        formula_type="algebraic",
        category_id=cats['working_mem'],
        source_id=sources['literature'],
        python_code="p = np.exp(Q / tau) / np.sum(np.exp(Q / tau))",
        domain="reinforcement-learning"
    )

    # Confidence computation
    add_formula(conn,
        name="Bayesian Confidence",
        latex=r"confidence \propto P(hypothesis|data)",
        description="Confidence from posterior probability",
        formula_type="algebraic",
        category_id=cats['working_mem'],
        source_id=sources['literature'],
        domain="decision-making"
    )

    log.info("-" * 40)
    log.info("Language & Cognition")
    log.info("-" * 40)

    # Shift-reduce parsing
    add_formula(conn,
        name="Shift-Reduce Parser",
        latex=r"\text{If } A \to BC \text{ matches: reduce}(B,C) \to A; \text{ Else: shift}",
        description="Syntactic parsing rule",
        formula_type="algorithm",
        category_id=cats['language'],
        source_id=sources['literature'],
        domain="language-parsing"
    )

    # Vector addition composition
    add_formula(conn,
        name="Vector Composition (Addition)",
        latex=r"v_{phrase} = v_1 + v_2",
        description="Simple additive semantic composition",
        formula_type="algebraic",
        category_id=cats['language'],
        source_id=sources['literature'],
        python_code="v_phrase = v1 + v2",
        domain="semantic-composition"
    )

    # Tensor product
    add_formula(conn,
        name="Tensor Product Composition",
        latex=r"T_{phrase} = v_1 \otimes v_2",
        description="Tensor product for structured composition",
        formula_type="algebraic",
        category_id=cats['language'],
        source_id=sources['literature'],
        python_code="T = np.outer(v1, v2)",
        domain="semantic-composition"
    )

    # Circular convolution
    add_formula(conn,
        name="Circular Convolution",
        latex=r"v_1 \star v_2 = \mathcal{F}^{-1}(\mathcal{F}(v_1) \cdot \mathcal{F}(v_2))",
        description="Bind vectors for structured representation",
        formula_type="algebraic",
        category_id=cats['language'],
        source_id=sources['literature'],
        domain="semantic-composition"
    )

    # Analogy
    add_formula(conn,
        name="Proportional Analogy",
        latex=r"a : b :: c : ? \rightarrow d = b - a + c",
        description="Solve analogy relations",
        formula_type="algebraic",
        category_id=cats['language'],
        source_id=sources['literature'],
        python_code="d = b - a + c",
        domain="semantic-composition"
    )

    # Modus ponens
    add_formula(conn,
        name="Modus Ponens",
        latex=r"(A \to B) \land A \Rightarrow B",
        description="Logical inference rule",
        formula_type="logic",
        category_id=cats['language'],
        source_id=sources['literature'],
        domain="logical-inference"
    )

    log.info("-" * 40)
    log.info("Motivation & Action")
    log.info("-" * 40)

    # TD error (dopamine)
    add_formula(conn,
        name="Temporal Difference Error",
        latex=r"\delta(t) = r(t) + \gamma V(s_{t+1}) - V(s_t)",
        description="Reward prediction error (dopamine signal)",
        formula_type="algebraic",
        category_id=cats['motivation'],
        source_id=sources['literature'],
        python_code="delta = r + gamma * V_next - V",
        domain="reward-prediction",
        doi="10.1016/0166-2236(93)90090-C",
        year=1993
    )

    # Threat evaluation
    add_formula(conn,
        name="Threat-Based Urgency",
        latex=r"Risk = P(threat) \cdot magnitude(harm)",
        description="Threat evaluation for action urgency",
        formula_type="algebraic",
        category_id=cats['motivation'],
        source_id=sources['literature'],
        python_code="risk = p_threat * harm_magnitude",
        domain="motivation"
    )

    # Temporal discounting
    add_formula(conn,
        name="Temporal Discounting (Hyperbolic)",
        latex=r"V(t) = \frac{V_0}{1 + kt}",
        description="Value decrease over time",
        formula_type="algebraic",
        category_id=cats['motivation'],
        source_id=sources['literature'],
        python_code="V = V_0 / (1 + k * t)",
        domain="motivation"
    )

    # Expected value
    add_formula(conn,
        name="Expected Value",
        latex=r"EV = \sum P(outcome_i) \cdot value(outcome_i)",
        description="Expected value computation",
        formula_type="algebraic",
        category_id=cats['motivation'],
        source_id=sources['literature'],
        python_code="EV = sum(p[i] * v[i] for i)",
        domain="motivation"
    )

    # Action-value
    add_formula(conn,
        name="Action-Value Function",
        latex=r"Q(s,a) = E[R | s,a]",
        description="Expected return for action in state",
        formula_type="algebraic",
        category_id=cats['motivation'],
        source_id=sources['literature'],
        domain="action-selection"
    )

    # Habit learning
    add_formula(conn,
        name="Habit Formation (Model-Free)",
        latex=r"Q_{MF}(s,a) \leftarrow Q_{MF} + \alpha \delta",
        description="Habitual action values from TD learning",
        formula_type="update_rule",
        category_id=cats['motivation'],
        source_id=sources['literature'],
        domain="learning"
    )

    # Model-based value
    add_formula(conn,
        name="Model-Based Value",
        latex=r"Q_{MB}(s,a) = \sum P(s'|s,a) \max_a' Q(s',a')",
        description="Goal-directed planning-based value",
        formula_type="algebraic",
        category_id=cats['motivation'],
        source_id=sources['literature'],
        python_code="Q_MB = sum(p_trans * max_Q_next)",
        domain="planning"
    )

    log.info("-" * 40)
    log.info("Probabilistic Inference")
    log.info("-" * 40)

    # Bayes rule
    add_formula(conn,
        name="Bayes' Rule",
        latex=r"P(\theta|D) = \frac{P(D|\theta) P(\theta)}{P(D)}",
        description="Posterior from likelihood and prior",
        formula_type="algebraic",
        category_id=cats['inference'],
        source_id=sources['literature'],
        python_code="posterior = likelihood * prior / evidence",
        domain="bayesian-inference"
    )

    # Log odds
    add_formula(conn,
        name="Log Odds Update",
        latex=r"\log\frac{P(A|D)}{P(\neg A|D)} = \log\frac{P(D|A)}{P(D|\neg A)} + \log\frac{P(A)}{P(\neg A)}",
        description="Logarithmic odds update rule",
        formula_type="algebraic",
        category_id=cats['inference'],
        source_id=sources['literature'],
        domain="bayesian-inference"
    )

    # Kalman predict
    add_formula(conn,
        name="Kalman Filter: Predict",
        latex=r"\hat{x}_{t|t-1} = F \hat{x}_{t-1|t-1}, P_{t|t-1} = F P_{t-1|t-1} F^T + Q",
        description="Kalman filter prediction step",
        formula_type="algebraic",
        category_id=cats['inference'],
        source_id=sources['literature'],
        domain="filtering"
    )

    # Kalman update
    add_formula(conn,
        name="Kalman Filter: Update",
        latex=r"K_t = P_{t|t-1} H^T (H P_{t|t-1} H^T + R)^{-1}",
        description="Kalman gain computation",
        formula_type="algebraic",
        category_id=cats['inference'],
        source_id=sources['literature'],
        domain="filtering"
    )

    # Belief propagation
    add_formula(conn,
        name="Belief Propagation (Sum-Product)",
        latex=r"m_{ij}(x_j) = \sum_{x_i} \psi(x_i,x_j) \phi(x_i) \prod_{k \in N(i)\j} m_{ki}(x_i)",
        description="Message passing for probabilistic inference",
        formula_type="algorithm",
        category_id=cats['inference'],
        source_id=sources['literature'],
        domain="graphical-models"
    )

    # Max-product
    add_formula(conn,
        name="Max-Product Algorithm",
        latex=r"m_{ij}(x_j) = \max_{x_i} \psi(x_i,x_j) \phi(x_i) \prod_{k \in N(i)\j} m_{ki}(x_i)",
        description="Max-product (Viterbi) for MAP inference",
        formula_type="algorithm",
        category_id=cats['inference'],
        source_id=sources['literature'],
        domain="graphical-models"
    )

    log.info("-" * 40)
    log.info("Optimization")
    log.info("-" * 40)

    # Gradient descent
    add_formula(conn,
        name="Gradient Descent",
        latex=r"\theta \leftarrow \theta - \eta \nabla L(\theta)",
        description="Basic gradient descent update",
        formula_type="update_rule",
        category_id=cats['optimization_cog'],
        source_id=sources['literature'],
        python_code="theta = theta - eta * gradient",
        domain="optimization"
    )

    # SGD with momentum
    add_formula(conn,
        name="SGD with Momentum",
        latex=r"v \leftarrow \beta v + \nabla L, \theta \leftarrow \theta - \eta v",
        description="Stochastic gradient descent with momentum",
        formula_type="update_rule",
        category_id=cats['optimization_cog'],
        source_id=sources['literature'],
        python_code="v = beta * v + grad; theta = theta - eta * v",
        domain="optimization"
    )

    # Adam optimizer first moment
    add_formula(conn,
        name="Adam: First Moment",
        latex=r"m \leftarrow \beta_1 m + (1-\beta_1) \nabla L",
        description="Adam exponential moving average of gradients",
        formula_type="update_rule",
        category_id=cats['optimization_cog'],
        source_id=sources['literature'],
        domain="optimization"
    )

    # Adam optimizer second moment
    add_formula(conn,
        name="Adam: Second Moment",
        latex=r"v \leftarrow \beta_2 v + (1-\beta_2) (\nabla L)^2",
        description="Adam exponential moving average of squared gradients",
        formula_type="update_rule",
        category_id=cats['optimization_cog'],
        source_id=sources['literature'],
        domain="optimization"
    )

    # RMSprop
    add_formula(conn,
        name="RMSprop Optimizer",
        latex=r"E[g^2]_t = \beta E[g^2]_{t-1} + (1-\beta) g_t^2, \theta \leftarrow \theta - \eta g_t/\sqrt{E[g^2]_t + \epsilon}",
        description="Root mean square propagation optimizer",
        formula_type="update_rule",
        category_id=cats['optimization_cog'],
        source_id=sources['literature'],
        domain="optimization"
    )

    # Matrix multiply
    add_formula(conn,
        name="Matrix Multiplication",
        latex=r"C_{ij} = \sum_k A_{ik} B_{kj}",
        description="Bilinear tensor contraction",
        formula_type="algebraic",
        category_id=cats['optimization_cog'],
        source_id=sources['literature'],
        python_code="C = np.dot(A, B)",
        domain="tensor-operations"
    )

    # GCN layer
    add_formula(conn,
        name="Graph Convolutional Layer",
        latex=r"H^{(l+1)} = \sigma(D^{-1/2} A D^{-1/2} H^{(l)} W^{(l)})",
        description="Graph convolution for relational data",
        formula_type="algebraic",
        category_id=cats['optimization_cog'],
        source_id=sources['literature'],
        domain="graph-neural-networks"
    )

    # Graph attention
    add_formula(conn,
        name="Graph Attention",
        latex=r"\alpha_{ij} = softmax(LeakyReLU(a^T[W h_i || W h_j]))",
        description="Attention mechanism for graphs",
        formula_type="algebraic",
        category_id=cats['optimization_cog'],
        source_id=sources['literature'],
        domain="graph-neural-networks"
    )

    # Fuzzy AND
    add_formula(conn,
        name="Fuzzy Logic AND",
        latex=r"\mu_{AND} = \min(\mu_A, \mu_B)",
        description="Min t-norm for fuzzy AND",
        formula_type="algebraic",
        category_id=cats['optimization_cog'],
        source_id=sources['literature'],
        python_code="fuzzy_and = min(mu_A, mu_B)",
        domain="fuzzy-logic"
    )

    # Fuzzy OR
    add_formula(conn,
        name="Fuzzy Logic OR",
        latex=r"\mu_{OR} = \max(\mu_A, \mu_B)",
        description="Max t-conorm for fuzzy OR",
        formula_type="algebraic",
        category_id=cats['optimization_cog'],
        source_id=sources['literature'],
        python_code="fuzzy_or = max(mu_A, mu_B)",
        domain="fuzzy-logic"
    )

    # EM algorithm E-step
    add_formula(conn,
        name="EM Algorithm: E-Step",
        latex=r"Q(\theta|\theta_{old}) = E_Z[\log P(X,Z|\theta) | X, \theta_{old}]",
        description="Expectation step of EM algorithm",
        formula_type="algorithm",
        category_id=cats['optimization_cog'],
        source_id=sources['literature'],
        domain="unsupervised-learning"
    )

    # VAE encoder
    add_formula(conn,
        name="VAE Encoder",
        latex=r"q_\phi(z|x) = \mathcal{N}(\mu_\phi(x), \sigma^2_\phi(x))",
        description="Variational autoencoder inference network",
        formula_type="algebraic",
        category_id=cats['optimization_cog'],
        source_id=sources['literature'],
        domain="generative-models"
    )

    # VAE ELBO
    add_formula(conn,
        name="VAE ELBO Loss",
        latex=r"L = -E_q[\log p_\theta(x|z)] + KL(q_\phi(z|x) || p(z))",
        description="Evidence lower bound for VAE",
        formula_type="loss_function",
        category_id=cats['optimization_cog'],
        source_id=sources['literature'],
        domain="generative-models"
    )

def main():
    """Main population routine."""
    log.info("=" * 60)
    log.info("BIOFORMULAS DATABASE POPULATION")
    log.info("=" * 60)
    log.info(f"Database: {DB_PATH}")
    log.info(f"Started: {datetime.now().isoformat()}")

    conn = get_connection()

    try:
        # Add sources and categories
        sources = populate_sources(conn)
        cats = populate_categories(conn)

        # Add formulas by domain
        populate_neuroscience_formulas(conn, sources, cats)
        populate_biochemistry_formulas(conn, sources, cats)
        populate_gene_regulation_formulas(conn, sources, cats)
        populate_systems_biology_formulas(conn, sources, cats)
        populate_cognitive_formulas(conn, sources, cats)

        # Summary statistics
        log.info("=" * 60)
        log.info("POPULATION COMPLETE")
        log.info("=" * 60)

        cursor = conn.execute("SELECT COUNT(*) FROM formulas")
        formula_count = cursor.fetchone()[0]

        cursor = conn.execute("SELECT COUNT(*) FROM categories")
        cat_count = cursor.fetchone()[0]

        cursor = conn.execute("SELECT COUNT(*) FROM sources")
        source_count = cursor.fetchone()[0]

        cursor = conn.execute("SELECT COUNT(*) FROM ion_channels")
        ion_count = cursor.fetchone()[0]

        cursor = conn.execute("SELECT COUNT(*) FROM synapses")
        syn_count = cursor.fetchone()[0]

        cursor = conn.execute("SELECT COUNT(*) FROM enzyme_kinetics")
        enzyme_count = cursor.fetchone()[0]

        cursor = conn.execute("SELECT COUNT(*) FROM neuron_models")
        neuron_count = cursor.fetchone()[0]

        cursor = conn.execute("SELECT COUNT(*) FROM plasticity_rules")
        plasticity_count = cursor.fetchone()[0]

        log.info(f"Total formulas:     {formula_count}")
        log.info(f"Categories:         {cat_count}")
        log.info(f"Sources:            {source_count}")
        log.info(f"Ion channels:       {ion_count}")
        log.info(f"Synapses:           {syn_count}")
        log.info(f"Enzyme kinetics:    {enzyme_count}")
        log.info(f"Neuron models:      {neuron_count}")
        log.info(f"Plasticity rules:   {plasticity_count}")

        # Show formula breakdown by type
        log.info("-" * 40)
        log.info("Formulas by type:")
        cursor = conn.execute("""
            SELECT formula_type, COUNT(*) as cnt
            FROM formulas
            GROUP BY formula_type
            ORDER BY cnt DESC
        """)
        for row in cursor.fetchall():
            log.info(f"  {row[0]}: {row[1]}")

        log.info("=" * 60)
        log.info(f"Finished: {datetime.now().isoformat()}")

    finally:
        conn.close()

if __name__ == "__main__":
    main()
