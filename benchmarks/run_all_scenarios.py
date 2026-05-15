#!/usr/bin/env python3
"""Run all validation scenarios"""

import sys
import time
import argparse
sys.path.insert(0, '.')

from swarmica import SwarmEngine, SwarmConfig


def run_scenario_s1(n_agents=500, steps=2000):
    """S1: Aerial formation diamond-V"""
    print(f"\n📍 S1: Aerial Formation (N={n_agents})")
    config = SwarmConfig(
        n_agents=n_agents,
        modality='aerial',
        target_config='diamond_V',
        mu_dissipation=0.02
    )
    engine = SwarmEngine(config)
    
    start = time.time()
    for step in range(steps):
        control = engine.step()
    elapsed = time.time() - start
    
    csi = engine.get_csi()
    eri = engine.get_eri()
    print(f"   CSI: {csi:.4f} | ERI: {eri:.4f} | Time: {elapsed:.2f}s")
    return csi, eri


def run_scenario_s2(n_agents=200, steps=2000):
    """S2: Ground convoy through obstacle field"""
    print(f"\n📍 S2: Ground Convoy (N={n_agents})")
    config = SwarmConfig(
        n_agents=n_agents,
        modality='ground',
        target_config='convoy_line',
        mu_dissipation=0.08
    )
    engine = SwarmEngine(config)
    
    start = time.time()
    for step in range(steps):
        control = engine.step()
    elapsed = time.time() - start
    
    csi = engine.get_csi()
    eri = engine.get_eri()
    print(f"   CSI: {csi:.4f} | ERI: {eri:.4f} | Time: {elapsed:.2f}s")
    return csi, eri


def run_scenario_s3(n_agents=300, steps=2000):
    """S3: Underwater school with current disturbance"""
    print(f"\n📍 S3: Underwater School (N={n_agents})")
    config = SwarmConfig(
        n_agents=n_agents,
        modality='underwater',
        target_config='school_sphere',
        mu_dissipation=0.05
    )
    engine = SwarmEngine(config)
    
    start = time.time()
    for step in range(steps):
        control = engine.step()
    elapsed = time.time() - start
    
    csi = engine.get_csi()
    eri = engine.get_eri()
    print(f"   CSI: {csi:.4f} | ERI: {eri:.4f} | Time: {elapsed:.2f}s")
    return csi, eri


def run_scenario_s4(n_agents=150, steps=2000):
    """S4: Mixed modality swarm"""
    print(f"\n📍 S4: Mixed Modality Swarm (N={n_agents})")
    config = SwarmConfig(
        n_agents=n_agents,
        modality='mixed',
        target_config='mixed_cluster',
        mu_dissipation=0.03
    )
    engine = SwarmEngine(config)
    
    start = time.time()
    for step in range(steps):
        control = engine.step()
    elapsed = time.time() - start
    
    csi = engine.get_csi()
    eri = engine.get_eri()
    print(f"   CSI: {csi:.4f} | ERI: {eri:.4f} | Time: {elapsed:.2f}s")
    return csi, eri


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scenarios', type=str, default='S1,S2,S3,S4')
    parser.add_argument('--n-monte-carlo', type=int, default=5)
    args = parser.parse_args()
    
    scenarios = args.scenarios.split(',')
    results = {}
    
    print("=" * 60)
    print("🐝 SWARMICA Validation Suite")
    print("=" * 60)
    
    for scenario in scenarios:
        csi_sum = 0
        eri_sum = 0
        for run in range(args.n_monte_carlo):
            if scenario == 'S1':
                csi, eri = run_scenario_s1(steps=1000)
            elif scenario == 'S2':
                csi, eri = run_scenario_s2(steps=1000)
            elif scenario == 'S3':
                csi, eri = run_scenario_s3(steps=1000)
            elif scenario == 'S4':
                csi, eri = run_scenario_s4(steps=1000)
            else:
                continue
            csi_sum += csi
            eri_sum += eri
        
        results[scenario] = {
            'csi_mean': csi_sum / args.n_monte_carlo,
            'eri_mean': eri_sum / args.n_monte_carlo
        }
    
    print("\n" + "=" * 60)
    print("📊 Summary Results")
    print("=" * 60)
    for scenario, res in results.items():
        print(f"{scenario}: CSI={res['csi_mean']:.4f} | ERI={res['eri_mean']:.4f}")


if __name__ == '__main__':
    main()
