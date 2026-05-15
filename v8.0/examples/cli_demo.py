#!/usr/bin/env python3
"""SWARMICA v8.0 - CLI Demo (Unified Field Control)"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.core.engine import SwarmicaV8

def main():
    print("=" * 60)
    print("⚙️ SWARMICA v8.0 - Unified Field Control Engine")
    print("=" * 60)
    
    sim = SwarmicaV8(n_agents=100, alpha=1.2, beta=2.0, gamma=0.5, sigma=0.1)
    
    print(f"Agents: {sim.n_agents}")
    print(f"Attractors: {sim.attractors}")
    print()
    print("Running simulation...")
    print("-" * 40)
    
    for step in range(500):
        result = sim.step()
        if (step + 1) % 100 == 0:
            print(f"Step {step+1:3d}: CSI={result['csi']:.4f}, Entropy={result['entropy']:.4f}, Lyapunov={result['lyapunov']:.4f}")
    
    print("-" * 40)
    print()
    print("📊 Final Results:")
    
    summary = sim.get_summary()
    print(f"  Final CSI: {summary['final_csi']:.4f}")
    print(f"  Initial CSI: {summary['initial_csi']:.4f}")
    print(f"  CSI Improvement: {summary['csi_improvement']:+.1f}%")
    print(f"  Entropy Reduction: {summary['entropy_reduction']:.1f}%")
    
    print()
    print("✅ SWARMICA v8.0 complete!")

if __name__ == "__main__":
    main()
