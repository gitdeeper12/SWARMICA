#!/usr/bin/env python3
"""SWARMICA v7.0 - CLI Demo (Continuous Control)"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.control.continuous_controller import ContinuousController

def main():
    print("=" * 60)
    print("🔬 SWARMICA v7.0 - Continuous Neural Control PDE System")
    print("=" * 60)
    
    controller = ContinuousController(n=60, beta=0.3, sigma=0.1, K_gain=1.2, lambda_reg=0.5)
    
    print(f"Grid: {controller.n}x{controller.n}")
    print(f"Control gain K: {controller.K_gain}")
    print(f"Diffusion β: {controller.beta}")
    print()
    print("Running continuous PDE simulation...")
    print("-" * 40)
    
    for step in range(100):
        result = controller.step()
        if (step + 1) % 20 == 0:
            print(f"Step {step+1:3d}: Energy={result['energy']:.4f}, Stability={result['stability_metric']:.4f}")
    
    print("-" * 40)
    print()
    print("📊 Final Results:")
    print(f"  Final Energy: {controller.history['energy'][-1]:.4f}")
    print(f"  Initial Energy: {controller.history['energy'][0]:.4f}")
    
    reduction = (controller.history['energy'][0] - controller.history['energy'][-1]) / controller.history['energy'][0] * 100
    print(f"  Energy Reduction: {reduction:.1f}%")
    
    cert = controller.get_stability_certificate()
    print(f"  Stability Certified: {cert['certified']}")
    print(f"  Lyapunov Decay: {cert['lyapunov_decay']:.2%}")
    
    print()
    print("✅ SWARMICA v7.0 complete!")

if __name__ == "__main__":
    main()
