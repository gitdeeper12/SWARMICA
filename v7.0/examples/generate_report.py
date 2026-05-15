#!/usr/bin/env python3
"""Generate Continuous Control simulation report"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.control.continuous_controller import ContinuousController
from swarmica.reporting import ContinuousControlReportGenerator


def main():
    print("=" * 60)
    print("📊 SWARMICA v7.0 - Continuous Control Report Generator")
    print("=" * 60)
    
    controller = ContinuousController(n=50, beta=0.3, sigma=0.1, K_gain=1.2, lambda_reg=0.5)
    
    print("\nRunning continuous PDE simulation...")
    controller.run(steps=100)
    
    report_gen = ContinuousControlReportGenerator()
    report = report_gen.generate_from_controller(controller)
    
    report_gen.print_summary(report)
    
    print("\nSaving reports...")
    report_gen.save_json(report)
    report_gen.save_markdown(report)
    report_gen.save_csv(report)
    
    print("\n✅ Reports generated successfully!")

if __name__ == "__main__":
    main()
