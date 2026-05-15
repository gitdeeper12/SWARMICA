#!/usr/bin/env python3
"""Generate Physics Discovery report"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.core.discovery_engine import DiscoveryEngine
from swarmica.reporting import DiscoveryReportGenerator


def main():
    print("=" * 60)
    print("📊 SWARMICA v13.0 - Physics Discovery Report Generator")
    print("=" * 60)
    
    engine = DiscoveryEngine(N=40, alpha=0.001)
    
    print("\nDiscovering physical laws from field observations...")
    result = engine.discover_physics()
    
    report_gen = DiscoveryReportGenerator()
    report = report_gen.generate_from_engine(engine, result)
    
    report_gen.print_summary(report)
    
    print("\nSaving reports...")
    report_gen.save_json(report)
    report_gen.save_markdown(report)
    report_gen.save_csv(report)
    
    print("\n✅ Reports generated successfully!")

if __name__ == "__main__":
    main()
