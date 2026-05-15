#!/usr/bin/env python3
"""SWARMICA v9.0 - CLI Demo (Continuum PDE)"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.pde.solver import ContinuumPDESolver

def main():
    print("=" * 60)
    print("🔬 SWARMICA v9.0 - Continuum PDE Swarm System")
    print("=" * 60)
    
    solver = ContinuumPDESolver(N=80, alpha=1.0, gamma=0.3, nu=0.2, dt=0.01)
    
    print(f"Grid: {solver.N}x{solver.N}")
    print(f"Gradient energy α: {solver.alpha}")
    print(f"Damping γ: {solver.gamma}")
    print(f"Viscosity ν: {solver.nu}")
    print()
    print("Running PDE simulation...")
    print("-" * 40)
    
    for step in range(200):
        result = solver.step()
        if (step + 1) % 50 == 0:
            print(f"Step {step+1:3d}: Coherence={result['coherence']:.4f}, Entropy={result['entropy']:.4f}, Energy={result['energy']:.4f}")
    
    print("-" * 40)
    print()
    print("📊 Final Results:")
    print(f"  Final Coherence: {solver.history['coherence'][-1]:.4f}")
    print(f"  Final Entropy: {solver.history['entropy'][-1]:.4f}")
    print(f"  Final Energy: {solver.history['energy'][-1]:.4f}")
    
    print()
    print("✅ SWARMICA v9.0 complete!")

if __name__ == "__main__":
    main()
