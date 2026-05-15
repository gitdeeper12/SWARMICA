"""Jacobian eigenvalue analysis for stability certification"""

import math
from typing import List, Tuple, Optional


class JacobianAnalyzer:
    """Jacobian stability certificate: Re(λ_i) < -σ_min < 0"""
    
    def __init__(self, n_basis: int = 64):
        self.n_basis = n_basis
    
    def compute_stiffness_matrix(self, hessian_diag: List[float], metric_inv: List[List[float]]) -> List[List[float]]:
        """J = -G(Q*)⁻¹ Hessian V_eff(Q*)"""
        j = [[0.0] * self.n_basis for _ in range(self.n_basis)]
        
        for i in range(min(self.n_basis, len(hessian_diag))):
            for j_idx in range(self.n_basis):
                if i == j_idx and i < len(metric_inv) and i < len(metric_inv[i]):
                    j[i][i] = -hessian_diag[i] * metric_inv[i][i]
        
        return j
    
    def compute_damping_matrix(self, mu: float, metric_inv: List[List[float]]) -> List[List[float]]:
        """J_v = -μ G(Q*)⁻¹ D_damp"""
        jv = [[0.0] * self.n_basis for _ in range(self.n_basis)]
        
        for i in range(self.n_basis):
            if i < len(metric_inv) and i < len(metric_inv[i]):
                jv[i][i] = -mu * metric_inv[i][i]
        
        return jv
    
    def compute_eigenvalues(self, matrix: List[List[float]]) -> List[complex]:
        """Compute eigenvalues of 2x2 block using simplified method"""
        # Simplified: for diagonal matrices, eigenvalues are diagonal entries
        eigenvalues = []
        n = min(len(matrix), self.n_basis)
        
        for i in range(n):
            if i < len(matrix) and i < len(matrix[i]):
                eigenvalues.append(complex(matrix[i][i], 0))
        
        # Pad with zeros if needed
        while len(eigenvalues) < 2 * self.n_basis:
            eigenvalues.append(complex(0, 0))
        
        return eigenvalues
    
    def check_stability(self, eigenvalues: List[complex], sigma_min: float = 1e-6) -> Tuple[bool, float]:
        """Check if all eigenvalues satisfy Re(λ) < -σ_min"""
        max_real = -float('inf')
        
        for eig in eigenvalues:
            if eig.real > max_real:
                max_real = eig.real
        
        is_stable = max_real < -sigma_min
        return is_stable, max_real
    
    def compute_sigma_min(self, min_hessian_eigenvalue: float, max_metric_eigenvalue: float) -> float:
        """σ_min = λ_min(Hessian V_eff) / λ_max(G(Q*))"""
        if max_metric_eigenvalue == 0:
            return 0.0
        return min_hessian_eigenvalue / max_metric_eigenvalue
    
    def get_convergence_rate(self, sigma_min: float) -> str:
        """Get exponential convergence rate description"""
        if sigma_min <= 0:
            return "No convergence guarantee"
        elif sigma_min < 0.01:
            return f"Slow convergence (τ = {1/sigma_min:.0f} steps)"
        elif sigma_min < 0.1:
            return f"Moderate convergence (τ = {1/sigma_min:.0f} steps)"
        else:
            return f"Fast convergence (τ = {1/sigma_min:.1f} steps)"
    
    def certificate(self, hessian_diag: List[float], metric_inv: List[List[float]], 
                    mu: float = 0.02) -> Tuple[bool, dict]:
        """Generate full stability certificate"""
        # Compute matrices
        j = self.compute_stiffness_matrix(hessian_diag, metric_inv)
        jv = self.compute_damping_matrix(mu, metric_inv)
        
        # Compute eigenvalues (simplified)
        j_eigs = self.compute_eigenvalues(j)
        jv_eigs = self.compute_eigenvalues(jv)
        
        # Combined eigenvalues
        all_eigs = j_eigs + jv_eigs
        
        # Check stability
        is_stable, max_real = self.check_stability(all_eigs)
        
        # Compute sigma_min
        min_hess = min(hessian_diag) if hessian_diag else 0.1
        max_metric = max(metric_inv[i][i] for i in range(min(self.n_basis, len(metric_inv))))
        sigma_min = self.compute_sigma_min(min_hess, max_metric) if max_metric > 0 else 0.01
        
        result = {
            'is_stable': is_stable,
            'max_eigenvalue_real': max_real,
            'sigma_min': sigma_min,
            'convergence_rate': self.get_convergence_rate(sigma_min),
            'n_basis': self.n_basis,
        }
        
        return is_stable, result


def create_jacobian_analyzer(n_basis: int = 64) -> JacobianAnalyzer:
    """Factory function to create Jacobian analyzer"""
    return JacobianAnalyzer(n_basis=n_basis)
