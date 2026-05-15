#!/usr/bin/env python3
"""SWARMICA v3.0 - CLI Demo (PDE Solver)"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.pde.solver import PDESolver

def main():
    print("=" * 60)
    print("🧠 SWARMICA v3.0 - PDE Swarm Physics Engine")
    print("=" * 60)
    
    # Create solver
    solver = PDESolver(n=50, alpha=1.0, beta=0.2, noise=0.05)
    
    print(f"Grid size: {solver.n}x{solver.n}")
    print(f"Time step: dt={solver.dt}")
    print()
    
    print("Running PDE simulation...")
    print("-" * 40)
    
    for step in range(100):
        result = solver.step()
        if (step + 1) % 20 == 0:
            print(f"Step {step+1:3d}: Energy={result['energy']:.4f}, Total Density={result['total_density']:.2f}")
    
    print("-" * 40)
    print()
    print("📊 Final Results:")
    print(f"  Final Energy:     {solver.history['energy'][-1]:.4f}")
    print(f"  Initial Energy:   {solver.history['energy'][0]:.4f}")
    
    reduction = (solver.history['energy'][0] - solver.history['energy'][-1]) / solver.history['energy'][0] * 100
    print(f"  Energy Reduction: {reduction:.1f}%")
    
    print()
    print("✅ SWARMICA v3.0 simulation complete!")

if __name__ == "__main__":
    main()
