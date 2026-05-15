#!/usr/bin/env python3
"""Generate PDE simulation report example"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.pde.solver import PDESolver
from swarmica.reporting import PDEReportGenerator


def main():
    print("=" * 60)
    print("📊 SWARMICA v3.0 - PDE Report Generator Demo")
    print("=" * 60)
    
    # Create solver
    solver = PDESolver(n=40, alpha=1.0, beta=0.2, noise=0.05)
    
    print("\nRunning PDE simulation...")
    solver.run(steps=100)
    
    # Generate report
    report_gen = PDEReportGenerator()
    report = report_gen.generate_from_solver(solver)
    
    # Print summary
    report_gen.print_summary(report)
    
    # Save reports
    print("\nSaving reports...")
    report_gen.save_json(report)
    report_gen.save_markdown(report)
    
    print("\n✅ Reports generated successfully!")
    print("   Check the 'reports/' directory")


if __name__ == "__main__":
    main()
