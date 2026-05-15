"""Report Generator for SWARMICA v4.0 - Neural Energy PDE Engine"""

import json
import math
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class NeuralPDEReport:
    """Data class for Neural PDE simulation results"""
    timestamp: str
    config: Dict[str, Any]
    history: Dict[str, List[float]]
    summary: Dict[str, float]
    phase_analysis: Dict[str, Any]
    energy_analysis: Dict[str, Any]


class NeuralPDEReportGenerator:
    """Generate comprehensive reports from Neural PDE simulations"""
    
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir
        self.reports = []
    
    def generate_from_solver(self, solver) -> NeuralPDEReport:
        """Generate report from NeuralPDESolver instance"""
        config = {
            'n': solver.n,
            'dt': solver.dt,
            'dx': solver.dx,
            'alpha': solver.alpha,
            'beta': solver.beta,
            'noise': solver.noise,
            'energy_lr': solver.energy_lr
        }
        
        energy_history = solver.history['energy']
        order_history = solver.history['order_parameter']
        
        # Phase analysis
        phase_report = solver.get_phase_report()
        
        # Energy analysis
        energy_analysis = self._analyze_energy(energy_history)
        
        # Summary metrics
        summary = {
            'final_energy': energy_history[-1] if energy_history else 0,
            'initial_energy': energy_history[0] if energy_history else 0,
            'energy_reduction': ((energy_history[0] - energy_history[-1]) / (energy_history[0] + 1e-8) * 100) if energy_history else 0,
            'final_order_parameter': order_history[-1] if order_history else 0,
            'initial_order_parameter': order_history[0] if order_history else 0,
            'order_parameter_change': ((order_history[-1] - order_history[0]) / (order_history[0] + 1e-8) * 100) if order_history else 0
        }
        
        report = NeuralPDEReport(
            timestamp=datetime.now().isoformat(),
            config=config,
            history={
                'energy': energy_history[-100:],
                'order_parameter': order_history[-100:]
            },
            summary=summary,
            phase_analysis=phase_report,
            energy_analysis=energy_analysis
        )
        
        self.reports.append(report)
        return report
    
    def _analyze_energy(self, energy_history: List[float]) -> Dict[str, Any]:
        """Analyze energy evolution"""
        if len(energy_history) < 10:
            return {'status': 'Insufficient data'}
        
        final_energy = energy_history[-1]
        initial_energy = energy_history[0]
        reduction = (initial_energy - final_energy) / initial_energy * 100
        
        if reduction > 70:
            status = "Excellent - Strong convergence"
        elif reduction > 50:
            status = "Good - Clear minimization"
        elif reduction > 30:
            status = "Fair - Moderate convergence"
        elif reduction > 10:
            status = "Poor - Weak minimization"
        else:
            status = "Unstable - No convergence"
        
        return {
            'status': status,
            'reduction_percent': reduction,
            'final_energy': final_energy,
            'initial_energy': initial_energy
        }
    
    def save_json(self, report: NeuralPDEReport, filename: str = None) -> str:
        """Save report as JSON"""
        if filename is None:
            filename = f"neural_pde_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = asdict(report)
        filepath = f"{self.reports_dir}/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ JSON report saved: {filepath}")
        return filepath
    
    def save_markdown(self, report: NeuralPDEReport, filename: str = None) -> str:
        """Save report as Markdown"""
        if filename is None:
            filename = f"neural_pde_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        lines = []
        lines.append(f"# SWARMICA v4.0 Neural PDE Simulation Report")
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
        lines.append(f"- **Energy Reduction**: {report.energy_analysis['reduction_percent']:.1f}%")
        lines.append("")
        lines.append("## Phase Transition Analysis")
        lines.append("")
        lines.append(f"- **Current Phase**: {report.phase_analysis.get('current_phase', 'N/A')}")
        lines.append(f"- **Order Parameter**: {report.phase_analysis.get('current_order_parameter', 0):.4f}")
        lines.append(f"- **Phase Transition Detected**: {report.phase_analysis.get('phase_transition_detected', False)}")
        lines.append("")
        lines.append("## Summary Metrics")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Initial Energy | {report.summary['initial_energy']:.4f} |")
        lines.append(f"| Final Energy | {report.summary['final_energy']:.4f} |")
        lines.append(f"| Energy Reduction | {report.summary['energy_reduction']:.1f}% |")
        lines.append(f"| Initial Order Parameter | {report.summary['initial_order_parameter']:.4f} |")
        lines.append(f"| Final Order Parameter | {report.summary['final_order_parameter']:.4f} |")
        lines.append("")
        lines.append("---")
        lines.append("*Report generated by SWARMICA v4.0 Neural PDE Engine*")
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("\n".join(lines))
        
        print(f"✅ Markdown report saved: {filepath}")
        return filepath
    
    def save_csv(self, report: NeuralPDEReport, filename: str = None) -> str:
        """Save metrics as CSV"""
        if filename is None:
            filename = f"neural_pde_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("step,energy,order_parameter\n")
            energy = report.history['energy']
            order = report.history['order_parameter']
            for i, (e, o) in enumerate(zip(energy, order)):
                f.write(f"{i},{e:.6f},{o:.6f}\n")
        
        print(f"✅ CSV saved: {filepath}")
        return filepath
    
    def print_summary(self, report: NeuralPDEReport):
        """Print summary to console"""
        print("\n" + "=" * 60)
        print("🧠 SWARMICA v4.0 Neural PDE Simulation Summary")
        print("=" * 60)
        print(f"Timestamp: {report.timestamp}")
        print()
        print("Energy Analysis:")
        print(f"  Status: {report.energy_analysis['status']}")
        print(f"  Reduction: {report.energy_analysis['reduction_percent']:.1f}%")
        print()
        print("Phase Analysis:")
        print(f"  Phase: {report.phase_analysis.get('current_phase', 'N/A')}")
        print(f"  Order Parameter: {report.phase_analysis.get('current_order_parameter', 0):.4f}")
        print(f"  Transition: {report.phase_analysis.get('phase_transition_detected', False)}")
        print("=" * 60)


def create_neural_pde_report_generator() -> NeuralPDEReportGenerator:
    """Factory function for report generator"""
    return NeuralPDEReportGenerator()
