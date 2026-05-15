"""Lyapunov stability analysis for SWARMICA v7.0"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class LyapunovStability:
    """Lyapunov functional for variational stability proof"""
    
    n: int = 100
    lambda_reg: float = 0.5   # Regularization parameter
    
    def energy_functional(self, rho: List[List[float]], target: List[List[float]], 
                          laplacian: List[List[float]]) -> float:
        """Energy functional: E[ρ] = ∫(ρ - ρ*)² dx + λ∫‖∇²ρ‖² dx"""
        # First term: deviation from target
        deviation = 0.0
        for i in range(self.n):
            for j in range(self.n):
                deviation += (rho[i][j] - target[i][j]) ** 2
        
        # Second term: spatial curvature (regularization)
        curvature = 0.0
        for i in range(self.n):
            for j in range(self.n):
                curvature += laplacian[i][j] ** 2
        
        return deviation + self.lambda_reg * curvature
    
    def lyapunov_function(self, rho: List[List[float]], target: List[List[float]],
                          grad_rho: List[List[float]]) -> float:
        """Lyapunov functional: V[ρ] = ∫(ρ - ρ*)² dx + ∫|∇ρ|² dx"""
        # Potential term
        potential = 0.0
        for i in range(self.n):
            for j in range(self.n):
                potential += (rho[i][j] - target[i][j]) ** 2
        
        # Kinetic term (gradient norm)
        kinetic = 0.0
        for i in range(self.n):
            for j in range(self.n):
                kinetic += grad_rho[i][j] ** 2
        
        return potential + kinetic
    
    def stability_metric(self, rho: List[List[float]]) -> float:
        """Stability metric: 1 / (1 + variance(ρ))"""
        # Compute mean
        total = 0.0
        for i in range(self.n):
            for j in range(self.n):
                total += rho[i][j]
        mean = total / (self.n * self.n)
        
        # Compute variance
        variance = 0.0
        for i in range(self.n):
            for j in range(self.n):
                variance += (rho[i][j] - mean) ** 2
        variance /= (self.n * self.n)
        
        return 1.0 / (1.0 + variance)
    
    def energy_decay_rate(self, energy_history: List[float]) -> float:
        """Compute exponential decay rate of energy"""
        if len(energy_history) < 10:
            return 0.0
        
        recent = energy_history[-10:]
        if recent[0] <= 0:
            return 0.0
        
        decay = (recent[0] - recent[-1]) / recent[0]
        return max(0.0, min(1.0, decay))
    
    def is_stable(self, stability_metric: float, threshold: float = 0.8) -> bool:
        """Check if system is stable"""
        return stability_metric >= threshold
    
    def lyapunov_derivative(self, V_now: float, V_prev: float, dt: float) -> float:
        """Compute derivative of Lyapunov function: dV/dt"""
        return (V_now - V_prev) / dt if dt > 0 else 0.0


def create_lyapunov_stability(n: int = 100) -> LyapunovStability:
    """Factory function for Lyapunov stability"""
    return LyapunovStability(n=n)
