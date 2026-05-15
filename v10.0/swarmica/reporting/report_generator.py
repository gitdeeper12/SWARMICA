"""Report Generator for SWARMICA v10.0 - Neural Field + Inverse Physics System"""

import json
import math
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class NeuralPhysicsReport:
    """Data class for Neural Physics simulation results"""
    timestamp: str
    config: Dict[str, Any]
    history: Dict[str, List[float]]
    summary: Dict[str, float]
    learning_analysis: Dict[str, Any]
    physics_discovery: Dict[str, Any]


class NeuralPhysicsReportGenerator:
    """Generate comprehensive reports from Neural Physics simulations"""
    
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir
    
    def generate_from_solver(self, solver) -> NeuralPhysicsReport:
        """Generate report from NeuralPDESolver instance"""
        config = {
            'N': solver.N,
            'dt': solver.dt,
            'dx': solver.dx,
            'nu': solver.nu,
            'gamma': solver.gamma,
            'learning': solver.learning
        }
        
        coherence_history = solver.history['coherence']
        entropy_history = solver.history['entropy']
        energy_loss_history = solver.history['energy_loss']
        
        # Learning analysis
        learning_analysis = self._analyze_learning(energy_loss_history, coherence_history)
        
        # Physics discovery
        physics_discovery = self._discover_physics(entropy_history, coherence_history)
        
        summary = {
            'final_coherence': coherence_history[-1] if coherence_history else 0,
            'initial_coherence': coherence_history[0] if coherence_history else 0,
            'coherence_improvement': ((coherence_history[-1] - coherence_history[0]) * 100) if coherence_history else 0,
            'final_entropy': entropy_history[-1] if entropy_history else 0,
            'initial_entropy': entropy_history[0] if entropy_history else 0,
            'entropy_reduction': ((entropy_history[0] - entropy_history[-1]) / (entropy_history[0] + 1e-8) * 100) if entropy_history else 0,
            'final_energy_loss': energy_loss_history[-1] if energy_loss_history else 0,
            'initial_energy_loss': energy_loss_history[0] if energy_loss_history else 0,
            'energy_loss_reduction': ((energy_loss_history[0] - energy_loss_history[-1]) / (energy_loss_history[0] + 1e-8) * 100) if energy_loss_history else 0
        }
        
        return NeuralPhysicsReport(
            timestamp=datetime.now().isoformat(),
            config=config,
            history={
                'coherence': coherence_history[-100:],
                'entropy': entropy_history[-100:],
                'energy_loss': energy_loss_history[-100:]
            },
            summary=summary,
            learning_analysis=learning_analysis,
            physics_discovery=physics_discovery
        )
    
    def _analyze_learning(self, energy_loss: List[float], coherence: List[float]) -> Dict[str, Any]:
        """Analyze learning progress"""
        if len(energy_loss) < 10:
            return {'status': 'Insufficient data'}
        
        final_loss = energy_loss[-1]
        initial_loss = energy_loss[0]
        loss_reduction = (initial_loss - final_loss) / (initial_loss + 1e-8) * 100
        
        final_coherence = coherence[-1]
        
        if loss_reduction > 50 and final_coherence > 0.8:
            learning_status = "Excellent - Physics successfully learned"
        elif loss_reduction > 30 and final_coherence > 0.6:
            learning_status = "Good - Physics partially learned"
        elif loss_reduction > 10:
            learning_status = "Moderate - Learning in progress"
        else:
            learning_status = "Poor - Learning not effective"
        
        return {
            'status': learning_status,
            'loss_reduction': loss_reduction,
            'final_loss': final_loss,
            'initial_loss': initial_loss,
            'learning_converged': loss_reduction > 30
        }
    
    def _discover_physics(self, entropy: List[float], coherence: List[float]) -> Dict[str, Any]:
        """Discover physical laws from dynamics"""
        if len(entropy) < 20:
            return {'status': 'Insufficient data'}
        
        entropy_trend = entropy[-1] - entropy[0]
        coherence_trend = coherence[-1] - coherence[0]
        
        # Discover law type
        if coherence_trend > 0.2:
            law_type = "Self-Organization"
            law_equation = "∂C/∂t > 0 → System ordering"
        elif coherence_trend < -0.2:
            law_type = "Dissipation"
            law_equation = "∂C/∂t < 0 → System disordering"
        else:
            law_type = "Meta-Stability"
            law_equation = "∂C/∂t ≈ 0 → Critical state"
        
        return {
            'status': law_type,
            'discovered_law': law_equation,
            'entropy_trend': entropy_trend,
            'coherence_trend': coherence_trend,
            'system_behavior': self._classify_behavior(entropy_trend, coherence_trend)
        }
    
    def _classify_behavior(self, entropy_trend: float, coherence_trend: float) -> str:
        if coherence_trend > 0 and entropy_trend < 0:
            return "Ordering (Energy minimization)"
        elif coherence_trend < 0 and entropy_trend > 0:
            return "Chaotic (Energy increase)"
        else:
            return "Critical (Phase transition)"
    
    def save_json(self, report: NeuralPhysicsReport, filename: str = None) -> str:
        if filename is None:
            filename = f"neural_physics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            json.dump(asdict(report), f, indent=2)
        print(f"✅ JSON saved: {filepath}")
        return filepath
    
    def save_markdown(self, report: NeuralPhysicsReport, filename: str = None) -> str:
        if filename is None:
            filename = f"neural_physics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        lines = []
        lines.append(f"# SWARMICA v10.0 Neural Physics Report")
        lines.append(f"*Generated: {report.timestamp}*")
        lines.append("")
        lines.append("## Configuration")
        for k, v in report.config.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")
        lines.append("## Learning Analysis")
        lines.append(f"- **Status**: {report.learning_analysis['status']}")
        lines.append(f"- **Loss Reduction**: {report.learning_analysis['loss_reduction']:.1f}%")
        lines.append(f"- **Learning Converged**: {report.learning_analysis['learning_converged']}")
        lines.append("")
        lines.append("## Physics Discovery")
        lines.append(f"- **Discovered Law**: {report.physics_discovery['discovered_law']}")
        lines.append(f"- **System Behavior**: {report.physics_discovery['system_behavior']}")
        lines.append(f"- **Entropy Trend**: {report.physics_discovery['entropy_trend']:+.4f}")
        lines.append(f"- **Coherence Trend**: {report.physics_discovery['coherence_trend']:+.4f}")
        lines.append("")
        lines.append("## Summary Metrics")
        lines.append("| Metric | Initial | Final | Change |")
        lines.append("|--------|---------|-------|--------|")
        lines.append(f"| Coherence | {report.summary['initial_coherence']:.4f} | {report.summary['final_coherence']:.4f} | {report.summary['coherence_improvement']:+.1f}% |")
        lines.append(f"| Entropy | {report.summary['initial_entropy']:.4f} | {report.summary['final_entropy']:.4f} | {report.summary['entropy_reduction']:+.1f}% |")
        lines.append(f"| Energy Loss | {report.summary['initial_energy_loss']:.4f} | {report.summary['final_energy_loss']:.4f} | {report.summary['energy_loss_reduction']:+.1f}% |")
        lines.append("")
        lines.append("## Neural Physics Formulation")
        lines.append("```")
        lines.append("∂ρ/∂t = -∇·(ρv)")
        lines.append("∂v/∂t = -∇E_θ(ρ) - γv + ν∇²v")
        lines.append("E_θ(ρ) = tanh(mean(ρ)) + var(ρ) + θ·mean(ρ²)")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("*Report generated by SWARMICA v10.0 Neural Physics Engine*")
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("\n".join(lines))
        print(f"✅ Markdown saved: {filepath}")
        return filepath
    
    def save_csv(self, report: NeuralPhysicsReport, filename: str = None) -> str:
        if filename is None:
            filename = f"neural_physics_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("step,coherence,entropy,energy_loss\n")
            coherence = report.history['coherence']
            entropy = report.history['entropy']
            energy_loss = report.history['energy_loss']
            for i, (c, e, el) in enumerate(zip(coherence, entropy, energy_loss)):
                f.write(f"{i},{c:.6f},{e:.6f},{el:.6f}\n")
        print(f"✅ CSV saved: {filepath}")
        return filepath
    
    def print_summary(self, report: NeuralPhysicsReport):
        print("\n" + "=" * 60)
        print("🧠 SWARMICA v10.0 Neural Physics Summary")
        print("=" * 60)
        print(f"Learning Status: {report.learning_analysis['status']}")
        print(f"Discovered Law: {report.physics_discovery['discovered_law']}")
        print(f"System Behavior: {report.physics_discovery['system_behavior']}")
        print(f"Final Coherence: {report.summary['final_coherence']:.4f}")
        print(f"Learning Converged: {report.learning_analysis['learning_converged']}")
        print("=" * 60)


def create_neural_physics_report_generator() -> NeuralPhysicsReportGenerator:
    return NeuralPhysicsReportGenerator()
