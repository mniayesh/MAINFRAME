#!/usr/bin/env python3
"""Expansion module 7: Cardiac and muscle models."""

from expand_base import *

def run():
    conn = get_conn()
    start = count_formulas(conn)
    log.info("="*50)
    log.info("EXPANDING: CARDIAC & MUSCLE MODELS")
    log.info("="*50)

    src = get_source_id(conn, 'BioModels Database')
    lit = get_source_id(conn, 'Scientific Literature')

    card = add_category(conn, 'Cardiac', None, 'Heart electrophysiology')
    vent = add_category(conn, 'Ventricular', 'Cardiac')
    atrial = add_category(conn, 'Atrial', 'Cardiac')
    pace = add_category(conn, 'Pacemaker', 'Cardiac')
    muscle = add_category(conn, 'Muscle', None, 'Skeletal and smooth muscle')

    # === VENTRICULAR MODELS ===
    log.info("--- Ventricular Action Potential Models ---")

    # Luo-Rudy I
    add_formula(conn, "Luo-Rudy I (LR1)",
        r"C_m\frac{dV}{dt} = -(I_{Na} + I_{si} + I_K + I_{K1} + I_{Kp} + I_b)",
        "Guinea pig ventricular myocyte",
        "ODE", vent, src,
        domain="cardiac", model_origin="luo-rudy-1",
        doi="10.1161/01.RES.68.6.1501", year=1991)

    # Luo-Rudy II (dynamic)
    add_formula(conn, "Luo-Rudy II (LRd)",
        r"C_m\frac{dV}{dt} = -(I_{Na} + I_{Ca} + I_{Kr} + I_{Ks} + I_{K1} + I_{NaK} + I_{NaCa} + ...)",
        "Dynamic LR model with Ca handling",
        "ODE", vent, src,
        domain="cardiac", model_origin="luo-rudy-2")

    # Ten Tusscher-Panfilov
    add_formula(conn, "ten Tusscher Human Ventricle",
        r"C_m\frac{dV}{dt} = -(I_{Na} + I_{to} + I_{Kr} + I_{Ks} + I_{K1} + I_{CaL} + I_{NaCa} + I_{NaK} + ...)",
        "Human ventricular myocyte model",
        "ODE", vent, src,
        domain="cardiac", model_origin="ten-tusscher",
        doi="10.1152/ajpheart.00794.2003", year=2004)

    # O'Hara-Rudy
    add_formula(conn, "O'Hara-Rudy Human Ventricle",
        r"C_m\frac{dV}{dt} = -(I_{Na} + I_{NaL} + I_{to} + I_{CaL} + I_{CaNa} + I_{CaK} + I_{Kr} + I_{Ks} + ...)",
        "Latest human ventricular model",
        "ODE", vent, src,
        domain="cardiac", model_origin="ohara-rudy",
        doi="10.1371/journal.pcbi.1002061", year=2011)

    # === ATRIAL MODELS ===
    log.info("--- Atrial Models ---")

    add_formula(conn, "Courtemanche Human Atrium",
        r"C_m\frac{dV}{dt} = -(I_{Na} + I_{to} + I_{Kur} + I_{Kr} + I_{Ks} + I_{K1} + I_{CaL} + ...)",
        "Human atrial myocyte",
        "ODE", atrial, src,
        domain="cardiac", model_origin="courtemanche",
        doi="10.1152/ajpheart.1998.275.1.H301", year=1998)

    add_formula(conn, "Grandi-Bhalla Atrium",
        r"C_m\frac{dV}{dt} = -(I_{Na} + I_{NaL} + I_{to} + I_{Kur} + I_{Kr} + I_{Ks} + I_{K1} + I_{CaL} + ...)",
        "Human atrial with detailed Ca handling",
        "ODE", atrial, src,
        domain="cardiac", model_origin="grandi-atrial")

    # === PACEMAKER MODELS ===
    log.info("--- Pacemaker Models ---")

    add_formula(conn, "Sinoatrial Node (Severi)",
        r"C_m\frac{dV}{dt} = -(I_{Na} + I_{CaL} + I_{CaT} + I_f + I_{Kr} + I_{Ks} + I_{to} + ...)",
        "Rabbit sinoatrial node cell",
        "ODE", pace, src,
        domain="cardiac", model_origin="severi-SAN")

    add_formula(conn, "Funny Current (If/Ih)",
        r"I_f = g_f y (V - E_f)",
        "HCN channel pacemaker current",
        "current_equation", pace, src,
        domain="cardiac", model_origin="If")

    add_formula(conn, "Calcium Clock",
        r"\frac{d[Ca]_{SR}}{dt} = J_{SERCA} - J_{leak} - J_{rel}",
        "SR Ca oscillations drive pacemaking",
        "ODE", pace, src,
        domain="cardiac", model_origin="Ca-clock")

    # === CARDIAC ION CURRENTS ===
    log.info("--- Cardiac Ion Currents ---")

    currents = [
        ("I_Na (cardiac)", r"I_{Na} = g_{Na} m^3 h j (V - E_{Na})", "Fast sodium with slow inactivation j"),
        ("I_NaL", r"I_{NaL} = g_{NaL} m_L h_L (V - E_{Na})", "Late/persistent sodium current"),
        ("I_CaL", r"I_{CaL} = g_{CaL} d f f_{Ca} (V - E_{Ca})", "L-type Ca with Ca-dependent inactivation"),
        ("I_CaT", r"I_{CaT} = g_{CaT} b g (V - E_{Ca})", "T-type calcium current"),
        ("I_to", r"I_{to} = g_{to} r s (V - E_K)", "Transient outward K current"),
        ("I_Kur", r"I_{Kur} = g_{Kur} a i (V - E_K)", "Ultra-rapid delayed rectifier (atrial)"),
        ("I_Kr", r"I_{Kr} = g_{Kr} x_r \sqrt{[K]_o/5.4} (V - E_K)", "Rapid delayed rectifier"),
        ("I_Ks", r"I_{Ks} = g_{Ks} x_s^2 (V - E_K)", "Slow delayed rectifier"),
        ("I_K1", r"I_{K1} = g_{K1} \frac{[K]_o}{[K]_o + K_m} \frac{V - E_K}{1 + \exp((V - E_K + 10)/10)}", "Inward rectifier"),
        ("I_NaK", r"I_{NaK} = I_{NaK,max} \frac{[K]_o}{[K]_o + K_m} \frac{[Na]_i^{1.5}}{[Na]_i^{1.5} + K_m^{1.5}}", "Na/K ATPase"),
        ("I_NaCa", r"I_{NaCa} = k_{NaCa} \frac{[Na]_i^3 [Ca]_o e^{V/V_T} - [Na]_o^3 [Ca]_i e^{-(V/V_T)}}{(K_m^3 + [Na]_o^3)(K_{Ca} + [Ca]_o)}", "Na/Ca exchanger"),
        ("I_pCa", r"I_{pCa} = I_{pCa,max} \frac{[Ca]_i}{K_m + [Ca]_i}", "Sarcolemmal Ca pump"),
        ("I_bCa", r"I_{bCa} = g_{bCa} (V - E_{Ca})", "Background Ca leak"),
        ("I_bNa", r"I_{bNa} = g_{bNa} (V - E_{Na})", "Background Na leak"),
    ]

    for name, formula, desc in currents:
        add_formula(conn, name, formula, desc, "current_equation", vent, src,
            domain="cardiac", model_origin=name.replace(" ", "-"))

    # === CALCIUM HANDLING ===
    log.info("--- Cardiac Ca Handling ---")

    add_formula(conn, "JSR Ca Release (RyR)",
        r"J_{rel} = v_{rel} \frac{[Ca]_{JSR}}{1 + (K_{rel}/[Ca]_i)^2}",
        "Junctional SR release",
        "algebraic", vent, src,
        domain="cardiac", model_origin="J-rel")

    add_formula(conn, "NSR-JSR Transfer",
        r"J_{tr} = ([Ca]_{NSR} - [Ca]_{JSR}) / \tau_{tr}",
        "Network to junctional SR transfer",
        "algebraic", vent, src,
        domain="cardiac", model_origin="J-tr")

    add_formula(conn, "SR Ca Leak",
        r"J_{leak} = v_{leak} ([Ca]_{NSR} - [Ca]_i)",
        "Passive leak from SR",
        "algebraic", vent, src,
        domain="cardiac", model_origin="J-leak")

    add_formula(conn, "SERCA (cardiac)",
        r"J_{up} = V_{max} \frac{[Ca]_i^2}{K_m^2 + [Ca]_i^2}",
        "SR Ca-ATPase uptake",
        "algebraic", vent, src,
        domain="cardiac", model_origin="J-up")

    add_formula(conn, "Cytosolic Ca Buffer",
        r"\frac{d[CaTrop]}{dt} = k_{on} [Ca]_i ([Trop]_T - [CaTrop]) - k_{off} [CaTrop]",
        "Troponin C Ca binding",
        "ODE", vent, src,
        domain="cardiac", model_origin="Ca-trop")

    # === MUSCLE CONTRACTION ===
    log.info("--- Muscle Contraction ---")

    add_formula(conn, "Cross-Bridge Cycling (Huxley)",
        r"\frac{dn}{dt} = (1-n) f(x) - n g(x)",
        "Fraction of attached cross-bridges",
        "ODE", muscle, lit,
        domain="muscle", model_origin="huxley-CB")

    add_formula(conn, "Force-Velocity (Hill)",
        r"(F + a)(v + b) = (F_0 + a) b",
        "Hill's muscle force-velocity relation",
        "algebraic", muscle, lit,
        domain="muscle", model_origin="hill-FV")

    add_formula(conn, "Active Force",
        r"F_{active} = F_{max} \cdot [Ca]_{bound} / [Ca]_{max} \cdot f_L(L) \cdot f_V(v)",
        "Ca-dependent force with length/velocity modulation",
        "algebraic", muscle, src,
        domain="muscle", model_origin="F-active")

    add_formula(conn, "Passive Force",
        r"F_{passive} = k_{PE} (\lambda - 1)^2 H(\lambda - 1)",
        "Parallel elastic element",
        "algebraic", muscle, lit,
        domain="muscle", model_origin="F-passive")

    add_formula(conn, "Length-Tension (Sarcomere)",
        r"f_L(L) = 1 - \left(\frac{L - L_0}{L_{width}}\right)^2",
        "Sarcomere length-tension relation",
        "algebraic", muscle, lit,
        domain="muscle", model_origin="length-tension")

    add_formula(conn, "Ca-Troponin Binding (3-state)",
        r"\frac{d[CaTnC]}{dt} = k_{on} [Ca][TnC] - k_{off}^{slow} [CaTnC] - k_{off}^{fast} [CaTnC] f(F)",
        "Force-dependent Ca-TnC unbinding",
        "ODE", muscle, src,
        domain="muscle", model_origin="CaTnC-3state")

    # === SMOOTH MUSCLE ===
    log.info("--- Smooth Muscle ---")

    add_formula(conn, "MLCK Activation",
        r"[MLCK^*] = [MLCK]_T \frac{[CaM_{Ca4}]^2}{K_d^2 + [CaM_{Ca4}]^2}",
        "Ca/CaM-dependent myosin light chain kinase",
        "algebraic", muscle, src,
        domain="smooth-muscle", model_origin="MLCK")

    add_formula(conn, "Myosin Phosphorylation",
        r"\frac{d[M_p]}{dt} = k_{MLCK} [MLCK^*] [M] - k_{MLCP} [M_p]",
        "Myosin phosphorylation/dephosphorylation",
        "ODE", muscle, src,
        domain="smooth-muscle", model_origin="myosin-phos")

    add_formula(conn, "Latch Bridge",
        r"\frac{d[AM_p]}{dt} = k_{att} [M_p] - (k_{det} + k_{latch}) [AM_p]",
        "Attached phosphorylated myosin",
        "ODE", muscle, src,
        domain="smooth-muscle", model_origin="latch")

    add_formula(conn, "Smooth Muscle Force",
        r"F = F_{max} ([AM_p] + 0.2[AM])",
        "Force from phosphorylated and latch bridges",
        "algebraic", muscle, src,
        domain="smooth-muscle", model_origin="SM-force")

    print_summary(conn, "CARDIAC & MUSCLE", start)
    conn.close()

if __name__ == "__main__":
    run()
