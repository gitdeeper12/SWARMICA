#!/usr/bin/env python3
"""Advanced demo with metrics and learning"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.pde.neural_solver import NeuralPDESolver
from swarmica.metrics import MetricsCalculator
from swarmica.learning import PhysicsDiscovery


def main():
    print("=" * 60)
    print("🧠 SWARMICA v10.0 - Advanced Demo (Metrics + Learning)")
    print("=" * 60)
    
    # Initialize components
    solver = NeuralPDESolver(N=50, nu=0.2, gamma=0.3, learning=True)
    metrics = MetricsCalculator(N=50)
    physics_discovery = PhysicsDiscovery(N=50)
    
    print("\nRunning simulation with physics discovery...")
    print("-" * 40)
    
    for step in range(200):
        result = solver.step()
        
        # Record trajectory for physics discovery
        physics_discovery.record_trajectory(solver.rho, step)
        
        # Compute advanced metrics every 50 steps
        if (step + 1) % 50 == 0:
            all_metrics = metrics.get_all_metrics(
                solver.rho, solver.vx, solver.vy,
                solver.energy_model.get_parameters()
            )
            print(f"\nStep {step+1}:")
            print(f"  Coherence: {all_metrics['coherence']:.4f}")
            print(f"  Entropy: {all_metrics['entropy']:.4f}")
            print(f"  Kinetic Energy: {all_metrics['kinetic_energy']:.4f}")
            print(f"  Potential Energy: {all_metrics['potential_energy']:.4f}")
            print(f"  Total Energy: {all_metrics['total_energy']:.4f}")
    
    # Discover physics from trajectories
    print("\n" + "=" * 40)
    print("🔬 Physics Discovery Results:")
    print("=" * 40)
    
    discovery = physics_discovery.discover_physics(target_stability=0.8)
    print(f"  Status: {discovery['status']}")
    print(f"  Discovered Law: {discovery['discovered_law']}")
    print(f"  Entropy Trend: {discovery['entropy_trend']:+.4f}")
    print(f"  Trajectories Analyzed: {discovery['trajectories_analyzed']}")
    
    print("\n✅ SWARMICA v10.0 advanced demo complete!")


if __name__ == "__main__":
    main()
