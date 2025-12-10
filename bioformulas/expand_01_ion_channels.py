#!/usr/bin/env python3
"""Expansion module 1: Comprehensive ion channel library."""

from expand_base import (
    DB_PATH, get_conn, get_source_id, get_category_id, add_category,
    add_formula, add_ion_channel, add_synapse, add_enzyme, add_neuron,
    add_plasticity, count_formulas, print_summary, log
)

def run():
    conn = get_conn()
    start = count_formulas(conn)
    log.info("="*50)
    log.info("EXPANDING: ION CHANNELS")
    log.info("="*50)

    src = get_source_id(conn, 'ModelDB')
    lit = get_source_id(conn, 'Scientific Literature')
    cat = add_category(conn, 'Ion Channels', 'Neuroscience')

    # === SODIUM CHANNELS ===
    log.info("--- Sodium Channels ---")

    na_channels = [
        ("Nav1.1", "SCN1A", "cortical interneurons", -40, 120),
        ("Nav1.2", "SCN2A", "pyramidal neurons", -38, 100),
        ("Nav1.3", "SCN3A", "embryonic/neonatal", -35, 110),
        ("Nav1.4", "SCN4A", "skeletal muscle", -42, 150),
        ("Nav1.5", "SCN5A", "cardiac muscle", -45, 80),
        ("Nav1.6", "SCN8A", "nodes of Ranvier", -40, 130),
        ("Nav1.7", "SCN9A", "DRG pain neurons", -38, 100),
        ("Nav1.8", "SCN10A", "DRG slow TTX-R", -30, 60),
        ("Nav1.9", "SCN11A", "DRG persistent", -55, 20),
    ]

    for name, gene, loc, v_half, gmax in na_channels:
        fid = add_formula(conn, f"{name} Sodium Current ({gene})",
            rf"I_{{{name}}} = g_{{{name}}} m^3 h (V - E_{{Na}})",
            f"{name} sodium channel current in {loc}",
            "current_equation", cat, src,
            python_code=f"I = g_{name} * m**3 * h * (V - E_Na)",
            domain="ion-channels", model_origin=name)
        add_ion_channel(conn, fid, name, "voltage-gated", 4, "m", "h", 50, gmax)

        # Activation
        add_formula(conn, f"{name} Activation",
            rf"m_\infty = \frac{{1}}{{1 + \exp((V_{{1/2,m}} - V)/k_m)}}",
            f"{name} steady-state activation", "algebraic", cat, src,
            python_code=f"m_inf = 1 / (1 + np.exp(({v_half} - V) / 6))",
            domain="ion-channels", model_origin=name)

        # Inactivation
        add_formula(conn, f"{name} Inactivation",
            rf"h_\infty = \frac{{1}}{{1 + \exp((V - V_{{1/2,h}})/k_h)}}",
            f"{name} steady-state inactivation", "algebraic", cat, src,
            python_code=f"h_inf = 1 / (1 + np.exp((V - {v_half-20}) / 6))",
            domain="ion-channels", model_origin=name)

    # === POTASSIUM CHANNELS ===
    log.info("--- Potassium Channels ---")

    # Kv (voltage-gated)
    kv_channels = [
        ("Kv1.1", "KCNA1", "axons, dendrites", -30, 10),
        ("Kv1.2", "KCNA2", "axons, juxtaparanodal", -25, 12),
        ("Kv1.3", "KCNA3", "T lymphocytes", -35, 8),
        ("Kv1.4", "KCNA4", "A-type, inactivating", -40, 15),
        ("Kv2.1", "KCNB1", "somatic delayed rectifier", -15, 20),
        ("Kv3.1", "KCNC1", "fast-spiking interneurons", -10, 30),
        ("Kv3.2", "KCNC2", "fast repolarization", -5, 25),
        ("Kv4.2", "KCND2", "A-type, somatodendritic", -45, 18),
        ("Kv4.3", "KCND3", "A-type, cardiac", -50, 16),
        ("Kv7.1", "KCNQ1", "cardiac IKs", -20, 5),
        ("Kv7.2", "KCNQ2", "M-current", -35, 3),
        ("Kv7.3", "KCNQ3", "M-current", -35, 3),
    ]

    for name, gene, loc, v_half, gmax in kv_channels:
        fid = add_formula(conn, f"{name} Potassium Current ({gene})",
            rf"I_{{{name}}} = g_{{{name}}} n^4 (V - E_K)",
            f"{name} potassium channel in {loc}",
            "current_equation", cat, src,
            python_code=f"I = g_{name} * n**4 * (V - E_K)",
            domain="ion-channels", model_origin=name)
        add_ion_channel(conn, fid, name, "voltage-gated", 4, "n", None, -90, gmax)

    # Kir (inward rectifier)
    kir_channels = [
        ("Kir2.1", "KCNJ2", "cardiac, neuronal IK1", 0.5),
        ("Kir2.2", "KCNJ12", "neuronal", 0.4),
        ("Kir3.1", "KCNJ3", "GIRK1, G-protein gated", 0.3),
        ("Kir3.2", "KCNJ6", "GIRK2, G-protein gated", 0.3),
        ("Kir3.4", "KCNJ5", "GIRK4, cardiac", 0.25),
        ("Kir6.1", "KCNJ8", "KATP vascular", 0.2),
        ("Kir6.2", "KCNJ11", "KATP pancreatic", 0.2),
    ]

    for name, gene, loc, gmax in kir_channels:
        fid = add_formula(conn, f"{name} Inward Rectifier ({gene})",
            rf"I_{{{name}}} = g_{{{name}}} \frac{{[K^+]_o}}{{[K^+]_o + K_{{0.5}}}} \frac{{V - E_K}}{{1 + \exp((V - E_K - V_r)/k)}}",
            f"{name} inward rectifier in {loc}",
            "current_equation", cat, src,
            domain="ion-channels", model_origin=name)
        add_ion_channel(conn, fid, name, "inward-rectifier", 1, None, None, -90, gmax)

    # KCa (calcium-activated)
    kca_channels = [
        ("BK", "KCNMA1", "big conductance", 200, "voltage+Ca"),
        ("SK1", "KCNN1", "small conductance", 10, "Ca-only"),
        ("SK2", "KCNN2", "small conductance", 10, "Ca-only"),
        ("SK3", "KCNN3", "small conductance", 10, "Ca-only"),
        ("IK", "KCNN4", "intermediate conductance", 30, "Ca-only"),
    ]

    for name, gene, loc, gmax, gating in kca_channels:
        fid = add_formula(conn, f"{name} Ca-activated K+ ({gene})",
            rf"I_{{{name}}} = g_{{{name}}} \frac{{[Ca^{{2+}}]^n}}{{[Ca^{{2+}}]^n + K_d^n}} (V - E_K)",
            f"{name} calcium-activated potassium, {loc}",
            "current_equation", cat, src,
            domain="ion-channels", model_origin=name)
        add_ion_channel(conn, fid, name, gating, 1, None, None, -90, gmax)

    # === CALCIUM CHANNELS ===
    log.info("--- Calcium Channels ---")

    ca_channels = [
        ("Cav1.1", "CACNA1S", "L-type skeletal", -10, 1.0, "slow"),
        ("Cav1.2", "CACNA1C", "L-type cardiac/neuronal", -15, 1.5, "slow"),
        ("Cav1.3", "CACNA1D", "L-type cochlear/cardiac", -40, 0.8, "slow"),
        ("Cav1.4", "CACNA1F", "L-type retinal", -35, 0.5, "slow"),
        ("Cav2.1", "CACNA1A", "P/Q-type presynaptic", -20, 2.0, "moderate"),
        ("Cav2.2", "CACNA1B", "N-type presynaptic", -15, 1.8, "moderate"),
        ("Cav2.3", "CACNA1E", "R-type dendritic", -25, 1.2, "fast"),
        ("Cav3.1", "CACNA1G", "T-type thalamic", -60, 0.5, "transient"),
        ("Cav3.2", "CACNA1H", "T-type cardiac/neuronal", -58, 0.4, "transient"),
        ("Cav3.3", "CACNA1I", "T-type thalamic", -65, 0.3, "transient"),
    ]

    for name, gene, loc, v_half, gmax, kinetics in ca_channels:
        fid = add_formula(conn, f"{name} Calcium Current ({gene})",
            rf"I_{{{name}}} = g_{{{name}}} m^2 h (V - E_{{Ca}})",
            f"{name} calcium channel ({kinetics}), {loc}",
            "current_equation", cat, src,
            domain="ion-channels", model_origin=name)
        add_ion_channel(conn, fid, name, "voltage-gated", 3, "m", "h", 120, gmax)

        # GHK formulation for Ca
        add_formula(conn, f"{name} GHK Current",
            rf"I_{{{name}}} = P_{{{name}}} m^2 h \frac{{4F^2V}}{{RT}} \frac{{[Ca]_i - [Ca]_o\exp(-2FV/RT)}}{{1 - \exp(-2FV/RT)}}",
            f"{name} calcium current with GHK driving force",
            "current_equation", cat, lit,
            domain="ion-channels", model_origin=f"{name}-GHK")

    # === CHLORIDE CHANNELS ===
    log.info("--- Chloride Channels ---")

    cl_channels = [
        ("ClC-1", "CLCN1", "skeletal muscle", 10),
        ("ClC-2", "CLCN2", "neuronal, epithelial", 5),
        ("ClC-Ka", "CLCNKA", "kidney", 3),
        ("ClC-Kb", "CLCNKB", "kidney", 3),
        ("CFTR", "CFTR", "epithelial cAMP-gated", 8),
        ("ANO1", "ANO1", "Ca-activated Cl", 6),
        ("ANO2", "ANO2", "Ca-activated Cl olfactory", 4),
        ("GABA-A", "GABRA1", "ligand-gated Cl", 30),
        ("Glycine", "GLRA1", "ligand-gated Cl", 25),
    ]

    for name, gene, loc, gmax in cl_channels:
        fid = add_formula(conn, f"{name} Chloride Current ({gene})",
            rf"I_{{{name}}} = g_{{{name}}} (V - E_{{Cl}})",
            f"{name} chloride channel in {loc}",
            "current_equation", cat, src,
            domain="ion-channels", model_origin=name)
        add_ion_channel(conn, fid, name, "chloride", 1, None, None, -70, gmax)

    # === HCN CHANNELS ===
    log.info("--- HCN Channels (Ih) ---")

    hcn_channels = [
        ("HCN1", "HCN1", "fast Ih, cortex", -70, 0.1),
        ("HCN2", "HCN2", "moderate Ih, thalamus", -85, 0.08),
        ("HCN3", "HCN3", "slow Ih", -80, 0.05),
        ("HCN4", "HCN4", "cardiac pacemaker", -90, 0.15),
    ]

    for name, gene, loc, v_half, gmax in hcn_channels:
        fid = add_formula(conn, f"{name} Hyperpolarization-activated ({gene})",
            rf"I_{{{name}}} = g_{{{name}}} h (V - E_h)",
            f"{name} hyperpolarization-activated current, {loc}",
            "current_equation", cat, src,
            python_code=f"I = g_{name} * h * (V - E_h)  # E_h ~ -30mV",
            domain="ion-channels", model_origin=name)
        add_ion_channel(conn, fid, name, "hyperpolarization-activated", 1, None, "h", -30, gmax)

        add_formula(conn, f"{name} Activation",
            rf"h_\infty = \frac{{1}}{{1 + \exp((V - V_{{1/2}})/k)}}",
            f"{name} steady-state activation", "algebraic", cat, src,
            python_code=f"h_inf = 1 / (1 + np.exp((V - {v_half}) / 8))",
            domain="ion-channels", model_origin=name)

    # === TRP CHANNELS ===
    log.info("--- TRP Channels ---")

    trp_channels = [
        ("TRPV1", "capsaicin receptor, heat", "nonselective cation"),
        ("TRPV2", "high threshold heat", "nonselective cation"),
        ("TRPV3", "warm temperature", "nonselective cation"),
        ("TRPV4", "osmomechanical", "nonselective cation"),
        ("TRPM2", "oxidative stress", "Ca permeable"),
        ("TRPM4", "Ca-activated nonselective", "monovalent"),
        ("TRPM5", "taste transduction", "monovalent"),
        ("TRPM7", "Mg/Ca permeable", "divalent"),
        ("TRPM8", "cold/menthol", "Ca permeable"),
        ("TRPA1", "noxious cold/irritants", "nonselective cation"),
        ("TRPC1", "store-operated", "nonselective cation"),
        ("TRPC3", "DAG-activated", "nonselective cation"),
        ("TRPC6", "mechanosensitive", "nonselective cation"),
    ]

    for name, function, selectivity in trp_channels:
        fid = add_formula(conn, f"{name} TRP Channel",
            rf"I_{{{name}}} = g_{{{name}}} \cdot f(stimulus) \cdot (V - E_{{rev}})",
            f"{name}: {function}, {selectivity}",
            "current_equation", cat, lit,
            domain="ion-channels", model_origin=name)
        add_ion_channel(conn, fid, name, "polymodal", 1, None, None, 0, 1.0)

    # === LEAK CHANNELS ===
    log.info("--- Leak Channels ---")

    leak_channels = [
        ("TASK-1", "KCNK3", "K2P acid-sensitive", -90, 0.5),
        ("TASK-3", "KCNK9", "K2P acid-sensitive", -90, 0.4),
        ("TREK-1", "KCNK2", "K2P mechano/temp", -90, 0.6),
        ("TREK-2", "KCNK10", "K2P mechano/temp", -90, 0.5),
        ("TRAAK", "KCNK4", "K2P arachidonate", -90, 0.3),
        ("TWIK-1", "KCNK1", "K2P weakly rectifying", -90, 0.2),
    ]

    for name, gene, loc, erev, gmax in leak_channels:
        fid = add_formula(conn, f"{name} Leak Channel ({gene})",
            rf"I_{{{name}}} = g_{{{name}}} (V - E_K)",
            f"{name} two-pore domain K+ channel, {loc}",
            "current_equation", cat, src,
            domain="ion-channels", model_origin=name)
        add_ion_channel(conn, fid, name, "leak", 1, None, None, erev, gmax)

    # === GENERIC GATING KINETICS ===
    log.info("--- Gating Kinetics ---")

    # Boltzmann activation
    add_formula(conn, "Boltzmann Activation",
        r"m_\infty(V) = \frac{1}{1 + \exp\left(\frac{V_{1/2} - V}{k}\right)}",
        "Generic steady-state activation function",
        "algebraic", cat, lit,
        python_code="m_inf = 1 / (1 + np.exp((V_half - V) / k))",
        domain="ion-channels", model_origin="boltzmann")

    # Time constant voltage dependence
    add_formula(conn, "Bell-shaped Time Constant",
        r"\tau_m(V) = \tau_{min} + \frac{\tau_{max} - \tau_{min}}{\cosh\left(\frac{V - V_{peak}}{2k}\right)}",
        "Voltage-dependent time constant with bell shape",
        "algebraic", cat, lit,
        domain="ion-channels", model_origin="tau-bell")

    # Hodgkin-Huxley style rates
    add_formula(conn, "Generic HH Alpha Rate",
        r"\alpha(V) = \frac{A(V - V_0)}{1 - \exp(-(V - V_0)/k)}",
        "Generic HH-style forward rate constant",
        "rate_equation", cat, lit,
        domain="ion-channels", model_origin="hh-alpha")

    add_formula(conn, "Generic HH Beta Rate",
        r"\beta(V) = B \exp\left(-\frac{V - V_0}{k}\right)",
        "Generic HH-style backward rate constant",
        "rate_equation", cat, lit,
        domain="ion-channels", model_origin="hh-beta")

    # Markov state transitions
    add_formula(conn, "Markov Channel - 2 State",
        r"\frac{dO}{dt} = \alpha(V)(1-O) - \beta(V)O",
        "Two-state Markov model (closed-open)",
        "ODE", cat, lit,
        domain="ion-channels", model_origin="markov-2state")

    add_formula(conn, "Markov Channel - 3 State",
        r"\begin{aligned} \frac{dC}{dt} &= -k_{CO}C + k_{OC}O \\ \frac{dO}{dt} &= k_{CO}C - (k_{OC} + k_{OI})O + k_{IO}I \\ \frac{dI}{dt} &= k_{OI}O - k_{IO}I \end{aligned}",
        "Three-state Markov model (closed-open-inactivated)",
        "ODE", cat, lit,
        domain="ion-channels", model_origin="markov-3state")

    add_formula(conn, "Markov Channel - 5 State",
        r"C_1 \rightleftharpoons C_2 \rightleftharpoons C_3 \rightleftharpoons O \rightleftharpoons I",
        "Five-state sequential Markov model",
        "ODE", cat, lit,
        domain="ion-channels", model_origin="markov-5state")

    print_summary(conn, "ION CHANNELS", start)
    conn.close()

if __name__ == "__main__":
    run()
