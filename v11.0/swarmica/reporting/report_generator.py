"""Report Generator for SWARMICA v11.0 - Neural Operator Swarm Physics"""

import json
import math
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class NeuralOperatorReport:
    """Data class for Neural Operator simulation results"""
    timestamp: str
    config: Dict[str, Any]
    history: Dict[str, List[float]]
    summary: Dict[str, float]
    operator_analysis: Dict[str, Any]
    law_discovery: Dict[str, Any]


class NeuralOperatorReportGenerator:
    """Generate comprehensive reports from Neural Operator simulations"""
    
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir
    
    def generate_from_solver(self, solver) -> NeuralOperatorReport:
        """Generate report from NeuralOperatorSolver instance"""
        config = {
            'N': solver.N,
            'dt': solver.dt,
            'learning': solver.learning
        }
        
        coherence_history = solver.history['coherence']
        entropy_history = solver.history['entropy']
        energy_history = solver.history['energy']
        loss_history = solver.history['operator_loss']
        
        # Operator analysis
        op_info = solver.get_operator_info()
        operator_analysis = self._analyze_operator(op_info, loss_history)
        
        # Law discovery - use W if available (simplified version)
        if hasattr(solver.operator, 'W'):
            W_real = solver.operator.W
            W_imag = [[0.0 for _ in range(solver.N)] for __ in range(solver.N)]
        else:
            W_real = [[0.0 for _ in range(solver.N)] for __ in range(solver.N)]
            W_imag = [[0.0 for _ in range(solver.N)] for __ in range(solver.N)]
        
        discovery = self._discover_law(W_real, W_imag, solver.N)
        
        summary = {
            'final_coherence': coherence_history[-1] if coherence_history else 0,
            'initial_coherence': coherence_history[0] if coherence_history else 0,
            'coherence_improvement': ((coherence_history[-1] - coherence_history[0]) * 100) if coherence_history else 0,
            'final_entropy': entropy_history[-1] if entropy_history else 0,
            'initial_entropy': entropy_history[0] if entropy_history else 0,
            'entropy_reduction': ((entropy_history[0] - entropy_history[-1]) / (entropy_history[0] + 1e-8) * 100) if entropy_history else 0,
            'final_energy': energy_history[-1] if energy_history else 0,
            'operator_loss_final': loss_history[-1] if loss_history else 0,
            'operator_norm': op_info['operator_norm']
        }
        
        return NeuralOperatorReport(
            timestamp=datetime.now().isoformat(),
            config=config,
            history={
                'coherence': coherence_history[-100:],
                'entropy': entropy_history[-100:],
                'energy': energy_history[-100:],
                'operator_loss': loss_history[-100:] if loss_history else []
            },
            summary=summary,
            operator_analysis=operator_analysis,
            law_discovery=discovery
        )
    
    def _analyze_operator(self, op_info: Dict, loss_history: List[float]) -> Dict[str, Any]:
        """Analyze neural operator performance"""
        if len(loss_history) < 10:
            return {'status': 'Insufficient data', 'loss_reduction': 0, 'operator_norm': op_info['operator_norm']}
        
        final_loss = loss_history[-1]
        initial_loss = loss_history[0]
        loss_reduction = (initial_loss - final_loss) / (initial_loss + 1e-8) * 100
        
        if loss_reduction > 70:
            operator_status = "Excellent - Operator well-trained"
        elif loss_reduction > 50:
            operator_status = "Good - Operator learning"
        elif loss_reduction > 30:
            operator_status = "Moderate - Partial learning"
        elif loss_reduction > 10:
            operator_status = "Poor - Limited learning"
        else:
            operator_status = "Ineffective - No learning"
        
        return {
            'status': operator_status,
            'loss_reduction': loss_reduction,
            'final_loss': final_loss,
            'operator_norm': op_info['operator_norm'],
            'real_mean': op_info.get('real_mean', 0),
            'imag_mean': op_info.get('imag_mean', 0)
        }
    
    def _discover_law(self, W_real: List[List[float]], W_imag: List[List[float]], N: int) -> Dict[str, Any]:
        """Discover physical law from operator weights"""
        # Compute statistics
        real_mean = 0.0
        real_std = 0.0
        
        for i in range(N):
            for j in range(N):
                real_mean += W_real[i][j]
        
        real_mean /= (N * N)
        
        for i in range(N):
            for j in range(N):
                real_std += (W_real[i][j] - real_mean) ** 2
        real_std = math.sqrt(real_std / (N * N))
        
        # Discover law type based on weight distribution
        if real_std < 0.05:
            law_type = "Homogeneous Linear PDE"
            law_equation = "∂ρ/∂t = κ∇²ρ + f(x)"
        elif real_std > 0.2:
            law_type = "Nonlinear Reaction-Diffusion"
            law_equation = "∂ρ/∂t = D∇²ρ + R(ρ)"
        else:
            law_type = "Mixed (Conservation + Dissipation)"
            law_equation = "∂ρ/∂t = -∇·(ρv) + D∇²ρ"
        
        # Determine system behavior
        if real_mean > 0:
            behavior = "Source-dominant (Energy increasing)"
        elif real_mean < 0:
            behavior = "Sink-dominant (Energy decreasing)"
        else:
            behavior = "Conservative (Energy preserving)"
        
        return {
            'discovered_law': law_type,
            'law_equation': law_equation,
            'system_behavior': behavior,
            'operator_mean': real_mean,
            'operator_std': real_std,
            'complexity': real_std
        }
    
    def save_json(self, report: NeuralOperatorReport, filename: str = None) -> str:
        """Save report as JSON"""
        if filename is None:
            filename = f"neural_operator_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            json.dump(asdict(report), f, indent=2)
        print(f"✅ JSON saved: {filepath}")
        return filepath
    
    def save_markdown(self, report: NeuralOperatorReport, filename: str = None) -> str:
        """Save report as Markdown"""
        if filename is None:
            filename = f"neural_operator_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        lines = []
        lines.append(f"# SWARMICA v11.0 Neural Operator Report")
        lines.append(f"*Generated: {report.timestamp}*")
        lines.append("")
        lines.append("## Configuration")
        for k, v in report.config.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")
        lines.append("## Operator Analysis")
        lines.append(f"- **Status**: {report.operator_analysis['status']}")
        lines.append(f"- **Loss Reduction**: {report.operator_analysis['loss_reduction']:.1f}%")
        lines.append(f"- **Operator Norm**: {report.operator_analysis['operator_norm']:.4f}")
        lines.append("")
        lines.append("## Physics Law Discovery")
        lines.append(f"- **Discovered Law**: {report.law_discovery['discovered_law']}")
        lines.append(f"- **Law Equation**: {report.law_discovery['law_equation']}")
        lines.append(f"- **System Behavior**: {report.law_discovery['system_behavior']}")
        lines.append(f"- **Operator Complexity**: {report.law_discovery['complexity']:.4f}")
        lines.append("")
        lines.append("## Summary Metrics")
        lines.append("| Metric | Initial | Final | Change |")
        lines.append("|--------|---------|-------|--------|")
        lines.append(f"| Coherence | {report.summary['initial_coherence']:.4f} | {report.summary['final_coherence']:.4f} | {report.summary['coherence_improvement']:+.1f}% |")
        lines.append(f"| Entropy | {report.summary['initial_entropy']:.4f} | {report.summary['final_entropy']:.4f} | {report.summary['entropy_reduction']:+.1f}% |")
        lines.append(f"| Operator Loss | - | {report.summary['operator_loss_final']:.4f} | - |")
        lines.append("")
        lines.append("## Neural Operator Formulation")
        lines.append("```")
        lines.append("u = (ρ, v)")
        lines.append("∂u/∂t = Fθ(u, ∇u, x)")
        lines.append("Fθ = W·u + nonlinear activation")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("*Report generated by SWARMICA v11.0 Neural Operator Engine*")
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("\n".join(lines))
        print(f"✅ Markdown saved: {filepath}")
        return filepath
    
    def save_csv(self, report: NeuralOperatorReport, filename: str = None) -> str:
        """Save metrics as CSV"""
        if filename is None:
            filename = f"neural_operator_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("step,coherence,entropy,energy,operator_loss\n")
            coherence = report.history['coherence']
            entropy = report.history['entropy']
            energy = report.history['energy']
            loss = report.history['operator_loss']
            
            max_len = max(len(coherence), len(entropy), len(energy), len(loss))
            for i in range(max_len):
                c = coherence[i] if i < len(coherence) else 0
                e = entropy[i] if i < len(entropy) else 0
                en = energy[i] if i < len(energy) else 0
                l = loss[i] if i < len(loss) else 0
                f.write(f"{i},{c:.6f},{e:.6f},{en:.6f},{l:.6f}\n")
        print(f"✅ CSV saved: {filepath}")
        return filepath
    
    def print_summary(self, report: NeuralOperatorReport):
        """Print summary to console"""
        print("\n" + "=" * 60)
        print("🧠 SWARMICA v11.0 Neural Operator Summary")
        print("=" * 60)
        print(f"Operator Status: {report.operator_analysis['status']}")
        print(f"Discovered Law: {report.law_discovery['discovered_law']}")
        print(f"System Behavior: {report.law_discovery['system_behavior']}")
        print(f"Final Coherence: {report.summary['final_coherence']:.4f}")
        print(f"Operator Norm: {report.operator_analysis['operator_norm']:.4f}")
        print("=" * 60)


def create_neural_operator_report_generator() -> NeuralOperatorReportGenerator:
    """Factory function for report generator"""
    return NeuralOperatorReportGenerator()
