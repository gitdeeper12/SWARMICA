#!/usr/bin/env python3
"""Generate simulation report example"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.control.swarm_controller import SwarmControllerV2
from swarmica.report_generator import ReportGenerator


def main():
    print("=" * 60)
    print("📊 SWARMICA v2.0 - Report Generator Demo")
    print("=" * 60)
    
    # Create controller
    controller = SwarmControllerV2(
        n_agents=80,
        alpha=0.8,
        beta=1.2,
        noise=0.2,
        inertia=0.85
    )
    
    print("\nRunning simulation...")
    controller.run(steps=200)
    
    # Generate report
    report_gen = ReportGenerator()
    config = {
        'n_agents': controller.n_agents,
        'grid_size': controller.grid_size,
        'alpha': controller.alpha,
        'beta': controller.beta,
        'noise': controller.noise,
        'inertia': controller.inertia,
        'dt': controller.dt
    }
    
    report = report_gen.generate_from_controller(controller, config)
    
    # Print summary
    report_gen.print_summary(report)
    
    # Save reports
    print("\nSaving reports...")
    report_gen.save_json(report)
    report_gen.save_markdown(report)
    report_gen.save_csv(report)
    
    print("\n✅ All reports generated successfully!")
    print("   Check the 'reports/' directory")


if __name__ == "__main__":
    main()
