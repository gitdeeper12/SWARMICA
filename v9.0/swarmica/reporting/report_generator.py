"""Report Generator for SWARMICA v9.0 - Continuum PDE System"""

import json
import math
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class PDEReport:
    """Data class for PDE simulation results"""
    timestamp: str
    config: Dict[str, Any]
    history: Dict[str, List[float]]
    summary: Dict[str, float]
    pde_analysis: Dict[str, Any]


class PDEReportGenerator:
    """Generate comprehensive reports from PDE simulations"""
    
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir
    
    def generate_from_solver(self, solver) -> PDEReport:
        """Generate report from ContinuumPDESolver instance"""
        config = {
            'N': solver.N,
            'dt': solver.dt,
            'dx': solver.dx,
            'alpha': solver.alpha,
            'gamma': solver.gamma,
            'nu': solver.nu
        }
        
        coherence_history = solver.history['coherence']
        entropy_history = solver.history['entropy']
        energy_history = solver.history['energy']
        
        # PDE analysis
        pde_analysis = self._analyze_pde(coherence_history, entropy_history, energy_history)
        
        summary = {
            'final_coherence': coherence_history[-1] if coherence_history else 0,
            'initial_coherence': coherence_history[0] if coherence_history else 0,
            'coherence_improvement': ((coherence_history[-1] - coherence_history[0]) * 100) if coherence_history else 0,
            'final_entropy': entropy_history[-1] if entropy_history else 0,
            'initial_entropy': entropy_history[0] if entropy_history else 0,
            'entropy_reduction': ((entropy_history[0] - entropy_history[-1]) / (entropy_history[0] + 1e-8) * 100) if entropy_history else 0,
            'final_energy': energy_history[-1] if energy_history else 0,
            'initial_energy': energy_history[0] if energy_history else 0,
            'energy_reduction': ((energy_history[0] - energy_history[-1]) / (energy_history[0] + 1e-8) * 100) if energy_history else 0
        }
        
        return PDEReport(
            timestamp=datetime.now().isoformat(),
            config=config,
            history={
                'coherence': coherence_history[-100:],
                'entropy': entropy_history[-100:],
                'energy': energy_history[-100:]
            },
            summary=summary,
            pde_analysis=pde_analysis
        )
    
    def _analyze_pde(self, coherence: List[float], entropy: List[float], 
                     energy: List[float]) -> Dict[str, Any]:
        """Analyze PDE system behavior"""
        if len(coherence) < 10:
            return {'status': 'Insufficient data'}
        
        final_coherence = coherence[-1]
        
        # Classification
        if final_coherence >= 0.8:
            status = "Excellent - High coherence"
        elif final_coherence >= 0.6:
            status = "Good - Moderate coherence"
        elif final_coherence >= 0.4:
            status = "Fair - Low coherence"
        elif final_coherence >= 0.2:
            status = "Poor - Very low coherence"
        else:
            status = "Critical - Disordered field"
        
        # Trend analysis
        coherence_trend = coherence[-1] - coherence[-10] if len(coherence) >= 10 else 0
        entropy_trend = entropy[-1] - entropy[-10] if len(entropy) >= 10 else 0
        energy_trend = energy[-1] - energy[-10] if len(energy) >= 10 else 0
        
        converged = final_coherence >= 0.7
        
        return {
            'status': status,
            'converged': converged,
            'final_coherence': final_coherence,
            'coherence_trend': coherence_trend,
            'entropy_trend': entropy_trend,
            'energy_trend': energy_trend,
            'recommendation': self._get_recommendation(status, coherence_trend)
        }
    
    def _get_recommendation(self, status: str, trend: float) -> str:
        if "Excellent" in status:
            return "System is optimal. PDE parameters well-tuned."
        elif "Good" in status:
            return "System stable. Slight increase in α may improve."
        elif "Fair" in status:
            return "Increase gradient energy α or reduce viscosity ν."
        elif "Poor" in status:
            return "Increase α > 1.5, reduce γ < 0.2"
        else:
            return "Major retuning needed: α > 2.0, γ < 0.1, ν < 0.1"
    
    def save_json(self, report: PDEReport, filename: str = None) -> str:
        if filename is None:
            filename = f"pde_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            json.dump(asdict(report), f, indent=2)
        print(f"✅ JSON saved: {filepath}")
        return filepath
    
    def save_markdown(self, report: PDEReport, filename: str = None) -> str:
        if filename is None:
            filename = f"pde_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        lines = []
        lines.append(f"# SWARMICA v9.0 PDE Simulation Report")
        lines.append(f"*Generated: {report.timestamp}*")
        lines.append("")
        lines.append("## Configuration")
        for k, v in report.config.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")
        lines.append("## PDE System Analysis")
        lines.append(f"- **Status**: {report.pde_analysis['status']}")
        lines.append(f"- **Converged**: {report.pde_analysis['converged']}")
        lines.append(f"- **Coherence Trend**: {report.pde_analysis['coherence_trend']:+.4f}")
        lines.append(f"- **Entropy Trend**: {report.pde_analysis['entropy_trend']:+.4f}")
        lines.append(f"- **Energy Trend**: {report.pde_analysis['energy_trend']:+.4f}")
        lines.append(f"- **Recommendation**: {report.pde_analysis['recommendation']}")
        lines.append("")
        lines.append("## Summary Metrics")
        lines.append("| Metric | Initial | Final | Change |")
        lines.append("|--------|---------|-------|--------|")
        lines.append(f"| Coherence | {report.summary['initial_coherence']:.4f} | {report.summary['final_coherence']:.4f} | {report.summary['coherence_improvement']:+.1f}% |")
        lines.append(f"| Entropy | {report.summary['initial_entropy']:.4f} | {report.summary['final_entropy']:.4f} | {report.summary['entropy_reduction']:+.1f}% |")
        lines.append(f"| Energy | {report.summary['initial_energy']:.4f} | {report.summary['final_energy']:.4f} | {report.summary['energy_reduction']:+.1f}% |")
        lines.append("")
        lines.append("## PDE Formulation")
        lines.append("```")
        lines.append("∂ρ/∂t + ∇·(ρv) = 0")
        lines.append("∂v/∂t = -∇E[ρ] - γv + ν∇²v")
        lines.append("E[ρ] = ∫(α|∇ρ|²) dx")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("*Report generated by SWARMICA v9.0 Continuum PDE Engine*")
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("\n".join(lines))
        print(f"✅ Markdown saved: {filepath}")
        return filepath
    
    def save_csv(self, report: PDEReport, filename: str = None) -> str:
        if filename is None:
            filename = f"pde_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("step,coherence,entropy,energy\n")
            coherence = report.history['coherence']
            entropy = report.history['entropy']
            energy = report.history['energy']
            for i, (c, e, en) in enumerate(zip(coherence, entropy, energy)):
                f.write(f"{i},{c:.6f},{e:.6f},{en:.6f}\n")
        print(f"✅ CSV saved: {filepath}")
        return filepath
    
    def print_summary(self, report: PDEReport):
        print("\n" + "=" * 60)
        print("🔬 SWARMICA v9.0 PDE Simulation Summary")
        print("=" * 60)
        print(f"Status: {report.pde_analysis['status']}")
        print(f"Final Coherence: {report.summary['final_coherence']:.4f}")
        print(f"Coherence Improvement: {report.summary['coherence_improvement']:+.1f}%")
        print(f"Entropy Reduction: {report.summary['entropy_reduction']:.1f}%")
        print(f"Energy Reduction: {report.summary['energy_reduction']:.1f}%")
        print(f"Converged: {report.pde_analysis['converged']}")
        print("=" * 60)


def create_pde_report_generator() -> PDEReportGenerator:
    return PDEReportGenerator()
