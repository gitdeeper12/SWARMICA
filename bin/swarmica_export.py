#!/usr/bin/env python3
"""Export SWARMICA model for deployment"""

import sys
import json
import pickle
sys.path.insert(0, '.')

from swarmica import SwarmEngine, SwarmConfig


def export_weights(output_path='swarmica_weights.pkl'):
    """Export model weights to pickle file"""
    print(f"📦 Exporting weights to {output_path}")
    
    config = SwarmConfig(n_agents=100, modality='aerial')
    engine = SwarmEngine(config)
    
    weights = {
        'version': '1.0.0',
        'n_basis': config.n_basis,
        'alpha': config.alpha,
        'k_coupling': config.k_coupling,
        'mu': config.mu_dissipation,
        'target_config': config.target_config
    }
    
    with open(output_path, 'wb') as f:
        pickle.dump(weights, f)
    
    print(f"✅ Exported {len(weights)} parameters")
    return weights


def export_config(output_path='swarmica_config.json'):
    """Export configuration to JSON"""
    print(f"📦 Exporting config to {output_path}")
    
    config = SwarmConfig()
    config_dict = {
        'n_agents': config.n_agents,
        'modality': config.modality,
        'n_basis': config.n_basis,
        'k_coupling': config.k_coupling,
        'mu_dissipation': config.mu_dissipation,
        'target_config': config.target_config,
        'sos_degree': config.sos_degree,
        'dt': config.dt,
        'alpha': config.alpha
    }
    
    with open(output_path, 'w') as f:
        json.dump(config_dict, f, indent=2)
    
    print(f"✅ Exported config to {output_path}")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, default='swarmica_weights.pkl')
    parser.add_argument('--format', type=str, choices=['pickle', 'json'], default='pickle')
    args = parser.parse_args()
    
    if args.format == 'json':
        export_config()
    else:
        export_weights(args.output)


if __name__ == '__main__':
    main()
