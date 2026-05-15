"""Report Generator for SWARMICA v8.0 - Unified Field Control Engine"""

import json
import math
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class SwarmReport:
    """Data class for swarm simulation results"""
    timestamp: str
    config: Dict[str, Any]
    history: Dict[str, List[float]]
    summary: Dict[str, float]
    stability_analysis: Dict[str, Any]


class SwarmReportGenerator:
    """Generate comprehensive reports from swarm simulations"""
    
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir
        self.reports = []
    
    def generate_from_simulator(self, simulator) -> SwarmReport:
        """Generate report from SwarmicaV8 instance"""
        config = {
            'n_agents': simulator.n_agents,
            'dim': simulator.dim,
            'dt': simulator.dt,
            'alpha': simulator.alpha,
            'beta': simulator.beta,
            'gamma': simulator.gamma,
            'sigma': simulator.sigma,
            'attractors': simulator.attractors
        }
        
        csi_history = simulator.history['csi']
        entropy_history = simulator.history['entropy']
        lyapunov_history = simulator.history['lyapunov']
        
        # Stability analysis
        stability_analysis = self._analyze_stability(csi_history, entropy_history, lyapunov_history)
        
        # Summary metrics
        summary = {
            'final_csi': csi_history[-1] if csi_history else 0,
            'initial_csi': csi_history[0] if csi_history else 0,
            'csi_improvement': ((csi_history[-1] - csi_history[0]) * 100) if csi_history else 0,
            'final_entropy': entropy_history[-1] if entropy_history else 0,
            'initial_entropy': entropy_history[0] if entropy_history else 0,
            'entropy_reduction': ((entropy_history[0] - entropy_history[-1]) / (entropy_history[0] + 1e-8) * 100) if entropy_history else 0,
            'final_lyapunov': lyapunov_history[-1] if lyapunov_history else 0,
            'initial_lyapunov': lyapunov_history[0] if lyapunov_history else 0,
            'lyapunov_reduction': ((lyapunov_history[0] - lyapunov_history[-1]) / (lyapunov_history[0] + 1e-8) * 100) if lyapunov_history and lyapunov_history[0] > 0 else 0
        }
        
        report = SwarmReport(
            timestamp=datetime.now().isoformat(),
            config=config,
            history={
                'csi': csi_history[-100:],
                'entropy': entropy_history[-100:],
                'lyapunov': lyapunov_history[-100:]
            },
            summary=summary,
            stability_analysis=stability_analysis
        )
        
        self.reports.append(report)
        return report
    
    def _analyze_stability(self, csi_history: List[float], entropy_history: List[float], 
                           lyapunov_history: List[float]) -> Dict[str, Any]:
        """Analyze stability characteristics"""
        if len(csi_history) < 10:
            return {'status': 'Insufficient data'}
        
        final_csi = csi_history[-1]
        
        # Stability classification
        if final_csi >= 0.9:
            status = "Excellent - Highly stable"
        elif final_csi >= 0.7:
            status = "Good - Stable"
        elif final_csi >= 0.5:
            status = "Fair - Moderately stable"
        elif final_csi >= 0.3:
            status = "Poor - Unstable"
        else:
            status = "Critical - Highly unstable"
        
        # CSI trend
        csi_trend = csi_history[-1] - csi_history[-10] if len(csi_history) >= 10 else 0
        
        # Entropy trend (lower is better)
        entropy_trend = entropy_history[-1] - entropy_history[-10] if len(entropy_history) >= 10 else 0
        
        # Lyapunov trend (lower is better)
        lyapunov_trend = lyapunov_history[-1] - lyapunov_history[-10] if len(lyapunov_history) >= 10 else 0
        
        # Convergence assessment
        converged = final_csi >= 0.85
        
        return {
            'status': status,
            'converged': converged,
            'final_csi': final_csi,
            'csi_trend': csi_trend,
            'entropy_trend': entropy_trend,
            'lyapunov_trend': lyapunov_trend,
            'recommendation': self._get_recommendation(status, csi_trend)
        }
    
    def _get_recommendation(self, status: str, trend: float) -> str:
        """Generate recommendation based on stability status"""
        if "Excellent" in status:
            return "System is optimal. Maintain current parameters."
        elif "Good" in status:
            return "System is stable. Slight tuning may improve performance."
        elif "Fair" in status:
            return "Consider increasing cohesion (α) or attractor strength (β)."
        elif "Poor" in status:
            return "Increase α and β. Reduce noise (σ) if possible."
        else:
            return "Major parameter adjustment needed. Increase α > 2.0, β > 3.0"
    
    def save_json(self, report: SwarmReport, filename: str = None) -> str:
        """Save report as JSON"""
        if filename is None:
            filename = f"swarm_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            json.dump(asdict(report), f, indent=2)
        print(f"✅ JSON saved: {filepath}")
        return filepath
    
    def save_markdown(self, report: SwarmReport, filename: str = None) -> str:
        """Save report as Markdown"""
        if filename is None:
            filename = f"swarm_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        lines = []
        lines.append(f"# SWARMICA v8.0 Simulation Report")
        lines.append(f"*Generated: {report.timestamp}*")
        lines.append("")
        lines.append("## Configuration")
        lines.append("")
        for k, v in report.config.items():
            if k != 'attractors':
                lines.append(f"- **{k}**: {v}")
        lines.append(f"- **Attractors**: {report.config['attractors']}")
        lines.append("")
        lines.append("## Stability Analysis")
        lines.append("")
        lines.append(f"- **Status**: {report.stability_analysis['status']}")
        lines.append(f"- **Converged**: {report.stability_analysis['converged']}")
        lines.append(f"- **CSI Trend**: {report.stability_analysis['csi_trend']:+.4f}")
        lines.append(f"- **Entropy Trend**: {report.stability_analysis['entropy_trend']:+.4f}")
        lines.append(f"- **Recommendation**: {report.stability_analysis['recommendation']}")
        lines.append("")
        lines.append("## Summary Metrics")
        lines.append("")
        lines.append("| Metric | Initial | Final | Change |")
        lines.append("|--------|---------|-------|--------|")
        lines.append(f"| CSI | {report.summary['initial_csi']:.4f} | {report.summary['final_csi']:.4f} | {report.summary['csi_improvement']:+.1f}% |")
        lines.append(f"| Entropy | {report.summary['initial_entropy']:.4f} | {report.summary['final_entropy']:.4f} | {report.summary['entropy_reduction']:+.1f}% |")
        lines.append(f"| Lyapunov | {report.summary['initial_lyapunov']:.4f} | {report.summary['final_lyapunov']:.4f} | {report.summary['lyapunov_reduction']:+.1f}% |")
        lines.append("")
        lines.append("## Mathematical Framework")
        lines.append("")
        lines.append("```")
        lines.append("F_total = α·cohesion + β·(A₁ + A₂) - γ·v + σ·dW")
        lines.append("v(t+1) = v(t) + F_total·dt")
        lines.append("x(t+1) = x(t) + v(t+1)·dt")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("*Report generated by SWARMICA v8.0 Unified Field Control Engine*")
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("\n".join(lines))
        print(f"✅ Markdown saved: {filepath}")
        return filepath
    
    def save_csv(self, report: SwarmReport, filename: str = None) -> str:
        """Save metrics as CSV"""
        if filename is None:
            filename = f"swarm_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("step,csi,entropy,lyapunov\n")
            csi = report.history['csi']
            entropy = report.history['entropy']
            lyapunov = report.history['lyapunov']
            for i, (c, e, l) in enumerate(zip(csi, entropy, lyapunov)):
                f.write(f"{i},{c:.6f},{e:.6f},{l:.6f}\n")
        print(f"✅ CSV saved: {filepath}")
        return filepath
    
    def print_summary(self, report: SwarmReport):
        """Print summary to console"""
        print("\n" + "=" * 60)
        print("⚙️ SWARMICA v8.0 Simulation Summary")
        print("=" * 60)
        print(f"Status: {report.stability_analysis['status']}")
        print(f"Final CSI: {report.summary['final_csi']:.4f}")
        print(f"CSI Improvement: {report.summary['csi_improvement']:+.1f}%")
        print(f"Entropy Reduction: {report.summary['entropy_reduction']:.1f}%")
        print(f"Converged: {report.stability_analysis['converged']}")
        print("=" * 60)


def create_swarm_report_generator() -> SwarmReportGenerator:
    """Factory function for report generator"""
    return SwarmReportGenerator()
