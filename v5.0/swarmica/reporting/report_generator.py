"""Report Generator for SWARMICA v5.0 - Variational Swarm Control System"""

import json
import math
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class VariationalControlReport:
    """Data class for Variational Control simulation results"""
    timestamp: str
    config: Dict[str, Any]
    history: Dict[str, List[float]]
    summary: Dict[str, float]
    variational_analysis: Dict[str, Any]


class VariationalReportGenerator:
    """Generate comprehensive reports from Variational Control simulations"""
    
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir
        self.reports = []
    
    def generate_from_controller(self, controller) -> VariationalControlReport:
        """Generate report from VariationalController instance"""
        config = {
            'n': controller.n,
            'dt': controller.dt,
            'dx': controller.dx,
            'alpha': controller.alpha,
            'beta': controller.beta,
            'sigma': controller.sigma,
            'control_gain': controller.control_gain
        }
        
        energy_history = controller.history['energy']
        entropy_history = controller.history['entropy']
        control_cost_history = controller.history['control_cost']
        total_cost_history = controller.history['total_cost']
        
        variational_analysis = self._analyze_variational_cost(total_cost_history, energy_history, control_cost_history)
        
        summary = {
            'final_energy': energy_history[-1] if energy_history else 0,
            'initial_energy': energy_history[0] if energy_history else 0,
            'energy_reduction': ((energy_history[0] - energy_history[-1]) / (energy_history[0] + 1e-8) * 100) if energy_history else 0,
            'final_total_cost': total_cost_history[-1] if total_cost_history else 0,
            'initial_total_cost': total_cost_history[0] if total_cost_history else 0,
            'total_cost_reduction': ((total_cost_history[0] - total_cost_history[-1]) / (total_cost_history[0] + 1e-8) * 100) if total_cost_history else 0,
            'final_control_cost': control_cost_history[-1] if control_cost_history else 0,
            'final_entropy': entropy_history[-1] if entropy_history else 0
        }
        
        report = VariationalControlReport(
            timestamp=datetime.now().isoformat(),
            config=config,
            history={
                'energy': energy_history[-100:],
                'entropy': entropy_history[-100:],
                'control_cost': control_cost_history[-100:],
                'total_cost': total_cost_history[-100:]
            },
            summary=summary,
            variational_analysis=variational_analysis
        )
        
        self.reports.append(report)
        return report
    
    def _analyze_variational_cost(self, total_cost: List[float], energy: List[float], control: List[float]) -> Dict[str, Any]:
        if len(total_cost) < 10:
            return {'status': 'Insufficient data'}
        
        final_cost = total_cost[-1]
        initial_cost = total_cost[0]
        reduction = (initial_cost - final_cost) / initial_cost * 100
        
        if reduction > 70:
            optimality = "Near-Optimal - Excellent cost reduction"
        elif reduction > 50:
            optimality = "Suboptimal - Good reduction"
        elif reduction > 30:
            optimality = "Moderate - Acceptable reduction"
        elif reduction > 10:
            optimality = "Poor - Limited reduction"
        else:
            optimality = "Ineffective - No significant reduction"
        
        energy_final = energy[-1] if energy else 0
        energy_initial = energy[0] if energy else 0
        energy_red = (energy_initial - energy_final) / (energy_initial + 1e-8) * 100
        
        control_final = control[-1] if control else 0
        control_initial = control[0] if control else 0
        control_red = (control_initial - control_final) / (control_initial + 1e-8) * 100 if control_initial > 0 else 0
        
        return {
            'status': optimality,
            'reduction_percent': reduction,
            'final_cost': final_cost,
            'initial_cost': initial_cost,
            'energy_reduction': energy_red,
            'control_reduction': control_red,
            'trade_off_ratio': energy_red / (control_red + 1e-8)
        }
    
    def save_json(self, report: VariationalControlReport, filename: str = None) -> str:
        if filename is None:
            filename = f"variational_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = asdict(report)
        filepath = f"{self.reports_dir}/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ JSON report saved: {filepath}")
        return filepath
    
    def save_markdown(self, report: VariationalControlReport, filename: str = None) -> str:
        if filename is None:
            filename = f"variational_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        lines = []
        lines.append(f"# SWARMICA v5.0 Variational Control Report")
        lines.append(f"*Generated: {report.timestamp}*")
        lines.append("")
        lines.append("## Configuration")
        for key, value in report.config.items():
            lines.append(f"- **{key}**: {value}")
        lines.append("")
        lines.append("## Variational Analysis")
        lines.append(f"- **Optimality Status**: {report.variational_analysis['status']}")
        lines.append(f"- **Total Cost Reduction**: {report.variational_analysis['reduction_percent']:.1f}%")
        lines.append(f"- **Energy Reduction**: {report.variational_analysis['energy_reduction']:.1f}%")
        lines.append(f"- **Control Reduction**: {report.variational_analysis['control_reduction']:.1f}%")
        lines.append("")
        lines.append("## Summary Metrics")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Initial Total Cost | {report.summary['initial_total_cost']:.4f} |")
        lines.append(f"| Final Total Cost | {report.summary['final_total_cost']:.4f} |")
        lines.append(f"| Total Cost Reduction | {report.summary['total_cost_reduction']:.1f}% |")
        lines.append(f"| Final Energy | {report.summary['final_energy']:.4f} |")
        lines.append(f"| Final Entropy | {report.summary['final_entropy']:.4f} |")
        lines.append("")
        lines.append("---")
        lines.append("*Report generated by SWARMICA v5.0 Variational Control Engine*")
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("\n".join(lines))
        
        print(f"✅ Markdown report saved: {filepath}")
        return filepath
    
    def save_csv(self, report: VariationalControlReport, filename: str = None) -> str:
        if filename is None:
            filename = f"variational_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("step,energy,entropy,control_cost,total_cost\n")
            energy = report.history['energy']
            entropy = report.history['entropy']
            control = report.history['control_cost']
            total = report.history['total_cost']
            for i, (e, ent, c, t) in enumerate(zip(energy, entropy, control, total)):
                f.write(f"{i},{e:.6f},{ent:.6f},{c:.6f},{t:.6f}\n")
        
        print(f"✅ CSV saved: {filepath}")
        return filepath
    
    def print_summary(self, report: VariationalControlReport):
        print("\n" + "=" * 60)
        print("🎮 SWARMICA v5.0 Variational Control Summary")
        print("=" * 60)
        print(f"Optimality Status: {report.variational_analysis['status']}")
        print(f"Total Cost Reduction: {report.variational_analysis['reduction_percent']:.1f}%")
        print(f"Final Total Cost: {report.summary['final_total_cost']:.4f}")
        print("=" * 60)


def create_variational_report_generator() -> VariationalReportGenerator:
    return VariationalReportGenerator()
