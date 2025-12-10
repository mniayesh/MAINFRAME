#!/usr/bin/env python3
"""Expansion module 5: Extended neuron models."""

from expand_base import *

def run():
    conn = get_conn()
    start = count_formulas(conn)
    log.info("="*50)
    log.info("EXPANDING: NEURON MODELS")
    log.info("="*50)

    src = get_source_id(conn, 'ModelDB')
    lit = get_source_id(conn, 'Scientific Literature')
    nml = get_source_id(conn, 'NeuroML')

    cat = add_category(conn, 'Neuron Models', 'Neuroscience')
    point = add_category(conn, 'Point Neurons', 'Neuron Models', 'Single compartment')
    multi = add_category(conn, 'Multi-compartment', 'Neuron Models', 'Morphological')
    specific = add_category(conn, 'Cell-type Specific', 'Neuron Models', 'Specific neuron types')

    # === POINT NEURON MODELS ===
    log.info("--- Point Neuron Models ---")

    # Quadratic IF
    fid = add_formula(conn, "Quadratic Integrate-and-Fire (QIF)",
        r"\tau \frac{dV}{dt} = (V - V_{rest})(V - V_{th}) + RI",
        "Canonical Type I neuron model",
        "ODE", point, lit,
        python_code="dV_dt = ((V - V_rest) * (V - V_th) + R * I) / tau",
        domain="computational-neuroscience", model_origin="QIF")
    add_neuron(conn, fid, "QIF", 1, -50, -65)

    # Theta neuron
    fid = add_formula(conn, "Theta Neuron",
        r"\frac{d\theta}{dt} = (1 - \cos\theta) + (1 + \cos\theta)(\eta + I)",
        "Phase representation of QIF on circle",
        "ODE", point, lit,
        domain="computational-neuroscience", model_origin="theta")
    add_neuron(conn, fid, "Theta", 1)

    # Resonate-and-Fire
    fid = add_formula(conn, "Resonate-and-Fire",
        r"\frac{dV}{dt} = bV - \omega W + I, \quad \frac{dW}{dt} = \omega V + bW",
        "Subthreshold oscillations with spike threshold",
        "ODE", point, lit,
        domain="computational-neuroscience", model_origin="resonate-fire")
    add_neuron(conn, fid, "Resonate-and-Fire", 1)

    # GIF (Generalized IF)
    fid = add_formula(conn, "Generalized Integrate-and-Fire (GIF)",
        r"C\frac{dV}{dt} = -g_L(V - E_L) + I - \sum_j \eta_j(t-t_j)",
        "LIF with spike-triggered adaptation currents",
        "ODE", point, src,
        domain="computational-neuroscience", model_origin="GIF")
    add_neuron(conn, fid, "GIF", 1, -50, -70, 1.0, 10)

    # SRM (Spike Response Model)
    fid = add_formula(conn, "Spike Response Model (SRM)",
        r"V(t) = \eta(t - \hat{t}) + \int_0^\infty \kappa(s) I(t-s) ds",
        "Kernel-based spike response model",
        "integral", point, lit,
        domain="computational-neuroscience", model_origin="SRM")
    add_neuron(conn, fid, "SRM", 1)

    # GLIF (Allen Institute)
    fid = add_formula(conn, "GLIF Model (Allen Institute)",
        r"C\frac{dV}{dt} = -g_L(V - E_L) + I - I_{AHP} - I_{ASC}",
        "Generalized LIF with after-spike currents",
        "ODE", point, src,
        domain="computational-neuroscience", model_origin="GLIF")
    add_neuron(conn, fid, "GLIF", 1, -50, -70, 1.0, 10)

    # MAT (Multi-timescale Adaptive Threshold)
    fid = add_formula(conn, "MAT Model",
        r"\frac{d\theta}{dt} = -\frac{\theta - \theta_0}{\tau_\theta} + \alpha \delta(t - t_{spike})",
        "Adaptive threshold model",
        "ODE", point, lit,
        domain="computational-neuroscience", model_origin="MAT")
    add_neuron(conn, fid, "MAT", 1)

    # === CONDUCTANCE-BASED MODELS ===
    log.info("--- Conductance-Based Models ---")

    # Traub-Miles
    fid = add_formula(conn, "Traub-Miles Pyramidal Cell",
        r"C\frac{dV}{dt} = -I_{Na} - I_{K} - I_{Ca} - I_{KCa} - I_{KM} - I_L + I_{syn}",
        "Detailed pyramidal neuron with multiple K+ and Ca2+ currents",
        "ODE", multi, src,
        domain="detailed-models", model_origin="traub-miles")
    add_neuron(conn, fid, "Traub-Miles", 1, -55, -70, 1.0)

    # Wang-Buzsaki Interneuron
    fid = add_formula(conn, "Wang-Buzsaki Fast-Spiking Interneuron",
        r"C\frac{dV}{dt} = -g_{Na}m_\infty^3 h(V-E_{Na}) - g_K n^4(V-E_K) - g_L(V-E_L) + I",
        "Fast-spiking interneuron model with instantaneous Na activation",
        "ODE", specific, src,
        domain="interneuron", model_origin="wang-buzsaki",
        doi="10.1523/JNEUROSCI.16-20-06402.1996", year=1996)
    add_neuron(conn, fid, "Wang-Buzsaki FS", 1, -55, -65)

    # Pospischil et al models
    cell_types = [
        ("Regular Spiking (RS)", "cortical pyramidal", "I_Na,I_Kd,I_M,I_L"),
        ("Fast Spiking (FS)", "cortical interneuron", "I_Na,I_Kd,I_L"),
        ("Intrinsically Bursting (IB)", "layer 5 pyramidal", "I_Na,I_Kd,I_M,I_L,I_Ca,I_KCa"),
        ("Low-Threshold Spiking (LTS)", "somatostatin interneuron", "I_Na,I_Kd,I_M,I_T,I_L"),
        ("Thalamocortical (TC)", "thalamic relay", "I_Na,I_Kd,I_T,I_h,I_L"),
        ("Reticular (RE)", "thalamic reticular", "I_Na,I_Kd,I_T,I_L"),
    ]

    for name, cell_type, currents in cell_types:
        fid = add_formula(conn, f"Pospischil {name}",
            rf"C\frac{{dV}}{{dt}} = -{currents.replace(',', ' - ')} + I_{{syn}}",
            f"{name} neuron model ({cell_type})",
            "ODE", specific, src,
            domain="detailed-models", model_origin=f"pospischil-{name}")
        add_neuron(conn, fid, f"Pospischil-{name}", 1, -55, -70)

    # Destexhe thalamic
    fid = add_formula(conn, "Destexhe Thalamocortical",
        r"C\frac{dV}{dt} = -I_{Na} - I_{K} - I_T - I_h - I_{Kir} - I_L + I_{syn}",
        "Detailed thalamocortical neuron with T-type Ca and h-current",
        "ODE", specific, src,
        domain="thalamic", model_origin="destexhe-TC")
    add_neuron(conn, fid, "Destexhe TC", 1, -55, -70)

    # === MULTI-COMPARTMENT MODELS ===
    log.info("--- Multi-Compartment Models ---")

    # Cable equation
    add_formula(conn, "Cable Equation (Passive)",
        r"\lambda^2 \frac{\partial^2 V}{\partial x^2} - \tau_m \frac{\partial V}{\partial t} = V - V_{rest}",
        "Passive voltage spread in dendrites",
        "PDE", multi, lit,
        domain="cable-theory", model_origin="cable-passive")

    # Active cable
    add_formula(conn, "Cable Equation (Active)",
        r"\frac{c_m}{2a} \frac{\partial V}{\partial t} = \frac{1}{2 r_i a} \frac{\partial^2 V}{\partial x^2} - g_m(V - E_L) - \sum_i g_i(V - E_i)",
        "Active dendritic cable with ion channels",
        "PDE", multi, lit,
        domain="cable-theory", model_origin="cable-active")

    # Compartmental coupling
    add_formula(conn, "Compartmental Coupling",
        r"C_j \frac{dV_j}{dt} = \sum_k g_{jk}(V_k - V_j) + I_{channels,j} + I_{syn,j}",
        "Coupled compartments with axial resistance",
        "ODE", multi, lit,
        domain="compartmental", model_origin="compartmental")

    # Rall's equivalent cylinder
    add_formula(conn, "Rall Equivalent Cylinder",
        r"d^{3/2}_{parent} = \sum_k d^{3/2}_{daughter,k}",
        "Rall's 3/2 power law for equivalent cylinders",
        "algebraic", multi, lit,
        domain="cable-theory", model_origin="rall-3-2")

    # Dendritic spike
    add_formula(conn, "Dendritic NMDA Spike",
        r"I_{NMDA-spike} = g_{NMDA} s(V) \sum_i w_i (V - E_{NMDA})",
        "NMDA-mediated dendritic plateau potential",
        "algebraic", multi, src,
        domain="dendritic", model_origin="NMDA-spike")

    # Calcium spike
    add_formula(conn, "Dendritic Calcium Spike",
        r"I_{Ca-spike} = g_{Ca} m_\infty^2(V)(V - E_{Ca})",
        "Dendritic calcium spike in distal dendrites",
        "current_equation", multi, src,
        domain="dendritic", model_origin="Ca-spike")

    # === SPECIFIC NEURON TYPES ===
    log.info("--- Specific Cell Types ---")

    # Purkinje cell
    fid = add_formula(conn, "Purkinje Cell (De Schutter-Bower)",
        r"C\frac{dV}{dt} = -I_{Na} - I_{NaP} - I_{CaP} - I_{CaT} - 3\times I_K - I_{KCa} - I_{Kh} - I_L",
        "Detailed cerebellar Purkinje cell model",
        "ODE", specific, src,
        domain="cerebellum", model_origin="purkinje-DS")
    add_neuron(conn, fid, "Purkinje-DeSchutter", 1, -55, -68)

    # Granule cell
    fid = add_formula(conn, "Cerebellar Granule Cell",
        r"C\frac{dV}{dt} = -I_{Na} - I_{K} - I_{KA} - I_{KIR} - I_{KCa} - I_{Ca} - I_L + I_{syn}",
        "Small cerebellar granule cell",
        "ODE", specific, src,
        domain="cerebellum", model_origin="granule")
    add_neuron(conn, fid, "Granule", 1, -55, -80)

    # Golgi cell
    fid = add_formula(conn, "Cerebellar Golgi Cell",
        r"C\frac{dV}{dt} = -I_{Na} - I_{NaP} - I_{Kv} - I_{KA} - I_{KM} - I_{KAH} - I_{Ca} - I_h - I_L",
        "Cerebellar Golgi interneuron",
        "ODE", specific, src,
        domain="cerebellum", model_origin="golgi")
    add_neuron(conn, fid, "Golgi", 1, -55, -60)

    # Stellate cell
    fid = add_formula(conn, "Cerebellar Stellate Cell",
        r"C\frac{dV}{dt} = -I_{Na} - I_K - I_{KA} - I_L + I_{syn}",
        "Cerebellar molecular layer interneuron",
        "ODE", specific, src,
        domain="cerebellum", model_origin="stellate")
    add_neuron(conn, fid, "Stellate", 1, -55, -70)

    # Dopamine neuron
    fid = add_formula(conn, "Dopamine Neuron (SNc)",
        r"C\frac{dV}{dt} = -I_{Na} - I_K - I_{Ca-L} - I_{SK} - I_h - I_L + I_{syn}",
        "Substantia nigra pars compacta DA neuron",
        "ODE", specific, src,
        domain="dopamine", model_origin="DA-SNc")
    add_neuron(conn, fid, "DA-SNc", 1, -55, -60)

    # Medium spiny neuron
    fid = add_formula(conn, "Medium Spiny Neuron (MSN)",
        r"C\frac{dV}{dt} = -I_{Na} - I_{Kdr} - I_{KA} - I_{Kir} - I_{KRP} - I_{Ca-N} - I_{Ca-Q} - I_L",
        "Striatal medium spiny neuron",
        "ODE", specific, src,
        domain="basal-ganglia", model_origin="MSN")
    add_neuron(conn, fid, "MSN", 1, -80, -85)

    # Hippocampal CA1
    fid = add_formula(conn, "CA1 Pyramidal Neuron",
        r"C\frac{dV}{dt} = -I_{Na} - I_{Kdr} - I_{KA} - I_{KM} - I_{KAH} - I_{Ca} - I_h - I_L + I_{syn}",
        "Hippocampal CA1 pyramidal neuron",
        "ODE", specific, src,
        domain="hippocampus", model_origin="CA1-pyr")
    add_neuron(conn, fid, "CA1 Pyr", 1, -55, -65)

    # CA3 pyramidal
    fid = add_formula(conn, "CA3 Pyramidal Neuron",
        r"C\frac{dV}{dt} = -I_{Na} - I_{Kdr} - I_{KA} - I_{KM} - I_{Ca-T} - I_{Ca-L} - I_h - I_L + I_{syn}",
        "Hippocampal CA3 pyramidal with strong recurrent connections",
        "ODE", specific, src,
        domain="hippocampus", model_origin="CA3-pyr")
    add_neuron(conn, fid, "CA3 Pyr", 1, -55, -65)

    # Dentate granule cell
    fid = add_formula(conn, "Dentate Granule Cell",
        r"C\frac{dV}{dt} = -I_{Na} - I_K - I_{KA} - I_L + I_{syn}",
        "Hippocampal dentate gyrus granule cell",
        "ODE", specific, src,
        domain="hippocampus", model_origin="DG-granule")
    add_neuron(conn, fid, "DG Granule", 1, -50, -75)

    # O-LM interneuron
    fid = add_formula(conn, "O-LM Interneuron",
        r"C\frac{dV}{dt} = -I_{Na} - I_K - I_{KA} - I_h - I_L + I_{syn}",
        "Oriens-lacunosum moleculare interneuron",
        "ODE", specific, src,
        domain="hippocampus", model_origin="O-LM")
    add_neuron(conn, fid, "O-LM", 1, -55, -65)

    # Basket cell
    fid = add_formula(conn, "Hippocampal Basket Cell",
        r"C\frac{dV}{dt} = -I_{Na} - I_K - I_L + I_{syn}",
        "Fast-spiking perisomatic interneuron",
        "ODE", specific, src,
        domain="hippocampus", model_origin="basket")
    add_neuron(conn, fid, "Basket", 1, -55, -65)

    # === SIMPLIFIED MULTI-COMPARTMENT ===
    log.info("--- Ball-and-Stick Models ---")

    # Two compartment
    add_formula(conn, "Two-Compartment (Pinsky-Rinzel)",
        r"C_s \frac{dV_s}{dt} = -I_{Na} - I_{Kdr} + g_c(V_d - V_s)/p + I/p",
        "Soma compartment of two-compartment model",
        "ODE", multi, src,
        domain="reduced-models", model_origin="pinsky-rinzel-soma")

    add_formula(conn, "Two-Compartment Dendrite",
        r"C_d \frac{dV_d}{dt} = -I_{Ca} - I_{KCa} - I_{KAH} + g_c(V_s - V_d)/(1-p)",
        "Dendrite compartment of two-compartment model",
        "ODE", multi, src,
        domain="reduced-models", model_origin="pinsky-rinzel-dend")

    # Three compartment
    add_formula(conn, "Three-Compartment Model",
        r"C_j \frac{dV_j}{dt} = g_{j,j-1}(V_{j-1} - V_j) + g_{j,j+1}(V_{j+1} - V_j) + I_{ion,j}",
        "Axon-soma-dendrite three compartment",
        "ODE", multi, lit,
        domain="reduced-models", model_origin="3-compartment")

    print_summary(conn, "NEURON MODELS", start)
    conn.close()

if __name__ == "__main__":
    run()
