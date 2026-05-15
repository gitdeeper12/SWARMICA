"""Report Generator for SWARMICA v3.0"""

import json
import math
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class PDESimulationReport:
    """Data class for PDE simulation results"""
    timestamp: str
    config: Dict[str, Any]
    history: Dict[str, List[float]]
    summary: Dict[str, float]
    energy_analysis: Dict[str, Any]


class PDEReportGenerator:
    """Generate comprehensive reports from PDE simulations"""
    
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir
        self.reports = []
    
    def generate_from_solver(self, solver) -> PDESimulationReport:
        """Generate report from PDESolver instance"""
        config = {
            'n': solver.n,
            'dt': solver.dt,
            'dx': solver.dx,
            'alpha': solver.alpha,
            'beta': solver.beta,
            'noise': solver.noise
        }
        
        energy_history = solver.history['energy']
        
        # Energy analysis
        energy_analysis = self._analyze_energy(energy_history)
        
        # Summary metrics
        summary = {
            'final_energy': energy_history[-1] if energy_history else 0,
            'initial_energy': energy_history[0] if energy_history else 0,
            'energy_reduction': ((energy_history[0] - energy_history[-1]) / (energy_history[0] + 1e-8) * 100) if energy_history else 0,
            'min_energy': min(energy_history) if energy_history else 0,
            'energy_std': self._std_dev(energy_history) if energy_history else 0
        }
        
        report = PDESimulationReport(
            timestamp=datetime.now().isoformat(),
            config=config,
            history={
                'energy': energy_history[-100:],  # Keep last 100
                'total_density': solver.history['total_density'][-100:]
            },
            summary=summary,
            energy_analysis=energy_analysis
        )
        
        self.reports.append(report)
        return report
    
    def _std_dev(self, data: List[float]) -> float:
        """Compute standard deviation"""
        if len(data) < 2:
            return 0.0
        mean = sum(data) / len(data)
        variance = sum((x - mean) ** 2 for x in data) / len(data)
        return math.sqrt(variance)
    
    def _analyze_energy(self, energy_history: List[float]) -> Dict[str, Any]:
        """Analyze energy evolution"""
        if len(energy_history) < 10:
            return {'status': 'Insufficient data'}
        
        final_energy = energy_history[-1]
        initial_energy = energy_history[0]
        reduction = (initial_energy - final_energy) / initial_energy * 100
        
        # Classification
        if reduction > 80:
            status = "Excellent - Strong convergence"
        elif reduction > 60:
            status = "Good - Clear minimization"
        elif reduction > 40:
            status = "Fair - Moderate convergence"
        elif reduction > 20:
            status = "Poor - Weak minimization"
        else:
            status = "Unstable - No convergence"
        
        # Convergence detection
        converged = reduction > 50
        
        return {
            'status': status,
            'converged': converged,
            'reduction_percent': reduction,
            'final_energy': final_energy,
            'initial_energy': initial_energy
        }
    
    def save_json(self, report: PDESimulationReport, filename: str = None) -> str:
        """Save report as JSON"""
        if filename is None:
            filename = f"pde_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = asdict(report)
        filepath = f"{self.reports_dir}/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ JSON report saved: {filepath}")
        return filepath
    
    def save_markdown(self, report: PDESimulationReport, filename: str = None) -> str:
        """Save report as Markdown"""
        if filename is None:
            filename = f"pde_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        lines = []
        lines.append(f"# SWARMICA v3.0 PDE Simulation Report")
        lines.append(f"*Generated: {report.timestamp}*")
        lines.append("")
        lines.append("## Configuration")
        lines.append("")
        for key, value in report.config.items():
            lines.append(f"- **{key}**: {value}")
        lines.append("")
        lines.append("## Energy Analysis")
        lines.append("")
        lines.append(f"- **Status**: {report.energy_analysis['status']}")
        lines.append(f"- **Converged**: {report.energy_analysis['converged']}")
        lines.append(f"- **Energy Reduction**: {report.energy_analysis['reduction_percent']:.1f}%")
        lines.append("")
        lines.append("## Summary Metrics")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Initial Energy | {report.summary['initial_energy']:.4f} |")
        lines.append(f"| Final Energy | {report.summary['final_energy']:.4f} |")
        lines.append(f"| Energy Reduction | {report.summary['energy_reduction']:.1f}% |")
        lines.append(f"| Minimum Energy | {report.summary['min_energy']:.4f} |")
        lines.append("")
        lines.append("---")
        lines.append("*Report generated by SWARMICA v3.0 PDE Engine*")
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("\n".join(lines))
        
        print(f"✅ Markdown report saved: {filepath}")
        return filepath
    
    def print_summary(self, report: PDESimulationReport):
        """Print summary to console"""
        print("\n" + "=" * 60)
        print("🧠 SWARMICA v3.0 PDE Simulation Summary")
        print("=" * 60)
        print(f"Timestamp: {report.timestamp}")
        print()
        print("Energy Analysis:")
        print(f"  Status: {report.energy_analysis['status']}")
        print(f"  Reduction: {report.energy_analysis['reduction_percent']:.1f}%")
        print(f"  Initial: {report.summary['initial_energy']:.4f}")
        print(f"  Final: {report.summary['final_energy']:.4f}")
        print("=" * 60)


def create_pde_report_generator() -> PDEReportGenerator:
    """Factory function for PDE report generator"""
    return PDEReportGenerator()
