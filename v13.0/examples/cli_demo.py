#!/usr/bin/env python3
"""SWARMICA v13.0 - CLI Demo (Physical Law Discovery)"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.core.discovery_engine import DiscoveryEngine

def main():
    print("=" * 60)
    print("🔬 SWARMICA v13.0 - Autonomous Physical Law Discovery")
    print("=" * 60)
    
    engine = DiscoveryEngine(N=50, alpha=0.001)
    
    print(f"Grid: {engine.N}x{engine.N}")
    print(f"Sparsity parameter α: {engine.alpha}")
    print()
    print("Observing field dynamics and discovering PDE...")
    print("-" * 40)
    
    results = engine.run_discovery(iterations=3)
    best = engine.get_best_pde(results)
    
    print("-" * 40)
    print()
    print("📜 Discovered Physical Law:")
    print(f"  {best.get('discovered_pde', 'No PDE discovered')}")
    print()
    print("📊 Coefficients:")
    for term, coeff in best.get('coefficients', {}).items():
        print(f"  {term}: {coeff:.4f}")
    print()
    print(f"  Number of terms: {best.get('num_terms', 0)}")
    print(f"  Sparsity: {best.get('sparsity', 0):.2%}")
    
    print()
    print("✅ SWARMICA v13.0 complete!")

if __name__ == "__main__":
    main()
