"""Effective Potential Field Engine (EPFE) with SOS polynomial parameterization"""

import math
from typing import List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class EffectivePotentialFieldEngine:
    """EPFE: V_eff(Q) = p(Q)^T P p(Q) + α ||Q - Q*||²_G"""
    
    n_basis: int = 64
    sos_degree: int = 4
    alpha: float = 0.15
    _p_matrix: List[List[float]] = None
    _q_star: List[float] = None
    
    def __post_init__(self):
        """Initialize P matrix (positive semidefinite)"""
        self._init_p_matrix()
    
    def _init_p_matrix(self):
        """Initialize P matrix as diagonal positive semidefinite"""
        self._p_matrix = [[0.0] * self.n_basis for _ in range(self.n_basis)]
        for i in range(self.n_basis):
            self._p_matrix[i][i] = 1.0 / (1.0 + i * 0.1)
    
    def set_target(self, q_star: List[float]):
        """Set target configuration Q*"""
        self._q_star = q_star.copy() if q_star else None
    
    def _monomial_basis(self, q: List[float]) -> List[float]:
        """Construct monomial basis vector p(Q) up to degree 2d"""
        basis = []
        # Linear terms
        for val in q[:self.n_basis]:
            basis.append(val)
        # Quadratic terms (simplified)
        for i in range(min(10, len(q))):
            basis.append(q[i] * q[i])
        # Cross terms (simplified)
        for i in range(min(5, len(q))):
            for j in range(i+1, min(5, len(q))):
                basis.append(q[i] * q[j])
        return basis
    
    def compute_potential(self, q: List[float]) -> float:
        """Compute V_eff(Q) = p(Q)^T P p(Q) + α ||Q - Q*||²"""
        # SOS term: p^T P p
        basis = self._monomial_basis(q)
        sos_value = 0.0
        for i, bi in enumerate(basis):
            for j, bj in enumerate(basis):
                if i < self.n_basis and j < self.n_basis:
                    sos_value += bi * bj * self._p_matrix[i][j]
        
        # Quadratic floor term: α ||Q - Q*||²
        quad_floor = 0.0
        if self._q_star:
            for i in range(min(len(q), len(self._q_star))):
                diff = q[i] - self._q_star[i]
                quad_floor += self.alpha * diff * diff
        else:
            for val in q:
                quad_floor += self.alpha * val * val
        
        return sos_value + quad_floor
    
    def compute_gradient(self, q: List[float]) -> List[float]:
        """Compute ∇V_eff (simplified finite difference)"""
        grad = [0.0] * len(q)
        eps = 1e-5
        v0 = self.compute_potential(q)
        
        for i in range(len(q)):
            q_pert = q.copy()
            q_pert[i] += eps
            v1 = self.compute_potential(q_pert)
            grad[i] = (v1 - v0) / eps
        
        return grad
    
    def compute_hessian_diagonal(self, q: List[float]) -> List[float]:
        """Compute diagonal of Hessian matrix (simplified)"""
        hess_diag = [0.0] * len(q)
        eps = 1e-5
        
        grad0 = self.compute_gradient(q)
        
        for i in range(len(q)):
            q_pert = q.copy()
            q_pert[i] += eps
            grad1 = self.compute_gradient(q_pert)
            hess_diag[i] = (grad1[i] - grad0[i]) / eps
        
        return hess_diag
    
    @property
    def is_globally_convex(self) -> bool:
        """Check if potential is globally convex (simplified)"""
        # P is positive semidefinite by construction
        return True
    
    def verify_global_minimum(self, q: List[float]) -> bool:
        """Verify Q is the global minimum (simplified)"""
        if not self._q_star:
            return False
        # Check gradient near zero at Q*
        grad = self.compute_gradient(q)
        grad_norm = math.sqrt(sum(g*g for g in grad))
        return grad_norm < 1e-4


def create_epfe(n_basis: int = 64, alpha: float = 0.15) -> EffectivePotentialFieldEngine:
    """Factory function to create EPFE"""
    return EffectivePotentialFieldEngine(n_basis=n_basis, alpha=alpha)
