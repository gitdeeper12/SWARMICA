#!/usr/bin/env python3
"""SWARMICA v6.0 - CLI Demo (Optimal Control)"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.control.optimal_swarm_controller import OptimalSwarmController

def main():
    print("=" * 60)
    print("🎯 SWARMICA v6.0 - Optimal Control Swarm System")
    print("=" * 60)
    
    controller = OptimalSwarmController(n=50, alpha=1.0, beta=0.25, sigma=0.1, 
                                         control_weight=0.8, adjoint_lr=0.002)
    
    print(f"Grid: {controller.n}x{controller.n}")
    print(f"Control penalty λ: {controller.control_weight}")
    print()
    print("Running optimal control simulation...")
    print("-" * 40)
    
    for step in range(100):
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
    print(f"  Optimality Gap: {controller.get_optimality_gap():.4f}")
    
    print()
    print("✅ SWARMICA v6.0 complete!")

if __name__ == "__main__":
    main()
