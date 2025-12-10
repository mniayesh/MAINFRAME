#!/usr/bin/env python3
"""
Extract specific formula examples for each network motif type.
Creates a clean reference with exact mathematical formulas.
"""

import sqlite3
import json

DB_PATH = '/home/user/MAINFRAME/bioformulas/bioformulas.db'

def get_formulas_by_category(conn):
    """Extract key formulas for each motif category."""
    cursor = conn.cursor()

    formulas = {}

    # 1. Positive Feedback Examples
    query = """
    SELECT f.formula_id, f.name, f.latex, f.description, f.domain
    FROM formulas f
    WHERE (f.name LIKE '%Izhikevich%' OR
           f.name LIKE '%FitzHugh%' OR
           f.name LIKE '%Hill%')
    AND f.latex IS NOT NULL
    LIMIT 10
    """
    cursor.execute(query)
    formulas['positive_feedback'] = [
        {'id': r[0], 'name': r[1], 'latex': r[2], 'description': r[3], 'domain': r[4]}
        for r in cursor.fetchall()
    ]

    # 2. Bistable Switches
    query = """
    SELECT f.formula_id, f.name, f.latex, f.description, f.domain
    FROM formulas f
    WHERE (f.name LIKE '%Toggle%' OR
           f.name LIKE '%bistable%')
    AND f.latex IS NOT NULL
    """
    cursor.execute(query)
    formulas['bistable_switches'] = [
        {'id': r[0], 'name': r[1], 'latex': r[2], 'description': r[3], 'domain': r[4]}
        for r in cursor.fetchall()
    ]

    # 3. STDP and Plasticity
    query = """
    SELECT f.formula_id, f.name, f.latex, f.description, f.domain
    FROM formulas f
    JOIN plasticity_rules pr ON f.formula_id = pr.formula_id
    """
    cursor.execute(query)
    formulas['plasticity_rules'] = [
        {'id': r[0], 'name': r[1], 'latex': r[2], 'description': r[3], 'domain': r[4]}
        for r in cursor.fetchall()
    ]

    # 4. MAPK Cascade
    query = """
    SELECT f.formula_id, f.name, f.latex, f.description, f.domain
    FROM formulas f
    WHERE f.domain = 'MAPK'
    """
    cursor.execute(query)
    formulas['mapk_cascade'] = [
        {'id': r[0], 'name': r[1], 'latex': r[2], 'description': r[3], 'domain': r[4]}
        for r in cursor.fetchall()
    ]

    # 5. Glycolysis (metabolic network motifs)
    query = """
    SELECT f.formula_id, f.name, f.latex, f.description, f.domain
    FROM formulas f
    WHERE f.domain = 'glycolysis'
    """
    cursor.execute(query)
    formulas['glycolysis'] = [
        {'id': r[0], 'name': r[1], 'latex': r[2], 'description': r[3], 'domain': r[4]}
        for r in cursor.fetchall()
    ]

    # 6. Ion channels (ultrasensitivity)
    query = """
    SELECT f.formula_id, f.name, f.latex, f.description, f.domain
    FROM formulas f
    WHERE f.domain = 'ion-channels' AND f.latex LIKE '%^4%'
    LIMIT 15
    """
    cursor.execute(query)
    formulas['ion_channels'] = [
        {'id': r[0], 'name': r[1], 'latex': r[2], 'description': r[3], 'domain': r[4]}
        for r in cursor.fetchall()
    ]

    # 7. Enzyme kinetics with cooperativity
    query = """
    SELECT f.formula_id, f.name, f.latex, f.description, f.domain,
           ek.hill_coefficient, ek.enzyme_name
    FROM formulas f
    JOIN enzyme_kinetics ek ON f.formula_id = ek.formula_id
    WHERE ek.hill_coefficient IS NOT NULL
    """
    cursor.execute(query)
    formulas['enzyme_cooperativity'] = [
        {'id': r[0], 'name': r[1], 'latex': r[2], 'description': r[3],
         'domain': r[4], 'hill_n': r[5], 'enzyme': r[6]}
        for r in cursor.fetchall()
    ]

    # 8. Inhibition patterns
    query = """
    SELECT f.formula_id, f.name, f.latex, f.description, f.domain
    FROM formulas f
    WHERE (f.name LIKE '%Inhibition%' OR f.name LIKE '%inhibit%')
    AND f.latex IS NOT NULL
    LIMIT 10
    """
    cursor.execute(query)
    formulas['inhibition_patterns'] = [
        {'id': r[0], 'name': r[1], 'latex': r[2], 'description': r[3], 'domain': r[4]}
        for r in cursor.fetchall()
    ]

    # 9. Neuron models (excitability)
    query = """
    SELECT f.formula_id, f.name, f.latex, f.description, f.domain
    FROM formulas f
    WHERE f.name LIKE '%Hodgkin%' OR
          f.name LIKE '%Izhikevich%' OR
          f.name LIKE '%FitzHugh%' OR
          f.name LIKE '%LIF%' OR
          f.name LIKE '%AdEx%'
    LIMIT 20
    """
    cursor.execute(query)
    formulas['neuron_models'] = [
        {'id': r[0], 'name': r[1], 'latex': r[2], 'description': r[3], 'domain': r[4]}
        for r in cursor.fetchall()
    ]

    # 10. Signaling pathways
    query = """
    SELECT DISTINCT f.domain, COUNT(*) as cnt
    FROM formulas f
    WHERE f.domain IN ('PI3K-AKT', 'JAK-STAT', 'Wnt', 'Notch', 'cAMP', 'NF-kB')
    GROUP BY f.domain
    """
    cursor.execute(query)
    pathway_counts = {r[0]: r[1] for r in cursor.fetchall()}

    formulas['pathway_summary'] = pathway_counts

    return formulas

def print_formulas(formulas):
    """Print formulas in a readable format."""

    print("=" * 80)
    print("NETWORK MOTIF FORMULA CATALOG")
    print("=" * 80)
    print("\nExact mathematical formulas extracted from bioformulas database")
    print("Total database size: 90,313 formulas\n")

    # 1. Positive Feedback
    print("\n" + "=" * 80)
    print("1. POSITIVE FEEDBACK CIRCUITS")
    print("=" * 80)
    print("\nThese formulas contain nonlinear (squared or higher) terms that")
    print("create self-amplifying dynamics.\n")

    for i, f in enumerate(formulas['positive_feedback'][:5], 1):
        print(f"\n{i}. {f['name']}")
        print(f"   {f['latex']}")
        print(f"   Description: {f['description']}")
        print(f"   Domain: {f['domain']}")

    # 2. Bistable Switches
    print("\n\n" + "=" * 80)
    print("2. BISTABLE SWITCHES (Toggle Circuits)")
    print("=" * 80)
    print("\nMutually inhibitory circuits that create two stable states.\n")

    for i, f in enumerate(formulas['bistable_switches'], 1):
        print(f"\n{i}. {f['name']}")
        print(f"   {f['latex']}")
        print(f"   Description: {f['description']}")

    # 3. Plasticity Rules
    print("\n\n" + "=" * 80)
    print("3. SYNAPTIC PLASTICITY RULES (Learning Motifs)")
    print("=" * 80)
    print("\nBiological learning rules for weight updates.\n")

    for i, f in enumerate(formulas['plasticity_rules'], 1):
        print(f"\n{i}. {f['name']}")
        print(f"   {f['latex']}")
        print(f"   Description: {f['description']}")

    # 4. MAPK Cascade
    print("\n\n" + "=" * 80)
    print("4. MAPK SIGNALING CASCADE (Feed-Forward)")
    print("=" * 80)
    print("\n3-tier kinase cascade: Raf (MAPKKK) → MEK (MAPKK) → ERK (MAPK)\n")

    for i, f in enumerate(formulas['mapk_cascade'], 1):
        print(f"\n{i}. {f['name']}")
        print(f"   {f['latex']}")
        print(f"   Description: {f['description']}")

    # 5. Enzyme Cooperativity
    print("\n\n" + "=" * 80)
    print("5. COOPERATIVE ENZYMES (Hill Functions)")
    print("=" * 80)
    print("\nEnzymes with Hill coefficient > 1 show cooperative binding.\n")

    for i, f in enumerate(formulas['enzyme_cooperativity'], 1):
        print(f"\n{i}. {f['name']} (n = {f['hill_n']})")
        print(f"   {f['latex']}")
        print(f"   Enzyme: {f['enzyme']}")
        print(f"   Description: {f['description']}")

    # 6. Ion Channels
    print("\n\n" + "=" * 80)
    print("6. ION CHANNELS (Ultrasensitive n^4 Gates)")
    print("=" * 80)
    print("\nPotassium channels use n^4 gating for ultra-sharp switching.\n")

    for i, f in enumerate(formulas['ion_channels'][:10], 1):
        print(f"\n{i}. {f['name']}")
        print(f"   {f['latex']}")

    # 7. Inhibition
    print("\n\n" + "=" * 80)
    print("7. INHIBITION PATTERNS")
    print("=" * 80)
    print("\nCompetitive, non-competitive, and uncompetitive inhibition.\n")

    for i, f in enumerate(formulas['inhibition_patterns'][:5], 1):
        print(f"\n{i}. {f['name']}")
        print(f"   {f['latex']}")
        print(f"   Description: {f['description']}")

    # 8. Glycolysis
    print("\n\n" + "=" * 80)
    print("8. GLYCOLYSIS PATHWAY (Metabolic Network Motifs)")
    print("=" * 80)
    print("\nKey regulatory enzymes with allosteric control.\n")

    for i, f in enumerate(formulas['glycolysis'], 1):
        print(f"\n{i}. {f['name']}")
        print(f"   {f['latex']}")
        print(f"   Description: {f['description']}")

    # 9. Neuron Models
    print("\n\n" + "=" * 80)
    print("9. COMPLETE NEURON MODELS")
    print("=" * 80)
    print("\nIntegrated models combining multiple motifs.\n")

    for i, f in enumerate(formulas['neuron_models'][:8], 1):
        print(f"\n{i}. {f['name']}")
        print(f"   {f['latex']}")

    # 10. Pathway Summary
    print("\n\n" + "=" * 80)
    print("10. SIGNALING PATHWAY SUMMARY")
    print("=" * 80)
    print("\nMajor cell signaling pathways in database:\n")

    for pathway, count in formulas['pathway_summary'].items():
        print(f"  {pathway}: {count} formulas")

def main():
    conn = sqlite3.connect(DB_PATH)
    formulas = get_formulas_by_category(conn)

    # Print to console
    print_formulas(formulas)

    # Save to JSON
    output_json = '/home/user/MAINFRAME/bioformulas/formula_catalog.json'
    with open(output_json, 'w') as f:
        json.dump(formulas, f, indent=2)

    print(f"\n\nFormula catalog saved to: {output_json}")

    conn.close()

if __name__ == "__main__":
    main()
