"""Report Generator for SWARMICA v6.0 - Neural Optimal Swarm Physics Engine"""

import json
import math
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class OptimalControlReport:
    """Data class for Optimal Control simulation results"""
    timestamp: str
    config: Dict[str, Any]
    history: Dict[str, List[float]]
    summary: Dict[str, float]
    pmp_analysis: Dict[str, Any]


class OptimalControlReportGenerator:
    """Generate comprehensive reports from Optimal Control simulations"""
    
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir
    
    def generate_from_controller(self, controller) -> OptimalControlReport:
        """Generate report from OptimalSwarmController instance"""
        config = {
            'n': controller.n,
            'dt': controller.dt,
            'dx': controller.dx,
            'alpha': controller.alpha,
            'beta': controller.beta,
            'sigma': controller.sigma,
            'control_weight': controller.control_weight,
            'adjoint_lr': controller.adjoint_lr
        }
        
        energy_history = controller.history['energy']
        control_history = controller.history['control_effort']
        total_cost_history = controller.history['total_cost']
        
        # PMP analysis
        pmp_analysis = self._analyze_pmp(total_cost_history, energy_history, control_history, controller)
        
        summary = {
            'final_energy': energy_history[-1] if energy_history else 0,
            'initial_energy': energy_history[0] if energy_history else 0,
            'energy_reduction': ((energy_history[0] - energy_history[-1]) / (energy_history[0] + 1e-8) * 100) if energy_history else 0,
            'final_total_cost': total_cost_history[-1] if total_cost_history else 0,
            'initial_total_cost': total_cost_history[0] if total_cost_history else 0,
            'total_cost_reduction': ((total_cost_history[0] - total_cost_history[-1]) / (total_cost_history[0] + 1e-8) * 100) if total_cost_history else 0,
            'final_control_effort': control_history[-1] if control_history else 0,
            'optimality_gap': controller.get_optimality_gap()
        }
        
        return OptimalControlReport(
            timestamp=datetime.now().isoformat(),
            config=config,
            history={
                'energy': energy_history[-100:],
                'control_effort': control_history[-100:],
                'total_cost': total_cost_history[-100:]
            },
            summary=summary,
            pmp_analysis=pmp_analysis
        )
    
    def _analyze_pmp(self, total_cost: List[float], energy: List[float], 
                     control: List[float], controller) -> Dict[str, Any]:
        """Analyze PMP optimality conditions"""
        if len(total_cost) < 10:
            return {'status': 'Insufficient data'}
        
        final_cost = total_cost[-1]
        initial_cost = total_cost[0]
        reduction = (initial_cost - final_cost) / initial_cost * 100
        
        if reduction > 80:
            optimality = "Near-Optimal - Excellent convergence"
        elif reduction > 60:
            optimality = "Suboptimal - Good convergence"
        elif reduction > 40:
            optimality = "Moderate - Acceptable"
        elif reduction > 20:
            optimality = "Poor - Limited convergence"
        else:
            optimality = "Ineffective - No convergence"
        
        energy_red = (energy[0] - energy[-1]) / (energy[0] + 1e-8) * 100 if energy else 0
        control_red = (control[0] - control[-1]) / (control[0] + 1e-8) * 100 if control and control[0] > 0 else 0
        optimality_gap = controller.get_optimality_gap()
        
        return {
            'status': optimality,
            'reduction_percent': reduction,
            'energy_reduction': energy_red,
            'control_reduction': control_red,
            'optimality_gap': optimality_gap,
            'pmp_satisfied': optimality_gap < 0.1
        }
    
    def save_json(self, report: OptimalControlReport, filename: str = None) -> str:
        if filename is None:
            filename = f"optimal_control_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            json.dump(asdict(report), f, indent=2)
        print(f"✅ JSON saved: {filepath}")
        return filepath
    
    def save_markdown(self, report: OptimalControlReport, filename: str = None) -> str:
        if filename is None:
            filename = f"optimal_control_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        lines = []
        lines.append(f"# SWARMICA v6.0 Optimal Control Report")
        lines.append(f"*Generated: {report.timestamp}*")
        lines.append("")
        lines.append("## Configuration")
        for k, v in report.config.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")
        lines.append("## Pontryagin Maximum Principle Analysis")
        lines.append(f"- **Optimality Status**: {report.pmp_analysis['status']}")
        lines.append(f"- **Total Cost Reduction**: {report.pmp_analysis['reduction_percent']:.1f}%")
        lines.append(f"- **Energy Reduction**: {report.pmp_analysis['energy_reduction']:.1f}%")
        lines.append(f"- **Control Reduction**: {report.pmp_analysis['control_reduction']:.1f}%")
        lines.append(f"- **Optimality Gap**: {report.pmp_analysis['optimality_gap']:.4f}")
        lines.append(f"- **PMP Satisfied**: {report.pmp_analysis['pmp_satisfied']}")
        lines.append("")
        lines.append("## Summary Metrics")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Initial Total Cost | {report.summary['initial_total_cost']:.4f} |")
        lines.append(f"| Final Total Cost | {report.summary['final_total_cost']:.4f} |")
        lines.append(f"| Total Cost Reduction | {report.summary['total_cost_reduction']:.1f}% |")
        lines.append(f"| Final Energy | {report.summary['final_energy']:.4f} |")
        lines.append(f"| Final Control Effort | {report.summary['final_control_effort']:.4f} |")
        lines.append(f"| Optimality Gap | {report.summary['optimality_gap']:.4f} |")
        lines.append("")
        lines.append("## Pontryagin Optimal Control Law")
        lines.append("```")
        lines.append("u* = -(1/λ) · p")
        lines.append("∂p/∂t = -∂H/∂ρ")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("*Report generated by SWARMICA v6.0 Neural Optimal Control Engine*")
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("\n".join(lines))
        print(f"✅ Markdown saved: {filepath}")
        return filepath
    
    def save_csv(self, report: OptimalControlReport, filename: str = None) -> str:
        if filename is None:
            filename = f"optimal_control_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("step,energy,control_effort,total_cost\n")
            energy = report.history['energy']
            control = report.history['control_effort']
            total = report.history['total_cost']
            for i, (e, c, t) in enumerate(zip(energy, control, total)):
                f.write(f"{i},{e:.6f},{c:.6f},{t:.6f}\n")
        print(f"✅ CSV saved: {filepath}")
        return filepath
    
    def print_summary(self, report: OptimalControlReport):
        print("\n" + "=" * 60)
        print("🎯 SWARMICA v6.0 Optimal Control Summary")
        print("=" * 60)
        print(f"Optimality Status: {report.pmp_analysis['status']}")
        print(f"Total Cost Reduction: {report.pmp_analysis['reduction_percent']:.1f}%")
        print(f"Optimality Gap: {report.pmp_analysis['optimality_gap']:.4f}")
        print(f"PMP Satisfied: {report.pmp_analysis['pmp_satisfied']}")
        print("=" * 60)


def create_optimal_control_report_generator() -> OptimalControlReportGenerator:
    return OptimalControlReportGenerator()
