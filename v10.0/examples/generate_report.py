#!/usr/bin/env python3
"""Generate Neural Physics simulation report"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.pde.neural_solver import NeuralPDESolver
from swarmica.reporting import NeuralPhysicsReportGenerator


def main():
    print("=" * 60)
    print("📊 SWARMICA v10.0 - Neural Physics Report Generator")
    print("=" * 60)
    
    solver = NeuralPDESolver(N=50, nu=0.2, gamma=0.3, learning=True)
    
    print("\nRunning neural physics simulation...")
    solver.run(steps=200)
    
    report_gen = NeuralPhysicsReportGenerator()
    report = report_gen.generate_from_solver(solver)
    
    report_gen.print_summary(report)
    
    print("\nSaving reports...")
    report_gen.save_json(report)
    report_gen.save_markdown(report)
    report_gen.save_csv(report)
    
    print("\n✅ Reports generated successfully!")

if __name__ == "__main__":
    main()
