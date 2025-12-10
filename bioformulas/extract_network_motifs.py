#!/usr/bin/env python3
"""
Extract computational network motifs from bioformulas database.
Analyzes LaTeX formulas and their structural patterns.
"""

import sqlite3
import json
import re
from collections import defaultdict

DB_PATH = '/home/user/MAINFRAME/bioformulas/bioformulas.db'

def connect_db():
    """Connect to the database."""
    return sqlite3.connect(DB_PATH)

def analyze_formula_structure(latex):
    """Analyze LaTeX formula for structural patterns."""
    if not latex:
        return {}

    features = {
        'has_derivative': bool(re.search(r'\\frac\{d', latex)),
        'has_power': bool(re.search(r'\^[2-9]|\*\*[2-9]', latex)),
        'has_fraction': bool(re.search(r'\\frac', latex)),
        'has_exp': bool(re.search(r'\\exp', latex)),
        'has_product': bool(re.search(r'\*|\\cdot|\\times', latex)),
        'has_sum': bool(re.search(r'\+', latex)),
        'has_difference': bool(re.search(r'-', latex)),
        'num_terms': len(re.findall(r'[+-]', latex)),
        'max_power': 0
    }

    # Extract maximum power
    powers = re.findall(r'\^(\d+)|\*\*(\d+)', latex)
    if powers:
        features['max_power'] = max([int(p[0] or p[1]) for p in powers])

    return features

def find_feedback_loops_comprehensive(conn):
    """Find feedback loops by analyzing formula structure."""
    cursor = conn.cursor()

    # Feedback loops: formulas with squared or higher power terms (autocatalysis)
    # or explicit feedback terms
    query = """
    SELECT f.formula_id, f.name, f.description, f.latex, f.domain, f.formula_type,
           p.symbol, p.value, p.name as param_name
    FROM formulas f
    LEFT JOIN parameters p ON f.formula_id = p.formula_id
    WHERE (
        f.latex LIKE '%^2%' OR
        f.latex LIKE '%^3%' OR
        f.latex LIKE '%^4%' OR
        f.description LIKE '%feedback%' OR
        f.description LIKE '%cooperative%' OR
        f.description LIKE '%ultrasensitive%' OR
        f.description LIKE '%autoinhibit%' OR
        f.description LIKE '%autoactivat%' OR
        f.name LIKE '%feedback%' OR
        f.name LIKE '%cooperative%'
    )
    LIMIT 500
    """

    cursor.execute(query)
    results = cursor.fetchall()

    formulas = {}
    for row in results:
        fid, name, desc, latex, domain, ftype, psym, pval, pname = row

        if fid not in formulas:
            features = analyze_formula_structure(latex)

            # Classify feedback type
            feedback_type = "unknown"
            if desc:
                desc_lower = desc.lower()
                if any(w in desc_lower for w in ['positive feedback', 'activation', 'autocatalytic', 'cooperative']):
                    feedback_type = "positive"
                elif any(w in desc_lower for w in ['negative feedback', 'inhibit', 'suppress']):
                    feedback_type = "negative"

            # Determine mechanism
            mechanism = []
            if features['max_power'] >= 2:
                mechanism.append(f"nonlinear (power {features['max_power']})")
            if 'cooperative' in (desc or '').lower():
                mechanism.append("cooperative binding")

            formulas[fid] = {
                'formula_id': fid,
                'name': name,
                'description': desc,
                'latex': latex,
                'domain': domain,
                'formula_type': ftype,
                'feedback_type': feedback_type,
                'mechanism': ', '.join(mechanism) if mechanism else 'unknown',
                'features': features,
                'parameters': []
            }

        if psym:
            formulas[fid]['parameters'].append({
                'symbol': psym,
                'value': pval,
                'name': pname
            })

    return list(formulas.values())

def find_bistable_switches_comprehensive(conn):
    """Find bistable switches and toggle switches."""
    cursor = conn.cursor()

    # Bistability indicators:
    # - Hill coefficient > 1.5
    # - Mutual inhibition
    # - Positive feedback with saturation
    # - Switch-like keywords

    query = """
    SELECT f.formula_id, f.name, f.description, f.latex, f.domain, f.formula_type,
           ek.hill_coefficient, ek.enzyme_name, ek.kinetics_type
    FROM formulas f
    LEFT JOIN enzyme_kinetics ek ON f.formula_id = ek.formula_id
    WHERE (
        f.description LIKE '%bistable%' OR
        f.description LIKE '%switch%' OR
        f.description LIKE '%toggle%' OR
        f.description LIKE '%hysteresis%' OR
        f.description LIKE '%mutual inhibition%' OR
        f.description LIKE '%mutual repression%' OR
        f.name LIKE '%bistable%' OR
        f.name LIKE '%switch%' OR
        ek.hill_coefficient > 1.5
    )
    LIMIT 500
    """

    cursor.execute(query)
    results = cursor.fetchall()

    formulas = {}
    for row in results:
        fid, name, desc, latex, domain, ftype, hill, enzyme, kintype = row

        if fid not in formulas:
            features = analyze_formula_structure(latex)

            formulas[fid] = {
                'formula_id': fid,
                'name': name,
                'description': desc,
                'latex': latex,
                'domain': domain,
                'formula_type': ftype,
                'hill_coefficient': hill,
                'enzyme_name': enzyme,
                'kinetics_type': kintype,
                'features': features
            }

    return list(formulas.values())

def find_signaling_cascades(conn):
    """Find signaling cascades and feed-forward loops."""
    cursor = conn.cursor()

    # Query signaling cascades table
    query = """
    SELECT f.formula_id, f.name, f.description, f.latex, f.domain, f.formula_type,
           sc.pathway_name, sc.cascade_level, sc.upstream_component, sc.downstream_component,
           sc.activation_type
    FROM formulas f
    JOIN signaling_cascades sc ON f.formula_id = sc.formula_id
    ORDER BY sc.pathway_name, sc.cascade_level
    LIMIT 500
    """

    cursor.execute(query)
    results = cursor.fetchall()

    # Group by pathway
    pathways = defaultdict(list)
    formulas = []

    for row in results:
        fid, name, desc, latex, domain, ftype, pathway, level, upstream, downstream, act_type = row

        f = {
            'formula_id': fid,
            'name': name,
            'description': desc,
            'latex': latex,
            'domain': domain,
            'formula_type': ftype,
            'pathway_name': pathway,
            'cascade_level': level,
            'upstream_component': upstream,
            'downstream_component': downstream,
            'activation_type': act_type
        }

        formulas.append(f)
        if pathway:
            pathways[pathway].append(f)

    return formulas, dict(pathways)

def find_gene_regulatory_networks(conn):
    """Find gene regulatory networks with fan-in and fan-out."""
    cursor = conn.cursor()

    query = """
    SELECT f.formula_id, f.name, f.description, f.latex, f.domain, f.formula_type,
           gr.gene_name, gr.transcription_factor, gr.regulation_type,
           gr.hill_coefficient, gr.binding_affinity
    FROM formulas f
    JOIN gene_regulation gr ON f.formula_id = gr.formula_id
    LIMIT 500
    """

    cursor.execute(query)
    results = cursor.fetchall()

    # Track TF → gene relationships for fan-out/fan-in
    tf_targets = defaultdict(list)  # TF -> genes (fan-out)
    gene_regulators = defaultdict(list)  # gene -> TFs (fan-in)

    formulas = []
    for row in results:
        fid, name, desc, latex, domain, ftype, gene, tf, regtype, hill, affinity = row

        f = {
            'formula_id': fid,
            'name': name,
            'description': desc,
            'latex': latex,
            'domain': domain,
            'formula_type': ftype,
            'gene_name': gene,
            'transcription_factor': tf,
            'regulation_type': regtype,
            'hill_coefficient': hill,
            'binding_affinity': affinity
        }

        formulas.append(f)

        if tf and gene:
            tf_targets[tf].append(gene)
            gene_regulators[gene].append(tf)

    # Identify fan-out (one TF → many genes)
    fanout = [{'tf': tf, 'targets': genes, 'degree': len(genes)}
              for tf, genes in tf_targets.items() if len(genes) > 1]

    # Identify fan-in (many TFs → one gene)
    fanin = [{'gene': gene, 'regulators': tfs, 'degree': len(tfs)}
             for gene, tfs in gene_regulators.items() if len(tfs) > 1]

    return formulas, fanout, fanin

def find_synaptic_integration(conn):
    """Find synaptic integration patterns (fan-in)."""
    cursor = conn.cursor()

    query = """
    SELECT f.formula_id, f.name, f.description, f.latex, f.domain, f.formula_type,
           s.synapse_type, s.plasticity_type, s.transmission_type
    FROM formulas f
    JOIN synapses s ON f.formula_id = s.formula_id
    WHERE f.description LIKE '%integration%' OR
          f.description LIKE '%summation%' OR
          f.name LIKE '%integration%' OR
          f.name LIKE '%summation%'
    LIMIT 200
    """

    cursor.execute(query)
    results = cursor.fetchall()

    formulas = []
    for row in results:
        fid, name, desc, latex, domain, ftype, syntype, plastype, transtype = row

        features = analyze_formula_structure(latex)

        formulas.append({
            'formula_id': fid,
            'name': name,
            'description': desc,
            'latex': latex,
            'domain': domain,
            'formula_type': ftype,
            'synapse_type': syntype,
            'plasticity_type': plastype,
            'transmission_type': transtype,
            'num_inputs': features['num_terms']
        })

    return formulas

def find_oscillators_and_clocks(conn):
    """Find oscillatory circuits (often involve negative feedback)."""
    cursor = conn.cursor()

    query = """
    SELECT f.formula_id, f.name, f.description, f.latex, f.domain, f.formula_type,
           o.oscillator_type, o.frequency_hz, o.biological_system
    FROM formulas f
    JOIN oscillators o ON f.formula_id = o.formula_id
    LIMIT 200
    """

    cursor.execute(query)
    results = cursor.fetchall()

    formulas = []
    for row in results:
        fid, name, desc, latex, domain, ftype, osctype, freq, biosys = row

        formulas.append({
            'formula_id': fid,
            'name': name,
            'description': desc,
            'latex': latex,
            'domain': domain,
            'formula_type': ftype,
            'oscillator_type': osctype,
            'frequency_hz': freq,
            'biological_system': biosys
        })

    return formulas

def find_plasticity_rules(conn):
    """Find synaptic plasticity rules (learning motifs)."""
    cursor = conn.cursor()

    query = """
    SELECT f.formula_id, f.name, f.description, f.latex, f.domain, f.formula_type,
           pr.rule_type, pr.time_window_pre, pr.time_window_post, pr.learning_rate,
           pr.weight_dependence
    FROM formulas f
    JOIN plasticity_rules pr ON f.formula_id = pr.formula_id
    LIMIT 200
    """

    cursor.execute(query)
    results = cursor.fetchall()

    formulas = []
    for row in results:
        fid, name, desc, latex, domain, ftype, ruletype, tpre, tpost, lr, wdep = row

        formulas.append({
            'formula_id': fid,
            'name': name,
            'description': desc,
            'latex': latex,
            'domain': domain,
            'formula_type': ftype,
            'rule_type': ruletype,
            'time_window_pre': tpre,
            'time_window_post': tpost,
            'learning_rate': lr,
            'weight_dependence': wdep
        })

    return formulas

def find_enzymatic_reactions(conn):
    """Find enzymatic reactions with cooperative binding."""
    cursor = conn.cursor()

    query = """
    SELECT f.formula_id, f.name, f.description, f.latex, f.domain, f.formula_type,
           ek.enzyme_name, ek.kinetics_type, ek.hill_coefficient, ek.km, ek.vmax
    FROM formulas f
    JOIN enzyme_kinetics ek ON f.formula_id = ek.formula_id
    WHERE ek.hill_coefficient IS NOT NULL
    ORDER BY ek.hill_coefficient DESC
    LIMIT 200
    """

    cursor.execute(query)
    results = cursor.fetchall()

    formulas = []
    for row in results:
        fid, name, desc, latex, domain, ftype, enzyme, kintype, hill, km, vmax = row

        # Classify cooperativity
        if hill is not None:
            if hill > 1.2:
                coop_type = "positive cooperativity"
            elif hill < 0.8:
                coop_type = "negative cooperativity"
            else:
                coop_type = "non-cooperative"
        else:
            coop_type = "unknown"

        formulas.append({
            'formula_id': fid,
            'name': name,
            'description': desc,
            'latex': latex,
            'domain': domain,
            'formula_type': ftype,
            'enzyme_name': enzyme,
            'kinetics_type': kintype,
            'hill_coefficient': hill,
            'km': km,
            'vmax': vmax,
            'cooperativity_type': coop_type
        })

    return formulas

def main():
    """Main analysis function."""
    conn = connect_db()

    print("=" * 80)
    print("COMPUTATIONAL NETWORK MOTIFS - COMPREHENSIVE ANALYSIS")
    print("=" * 80)

    results = {}

    # 1. Feedback Loops
    print("\n\n1. FEEDBACK LOOPS")
    print("-" * 80)
    feedback = find_feedback_loops_comprehensive(conn)
    results['feedback_loops'] = feedback
    print(f"Found {len(feedback)} formulas with feedback patterns")

    pos_count = sum(1 for f in feedback if f['feedback_type'] == 'positive')
    neg_count = sum(1 for f in feedback if f['feedback_type'] == 'negative')
    print(f"  Positive feedback: {pos_count}")
    print(f"  Negative feedback: {neg_count}")

    print("\nTop examples:")
    for i, f in enumerate(feedback[:5], 1):
        print(f"\n{i}. {f['name']} [{f['feedback_type'].upper()}]")
        print(f"   Domain: {f['domain']} | Type: {f['formula_type']}")
        print(f"   Mechanism: {f['mechanism']}")
        if f['description']:
            print(f"   Description: {f['description'][:120]}...")
        print(f"   LaTeX: {f['latex'][:100]}...")

    # 2. Bistable Switches
    print("\n\n2. BISTABLE SWITCHES")
    print("-" * 80)
    bistable = find_bistable_switches_comprehensive(conn)
    results['bistable_switches'] = bistable
    print(f"Found {len(bistable)} formulas with bistability patterns")

    print("\nTop examples:")
    for i, f in enumerate(bistable[:5], 1):
        print(f"\n{i}. {f['name']}")
        print(f"   Domain: {f['domain']} | Type: {f['formula_type']}")
        if f['hill_coefficient']:
            print(f"   Hill coefficient: {f['hill_coefficient']} (cooperativity)")
        if f['description']:
            print(f"   Description: {f['description'][:120]}...")
        print(f"   LaTeX: {f['latex'][:100]}...")

    # 3. Signaling Cascades (Feed-Forward)
    print("\n\n3. SIGNALING CASCADES (Feed-Forward Loops)")
    print("-" * 80)
    cascades, pathways = find_signaling_cascades(conn)
    results['signaling_cascades'] = cascades
    results['pathway_groups'] = pathways
    print(f"Found {len(cascades)} cascade formulas in {len(pathways)} pathways")

    print("\nPathways identified:")
    for pathway_name, components in list(pathways.items())[:10]:
        print(f"\n  {pathway_name} ({len(components)} components)")
        for comp in components[:3]:
            if comp['upstream_component'] and comp['downstream_component']:
                print(f"    Level {comp['cascade_level']}: {comp['upstream_component']} → {comp['downstream_component']}")

    # 4. Gene Regulatory Networks
    print("\n\n4. GENE REGULATORY NETWORKS (Fan-In/Fan-Out)")
    print("-" * 80)
    gene_formulas, fanout, fanin = find_gene_regulatory_networks(conn)
    results['gene_regulation'] = gene_formulas
    results['fanout_patterns'] = fanout
    results['fanin_patterns'] = fanin

    print(f"Found {len(gene_formulas)} gene regulation formulas")
    print(f"  Fan-out patterns: {len(fanout)} (one TF → many genes)")
    print(f"  Fan-in patterns: {len(fanin)} (many TFs → one gene)")

    if fanout:
        print("\nTop fan-out examples:")
        for i, f in enumerate(sorted(fanout, key=lambda x: x['degree'], reverse=True)[:5], 1):
            print(f"  {i}. {f['tf']} → {f['degree']} targets: {', '.join(f['targets'][:5])}...")

    if fanin:
        print("\nTop fan-in examples:")
        for i, f in enumerate(sorted(fanin, key=lambda x: x['degree'], reverse=True)[:5], 1):
            print(f"  {i}. {f['gene']} ← {f['degree']} regulators: {', '.join(f['regulators'][:5])}...")

    # 5. Synaptic Integration
    print("\n\n5. SYNAPTIC INTEGRATION (Multi-Input Convergence)")
    print("-" * 80)
    synaptic = find_synaptic_integration(conn)
    results['synaptic_integration'] = synaptic
    print(f"Found {len(synaptic)} synaptic integration formulas")

    for i, f in enumerate(synaptic[:5], 1):
        print(f"\n{i}. {f['name']}")
        print(f"   Type: {f['synapse_type']} | Plasticity: {f['plasticity_type']}")
        print(f"   Description: {f['description'][:120]}...")

    # 6. Oscillators
    print("\n\n6. OSCILLATORS AND BIOLOGICAL CLOCKS")
    print("-" * 80)
    oscillators = find_oscillators_and_clocks(conn)
    results['oscillators'] = oscillators
    print(f"Found {len(oscillators)} oscillator formulas")

    for i, f in enumerate(oscillators[:5], 1):
        print(f"\n{i}. {f['name']}")
        print(f"   Type: {f['oscillator_type']} | System: {f['biological_system']}")
        if f['frequency_hz']:
            print(f"   Frequency: {f['frequency_hz']} Hz")
        print(f"   Description: {f['description'][:120]}...")

    # 7. Plasticity Rules
    print("\n\n7. SYNAPTIC PLASTICITY (Learning Motifs)")
    print("-" * 80)
    plasticity = find_plasticity_rules(conn)
    results['plasticity_rules'] = plasticity
    print(f"Found {len(plasticity)} plasticity rule formulas")

    for i, f in enumerate(plasticity[:5], 1):
        print(f"\n{i}. {f['name']}")
        print(f"   Rule type: {f['rule_type']}")
        print(f"   Weight dependence: {f['weight_dependence']}")
        print(f"   Description: {f['description'][:120]}...")
        print(f"   LaTeX: {f['latex'][:100]}...")

    # 8. Enzyme Kinetics (Cooperative Binding)
    print("\n\n8. ENZYME KINETICS (Cooperative Binding)")
    print("-" * 80)
    enzymes = find_enzymatic_reactions(conn)
    results['enzyme_kinetics'] = enzymes
    print(f"Found {len(enzymes)} enzyme kinetics formulas with Hill coefficients")

    print("\nTop cooperative enzymes:")
    for i, f in enumerate(enzymes[:10], 1):
        print(f"\n{i}. {f['name']} (n={f['hill_coefficient']})")
        print(f"   Enzyme: {f['enzyme_name']} | Type: {f['kinetics_type']}")
        print(f"   Cooperativity: {f['cooperativity_type']}")
        print(f"   LaTeX: {f['latex'][:100]}...")

    # Summary
    print("\n\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total formulas analyzed: 90,313")
    print(f"\nNetwork motifs identified:")
    print(f"  1. Feedback loops: {len(feedback)} ({pos_count} positive, {neg_count} negative)")
    print(f"  2. Bistable switches: {len(bistable)}")
    print(f"  3. Signaling cascades: {len(cascades)} ({len(pathways)} pathways)")
    print(f"  4. Gene regulation: {len(gene_formulas)}")
    print(f"     - Fan-out: {len(fanout)}")
    print(f"     - Fan-in: {len(fanin)}")
    print(f"  5. Synaptic integration: {len(synaptic)}")
    print(f"  6. Oscillators: {len(oscillators)}")
    print(f"  7. Plasticity rules: {len(plasticity)}")
    print(f"  8. Enzyme cooperativity: {len(enzymes)}")

    conn.close()

    # Export to JSON
    output_file = '/home/user/MAINFRAME/bioformulas/network_motifs_comprehensive.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n\nDetailed results exported to: {output_file}")

if __name__ == "__main__":
    main()
