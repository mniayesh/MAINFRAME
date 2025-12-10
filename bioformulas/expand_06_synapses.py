#!/usr/bin/env python3
"""Expansion module 6: Synapses and plasticity."""

from expand_base import (
    DB_PATH, get_conn, get_source_id, get_category_id, add_category,
    add_formula, add_ion_channel, add_synapse, add_enzyme, add_neuron,
    add_plasticity, count_formulas, print_summary, log
)

def run():
    conn = get_conn()
    start = count_formulas(conn)
    log.info("="*50)
    log.info("EXPANDING: SYNAPSES & PLASTICITY")
    log.info("="*50)

    src = get_source_id(conn, 'ModelDB')
    lit = get_source_id(conn, 'Scientific Literature')

    syn = add_category(conn, 'Synaptic Transmission', 'Neuroscience')
    stp = add_category(conn, 'Short-Term Plasticity', 'Synaptic Transmission')
    ltp = add_category(conn, 'Long-Term Plasticity', 'Neuroscience')
    homeo = add_category(conn, 'Homeostatic Plasticity', 'Neuroscience')

    # === VESICLE DYNAMICS ===
    log.info("--- Vesicle Dynamics ---")

    add_formula(conn, "Vesicle Release Probability",
        r"P_{rel} = 1 - \exp(-[Ca^{2+}]^n / K_d^n)",
        "Calcium-dependent release probability",
        "algebraic", syn, src,
        domain="presynaptic", model_origin="P-release")

    add_formula(conn, "Readily Releasable Pool (RRP)",
        r"\frac{dR}{dt} = \frac{R_0 - R}{\tau_{rec}} - P_{rel} R \delta(t - t_{spike})",
        "RRP depletion and recovery",
        "ODE", syn, src,
        domain="presynaptic", model_origin="RRP")

    add_formula(conn, "Docked Vesicles (Tsodyks-Markram)",
        r"\frac{dx}{dt} = \frac{1-x}{\tau_D} - u x \delta(t - t_{spike})",
        "Fraction of available vesicles",
        "ODE", syn, src,
        domain="presynaptic", model_origin="TM-x")

    add_formula(conn, "Facilitation Variable (Tsodyks-Markram)",
        r"\frac{du}{dt} = \frac{U - u}{\tau_F} + U(1-u) \delta(t - t_{spike})",
        "Use-dependent facilitation",
        "ODE", syn, src,
        domain="presynaptic", model_origin="TM-u")

    add_formula(conn, "Vesicle Pool Model (3-pool)",
        r"\frac{dN_R}{dt} = -P_{rel} N_R \delta(t) + k_{ref} N_I - k_{mob} N_R",
        "Readily releasable, intermediate, and reserve pools",
        "ODE", syn, src,
        domain="presynaptic", model_origin="3-pool")

    add_formula(conn, "Calcium Sensor (Bhalla-Bhalla)",
        r"\frac{dC_n}{dt} = k_+ [Ca]^n (1 - C_n) - k_- C_n",
        "Multi-site calcium sensor for release",
        "ODE", syn, src,
        domain="presynaptic", model_origin="Ca-sensor")

    # === SHORT-TERM PLASTICITY ===
    log.info("--- Short-Term Plasticity ---")

    add_formula(conn, "Paired-Pulse Ratio",
        r"PPR = \frac{EPSC_2}{EPSC_1} = \frac{u_2 x_2}{u_1 x_1}",
        "Ratio of second to first response",
        "algebraic", stp, lit,
        domain="short-term-plasticity", model_origin="PPR")

    add_formula(conn, "Depression-Dominated Synapse",
        r"A_n = A_0 u_0 x_0 (1-x_0)^{n-1}",
        "Amplitude of nth spike with strong depression",
        "algebraic", stp, lit,
        domain="short-term-plasticity", model_origin="depression")

    add_formula(conn, "Facilitation-Dominated Synapse",
        r"A_n = A_0 u_0 [1 + (U_{max}/u_0 - 1)(1-e^{-n/\tau_F})]",
        "Amplitude buildup with facilitation",
        "algebraic", stp, lit,
        domain="short-term-plasticity", model_origin="facilitation")

    add_formula(conn, "Abbott-Varela STP Model",
        r"g_{syn}(t) = g_{max} F D \sum_j \alpha(t - t_j)",
        "Combined facilitation (F) and depression (D)",
        "algebraic", stp, src,
        domain="short-term-plasticity", model_origin="abbott-varela")

    add_formula(conn, "Augmentation",
        r"\frac{dA}{dt} = -\frac{A - 1}{\tau_A} + \Delta A \cdot \delta(t - t_{spike})",
        "Slow enhancement lasting seconds",
        "ODE", stp, lit,
        domain="short-term-plasticity", model_origin="augmentation")

    add_formula(conn, "Post-Tetanic Potentiation",
        r"\frac{dP}{dt} = -\frac{P - 1}{\tau_P} + \Delta P \cdot H([Ca] - \theta)",
        "Minutes-long enhancement after tetanus",
        "ODE", stp, lit,
        domain="short-term-plasticity", model_origin="PTP")

    # === LONG-TERM PLASTICITY ===
    log.info("--- Long-Term Plasticity ---")

    # Calcium-based models
    add_formula(conn, "Shouval Calcium Model",
        r"\frac{dw}{dt} = \eta([Ca]) \cdot (\Omega([Ca]) - w)",
        "Weight change depends on Ca level",
        "ODE", ltp, src,
        domain="LTP-LTD", model_origin="shouval")
    add_plasticity(conn, 0, "Shouval-Ca", 100, 100, 0.001, "subtractive", True)

    add_formula(conn, "Omega Function (LTP/LTD)",
        r"\Omega([Ca]) = \text{sig}([Ca] - \theta_{LTP}) - 0.5 \cdot \text{sig}([Ca] - \theta_{LTD})",
        "Direction of plasticity based on Ca thresholds",
        "algebraic", ltp, src,
        domain="LTP-LTD", model_origin="omega")

    # STDP variants
    stdp_types = [
        ("Symmetric STDP", r"\Delta w = A \exp(-|\Delta t|/\tau)", "both pre and post-before-pre cause LTP"),
        ("Asymmetric STDP", r"\Delta w = A_+ e^{-\Delta t/\tau_+} - A_- e^{\Delta t/\tau_-}", "classic Hebbian timing"),
        ("Anti-Hebbian STDP", r"\Delta w = -A_+ e^{-\Delta t/\tau_+} + A_- e^{\Delta t/\tau_-}", "found in some interneurons"),
        ("Mexican Hat STDP", r"\Delta w = A_1 e^{-\Delta t^2/2\sigma_1^2} - A_2 e^{-\Delta t^2/2\sigma_2^2}", "DoG temporal window"),
    ]

    for name, formula, desc in stdp_types:
        fid = add_formula(conn, name, formula, desc, "plasticity_rule", ltp, lit,
            domain="STDP", model_origin=name.lower().replace(" ", "-"))
        add_plasticity(conn, fid, name, 20, 20, 0.01, "additive", False)

    # Weight dependence
    add_formula(conn, "Multiplicative STDP (Soft Bounds)",
        r"\Delta w = \begin{cases} (w_{max} - w) \cdot f_+(\Delta t) & \text{LTP} \\ w \cdot f_-(\Delta t) & \text{LTD} \end{cases}",
        "Weight-dependent updates preserve stability",
        "plasticity_rule", ltp, lit,
        domain="STDP", model_origin="multiplicative-STDP")

    add_formula(conn, "Log-STDP",
        r"\Delta w = \eta \log(1 + w/w_0) \cdot f(\Delta t)",
        "Logarithmic weight dependence",
        "plasticity_rule", ltp, lit,
        domain="STDP", model_origin="log-STDP")

    add_formula(conn, "Power-Law STDP",
        r"\Delta w = \eta \cdot w^\mu \cdot f(\Delta t)",
        "Power-law weight dependence (mu < 1)",
        "plasticity_rule", ltp, lit,
        domain="STDP", model_origin="power-STDP")

    # Voltage-based STDP
    add_formula(conn, "Voltage-Dependent STDP (Clopath)",
        r"\frac{dw}{dt} = A_{LTD} \bar{x} (V - \theta_{LTD})_- + A_{LTP} x (\bar{V} - \theta_{LTP})_+ (V - \theta_{LTD})_+",
        "STDP driven by voltage rather than spikes",
        "ODE", ltp, src,
        domain="STDP", model_origin="clopath",
        doi="10.1038/nn.2479", year=2010)

    add_formula(conn, "Clopath LTD Term",
        r"LTD = A_{LTD} \bar{x}_j (u_i - \theta_{LTD})_-",
        "Presynaptic trace times postsynaptic voltage",
        "algebraic", ltp, src,
        domain="STDP", model_origin="clopath-LTD")

    # Reward-modulated STDP
    add_formula(conn, "Reward-Modulated STDP",
        r"\frac{dw}{dt} = c \cdot STDP(\Delta t) \cdot (R - \bar{R})",
        "Eligibility trace gated by reward signal",
        "ODE", ltp, lit,
        domain="reward-learning", model_origin="R-STDP")

    add_formula(conn, "Eligibility Trace",
        r"\frac{de}{dt} = -\frac{e}{\tau_e} + STDP(\Delta t) \cdot \delta(t - t_{spike})",
        "Decaying trace of recent STDP events",
        "ODE", ltp, lit,
        domain="reward-learning", model_origin="eligibility")

    # Metaplasticity
    add_formula(conn, "BCM Sliding Threshold",
        r"\frac{d\theta}{dt} = \frac{\bar{c}^2 - \theta}{\tau_\theta}",
        "Activity-dependent sliding threshold",
        "ODE", ltp, lit,
        domain="metaplasticity", model_origin="BCM-theta")

    add_formula(conn, "Metaplastic Threshold",
        r"\theta_m = \langle c^2 \rangle / \theta_0",
        "Threshold proportional to recent activity",
        "algebraic", ltp, lit,
        domain="metaplasticity", model_origin="metaplastic")

    # === HOMEOSTATIC PLASTICITY ===
    log.info("--- Homeostatic Plasticity ---")

    add_formula(conn, "Synaptic Scaling",
        r"\frac{dw}{dt} = \alpha (r_{target} - r)",
        "Global multiplicative scaling to target rate",
        "ODE", homeo, lit,
        domain="homeostatic", model_origin="synaptic-scaling")

    add_formula(conn, "Multiplicative Scaling",
        r"w_{new} = w_{old} \cdot s, \quad s = r_{target} / r_{actual}",
        "Scale all weights by same factor",
        "algebraic", homeo, lit,
        domain="homeostatic", model_origin="mult-scaling")

    add_formula(conn, "Intrinsic Excitability",
        r"\frac{dg_{max}}{dt} = \beta (r_{target} - r)",
        "Adjust ion channel density to target rate",
        "ODE", homeo, lit,
        domain="homeostatic", model_origin="intrinsic")

    add_formula(conn, "Heterosynaptic Plasticity",
        r"\Delta w_i = -\gamma \sum_{j \neq i} \Delta w_j",
        "Competition between synapses",
        "algebraic", homeo, lit,
        domain="homeostatic", model_origin="heterosynaptic")

    add_formula(conn, "Sliding Threshold (Turrigiano)",
        r"\theta_{LTP} = f(\langle [Ca^{2+}] \rangle)",
        "LTP threshold depends on average Ca level",
        "algebraic", homeo, lit,
        domain="homeostatic", model_origin="turrigiano")

    # === STRUCTURAL PLASTICITY ===
    log.info("--- Structural Plasticity ---")

    add_formula(conn, "Spine Formation Rate",
        r"\frac{dN_{spine}}{dt} = \alpha \cdot activity - \beta \cdot N_{spine}",
        "Activity-dependent spine creation",
        "ODE", ltp, lit,
        domain="structural", model_origin="spine-formation")

    add_formula(conn, "Spine Elimination",
        r"P_{elim} = \exp(-w / w_0)",
        "Weak synapses more likely eliminated",
        "algebraic", ltp, lit,
        domain="structural", model_origin="spine-elim")

    add_formula(conn, "Synapse Maturation",
        r"\frac{dV_{spine}}{dt} = \gamma \cdot w - \delta \cdot V_{spine}",
        "Spine volume tracks synaptic weight",
        "ODE", ltp, lit,
        domain="structural", model_origin="spine-volume")

    add_formula(conn, "Axon Branching",
        r"P_{branch} = \sigma([BDNF] / K_d)",
        "BDNF-dependent axon branching probability",
        "algebraic", ltp, lit,
        domain="structural", model_origin="axon-branch")

    print_summary(conn, "SYNAPSES & PLASTICITY", start)
    conn.close()

if __name__ == "__main__":
    run()
