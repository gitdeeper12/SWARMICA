#!/usr/bin/env python3
"""SWARMICA v5.0 - CLI Demo (Variational Control)"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.control.variational_controller import VariationalController

def main():
    print("=" * 60)
    print("🎮 SWARMICA v5.0 - Variational Swarm Control System")
    print("=" * 60)
    
    controller = VariationalController(n=40, alpha=1.2, beta=0.3, sigma=0.08, control_gain=0.6)
    
    print(f"Grid: {controller.n}x{controller.n}")
    print(f"Control gain λ: {controller.control_gain}")
    print()
    print("Running variational control simulation...")
    print("-" * 40)
    
    for step in range(80):
        result = controller.step()
        if (step + 1) % 20 == 0:
            print(f"Step {step+1:3d}: Total Cost={result['total_cost']:.4f}, Energy={result['energy']:.4f}")
    
    print("-" * 40)
    print()
    print("📊 Final Results:")
    print(f"  Final Total Cost: {controller.history['total_cost'][-1]:.4f}")
    print(f"  Initial Total Cost: {controller.history['total_cost'][0]:.4f}")
    
    reduction = (controller.history['total_cost'][0] - controller.history['total_cost'][-1]) / controller.history['total_cost'][0] * 100
    print(f"  Cost Reduction: {reduction:.1f}%")
    
    print()
    print("✅ SWARMICA v5.0 complete!")

if __name__ == "__main__":
    main()
