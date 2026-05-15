"""Report Generator for SWARMICA v7.0 - Continuous Neural Control PDE System"""

import json
import math
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class ContinuousControlReport:
    """Data class for Continuous Control simulation results"""
    timestamp: str
    config: Dict[str, Any]
    history: Dict[str, List[float]]
    summary: Dict[str, float]
    stability_certificate: Dict[str, Any]


class ContinuousControlReportGenerator:
    """Generate comprehensive reports from Continuous Control simulations"""
    
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir
    
    def generate_from_controller(self, controller) -> ContinuousControlReport:
        """Generate report from ContinuousController instance"""
        config = {
            'n': controller.n,
            'dt': controller.dt,
            'dx': controller.dx,
            'beta': controller.beta,
            'sigma': controller.sigma,
            'K_gain': controller.K_gain,
            'lambda_reg': controller.lambda_reg
        }
        
        energy_history = controller.history['energy']
        stability_history = controller.history['stability_metric']
        lyapunov_history = controller.history['lyapunov']
        
        cert = controller.get_stability_certificate()
        
        summary = {
            'final_energy': energy_history[-1] if energy_history else 0,
            'initial_energy': energy_history[0] if energy_history else 0,
            'energy_reduction': ((energy_history[0] - energy_history[-1]) / (energy_history[0] + 1e-8) * 100) if energy_history else 0,
            'final_stability': stability_history[-1] if stability_history else 0,
            'initial_stability': stability_history[0] if stability_history else 0,
            'stability_improvement': ((stability_history[-1] - stability_history[0]) * 100) if stability_history else 0,
            'final_lyapunov': lyapunov_history[-1] if lyapunov_history else 0,
            'initial_lyapunov': lyapunov_history[0] if lyapunov_history else 0
        }
        
        return ContinuousControlReport(
            timestamp=datetime.now().isoformat(),
            config=config,
            history={
                'energy': energy_history[-100:],
                'stability_metric': stability_history[-100:],
                'lyapunov': lyapunov_history[-100:]
            },
            summary=summary,
            stability_certificate=cert
        )
    
    def save_json(self, report: ContinuousControlReport, filename: str = None) -> str:
        """Save report as JSON"""
        if filename is None:
            filename = f"continuous_control_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            json.dump(asdict(report), f, indent=2)
        print(f"✅ JSON saved: {filepath}")
        return filepath
    
    def save_markdown(self, report: ContinuousControlReport, filename: str = None) -> str:
        """Save report as Markdown"""
        if filename is None:
            filename = f"continuous_control_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        lines = []
        lines.append(f"# SWARMICA v7.0 Continuous Control Report")
        lines.append(f"*Generated: {report.timestamp}*")
        lines.append("")
        lines.append("## Configuration")
        for k, v in report.config.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")
        lines.append("## Stability Certificate")
        lines.append(f"- **Certified**: {report.stability_certificate['certified']}")
        lines.append(f"- **Lyapunov Decay**: {report.stability_certificate['lyapunov_decay']:.2%}")
        lines.append(f"- **Final Stability**: {report.stability_certificate['final_stability']:.4f}")
        lines.append(f"- **Energy Reduction**: {report.stability_certificate['energy_reduction']:.1f}%")
        lines.append("")
        lines.append("## Summary Metrics")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Initial Energy | {report.summary['initial_energy']:.4f} |")
        lines.append(f"| Final Energy | {report.summary['final_energy']:.4f} |")
        lines.append(f"| Energy Reduction | {report.summary['energy_reduction']:.1f}% |")
        lines.append(f"| Initial Stability | {report.summary['initial_stability']:.4f} |")
        lines.append(f"| Final Stability | {report.summary['final_stability']:.4f} |")
        lines.append(f"| Stability Improvement | {report.summary['stability_improvement']:.1f}% |")
        lines.append("")
        lines.append("## Continuous PDE Formulation")
        lines.append("```")
        lines.append("∂ρ/∂t = Nθ(ρ) - K∇Φ(ρ) + βΔρ + σξ(x,t)")
        lines.append("E[ρ] = ∫(ρ - ρ*)² dx + λ∫‖∇ρ‖² dx")
        lines.append("V[ρ] = ∫(ρ - ρ*)² dx + ∫|∇ρ|² dx")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("*Report generated by SWARMICA v7.0 Continuous Control Engine*")
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("\n".join(lines))
        print(f"✅ Markdown saved: {filepath}")
        return filepath
    
    def save_csv(self, report: ContinuousControlReport, filename: str = None) -> str:
        """Save metrics as CSV"""
        if filename is None:
            filename = f"continuous_control_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("step,energy,stability_metric,lyapunov\n")
            energy = report.history['energy']
            stability = report.history['stability_metric']
            lyapunov = report.history['lyapunov']
            for i, (e, s, l) in enumerate(zip(energy, stability, lyapunov)):
                f.write(f"{i},{e:.6f},{s:.6f},{l:.6f}\n")
        print(f"✅ CSV saved: {filepath}")
        return filepath
    
    def print_summary(self, report: ContinuousControlReport):
        """Print summary to console"""
        print("\n" + "=" * 60)
        print("🔬 SWARMICA v7.0 Continuous Control Summary")
        print("=" * 60)
        print(f"Stability Certified: {report.stability_certificate['certified']}")
        print(f"Lyapunov Decay: {report.stability_certificate['lyapunov_decay']:.2%}")
        print(f"Energy Reduction: {report.stability_certificate['energy_reduction']:.1f}%")
        print(f"Final Stability: {report.stability_certificate['final_stability']:.4f}")
        print("=" * 60)


def create_continuous_control_report_generator() -> ContinuousControlReportGenerator:
    """Factory function for report generator"""
    return ContinuousControlReportGenerator()
