#!/usr/bin/env python3
"""Generate PDE simulation report"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.pde.solver import ContinuumPDESolver
from swarmica.reporting import PDEReportGenerator


def main():
    print("=" * 60)
    print("📊 SWARMICA v9.0 - PDE Report Generator Demo")
    print("=" * 60)
    
    solver = ContinuumPDESolver(N=60, alpha=1.0, gamma=0.3, nu=0.2)
    
    print("\nRunning PDE simulation...")
    solver.run(steps=200)
    
    report_gen = PDEReportGenerator()
    report = report_gen.generate_from_solver(solver)
    
    report_gen.print_summary(report)
    
    print("\nSaving reports...")
    report_gen.save_json(report)
    report_gen.save_markdown(report)
    report_gen.save_csv(report)
    
    print("\n✅ Reports generated successfully!")

if __name__ == "__main__":
    main()
