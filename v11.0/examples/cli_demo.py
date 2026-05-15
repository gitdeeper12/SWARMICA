#!/usr/bin/env python3
"""SWARMICA v11.0 - CLI Demo (Neural Operator)"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.integrator.solver import NeuralOperatorSolver

def main():
    print("=" * 60)
    print("🧠 SWARMICA v11.0 - Neural Operator Swarm Physics")
    print("=" * 60)
    
    solver = NeuralOperatorSolver(N=50, learning=True)
    
    print(f"Grid: {solver.N}x{solver.N}")
    print(f"Operator Learning: {solver.learning}")
    print()
    print("Running neural operator simulation (learning physics)...")
    print("-" * 40)
    
    for step in range(200):
        result = solver.step()
        if (step + 1) % 50 == 0:
            print(f"Step {step+1:3d}: Coherence={result['coherence']:.4f}, Loss={result['operator_loss']:.4f}")
    
    print("-" * 40)
    print()
    print("📊 Final Results:")
    print(f"  Final Coherence: {solver.history['coherence'][-1]:.4f}")
    print(f"  Final Entropy: {solver.history['entropy'][-1]:.4f}")
    print(f"  Operator Norm: {solver.get_operator_info()['operator_norm']:.4f}")
    
    print()
    print("✅ SWARMICA v11.0 complete!")

if __name__ == "__main__":
    main()
