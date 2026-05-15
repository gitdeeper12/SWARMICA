#!/usr/bin/env python3
"""Generate Neural Operator simulation report"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.integrator.solver import NeuralOperatorSolver
from swarmica.reporting import NeuralOperatorReportGenerator


def main():
    print("=" * 60)
    print("📊 SWARMICA v11.0 - Neural Operator Report Generator")
    print("=" * 60)
    
    solver = NeuralOperatorSolver(N=50, learning=True)
    
    print("\nRunning neural operator simulation...")
    solver.run(steps=200)
    
    report_gen = NeuralOperatorReportGenerator()
    report = report_gen.generate_from_solver(solver)
    
    report_gen.print_summary(report)
    
    print("\nSaving reports...")
    report_gen.save_json(report)
    report_gen.save_markdown(report)
    report_gen.save_csv(report)
    
    print("\n✅ Reports generated successfully!")

if __name__ == "__main__":
    main()
