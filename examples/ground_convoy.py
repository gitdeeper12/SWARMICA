#!/usr/bin/env python3
"""Ground convoy through obstacle field example"""

import sys
sys.path.insert(0, '.')

from swarmica import SwarmEngine, SwarmConfig

print("🚚 SWARMICA Ground Convoy Example")
print("=" * 50)

config = SwarmConfig(
    n_agents=100,
    modality='ground',
    n_basis=32,
    k_coupling=3.0,
    mu_dissipation=0.08,
    target_config='convoy_line'
)

engine = SwarmEngine(config)

print("\nNavigating obstacle field...")
for step in range(300):
    control = engine.step()
    if step % 50 == 0:
        csi = engine.get_csi()
        print(f"  Step {step:3d}: CSI={csi:.4f}")

print(f"\n✅ Convoy formed! Final CSI: {engine.get_csi():.4f}")
