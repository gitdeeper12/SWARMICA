#!/usr/bin/env python3
"""SWARMICA v4.0 - CLI Demo (Neural PDE)"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.control.neural_pde_solver import NeuralPDESolver

def main():
    print("=" * 60)
    print("🧠 SWARMICA v4.0 - Neural PDE Swarm Engine")
    print("=" * 60)
    
    solver = NeuralPDESolver(n=50, alpha=1.0, beta=0.25, noise=0.05, energy_lr=0.001)
    
    print(f"Grid: {solver.n}x{solver.n}")
    print()
    print("Running neural PDE simulation...")
    print("-" * 40)
    
    for step in range(80):
        result = solver.step()
        if (step + 1) % 20 == 0:
            print(f"Step {step+1:3d}: Energy={result['energy']:.4f}, Order={result['order_parameter']:.4f}, Phase={result['phase']}")
    
    print("-" * 40)
    print()
    print("📊 Phase Analysis:")
    report = solver.get_phase_report()
    print(f"  Final Phase: {report.get('current_phase', 'N/A')}")
    print(f"  Order Parameter: {report.get('current_order_parameter', 0):.4f}")
    print(f"  Phase Transition: {report.get('phase_transition_detected', False)}")
    
    print()
    print("✅ SWARMICA v4.0 complete!")

if __name__ == "__main__":
    main()
