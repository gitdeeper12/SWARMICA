#!/usr/bin/env python3
"""Benchmark SWARMICA performance"""

import sys
import time
sys.path.insert(0, '.')

from swarmica import SwarmEngine, SwarmConfig


def benchmark_agent_scaling():
    """Test CSI vs number of agents"""
    print("\n📈 Agent Scaling Benchmark")
    print("-" * 40)
    
    agent_counts = [10, 50, 100, 200, 500]
    results = []
    
    for n in agent_counts:
        config = SwarmConfig(n_agents=n, modality='aerial')
        engine = SwarmEngine(config)
        
        start = time.time()
        for _ in range(500):
            engine.step()
        elapsed = time.time() - start
        
        csi = engine.get_csi()
        results.append((n, csi, elapsed))
        print(f"  N={n:3d}: CSI={csi:.4f}, Time={elapsed:.2f}s")
    
    return results


def benchmark_convergence():
    """Test convergence speed"""
    print("\n⏱️ Convergence Benchmark")
    print("-" * 40)
    
    config = SwarmConfig(n_agents=100, modality='aerial')
    engine = SwarmEngine(config)
    
    csi_history = []
    for step in range(1000):
        engine.step()
        csi_history.append(engine.get_csi())
    
    # Find when CSI exceeds 0.9
    convergence_step = 0
    for i, csi in enumerate(csi_history):
        if csi > 0.9:
            convergence_step = i
            break
    
    print(f"  Convergence to CSI>0.9: {convergence_step} steps")
    print(f"  Final CSI: {csi_history[-1]:.4f}")
    return convergence_step, csi_history[-1]


def main():
    print("=" * 50)
    print("🏃 SWARMICA Benchmark Suite")
    print("=" * 50)
    
    benchmark_agent_scaling()
    benchmark_convergence()
    
    print("\n✅ Benchmark complete!")


if __name__ == '__main__':
    main()
