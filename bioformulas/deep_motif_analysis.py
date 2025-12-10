#!/usr/bin/env python3
"""
Deep analysis of network motifs by examining reaction networks,
metabolic pathways, and mathematical structures.
"""

import sqlite3
import json
import re
from collections import defaultdict, Counter

DB_PATH = '/home/user/MAINFRAME/bioformulas/bioformulas.db'

def connect_db():
    return sqlite3.connect(DB_PATH)

def analyze_reactions_network(conn):
    """Analyze reaction networks for network motifs."""
    cursor = conn.cursor()

    # Get all reactions
    query = """
    SELECT r.reaction_id, r.formula_id, r.reaction_name, r.reactants, r.products,
           r.stoichiometry, r.rate_law, r.reversible, r.compartment,
           f.name, f.latex, f.domain
    FROM reactions r
    JOIN formulas f ON r.formula_id = f.formula_id
    """

    cursor.execute(query)
    results = cursor.fetchall()

    reactions = []
    # Build reaction network graph
    metabolite_to_reactions = defaultdict(list)  # metabolite -> reactions producing it
    reaction_to_metabolites = {}  # reaction -> (reactants, products)

    for row in results:
        rid, fid, rname, reactants, products, stoich, rlaw, reversible, comp, fname, latex, domain = row

        # Parse reactants and products
        try:
            reactants_list = json.loads(reactants) if reactants else []
            products_list = json.loads(products) if products else []
        except:
            reactants_list = []
            products_list = []

        reactions.append({
            'reaction_id': rid,
            'formula_id': fid,
            'reaction_name': rname,
            'reactants': reactants_list,
            'products': products_list,
            'rate_law': rlaw,
            'reversible': reversible,
            'compartment': comp,
            'formula_name': fname,
            'latex': latex,
            'domain': domain
        })

        # Build network
        reaction_to_metabolites[rid] = (reactants_list, products_list)
        for product in products_list:
            metabolite_to_reactions[product].append(rid)

    # Find feed-forward loops: A -> B -> C and A -> C
    feedforward_loops = []
    for metabolite_A in metabolite_to_reactions:
        reactions_producing_A = metabolite_to_reactions[metabolite_A]
        for rxn in reactions_producing_A:
            reactants, products = reaction_to_metabolites.get(rxn, ([], []))
            # Check if any product (B) also produces another metabolite (C)
            # And check if metabolite_A also directly produces C
            for metabolite_B in products:
                if metabolite_B != metabolite_A and metabolite_B in metabolite_to_reactions:
                    reactions_producing_C_from_B = metabolite_to_reactions[metabolite_B]
                    # Check for direct path A -> C
                    for rxn2 in reactions_producing_C_from_B:
                        _, products_C = reaction_to_metabolites.get(rxn2, ([], []))
                        for metabolite_C in products_C:
                            # Check if there's also a direct A -> C path
                            if metabolite_C in metabolite_to_reactions:
                                direct_rxns = [r for r in metabolite_to_reactions[metabolite_C]
                                             if r != rxn and r != rxn2]
                                if direct_rxns:
                                    feedforward_loops.append({
                                        'A': metabolite_A,
                                        'B': metabolite_B,
                                        'C': metabolite_C,
                                        'A_to_B': rxn,
                                        'B_to_C': rxn2,
                                        'A_to_C': direct_rxns[0]
                                    })

    # Find fan-out: one metabolite used by many reactions
    fanout = []
    for metabolite, rxns in metabolite_to_reactions.items():
        if len(rxns) > 2:  # Metabolite is used by multiple reactions
            fanout.append({
                'metabolite': metabolite,
                'num_targets': len(rxns),
                'reactions': rxns[:10]  # Limit for JSON size
            })

    # Find fan-in: one reaction uses many metabolites
    fanin = []
    for rid, (reactants, products) in reaction_to_metabolites.items():
        if len(reactants) > 2:
            fanin.append({
                'reaction_id': rid,
                'num_inputs': len(reactants),
                'reactants': reactants
            })

    return {
        'reactions': reactions[:100],  # Limit for JSON size
        'feedforward_loops': feedforward_loops[:50],
        'fanout_patterns': sorted(fanout, key=lambda x: x['num_targets'], reverse=True)[:50],
        'fanin_patterns': sorted(fanin, key=lambda x: x['num_inputs'], reverse=True)[:50],
        'total_reactions': len(reactions),
        'total_metabolites': len(metabolite_to_reactions)
    }

def analyze_metabolic_domains(conn):
    """Analyze specific metabolic pathways for known motifs."""
    cursor = conn.cursor()

    # Glycolysis often has feedback and feedforward loops
    domains_of_interest = [
        'glycolysis', 'TCA-cycle', 'OXPHOS', 'PPP',
        'MAPK', 'PI3K-AKT', 'JAK-STAT', 'Wnt', 'Notch',
        'cAMP', 'calcium-signaling'
    ]

    domain_analysis = {}

    for domain in domains_of_interest:
        query = """
        SELECT f.formula_id, f.name, f.description, f.latex, f.formula_type,
               p.symbol, p.value
        FROM formulas f
        LEFT JOIN parameters p ON f.formula_id = p.formula_id
        WHERE f.domain = ?
        """

        cursor.execute(query, (domain,))
        results = cursor.fetchall()

        formulas = {}
        for row in results:
            fid, name, desc, latex, ftype, psym, pval = row

            if fid not in formulas:
                formulas[fid] = {
                    'formula_id': fid,
                    'name': name,
                    'description': desc,
                    'latex': latex,
                    'formula_type': ftype,
                    'parameters': []
                }

            if psym:
                formulas[fid]['parameters'].append({'symbol': psym, 'value': pval})

        if formulas:
            domain_analysis[domain] = {
                'count': len(formulas),
                'formulas': list(formulas.values())[:20]  # Limit for JSON
            }

    return domain_analysis

def find_coupled_odes(conn):
    """Find systems of coupled ODEs that form networks."""
    cursor = conn.cursor()

    # Get formulas that are part of the same biological system
    query = """
    SELECT f.formula_id, f.name, f.description, f.latex, f.domain, f.model_origin
    FROM formulas f
    WHERE f.formula_type = 'ODE'
    AND f.model_origin IS NOT NULL
    ORDER BY f.model_origin, f.formula_id
    LIMIT 1000
    """

    cursor.execute(query)
    results = cursor.fetchall()

    # Group by model origin
    models = defaultdict(list)
    for row in results:
        fid, name, desc, latex, domain, origin = row
        models[origin].append({
            'formula_id': fid,
            'name': name,
            'description': desc,
            'latex': latex,
            'domain': domain
        })

    # Find models with multiple coupled equations (potential networks)
    coupled_systems = {}
    for origin, formulas in models.items():
        if len(formulas) >= 2:  # At least 2 equations coupled
            coupled_systems[origin] = {
                'num_equations': len(formulas),
                'domain': formulas[0]['domain'],
                'formulas': formulas
            }

    return coupled_systems

def analyze_allosteric_regulation(conn):
    """Find allosteric regulation patterns (common regulatory motif)."""
    cursor = conn.cursor()

    # Allosteric regulation often involves cooperative binding
    query = """
    SELECT f.formula_id, f.name, f.description, f.latex, f.domain
    FROM formulas f
    WHERE (
        f.description LIKE '%allosteric%' OR
        f.description LIKE '%activation%inhibition%' OR
        f.description LIKE '%activator%' OR
        f.description LIKE '%inhibitor%' OR
        f.name LIKE '%allosteric%'
    )
    AND f.latex IS NOT NULL
    LIMIT 200
    """

    cursor.execute(query)
    results = cursor.fetchall()

    allosteric = []
    for row in results:
        fid, name, desc, latex, domain = row

        # Classify regulation type
        reg_type = []
        if desc:
            desc_lower = desc.lower()
            if 'activat' in desc_lower:
                reg_type.append('activation')
            if 'inhibit' in desc_lower:
                reg_type.append('inhibition')
            if 'allosteric' in desc_lower:
                reg_type.append('allosteric')

        allosteric.append({
            'formula_id': fid,
            'name': name,
            'description': desc,
            'latex': latex,
            'domain': domain,
            'regulation_types': reg_type
        })

    return allosteric

def find_ultrasensitive_responses(conn):
    """Find ultrasensitive and switch-like responses."""
    cursor = conn.cursor()

    # Ultrasensitivity keywords and mathematical signatures
    query = """
    SELECT f.formula_id, f.name, f.description, f.latex, f.domain, f.formula_type
    FROM formulas f
    WHERE (
        f.description LIKE '%ultrasensitive%' OR
        f.description LIKE '%switch%' OR
        f.description LIKE '%sigmoidal%' OR
        f.description LIKE '%steep%' OR
        f.description LIKE '%threshold%' OR
        f.latex LIKE '%^3%' OR
        f.latex LIKE '%^4%' OR
        f.latex LIKE '%^5%'
    )
    LIMIT 300
    """

    cursor.execute(query)
    results = cursor.fetchall()

    ultrasensitive = []
    for row in results:
        fid, name, desc, latex, domain, ftype = row

        # Extract power/Hill coefficient from LaTeX
        powers = re.findall(r'\^(\d+)', latex) if latex else []
        max_power = max([int(p) for p in powers]) if powers else 0

        ultrasensitive.append({
            'formula_id': fid,
            'name': name,
            'description': desc,
            'latex': latex,
            'domain': domain,
            'formula_type': ftype,
            'max_power': max_power
        })

    return ultrasensitive

def main():
    """Main analysis."""
    conn = connect_db()

    print("=" * 80)
    print("DEEP NETWORK MOTIF ANALYSIS")
    print("=" * 80)

    all_results = {}

    # 1. Reaction network analysis
    print("\n\n1. REACTION NETWORK MOTIFS")
    print("-" * 80)
    reaction_motifs = analyze_reactions_network(conn)
    all_results['reaction_networks'] = reaction_motifs

    print(f"Total reactions: {reaction_motifs['total_reactions']}")
    print(f"Total metabolites: {reaction_motifs['total_metabolites']}")
    print(f"Feed-forward loops found: {len(reaction_motifs['feedforward_loops'])}")
    print(f"Fan-out patterns: {len(reaction_motifs['fanout_patterns'])}")
    print(f"Fan-in patterns: {len(reaction_motifs['fanin_patterns'])}")

    if reaction_motifs['feedforward_loops']:
        print("\nTop feed-forward loops:")
        for i, ffl in enumerate(reaction_motifs['feedforward_loops'][:5], 1):
            print(f"  {i}. {ffl['A']} → {ffl['B']} → {ffl['C']} (with direct {ffl['A']} → {ffl['C']})")

    if reaction_motifs['fanout_patterns']:
        print("\nTop fan-out patterns:")
        for i, fo in enumerate(reaction_motifs['fanout_patterns'][:5], 1):
            print(f"  {i}. {fo['metabolite']} → {fo['num_targets']} reactions")

    # 2. Metabolic pathway analysis
    print("\n\n2. METABOLIC PATHWAY ANALYSIS")
    print("-" * 80)
    domain_analysis = analyze_metabolic_domains(conn)
    all_results['pathway_analysis'] = domain_analysis

    for domain, data in domain_analysis.items():
        print(f"\n{domain}: {data['count']} formulas")
        if data['formulas']:
            for f in data['formulas'][:3]:
                print(f"  - {f['name']}")

    # 3. Coupled ODE systems
    print("\n\n3. COUPLED ODE SYSTEMS (Network Dynamics)")
    print("-" * 80)
    coupled = find_coupled_odes(conn)
    all_results['coupled_systems'] = {k: v for k, v in list(coupled.items())[:20]}

    print(f"Found {len(coupled)} coupled systems")
    for i, (origin, system) in enumerate(list(coupled.items())[:10], 1):
        print(f"\n{i}. {origin} ({system['num_equations']} equations, {system['domain']})")
        for eq in system['formulas'][:3]:
            print(f"   - {eq['name']}")

    # 4. Allosteric regulation
    print("\n\n4. ALLOSTERIC REGULATION")
    print("-" * 80)
    allosteric = analyze_allosteric_regulation(conn)
    all_results['allosteric_regulation'] = allosteric[:100]

    print(f"Found {len(allosteric)} allosteric regulation formulas")
    for i, a in enumerate(allosteric[:10], 1):
        print(f"\n{i}. {a['name']}")
        print(f"   Domain: {a['domain']}")
        print(f"   Regulation: {', '.join(a['regulation_types'])}")
        print(f"   LaTeX: {a['latex'][:80]}...")

    # 5. Ultrasensitive responses
    print("\n\n5. ULTRASENSITIVE/SWITCH-LIKE RESPONSES")
    print("-" * 80)
    ultrasensitive = find_ultrasensitive_responses(conn)
    all_results['ultrasensitive_responses'] = ultrasensitive[:100]

    print(f"Found {len(ultrasensitive)} ultrasensitive response formulas")
    print("\nHighest cooperativity:")
    sorted_ultra = sorted(ultrasensitive, key=lambda x: x['max_power'], reverse=True)
    for i, u in enumerate(sorted_ultra[:10], 1):
        print(f"\n{i}. {u['name']} (power: {u['max_power']})")
        print(f"   Domain: {u['domain']}")
        print(f"   LaTeX: {u['latex'][:80]}...")

    conn.close()

    # Export
    output_file = '/home/user/MAINFRAME/bioformulas/deep_network_motifs.json'
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    print(f"\n\nResults exported to: {output_file}")

if __name__ == "__main__":
    main()
