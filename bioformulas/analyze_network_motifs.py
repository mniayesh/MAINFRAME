#!/usr/bin/env python3
"""
Analyze bioformulas database for computational network motifs.
"""

import sqlite3
import json
import re
from collections import defaultdict

DB_PATH = '/home/user/MAINFRAME/bioformulas/bioformulas.db'

def connect_db():
    """Connect to the database."""
    return sqlite3.connect(DB_PATH)

def find_feedback_loops(conn):
    """Find formulas exhibiting feedback loop patterns."""
    cursor = conn.cursor()

    # Look for feedback patterns in various formula types
    feedback_formulas = []

    # Query formulas with descriptions or symbolic expressions containing feedback indicators
    query = """
    SELECT f.formula_id, f.name, f.description, f.symbolic, f.latex, f.formula_type, f.domain
    FROM formulas f
    WHERE (
        f.description LIKE '%feedback%' OR
        f.description LIKE '%autoregulation%' OR
        f.description LIKE '%autoinhibit%' OR
        f.description LIKE '%self-regulation%' OR
        f.name LIKE '%feedback%' OR
        f.symbolic LIKE '%**2%' OR  -- squared terms often indicate feedback
        f.symbolic LIKE '%**3%'     -- higher order terms
    )
    AND f.symbolic IS NOT NULL
    LIMIT 200
    """

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        formula_id, name, desc, symbolic, latex, ftype, domain = row

        # Classify as positive or negative feedback
        feedback_type = "unknown"
        if desc:
            desc_lower = desc.lower()
            if any(word in desc_lower for word in ['positive feedback', 'activation', 'amplif', 'cooperative']):
                feedback_type = "positive"
            elif any(word in desc_lower for word in ['negative feedback', 'inhibit', 'suppress', 'dampen']):
                feedback_type = "negative"

        feedback_formulas.append({
            'formula_id': formula_id,
            'name': name,
            'description': desc,
            'symbolic': symbolic,
            'latex': latex,
            'formula_type': ftype,
            'domain': domain,
            'feedback_type': feedback_type
        })

    return feedback_formulas

def find_bistable_switches(conn):
    """Find formulas exhibiting bistability (two stable states)."""
    cursor = conn.cursor()

    # Bistability often involves:
    # - Hill functions with high coefficients
    # - Mutual inhibition
    # - Positive feedback with saturation

    query = """
    SELECT f.formula_id, f.name, f.description, f.symbolic, f.latex, f.formula_type, f.domain,
           ek.hill_coefficient
    FROM formulas f
    LEFT JOIN enzyme_kinetics ek ON f.formula_id = ek.formula_id
    WHERE (
        f.description LIKE '%bistable%' OR
        f.description LIKE '%switch%' OR
        f.description LIKE '%hysteresis%' OR
        f.description LIKE '%mutual inhibition%' OR
        f.description LIKE '%toggle%' OR
        ek.hill_coefficient > 2.0 OR
        f.name LIKE '%switch%' OR
        f.name LIKE '%bistable%'
    )
    AND f.symbolic IS NOT NULL
    LIMIT 200
    """

    cursor.execute(query)
    results = cursor.fetchall()

    bistable_formulas = []
    for row in results:
        formula_id, name, desc, symbolic, latex, ftype, domain, hill = row
        bistable_formulas.append({
            'formula_id': formula_id,
            'name': name,
            'description': desc,
            'symbolic': symbolic,
            'latex': latex,
            'formula_type': ftype,
            'domain': domain,
            'hill_coefficient': hill
        })

    return bistable_formulas

def find_feedforward_loops(conn):
    """Find formulas exhibiting feed-forward loop patterns."""
    cursor = conn.cursor()

    # Look for signaling cascades and multi-step activation
    query = """
    SELECT f.formula_id, f.name, f.description, f.symbolic, f.latex, f.formula_type, f.domain,
           sc.pathway_name, sc.cascade_level, sc.upstream_component, sc.downstream_component
    FROM formulas f
    LEFT JOIN signaling_cascades sc ON f.formula_id = sc.formula_id
    WHERE (
        f.description LIKE '%cascade%' OR
        f.description LIKE '%feed-forward%' OR
        f.description LIKE '%feedforward%' OR
        f.description LIKE '%multi-step%' OR
        sc.cascade_id IS NOT NULL
    )
    AND f.symbolic IS NOT NULL
    LIMIT 200
    """

    cursor.execute(query)
    results = cursor.fetchall()

    feedforward_formulas = []
    for row in results:
        formula_id, name, desc, symbolic, latex, ftype, domain, pathway, level, upstream, downstream = row
        feedforward_formulas.append({
            'formula_id': formula_id,
            'name': name,
            'description': desc,
            'symbolic': symbolic,
            'latex': latex,
            'formula_type': ftype,
            'domain': domain,
            'pathway_name': pathway,
            'cascade_level': level,
            'upstream_component': upstream,
            'downstream_component': downstream
        })

    return feedforward_formulas

def find_fanout_patterns(conn):
    """Find fan-out patterns: one signal → many targets."""
    cursor = conn.cursor()

    # Look for formulas where one input affects multiple outputs
    # This includes gene regulation and signaling pathways

    query = """
    SELECT f.formula_id, f.name, f.description, f.symbolic, f.latex, f.formula_type, f.domain,
           gr.transcription_factor, gr.gene_name
    FROM formulas f
    LEFT JOIN gene_regulation gr ON f.formula_id = gr.formula_id
    WHERE (
        f.description LIKE '%multiple targets%' OR
        f.description LIKE '%branching%' OR
        f.description LIKE '%divergent%' OR
        f.description LIKE '%broadcast%' OR
        gr.transcription_factor IS NOT NULL
    )
    AND f.symbolic IS NOT NULL
    LIMIT 200
    """

    cursor.execute(query)
    results = cursor.fetchall()

    fanout_formulas = []
    for row in results:
        formula_id, name, desc, symbolic, latex, ftype, domain, tf, gene = row
        fanout_formulas.append({
            'formula_id': formula_id,
            'name': name,
            'description': desc,
            'symbolic': symbolic,
            'latex': latex,
            'formula_type': ftype,
            'domain': domain,
            'transcription_factor': tf,
            'gene_name': gene
        })

    return fanout_formulas

def find_fanin_patterns(conn):
    """Find fan-in patterns: many signals → one target."""
    cursor = conn.cursor()

    # Look for formulas with multiple inputs converging
    # Including synaptic integration and signal summation

    query = """
    SELECT f.formula_id, f.name, f.description, f.symbolic, f.latex, f.formula_type, f.domain
    FROM formulas f
    WHERE (
        f.description LIKE '%integration%' OR
        f.description LIKE '%summation%' OR
        f.description LIKE '%convergent%' OR
        f.description LIKE '%multiple inputs%' OR
        f.description LIKE '%combinatorial%' OR
        f.name LIKE '%integration%' OR
        f.name LIKE '%summation%'
    )
    AND f.symbolic IS NOT NULL
    AND f.symbolic LIKE '%+%'  -- Contains addition (multiple inputs)
    LIMIT 200
    """

    cursor.execute(query)
    results = cursor.fetchall()

    fanin_formulas = []
    for row in results:
        formula_id, name, desc, symbolic, latex, ftype, domain = row

        # Count number of additive terms as proxy for fan-in degree
        if symbolic:
            fanin_degree = symbolic.count('+') + 1
        else:
            fanin_degree = 0

        fanin_formulas.append({
            'formula_id': formula_id,
            'name': name,
            'description': desc,
            'symbolic': symbolic,
            'latex': latex,
            'formula_type': ftype,
            'domain': domain,
            'fanin_degree': fanin_degree
        })

    return fanin_formulas

def find_coherent_incoherent_loops(conn):
    """Find coherent vs incoherent feed-forward loops."""
    cursor = conn.cursor()

    # Coherent: all paths have same sign (all activation or all inhibition)
    # Incoherent: mixed signs (activation through one path, inhibition through another)

    query = """
    SELECT f.formula_id, f.name, f.description, f.symbolic, f.latex, f.formula_type, f.domain,
           gr.regulation_type
    FROM formulas f
    LEFT JOIN gene_regulation gr ON f.formula_id = gr.formula_id
    WHERE (
        f.description LIKE '%coherent%' OR
        f.description LIKE '%incoherent%' OR
        (f.description LIKE '%activation%' AND f.description LIKE '%repression%') OR
        gr.regulation_type = 'mixed'
    )
    AND f.symbolic IS NOT NULL
    LIMIT 200
    """

    cursor.execute(query)
    results = cursor.fetchall()

    loop_formulas = []
    for row in results:
        formula_id, name, desc, symbolic, latex, ftype, domain, reg_type = row

        # Classify loop type
        loop_type = "unknown"
        if desc:
            desc_lower = desc.lower()
            if 'incoherent' in desc_lower:
                loop_type = "incoherent"
            elif 'coherent' in desc_lower:
                loop_type = "coherent"

        if reg_type == 'mixed':
            loop_type = "incoherent"

        loop_formulas.append({
            'formula_id': formula_id,
            'name': name,
            'description': desc,
            'symbolic': symbolic,
            'latex': latex,
            'formula_type': ftype,
            'domain': domain,
            'loop_type': loop_type,
            'regulation_type': reg_type
        })

    return loop_formulas

def analyze_hill_functions(conn):
    """Analyze Hill functions which are key to nonlinear switching."""
    cursor = conn.cursor()

    query = """
    SELECT f.formula_id, f.name, f.description, f.symbolic, f.latex, f.domain,
           ek.hill_coefficient, ek.km, ek.enzyme_name
    FROM formulas f
    JOIN enzyme_kinetics ek ON f.formula_id = ek.formula_id
    WHERE ek.hill_coefficient IS NOT NULL
    AND f.symbolic IS NOT NULL
    ORDER BY ek.hill_coefficient DESC
    LIMIT 100
    """

    cursor.execute(query)
    results = cursor.fetchall()

    hill_formulas = []
    for row in results:
        formula_id, name, desc, symbolic, latex, domain, hill, km, enzyme = row
        hill_formulas.append({
            'formula_id': formula_id,
            'name': name,
            'description': desc,
            'symbolic': symbolic,
            'latex': latex,
            'domain': domain,
            'hill_coefficient': hill,
            'km': km,
            'enzyme_name': enzyme
        })

    return hill_formulas

def main():
    """Main analysis function."""
    conn = connect_db()

    print("=" * 80)
    print("COMPUTATIONAL NETWORK MOTIFS IN BIOFORMULAS DATABASE")
    print("=" * 80)

    # 1. Feedback Loops
    print("\n\n1. FEEDBACK LOOPS (Positive and Negative)")
    print("-" * 80)
    feedback = find_feedback_loops(conn)
    print(f"Found {len(feedback)} formulas with feedback patterns\n")

    for i, f in enumerate(feedback[:10], 1):
        print(f"\n{i}. {f['name']} [{f['feedback_type'].upper()}]")
        print(f"   Domain: {f['domain']} | Type: {f['formula_type']}")
        if f['description']:
            print(f"   Description: {f['description'][:150]}...")
        if f['symbolic']:
            print(f"   Symbolic: {f['symbolic'][:100]}...")

    # 2. Bistable Switches
    print("\n\n2. BISTABLE SWITCHES (Two Stable States)")
    print("-" * 80)
    bistable = find_bistable_switches(conn)
    print(f"Found {len(bistable)} formulas with bistability patterns\n")

    for i, f in enumerate(bistable[:10], 1):
        print(f"\n{i}. {f['name']}")
        print(f"   Domain: {f['domain']} | Type: {f['formula_type']}")
        if f['hill_coefficient']:
            print(f"   Hill Coefficient: {f['hill_coefficient']}")
        if f['description']:
            print(f"   Description: {f['description'][:150]}...")
        if f['symbolic']:
            print(f"   Symbolic: {f['symbolic'][:100]}...")

    # 3. Feed-Forward Loops
    print("\n\n3. FEED-FORWARD LOOPS (A→B→C and A→C)")
    print("-" * 80)
    feedforward = find_feedforward_loops(conn)
    print(f"Found {len(feedforward)} formulas with feed-forward patterns\n")

    for i, f in enumerate(feedforward[:10], 1):
        print(f"\n{i}. {f['name']}")
        print(f"   Domain: {f['domain']} | Type: {f['formula_type']}")
        if f['pathway_name']:
            print(f"   Pathway: {f['pathway_name']} | Level: {f['cascade_level']}")
            print(f"   {f['upstream_component']} → {f['downstream_component']}")
        if f['description']:
            print(f"   Description: {f['description'][:150]}...")

    # 4. Fan-Out Patterns
    print("\n\n4. FAN-OUT PATTERNS (One Signal → Many Targets)")
    print("-" * 80)
    fanout = find_fanout_patterns(conn)
    print(f"Found {len(fanout)} formulas with fan-out patterns\n")

    for i, f in enumerate(fanout[:10], 1):
        print(f"\n{i}. {f['name']}")
        print(f"   Domain: {f['domain']} | Type: {f['formula_type']}")
        if f['transcription_factor']:
            print(f"   TF: {f['transcription_factor']} → Gene: {f['gene_name']}")
        if f['description']:
            print(f"   Description: {f['description'][:150]}...")

    # 5. Fan-In Patterns
    print("\n\n5. FAN-IN PATTERNS (Many Signals → One Target)")
    print("-" * 80)
    fanin = find_fanin_patterns(conn)
    print(f"Found {len(fanin)} formulas with fan-in patterns\n")

    for i, f in enumerate(fanin[:10], 1):
        print(f"\n{i}. {f['name']} [Degree: {f['fanin_degree']}]")
        print(f"   Domain: {f['domain']} | Type: {f['formula_type']}")
        if f['description']:
            print(f"   Description: {f['description'][:150]}...")
        if f['symbolic']:
            print(f"   Symbolic: {f['symbolic'][:100]}...")

    # 6. Coherent vs Incoherent Loops
    print("\n\n6. COHERENT vs INCOHERENT LOOPS")
    print("-" * 80)
    loops = find_coherent_incoherent_loops(conn)
    print(f"Found {len(loops)} formulas with coherent/incoherent patterns\n")

    for i, f in enumerate(loops[:10], 1):
        print(f"\n{i}. {f['name']} [{f['loop_type'].upper()}]")
        print(f"   Domain: {f['domain']} | Type: {f['formula_type']}")
        if f['regulation_type']:
            print(f"   Regulation: {f['regulation_type']}")
        if f['description']:
            print(f"   Description: {f['description'][:150]}...")

    # 7. Hill Functions Analysis
    print("\n\n7. HILL FUNCTIONS (Nonlinear Switching)")
    print("-" * 80)
    hill = analyze_hill_functions(conn)
    print(f"Found {len(hill)} formulas with Hill coefficients\n")

    for i, f in enumerate(hill[:10], 1):
        print(f"\n{i}. {f['name']} [n={f['hill_coefficient']}]")
        print(f"   Domain: {f['domain']} | Enzyme: {f['enzyme_name']}")
        if f['km']:
            print(f"   Km: {f['km']}")
        if f['symbolic']:
            print(f"   Symbolic: {f['symbolic'][:100]}...")

    # Summary statistics
    print("\n\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(f"Feedback Loops: {len(feedback)}")
    print(f"  - Positive: {sum(1 for f in feedback if f['feedback_type'] == 'positive')}")
    print(f"  - Negative: {sum(1 for f in feedback if f['feedback_type'] == 'negative')}")
    print(f"\nBistable Switches: {len(bistable)}")
    print(f"Feed-Forward Loops: {len(feedforward)}")
    print(f"Fan-Out Patterns: {len(fanout)}")
    print(f"Fan-In Patterns: {len(fanin)}")
    print(f"Coherent/Incoherent Loops: {len(loops)}")
    print(f"  - Coherent: {sum(1 for f in loops if f['loop_type'] == 'coherent')}")
    print(f"  - Incoherent: {sum(1 for f in loops if f['loop_type'] == 'incoherent')}")
    print(f"\nHill Functions: {len(hill)}")

    conn.close()

    # Export results to JSON
    results = {
        'feedback_loops': feedback,
        'bistable_switches': bistable,
        'feedforward_loops': feedforward,
        'fanout_patterns': fanout,
        'fanin_patterns': fanin,
        'coherent_incoherent_loops': loops,
        'hill_functions': hill
    }

    with open('/home/user/MAINFRAME/bioformulas/network_motifs.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n\nResults exported to: /home/user/MAINFRAME/bioformulas/network_motifs.json")

if __name__ == "__main__":
    main()
