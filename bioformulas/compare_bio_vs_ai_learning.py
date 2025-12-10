#!/usr/bin/env python3
"""
Compare biological learning rules to artificial neural network learning algorithms.

This script implements both biological (STDP, BCM, Oja) and AI (backprop, Hebbian)
learning rules and compares their properties.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from typing import Callable, Tuple
from dataclasses import dataclass


@dataclass
class LearningRuleProperties:
    """Properties of a learning rule."""
    name: str
    local: bool  # Can be computed using only local information
    supervised: bool  # Requires labels/error signals
    temporal: bool  # Uses precise timing information
    symmetric: bool  # Requires symmetric forward/backward weights
    stable: bool  # Has intrinsic stability mechanisms
    biological: bool  # Biologically plausible


class BiologicalLearningRules:
    """Implementation of biological learning rules from the database."""

    @staticmethod
    def pair_stdp(dt: float, A_plus: float = 1.0, A_minus: float = 1.0,
                  tau_plus: float = 20.0, tau_minus: float = 20.0) -> float:
        """
        Pair-based STDP (Spike-Timing Dependent Plasticity).

        Args:
            dt: Time difference (t_post - t_pre) in ms
            A_plus: LTP amplitude
            A_minus: LTD amplitude
            tau_plus: LTP time constant (ms)
            tau_minus: LTD time constant (ms)

        Returns:
            Weight change Δw
        """
        if dt > 0:
            # Pre before post → LTP (potentiation)
            return A_plus * np.exp(-dt / tau_plus)
        else:
            # Post before pre → LTD (depression)
            return -A_minus * np.exp(dt / tau_minus)

    @staticmethod
    def triplet_stdp(pre_trace: float, post_trace: float,
                     pre_trace2: float, post_trace2: float,
                     A2_plus: float = 1.0, A3_plus: float = 0.5,
                     A2_minus: float = 1.0, A3_minus: float = 0.5) -> float:
        """
        Triplet STDP capturing frequency dependence.

        Args:
            pre_trace: Recent pre-synaptic activity trace
            post_trace: Recent post-synaptic activity trace
            pre_trace2: Second-order pre-synaptic trace
            post_trace2: Second-order post-synaptic trace
            A2_plus, A3_plus: LTP parameters
            A2_minus, A3_minus: LTD parameters

        Returns:
            Weight change Δw
        """
        ltp = pre_trace * (A2_plus + A3_plus * post_trace2)
        ltd = post_trace * (A2_minus + A3_minus * pre_trace2)
        return ltp - ltd

    @staticmethod
    def bcm_rule(c_post: float, c_pre: float, eta: float = 0.001,
                 theta: float = 1.0, power: float = 2.0) -> float:
        """
        BCM (Bienenstock-Cooper-Munro) plasticity rule.

        Args:
            c_post: Post-synaptic activity
            c_pre: Pre-synaptic activity
            eta: Learning rate
            theta: Sliding threshold
            power: Nonlinearity power

        Returns:
            Weight change dw/dt
        """
        # φ(c) = c(c - θ^p) - nonlinear function with threshold
        phi = c_post * (c_post - theta**power)
        return eta * phi * c_pre

    @staticmethod
    def oja_rule(x: np.ndarray, y: float, w: np.ndarray, eta: float = 0.01) -> np.ndarray:
        """
        Oja's learning rule (Hebbian with normalization).

        Performs PCA - extracts principal component.

        Args:
            x: Input vector (pre-synaptic)
            y: Output (post-synaptic)
            w: Weight vector
            eta: Learning rate

        Returns:
            Weight change Δw
        """
        return eta * y * (x - y * w)

    @staticmethod
    def calcium_plasticity(ca_concentration: float,
                          w: float,
                          gamma_p: float = 0.001,
                          gamma_d: float = 0.001,
                          theta_p: float = 1.0,
                          theta_d: float = 2.0) -> float:
        """
        Calcium-based plasticity.

        Different calcium levels trigger different plasticity:
        - Low [Ca2+]: LTD
        - Medium [Ca2+]: No change
        - High [Ca2+]: LTP

        Args:
            ca_concentration: Calcium concentration
            w: Current weight
            gamma_p: Potentiation rate
            gamma_d: Depression rate
            theta_p: LTD threshold
            theta_d: LTP threshold

        Returns:
            Weight change dw/dt
        """
        # Omega functions (nonlinear calcium dependence)
        if ca_concentration < theta_p:
            omega_p = 0
            omega_d = 1
        elif ca_concentration < theta_d:
            omega_p = 0
            omega_d = 0
        else:
            omega_p = 1
            omega_d = 0

        return gamma_p * omega_p - gamma_d * omega_d * w

    @staticmethod
    def covariance_rule(x: np.ndarray, y: np.ndarray,
                       x_mean: np.ndarray, y_mean: np.ndarray,
                       eta: float = 0.01) -> np.ndarray:
        """
        Covariance learning rule.

        Args:
            x: Pre-synaptic activity
            y: Post-synaptic activity
            x_mean: Mean pre-synaptic activity
            y_mean: Mean post-synaptic activity
            eta: Learning rate

        Returns:
            Weight change Δw
        """
        return eta * np.outer(x - x_mean, y - y_mean)


class AILearningRules:
    """Implementation of standard AI learning algorithms."""

    @staticmethod
    def backpropagation(output: np.ndarray, target: np.ndarray,
                       activation: np.ndarray, learning_rate: float = 0.01) -> np.ndarray:
        """
        Standard backpropagation gradient descent.

        Args:
            output: Network output
            target: Target values (labels)
            activation: Pre-synaptic activation
            learning_rate: Learning rate

        Returns:
            Weight change Δw
        """
        # Error signal (requires labels)
        delta = output - target

        # Gradient (requires error from output)
        dw = learning_rate * np.outer(activation, delta)

        return -dw  # Negative gradient

    @staticmethod
    def hebbian(x: np.ndarray, y: np.ndarray, eta: float = 0.01) -> np.ndarray:
        """
        Basic Hebbian learning: "neurons that fire together, wire together".

        Args:
            x: Pre-synaptic activity
            y: Post-synaptic activity
            eta: Learning rate

        Returns:
            Weight change Δw
        """
        return eta * np.outer(x, y)

    @staticmethod
    def contrastive_learning(z1: np.ndarray, z2: np.ndarray,
                            temperature: float = 0.5) -> float:
        """
        Simplified contrastive learning (e.g., SimCLR-style).

        Positive pairs (z1, z2 are augmented views of same sample) should have high similarity.

        Args:
            z1: First representation
            z2: Second representation
            temperature: Temperature parameter

        Returns:
            Similarity score
        """
        # Cosine similarity
        similarity = np.dot(z1, z2) / (np.linalg.norm(z1) * np.linalg.norm(z2))
        return similarity / temperature


def plot_stdp_window():
    """Plot STDP learning window."""
    dt = np.linspace(-50, 50, 1000)
    dw = np.array([BiologicalLearningRules.pair_stdp(t) for t in dt])

    plt.figure(figsize=(10, 6))
    plt.plot(dt, dw, linewidth=2)
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='--', alpha=0.3)
    plt.xlabel('Spike timing Δt = t_post - t_pre (ms)', fontsize=12)
    plt.ylabel('Weight change Δw', fontsize=12)
    plt.title('STDP Learning Window: Biology\'s Temporal Credit Assignment', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)

    # Annotate regions
    plt.text(20, 0.5, 'LTP\n(potentiation)', ha='center', fontsize=10, color='green')
    plt.text(-20, -0.5, 'LTD\n(depression)', ha='center', fontsize=10, color='red')
    plt.text(0, -0.8, 'Pre before Post → Strengthen\nPost before Pre → Weaken',
             ha='center', fontsize=9, style='italic')

    plt.tight_layout()
    plt.savefig('/home/user/MAINFRAME/bioformulas/stdp_window.png', dpi=150)
    print("Saved: stdp_window.png")


def plot_calcium_plasticity():
    """Plot calcium-dependent plasticity."""
    ca_levels = np.linspace(0, 5, 1000)
    dw = np.array([BiologicalLearningRules.calcium_plasticity(ca, w=1.0,
                                                               theta_p=1.5,
                                                               theta_d=3.0)
                   for ca in ca_levels])

    plt.figure(figsize=(10, 6))
    plt.plot(ca_levels, dw, linewidth=2, color='purple')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.xlabel('[Ca²⁺] concentration (arbitrary units)', fontsize=12)
    plt.ylabel('Weight change dw/dt', fontsize=12)
    plt.title('Calcium-Dependent Plasticity: Biology\'s Biochemical Learning', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)

    # Annotate regions
    plt.axvspan(0, 1.5, alpha=0.1, color='red', label='LTD zone')
    plt.axvspan(1.5, 3.0, alpha=0.1, color='gray', label='No change')
    plt.axvspan(3.0, 5.0, alpha=0.1, color='green', label='LTP zone')
    plt.legend()

    plt.text(0.75, -0.0005, 'Low [Ca²⁺]\n→ LTD', ha='center', fontsize=9)
    plt.text(2.25, 0, 'Medium [Ca²⁺]\n→ No change', ha='center', fontsize=9)
    plt.text(4.0, 0.0005, 'High [Ca²⁺]\n→ LTP', ha='center', fontsize=9)

    plt.tight_layout()
    plt.savefig('/home/user/MAINFRAME/bioformulas/calcium_plasticity.png', dpi=150)
    print("Saved: calcium_plasticity.png")


def plot_bcm_rule():
    """Plot BCM plasticity rule."""
    c_post = np.linspace(0, 3, 1000)
    theta = 1.5
    phi = c_post * (c_post - theta**2)  # BCM nonlinearity

    plt.figure(figsize=(10, 6))
    plt.plot(c_post, phi, linewidth=2, color='blue')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.axvline(x=theta, color='r', linestyle='--', alpha=0.5, label=f'Threshold θ = {theta}')
    plt.xlabel('Post-synaptic activity c_post', fontsize=12)
    plt.ylabel('Plasticity function φ(c)', fontsize=12)
    plt.title('BCM Rule: Sliding Threshold Plasticity', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Annotate regions
    plt.fill_between(c_post, phi, 0, where=(phi < 0), alpha=0.2, color='red', label='LTD')
    plt.fill_between(c_post, phi, 0, where=(phi > 0), alpha=0.2, color='green', label='LTP')

    plt.text(0.7, -0.5, 'Low activity\n→ LTD', ha='center', fontsize=9)
    plt.text(2.3, 0.5, 'High activity\n→ LTP', ha='center', fontsize=9)

    plt.tight_layout()
    plt.savefig('/home/user/MAINFRAME/bioformulas/bcm_rule.png', dpi=150)
    print("Saved: bcm_rule.png")


def compare_learning_rules():
    """Compare properties of biological vs. AI learning rules."""
    rules = [
        LearningRuleProperties("Pair STDP", True, False, True, False, False, True),
        LearningRuleProperties("Triplet STDP", True, False, True, False, False, True),
        LearningRuleProperties("BCM Rule", True, False, False, False, True, True),
        LearningRuleProperties("Oja's Rule", True, False, False, False, True, True),
        LearningRuleProperties("Calcium Plasticity", True, False, True, False, True, True),
        LearningRuleProperties("Backpropagation", False, True, False, True, False, False),
        LearningRuleProperties("Basic Hebbian", True, False, False, False, False, True),
        LearningRuleProperties("Contrastive Learning", False, False, False, False, False, False),
    ]

    print("\n" + "="*100)
    print("COMPARISON: BIOLOGICAL vs. AI LEARNING RULES")
    print("="*100)
    print(f"{'Rule':<25} {'Local':<8} {'Supervised':<12} {'Temporal':<10} {'Symmetric':<11} {'Stable':<8} {'Biological':<12}")
    print("-"*100)

    for rule in rules:
        print(f"{rule.name:<25} {str(rule.local):<8} {str(rule.supervised):<12} "
              f"{str(rule.temporal):<10} {str(rule.symmetric):<11} {str(rule.stable):<8} "
              f"{str(rule.biological):<12}")

    print("-"*100)
    print("\nKEY INSIGHTS:")
    print("1. All biological rules are LOCAL - no global error signals needed")
    print("2. Biological rules are mostly UNSUPERVISED - work without labels")
    print("3. Many biological rules use TEMPORAL information (spike timing)")
    print("4. Biological rules often have INTRINSIC STABILITY (BCM threshold, Oja normalization)")
    print("5. Backprop requires SYMMETRIC weights (weight transport problem)")
    print("="*100)


def demonstrate_oja_pca():
    """Demonstrate that Oja's rule performs PCA."""
    print("\n" + "="*80)
    print("DEMONSTRATION: OJA'S RULE PERFORMS PCA")
    print("="*80)

    # Create correlated 2D data
    np.random.seed(42)
    n_samples = 1000

    # Data with principal axis at 45 degrees
    x1 = np.random.randn(n_samples)
    x2 = x1 + 0.3 * np.random.randn(n_samples)
    X = np.column_stack([x1, x2])

    # Standardize
    X = (X - X.mean(axis=0)) / X.std(axis=0)

    # Initialize random weight vector
    w = np.random.randn(2)
    w = w / np.linalg.norm(w)

    # True PCA
    from numpy.linalg import eig
    cov_matrix = np.cov(X.T)
    eigenvalues, eigenvectors = eig(cov_matrix)
    pc1 = eigenvectors[:, np.argmax(eigenvalues)]

    print(f"\nTrue PC1 (from eigendecomposition): {pc1}")
    print(f"Initial random weight: {w}")

    # Train with Oja's rule
    eta = 0.01
    n_epochs = 100

    for epoch in range(n_epochs):
        for x in X:
            y = np.dot(w, x)
            dw = BiologicalLearningRules.oja_rule(x, y, w, eta)
            w += dw

            # Normalize (Oja's rule should do this automatically, but helps stability)
            w = w / np.linalg.norm(w)

        if (epoch + 1) % 20 == 0:
            print(f"Epoch {epoch+1}: w = {w}, alignment with PC1 = {abs(np.dot(w, pc1)):.4f}")

    print(f"\nFinal weight after Oja's rule: {w}")
    print(f"Alignment with true PC1: {abs(np.dot(w, pc1)):.4f} (1.0 = perfect)")
    print("\n→ Oja's rule successfully finds the principal component!")
    print("="*80)


def main():
    """Run all comparisons and demonstrations."""
    print("="*80)
    print("BIOLOGICAL vs. AI LEARNING RULES: COMPREHENSIVE COMPARISON")
    print("="*80)

    # Plot STDP window
    print("\nGenerating STDP learning window plot...")
    plot_stdp_window()

    # Plot calcium plasticity
    print("\nGenerating calcium plasticity plot...")
    plot_calcium_plasticity()

    # Plot BCM rule
    print("\nGenerating BCM rule plot...")
    plot_bcm_rule()

    # Compare rule properties
    compare_learning_rules()

    # Demonstrate Oja's rule
    demonstrate_oja_pca()

    print("\n" + "="*80)
    print("SUMMARY: WHAT AI CAN LEARN FROM BIOLOGY")
    print("="*80)
    print("""
1. LOCAL LEARNING IS POSSIBLE
   - STDP, BCM, Oja all work with purely local information
   - No need for global error signals or backpropagation
   - Enables distributed, parallel learning

2. TIME IS A POWERFUL LEARNING SIGNAL
   - STDP uses precise spike timing (±20ms) for credit assignment
   - Causality detection: pre-before-post → strengthen
   - No external error signal needed

3. MULTIPLE TIMESCALES MATTER
   - Fast: STDP (~20ms)
   - Slow: Calcium dynamics (~100ms)
   - Very slow: BCM threshold adaptation (minutes-hours)

4. STABILITY THROUGH HOMEOSTASIS
   - BCM: sliding threshold prevents runaway potentiation
   - Oja: normalization prevents weight explosion
   - Synaptic scaling: maintains overall activity levels

5. BIOCHEMISTRY = COMPUTATION
   - Calcium concentration acts as a multi-purpose signal
   - Nonlinear thresholds create discrete learning modes
   - NMDA receptors = molecular AND gates (coincidence detectors)

6. UNSUPERVISED ≠ USELESS
   - Biology builds sophisticated representations without labels
   - Visual cortex, hippocampus, cerebellum all use unsupervised learning
   - Supervised learning is evolutionarily recent (language, etc.)
    """)
    print("="*80)

    print("\n✓ Analysis complete!")
    print("✓ Generated 3 plots:")
    print("  - stdp_window.png")
    print("  - calcium_plasticity.png")
    print("  - bcm_rule.png")


if __name__ == "__main__":
    main()
