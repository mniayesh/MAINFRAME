#!/usr/bin/env python3
"""Expansion module 3: Receptors and ligand binding."""

from expand_base import (
    DB_PATH, get_conn, get_source_id, get_category_id, add_category,
    add_formula, add_ion_channel, add_synapse, add_enzyme, add_neuron,
    add_plasticity, count_formulas, print_summary, log
)

def run():
    conn = get_conn()
    start = count_formulas(conn)
    log.info("="*50)
    log.info("EXPANDING: RECEPTORS & LIGAND BINDING")
    log.info("="*50)

    src = get_source_id(conn, 'BioModels Database')
    lit = get_source_id(conn, 'Scientific Literature')

    rec = add_category(conn, 'Receptors', None, 'Receptor binding and activation')
    gpcr = add_category(conn, 'GPCRs', 'Receptors', 'G-protein coupled receptors')
    lgic = add_category(conn, 'Ligand-gated Ion Channels', 'Receptors', 'Ionotropic receptors')
    rtk = add_category(conn, 'Receptor Tyrosine Kinases', 'Receptors', 'Growth factor receptors')
    nuclear = add_category(conn, 'Nuclear Receptors', 'Receptors', 'Transcription factor receptors')

    # === GENERIC BINDING MODELS ===
    log.info("--- Generic Binding Models ---")

    add_formula(conn, "Simple Binding Equilibrium",
        r"[RL] = \frac{[R]_T [L]}{K_d + [L]}",
        "Receptor-ligand binding at equilibrium",
        "algebraic", rec, lit,
        python_code="RL = R_total * L / (Kd + L)",
        domain="receptor-binding", model_origin="simple-binding")

    add_formula(conn, "Binding On Rate",
        r"\frac{d[RL]}{dt} = k_{on} [R][L] - k_{off} [RL]",
        "Receptor-ligand association/dissociation kinetics",
        "ODE", rec, lit,
        python_code="dRL_dt = k_on * R * L - k_off * RL",
        domain="receptor-binding", model_origin="binding-kinetics")

    add_formula(conn, "Two-Site Binding",
        r"[RL] = [R]_T \left( \frac{f_{high} [L]}{K_{d,high} + [L]} + \frac{(1-f_{high}) [L]}{K_{d,low} + [L]} \right)",
        "Binding with high and low affinity sites",
        "algebraic", rec, lit,
        domain="receptor-binding", model_origin="two-site")

    add_formula(conn, "Competitive Binding",
        r"[RL] = \frac{[R]_T [L]}{K_d (1 + [I]/K_i) + [L]}",
        "Ligand binding with competitive inhibitor",
        "algebraic", rec, lit,
        domain="receptor-binding", model_origin="competitive")

    add_formula(conn, "Allosteric Binding (MWC)",
        r"Y = \frac{[L]/K_R (1 + [L]/K_R)^{n-1} + L c [L]/K_R (1 + c[L]/K_R)^{n-1}}{(1 + [L]/K_R)^n + L(1 + c[L]/K_R)^n}",
        "Monod-Wyman-Changeux allosteric binding model",
        "algebraic", rec, lit,
        domain="receptor-binding", model_origin="MWC-receptor")

    add_formula(conn, "Operational Model of Agonism",
        r"E = \frac{E_{max} \tau [A]}{K_A + [A](1 + \tau)}",
        "Black-Leff operational model for receptor activation",
        "algebraic", rec, lit,
        domain="receptor-binding", model_origin="operational")

    # === GPCR SIGNALING ===
    log.info("--- GPCR Signaling ---")

    gpcr_types = [
        ("beta1-AR", "Gs", "heart contractility, cAMP↑", "epinephrine,norepinephrine"),
        ("beta2-AR", "Gs", "bronchodilation, cAMP↑", "epinephrine"),
        ("alpha1-AR", "Gq", "vasoconstriction, IP3/DAG", "norepinephrine"),
        ("alpha2-AR", "Gi", "presynaptic inhibition, cAMP↓", "norepinephrine"),
        ("M1-mAChR", "Gq", "cognitive, IP3/DAG", "acetylcholine"),
        ("M2-mAChR", "Gi", "cardiac slowing, cAMP↓", "acetylcholine"),
        ("M3-mAChR", "Gq", "smooth muscle, secretion", "acetylcholine"),
        ("D1R", "Gs", "reward, motor, cAMP↑", "dopamine"),
        ("D2R", "Gi", "motor control, cAMP↓", "dopamine"),
        ("D3R", "Gi", "limbic, cAMP↓", "dopamine"),
        ("D4R", "Gi", "frontal cortex", "dopamine"),
        ("5-HT1A", "Gi", "anxiolytic, cAMP↓", "serotonin"),
        ("5-HT2A", "Gq", "hallucinogenic, IP3/DAG", "serotonin"),
        ("5-HT2C", "Gq", "appetite, mood", "serotonin"),
        ("GABA-B", "Gi", "presynaptic inhibition", "GABA"),
        ("mGluR1", "Gq", "LTD, IP3/DAG", "glutamate"),
        ("mGluR2", "Gi", "presynaptic inhibition", "glutamate"),
        ("mGluR5", "Gq", "LTP modulation, IP3/DAG", "glutamate"),
        ("CB1", "Gi", "retrograde signaling", "anandamide,2-AG"),
        ("CB2", "Gi", "immune modulation", "anandamide,2-AG"),
        ("mu-OR", "Gi", "analgesia, reward", "endorphins"),
        ("delta-OR", "Gi", "analgesia", "enkephalins"),
        ("kappa-OR", "Gi", "dysphoria", "dynorphins"),
        ("H1R", "Gq", "allergic response, IP3/DAG", "histamine"),
        ("H2R", "Gs", "gastric acid, cAMP↑", "histamine"),
        ("A1R", "Gi", "cardiac, neuronal depression", "adenosine"),
        ("A2AR", "Gs", "vasodilation, cAMP↑", "adenosine"),
        ("P2Y1", "Gq", "platelet aggregation", "ADP"),
        ("P2Y12", "Gi", "platelet aggregation", "ADP"),
        ("PAR1", "Gq", "thrombin signaling", "thrombin"),
        ("V1aR", "Gq", "vasoconstriction", "vasopressin"),
        ("V2R", "Gs", "water reabsorption", "vasopressin"),
        ("OTR", "Gq", "social bonding, uterine", "oxytocin"),
    ]

    for name, gtype, function, ligands in gpcr_types:
        fid = add_formula(conn, f"{name} GPCR Activation",
            rf"R^* = \frac{{[L]/K_d}}{{1 + [L]/K_d}} \cdot R_{{total}}",
            f"{name} ({gtype}-coupled): {function}. Ligands: {ligands}",
            "algebraic", gpcr, src,
            domain="GPCR", model_origin=name)

    # G-protein cycle
    add_formula(conn, "G-protein Activation Cycle",
        r"\frac{d[G^*]}{dt} = k_{act} [R^*][G_{GDP}] - k_{hyd} [G^*]",
        "G-protein GTP loading and hydrolysis",
        "ODE", gpcr, src,
        python_code="dG_active_dt = k_act * R_active * G_GDP - k_hyd * G_active",
        domain="GPCR", model_origin="G-protein-cycle")

    # cAMP dynamics
    add_formula(conn, "cAMP Production (Gs)",
        r"\frac{d[cAMP]}{dt} = k_{AC} [G_s^*] - k_{PDE} [cAMP]",
        "Adenylyl cyclase activation by Gs, PDE degradation",
        "ODE", gpcr, src,
        python_code="dcAMP_dt = k_AC * Gs_active - k_PDE * cAMP",
        domain="GPCR", model_origin="cAMP-Gs")

    # IP3/DAG production
    add_formula(conn, "IP3/DAG Production (Gq)",
        r"\frac{d[IP_3]}{dt} = k_{PLC} [G_q^*] [PIP_2] - k_{deg} [IP_3]",
        "Phospholipase C activation by Gq",
        "ODE", gpcr, src,
        domain="GPCR", model_origin="IP3-Gq")

    # Beta-arrestin
    add_formula(conn, "Beta-arrestin Recruitment",
        r"\frac{d[R-\beta arr]}{dt} = k_{arr} [R^*_{phos}][\beta arr] - k_{diss} [R-\beta arr]",
        "Arrestin-mediated receptor desensitization",
        "ODE", gpcr, src,
        domain="GPCR", model_origin="beta-arrestin")

    # === LIGAND-GATED ION CHANNELS ===
    log.info("--- Ligand-gated Ion Channels ---")

    lgics = [
        ("nAChR-muscle", "ACh", "(α1)2β1δε", "Na,K", 0, 25, 1.0, 3.0),
        ("nAChR-α4β2", "ACh", "neuronal high-affinity", "Na,K,Ca", 0, 15, 1.5, 5.0),
        ("nAChR-α7", "ACh", "neuronal fast", "Na,K,Ca", 0, 30, 0.5, 1.5),
        ("GABA-A-α1β2γ2", "GABA", "main inhibitory", "Cl", -70, 30, 1.0, 10.0),
        ("GABA-A-α2β3γ2", "GABA", "anxiolytic-sensitive", "Cl", -70, 25, 1.2, 12.0),
        ("GABA-A-α5β3γ2", "GABA", "extrasynaptic tonic", "Cl", -70, 20, 2.0, 50.0),
        ("GlyR-α1", "glycine", "spinal cord", "Cl", -70, 40, 0.8, 8.0),
        ("5-HT3", "serotonin", "nausea/vomiting", "Na,K", 0, 20, 1.0, 5.0),
        ("P2X1", "ATP", "smooth muscle", "Na,K,Ca", 0, 10, 0.3, 1.0),
        ("P2X4", "ATP", "microglial", "Na,K,Ca", 0, 8, 0.5, 2.0),
        ("P2X7", "ATP", "immune, pore-forming", "Na,K,Ca", 0, 5, 1.0, 5.0),
        ("ASIC1a", "H+", "acid sensing, fear", "Na", 0, 10, "pH", "pH"),
        ("ENaC", "constitutive", "epithelial sodium", "Na", 0, 5, "-", "-"),
    ]

    for name, ligand, function, ions, erev, gmax, tau_r, tau_d in lgics:
        fid = add_formula(conn, f"{name} Current",
            rf"I_{{{name}}} = g_{{{name}}} \cdot P_{{open}}([{ligand}]) \cdot (V - E_{{rev}})",
            f"{name}: {function}. Permeable to {ions}",
            "current_equation", lgic, src,
            domain="LGIC", model_origin=name)
        add_ion_channel(conn, fid, name, "ligand-gated", 1, None, None, erev, gmax)

        if tau_r != "-":
            add_formula(conn, f"{name} Kinetics",
                rf"P_{{open}} = \frac{{[{ligand}]^n}}{{EC_{{50}}^n + [{ligand}]^n}}",
                f"{name} open probability with Hill coefficient",
                "algebraic", lgic, src,
                domain="LGIC", model_origin=f"{name}-kinetics")

    # Desensitization models
    add_formula(conn, "LGIC Desensitization (3-state)",
        r"\begin{aligned} C &\xrightleftharpoons[k_{-1}]{k_1[L]} O \xrightleftharpoons[k_{-2}]{k_2} D \end{aligned}",
        "Closed-Open-Desensitized model",
        "ODE", lgic, src,
        domain="LGIC", model_origin="COD-model")

    # === RECEPTOR TYROSINE KINASES ===
    log.info("--- Receptor Tyrosine Kinases ---")

    rtks = [
        ("EGFR", "EGF,TGFα", "cell proliferation", "RAS-MAPK, PI3K-AKT"),
        ("HER2", "none (constitutive)", "breast cancer", "RAS-MAPK, PI3K-AKT"),
        ("PDGFR", "PDGF", "wound healing", "RAS-MAPK, PI3K-AKT, PLCγ"),
        ("VEGFR2", "VEGF", "angiogenesis", "RAS-MAPK, PI3K-AKT"),
        ("FGFR1", "FGF", "development", "RAS-MAPK, PI3K-AKT, PLCγ"),
        ("InsR", "insulin", "glucose uptake", "PI3K-AKT, RAS-MAPK"),
        ("IGF1R", "IGF-1", "growth", "PI3K-AKT, RAS-MAPK"),
        ("TrkA", "NGF", "neuronal survival", "RAS-MAPK, PI3K-AKT, PLCγ"),
        ("TrkB", "BDNF,NT-4", "synaptic plasticity", "RAS-MAPK, PI3K-AKT, PLCγ"),
        ("TrkC", "NT-3", "proprioception", "RAS-MAPK, PI3K-AKT"),
        ("EphA4", "ephrinA", "axon guidance", "RAS-MAPK, RhoGTPases"),
        ("EphB2", "ephrinB", "synapse formation", "RAS-MAPK, RhoGTPases"),
        ("Met", "HGF", "cell motility", "RAS-MAPK, PI3K-AKT"),
        ("Kit", "SCF", "hematopoiesis", "RAS-MAPK, PI3K-AKT"),
        ("RET", "GDNF", "neural crest", "RAS-MAPK, PI3K-AKT"),
    ]

    for name, ligands, function, pathways in rtks:
        fid = add_formula(conn, f"{name} Dimerization & Activation",
            rf"\frac{{d[{name}_2^*]}}{{dt}} = k_{{dim}} [{name}-L]^2 - k_{{undim}} [{name}_2^*]",
            f"{name}: Ligands: {ligands}. Function: {function}. Activates: {pathways}",
            "ODE", rtk, src,
            domain="RTK", model_origin=name)

        add_formula(conn, f"{name} Autophosphorylation",
            rf"\frac{{d[{name}_{{phos}}]}}{{dt}} = k_{{auto}} [{name}_2^*] - k_{{dephos}} [{name}_{{phos}}]",
            f"{name} trans-autophosphorylation and dephosphorylation",
            "ODE", rtk, src,
            domain="RTK", model_origin=f"{name}-phos")

    # SH2 domain recruitment
    add_formula(conn, "SH2 Domain Recruitment",
        r"[Adapter-pY] = \frac{[Adapter]_T [pY]}{K_d + [pY]}",
        "SH2/PTB domain binding to phosphotyrosine",
        "algebraic", rtk, lit,
        domain="RTK", model_origin="SH2-binding")

    # === NUCLEAR RECEPTORS ===
    log.info("--- Nuclear Receptors ---")

    nrs = [
        ("GR", "cortisol", "stress response, metabolism"),
        ("MR", "aldosterone", "sodium balance"),
        ("PR", "progesterone", "reproduction"),
        ("AR", "testosterone,DHT", "male development"),
        ("ERα", "estradiol", "reproduction, bone"),
        ("ERβ", "estradiol", "brain, cardiovascular"),
        ("TRα", "T3", "metabolism, development"),
        ("TRβ", "T3", "metabolism, heart"),
        ("RARα", "retinoic acid", "development"),
        ("RXRα", "9-cis-RA", "heterodimer partner"),
        ("VDR", "calcitriol", "calcium homeostasis"),
        ("PPARα", "fatty acids", "lipid metabolism"),
        ("PPARγ", "fatty acids", "adipogenesis"),
        ("PPARδ", "fatty acids", "fatty acid oxidation"),
        ("LXRα", "oxysterols", "cholesterol efflux"),
        ("FXR", "bile acids", "bile acid metabolism"),
    ]

    for name, ligands, function in nrs:
        add_formula(conn, f"{name} Transcriptional Activation",
            rf"Rate_{{transcription}} = k_{{basal}} + k_{{max}} \frac{{[{name}-L]^n}}{{K_d^n + [{name}-L]^n}}",
            f"{name}: Ligands: {ligands}. Function: {function}",
            "algebraic", nuclear, src,
            domain="nuclear-receptor", model_origin=name)

        add_formula(conn, f"{name} Ligand Binding",
            rf"\frac{{d[{name}-L]}}{{dt}} = k_{{on}} [{name}][L] - k_{{off}} [{name}-L]",
            f"{name} ligand binding kinetics",
            "ODE", nuclear, src,
            domain="nuclear-receptor", model_origin=f"{name}-binding")

    print_summary(conn, "RECEPTORS", start)
    conn.close()

if __name__ == "__main__":
    run()
