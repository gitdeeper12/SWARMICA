"""Advanced metrics calculator for SWARMICA v11.0 - Neural Operator System"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class MetricsCalculator:
    """Compute advanced metrics for neural operator dynamics"""
    
    N: int = 64
    
    def shannon_entropy(self, rho: List[List[float]]) -> float:
        """Shannon entropy: H = -Σ p log(p)"""
        total = 0.0
        for i in range(self.N):
            for j in range(self.N):
                total += rho[i][j]
        
        if total < 1e-8:
            return 0.0
        
        entropy = 0.0
        for i in range(self.N):
            for j in range(self.N):
                p = rho[i][j] / total
                if p > 1e-8:
                    entropy -= p * math.log(p)
        
        return entropy
    
    def coherence_index(self, rho: List[List[float]]) -> float:
        """Coherence index: C = 1/(1+var(ρ))"""
        mean = 0.0
        for i in range(self.N):
            for j in range(self.N):
                mean += rho[i][j]
        mean /= (self.N * self.N)
        
        variance = 0.0
        for i in range(self.N):
            for j in range(self.N):
                variance += (rho[i][j] - mean) ** 2
        variance /= (self.N * self.N)
        
        return 1.0 / (1.0 + variance)
    
    def total_energy(self, rho: List[List[float]], 
                     vx: List[List[float]], vy: List[List[float]]) -> float:
        """Total energy: E = ∫ρ² dx + ½∫|v|² dx"""
        potential = 0.0
        kinetic = 0.0
        
        for i in range(self.N):
            for j in range(self.N):
                potential += rho[i][j] * rho[i][j]
                kinetic += 0.5 * (vx[i][j] * vx[i][j] + vy[i][j] * vy[i][j])
        
        return (potential + kinetic) / (self.N * self.N)
    
    def operator_gain(self, W_real: List[List[float]], W_imag: List[List[float]]) -> float:
        """Operator gain: average magnitude of learned weights"""
        total = 0.0
        for i in range(self.N):
            for j in range(self.N):
                total += math.sqrt(W_real[i][j] * W_real[i][j] + W_imag[i][j] * W_imag[i][j])
        return total / (self.N * self.N)
    
    def spectral_entropy(self, spectrum: List[float]) -> float:
        """Spectral entropy: measures complexity of learned operator"""
        total = sum(spectrum)
        if total < 1e-8:
            return 0.0
        
        entropy = 0.0
        for s in spectrum:
            p = s / total
            if p > 1e-8:
                entropy -= p * math.log(p)
        
        return entropy / math.log(len(spectrum)) if spectrum else 0.0
    
    def prediction_error(self, pred: List[List[float]], target: List[List[float]]) -> float:
        """Prediction error: MSE between predicted and true dynamics"""
        mse = 0.0
        for i in range(self.N):
            for j in range(self.N):
                diff = pred[i][j] - target[i][j]
                mse += diff * diff
        return mse / (self.N * self.N)
    
    def operator_stability(self, W_real: List[List[float]], W_imag: List[List[float]]) -> str:
        """Assess operator stability based on weight distribution"""
        gain = self.operator_gain(W_real, W_imag)
        
        if gain < 0.1:
            return "Stable (Low gain)"
        elif gain < 0.3:
            return "Moderately stable"
        elif gain < 0.5:
            return "Critical (Moderate gain)"
        else:
            return "Unstable (High gain)"
    
    def learning_progress(self, loss_history: List[float]) -> Dict[str, Any]:
        """Analyze learning progress from loss history"""
        if len(loss_history) < 10:
            return {'status': 'Insufficient data'}
        
        initial_loss = loss_history[0]
        final_loss = loss_history[-1]
        loss_reduction = (initial_loss - final_loss) / (initial_loss + 1e-8) * 100
        
        # Check for convergence
        recent_losses = loss_history[-20:]
        recent_std = 0.0
        if recent_losses:
            mean_recent = sum(recent_losses) / len(recent_losses)
            recent_std = math.sqrt(sum((l - mean_recent) ** 2 for l in recent_losses) / len(recent_losses))
        
        converged = recent_std < 0.01 and loss_reduction > 50
        
        if loss_reduction > 70:
            status = "Excellent - Fast convergence"
        elif loss_reduction > 50:
            status = "Good - Steady learning"
        elif loss_reduction > 30:
            status = "Moderate - Slow learning"
        elif loss_reduction > 10:
            status = "Poor - Limited progress"
        else:
            status = "Ineffective - No learning"
        
        return {
            'status': status,
            'loss_reduction': loss_reduction,
            'final_loss': final_loss,
            'initial_loss': initial_loss,
            'converged': converged,
            'stability': recent_std
        }
    
    def get_all_metrics(self, rho: List[List[float]], vx: List[List[float]], vy: List[List[float]],
                        W_real: List[List[float]], W_imag: List[List[float]],
                        loss_history: List[float] = None) -> Dict[str, Any]:
        """Compute all metrics at once"""
        metrics = {
            'entropy': self.shannon_entropy(rho),
            'coherence': self.coherence_index(rho),
            'total_energy': self.total_energy(rho, vx, vy),
            'operator_gain': self.operator_gain(W_real, W_imag),
            'operator_stability': self.operator_stability(W_real, W_imag)
        }
        
        if loss_history:
            metrics['learning'] = self.learning_progress(loss_history)
        
        return metrics


def create_metrics_calculator(N: int = 64) -> MetricsCalculator:
    """Factory function for metrics calculator"""
    return MetricsCalculator(N=N)
