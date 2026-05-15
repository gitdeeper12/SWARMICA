#!/usr/bin/env python3
"""Quick start example - 50-agent aerial formation"""

import sys
sys.path.insert(0, '.')

from swarmica import SwarmEngine, SwarmConfig

print("🐝 SWARMICA Quick Start Example")
print("=" * 50)

# Configure swarm
config = SwarmConfig(
    n_agents=50,
    modality='aerial',
    n_basis=32,
    k_coupling=3.0,
    mu_dissipation=0.02,
    target_config='diamond_V'
)

print(f"Config: {config.n_agents} agents, {config.modality} mode")

# Create engine
engine = SwarmEngine(config)

# Run control loop
print("\nRunning control loop...")
for step in range(500):
    control = engine.step()
    if step % 100 == 0:
        csi = engine.get_csi()
        entropy = engine.get_structural_entropy()
        print(f"  Step {step:4d}: CSI={csi:.4f}, Entropy={entropy:.4f}")

print(f"\n✅ Done!")
print(f"  Final CSI: {engine.get_csi():.4f}")
print(f"  ERI: {engine.get_eri():.4f}")
