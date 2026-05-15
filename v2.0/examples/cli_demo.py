#!/usr/bin/env python3
"""SWARMICA v2.0 - CLI Demo (No Streamlit)"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.control.swarm_controller import SwarmControllerV2

def main():
    print("=" * 60)
    print("🐝 SWARMICA v2.0 - CLI Demo")
    print("=" * 60)
    
    # Create controller
    controller = SwarmControllerV2(n_agents=80, alpha=0.8, beta=1.2, noise=0.2)
    
    print(f"Agents: {controller.n_agents}")
    print(f"Grid size: {controller.grid_size}x{controller.grid_size}")
    print(f"Attractors: A1={controller.A1}, A2={controller.A2}")
    print()
    
    print("Running simulation...")
    print("-" * 40)
    
    for step in range(100):
        result = controller.step()
        if (step + 1) % 20 == 0:
            print(f"Step {step+1:3d}: CSI={result['csi']:.4f}, Entropy={result['entropy']:.4f}")
    
    print("-" * 40)
    print()
    print("📊 Final Results:")
    print(f"  Final CSI:      {controller.history['csi'][-1]:.4f}")
    print(f"  Final Entropy:  {controller.history['entropy'][-1]:.4f}")
    print(f"  CSI Improvement: {(controller.history['csi'][-1] - controller.history['csi'][0])*100:+.1f}%")
    
    print()
    print("✅ SWARMICA v2.0 simulation complete!")

if __name__ == "__main__":
    main()
