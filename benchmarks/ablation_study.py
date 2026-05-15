#!/usr/bin/env python3
"""Ablation study - compare full SWARMICA vs components"""

import sys
sys.path.insert(0, '.')

from swarmica import SwarmEngine, SwarmConfig


def run_full_swarmica(n_agents=100, steps=1000):
    """Full SWARMICA with CLO + EPFE + KPSL"""
    config = SwarmConfig(n_agents=n_agents, modality='aerial')
    engine = SwarmEngine(config)
    for _ in range(steps):
        engine.step()
    return engine.get_csi(), engine.get_eri()


def run_no_epfe(n_agents=100, steps=1000):
    """Without EPFE (random potential)"""
    config = SwarmConfig(n_agents=n_agents, modality='aerial')
    engine = SwarmEngine(config)
    # Override potential force to be random
    engine._compute_potential_force = lambda: [v * 0.1 for v in engine._q]
    for _ in range(steps):
        engine.step()
    return engine.get_csi(), engine.get_eri()


def run_no_kpsl(n_agents=100, steps=1000):
    """Without KPSL (no phase synchronization)"""
    config = SwarmConfig(n_agents=n_agents, modality='aerial')
    engine = SwarmEngine(config)
    # Reduce coupling to simulate no KPSL
    config.k_coupling = 0.1
    for _ in range(steps):
        engine.step()
    return engine.get_csi(), engine.get_eri()


def main():
    print("=" * 60)
    print("🔬 SWARMICA Ablation Study")
    print("=" * 60)
    
    print("\nRunning Full SWARMICA...")
    csi_full, eri_full = run_full_swarmica()
    
    print("\nRunning Without EPFE...")
    csi_no_epfe, eri_no_epfe = run_no_epfe()
    
    print("\nRunning Without KPSL...")
    csi_no_kpsl, eri_no_kpsl = run_no_kpsl()
    
    print("\n" + "=" * 60)
    print("📊 Ablation Results")
    print("=" * 60)
    print(f"Full SWARMICA:     CSI={csi_full:.4f} | ERI={eri_full:.4f}")
    print(f"Without EPFE:      CSI={csi_no_epfe:.4f} | ERI={eri_no_epfe:.4f}")
    print(f"Without KPSL:      CSI={csi_no_kpsl:.4f} | ERI={eri_no_kpsl:.4f}")
    print(f"\nEPFE contribution:  +{(csi_full - csi_no_epfe)*100:.1f} pp")
    print(f"KPSL contribution: +{(csi_full - csi_no_kpsl)*100:.1f} pp")


if __name__ == '__main__':
    main()
