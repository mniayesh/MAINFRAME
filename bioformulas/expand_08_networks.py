#!/usr/bin/env python3
"""Expansion module 8: Network dynamics and population models."""

from expand_base import *

def run():
    conn = get_conn()
    start = count_formulas(conn)
    log.info("="*50)
    log.info("EXPANDING: NETWORK DYNAMICS")
    log.info("="*50)

    src = get_source_id(conn, 'ModelDB')
    lit = get_source_id(conn, 'Scientific Literature')

    net = add_category(conn, 'Neural Networks', 'Neuroscience')
    pop = add_category(conn, 'Population Models', 'Neural Networks')
    osc = add_category(conn, 'Oscillations', 'Neural Networks')
    attractor = add_category(conn, 'Attractor Networks', 'Neural Networks')
    learn = add_category(conn, 'Learning Rules', 'Neural Networks')

    # === POPULATION RATE MODELS ===
    log.info("--- Population Rate Models ---")

    add_formula(conn, "Wilson-Cowan (full)",
        r"\tau_E \frac{dE}{dt} = -E + (1-r_E E) S_E(w_{EE}E - w_{EI}I + I_E)",
        "Excitatory population with refractory term",
        "ODE", pop, lit,
        domain="rate-models", model_origin="wilson-cowan-full")

    add_formula(conn, "Sigmoid Transfer Function",
        r"S(x) = \frac{F_{max}}{1 + \exp(-\beta(x - \theta))}",
        "Population firing rate function",
        "algebraic", pop, lit,
        domain="rate-models", model_origin="sigmoid-transfer")

    add_formula(conn, "Threshold-Linear",
        r"S(x) = [x - \theta]_+ = \max(0, x - \theta)",
        "Rectified linear activation",
        "algebraic", pop, lit,
        domain="rate-models", model_origin="threshold-linear")

    add_formula(conn, "Rate Model with Adaptation",
        r"\tau_r \frac{dr}{dt} = -r + S(I - a), \quad \tau_a \frac{da}{dt} = -a + \beta r",
        "Firing rate with spike-frequency adaptation",
        "ODE", pop, lit,
        domain="rate-models", model_origin="rate-adaptation")

    # === MEAN-FIELD THEORY ===
    log.info("--- Mean-Field Models ---")

    add_formula(conn, "Fokker-Planck (LIF)",
        r"\tau_m \frac{\partial p}{\partial t} = \frac{\partial}{\partial V}[(V - \mu)p] + \frac{\sigma^2}{2}\frac{\partial^2 p}{\partial V^2}",
        "Probability density for membrane potential",
        "PDE", pop, lit,
        domain="mean-field", model_origin="fokker-planck")

    add_formula(conn, "Mean-Field Firing Rate (Siegert)",
        r"\nu = \left(\tau_{ref} + \tau_m \sqrt{\pi} \int_{\frac{V_r - \mu}{\sigma}}^{\frac{V_{th} - \mu}{\sigma}} e^{x^2}(1 + \text{erf}(x)) dx\right)^{-1}",
        "Steady-state firing rate for LIF with noise",
        "algebraic", pop, lit,
        domain="mean-field", model_origin="siegert")

    add_formula(conn, "Self-Consistent Mean-Field",
        r"\nu = \Phi(\mu(\nu), \sigma(\nu))",
        "Self-consistency equation for network rate",
        "algebraic", pop, lit,
        domain="mean-field", model_origin="self-consistent")

    add_formula(conn, "Mean Synaptic Input",
        r"\mu = \tau_m (J_{ext} \nu_{ext} + J \nu)",
        "Mean input from external and recurrent",
        "algebraic", pop, lit,
        domain="mean-field", model_origin="mean-input")

    add_formula(conn, "Input Variance",
        r"\sigma^2 = \tau_m (J_{ext}^2 \nu_{ext} + J^2 \nu)",
        "Variance of synaptic input",
        "algebraic", pop, lit,
        domain="mean-field", model_origin="input-variance")

    # === BALANCED NETWORKS ===
    log.info("--- Balanced Networks ---")

    add_formula(conn, "E-I Balance Condition",
        r"J_E \nu_E = J_I \nu_I + I_{ext}",
        "Balance of excitation and inhibition",
        "algebraic", pop, lit,
        domain="balanced", model_origin="EI-balance")

    add_formula(conn, "Asynchronous Irregular State",
        r"CV_{ISI} \approx 1, \quad C_{ij} \approx 0",
        "Irregular firing with low correlations",
        "algebraic", pop, lit,
        domain="balanced", model_origin="AI-state")

    add_formula(conn, "Brunel Network Phases",
        r"\nu = \Phi\left(\frac{J_E C_E \nu_E + J_I C_I \nu_I + I_{ext}}{\sigma}\right)",
        "Phase diagram of balanced random network",
        "algebraic", pop, src,
        domain="balanced", model_origin="brunel",
        doi="10.1023/A:1008925309027", year=2000)

    # === OSCILLATIONS & RHYTHMS ===
    log.info("--- Oscillations ---")

    add_formula(conn, "PING (Pyramidal-Interneuron Gamma)",
        r"\tau_E \frac{dE}{dt} = -E + S(w_{EE}E - w_{EI}I), \quad \tau_I \frac{dI}{dt} = -I + S(w_{IE}E)",
        "Gamma oscillation from E-I loop",
        "ODE", osc, lit,
        domain="oscillations", model_origin="PING")

    add_formula(conn, "ING (Interneuron Gamma)",
        r"\tau_I \frac{dI}{dt} = -I + S(w_{II}I + I_{ext})",
        "Gamma from mutual I-I inhibition",
        "ODE", osc, lit,
        domain="oscillations", model_origin="ING")

    add_formula(conn, "Theta Oscillation",
        r"\tau_{slow} \frac{dh}{dt} = h_\infty([Ca]) - h",
        "Slow h-current for theta rhythm",
        "ODE", osc, src,
        domain="oscillations", model_origin="theta-rhythm")

    add_formula(conn, "Coupled Oscillators (Kuramoto)",
        r"\frac{d\theta_i}{dt} = \omega_i + \frac{K}{N} \sum_{j=1}^N \sin(\theta_j - \theta_i)",
        "Phase oscillators with global coupling",
        "ODE", osc, lit,
        domain="oscillations", model_origin="kuramoto")

    add_formula(conn, "Order Parameter",
        r"r e^{i\psi} = \frac{1}{N} \sum_{j=1}^N e^{i\theta_j}",
        "Synchronization measure",
        "algebraic", osc, lit,
        domain="oscillations", model_origin="order-param")

    add_formula(conn, "Phase Response Curve",
        r"\Delta\phi = Z(\phi) \cdot \epsilon",
        "Phase shift from perturbation",
        "algebraic", osc, lit,
        domain="oscillations", model_origin="PRC")

    add_formula(conn, "Cross-Frequency Coupling",
        r"MI = \sum_j p_j \log\frac{p_j}{q_j}",
        "Modulation index for phase-amplitude coupling",
        "algebraic", osc, lit,
        domain="oscillations", model_origin="CFC")

    # === ATTRACTOR NETWORKS ===
    log.info("--- Attractor Networks ---")

    add_formula(conn, "Hopfield Energy",
        r"E = -\frac{1}{2} \sum_{i,j} w_{ij} s_i s_j + \sum_i \theta_i s_i",
        "Energy function for associative memory",
        "algebraic", attractor, lit,
        domain="attractor", model_origin="hopfield-energy")

    add_formula(conn, "Hopfield Update",
        r"s_i(t+1) = \text{sign}\left(\sum_j w_{ij} s_j - \theta_i\right)",
        "Asynchronous binary update rule",
        "discrete", attractor, lit,
        domain="attractor", model_origin="hopfield-update")

    add_formula(conn, "Hebbian Weight Storage",
        r"w_{ij} = \frac{1}{P} \sum_{\mu=1}^P \xi_i^\mu \xi_j^\mu",
        "Store P patterns with outer products",
        "algebraic", attractor, lit,
        domain="attractor", model_origin="hebb-storage")

    add_formula(conn, "Continuous Hopfield",
        r"\tau \frac{dV_i}{dt} = -V_i + \sum_j w_{ij} g(V_j) + I_i",
        "Continuous-time analog network",
        "ODE", attractor, lit,
        domain="attractor", model_origin="hopfield-continuous")

    add_formula(conn, "Ring Attractor (Head Direction)",
        r"\tau \frac{dm_i}{dt} = -m_i + \phi\left(\sum_j w_{ij} m_j + I_i\right)",
        "Continuous attractor for head direction",
        "ODE", attractor, src,
        domain="attractor", model_origin="ring-attractor")

    add_formula(conn, "Bump Attractor",
        r"w_{ij} = J_0 + J_1 \cos(\theta_i - \theta_j)",
        "Cosine connectivity for bump",
        "algebraic", attractor, lit,
        domain="attractor", model_origin="bump-weights")

    add_formula(conn, "Line Attractor (Integration)",
        r"\frac{dm}{dt} = I(t), \quad \text{(neutral stability)}",
        "Perfect integrator without decay",
        "ODE", attractor, lit,
        domain="attractor", model_origin="line-attractor")

    # === WORKING MEMORY ===
    log.info("--- Working Memory ---")

    add_formula(conn, "Persistent Activity (Bistable)",
        r"\tau \frac{dr}{dt} = -r + f(Jr + I_{ext})",
        "Bistable attractor for persistent firing",
        "ODE", attractor, src,
        domain="working-memory", model_origin="bistable")

    add_formula(conn, "NMDA-based Persistence",
        r"\tau_{NMDA} \frac{ds}{dt} = -s + \alpha (1-s) r",
        "Slow NMDA maintains activity",
        "ODE", attractor, src,
        domain="working-memory", model_origin="NMDA-persistence")

    # === LEARNING RULES ===
    log.info("--- Network Learning Rules ---")

    add_formula(conn, "Covariance Learning",
        r"\Delta w_{ij} = \eta (x_i - \bar{x}_i)(y_j - \bar{y}_j)",
        "Covariance rule with mean subtraction",
        "plasticity_rule", learn, lit,
        domain="learning", model_origin="covariance")

    add_formula(conn, "BCM Network",
        r"\frac{dw_{ij}}{dt} = \eta x_i y_j (y_j - \theta_j)",
        "BCM rule with sliding threshold",
        "ODE", learn, lit,
        domain="learning", model_origin="BCM-network")

    add_formula(conn, "Infomax/ICA",
        r"\Delta W = \eta (I + (1 - 2y)u^T) W",
        "Information maximization for ICA",
        "plasticity_rule", learn, lit,
        domain="learning", model_origin="infomax")

    add_formula(conn, "Sparse Coding",
        r"\min_a ||x - \Phi a||^2 + \lambda ||a||_1",
        "L1 regularized reconstruction",
        "algebraic", learn, lit,
        domain="learning", model_origin="sparse-coding")

    add_formula(conn, "Predictive Coding Error",
        r"\epsilon = x - \hat{x} = x - Wr",
        "Prediction error for hierarchical coding",
        "algebraic", learn, lit,
        domain="learning", model_origin="pred-coding")

    add_formula(conn, "Contrastive Learning",
        r"\Delta w_{ij} = \eta (\langle s_i s_j \rangle_{data} - \langle s_i s_j \rangle_{model})",
        "Contrastive divergence update",
        "plasticity_rule", learn, lit,
        domain="learning", model_origin="contrastive")

    # === DECISION MAKING ===
    log.info("--- Decision Making ---")

    add_formula(conn, "Drift-Diffusion Model",
        r"dx = \mu dt + \sigma dW",
        "Evidence accumulation with noise",
        "SDE", net, lit,
        domain="decision", model_origin="drift-diffusion")

    add_formula(conn, "Urgency-Gating",
        r"dx = (\mu + u(t)) dt + \sigma dW",
        "Time-dependent urgency signal",
        "SDE", net, lit,
        domain="decision", model_origin="urgency")

    add_formula(conn, "Race Model",
        r"dx_i = \mu_i dt + \sigma dW_i, \quad \text{first to threshold wins}",
        "Independent accumulators race",
        "SDE", net, lit,
        domain="decision", model_origin="race")

    add_formula(conn, "Mutual Inhibition Decision",
        r"\tau \frac{dr_i}{dt} = -r_i + f(I_i - w \sum_{j \neq i} r_j)",
        "Winner-take-all with lateral inhibition",
        "ODE", net, src,
        domain="decision", model_origin="WTA")

    # === NORMALIZATION ===
    log.info("--- Normalization ---")

    add_formula(conn, "Divisive Normalization",
        r"R_i = \frac{L_i^n}{\sigma^n + \sum_j L_j^n}",
        "Response normalized by pool activity",
        "algebraic", net, lit,
        domain="normalization", model_origin="divisive-norm")

    add_formula(conn, "Gain Modulation",
        r"R = f(x) \cdot g(y)",
        "Multiplicative gain control",
        "algebraic", net, lit,
        domain="normalization", model_origin="gain-mod")

    add_formula(conn, "Subtractive Normalization",
        r"R_i = L_i - \frac{1}{N}\sum_j L_j",
        "Mean subtraction",
        "algebraic", net, lit,
        domain="normalization", model_origin="subtractive")

    print_summary(conn, "NETWORK DYNAMICS", start)
    conn.close()

if __name__ == "__main__":
    run()
