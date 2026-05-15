#!/usr/bin/env python3
"""Generate Variational Control simulation report"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.control.variational_controller import VariationalController
from swarmica.reporting import VariationalReportGenerator


def main():
    print("=" * 60)
    print("📊 SWARMICA v5.0 - Variational Control Report Generator")
    print("=" * 60)
    
    # Create controller
    controller = VariationalController(n=40, alpha=1.2, beta=0.3, sigma=0.08, control_gain=0.6)
    
    print("\nRunning Variational Control simulation...")
    controller.run(steps=80)
    
    # Generate report
    report_gen = VariationalReportGenerator()
    report = report_gen.generate_from_controller(controller)
    
    # Print summary
    report_gen.print_summary(report)
    
    # Save reports
    print("\nSaving reports...")
    report_gen.save_json(report)
    report_gen.save_markdown(report)
    report_gen.save_csv(report)
    
    print("\n✅ Reports generated successfully!")
    print("   Check the 'reports/' directory")


if __name__ == "__main__":
    main()
