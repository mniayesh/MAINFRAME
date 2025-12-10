"""
Visualize Signal Amplification Mechanisms
Generate plots for all five core amplification principles
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6']

def plot_mapk_cascade():
    """Plot MAPK cascade dynamics"""
    def mapk_system(state, t, signal):
        Raf, MEK, ERK = state

        # Parameters
        k1, Km1, k2, Km2 = 10.0, 5.0, 1.0, 5.0
        k3, Km3, k4, Km4 = 10.0, 5.0, 1.0, 5.0
        k5, Km5, k6, Km6 = 10.0, 5.0, 1.0, 5.0

        Raf_total = MEK_total = ERK_total = 100.0

        dRaf = (k1 * signal * (Raf_total - Raf)) / (Km1 + (Raf_total - Raf)) - (k2 * Raf) / (Km2 + Raf)
        dMEK = (k3 * Raf * (MEK_total - MEK)) / (Km3 + (MEK_total - MEK)) - (k4 * MEK) / (Km4 + MEK)
        dERK = (k5 * MEK * (ERK_total - ERK)) / (Km5 + (ERK_total - ERK)) - (k6 * ERK) / (Km6 + ERK)

        return [dRaf, dMEK, dERK]

    t = np.linspace(0, 10, 1000)
    signal = 1.0  # Single Ras-GTP molecule
    state0 = [0.0, 0.0, 0.0]

    solution = odeint(mapk_system, state0, t, args=(signal,))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Time course
    ax1.plot(t, solution[:, 0], label='Raf* (Layer 1)', color=colors[0], linewidth=2)
    ax1.plot(t, solution[:, 1], label='MEK* (Layer 2)', color=colors[1], linewidth=2)
    ax1.plot(t, solution[:, 2], label='ERK* (Layer 3)', color=colors[2], linewidth=2)
    ax1.axhline(y=signal, color='gray', linestyle='--', label=f'Input Signal = {signal}')
    ax1.set_xlabel('Time (arbitrary units)', fontsize=12)
    ax1.set_ylabel('Active Kinase Concentration', fontsize=12)
    ax1.set_title('MAPK Cascade: Sequential Amplification', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)

    # Amplification at each stage
    stages = ['Input\n(Ras-GTP)', 'Layer 1\n(Raf)', 'Layer 2\n(MEK)', 'Layer 3\n(ERK)']
    values = [signal, solution[-1, 0], solution[-1, 1], solution[-1, 2]]
    amplifications = [1, values[1]/values[0], values[2]/values[1], values[3]/values[2]]

    bars = ax2.bar(stages, values, color=[colors[3]] + colors[:3], alpha=0.7, edgecolor='black')
    ax2.set_ylabel('Steady-State Concentration', fontsize=12)
    ax2.set_title('Amplification at Each Stage', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')

    # Add amplification factors
    for i, (bar, amp) in enumerate(zip(bars[1:], amplifications[1:]), 1):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{amp:.1f}x',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Total amplification
    total_amp = values[-1] / values[0]
    ax2.text(0.5, 0.95, f'Total Amplification: {total_amp:.1f}x',
            transform=ax2.transAxes, ha='center', va='top',
            fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig('/home/user/MAINFRAME/mapk_cascade.png', dpi=300, bbox_inches='tight')
    print("Saved: mapk_cascade.png")
    plt.close()

def plot_goldbeter_koshland():
    """Plot Goldbeter-Koshland ultrasensitivity"""
    def gk_formula(v1, v2, J1, J2):
        B = v2 - v1 + J1*v2 + J2*v1
        discriminant = B**2 - 4*(v2-v1)*v1*J2
        discriminant = np.maximum(discriminant, 0)
        return (2*v1*J2) / (B + np.sqrt(discriminant))

    v1_range = np.linspace(0.01, 10, 200)
    v2 = 5.0

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Different J values (enzyme saturation levels)
    J_values = [(0.01, 0.01, 'High saturation'), (0.1, 0.1, 'Medium saturation'), (1.0, 1.0, 'Low saturation')]

    for i, (J1, J2, label) in enumerate(J_values):
        response = [gk_formula(v1, v2, J1, J2) for v1 in v1_range]
        ax1.plot(v1_range, response, label=label, linewidth=2, color=colors[i])

    ax1.set_xlabel('Kinase Activity (v₁)', fontsize=12)
    ax1.set_ylabel('Activated Protein [W*]', fontsize=12)
    ax1.set_title('Goldbeter-Koshland Ultrasensitivity', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 10)

    # Compare with Michaelis-Menten (no ultrasensitivity)
    v1_range2 = np.linspace(0.01, 10, 200)
    gk_response = [gk_formula(v1, v2, 0.1, 0.1) for v1 in v1_range2]
    mm_response = v1_range2 / (1 + v1_range2)  # Michaelis-Menten

    # Normalize for comparison
    gk_norm = np.array(gk_response) / np.max(gk_response)
    mm_norm = mm_response / np.max(mm_response)

    ax2.plot(v1_range2, gk_norm, label='Goldbeter-Koshland\n(ultrasensitive)', linewidth=2, color=colors[0])
    ax2.plot(v1_range2, mm_norm, label='Michaelis-Menten\n(standard)', linewidth=2, color=colors[3], linestyle='--')

    # Mark 10% and 90% points
    idx_10_gk = np.argmin(np.abs(gk_norm - 0.1))
    idx_90_gk = np.argmin(np.abs(gk_norm - 0.9))
    idx_10_mm = np.argmin(np.abs(mm_norm - 0.1))
    idx_90_mm = np.argmin(np.abs(mm_norm - 0.9))

    ax2.plot([v1_range2[idx_10_gk], v1_range2[idx_90_gk]], [0.1, 0.9], 'o-', color=colors[0], markersize=8)
    ax2.plot([v1_range2[idx_10_mm], v1_range2[idx_90_mm]], [0.1, 0.9], 'o-', color=colors[3], markersize=8)

    # Dynamic range
    dr_gk = v1_range2[idx_90_gk] / v1_range2[idx_10_gk]
    dr_mm = v1_range2[idx_90_mm] / v1_range2[idx_10_mm]

    ax2.text(0.05, 0.95, f'GK dynamic range: {dr_gk:.1f}x\nMM dynamic range: {dr_mm:.1f}x',
            transform=ax2.transAxes, va='top', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ax2.set_xlabel('Input Signal', fontsize=12)
    ax2.set_ylabel('Normalized Response', fontsize=12)
    ax2.set_title('Ultrasensitive vs Standard Response', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/user/MAINFRAME/goldbeter_koshland.png', dpi=300, bbox_inches='tight')
    print("Saved: goldbeter_koshland.png")
    plt.close()

def plot_hill_cooperativity():
    """Plot Hill equation with different coefficients"""
    def hill_equation(S, Vmax, K, n):
        return Vmax * S**n / (K**n + S**n)

    S_range = np.logspace(-2, 2, 300)
    Vmax = 1.0
    K = 1.0

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Different Hill coefficients
    hill_coeffs = [1, 2, 4, 8]

    for i, n in enumerate(hill_coeffs):
        response = [hill_equation(s, Vmax, K, n) for s in S_range]
        ax1.plot(S_range, response, label=f'n = {n}', linewidth=2, color=colors[i % len(colors)])

    ax1.set_xscale('log')
    ax1.set_xlabel('Substrate Concentration [S]', fontsize=12)
    ax1.set_ylabel('Reaction Rate v', fontsize=12)
    ax1.set_title('Hill Equation: Cooperative Binding', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.axvline(x=K, color='gray', linestyle='--', alpha=0.5, label='K₀.₅')
    ax1.axhline(y=Vmax/2, color='gray', linestyle='--', alpha=0.5)

    # Steepness comparison (log-log plot)
    for i, n in enumerate(hill_coeffs):
        response = [hill_equation(s, Vmax, K, n) for s in S_range]
        # Transform to show steepness
        y_transform = np.array([r/(Vmax - r + 1e-10) for r in response])
        ax2.plot(S_range, y_transform, label=f'n = {n}', linewidth=2, color=colors[i % len(colors)])

    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('Substrate Concentration [S]', fontsize=12)
    ax2.set_ylabel('Response Ratio (logit scale)', fontsize=12)
    ax2.set_title('Response Steepness (Hill Plot)', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig('/home/user/MAINFRAME/hill_cooperativity.png', dpi=300, bbox_inches='tight')
    print("Saved: hill_cooperativity.png")
    plt.close()

def plot_bistable_switch():
    """Plot toggle switch bistability"""
    def toggle_switch(state, t, alpha1, alpha2, beta, gamma):
        u, v = state
        du = alpha1 / (1 + v**beta) - u
        dv = alpha2 / (1 + u**gamma) - v
        return [du, dv]

    alpha1, alpha2 = 10.0, 10.0
    beta, gamma = 4.0, 4.0

    t = np.linspace(0, 20, 1000)

    # Two different initial conditions
    state0_low = [0.1, 9.0]   # Low u, High v
    state0_high = [9.0, 0.1]  # High u, Low v

    sol_low = odeint(toggle_switch, state0_low, t, args=(alpha1, alpha2, beta, gamma))
    sol_high = odeint(toggle_switch, state0_high, t, args=(alpha1, alpha2, beta, gamma))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Time course
    ax1.plot(t, sol_low[:, 0], label='u (from low state)', color=colors[0], linewidth=2)
    ax1.plot(t, sol_low[:, 1], label='v (from low state)', color=colors[1], linewidth=2, linestyle='--')
    ax1.plot(t, sol_high[:, 0], label='u (from high state)', color=colors[2], linewidth=2)
    ax1.plot(t, sol_high[:, 1], label='v (from high state)', color=colors[3], linewidth=2, linestyle='--')

    ax1.set_xlabel('Time', fontsize=12)
    ax1.set_ylabel('Gene Expression Level', fontsize=12)
    ax1.set_title('Bistable Toggle Switch: Memory', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Phase plane
    u_range = np.linspace(0, 10, 30)
    v_range = np.linspace(0, 10, 30)
    U, V = np.meshgrid(u_range, v_range)

    dU = alpha1 / (1 + V**beta) - U
    dV = alpha2 / (1 + U**gamma) - V

    ax2.streamplot(U, V, dU, dV, color='gray', linewidth=0.5, density=1.5)
    ax2.plot(sol_low[:, 0], sol_low[:, 1], color=colors[0], linewidth=2, label='Trajectory 1')
    ax2.plot(sol_high[:, 0], sol_high[:, 1], color=colors[2], linewidth=2, label='Trajectory 2')
    ax2.plot(sol_low[0, 0], sol_low[0, 1], 'o', color=colors[0], markersize=10, label='Start 1')
    ax2.plot(sol_high[0, 0], sol_high[0, 1], 'o', color=colors[2], markersize=10, label='Start 2')
    ax2.plot(sol_low[-1, 0], sol_low[-1, 1], 's', color=colors[0], markersize=10, label='End 1')
    ax2.plot(sol_high[-1, 0], sol_high[-1, 1], 's', color=colors[2], markersize=10, label='End 2')

    ax2.set_xlabel('Gene u Expression', fontsize=12)
    ax2.set_ylabel('Gene v Expression', fontsize=12)
    ax2.set_title('Phase Plane: Two Stable States', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/user/MAINFRAME/bistable_switch.png', dpi=300, bbox_inches='tight')
    print("Saved: bistable_switch.png")
    plt.close()

def plot_gtpase_cycle():
    """Plot GTPase cycle amplification"""
    def gtpase_system(state, t, signal, k_GEF, k_GAP, k_intrinsic):
        Ras_GDP, Ras_GTP = state
        total_Ras = 100.0
        Ras_GDP = total_Ras - Ras_GTP

        activation = k_GEF * signal * Ras_GDP
        deactivation = (k_GAP + k_intrinsic) * Ras_GTP

        dRas_GTP = activation - deactivation
        dRas_GDP = -dRas_GTP

        return [dRas_GDP, dRas_GTP]

    t = np.linspace(0, 10, 1000)

    # Different signal strengths
    signals = [0.5, 1.0, 2.0]
    k_GEF = 5.0
    k_GAP = 0.5
    k_intrinsic = 0.1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    amplifications = []

    for i, signal in enumerate(signals):
        state0 = [100.0, 0.0]
        solution = odeint(gtpase_system, state0, t, args=(signal, k_GEF, k_GAP, k_intrinsic))

        ax1.plot(t, solution[:, 1], label=f'Signal = {signal}', linewidth=2, color=colors[i])

        # Calculate amplification
        steady_state_RasGTP = solution[-1, 1]
        amp = steady_state_RasGTP / signal
        amplifications.append(amp)

    ax1.set_xlabel('Time', fontsize=12)
    ax1.set_ylabel('[Ras-GTP] (Active)', fontsize=12)
    ax1.set_title('GTPase Cycle: Catalytic Amplification', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)

    # Amplification bar chart
    bars = ax2.bar([f'Signal\n{s}' for s in signals], amplifications, color=colors[:3], alpha=0.7, edgecolor='black')
    ax2.set_ylabel('Amplification Factor', fontsize=12)
    ax2.set_title('GTPase Amplification Factor', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')

    # Add values on bars
    for bar, amp in zip(bars, amplifications):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{amp:.1f}x',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Average amplification
    avg_amp = np.mean(amplifications)
    ax2.text(0.5, 0.95, f'Average Amplification: {avg_amp:.1f}x',
            transform=ax2.transAxes, ha='center', va='top',
            fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig('/home/user/MAINFRAME/gtpase_cycle.png', dpi=300, bbox_inches='tight')
    print("Saved: gtpase_cycle.png")
    plt.close()

def plot_combined_summary():
    """Summary plot of all amplification mechanisms"""
    fig, ax = plt.subplots(figsize=(12, 8))

    mechanisms = ['MAPK\nCascade', 'GTPase\nCycle', 'Goldbeter-\nKoshland', 'Hill\nCooperativity\n(n=8)', 'Bistable\nSwitch']
    amplifications = [100, 89, 4.5, 8, 100]  # Representative values
    types = ['Sequential', 'Catalytic', 'Zero-Order', 'Cooperative', 'Feedback']

    bars = ax.bar(mechanisms, amplifications, color=colors, alpha=0.7, edgecolor='black', linewidth=2)

    # Add values on bars
    for bar, amp, mech_type in zip(bars, amplifications, types):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{amp:.1f}x',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
        ax.text(bar.get_x() + bar.get_width()/2., height/2,
                mech_type,
                ha='center', va='center', fontsize=9, rotation=0,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.set_ylabel('Amplification Factor', fontsize=14, fontweight='bold')
    ax.set_title('Biological Signal Amplification Mechanisms', fontsize=16, fontweight='bold')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3, axis='y')

    # Add combined amplification annotation
    combined = 100 * 89 * 4.5  # Cascaded effect
    ax.text(0.5, 0.95, f'Combined Cascade: ~{combined/1000:.0f},000x → 1000x (with saturation)',
            transform=ax.transAxes, ha='center', va='top',
            fontsize=13, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

    plt.tight_layout()
    plt.savefig('/home/user/MAINFRAME/amplification_summary.png', dpi=300, bbox_inches='tight')
    print("Saved: amplification_summary.png")
    plt.close()

if __name__ == "__main__":
    print("Generating amplification visualizations...")
    print("-" * 50)

    plot_mapk_cascade()
    plot_goldbeter_koshland()
    plot_hill_cooperativity()
    plot_bistable_switch()
    plot_gtpase_cycle()
    plot_combined_summary()

    print("-" * 50)
    print("All visualizations generated!")
    print("\nFiles created:")
    print("  1. mapk_cascade.png - Sequential amplification")
    print("  2. goldbeter_koshland.png - Ultrasensitivity")
    print("  3. hill_cooperativity.png - Cooperative binding")
    print("  4. bistable_switch.png - Memory and bistability")
    print("  5. gtpase_cycle.png - Catalytic amplification")
    print("  6. amplification_summary.png - All mechanisms")
