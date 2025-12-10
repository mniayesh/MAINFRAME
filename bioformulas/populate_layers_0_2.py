#!/usr/bin/env python3
"""
Populate bioformulas database with Layer 0-2 mathematical formulations.

This script adds the fundamental equations for:
  - Layer 0: Physical Substrate (Langevin, diffusion, energy landscapes)
  - Layer 1: Capability Graph (graph theory, GNNs)
  - Layer 2: Morphogenesis (reaction-diffusion, Turing patterns, CA)
"""

import sqlite3
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent / 'bioformulas.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_source(conn, name, url, description):
    """Add a data source."""
    cur = conn.execute("""
        INSERT OR IGNORE INTO sources (name, url, description)
        VALUES (?, ?, ?)
    """, (name, url, description))
    conn.commit()
    if cur.rowcount > 0:
        log.info(f"📚 Added source: {name}")
    return conn.execute("SELECT source_id FROM sources WHERE name = ?", (name,)).fetchone()[0]

def add_category(conn, name, parent_id=None, description=None):
    """Add a category."""
    cur = conn.execute("""
        INSERT OR IGNORE INTO categories (name, parent_category_id, description)
        VALUES (?, ?, ?)
    """, (name, parent_id, description))
    conn.commit()
    if cur.rowcount > 0:
        log.info(f"📁 Added category: {name}")
    return conn.execute("SELECT category_id FROM categories WHERE name = ?", (name,)).fetchone()[0]

def add_formula(conn, name, latex, description, formula_type, category_id, source_id,
                mathml=None, symbolic=None, python_code=None,
                domain=None, model_origin=None, doi=None, year=None):
    """Add a formula."""
    cur = conn.execute("""
        INSERT INTO formulas (name, latex, mathml, symbolic, python_code, description,
                              formula_type, domain, model_origin, source_id, category_id,
                              publication_doi, publication_year)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, latex, mathml, symbolic, python_code, description,
          formula_type, domain, model_origin, source_id, category_id,
          doi, year))
    conn.commit()
    formula_id = cur.lastrowid
    log.info(f"➕ [{formula_type}] {name}")
    return formula_id

def populate_layer_0_formulas(conn, source_id, category_id):
    """Add Layer 0: Physical Substrate formulas."""
    log.info("=" * 60)
    log.info("LAYER 0: Physical Substrate")
    log.info("=" * 60)

    # Langevin Equation (overdamped)
    add_formula(
        conn,
        name="Langevin Equation (Overdamped)",
        latex=r"\frac{dx}{dt} = -\frac{1}{\gamma}\nabla U(x) + \sqrt{2D}\eta(t)",
        symbolic="Derivative(x(t), t) = -(1/gamma)*gradient(U(x)) + sqrt(2*D)*eta(t)",
        python_code="""def langevin_step(x, dt, U_grad, gamma, D):
    drift = -(1/gamma) * U_grad(x)
    noise = np.sqrt(2*D*dt) * np.random.randn(*x.shape)
    return x + drift*dt + noise""",
        description="Overdamped Langevin equation describing motion of particles in viscous medium with thermal fluctuations. Used for molecular dynamics, protein folding, Brownian motion.",
        formula_type="SDE",
        domain="statistical_mechanics",
        model_origin="Layer 0: Physical Substrate",
        doi="10.1007/978-3-642-61544-3",
        year=1996,
        category_id=category_id,
        source_id=source_id
    )

    # Langevin Equation (underdamped)
    add_formula(
        conn,
        name="Langevin Equation (Underdamped)",
        latex=r"m\frac{d^2x}{dt^2} = -\gamma\frac{dx}{dt} - \nabla U(x) + \sqrt{2\gamma k_B T}\eta(t)",
        symbolic="m*Derivative(x(t), t, t) = -gamma*Derivative(x(t), t) - gradient(U(x)) + sqrt(2*gamma*kB*T)*eta(t)",
        python_code="""def underdamped_langevin_step(x, v, dt, m, gamma, U_grad, kB, T):
    force = -gamma*v - U_grad(x) + np.sqrt(2*gamma*kB*T/dt)*np.random.randn(*x.shape)
    v_new = v + (force/m)*dt
    x_new = x + v_new*dt
    return x_new, v_new""",
        description="Underdamped Langevin equation with inertial effects. Includes momentum term for systems where mass matters.",
        formula_type="SDE",
        domain="statistical_mechanics",
        model_origin="Layer 0: Physical Substrate",
        category_id=category_id,
        source_id=source_id
    )

    # Fokker-Planck Equation
    add_formula(
        conn,
        name="Fokker-Planck Equation",
        latex=r"\frac{\partial\rho}{\partial t} = \frac{1}{\gamma}\nabla\cdot[\nabla U(x)\rho] + D\nabla^2\rho",
        symbolic="Derivative(rho(x,t), t) = (1/gamma)*divergence(gradient(U)*rho) + D*laplacian(rho)",
        python_code="""def fokker_planck_step(rho, dx, dt, gamma, D, U_grad):
    # Drift term
    drift = divergence(U_grad * rho) / gamma
    # Diffusion term
    diffusion = D * laplacian(rho, dx)
    return rho + (drift + diffusion) * dt""",
        description="Evolution equation for probability density in Langevin dynamics. Gives ensemble behavior from single-particle stochastic equation.",
        formula_type="PDE",
        domain="statistical_mechanics",
        model_origin="Layer 0: Physical Substrate",
        doi="10.1007/978-3-642-61544-3",
        year=1996,
        category_id=category_id,
        source_id=source_id
    )

    # Boltzmann Distribution
    add_formula(
        conn,
        name="Boltzmann Distribution (Equilibrium)",
        latex=r"\rho_{eq}(x) \propto \exp\left(-\frac{U(x)}{k_B T}\right)",
        symbolic="rho_eq(x) = exp(-U(x)/(kB*T)) / Z",
        python_code="""def boltzmann_distribution(x, U, kB, T):
    return np.exp(-U(x) / (kB * T))""",
        description="Equilibrium probability distribution in energy landscape. States with lower energy are exponentially more probable.",
        formula_type="algebraic",
        domain="statistical_mechanics",
        model_origin="Layer 0: Physical Substrate",
        year=1877,
        category_id=category_id,
        source_id=source_id
    )

    # Diffusion Equation (Fick's 2nd Law)
    add_formula(
        conn,
        name="Diffusion Equation (Fick's Second Law)",
        latex=r"\frac{\partial c}{\partial t} = D\nabla^2 c",
        symbolic="Derivative(c(x,t), t) = D*laplacian(c)",
        python_code="""def diffusion_step(c, dx, dt, D):
    laplacian = (np.roll(c,1) - 2*c + np.roll(c,-1)) / dx**2
    return c + D * laplacian * dt""",
        description="Describes spreading of concentration through diffusion. Fundamental equation for molecular transport.",
        formula_type="PDE",
        domain="transport",
        model_origin="Layer 0: Physical Substrate",
        year=1855,
        category_id=category_id,
        source_id=source_id
    )

    # Einstein Relation
    add_formula(
        conn,
        name="Einstein Relation (Mean Squared Displacement)",
        latex=r"\langle x^2(t) \rangle = 2Dt",
        symbolic="mean(x(t)**2) = 2*D*t",
        python_code="""def msd_theory(t, D):
    return 2 * D * t""",
        description="Mean-squared displacement grows linearly with time in free diffusion. Used to extract diffusion coefficient from experiments.",
        formula_type="algebraic",
        domain="transport",
        model_origin="Layer 0: Physical Substrate",
        doi="10.1002/andp.19053220806",
        year=1905,
        category_id=category_id,
        source_id=source_id
    )

    # Kramers Rate (Barrier Crossing)
    add_formula(
        conn,
        name="Kramers Rate (Barrier Crossing)",
        latex=r"k = \frac{\omega_0\omega_b}{2\pi\gamma}\exp\left(-\frac{\Delta U}{k_B T}\right)",
        symbolic="k = (omega_0*omega_b)/(2*pi*gamma) * exp(-Delta_U/(kB*T))",
        python_code="""def kramers_rate(omega_0, omega_b, gamma, Delta_U, kB, T):
    prefactor = (omega_0 * omega_b) / (2 * np.pi * gamma)
    boltzmann = np.exp(-Delta_U / (kB * T))
    return prefactor * boltzmann""",
        description="Rate of escape over energy barrier by thermal activation. Critical for protein folding, chemical reactions, state transitions.",
        formula_type="algebraic",
        domain="kinetics",
        model_origin="Layer 0: Physical Substrate",
        year=1940,
        category_id=category_id,
        source_id=source_id
    )

    # Fluctuation-Dissipation Theorem
    add_formula(
        conn,
        name="Fluctuation-Dissipation Theorem",
        latex=r"\langle x(0) \cdot x(t) \rangle = \frac{k_B T}{\gamma}e^{-\gamma t/m}",
        symbolic="correlation(x(0), x(t)) = (kB*T/gamma) * exp(-gamma*t/m)",
        python_code="""def autocorrelation(t, kB, T, gamma, m):
    return (kB * T / gamma) * np.exp(-gamma * t / m)""",
        description="Relates spontaneous fluctuations to dissipation (friction). Fundamental theorem connecting equilibrium fluctuations to transport coefficients.",
        formula_type="algebraic",
        domain="statistical_mechanics",
        model_origin="Layer 0: Physical Substrate",
        year=1966,
        category_id=category_id,
        source_id=source_id
    )

    log.info(f"✓ Added {8} Layer 0 formulas")

def populate_layer_1_formulas(conn, source_id, category_id):
    """Add Layer 1: Capability Graph formulas."""
    log.info("=" * 60)
    log.info("LAYER 1: Capability Graph")
    log.info("=" * 60)

    # Graph Laplacian
    add_formula(
        conn,
        name="Graph Laplacian",
        latex=r"L = D - A",
        symbolic="L = diag(degree) - adjacency",
        python_code="""def graph_laplacian(adjacency):
    degree = np.diag(np.sum(adjacency, axis=1))
    return degree - adjacency""",
        description="Graph Laplacian matrix governing diffusion on graphs. Eigenvalues encode connectivity structure.",
        formula_type="algebraic",
        domain="graph_theory",
        model_origin="Layer 1: Capability Graph",
        category_id=category_id,
        source_id=source_id
    )

    # Normalized Graph Laplacian
    add_formula(
        conn,
        name="Normalized Graph Laplacian",
        latex=r"\mathcal{L} = I - D^{-1/2}AD^{-1/2}",
        symbolic="L_norm = I - D_inv_sqrt @ A @ D_inv_sqrt",
        python_code="""def normalized_laplacian(adjacency):
    degree = np.sum(adjacency, axis=1)
    D_inv_sqrt = np.diag(1.0 / np.sqrt(degree + 1e-10))
    return np.eye(len(adjacency)) - D_inv_sqrt @ adjacency @ D_inv_sqrt""",
        description="Normalized Laplacian with eigenvalues in [0,2]. Better numerical properties than unnormalized version.",
        formula_type="algebraic",
        domain="graph_theory",
        model_origin="Layer 1: Capability Graph",
        category_id=category_id,
        source_id=source_id
    )

    # Heat Diffusion on Graph
    add_formula(
        conn,
        name="Heat Equation on Graph",
        latex=r"\frac{\partial s}{\partial t} = -Ls",
        symbolic="Derivative(s(t), t) = -L @ s",
        python_code="""def graph_diffusion_step(s, L, dt):
    return s - L @ s * dt""",
        description="Diffusion of signal on graph. Solution: s(t) = exp(-Lt)·s(0). Converges to uniform distribution.",
        formula_type="ODE",
        domain="graph_theory",
        model_origin="Layer 1: Capability Graph",
        category_id=category_id,
        source_id=source_id
    )

    # Graph Convolutional Network Layer
    add_formula(
        conn,
        name="Graph Convolutional Network (GCN) Layer",
        latex=r"H^{(l+1)} = \sigma(\tilde{D}^{-1/2}\tilde{A}\tilde{D}^{-1/2}H^{(l)}W^{(l)})",
        symbolic="H_next = activation(norm_adj @ H @ W)",
        python_code="""def gcn_layer(H, adjacency, W, activation=np.tanh):
    # Add self-loops
    A_hat = adjacency + np.eye(len(adjacency))
    # Normalize
    D_hat = np.diag(np.sum(A_hat, axis=1))
    D_inv_sqrt = np.diag(1.0 / np.sqrt(np.diag(D_hat)))
    norm_adj = D_inv_sqrt @ A_hat @ D_inv_sqrt
    # Propagate
    return activation(norm_adj @ H @ W)""",
        description="Graph convolutional layer for learning on graph-structured data. Aggregates neighbor features with learned weights.",
        formula_type="algebraic",
        domain="machine_learning",
        model_origin="Layer 1: Capability Graph",
        doi="10.48550/arXiv.1609.02907",
        year=2017,
        category_id=category_id,
        source_id=source_id
    )

    # Message Passing Neural Network
    add_formula(
        conn,
        name="Message Passing Neural Network (MPNN)",
        latex=r"m_v^{(t)} = \sum_{u \in \mathcal{N}(v)} M_t(h_v^{(t-1)}, h_u^{(t-1)}, e_{uv})",
        symbolic="message_v = sum(message_fn(h_v, h_u, edge_uv) for u in neighbors(v))",
        python_code="""def message_passing_step(node_states, adjacency, message_fn, update_fn):
    messages = np.zeros_like(node_states)
    for i in range(len(node_states)):
        for j in range(len(node_states)):
            if adjacency[j, i] > 0:
                messages[i] += message_fn(node_states[i], node_states[j], adjacency[j,i])
    return update_fn(node_states, messages)""",
        description="General framework for graph neural networks. Nodes aggregate messages from neighbors and update states.",
        formula_type="algebraic",
        domain="machine_learning",
        model_origin="Layer 1: Capability Graph",
        year=2017,
        category_id=category_id,
        source_id=source_id
    )

    # Clustering Coefficient
    add_formula(
        conn,
        name="Clustering Coefficient",
        latex=r"C = \frac{3 \times \text{number of triangles}}{\text{number of connected triples}}",
        symbolic="C = 3 * n_triangles / n_triples",
        python_code="""def clustering_coefficient(adjacency):
    import networkx as nx
    G = nx.from_numpy_array(adjacency)
    return nx.average_clustering(G)""",
        description="Measures local clustering in networks. High C indicates community structure.",
        formula_type="algebraic",
        domain="graph_theory",
        model_origin="Layer 1: Capability Graph",
        category_id=category_id,
        source_id=source_id
    )

    log.info(f"✓ Added {6} Layer 1 formulas")

def populate_layer_2_formulas(conn, source_id, category_id):
    """Add Layer 2: Morphogenesis formulas."""
    log.info("=" * 60)
    log.info("LAYER 2: Morphogenesis")
    log.info("=" * 60)

    # Turing Reaction-Diffusion (General)
    add_formula(
        conn,
        name="Turing Reaction-Diffusion System",
        latex=r"\frac{\partial u}{\partial t} = D_u\nabla^2 u + f(u,v), \quad \frac{\partial v}{\partial t} = D_v\nabla^2 v + g(u,v)",
        symbolic="Derivative(u,t) = D_u*laplacian(u) + f(u,v); Derivative(v,t) = D_v*laplacian(v) + g(u,v)",
        python_code="""def reaction_diffusion_step(u, v, dx, dt, D_u, D_v, f, g):
    lap_u = laplacian(u, dx)
    lap_v = laplacian(v, dx)
    u_new = u + (D_u*lap_u + f(u,v)) * dt
    v_new = v + (D_v*lap_v + g(u,v)) * dt
    return u_new, v_new""",
        description="General form of Turing reaction-diffusion system. Local reaction + differential diffusion → spatial patterns.",
        formula_type="PDE",
        domain="morphogenesis",
        model_origin="Layer 2: Morphogenesis",
        doi="10.1098/rstb.1952.0012",
        year=1952,
        category_id=category_id,
        source_id=source_id
    )

    # Gray-Scott Model
    add_formula(
        conn,
        name="Gray-Scott Model",
        latex=r"\frac{\partial u}{\partial t} = D_u\nabla^2 u - uv^2 + F(1-u), \quad \frac{\partial v}{\partial t} = D_v\nabla^2 v + uv^2 - (F+k)v",
        symbolic="Derivative(u,t) = D_u*laplacian(u) - u*v**2 + F*(1-u); Derivative(v,t) = D_v*laplacian(v) + u*v**2 - (F+k)*v",
        python_code="""def gray_scott_step(u, v, dx, dt, D_u=0.16, D_v=0.08, F=0.060, k=0.062):
    lap_u = laplacian(u, dx)
    lap_v = laplacian(v, dx)
    uvv = u * v * v
    du = D_u*lap_u - uvv + F*(1-u)
    dv = D_v*lap_v + uvv - (F+k)*v
    return u + du*dt, v + dv*dt""",
        description="Autocatalytic reaction-diffusion producing spots, stripes, spirals. Parameters F,k control pattern type.",
        formula_type="PDE",
        domain="morphogenesis",
        model_origin="Layer 2: Morphogenesis",
        doi="10.1126/science.261.5118.189",
        year=1993,
        category_id=category_id,
        source_id=source_id
    )

    # Gierer-Meinhardt Model
    add_formula(
        conn,
        name="Gierer-Meinhardt (Activator-Inhibitor)",
        latex=r"\frac{\partial a}{\partial t} = c_a\left(\frac{a^2}{h} - \mu_a a + \rho_a\right) + D_a\nabla^2 a",
        symbolic="Derivative(a,t) = c_a*(a**2/h - mu_a*a + rho_a) + D_a*laplacian(a)",
        python_code="""def gierer_meinhardt_step(a, h, dx, dt, D_a=0.01, D_h=1.0, c_a=0.01, mu_a=0.01):
    lap_a = laplacian(a, dx)
    lap_h = laplacian(h, dx)
    da = c_a*(a**2/(h+1e-10) - mu_a*a + rho_a) + D_a*lap_a
    dh = c_h*(a**2 - mu_h*h + rho_h) + D_h*lap_h
    return a + da*dt, h + dh*dt""",
        description="Activator-inhibitor model: short-range activation, long-range inhibition. Produces periodic patterns, segments.",
        formula_type="PDE",
        domain="morphogenesis",
        model_origin="Layer 2: Morphogenesis",
        year=1972,
        category_id=category_id,
        source_id=source_id
    )

    # Morphogen Gradient (Exponential)
    add_formula(
        conn,
        name="Morphogen Gradient (Steady State)",
        latex=r"c(x) = c_0 e^{-x/\lambda}, \quad \lambda = \sqrt{D/k}",
        symbolic="c(x) = c_0 * exp(-x/lambda); lambda = sqrt(D/k)",
        python_code="""def morphogen_gradient(x, c_0, D, k):
    lambda_decay = np.sqrt(D / k)
    return c_0 * np.exp(-x / lambda_decay)""",
        description="Exponential morphogen gradient from source. Length scale λ = √(D/k) sets spatial extent. Basis of positional information.",
        formula_type="algebraic",
        domain="morphogenesis",
        model_origin="Layer 2: Morphogenesis",
        doi="10.1016/0022-5193(69)90079-9",
        year=1969,
        category_id=category_id,
        source_id=source_id
    )

    # Morphogen Diffusion-Degradation
    add_formula(
        conn,
        name="Morphogen Diffusion-Degradation Equation",
        latex=r"\frac{\partial c}{\partial t} = D\nabla^2 c - kc + S(x)",
        symbolic="Derivative(c,t) = D*laplacian(c) - k*c + source(x)",
        python_code="""def morphogen_evolution_step(c, dx, dt, D, k, source):
    lap_c = laplacian(c, dx)
    dc = D*lap_c - k*c + source
    return c + dc*dt""",
        description="Time evolution of morphogen with production, diffusion, and degradation. Steady state gives exponential gradient.",
        formula_type="PDE",
        domain="morphogenesis",
        model_origin="Layer 2: Morphogenesis",
        category_id=category_id,
        source_id=source_id
    )

    # Cellular Automaton (Game of Life)
    add_formula(
        conn,
        name="Conway's Game of Life Rule",
        latex=r"s_{i,j}^{t+1} = \begin{cases} 1 & \text{if } N=3 \text{ or } (s_{i,j}^t=1 \text{ and } N \in \{2,3\}) \\ 0 & \text{otherwise} \end{cases}",
        symbolic="s_next = 1 if (N==3 or (s==1 and N in [2,3])) else 0",
        python_code="""def game_of_life_rule(state, neighbors):
    if state == 1:
        return 1 if neighbors in [2, 3] else 0
    else:
        return 1 if neighbors == 3 else 0""",
        description="Cellular automaton rule producing complex emergent behavior from simple local rules. B3/S23 notation.",
        formula_type="discrete",
        domain="cellular_automata",
        model_origin="Layer 2: Morphogenesis",
        year=1970,
        category_id=category_id,
        source_id=source_id
    )

    # Elementary CA Rule
    add_formula(
        conn,
        name="Elementary Cellular Automaton (1D)",
        latex=r"s_i^{t+1} = f(s_{i-1}^t, s_i^t, s_{i+1}^t)",
        symbolic="s_next[i] = rule_lookup[(s[i-1], s[i], s[i+1])]",
        python_code="""def elementary_ca_step(state, rule_number):
    rule = {k: int(b) for k, b in zip(['111','110','101','100','011','010','001','000'],
                                       format(rule_number, '08b'))}
    new_state = np.zeros_like(state)
    for i in range(len(state)):
        config = f'{state[i-1]}{state[i]}{state[(i+1)%len(state)]}'
        new_state[i] = rule[config]
    return new_state""",
        description="1D cellular automaton with 256 possible rules (Wolfram classification). Rule 110 is Turing-complete.",
        formula_type="discrete",
        domain="cellular_automata",
        model_origin="Layer 2: Morphogenesis",
        year=2002,
        category_id=category_id,
        source_id=source_id
    )

    log.info(f"✓ Added {7} Layer 2 formulas")

def main():
    """Populate database with Layer 0-2 formulas."""
    conn = get_connection()

    log.info("=" * 60)
    log.info("BioAI Layers 0-2 Formula Database Population")
    log.info("=" * 60)

    # Add source
    source_id = add_source(
        conn,
        name="BioAI Layers 0-2 Reference",
        url="file:///home/user/MAINFRAME/BIOAI_LAYERS_0_2_MATHEMATICAL_REFERENCE.md",
        description="Mathematical formulations for biological computing layers 0-2: Physical substrate, capability graphs, and morphogenesis"
    )

    # Add categories
    layer0_cat = add_category(
        conn,
        name="Layer 0: Physical Substrate",
        description="Energy landscapes, stochastic dynamics, thermal noise, Langevin equations"
    )

    layer1_cat = add_category(
        conn,
        name="Layer 1: Capability Graph",
        description="Graph representations, spectral methods, graph neural networks, topology metrics"
    )

    layer2_cat = add_category(
        conn,
        name="Layer 2: Morphogenesis",
        description="Reaction-diffusion, Turing patterns, morphogen gradients, cellular automata"
    )

    # Populate formulas
    populate_layer_0_formulas(conn, source_id, layer0_cat)
    populate_layer_1_formulas(conn, source_id, layer1_cat)
    populate_layer_2_formulas(conn, source_id, layer2_cat)

    # Update formula counts
    conn.execute("""
        UPDATE sources
        SET formula_count = (
            SELECT COUNT(*)
            FROM formulas
            WHERE formulas.source_id = sources.source_id
        )
    """)
    conn.commit()

    log.info("=" * 60)
    log.info("✓ Database population complete!")
    log.info("=" * 60)

    # Summary statistics
    stats = conn.execute("""
        SELECT
            c.name as category,
            COUNT(f.formula_id) as formula_count
        FROM categories c
        LEFT JOIN formulas f ON c.category_id = f.category_id
        WHERE c.name LIKE 'Layer %'
        GROUP BY c.category_id
        ORDER BY c.name
    """).fetchall()

    log.info("\nSummary:")
    for row in stats:
        log.info(f"  {row['category']}: {row['formula_count']} formulas")

    total = conn.execute("SELECT COUNT(*) as total FROM formulas").fetchone()['total']
    log.info(f"\nTotal formulas in database: {total}")

    conn.close()

if __name__ == '__main__':
    main()
