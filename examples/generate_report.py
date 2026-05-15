#!/usr/bin/env python3
"""Generate Neural PDE simulation report"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.control.neural_pde_solver import NeuralPDESolver
from swarmica.reporting import NeuralPDEReportGenerator


def main():
    print("=" * 60)
    print("📊 SWARMICA v4.0 - Neural PDE Report Generator Demo")
    print("=" * 60)
    
    # Create solver
    solver = NeuralPDESolver(n=40, alpha=1.0, beta=0.25, noise=0.05, energy_lr=0.001)
    
    print("\nRunning Neural PDE simulation...")
    solver.run(steps=80)
    
    # Generate report
    report_gen = NeuralPDEReportGenerator()
    report = report_gen.generate_from_solver(solver)
    
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
