#!/usr/bin/env python3
"""Generate Optimal Control simulation report"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.control.optimal_swarm_controller import OptimalSwarmController
from swarmica.reporting import OptimalControlReportGenerator


def main():
    print("=" * 60)
    print("📊 SWARMICA v6.0 - Optimal Control Report Generator")
    print("=" * 60)
    
    controller = OptimalSwarmController(n=40, alpha=1.0, beta=0.25, sigma=0.1,
                                         control_weight=0.8, adjoint_lr=0.002)
    
    print("\nRunning optimal control simulation...")
    controller.run(steps=100)
    
    report_gen = OptimalControlReportGenerator()
    report = report_gen.generate_from_controller(controller)
    
    report_gen.print_summary(report)
    
    print("\nSaving reports...")
    report_gen.save_json(report)
    report_gen.save_markdown(report)
    report_gen.save_csv(report)
    
    print("\n✅ Reports generated successfully!")

if __name__ == "__main__":
    main()
