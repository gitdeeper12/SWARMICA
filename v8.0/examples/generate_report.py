#!/usr/bin/env python3
"""Generate swarm simulation report"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.core.engine import SwarmicaV8
from swarmica.reporting import SwarmReportGenerator


def main():
    print("=" * 60)
    print("📊 SWARMICA v8.0 - Report Generator Demo")
    print("=" * 60)
    
    sim = SwarmicaV8(n_agents=100, alpha=1.2, beta=2.0, gamma=0.5, sigma=0.1)
    
    print("\nRunning simulation...")
    sim.run(steps=300)
    
    report_gen = SwarmReportGenerator()
    report = report_gen.generate_from_simulator(sim)
    
    report_gen.print_summary(report)
    
    print("\nSaving reports...")
    report_gen.save_json(report)
    report_gen.save_markdown(report)
    report_gen.save_csv(report)
    
    print("\n✅ Reports generated successfully!")

if __name__ == "__main__":
    main()
