#!/usr/bin/env python3
"""Expansion module 4: Cell signaling cascades."""

from expand_base import *

def run():
    conn = get_conn()
    start = count_formulas(conn)
    log.info("="*50)
    log.info("EXPANDING: SIGNALING CASCADES")
    log.info("="*50)

    src = get_source_id(conn, 'BioModels Database')
    lit = get_source_id(conn, 'Scientific Literature')

    sig = add_category(conn, 'Cell Signaling', 'Biochemistry')
    mapk = add_category(conn, 'MAPK Cascade', 'Cell Signaling', 'Mitogen-activated protein kinase')
    pi3k = add_category(conn, 'PI3K-AKT', 'Cell Signaling', 'Survival signaling')
    calc = add_category(conn, 'Calcium Signaling', 'Cell Signaling', 'Ca2+ dynamics')
    camp = add_category(conn, 'cAMP-PKA', 'Cell Signaling', 'Cyclic AMP signaling')
    nfkb = add_category(conn, 'NF-κB', 'Cell Signaling', 'Inflammatory signaling')
    wnt = add_category(conn, 'Wnt', 'Cell Signaling', 'Wnt/β-catenin pathway')
    notch = add_category(conn, 'Notch', 'Cell Signaling', 'Notch signaling')
    tgfb = add_category(conn, 'TGF-β/SMAD', 'Cell Signaling', 'TGF-beta pathway')
    jak = add_category(conn, 'JAK-STAT', 'Cell Signaling', 'Cytokine signaling')

    # === MAPK CASCADE ===
    log.info("--- MAPK Cascade ---")

    # Full 3-tier cascade
    add_formula(conn, "MAPKKK Activation (Raf)",
        r"\frac{d[Raf^*]}{dt} = \frac{k_1 [RasGTP][Raf]}{K_{m1} + [Raf]} - \frac{k_2 [Raf^*]}{K_{m2} + [Raf^*]}",
        "Ras-GTP activates Raf (MAPKKK)",
        "ODE", mapk, src,
        domain="MAPK", model_origin="Raf")

    add_formula(conn, "MAPKK Activation (MEK)",
        r"\frac{d[MEK^*]}{dt} = \frac{k_3 [Raf^*][MEK]}{K_{m3} + [MEK]} - \frac{k_4 [MEK^*]}{K_{m4} + [MEK^*]}",
        "Raf activates MEK (MAPKK) - dual phosphorylation",
        "ODE", mapk, src,
        domain="MAPK", model_origin="MEK")

    add_formula(conn, "MAPKK Double Phosphorylation",
        r"\frac{d[MEK_{pp}]}{dt} = \frac{k_3' [Raf^*][MEK_p]}{K_{m3'} + [MEK_p]} - \frac{k_4' [MEK_{pp}]}{K_{m4'} + [MEK_{pp}]}",
        "Second phosphorylation of MEK",
        "ODE", mapk, src,
        domain="MAPK", model_origin="MEK-pp")

    add_formula(conn, "MAPK Activation (ERK)",
        r"\frac{d[ERK^*]}{dt} = \frac{k_5 [MEK^*][ERK]}{K_{m5} + [ERK]} - \frac{k_6 [ERK^*]}{K_{m6} + [ERK^*]}",
        "MEK activates ERK (MAPK)",
        "ODE", mapk, src,
        domain="MAPK", model_origin="ERK")

    add_formula(conn, "ERK Double Phosphorylation",
        r"\frac{d[ERK_{pp}]}{dt} = \frac{k_5' [MEK^*][ERK_p]}{K_{m5'} + [ERK_p]} - \frac{k_6' [ERK_{pp}]}{K_{m6'} + [ERK_{pp}]}",
        "Second phosphorylation of ERK",
        "ODE", mapk, src,
        domain="MAPK", model_origin="ERK-pp")

    # Feedback loops
    add_formula(conn, "ERK Negative Feedback to Raf",
        r"k_1^{eff} = \frac{k_1}{1 + [ERK^*]/K_i}",
        "ERK phosphorylates Raf reducing its activation",
        "algebraic", mapk, src,
        domain="MAPK", model_origin="ERK-feedback")

    add_formula(conn, "ERK Negative Feedback to SOS",
        r"\frac{d[SOS]}{dt} = -k_{phos} [ERK^*][SOS] + k_{dephos} [SOS_p]",
        "ERK phosphorylates SOS reducing Ras activation",
        "ODE", mapk, src,
        domain="MAPK", model_origin="SOS-feedback")

    # Other MAPK pathways
    mapk_pathways = [
        ("JNK", "stress, apoptosis", "MKK4/7", "c-Jun"),
        ("p38", "stress, inflammation", "MKK3/6", "ATF2"),
        ("ERK5", "growth, survival", "MEK5", "MEF2"),
    ]

    for name, function, upstream, downstream in mapk_pathways:
        add_formula(conn, f"{name} Activation",
            rf"\frac{{d[{name}^*]}}{{dt}} = \frac{{k_{{act}} [{upstream}^*][{name}]}}{{K_m + [{name}]}} - \frac{{k_{{deact}} [{name}^*]}}{{K_m' + [{name}^*]}}",
            f"{name} MAPK pathway: {function}. Activates {downstream}",
            "ODE", mapk, src,
            domain="MAPK", model_origin=name)

    # === PI3K-AKT PATHWAY ===
    log.info("--- PI3K-AKT Pathway ---")

    add_formula(conn, "PI3K Activation",
        r"\frac{d[PIP_3]}{dt} = k_{PI3K} [RTK^*][PIP_2] - k_{PTEN} [PIP_3]",
        "PI3K produces PIP3, PTEN degrades it",
        "ODE", pi3k, src,
        domain="PI3K-AKT", model_origin="PI3K")

    add_formula(conn, "AKT Membrane Recruitment",
        r"[AKT_{mem}] = \frac{[AKT][PIP_3]}{K_d + [PIP_3]}",
        "AKT recruitment to membrane via PH domain",
        "algebraic", pi3k, src,
        domain="PI3K-AKT", model_origin="AKT-recruitment")

    add_formula(conn, "AKT Phosphorylation (PDK1)",
        r"\frac{d[AKT_{T308}]}{dt} = k_{PDK1} [PDK1][AKT_{mem}] - k_{PP2A} [AKT_{T308}]",
        "PDK1 phosphorylates AKT at T308",
        "ODE", pi3k, src,
        domain="PI3K-AKT", model_origin="AKT-T308")

    add_formula(conn, "AKT Phosphorylation (mTORC2)",
        r"\frac{d[AKT_{S473}]}{dt} = k_{mTORC2} [mTORC2][AKT_{T308}] - k_{PHLPP} [AKT_{S473}]",
        "mTORC2 phosphorylates AKT at S473 for full activation",
        "ODE", pi3k, src,
        domain="PI3K-AKT", model_origin="AKT-S473")

    # AKT targets
    akt_targets = [
        ("GSK3β", "inhibition", "glycogen synthesis, Wnt"),
        ("FOXO", "inhibition", "apoptosis genes"),
        ("BAD", "inhibition", "pro-apoptotic"),
        ("TSC2", "inhibition", "mTORC1 activation"),
        ("MDM2", "activation", "p53 degradation"),
        ("AS160", "activation", "GLUT4 translocation"),
    ]

    for target, effect, function in akt_targets:
        add_formula(conn, f"AKT → {target} ({effect})",
            rf"\frac{{d[{target}_{{phos}}]}}{{dt}} = k_{{AKT}} [AKT^*][{target}] - k_{{PP}} [{target}_{{phos}}]",
            f"AKT {effect} of {target}: {function}",
            "ODE", pi3k, src,
            domain="PI3K-AKT", model_origin=f"AKT-{target}")

    # mTOR signaling
    add_formula(conn, "mTORC1 Activation",
        r"\frac{d[mTORC1^*]}{dt} = k_{act} [Rheb_{GTP}][mTORC1] - k_{deact} [mTORC1^*]",
        "Rheb-GTP activates mTORC1 (when TSC is inhibited)",
        "ODE", pi3k, src,
        domain="mTOR", model_origin="mTORC1")

    add_formula(conn, "S6K Activation by mTORC1",
        r"\frac{d[S6K^*]}{dt} = k_{mTORC1} [mTORC1^*][S6K] - k_{PP} [S6K^*]",
        "mTORC1 activates S6K for protein synthesis",
        "ODE", pi3k, src,
        domain="mTOR", model_origin="S6K")

    add_formula(conn, "4E-BP1 Phosphorylation",
        r"\frac{d[4EBP1_p]}{dt} = k_{mTORC1} [mTORC1^*][4EBP1] - k_{PP} [4EBP1_p]",
        "mTORC1 phosphorylates 4E-BP1, releasing eIF4E",
        "ODE", pi3k, src,
        domain="mTOR", model_origin="4EBP1")

    # === CALCIUM SIGNALING ===
    log.info("--- Calcium Signaling ---")

    add_formula(conn, "IP3 Receptor (De Young-Bhalla)",
        r"J_{IP3R} = v_{IP3R} m_\infty^3 h^3 ([Ca^{2+}]_{ER} - [Ca^{2+}]_{cyt})",
        "IP3R calcium release with Ca and IP3 dependence",
        "algebraic", calc, src,
        domain="calcium", model_origin="IP3R-DYB")

    add_formula(conn, "IP3R m_infinity",
        r"m_\infty = \frac{[IP_3]}{K_{IP3} + [IP_3]} \cdot \frac{[Ca^{2+}]}{K_{act} + [Ca^{2+}]}",
        "IP3R activation by IP3 and Ca",
        "algebraic", calc, src,
        domain="calcium", model_origin="IP3R-m")

    add_formula(conn, "IP3R h (inactivation)",
        r"\frac{dh}{dt} = \frac{h_\infty - h}{\tau_h}, \quad h_\infty = \frac{K_{inh}}{K_{inh} + [Ca^{2+}]}",
        "IP3R Ca-dependent inactivation",
        "ODE", calc, src,
        domain="calcium", model_origin="IP3R-h")

    add_formula(conn, "Ryanodine Receptor (RyR)",
        r"J_{RyR} = v_{RyR} \frac{[Ca^{2+}]^n}{K_d^n + [Ca^{2+}]^n} ([Ca^{2+}]_{ER} - [Ca^{2+}]_{cyt})",
        "CICR through ryanodine receptor",
        "algebraic", calc, src,
        domain="calcium", model_origin="RyR")

    add_formula(conn, "SERCA Pump",
        r"J_{SERCA} = V_{SERCA} \frac{[Ca^{2+}]_{cyt}^2}{K_{SERCA}^2 + [Ca^{2+}]_{cyt}^2}",
        "SR/ER Ca-ATPase",
        "algebraic", calc, src,
        domain="calcium", model_origin="SERCA")

    add_formula(conn, "PMCA Pump",
        r"J_{PMCA} = V_{PMCA} \frac{[Ca^{2+}]_{cyt}}{K_{PMCA} + [Ca^{2+}]_{cyt}}",
        "Plasma membrane Ca-ATPase",
        "algebraic", calc, src,
        domain="calcium", model_origin="PMCA")

    add_formula(conn, "NCX (Na/Ca Exchanger)",
        r"J_{NCX} = k_{NCX} \left( [Na^+]_i^3 [Ca^{2+}]_o e^{\eta FV/RT} - [Na^+]_o^3 [Ca^{2+}]_i e^{(\eta-1)FV/RT} \right)",
        "Sodium-calcium exchanger",
        "algebraic", calc, src,
        domain="calcium", model_origin="NCX")

    add_formula(conn, "Calcium Buffering",
        r"\frac{d[CaB]}{dt} = k_{on} [Ca^{2+}][B] - k_{off} [CaB]",
        "Calcium binding to buffer proteins",
        "ODE", calc, src,
        domain="calcium", model_origin="Ca-buffer")

    add_formula(conn, "Calmodulin Binding",
        r"[CaM_{Ca4}] = [CaM]_T \frac{[Ca^{2+}]^4}{K_d^4 + [Ca^{2+}]^4}",
        "Four Ca2+ ions bind calmodulin cooperatively",
        "algebraic", calc, src,
        domain="calcium", model_origin="calmodulin")

    add_formula(conn, "CaMKII Activation",
        r"\frac{d[CaMKII^*]}{dt} = k_{act} [CaM_{Ca4}][CaMKII] - k_{PP1} [CaMKII^*]",
        "CaMKII activation by Ca/CaM",
        "ODE", calc, src,
        domain="calcium", model_origin="CaMKII")

    add_formula(conn, "CaMKII Autophosphorylation",
        r"\frac{d[CaMKII_{auto}]}{dt} = k_{auto} [CaMKII^*]^2 - k_{PP1} [CaMKII_{auto}]",
        "CaMKII autonomous activity after autophosphorylation",
        "ODE", calc, src,
        domain="calcium", model_origin="CaMKII-auto")

    add_formula(conn, "Calcineurin Activation",
        r"[CN^*] = [CN]_T \frac{[CaM_{Ca4}]}{K_d + [CaM_{Ca4}]}",
        "Calcineurin (PP2B) activation by Ca/CaM",
        "algebraic", calc, src,
        domain="calcium", model_origin="calcineurin")

    # === cAMP-PKA PATHWAY ===
    log.info("--- cAMP-PKA Pathway ---")

    add_formula(conn, "Adenylyl Cyclase (Gs-stimulated)",
        r"\frac{d[cAMP]}{dt} = V_{AC} \frac{[G_s^*]}{K_m + [G_s^*]} \frac{[ATP]}{K_{ATP} + [ATP]} - V_{PDE} \frac{[cAMP]}{K_m + [cAMP]}",
        "cAMP production by AC and degradation by PDE",
        "ODE", camp, src,
        domain="cAMP", model_origin="AC")

    add_formula(conn, "PKA Activation",
        r"[PKA_{active}] = [PKA]_T \frac{[cAMP]^4}{K_d^4 + [cAMP]^4}",
        "PKA activation by cAMP (4 binding sites)",
        "algebraic", camp, src,
        domain="cAMP", model_origin="PKA")

    add_formula(conn, "PKA Regulatory Subunit Dissociation",
        r"R_2C_2 + 4cAMP \rightleftharpoons R_2(cAMP)_4 + 2C",
        "PKA holoenzyme dissociation model",
        "algebraic", camp, src,
        domain="cAMP", model_origin="PKA-dissoc")

    add_formula(conn, "CREB Phosphorylation",
        r"\frac{d[CREB_p]}{dt} = k_{PKA} [PKA^*][CREB] - k_{PP1} [CREB_p]",
        "PKA phosphorylates CREB at Ser133",
        "ODE", camp, src,
        domain="cAMP", model_origin="CREB")

    add_formula(conn, "PDE4 Feedback",
        r"\frac{d[PDE4^*]}{dt} = k_{PKA} [PKA^*][PDE4] - k_{PP} [PDE4^*]",
        "PKA activates PDE4 (negative feedback)",
        "ODE", camp, src,
        domain="cAMP", model_origin="PDE4-feedback")

    # === NF-κB PATHWAY ===
    log.info("--- NF-κB Pathway ---")

    add_formula(conn, "IKK Activation",
        r"\frac{d[IKK^*]}{dt} = k_{act} [Signal][IKK] - k_{deact} [A20][IKK^*]",
        "IKK activation by upstream signals, inhibition by A20",
        "ODE", nfkb, src,
        domain="NF-kB", model_origin="IKK")

    add_formula(conn, "IκBα Phosphorylation",
        r"\frac{d[I\kappa B\alpha_p]}{dt} = k_{IKK} [IKK^*][I\kappa B\alpha] - k_{deg} [I\kappa B\alpha_p]",
        "IKK phosphorylates IκBα marking for degradation",
        "ODE", nfkb, src,
        domain="NF-kB", model_origin="IkBa-phos")

    add_formula(conn, "NF-κB Nuclear Translocation",
        r"\frac{d[NF\kappa B_{nuc}]}{dt} = k_{in} [NF\kappa B_{cyt}] - k_{out} [I\kappa B\alpha_{nuc}][NF\kappa B_{nuc}]",
        "Free NF-κB enters nucleus, IκBα exports it",
        "ODE", nfkb, src,
        domain="NF-kB", model_origin="NFkB-nuclear")

    add_formula(conn, "IκBα Transcription (Negative Feedback)",
        r"\frac{d[I\kappa B\alpha_{mRNA}]}{dt} = k_{tx} [NF\kappa B_{nuc}] - k_{deg} [I\kappa B\alpha_{mRNA}]",
        "NF-κB induces IκBα transcription",
        "ODE", nfkb, src,
        domain="NF-kB", model_origin="IkBa-tx")

    add_formula(conn, "A20 Transcription (Negative Feedback)",
        r"\frac{d[A20_{mRNA}]}{dt} = k_{tx} [NF\kappa B_{nuc}] - k_{deg} [A20_{mRNA}]",
        "NF-κB induces A20 transcription",
        "ODE", nfkb, src,
        domain="NF-kB", model_origin="A20-tx")

    # === WNT PATHWAY ===
    log.info("--- Wnt/β-catenin Pathway ---")

    add_formula(conn, "β-catenin Destruction Complex",
        r"\frac{d[\beta cat]}{dt} = k_{syn} - k_{dest} [APC \cdot Axin \cdot GSK3] [\beta cat] - k_{deg} [\beta cat]",
        "APC/Axin/GSK3 complex targets β-catenin for degradation",
        "ODE", wnt, src,
        domain="Wnt", model_origin="beta-cat-dest")

    add_formula(conn, "Wnt-Frizzled Binding",
        r"\frac{d[Wnt \cdot Fz]}{dt} = k_{on} [Wnt][Fz] - k_{off} [Wnt \cdot Fz]",
        "Wnt ligand binds Frizzled receptor",
        "ODE", wnt, src,
        domain="Wnt", model_origin="Wnt-Fz")

    add_formula(conn, "Dishevelled Activation",
        r"\frac{d[Dvl^*]}{dt} = k_{act} [Wnt \cdot Fz][Dvl] - k_{deact} [Dvl^*]",
        "Dishevelled activation inhibits destruction complex",
        "ODE", wnt, src,
        domain="Wnt", model_origin="Dvl")

    add_formula(conn, "β-catenin Nuclear Accumulation",
        r"\frac{d[\beta cat_{nuc}]}{dt} = k_{in} [\beta cat] - k_{out} [\beta cat_{nuc}]",
        "β-catenin nuclear import",
        "ODE", wnt, src,
        domain="Wnt", model_origin="beta-cat-nuc")

    add_formula(conn, "TCF/LEF Target Gene Activation",
        r"Rate_{tx} = k_{basal} + k_{max} \frac{[\beta cat_{nuc}]^n}{K_d^n + [\beta cat_{nuc}]^n}",
        "β-catenin/TCF activates Wnt target genes",
        "algebraic", wnt, src,
        domain="Wnt", model_origin="TCF-target")

    # === NOTCH PATHWAY ===
    log.info("--- Notch Pathway ---")

    add_formula(conn, "Notch-Delta Binding",
        r"\frac{d[N \cdot D]}{dt} = k_{on} [N][D_{trans}] - k_{off} [N \cdot D]",
        "Notch receptor binds Delta ligand on neighboring cell",
        "ODE", notch, src,
        domain="Notch", model_origin="N-D-binding")

    add_formula(conn, "Notch Cleavage (γ-secretase)",
        r"\frac{d[NICD]}{dt} = k_{cleave} [N \cdot D] - k_{deg} [NICD]",
        "γ-secretase releases Notch intracellular domain",
        "ODE", notch, src,
        domain="Notch", model_origin="NICD")

    add_formula(conn, "Hes/Hey Transcription",
        r"\frac{d[Hes]}{dt} = k_{tx} [NICD \cdot CSL] - k_{deg} [Hes]",
        "NICD/CSL complex activates Hes/Hey genes",
        "ODE", notch, src,
        domain="Notch", model_origin="Hes")

    add_formula(conn, "Lateral Inhibition",
        r"\frac{d[D]}{dt} = k_{syn} \frac{K_i^n}{K_i^n + [Hes]^n} - k_{deg} [D]",
        "Hes represses Delta, creating lateral inhibition",
        "ODE", notch, src,
        domain="Notch", model_origin="lateral-inhib")

    # === TGF-β/SMAD PATHWAY ===
    log.info("--- TGF-β/SMAD Pathway ---")

    add_formula(conn, "TGF-β Receptor Activation",
        r"\frac{d[TGF\beta R^*]}{dt} = k_{bind} [TGF\beta][TGF\beta R] - k_{off} [TGF\beta R^*]",
        "TGF-β binds and activates receptor complex",
        "ODE", tgfb, src,
        domain="TGF-beta", model_origin="TGFbR")

    add_formula(conn, "SMAD2/3 Phosphorylation",
        r"\frac{d[SMAD_{23p}]}{dt} = k_{phos} [TGF\beta R^*][SMAD_{23}] - k_{dephos} [SMAD_{23p}]",
        "Receptor phosphorylates SMAD2/3",
        "ODE", tgfb, src,
        domain="TGF-beta", model_origin="SMAD23")

    add_formula(conn, "SMAD Complex Formation",
        r"\frac{d[SMAD_{23p} \cdot SMAD4]}{dt} = k_{on} [SMAD_{23p}][SMAD4] - k_{off} [SMAD_{23p} \cdot SMAD4]",
        "Phospho-SMAD2/3 binds SMAD4",
        "ODE", tgfb, src,
        domain="TGF-beta", model_origin="SMAD-complex")

    add_formula(conn, "SMAD Nuclear Translocation",
        r"\frac{d[SMAD_{nuc}]}{dt} = k_{in} [SMAD_{23p} \cdot SMAD4] - k_{out} [SMAD_{nuc}]",
        "SMAD complex enters nucleus",
        "ODE", tgfb, src,
        domain="TGF-beta", model_origin="SMAD-nuc")

    # === JAK-STAT PATHWAY ===
    log.info("--- JAK-STAT Pathway ---")

    add_formula(conn, "Cytokine Receptor Activation",
        r"\frac{d[R^*]}{dt} = k_{bind} [Cytokine][R] - k_{off} [R^*]",
        "Cytokine binding activates receptor dimerization",
        "ODE", jak, src,
        domain="JAK-STAT", model_origin="cytokine-R")

    add_formula(conn, "JAK Activation",
        r"\frac{d[JAK^*]}{dt} = k_{act} [R^*][JAK] - k_{SOCS} [SOCS][JAK^*]",
        "JAK trans-phosphorylation and SOCS inhibition",
        "ODE", jak, src,
        domain="JAK-STAT", model_origin="JAK")

    add_formula(conn, "STAT Phosphorylation",
        r"\frac{d[STAT_p]}{dt} = k_{JAK} [JAK^*][STAT] - k_{PTP} [STAT_p]",
        "JAK phosphorylates STAT",
        "ODE", jak, src,
        domain="JAK-STAT", model_origin="STAT")

    add_formula(conn, "STAT Dimerization",
        r"\frac{d[STAT_p \cdot STAT_p]}{dt} = k_{dim} [STAT_p]^2 - k_{undim} [STAT_p \cdot STAT_p]",
        "Phospho-STAT dimerizes via SH2 domains",
        "ODE", jak, src,
        domain="JAK-STAT", model_origin="STAT-dimer")

    add_formula(conn, "SOCS Transcription (Negative Feedback)",
        r"\frac{d[SOCS_{mRNA}]}{dt} = k_{tx} [STAT_{nuc}] - k_{deg} [SOCS_{mRNA}]",
        "STAT induces SOCS expression",
        "ODE", jak, src,
        domain="JAK-STAT", model_origin="SOCS")

    print_summary(conn, "SIGNALING CASCADES", start)
    conn.close()

if __name__ == "__main__":
    run()
