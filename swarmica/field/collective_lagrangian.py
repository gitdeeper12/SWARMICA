"""Collective Lagrangian Operator (CLO) - derives swarm dynamics from variational principle"""

import math
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class CollectiveLagrangian:
    """CLO: L[Q, Q_dot] = T[Q_dot] - V_eff[Q]"""
    
    n_basis: int = 64
    alpha: float = 0.15  # quadratic floor coefficient
    mu_dissipation: float = 0.02  # drag coefficient
    
    def kinetic_energy(self, q_dot: List[float], metric: List[List[float]]) -> float:
        """T = 0.5 * Q_dot^T G(Q) Q_dot"""
        t = 0.0
        for i in range(min(self.n_basis, len(q_dot))):
            for j in range(min(self.n_basis, len(q_dot))):
                t += 0.5 * q_dot[i] * q_dot[j] * metric[i][j]
        return t
    
    def potential_energy(self, q: List[float], q_star: Optional[List[float]] = None) -> float:
        """V_eff(Q) = SOS potential + quadratic floor"""
        v = 0.0
        # Quadratic floor term: α ||Q - Q*||²
        if q_star:
            for i in range(min(self.n_basis, len(q), len(q_star))):
                diff = q[i] - q_star[i]
                v += self.alpha * diff * diff
        else:
            for val in q:
                v += self.alpha * val * val
        return v
    
    def euler_lagrange(self, q: List[float], q_dot: List[float], q_star: Optional[List[float]] = None) -> List[float]:
        """Compute Euler-Lagrange equations: G(Q) Q̈ + C(Q,Q̇) Q̇ + ∇V_eff = F_ctrl"""
        # Simplified: F_ctrl = -∇V_eff - C·Q̇ - μ·Q̇
        forces = []
        for i in range(min(self.n_basis, len(q))):
            # Gradient of potential
            grad_v = 0.0
            if q_star and i < len(q_star):
                grad_v = 2.0 * self.alpha * (q[i] - q_star[i])
            else:
                grad_v = 2.0 * self.alpha * q[i]
            
            # Damping term
            damping = self.mu_dissipation * (q_dot[i] if i < len(q_dot) else 0)
            
            force = -grad_v - damping
            forces.append(force)
        
        return forces
    
    def lagrangian(self, q: List[float], q_dot: List[float], metric: List[List[float]], 
                   q_star: Optional[List[float]] = None) -> float:
        """L = T - V_eff"""
        t = self.kinetic_energy(q_dot, metric)
        v = self.potential_energy(q, q_star)
        return t - v


def create_clo(n_basis: int = 64, mu: float = 0.02, alpha: float = 0.15) -> CollectiveLagrangian:
    """Factory function to create Collective Lagrangian Operator"""
    return CollectiveLagrangian(n_basis=n_basis, mu_dissipation=mu, alpha=alpha)
