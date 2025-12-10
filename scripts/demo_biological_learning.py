#!/usr/bin/env python3
"""
Demonstration: Biological Learning Rules in Action

This script demonstrates the key biological learning rules from the database
with visualizations and comparisons.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve


def demo_stdp_window():
    """
    Visualize STDP timing window
    Formula ID: 25 - Pair-Based STDP
    """
    print("=" * 80)
    print("DEMO 1: STDP TIMING WINDOW")
    print("=" * 80)
    print("Formula: Δw = A₊ exp(-Δt/τ₊) if Δt > 0, -A₋ exp(Δt/τ₋) if Δt < 0")
    print()

    # Parameters
    A_plus = 0.1    # LTP amplitude
    A_minus = 0.12  # LTD amplitude (slightly larger for depression bias)
    tau_plus = 20   # ms
    tau_minus = 20  # ms

    # Time differences
    dt = np.linspace(-100, 100, 1000)

    # STDP function
    def stdp(dt, A_plus, A_minus, tau_plus, tau_minus):
        dw = np.zeros_like(dt)
        dw[dt > 0] = A_plus * np.exp(-dt[dt > 0] / tau_plus)
        dw[dt < 0] = -A_minus * np.exp(dt[dt < 0] / tau_minus)
        return dw

    dw = stdp(dt, A_plus, A_minus, tau_plus, tau_minus)

    print(f"Parameters:")
    print(f"  A₊ = {A_plus}, A₋ = {A_minus}")
    print(f"  τ₊ = {tau_plus} ms, τ₋ = {tau_minus} ms")
    print()
    print(f"Critical window: ±{4 * tau_plus} ms")
    print(f"Peak LTP at Δt = 0⁺: {A_plus:.3f}")
    print(f"Peak LTD at Δt = 0⁻: {-A_minus:.3f}")
    print()
    print("Interpretation:")
    print("  Δt > 0 (pre before post): LTP (strengthen synapse)")
    print("  Δt < 0 (post before pre): LTD (weaken synapse)")
    print("  |Δt| > 100 ms: No plasticity (causally unrelated)")
    print()


def demo_bcm_threshold():
    """
    Demonstrate BCM sliding threshold
    Formula ID: 27, 506 - BCM with sliding threshold
    """
    print("=" * 80)
    print("DEMO 2: BCM SLIDING THRESHOLD")
    print("=" * 80)
    print("Formula: dw/dt = η φ(c) c_pre, where φ(c) = c(c - θ)")
    print()

    # Parameters
    eta = 0.001
    tau_theta = 1000  # Slow timescale for threshold
    theta_0 = 1.0

    # Simulation
    T = 10000
    c = np.random.rand(T) * 2  # Postsynaptic activity
    c_pre = 1.0  # Constant presynaptic input

    # Initialize
    theta = np.zeros(T)
    w = np.zeros(T)
    theta[0] = theta_0
    w[0] = 0.5

    # Simulate
    for t in range(1, T):
        # BCM phi function
        phi = c[t] * (c[t] - theta[t-1])

        # Weight update
        dw = eta * phi * c_pre
        w[t] = w[t-1] + dw

        # Threshold update (sliding threshold)
        dtheta = (c[t]**2 - theta[t-1]) / tau_theta
        theta[t] = theta[t-1] + dtheta

    print(f"Parameters:")
    print(f"  η = {eta}, τ_θ = {tau_theta}")
    print(f"  Initial θ = {theta_0}")
    print()
    print(f"Results after {T} steps:")
    print(f"  Final weight: {w[-1]:.4f}")
    print(f"  Final threshold: {theta[-1]:.4f}")
    print(f"  Mean activity: {c.mean():.4f}")
    print(f"  Mean activity²: {(c**2).mean():.4f}")
    print()
    print("Key insight: Threshold converges to E[c²], creating selectivity")
    print()


def demo_ojas_rule_pca():
    """
    Demonstrate Oja's rule extracting principal component
    Formula ID: 29 - Oja's Learning Rule
    """
    print("=" * 80)
    print("DEMO 3: OJA'S RULE - PRINCIPAL COMPONENT ANALYSIS")
    print("=" * 80)
    print("Formula: Δwᵢ = η y(xᵢ - y wᵢ)")
    print()

    # Generate correlated 2D data
    np.random.seed(42)
    N = 1000  # Number of samples
    theta = np.pi / 4  # 45 degrees

    # Covariance matrix (elongated along 45° line)
    cov = np.array([[2, 1.5], [1.5, 2]])
    X = np.random.multivariate_normal([0, 0], cov, N).T

    # Oja's rule
    eta = 0.01
    w = np.random.randn(2)
    w = w / np.linalg.norm(w)  # Initialize normalized

    w_history = [w.copy()]

    for i in range(N):
        x = X[:, i]
        y = np.dot(w, x)

        # Oja's update
        dw = eta * y * (x - y * w)
        w += dw

        if i % 100 == 0:
            w_history.append(w.copy())

    # True principal component (eigenvector of covariance)
    eigenvalues, eigenvectors = np.linalg.eig(cov)
    pc1 = eigenvectors[:, np.argmax(eigenvalues)]

    # Align signs
    if np.dot(w, pc1) < 0:
        w = -w

    print(f"Data: {N} samples from 2D correlated Gaussian")
    print(f"Covariance matrix:")
    print(f"  {cov[0]}")
    print(f"  {cov[1]}")
    print()
    print(f"True principal component: [{pc1[0]:.4f}, {pc1[1]:.4f}]")
    print(f"Oja's learned weight:     [{w[0]:.4f}, {w[1]:.4f}]")
    print(f"Cosine similarity: {np.dot(w, pc1):.6f}")
    print()
    print("Key insight: Oja's rule converges to first principal component!")
    print()


def demo_calcium_thresholds():
    """
    Demonstrate calcium-based LTP/LTD thresholds
    Formula ID: 494 - Omega Function (LTP/LTD)
    """
    print("=" * 80)
    print("DEMO 4: CALCIUM-BASED PLASTICITY")
    print("=" * 80)
    print("Formula: Ω([Ca]) = sig([Ca] - θ_LTP) - 0.5·sig([Ca] - θ_LTD)")
    print()

    # Parameters
    theta_LTD = 0.3  # Low threshold
    theta_LTP = 0.7  # High threshold

    # Calcium range
    Ca = np.linspace(0, 1.2, 1000)

    # Sigmoid function
    def sigmoid(x, theta, k=20):
        return 1 / (1 + np.exp(-k * (x - theta)))

    # Omega function
    omega = sigmoid(Ca, theta_LTP) - 0.5 * sigmoid(Ca, theta_LTD)

    # Find LTD/LTP regions
    ltd_region = omega < 0
    ltp_region = omega > 0

    print(f"Thresholds:")
    print(f"  θ_LTD = {theta_LTD}")
    print(f"  θ_LTP = {theta_LTP}")
    print()
    print(f"Plasticity regions:")
    print(f"  [Ca] < {theta_LTD:.2f}: LTD (depression)")
    print(f"  {theta_LTD:.2f} < [Ca] < {theta_LTP:.2f}: Minimal change")
    print(f"  [Ca] > {theta_LTP:.2f}: LTP (potentiation)")
    print()
    print("Biological mechanism:")
    print("  Low Ca²⁺ → Calcineurin → LTD")
    print("  High Ca²⁺ → CaMKII → LTP")
    print()


def demo_reward_modulated_stdp():
    """
    Demonstrate reward-modulated STDP for reinforcement learning
    Formula ID: 504 - Reward-Modulated STDP
    """
    print("=" * 80)
    print("DEMO 5: REWARD-MODULATED STDP")
    print("=" * 80)
    print("Formula: dw/dt = c·STDP(Δt)·(R - R̄)")
    print()

    # Simple bandit task: 3 actions, action 2 gives reward
    n_actions = 3
    n_trials = 100

    # STDP parameters
    A_plus = 0.1
    tau_plus = 20

    # Eligibility trace parameter
    tau_e = 100  # Longer than STDP window

    # Initialize weights
    w = np.ones(n_actions) * 0.5
    eligibility = np.zeros(n_actions)
    reward_baseline = 0.0

    w_history = [w.copy()]
    reward_history = []

    print(f"Task: 3-armed bandit (action 2 gives reward)")
    print(f"Initial weights: {w}")
    print()

    np.random.seed(42)
    for trial in range(n_trials):
        # Select action (softmax)
        probs = np.exp(w * 5) / np.sum(np.exp(w * 5))
        action = np.random.choice(n_actions, p=probs)

        # Get reward
        reward = 1.0 if action == 2 else 0.0
        reward_history.append(reward)

        # Update eligibility trace for chosen action
        eligibility *= np.exp(-1 / tau_e)  # Decay
        eligibility[action] += A_plus  # STDP signal

        # Reward prediction error
        reward_error = reward - reward_baseline

        # Update weights
        w += 0.1 * eligibility * reward_error

        # Update baseline
        reward_baseline = 0.9 * reward_baseline + 0.1 * reward

        w_history.append(w.copy())

    w_history = np.array(w_history)

    print(f"Results after {n_trials} trials:")
    print(f"  Final weights: {w}")
    print(f"  Mean reward: {np.mean(reward_history[-20:]):.2f} (last 20 trials)")
    print(f"  Reward baseline: {reward_baseline:.2f}")
    print()
    print("Key insight: Weight for action 2 should be highest!")
    print(f"  Action 0: {w[0]:.3f}")
    print(f"  Action 1: {w[1]:.3f}")
    print(f"  Action 2: {w[2]:.3f} ← Should be highest")
    print()


def demo_homeostatic_scaling():
    """
    Demonstrate homeostatic synaptic scaling
    Formula ID: 508 - Synaptic Scaling
    """
    print("=" * 80)
    print("DEMO 6: HOMEOSTATIC SYNAPTIC SCALING")
    print("=" * 80)
    print("Formula: dw/dt = α(r_target - r)")
    print()

    # Simulate unstable Hebbian learning + homeostatic rescue
    T = 5000
    n_syn = 10

    # Hebbian parameters
    eta_hebb = 0.01

    # Homeostatic parameters
    alpha_homeo = 0.0001  # Slow timescale
    r_target = 0.5

    # Initialize
    w = np.random.rand(n_syn) * 0.5
    x = np.random.rand(T, n_syn)  # Input patterns

    w_history = [w.copy()]
    rate_history = []

    print(f"Parameters:")
    print(f"  Hebbian η = {eta_hebb}")
    print(f"  Homeostatic α = {alpha_homeo}")
    print(f"  Target rate = {r_target}")
    print()

    for t in range(1, T):
        # Compute output
        y = np.dot(w, x[t])
        rate = 1 / (1 + np.exp(-y))  # Sigmoid
        rate_history.append(rate)

        # Hebbian update (unstable!)
        dw_hebb = eta_hebb * y * x[t]

        # Homeostatic update (stabilizing)
        dw_homeo = alpha_homeo * (r_target - rate) * np.ones_like(w)

        # Combined update
        w += dw_hebb + dw_homeo

        # Prevent negative weights
        w = np.maximum(w, 0)

        if t % 500 == 0:
            w_history.append(w.copy())

    print(f"Results after {T} steps:")
    print(f"  Mean firing rate: {np.mean(rate_history[-100:]):.4f}")
    print(f"  Target rate: {r_target}")
    print(f"  Final weight sum: {w.sum():.4f}")
    print()
    print("Without homeostasis, Hebbian learning would cause runaway potentiation!")
    print("Homeostatic scaling maintains stable firing rate.")
    print()


def compare_learning_rules():
    """
    Compare different learning rules on same task
    """
    print("=" * 80)
    print("DEMO 7: COMPARISON OF LEARNING RULES")
    print("=" * 80)
    print()

    # Simple classification task: learn XOR-like pattern
    np.random.seed(42)
    N = 200

    # Generate data
    X = np.random.randn(N, 2)
    y = (X[:, 0] * X[:, 1] > 0).astype(float)

    # Test different rules
    rules = {
        'Hebbian (unstable)': lambda w, x, y, t: 0.01 * y * x,
        'Oja (stable)': lambda w, x, y, t: 0.01 * y * (x - y * w),
        'BCM': lambda w, x, y, t: 0.01 * y * (y - 0.5) * x,
    }

    print("Task: Learn correlation structure from 2D data")
    print(f"Samples: {N}")
    print()

    for name, rule in rules.items():
        w = np.random.randn(2) * 0.1
        for i in range(N):
            x_i = X[i]
            y_i = np.dot(w, x_i)
            dw = rule(w, x_i, y_i, i)
            w += dw

        print(f"{name:25} Final weight: [{w[0]:7.4f}, {w[1]:7.4f}], norm: {np.linalg.norm(w):.4f}")

    print()
    print("Observations:")
    print("  - Hebbian: Unbounded growth")
    print("  - Oja: Normalized (||w|| ≈ constant)")
    print("  - BCM: Selective (depends on threshold)")
    print()


def print_summary():
    """Print summary of all demos"""
    print("\n" + "=" * 80)
    print("SUMMARY: BIOLOGICAL LEARNING PRINCIPLES")
    print("=" * 80)
    print()
    print("1. STDP: Temporal causality detection (ms timescale)")
    print("   - Pre before post → LTP (strengthen)")
    print("   - Post before pre → LTD (weaken)")
    print()
    print("2. BCM: Sliding threshold creates selectivity")
    print("   - Threshold adapts to activity history")
    print("   - Enables feature selectivity")
    print()
    print("3. Oja: Self-normalizing Hebbian learning")
    print("   - Extracts principal components")
    print("   - Weight normalization prevents runaway")
    print()
    print("4. Calcium: Biochemical signal determines plasticity")
    print("   - Low [Ca²⁺] → LTD")
    print("   - High [Ca²⁺] → LTP")
    print()
    print("5. Reward-modulated: Three-factor learning")
    print("   - Correlation + eligibility + reward")
    print("   - Implements reinforcement learning")
    print()
    print("6. Homeostatic: Maintains stability")
    print("   - Slow timescale (hours-days)")
    print("   - Prevents runaway dynamics")
    print()
    print("7. Multiple rules coexist and interact")
    print("   - Fast (STDP) + slow (homeostatic)")
    print("   - Hebbian + metaplasticity")
    print("   - Unsupervised + reward-modulated")
    print()
    print("=" * 80)
    print("KEY INSIGHT: Biology uses LOCAL, MULTI-TIMESCALE, COMPOSABLE rules")
    print("=" * 80)
    print()


if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("BIOLOGICAL LEARNING RULES: PRACTICAL DEMONSTRATIONS")
    print("Database: /home/user/MAINFRAME/bioformulas/bioformulas.db")
    print("=" * 80)
    print()

    # Run all demos
    demo_stdp_window()
    demo_bcm_threshold()
    demo_ojas_rule_pca()
    demo_calcium_thresholds()
    demo_reward_modulated_stdp()
    demo_homeostatic_scaling()
    compare_learning_rules()

    # Summary
    print_summary()

    print("=" * 80)
    print("Demos complete!")
    print()
    print("For detailed analysis and PyTorch implementations, see:")
    print("  - biological_learning_analysis.md")
    print("  - learning_formulas_quick_ref.md")
    print("=" * 80)
