"""Report Generator for SWARMICA v2.0 - Generate simulation reports and metrics"""

import json
import math
from datetime import datetime
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class SimulationReport:
    """Data class for simulation results"""
    timestamp: str
    config: Dict[str, Any]
    metrics: Dict[str, List[float]]
    summary: Dict[str, float]
    stability_analysis: Dict[str, Any]


class ReportGenerator:
    """Generate comprehensive reports from SWARMICA simulations"""
    
    def __init__(self):
        self.reports = []
    
    def generate_from_controller(self, controller, config: Dict[str, Any] = None) -> SimulationReport:
        """Generate report from SwarmController instance"""
        from .control.swarm_controller import SwarmControllerV2
        
        if config is None:
            config = {
                'n_agents': controller.n_agents,
                'grid_size': controller.grid_size,
                'alpha': controller.alpha,
                'beta': controller.beta,
                'noise': controller.noise,
                'inertia': controller.inertia,
                'dt': controller.dt
            }
        
        # Compute additional metrics
        csi_history = controller.history['csi']
        entropy_history = controller.history['entropy']
        lyapunov_history = controller.history['lyapunov']
        
        # Stability analysis
        stability_analysis = self._analyze_stability(csi_history, entropy_history)
        
        # Summary metrics
        summary = {
            'final_csi': csi_history[-1] if csi_history else 0,
            'final_entropy': entropy_history[-1] if entropy_history else 0,
            'final_lyapunov': lyapunov_history[-1] if lyapunov_history else 0,
            'mean_csi': sum(csi_history) / len(csi_history) if csi_history else 0,
            'mean_entropy': sum(entropy_history) / len(entropy_history) if entropy_history else 0,
            'csi_improvement': ((csi_history[-1] - csi_history[0]) * 100) if len(csi_history) > 1 else 0,
            'entropy_reduction': ((entropy_history[0] - entropy_history[-1]) / (entropy_history[0] + 1e-8) * 100) if entropy_history else 0,
            'csi_variance': self._variance(csi_history) if csi_history else 0,
            'convergence_step': self._find_convergence_step(csi_history, threshold=0.9)
        }
        
        report = SimulationReport(
            timestamp=datetime.now().isoformat(),
            config=config,
            metrics={
                'csi': csi_history,
                'entropy': entropy_history,
                'lyapunov': lyapunov_history
            },
            summary=summary,
            stability_analysis=stability_analysis
        )
        
        self.reports.append(report)
        return report
    
    def _variance(self, data: List[float]) -> float:
        """Compute variance of a list"""
        if len(data) < 2:
            return 0.0
        mean = sum(data) / len(data)
        return sum((x - mean) ** 2 for x in data) / len(data)
    
    def _find_convergence_step(self, csi_history: List[float], threshold: float = 0.9) -> int:
        """Find step where CSI first exceeds threshold"""
        for i, csi in enumerate(csi_history):
            if csi >= threshold:
                return i
        return -1
    
    def _analyze_stability(self, csi_history: List[float], entropy_history: List[float]) -> Dict[str, Any]:
        """Analyze stability characteristics"""
        if len(csi_history) < 10:
            return {'status': 'Insufficient data'}
        
        # Calculate trends
        recent_csi = csi_history[-10:]
        recent_entropy = entropy_history[-10:]
        
        csi_trend = recent_csi[-1] - recent_csi[0]
        entropy_trend = recent_entropy[0] - recent_entropy[-1]
        
        # Stability classification
        final_csi = csi_history[-1]
        if final_csi >= 0.95:
            stability_status = "Excellent"
        elif final_csi >= 0.90:
            stability_status = "Good"
        elif final_csi >= 0.80:
            stability_status = "Fair"
        elif final_csi >= 0.70:
            stability_status = "Poor"
        else:
            stability_status = "Unstable"
        
        # Convergence assessment
        converged = final_csi >= 0.9
        
        return {
            'status': stability_status,
            'converged': converged,
            'csi_trend': csi_trend,
            'entropy_trend': entropy_trend,
            'final_csi': final_csi,
            'csi_stability': self._variance(recent_csi),
            'recommendation': self._get_recommendation(stability_status, csi_trend)
        }
    
    def _get_recommendation(self, status: str, trend: float) -> str:
        """Generate recommendation based on stability status"""
        if status == "Excellent":
            return "System is stable. Consider reducing control gain for energy efficiency."
        elif status == "Good":
            return "System is stable. Fine-tuning may improve performance."
        elif status == "Fair":
            return "Consider increasing cohesion strength (α) or attractor strength (β)."
        elif status == "Poor":
            return "Increase control gains significantly. Check noise levels."
        else:
            return "System requires major parameter adjustment. Reduce noise and increase cohesion."
    
    def save_json(self, report: SimulationReport, filename: str = None) -> str:
        """Save report as JSON file"""
        if filename is None:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Convert to serializable dict
        data = asdict(report)
        # Truncate long metric histories for file size
        data['metrics']['csi'] = data['metrics']['csi'][-100:]  # Keep last 100
        data['metrics']['entropy'] = data['metrics']['entropy'][-100:]
        data['metrics']['lyapunov'] = data['metrics']['lyapunov'][-100:]
        
        filepath = f"reports/{filename}"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Report saved: {filepath}")
        return filepath
    
    def save_markdown(self, report: SimulationReport, filename: str = None) -> str:
        """Save report as Markdown file"""
        if filename is None:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        lines = []
        lines.append(f"# SWARMICA v2.0 Simulation Report")
        lines.append(f"*Generated: {report.timestamp}*")
        lines.append("")
        lines.append("## Configuration")
        lines.append("")
        for key, value in report.config.items():
            lines.append(f"- **{key}**: {value}")
        lines.append("")
        lines.append("## Summary Metrics")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Final CSI | {report.summary['final_csi']:.4f} |")
        lines.append(f"| Final Entropy | {report.summary['final_entropy']:.4f} |")
        lines.append(f"| Final Lyapunov | {report.summary['final_lyapunov']:.4f} |")
        lines.append(f"| Mean CSI | {report.summary['mean_csi']:.4f} |")
        lines.append(f"| CSI Improvement | {report.summary['csi_improvement']:+.1f}% |")
        lines.append(f"| Entropy Reduction | {report.summary['entropy_reduction']:.1f}% |")
        lines.append(f"| Convergence Step | {report.summary['convergence_step']} |")
        lines.append("")
        lines.append("## Stability Analysis")
        lines.append("")
        sa = report.stability_analysis
        lines.append(f"- **Status**: {sa.get('status', 'N/A')}")
        lines.append(f"- **Converged**: {sa.get('converged', False)}")
        lines.append(f"- **CSI Trend**: {sa.get('csi_trend', 0):+.4f}")
        lines.append(f"- **Recommendation**: {sa.get('recommendation', 'N/A')}")
        lines.append("")
        lines.append("## Raw Metrics (Last 10 steps)")
        lines.append("")
        lines.append("| Step | CSI | Entropy | Lyapunov |")
        lines.append("|------|-----|---------|----------|")
        
        csi = report.metrics['csi'][-10:]
        entropy = report.metrics['entropy'][-10:]
        lyap = report.metrics['lyapunov'][-10:]
        
        for i, (c, e, l) in enumerate(zip(csi, entropy, lyap)):
            step_idx = len(report.metrics['csi']) - 10 + i
            lines.append(f"| {step_idx} | {c:.4f} | {e:.4f} | {l:.4f} |")
        
        lines.append("")
        lines.append("---")
        lines.append("*Report generated by SWARMICA v2.0*")
        
        filepath = f"reports/{filename}"
        with open(filepath, 'w') as f:
            f.write("\n".join(lines))
        print(f"✅ Markdown report saved: {filepath}")
        return filepath
    
    def save_csv(self, report: SimulationReport, filename: str = None) -> str:
        """Save metrics as CSV file"""
        if filename is None:
            filename = f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = f"reports/{filename}"
        with open(filepath, 'w') as f:
            f.write("step,csi,entropy,lyapunov\n")
            csi = report.metrics['csi']
            entropy = report.metrics['entropy']
            lyap = report.metrics['lyapunov']
            for i, (c, e, l) in enumerate(zip(csi, entropy, lyap)):
                f.write(f"{i},{c:.6f},{e:.6f},{l:.6f}\n")
        
        print(f"✅ CSV saved: {filepath}")
        return filepath
    
    def print_summary(self, report: SimulationReport):
        """Print summary to console"""
        print("\n" + "=" * 60)
        print("📊 SWARMICA v2.0 Simulation Summary")
        print("=" * 60)
        print(f"Timestamp: {report.timestamp}")
        print()
        print("Configuration:")
        for key, value in report.config.items():
            print(f"  {key}: {value}")
        print()
        print("Results:")
        print(f"  Final CSI:      {report.summary['final_csi']:.4f}")
        print(f"  Final Entropy:  {report.summary['final_entropy']:.4f}")
        print(f"  CSI Improvement: {report.summary['csi_improvement']:+.1f}%")
        print(f"  Convergence at: step {report.summary['convergence_step']}")
        print()
        print(f"Stability Status: {report.stability_analysis.get('status', 'N/A')}")
        print(f"Recommendation: {report.stability_analysis.get('recommendation', 'N/A')}")
        print("=" * 60)


def create_report_generator() -> ReportGenerator:
    """Factory function for ReportGenerator"""
    return ReportGenerator()
