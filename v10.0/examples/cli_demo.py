#!/usr/bin/env python3
"""SWARMICA v10.0 - CLI Demo (Neural Physics)"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.pde.neural_solver import NeuralPDESolver

def main():
    print("=" * 60)
    print("🧠 SWARMICA v10.0 - Neural Field + Inverse Physics System")
    print("=" * 60)
    
    solver = NeuralPDESolver(N=60, nu=0.2, gamma=0.3, learning=True)
    
    print(f"Grid: {solver.N}x{solver.N}")
    print(f"Learning active: {solver.learning}")
    print()
    print("Running neural PDE simulation (learning physics)...")
    print("-" * 40)
    
    for step in range(200):
        result = solver.step()
        if (step + 1) % 50 == 0:
            print(f"Step {step+1:3d}: Coherence={result['coherence']:.4f}, Energy Loss={result['energy_loss']:.4f}")
    
    print("-" * 40)
    print()
    print("📊 Final Results:")
    print(f"  Final Coherence: {solver.history['coherence'][-1]:.4f}")
    print(f"  Final Entropy: {solver.history['entropy'][-1]:.4f}")
    print(f"  Final Energy Loss: {solver.history['energy_loss'][-1]:.4f}")
    
    print()
    print("✅ SWARMICA v10.0 complete - Physics learned!")

if __name__ == "__main__":
    main()
