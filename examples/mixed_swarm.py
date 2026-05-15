#!/usr/bin/env python3
"""Mixed modality swarm example"""

import sys
sys.path.insert(0, '.')

from swarmica import SwarmEngine, SwarmConfig

print("🔄 SWARMICA Mixed Modality Example")
print("=" * 50)

config = SwarmConfig(
    n_agents=80,
    modality='mixed',
    n_basis=32,
    k_coupling=3.0,
    mu_dissipation=0.03,
    target_config='mixed_cluster'
)

engine = SwarmEngine(config)

print("\nCoordinating aerial + ground agents...")
for step in range(400):
    control = engine.step()
    if step % 100 == 0:
        csi = engine.get_csi()
        print(f"  Step {step:3d}: CSI={csi:.4f}")

print(f"\n✅ Mixed swarm stable! Final CSI: {engine.get_csi():.4f}")
