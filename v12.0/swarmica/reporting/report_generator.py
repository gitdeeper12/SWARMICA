"""Report Generator for SWARMICA v12.0 - Constrained Neural Physics"""

import json
import math
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class ConstrainedPhysicsReport:
    """Data class for Constrained Physics simulation results"""
    timestamp: str
    config: Dict[str, Any]
    history: Dict[str, List[float]]
    summary: Dict[str, float]
    conservation_report: Dict[str, Any]
    hamiltonian_analysis: Dict[str, Any]


class ConstrainedPhysicsReportGenerator:
    """Generate comprehensive reports from Constrained Physics simulations"""
    
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir
    
    def generate_from_solver(self, solver) -> ConstrainedPhysicsReport:
        """Generate report from ConstrainedNeuralSolver instance"""
        config = {
            'N': solver.N,
            'dt': solver.dt,
            'learning': solver.learning
        }
        
        mass_history = solver.history['mass']
        energy_history = solver.history['energy']
        entropy_history = solver.history['entropy']
        coherence_history = solver.history['coherence']
        
        # Conservation report
        conservation_report = solver.get_conservation_report()
        
        # Hamiltonian analysis
        ham_params = solver.hamiltonian.get_parameters()
        hamiltonian_analysis = self._analyze_hamiltonian(ham_params, energy_history)
        
        summary = {
            'final_coherence': coherence_history[-1] if coherence_history else 0,
            'initial_coherence': coherence_history[0] if coherence_history else 0,
            'coherence_improvement': ((coherence_history[-1] - coherence_history[0]) * 100) if coherence_history else 0,
            'final_energy': energy_history[-1] if energy_history else 0,
            'initial_energy': energy_history[0] if energy_history else 0,
            'energy_reduction': ((energy_history[0] - energy_history[-1]) / (energy_history[0] + 1e-8) * 100) if energy_history else 0,
            'final_entropy': entropy_history[-1] if entropy_history else 0,
            'mass_conserved': conservation_report.get('mass_conserved', False),
            'mass_variation': conservation_report.get('mass_variation', 0)
        }
        
        return ConstrainedPhysicsReport(
            timestamp=datetime.now().isoformat(),
            config=config,
            history={
                'coherence': coherence_history[-100:],
                'energy': energy_history[-100:],
                'entropy': entropy_history[-100:],
                'mass': mass_history[-100:]
            },
            summary=summary,
            conservation_report=conservation_report,
            hamiltonian_analysis=hamiltonian_analysis
        )
    
    def _analyze_hamiltonian(self, ham_params: Dict, energy_history: List[float]) -> Dict[str, Any]:
        """Analyze Hamiltonian structure"""
        if len(energy_history) < 10:
            return {'status': 'Insufficient data'}
        
        energy_final = energy_history[-1]
        energy_initial = energy_history[0]
        energy_reduction = (energy_initial - energy_final) / (energy_initial + 1e-8) * 100
        
        if energy_reduction > 50:
            status = "Excellent - Energy minimization"
        elif energy_reduction > 30:
            status = "Good - Energy decreasing"
        elif energy_reduction > 10:
            status = "Moderate - Slow minimization"
        else:
            status = "Poor - No minimization"
        
        return {
            'status': status,
            'energy_reduction': energy_reduction,
            'rho_potential_mean': ham_params.get('rho_potential_mean', 0),
            'kinetic_mean': ham_params.get('kinetic_mean', 0),
            'hamiltonian_structure': 'Symplectic'
        }
    
    def save_json(self, report: ConstrainedPhysicsReport, filename: str = None) -> str:
        if filename is None:
            filename = f"constrained_physics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            json.dump(asdict(report), f, indent=2)
        print(f"✅ JSON saved: {filepath}")
        return filepath
    
    def save_markdown(self, report: ConstrainedPhysicsReport, filename: str = None) -> str:
        if filename is None:
            filename = f"constrained_physics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        lines = []
        lines.append(f"# SWARMICA v12.0 Constrained Physics Report")
        lines.append(f"*Generated: {report.timestamp}*")
        lines.append("")
        lines.append("## Configuration")
        for k, v in report.config.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")
        lines.append("## Conservation Laws")
        lines.append(f"- **Mass Conserved**: {report.conservation_report.get('mass_conserved', False)}")
        lines.append(f"- **Mass Variation**: {report.conservation_report.get('mass_variation', 0):.6f}")
        lines.append(f"- **Symplectic Structure**: {report.conservation_report.get('symplectic_structure', 'N/A')}")
        lines.append("")
        lines.append("## Hamiltonian Analysis")
        lines.append(f"- **Status**: {report.hamiltonian_analysis['status']}")
        lines.append(f"- **Energy Reduction**: {report.hamiltonian_analysis['energy_reduction']:.1f}%")
        lines.append(f"- **Structure**: {report.hamiltonian_analysis['hamiltonian_structure']}")
        lines.append("")
        lines.append("## Summary Metrics")
        lines.append("| Metric | Initial | Final | Change |")
        lines.append("|--------|---------|-------|--------|")
        lines.append(f"| Coherence | {report.summary['initial_coherence']:.4f} | {report.summary['final_coherence']:.4f} | {report.summary['coherence_improvement']:+.1f}% |")
        lines.append(f"| Energy | {report.summary['initial_energy']:.4f} | {report.summary['final_energy']:.4f} | {report.summary['energy_reduction']:.1f}% |")
        lines.append(f"| Mass | - | {report.summary['final_energy']:.4f} | Conserved: {report.summary['mass_conserved']} |")
        lines.append("")
        lines.append("## Hamiltonian Formulation")
        lines.append("```")
        lines.append("Hθ(ρ, v) = H_ρ(ρ) + H_v(v)")
        lines.append("∂u/∂t = J ∇Hθ(u)")
        lines.append("∫ρ dx = constant")
        lines.append("dS/dt ≥ 0")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("*Report generated by SWARMICA v12.0 Constrained Physics Engine*")
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("\n".join(lines))
        print(f"✅ Markdown saved: {filepath}")
        return filepath
    
    def save_csv(self, report: ConstrainedPhysicsReport, filename: str = None) -> str:
        if filename is None:
            filename = f"constrained_physics_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = f"{self.reports_dir}/{filename}"
        with open(filepath, 'w') as f:
            f.write("step,coherence,energy,entropy,mass\n")
            coherence = report.history['coherence']
            energy = report.history['energy']
            entropy = report.history['entropy']
            mass = report.history['mass']
            
            max_len = max(len(coherence), len(energy), len(entropy), len(mass))
            for i in range(max_len):
                c = coherence[i] if i < len(coherence) else 0
                e = energy[i] if i < len(energy) else 0
                ent = entropy[i] if i < len(entropy) else 0
                m = mass[i] if i < len(mass) else 0
                f.write(f"{i},{c:.6f},{e:.6f},{ent:.6f},{m:.6f}\n")
        print(f"✅ CSV saved: {filepath}")
        return filepath
    
    def print_summary(self, report: ConstrainedPhysicsReport):
        print("\n" + "=" * 60)
        print("🔬 SWARMICA v12.0 Constrained Physics Summary")
        print("=" * 60)
        print(f"Mass Conserved: {report.conservation_report.get('mass_conserved', False)}")
        print(f"Hamiltonian Status: {report.hamiltonian_analysis['status']}")
        print(f"Final Coherence: {report.summary['final_coherence']:.4f}")
        print(f"Energy Reduction: {report.hamiltonian_analysis['energy_reduction']:.1f}%")
        print("=" * 60)


def create_constrained_physics_report_generator() -> ConstrainedPhysicsReportGenerator:
    return ConstrainedPhysicsReportGenerator()
