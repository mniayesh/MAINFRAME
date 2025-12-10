"""
Sample Data Population Script for Biological Architectural Primitives Database

This script demonstrates how to populate the database with sample data from
various sources, including:
- Top-tier entities (mechanisms, processes, circuit motifs, etc.)
- Middle-tier entities (enzymes, receptors, cell types, etc.)
- Relationships between entities
- Computational mappings
- Cross-references to external databases
- Formulas and parameters

Usage:
    python populate_bio_architecture_db.py

This will create and populate a new database with sample data.
"""

from bio_architecture_db_utils import BioArchDB
import json


def populate_mechanisms(db: BioArchDB):
    """Populate sample mechanisms."""
    print("\n=== Populating Mechanisms ===")

    mechanisms = [
        {
            'identifier': 'MECH_001',
            'name': 'Lateral Inhibition',
            'description': 'Mechanism where active neurons suppress neighboring neurons to enhance contrast',
            'update_rule': 'dy_i/dt = -y_i + f(x_i - sum(w_ij * y_j))',
            'mechanism_class': 'lateral_inhibition',
            'time_scale_ms': 50.0,
            'reversibility': True,
            'confidence_score': 0.95,
            'evidence_strength': 'experimental'
        },
        {
            'identifier': 'MECH_002',
            'name': 'Hebbian Learning',
            'description': 'Synaptic plasticity mechanism: neurons that fire together wire together',
            'update_rule': 'dw_ij/dt = eta * x_i * y_j',
            'mechanism_class': 'synaptic_plasticity',
            'time_scale_ms': 1000.0,
            'reversibility': False,
            'confidence_score': 0.98,
            'evidence_strength': 'experimental'
        },
        {
            'identifier': 'MECH_003',
            'name': 'Spike-Timing Dependent Plasticity',
            'description': 'Synaptic strength modulated by precise timing of pre- and post-synaptic spikes',
            'update_rule': 'dw/dt = A+ * exp(-Δt/τ+) if Δt > 0 else A- * exp(Δt/τ-)',
            'mechanism_class': 'synaptic_plasticity',
            'time_scale_ms': 20.0,
            'reversibility': True,
            'confidence_score': 0.96,
            'evidence_strength': 'experimental'
        },
        {
            'identifier': 'MECH_004',
            'name': 'Feedback Inhibition',
            'description': 'Output inhibits its own production to maintain homeostasis',
            'update_rule': 'dx/dt = k_prod - k_deg * x - k_fb * x^n',
            'mechanism_class': 'feedback',
            'time_scale_ms': 100.0,
            'reversibility': True,
            'confidence_score': 0.92,
            'evidence_strength': 'experimental'
        },
        {
            'identifier': 'MECH_005',
            'name': 'Feedforward Activation',
            'description': 'Input activates both output and inhibitor of output',
            'update_rule': 'dy/dt = k1 * x - k2 * y - k3 * z * y; dz/dt = k4 * x - k5 * z',
            'mechanism_class': 'feedforward',
            'time_scale_ms': 75.0,
            'reversibility': True,
            'confidence_score': 0.90,
            'evidence_strength': 'experimental'
        }
    ]

    mechanism_ids = []
    for mech in mechanisms:
        mech_id = db.create_mechanism(**mech)
        mechanism_ids.append(mech_id)
        print(f"  Created: {mech['name']} (ID: {mech_id})")

    return mechanism_ids


def populate_processes(db: BioArchDB):
    """Populate sample biological processes."""
    print("\n=== Populating Processes ===")

    processes = [
        {
            'identifier': 'GO:0006096',
            'name': 'Glycolysis',
            'description': 'Metabolic process converting glucose to pyruvate with ATP production',
            'process_category': 'metabolic',
            'temporal_dynamics': 'sustained',
            'spatial_scale': 'cellular',
            'rate_equation': 'v = Vmax * [S] / (Km + [S])',
            'confidence_score': 0.99,
            'source_database': 'Gene Ontology'
        },
        {
            'identifier': 'GO:0007165',
            'name': 'Signal Transduction',
            'description': 'Transmission of molecular signals from cell exterior to interior',
            'process_category': 'signaling',
            'temporal_dynamics': 'transient',
            'spatial_scale': 'cellular',
            'rate_equation': 'cascade amplification model',
            'confidence_score': 0.95,
            'source_database': 'Gene Ontology'
        },
        {
            'identifier': 'PROC_001',
            'name': 'Action Potential Propagation',
            'description': 'Electrical signal propagation along axon via voltage-gated ion channels',
            'process_category': 'electrical',
            'temporal_dynamics': 'transient',
            'spatial_scale': 'cellular',
            'rate_equation': 'Hodgkin-Huxley model',
            'confidence_score': 0.97,
            'evidence_strength': 'experimental'
        },
        {
            'identifier': 'PROC_002',
            'name': 'Calcium Oscillations',
            'description': 'Rhythmic variations in intracellular calcium concentration',
            'process_category': 'signaling',
            'temporal_dynamics': 'oscillatory',
            'spatial_scale': 'cellular',
            'rate_equation': 'd[Ca]/dt = Jin - Jout + Jleak',
            'confidence_score': 0.93,
            'evidence_strength': 'experimental'
        }
    ]

    process_ids = []
    for proc in processes:
        proc_id = db.create_process(**proc)
        process_ids.append(proc_id)
        print(f"  Created: {proc['name']} (ID: {proc_id})")

    return process_ids


def populate_circuit_motifs(db: BioArchDB):
    """Populate sample circuit motifs."""
    print("\n=== Populating Circuit Motifs ===")

    # For circuit motifs, we need to use the generic create_entity since
    # we haven't implemented create_circuit_motif helper
    motifs_data = [
        {
            'identifier': 'MOTIF_001',
            'name': 'Feedforward Loop',
            'description': 'Three-node circuit where A regulates C directly and via B',
            'motif_topology': 'feedforward',
            'node_count': 3,
            'connection_pattern': 'A->B, A->C, B->C'
        },
        {
            'identifier': 'MOTIF_002',
            'name': 'Mutual Inhibition',
            'description': 'Two neurons inhibit each other, implementing bistability',
            'motif_topology': 'recurrent',
            'node_count': 2,
            'connection_pattern': 'A-|B, B-|A'
        }
    ]

    motif_ids = []
    for motif_data in motifs_data:
        # Separate type-specific fields
        type_specific = {
            'motif_topology': motif_data.pop('motif_topology'),
            'node_count': motif_data.pop('node_count'),
            'connection_pattern': motif_data.pop('connection_pattern')
        }

        # Create base entity
        motif_id = db.create_entity(
            entity_type='circuit_motif',
            confidence_score=0.90,
            **motif_data
        )

        # Insert type-specific data
        db.cursor.execute('''
            INSERT INTO circuit_motifs (motif_id, entity_id, motif_topology, node_count, connection_pattern)
            VALUES (?, ?, ?, ?, ?)
        ''', (motif_id, motif_id, type_specific['motif_topology'],
              type_specific['node_count'], type_specific['connection_pattern']))
        db.conn.commit()

        motif_ids.append(motif_id)
        print(f"  Created: {motif_data['name']} (ID: {motif_id})")

    return motif_ids


def populate_enzymes(db: BioArchDB):
    """Populate sample enzymes."""
    print("\n=== Populating Enzymes ===")

    enzymes = [
        {
            'identifier': 'UNIPROT:P00367',
            'name': 'Alcohol dehydrogenase 1A',
            'description': 'Catalyzes reversible oxidation of alcohols to aldehydes',
            'ec_number': 'EC 1.1.1.1',
            'km_value': 0.8,  # mM
            'kcat_value': 350.0,  # s^-1
            'catalytic_mechanism': 'Zinc-dependent oxidoreduction',
            'confidence_score': 0.98,
            'source_database': 'UniProt'
        },
        {
            'identifier': 'UNIPROT:P00558',
            'name': 'Phosphoglycerate kinase 1',
            'description': 'Key enzyme in glycolysis, catalyzes phosphoryl transfer',
            'ec_number': 'EC 2.7.2.3',
            'km_value': 0.15,
            'kcat_value': 500.0,
            'catalytic_mechanism': 'Phosphoryl transfer',
            'confidence_score': 0.99,
            'source_database': 'UniProt'
        }
    ]

    enzyme_ids = []
    for enz in enzymes:
        enz_id = db.create_enzyme(**enz)
        enzyme_ids.append(enz_id)
        print(f"  Created: {enz['name']} (ID: {enz_id})")

    return enzyme_ids


def populate_architectural_patterns(db: BioArchDB):
    """Populate architectural patterns."""
    print("\n=== Populating Architectural Patterns ===")

    patterns = [
        {
            'pattern_name': 'Winner-Take-All Network',
            'pattern_category': 'neural_network',
            'formal_description': 'Competitive network where strongest input suppresses all others',
            'pseudocode': '''
                for each node i:
                    activation[i] = input[i]
                    for each neighbor j:
                        activation[i] -= weight[i,j] * activation[j]
                    activation[i] = max(0, activation[i])
            ''',
            'complexity_class': 'O(n^2)',
            'properties': {'competitive': True, 'stable': True}
        },
        {
            'pattern_name': 'Leaky Integrator',
            'pattern_category': 'temporal_processing',
            'formal_description': 'Integrates input over time with exponential decay',
            'pseudocode': '''
                state = 0
                for each timestep:
                    state = leak_rate * state + input
            ''',
            'complexity_class': 'O(1)',
            'properties': {'temporal': True, 'continuous': True}
        },
        {
            'pattern_name': 'Recurrent Neural Network',
            'pattern_category': 'neural_network',
            'formal_description': 'Network with feedback connections enabling temporal dynamics',
            'pseudocode': '''
                hidden_state = zeros(n)
                for each timestep:
                    hidden_state = tanh(W_in @ input + W_rec @ hidden_state)
                    output = W_out @ hidden_state
            ''',
            'complexity_class': 'O(n^2)',
            'properties': {'recurrent': True, 'temporal': True}
        },
        {
            'pattern_name': 'Negative Feedback Controller',
            'pattern_category': 'control_flow',
            'formal_description': 'Control system maintaining setpoint via negative feedback',
            'pseudocode': '''
                error = setpoint - measured_value
                control_signal = Kp * error + Ki * integral(error) + Kd * derivative(error)
            ''',
            'complexity_class': 'O(1)',
            'properties': {'stable': True, 'homeostatic': True}
        },
        {
            'pattern_name': 'Sparse Distributed Representation',
            'pattern_category': 'data_structure',
            'formal_description': 'Information encoded in sparse pattern of active units',
            'pseudocode': '''
                encoding = zeros(N)  # Large N
                active_indices = hash_function(input)  # Small set
                encoding[active_indices] = 1
            ''',
            'complexity_class': 'O(k) where k << N',
            'properties': {'sparse': True, 'distributed': True, 'fault_tolerant': True}
        }
    ]

    pattern_ids = []
    for pattern in patterns:
        pattern_id = db.create_architectural_pattern(**pattern)
        pattern_ids.append(pattern_id)
        print(f"  Created: {pattern['pattern_name']} (ID: {pattern_id})")

    return pattern_ids


def populate_computational_mappings(db: BioArchDB, mechanism_ids, pattern_ids):
    """Create computational mappings between biological mechanisms and architectural patterns."""
    print("\n=== Populating Computational Mappings ===")

    # Mapping definitions: (mechanism_id_idx, pattern_id_idx, mapping_details)
    mappings = [
        # Lateral Inhibition -> Winner-Take-All
        (0, 0, {
            'mapping_type': 'isomorphic',
            'fidelity_score': 0.92,
            'description': 'Lateral inhibition implements winner-take-all competition through mutual suppression',
            'mathematical_correspondence': 'Inhibitory connections w_ij directly map to competitive suppression matrix',
            'validated': True
        }),

        # Hebbian Learning -> Recurrent Neural Network
        (1, 2, {
            'mapping_type': 'analogous',
            'fidelity_score': 0.85,
            'description': 'Hebbian synaptic modification enables recurrent network learning',
            'mathematical_correspondence': 'Weight update rule Δw = η·x·y maps to gradient descent on recurrent weights',
            'validated': True
        }),

        # STDP -> Recurrent Neural Network
        (2, 2, {
            'mapping_type': 'analogous',
            'fidelity_score': 0.88,
            'description': 'STDP implements temporally-asymmetric Hebbian learning in recurrent networks',
            'mathematical_correspondence': 'Timing-dependent window function maps to temporal credit assignment',
            'validated': True
        }),

        # Feedback Inhibition -> Negative Feedback Controller
        (3, 3, {
            'mapping_type': 'isomorphic',
            'fidelity_score': 0.94,
            'description': 'Biological feedback inhibition implements classic negative feedback control',
            'mathematical_correspondence': 'Inhibition term k_fb·x^n maps to proportional feedback control',
            'validated': True
        }),

        # Hebbian Learning -> Sparse Distributed Representation
        (1, 4, {
            'mapping_type': 'approximates',
            'fidelity_score': 0.70,
            'description': 'Hebbian learning can develop sparse distributed representations through competition',
            'mathematical_correspondence': 'Lateral inhibition + Hebbian learning → sparse codes',
            'validated': False
        })
    ]

    mapping_ids = []
    for mech_idx, pattern_idx, details in mappings:
        if mech_idx < len(mechanism_ids) and pattern_idx < len(pattern_ids):
            mapping_id = db.add_computational_mapping(
                entity_id=mechanism_ids[mech_idx],
                pattern_id=pattern_ids[pattern_idx],
                **details
            )
            mapping_ids.append(mapping_id)

            # Get names for display
            mech = db.get_entity_by_id(mechanism_ids[mech_idx])
            pattern = db.cursor.execute(
                'SELECT pattern_name FROM architectural_patterns WHERE pattern_id = ?',
                (pattern_ids[pattern_idx],)
            ).fetchone()

            print(f"  Mapped: {mech['name']} → {pattern[0]} (fidelity: {details['fidelity_score']})")

    return mapping_ids


def populate_relationships(db: BioArchDB, mechanism_ids, process_ids):
    """Create relationships between entities."""
    print("\n=== Populating Relationships ===")

    relationships = []

    # Mechanisms participate in processes
    if len(mechanism_ids) >= 3 and len(process_ids) >= 1:
        # STDP is part of signal transduction
        rel_id = db.add_relationship(
            source_entity_id=process_ids[1],  # Signal Transduction
            target_entity_id=mechanism_ids[2],  # STDP
            relationship_type='has_part',
            strength=0.8,
            confidence=0.9,
            context='STDP is a mechanism within signal transduction at synapses'
        )
        relationships.append(rel_id)
        print(f"  Created relationship: Signal Transduction has_part STDP")

    # Mechanisms regulate each other
    if len(mechanism_ids) >= 4:
        # Feedback inhibition regulates Hebbian learning
        rel_id = db.add_relationship(
            source_entity_id=mechanism_ids[3],  # Feedback Inhibition
            target_entity_id=mechanism_ids[1],  # Hebbian Learning
            relationship_type='regulates',
            strength=0.7,
            confidence=0.85,
            context='Feedback mechanisms can modulate synaptic plasticity'
        )
        relationships.append(rel_id)
        print(f"  Created relationship: Feedback Inhibition regulates Hebbian Learning")

    # Similar mechanisms
    if len(mechanism_ids) >= 3:
        # Hebbian and STDP are similar
        rel_id = db.add_relationship(
            source_entity_id=mechanism_ids[1],  # Hebbian
            target_entity_id=mechanism_ids[2],  # STDP
            relationship_type='similar_to',
            strength=0.85,
            confidence=0.95,
            context='Both are synaptic plasticity mechanisms'
        )
        relationships.append(rel_id)
        print(f"  Created relationship: Hebbian Learning similar_to STDP")

    return relationships


def populate_cross_references(db: BioArchDB, mechanism_ids, process_ids, enzyme_ids):
    """Add cross-references to external databases."""
    print("\n=== Populating Cross-References ===")

    xrefs = []

    # Mechanisms to ModelDB
    if mechanism_ids:
        xref_id = db.add_cross_reference(
            entity_id=mechanism_ids[0],  # Lateral Inhibition
            database_name='ModelDB',
            external_id='12345',
            external_url='https://modeldb.science/12345',
            confidence=0.9
        )
        xrefs.append(xref_id)
        print(f"  Added cross-ref: Lateral Inhibition → ModelDB:12345")

    # Processes to GO
    if process_ids:
        xref_id = db.add_cross_reference(
            entity_id=process_ids[0],  # Glycolysis
            database_name='GO',
            external_id='GO:0006096',
            external_url='http://geneontology.org/GO:0006096',
            confidence=1.0
        )
        xrefs.append(xref_id)
        print(f"  Added cross-ref: Glycolysis → GO:0006096")

    # Enzymes to UniProt
    for i, enzyme_id in enumerate(enzyme_ids[:2]):
        enzyme = db.get_entity_by_id(enzyme_id)
        uniprot_id = enzyme['identifier'].replace('UNIPROT:', '')

        xref_id = db.add_cross_reference(
            entity_id=enzyme_id,
            database_name='UniProt',
            external_id=uniprot_id,
            external_url=f'https://www.uniprot.org/uniprot/{uniprot_id}',
            confidence=0.99
        )
        xrefs.append(xref_id)
        print(f"  Added cross-ref: {enzyme['name']} → UniProt:{uniprot_id}")

    return xrefs


def populate_parameters(db: BioArchDB, mechanism_ids):
    """Add quantitative parameters to entities."""
    print("\n=== Populating Parameters ===")

    parameters = []

    if mechanism_ids:
        # Time constant for lateral inhibition
        param_id = db.add_parameter(
            entity_id=mechanism_ids[0],
            parameter_type='time_constant',
            value=50.0,
            uncertainty=5.0,
            value_min=40.0,
            value_max=60.0,
            organism='Homo sapiens',
            confidence=0.90
        )
        parameters.append(param_id)
        print(f"  Added parameter: time_constant = 50.0 ms (Lateral Inhibition)")

        # Rate constant for Hebbian learning
        if len(mechanism_ids) >= 2:
            param_id = db.add_parameter(
                entity_id=mechanism_ids[1],
                parameter_type='rate_constant',
                value=0.001,
                uncertainty=0.0002,
                organism='Rattus norvegicus',
                confidence=0.85
            )
            parameters.append(param_id)
            print(f"  Added parameter: rate_constant = 0.001 s^-1 (Hebbian Learning)")

    return parameters


def populate_formulas(db: BioArchDB):
    """Add formulas to the database."""
    print("\n=== Populating Formulas ===")

    formulas = [
        {
            'name': 'Michaelis-Menten Equation',
            'category_id': 1,  # kinetics
            'latex_notation': r'v = \frac{V_{max} [S]}{K_m + [S]}',
            'python_code': 'v = (V_max * S) / (K_m + S)',
            'description': 'Describes rate of enzymatic reactions',
            'formula_type': 'algebraic',
            'dimensionality': 'scalar',
            'variables_json': json.dumps([
                {'name': 'v', 'description': 'reaction rate', 'unit': 'M/s'},
                {'name': 'S', 'description': 'substrate concentration', 'unit': 'M'},
                {'name': 'V_max', 'description': 'maximum rate', 'unit': 'M/s'},
                {'name': 'K_m', 'description': 'Michaelis constant', 'unit': 'M'}
            ]),
            'validated': True
        },
        {
            'name': 'Hodgkin-Huxley Equations',
            'category_id': 4,  # electrophysiology
            'latex_notation': r'C_m \frac{dV}{dt} = I_{ext} - \bar{g}_{Na} m^3 h (V - E_{Na}) - \bar{g}_K n^4 (V - E_K) - \bar{g}_L (V - E_L)',
            'python_code': 'dV_dt = (I_ext - g_Na * m**3 * h * (V - E_Na) - g_K * n**4 * (V - E_K) - g_L * (V - E_L)) / C_m',
            'description': 'Mathematical model of action potential generation',
            'formula_type': 'differential',
            'dimensionality': 'vector',
            'validated': True
        },
        {
            'name': 'Hebbian Learning Rule',
            'category_id': 2,  # dynamics
            'latex_notation': r'\frac{dw_{ij}}{dt} = \eta x_i y_j',
            'python_code': 'dw_dt = eta * x_i * y_j',
            'description': 'Synaptic weight change proportional to pre- and post-synaptic activity',
            'formula_type': 'differential',
            'dimensionality': 'matrix',
            'validated': True
        }
    ]

    formula_ids = []
    for formula in formulas:
        db.cursor.execute('''
            INSERT INTO formulas (
                name, category_id, latex_notation, python_code,
                description, formula_type, dimensionality,
                variables_json, validated
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            formula['name'], formula['category_id'], formula['latex_notation'],
            formula['python_code'], formula['description'], formula['formula_type'],
            formula['dimensionality'], formula.get('variables_json'),
            formula['validated']
        ))
        formula_id = db.cursor.lastrowid
        formula_ids.append(formula_id)
        print(f"  Created: {formula['name']} (ID: {formula_id})")

    db.conn.commit()
    return formula_ids


def link_formulas_to_entities(db: BioArchDB, mechanism_ids, enzyme_ids, formula_ids):
    """Link formulas to relevant entities."""
    print("\n=== Linking Formulas to Entities ===")

    links = []

    # Michaelis-Menten to enzymes
    if formula_ids and enzyme_ids:
        for enzyme_id in enzyme_ids:
            db.cursor.execute('''
                INSERT INTO entity_formulas (entity_id, formula_id, role)
                VALUES (?, ?, ?)
            ''', (enzyme_id, formula_ids[0], 'governing_equation'))
            links.append(db.cursor.lastrowid)

        enzyme = db.get_entity_by_id(enzyme_ids[0])
        print(f"  Linked: Michaelis-Menten → {enzyme['name']}")

    # Hebbian learning rule to Hebbian mechanism
    if len(formula_ids) >= 3 and len(mechanism_ids) >= 2:
        db.cursor.execute('''
            INSERT INTO entity_formulas (entity_id, formula_id, role)
            VALUES (?, ?, ?)
        ''', (mechanism_ids[1], formula_ids[2], 'governing_equation'))
        links.append(db.cursor.lastrowid)
        print(f"  Linked: Hebbian Learning Rule → Hebbian Learning mechanism")

    db.conn.commit()
    return links


def main():
    """Main population script."""
    print("=" * 70)
    print("Biological Architectural Primitives Database - Sample Data Population")
    print("=" * 70)

    # Initialize database
    db = BioArchDB('bio_architecture.db')

    # Initialize schema
    print("\n=== Initializing Database Schema ===")
    try:
        db.initialize_schema('bio_architecture_schema.sql')
        print("Schema initialized successfully")
    except Exception as e:
        print(f"Schema initialization failed (may already exist): {e}")

    # Populate data
    mechanism_ids = populate_mechanisms(db)
    process_ids = populate_processes(db)
    motif_ids = populate_circuit_motifs(db)
    enzyme_ids = populate_enzymes(db)
    pattern_ids = populate_architectural_patterns(db)

    # Create connections
    mapping_ids = populate_computational_mappings(db, mechanism_ids, pattern_ids)
    relationship_ids = populate_relationships(db, mechanism_ids, process_ids)
    xref_ids = populate_cross_references(db, mechanism_ids, process_ids, enzyme_ids)
    parameter_ids = populate_parameters(db, mechanism_ids)
    formula_ids = populate_formulas(db)
    formula_links = link_formulas_to_entities(db, mechanism_ids, enzyme_ids, formula_ids)

    # Print statistics
    print("\n" + "=" * 70)
    db.print_statistics()
    print("=" * 70)

    print("\n=== Population Complete ===")
    print(f"Database created: bio_architecture.db")
    print(f"\nNext steps:")
    print(f"  1. Query the database: python -c 'from bio_architecture_db_utils import BioArchDB; db = BioArchDB(); db.print_statistics()'")
    print(f"  2. Search entities: db.search_entities(\"lateral inhibition\")")
    print(f"  3. Get computational mappings: db.get_computational_mappings()")
    print(f"  4. Explore relationships: db.get_relationships(entity_id)")

    db.close()


if __name__ == '__main__':
    main()
