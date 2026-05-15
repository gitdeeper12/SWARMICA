#!/usr/bin/env python3
"""Advanced demo with metrics and operator learning"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.integrator.solver import NeuralOperatorSolver
from swarmica.metrics import MetricsCalculator
from swarmica.learning import PhysicsLawDiscovery


def main():
    print("=" * 60)
    print("🧠 SWARMICA v11.0 - Advanced Demo (Metrics + Law Discovery)")
    print("=" * 60)
    
    solver = NeuralOperatorSolver(N=50, learning=True)
    metrics = MetricsCalculator(N=50)
    law_discovery = PhysicsLawDiscovery(N=50)
    
    print("\nRunning neural operator simulation...")
    print("-" * 40)
    
    for step in range(200):
        result = solver.step()
        
        if (step + 1) % 50 == 0:
            # Compute advanced metrics
            all_metrics = metrics.get_all_metrics(
                solver.rho, solver.vx, solver.vy,
                solver.operator.W_real, solver.operator.W_imag,
                solver.history['operator_loss']
            )
            
            print(f"\nStep {step+1}:")
            print(f"  Coherence: {all_metrics['coherence']:.4f}")
            print(f"  Entropy: {all_metrics['entropy']:.4f}")
            print(f"  Operator Gain: {all_metrics['operator_gain']:.4f}")
            print(f"  Operator Stability: {all_metrics['operator_stability']}")
            
            if 'learning' in all_metrics:
                print(f"  Learning Status: {all_metrics['learning']['status']}")
    
    # Discover physical law
    print("\n" + "=" * 40)
    print("🔬 Physics Law Discovery Results:")
    print("=" * 40)
    
    W_real, W_imag = solver.operator.W_real, solver.operator.W_imag
    discovery = law_discovery.discover_law(W_real, W_imag)
    
    print(f"  Discovered Law: {discovery['discovered_law']}")
    print(f"  Law Equation: {discovery['law_equation']}")
    print(f"  System Behavior: {discovery['system_behavior']}")
    print(f"  Operator Complexity: {discovery['complexity']:.4f}")
    
    print("\n✅ SWARMICA v11.0 advanced demo complete!")


if __name__ == "__main__":
    main()
