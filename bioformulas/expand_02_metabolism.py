#!/usr/bin/env python3
"""Expansion module 2: Metabolic pathways - glycolysis, TCA, OXPHOS, etc."""

from expand_base import (
    DB_PATH, get_conn, get_source_id, get_category_id, add_category,
    add_formula, add_ion_channel, add_synapse, add_enzyme, add_neuron,
    add_plasticity, count_formulas, print_summary, log
)

def run():
    conn = get_conn()
    start = count_formulas(conn)
    log.info("="*50)
    log.info("EXPANDING: METABOLIC PATHWAYS")
    log.info("="*50)

    src = get_source_id(conn, 'BioModels Database')
    lit = get_source_id(conn, 'Scientific Literature')

    # Categories
    met = add_category(conn, 'Metabolism', None, 'Metabolic pathways and reactions')
    glyc = add_category(conn, 'Glycolysis', 'Metabolism', 'Glucose breakdown')
    tca = add_category(conn, 'TCA Cycle', 'Metabolism', 'Citric acid cycle')
    oxphos = add_category(conn, 'Oxidative Phosphorylation', 'Metabolism', 'Electron transport chain')
    ppp = add_category(conn, 'Pentose Phosphate Pathway', 'Metabolism', 'NADPH and ribose production')
    gluconeo = add_category(conn, 'Gluconeogenesis', 'Metabolism', 'Glucose synthesis')
    fatox = add_category(conn, 'Fatty Acid Oxidation', 'Metabolism', 'Beta oxidation')
    aasyn = add_category(conn, 'Amino Acid Metabolism', 'Metabolism', 'Amino acid synthesis and degradation')

    # === GLYCOLYSIS ===
    log.info("--- Glycolysis (10 reactions) ---")

    glycolysis_rxns = [
        ("Hexokinase", "HK", "Glucose + ATP → G6P + ADP", "glucose", "G6P", 0.1, 100),
        ("Phosphoglucose Isomerase", "PGI", "G6P ⇌ F6P", "G6P", "F6P", 0.3, 500),
        ("Phosphofructokinase-1", "PFK1", "F6P + ATP → F1,6BP + ADP", "F6P", "F1,6BP", 0.05, 80),
        ("Aldolase", "ALDO", "F1,6BP ⇌ DHAP + G3P", "F1,6BP", "G3P", 0.02, 100),
        ("Triose Phosphate Isomerase", "TPI", "DHAP ⇌ G3P", "DHAP", "G3P", 0.4, 1000),
        ("G3P Dehydrogenase", "GAPDH", "G3P + NAD+ + Pi ⇌ 1,3BPG + NADH", "G3P", "1,3BPG", 0.05, 200),
        ("Phosphoglycerate Kinase", "PGK", "1,3BPG + ADP ⇌ 3PG + ATP", "1,3BPG", "3PG", 0.3, 400),
        ("Phosphoglycerate Mutase", "PGM", "3PG ⇌ 2PG", "3PG", "2PG", 0.1, 200),
        ("Enolase", "ENO", "2PG ⇌ PEP + H2O", "2PG", "PEP", 0.05, 150),
        ("Pyruvate Kinase", "PK", "PEP + ADP → Pyruvate + ATP", "PEP", "pyruvate", 0.15, 200),
    ]

    for name, abbr, rxn, sub, prod, km, vmax in glycolysis_rxns:
        fid = add_formula(conn, f"{name} ({abbr})",
            rf"v_{{{abbr}}} = \frac{{V_{{max}} [{sub}]}}{{K_m + [{sub}]}}",
            f"Glycolysis step: {rxn}",
            "rate_equation", glyc, src,
            python_code=f"v = Vmax * {sub} / (Km + {sub})",
            domain="glycolysis", model_origin=abbr)
        add_enzyme(conn, fid, name, "michaelis-menten", sub, prod, km, vmax)

    # PFK1 allosteric regulation (key regulatory enzyme)
    fid = add_formula(conn, "PFK1 Allosteric Regulation",
        r"v_{PFK1} = V_{max} \frac{[F6P]^n [ATP]}{(K_{F6P}^n + [F6P]^n)(K_{ATP} + [ATP])} \cdot \frac{K_i^m}{K_i^m + [ATP]^m} \cdot \frac{[AMP]^p + K_a^p}{K_a^p}",
        "PFK1 with ATP inhibition, AMP activation, F6P cooperativity",
        "rate_equation", glyc, src,
        domain="glycolysis", model_origin="PFK1-allosteric")
    add_enzyme(conn, fid, "PFK1", "allosteric", "F6P,ATP", "F1,6BP", hill=2.0)

    # Pyruvate kinase allosteric
    fid = add_formula(conn, "Pyruvate Kinase Allosteric",
        r"v_{PK} = V_{max} \frac{[PEP]^n [ADP]}{(K_{PEP}^n + [PEP]^n)(K_{ADP} + [ADP])} \cdot \frac{[F1,6BP]}{K_a + [F1,6BP]}",
        "PK with F1,6BP feedforward activation",
        "rate_equation", glyc, src,
        domain="glycolysis", model_origin="PK-allosteric")
    add_enzyme(conn, fid, "PK", "allosteric", "PEP,ADP", "pyruvate,ATP", hill=3.0)

    # === TCA CYCLE ===
    log.info("--- TCA Cycle (8 reactions) ---")

    tca_rxns = [
        ("Citrate Synthase", "CS", "Acetyl-CoA + OAA → Citrate + CoA", "acetyl-CoA,OAA", "citrate", 0.005, 50),
        ("Aconitase", "ACO", "Citrate ⇌ Isocitrate", "citrate", "isocitrate", 0.2, 100),
        ("Isocitrate Dehydrogenase", "IDH", "Isocitrate + NAD+ → α-KG + CO2 + NADH", "isocitrate", "alpha-KG", 0.05, 30),
        ("α-Ketoglutarate Dehydrogenase", "OGDH", "α-KG + NAD+ + CoA → Succinyl-CoA + CO2 + NADH", "alpha-KG", "succinyl-CoA", 0.1, 25),
        ("Succinyl-CoA Synthetase", "SCS", "Succinyl-CoA + GDP + Pi ⇌ Succinate + GTP + CoA", "succinyl-CoA", "succinate", 0.05, 40),
        ("Succinate Dehydrogenase", "SDH", "Succinate + FAD → Fumarate + FADH2", "succinate", "fumarate", 0.02, 60),
        ("Fumarase", "FUM", "Fumarate + H2O ⇌ Malate", "fumarate", "malate", 0.01, 200),
        ("Malate Dehydrogenase", "MDH", "Malate + NAD+ ⇌ OAA + NADH", "malate", "OAA", 0.03, 150),
    ]

    for name, abbr, rxn, sub, prod, km, vmax in tca_rxns:
        fid = add_formula(conn, f"{name} ({abbr})",
            rf"v_{{{abbr}}} = \frac{{V_{{max}} [S]}}{{K_m + [S]}}",
            f"TCA cycle: {rxn}",
            "rate_equation", tca, src,
            domain="TCA-cycle", model_origin=abbr)
        add_enzyme(conn, fid, name, "michaelis-menten", sub, prod, km, vmax)

    # IDH regulation (key control point)
    fid = add_formula(conn, "IDH NAD-dependent Regulation",
        r"v_{IDH} = V_{max} \frac{[Isocitrate]^n [NAD^+]}{(K_m^n + [Isocitrate]^n)(K_{NAD} + [NAD^+])} \cdot \frac{K_i}{K_i + [NADH]} \cdot \frac{[ADP] + K_a}{K_a}",
        "IDH with NADH product inhibition and ADP activation",
        "rate_equation", tca, src,
        domain="TCA-cycle", model_origin="IDH-regulated")
    add_enzyme(conn, fid, "IDH", "allosteric", "isocitrate,NAD", "alpha-KG,NADH", hill=2.0)

    # === OXIDATIVE PHOSPHORYLATION ===
    log.info("--- Oxidative Phosphorylation ---")

    # Complex I
    fid = add_formula(conn, "Complex I (NADH Dehydrogenase)",
        r"v_{CI} = k_{CI} [NADH] [Q] \exp\left(\frac{n_H F \Delta\Psi}{RT}\right)",
        "NADH:ubiquinone oxidoreductase, proton pumping",
        "rate_equation", oxphos, src,
        domain="OXPHOS", model_origin="complex-I")
    add_enzyme(conn, fid, "Complex I", "electron-transport", "NADH,Q", "NAD,QH2")

    # Complex II
    fid = add_formula(conn, "Complex II (Succinate Dehydrogenase)",
        r"v_{CII} = \frac{V_{max} [Succinate] [Q]}{(K_{Succ} + [Succinate])(K_Q + [Q])}",
        "Succinate:ubiquinone oxidoreductase (no proton pumping)",
        "rate_equation", oxphos, src,
        domain="OXPHOS", model_origin="complex-II")
    add_enzyme(conn, fid, "Complex II", "electron-transport", "succinate,Q", "fumarate,QH2")

    # Complex III
    fid = add_formula(conn, "Complex III (Cytochrome bc1)",
        r"v_{CIII} = k_{CIII} [QH_2] [cytc_{ox}] \exp\left(\frac{2 F \Delta\Psi}{RT}\right)",
        "Ubiquinol:cytochrome c oxidoreductase, Q cycle",
        "rate_equation", oxphos, src,
        domain="OXPHOS", model_origin="complex-III")
    add_enzyme(conn, fid, "Complex III", "electron-transport", "QH2,cytc_ox", "Q,cytc_red")

    # Complex IV
    fid = add_formula(conn, "Complex IV (Cytochrome c Oxidase)",
        r"v_{CIV} = k_{CIV} [cytc_{red}]^4 [O_2] \exp\left(\frac{4 F \Delta\Psi}{RT}\right)",
        "Cytochrome c oxidase, final electron acceptor",
        "rate_equation", oxphos, src,
        domain="OXPHOS", model_origin="complex-IV")
    add_enzyme(conn, fid, "Complex IV", "electron-transport", "cytc_red,O2", "cytc_ox,H2O")

    # Complex V (ATP Synthase)
    fid = add_formula(conn, "ATP Synthase (Complex V)",
        r"v_{CV} = k_f [ADP][P_i] \exp\left(\frac{n F \Delta\Psi}{RT}\right) - k_r [ATP]",
        "F1F0 ATP synthase, chemiosmotic coupling",
        "rate_equation", oxphos, src,
        domain="OXPHOS", model_origin="ATP-synthase")
    add_enzyme(conn, fid, "ATP Synthase", "rotary-motor", "ADP,Pi", "ATP")

    # Proton motive force
    add_formula(conn, "Proton Motive Force",
        r"\Delta p = \Delta\Psi - \frac{2.303 RT}{F} \Delta pH",
        "Electrochemical proton gradient",
        "algebraic", oxphos, lit,
        python_code="Delta_p = Delta_Psi - 2.303 * R * T / F * Delta_pH",
        domain="OXPHOS", model_origin="pmf")

    # ANT (adenine nucleotide translocator)
    add_formula(conn, "Adenine Nucleotide Translocator",
        r"v_{ANT} = V_{max} \frac{[ADP]_c [ATP]_m - [ADP]_m [ATP]_c / K_{eq}}{(K_{ADP} + [ADP]_c)(K_{ATP} + [ATP]_m)}",
        "ATP/ADP exchange across inner mitochondrial membrane",
        "rate_equation", oxphos, src,
        domain="OXPHOS", model_origin="ANT")

    # === PENTOSE PHOSPHATE PATHWAY ===
    log.info("--- Pentose Phosphate Pathway ---")

    ppp_rxns = [
        ("G6P Dehydrogenase", "G6PD", "G6P + NADP+ → 6PGL + NADPH", "G6P", "6PGL", 0.02, 50),
        ("6-Phosphogluconolactonase", "6PGL", "6PGL + H2O → 6PG", "6PGL", "6PG", 0.1, 200),
        ("6PG Dehydrogenase", "6PGD", "6PG + NADP+ → Ru5P + CO2 + NADPH", "6PG", "Ru5P", 0.03, 40),
        ("Ribose-5-P Isomerase", "RPI", "Ru5P ⇌ R5P", "Ru5P", "R5P", 0.2, 500),
        ("Ribulose-5-P Epimerase", "RPE", "Ru5P ⇌ Xu5P", "Ru5P", "Xu5P", 0.15, 400),
        ("Transketolase 1", "TK1", "R5P + Xu5P ⇌ S7P + G3P", "R5P,Xu5P", "S7P,G3P", 0.1, 100),
        ("Transaldolase", "TA", "S7P + G3P ⇌ E4P + F6P", "S7P,G3P", "E4P,F6P", 0.05, 80),
        ("Transketolase 2", "TK2", "Xu5P + E4P ⇌ F6P + G3P", "Xu5P,E4P", "F6P,G3P", 0.1, 100),
    ]

    for name, abbr, rxn, sub, prod, km, vmax in ppp_rxns:
        fid = add_formula(conn, f"{name} ({abbr})",
            rf"v_{{{abbr}}} = \frac{{V_{{max}} [S]}}{{K_m + [S]}}",
            f"PPP: {rxn}",
            "rate_equation", ppp, src,
            domain="PPP", model_origin=abbr)
        add_enzyme(conn, fid, name, "michaelis-menten", sub, prod, km, vmax)

    # === GLUCONEOGENESIS ===
    log.info("--- Gluconeogenesis ---")

    gluconeo_rxns = [
        ("Pyruvate Carboxylase", "PC", "Pyruvate + CO2 + ATP → OAA + ADP + Pi", "pyruvate,CO2,ATP", "OAA", 0.2, 30),
        ("PEP Carboxykinase", "PEPCK", "OAA + GTP → PEP + CO2 + GDP", "OAA,GTP", "PEP", 0.1, 25),
        ("Fructose-1,6-bisphosphatase", "FBP1", "F1,6BP + H2O → F6P + Pi", "F1,6BP", "F6P", 0.005, 20),
        ("Glucose-6-phosphatase", "G6Pase", "G6P + H2O → Glucose + Pi", "G6P", "glucose", 0.01, 40),
    ]

    for name, abbr, rxn, sub, prod, km, vmax in gluconeo_rxns:
        fid = add_formula(conn, f"{name} ({abbr})",
            rf"v_{{{abbr}}} = \frac{{V_{{max}} [S]}}{{K_m + [S]}}",
            f"Gluconeogenesis: {rxn}",
            "rate_equation", gluconeo, src,
            domain="gluconeogenesis", model_origin=abbr)
        add_enzyme(conn, fid, name, "michaelis-menten", sub, prod, km, vmax)

    # === FATTY ACID OXIDATION ===
    log.info("--- Fatty Acid Beta-Oxidation ---")

    betaox_rxns = [
        ("Acyl-CoA Dehydrogenase", "ACAD", "Acyl-CoA + FAD → Enoyl-CoA + FADH2", "acyl-CoA", "enoyl-CoA", 0.01, 15),
        ("Enoyl-CoA Hydratase", "ECH", "Enoyl-CoA + H2O → 3-Hydroxyacyl-CoA", "enoyl-CoA", "3-hydroxyacyl-CoA", 0.05, 100),
        ("3-Hydroxyacyl-CoA Dehydrogenase", "HADH", "3-Hydroxyacyl-CoA + NAD+ → 3-Ketoacyl-CoA + NADH", "3-hydroxyacyl-CoA", "3-ketoacyl-CoA", 0.02, 40),
        ("3-Ketoacyl-CoA Thiolase", "ACAT", "3-Ketoacyl-CoA + CoA → Acyl-CoA(n-2) + Acetyl-CoA", "3-ketoacyl-CoA", "acetyl-CoA", 0.01, 50),
    ]

    for name, abbr, rxn, sub, prod, km, vmax in betaox_rxns:
        fid = add_formula(conn, f"{name} ({abbr})",
            rf"v_{{{abbr}}} = \frac{{V_{{max}} [S]}}{{K_m + [S]}}",
            f"Beta-oxidation: {rxn}",
            "rate_equation", fatox, src,
            domain="beta-oxidation", model_origin=abbr)
        add_enzyme(conn, fid, name, "michaelis-menten", sub, prod, km, vmax)

    # CPT1/CPT2 (carnitine shuttle)
    fid = add_formula(conn, "CPT1 (Carnitine Palmitoyltransferase 1)",
        r"v_{CPT1} = \frac{V_{max} [Acyl-CoA] [Carnitine]}{(K_{AcylCoA} + [Acyl-CoA])(K_{Carn} + [Carnitine])} \cdot \frac{K_i}{K_i + [Malonyl-CoA]}",
        "Rate-limiting step of fatty acid import, inhibited by malonyl-CoA",
        "rate_equation", fatox, src,
        domain="beta-oxidation", model_origin="CPT1")
    add_enzyme(conn, fid, "CPT1", "regulated", "acyl-CoA,carnitine", "acylcarnitine")

    # === AMINO ACID METABOLISM ===
    log.info("--- Amino Acid Metabolism ---")

    aa_rxns = [
        ("Glutamate Dehydrogenase", "GDH", "Glutamate + NAD(P)+ ⇌ α-KG + NH4+ + NAD(P)H", "glutamate", "alpha-KG,NH4", 1.0, 50),
        ("Glutamine Synthetase", "GS", "Glutamate + NH4+ + ATP → Glutamine + ADP + Pi", "glutamate,NH4,ATP", "glutamine", 0.3, 30),
        ("Glutaminase", "GLS", "Glutamine + H2O → Glutamate + NH4+", "glutamine", "glutamate,NH4", 0.5, 40),
        ("Aspartate Aminotransferase", "AST", "Aspartate + α-KG ⇌ OAA + Glutamate", "aspartate,alpha-KG", "OAA,glutamate", 2.0, 200),
        ("Alanine Aminotransferase", "ALT", "Alanine + α-KG ⇌ Pyruvate + Glutamate", "alanine,alpha-KG", "pyruvate,glutamate", 1.5, 150),
        ("Branched-chain Aminotransferase", "BCAT", "BCAA + α-KG ⇌ BCKA + Glutamate", "BCAA,alpha-KG", "BCKA,glutamate", 0.5, 60),
        ("Phenylalanine Hydroxylase", "PAH", "Phe + O2 + BH4 → Tyr + H2O + BH2", "phenylalanine,O2,BH4", "tyrosine", 0.1, 20),
        ("Tyrosine Aminotransferase", "TAT", "Tyrosine + α-KG → 4-HPP + Glutamate", "tyrosine,alpha-KG", "4-HPP,glutamate", 0.3, 30),
    ]

    for name, abbr, rxn, sub, prod, km, vmax in aa_rxns:
        fid = add_formula(conn, f"{name} ({abbr})",
            rf"v_{{{abbr}}} = \frac{{V_{{max}} [S]}}{{K_m + [S]}}",
            f"Amino acid metabolism: {rxn}",
            "rate_equation", aasyn, src,
            domain="amino-acid-metabolism", model_origin=abbr)
        add_enzyme(conn, fid, name, "michaelis-menten", sub, prod, km, vmax)

    # Urea cycle
    log.info("--- Urea Cycle ---")

    urea_rxns = [
        ("Carbamoyl Phosphate Synthetase I", "CPS1", "NH4+ + CO2 + 2ATP → Carbamoyl-P + 2ADP + Pi", "NH4,CO2,ATP", "carbamoyl-P", 0.5, 20),
        ("Ornithine Transcarbamylase", "OTC", "Ornithine + Carbamoyl-P → Citrulline + Pi", "ornithine,carbamoyl-P", "citrulline", 0.1, 100),
        ("Argininosuccinate Synthetase", "ASS", "Citrulline + Aspartate + ATP → Argininosuccinate + AMP + PPi", "citrulline,aspartate,ATP", "argininosuccinate", 0.05, 30),
        ("Argininosuccinate Lyase", "ASL", "Argininosuccinate → Arginine + Fumarate", "argininosuccinate", "arginine,fumarate", 0.02, 80),
        ("Arginase", "ARG", "Arginine + H2O → Ornithine + Urea", "arginine", "ornithine,urea", 1.0, 200),
    ]

    for name, abbr, rxn, sub, prod, km, vmax in urea_rxns:
        fid = add_formula(conn, f"{name} ({abbr})",
            rf"v_{{{abbr}}} = \frac{{V_{{max}} [S]}}{{K_m + [S]}}",
            f"Urea cycle: {rxn}",
            "rate_equation", aasyn, src,
            domain="urea-cycle", model_origin=abbr)
        add_enzyme(conn, fid, name, "michaelis-menten", sub, prod, km, vmax)

    print_summary(conn, "METABOLIC PATHWAYS", start)
    conn.close()

if __name__ == "__main__":
    run()
