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
