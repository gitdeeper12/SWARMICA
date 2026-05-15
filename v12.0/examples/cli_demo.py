#!/usr/bin/env python3
"""SWARMICA v12.0 - CLI Demo (Constrained Physics)"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.solver.constrained_solver import ConstrainedNeuralSolver

def main():
    print("=" * 60)
    print("🔬 SWARMICA v12.0 - Constrained Neural Physics Discovery")
    print("=" * 60)
    
    solver = ConstrainedNeuralSolver(N=50, learning=True)
    
    print(f"Grid: {solver.N}x{solver.N}")
    print("Constraints: Mass Conservation | Symplectic Structure | Entropy dS/dt ≥ 0")
    print()
    print("Running constrained Hamiltonian simulation...")
    print("-" * 40)
    
    for step in range(200):
        result = solver.step()
        if (step + 1) % 50 == 0:
            print(f"Step {step+1:3d}: Energy={result['energy']:.4f}, Mass={result['mass']:.4f}, Coherence={result['coherence']:.4f}")
    
    print("-" * 40)
    print()
    print("📊 Conservation Report:")
    cons = solver.get_conservation_report()
    print(f"  Mass Conserved: {cons['mass_conserved']}")
    print(f"  Energy Variation: {cons['energy_variation']:.6f}")
    print(f"  Symplectic Structure: {cons['symplectic_structure']}")
    
    print()
    print("✅ SWARMICA v12.0 complete!")

if __name__ == "__main__":
    main()
