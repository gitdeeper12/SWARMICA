#!/usr/bin/env python3
"""SWARMICA CLI - run validation scenarios"""

import sys
import argparse
sys.path.insert(0, '.')

from swarmica.control.swarm_engine import SwarmEngine, SwarmConfig


def main():
    parser = argparse.ArgumentParser(description='SWARMICA CLI')
    parser.add_argument('--scenario', type=str, default='S1', help='Scenario: S1, S2, S3, S4')
    parser.add_argument('--n-agents', type=int, default=100, help='Number of agents')
    parser.add_argument('--modality', type=str, default='aerial', help='aerial/ground/underwater/mixed')
    parser.add_argument('--steps', type=int, default=1000, help='Number of control steps')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    config = SwarmConfig(
        n_agents=args.n_agents,
        modality=args.modality,
        target_config='diamond_V' if args.modality == 'aerial' else 'convoy_line'
    )
    
    engine = SwarmEngine(config)
    
    print(f"Running SWARMICA scenario {args.scenario}")
    print(f"  Agents: {args.n_agents}")
    print(f"  Modality: {args.modality}")
    print(f"  Steps: {args.steps}")
    
    for step in range(args.steps):
        control = engine.step()
        if args.verbose and step % 100 == 0:
            csi = engine.get_csi()
            entropy = engine.get_structural_entropy()
            print(f"  Step {step}: CSI={csi:.4f}, Entropy={entropy:.4f}")
    
    print(f"\nFinal Results:")
    print(f"  Final CSI: {engine.get_csi():.4f}")
    print(f"  Entropy Reduction Index: {engine.get_eri():.4f}")
    print(f"  Final Structural Entropy: {engine.get_structural_entropy():.4f}")


if __name__ == '__main__':
    main()
