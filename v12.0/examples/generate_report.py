#!/usr/bin/env python3
"""Generate Constrained Physics simulation report"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.solver.constrained_solver import ConstrainedNeuralSolver
from swarmica.reporting import ConstrainedPhysicsReportGenerator


def main():
    print("=" * 60)
    print("📊 SWARMICA v12.0 - Constrained Physics Report Generator")
    print("=" * 60)
    
    solver = ConstrainedNeuralSolver(N=40, learning=True)
    
    print("\nRunning constrained Hamiltonian simulation...")
    solver.run(steps=150)
    
    report_gen = ConstrainedPhysicsReportGenerator()
    report = report_gen.generate_from_solver(solver)
    
    report_gen.print_summary(report)
    
    print("\nSaving reports...")
    report_gen.save_json(report)
    report_gen.save_markdown(report)
    report_gen.save_csv(report)
    
    print("\n✅ Reports generated successfully!")

if __name__ == "__main__":
    main()
