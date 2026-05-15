"""Sparse Physics Selector for SWARMICA v13.0 - Lasso regression for PDE discovery"""

import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field


@dataclass
class SparseSelector:
    """Sparse identification of nonlinear dynamics using Lasso regression"""
    
    N: int = 64
    alpha: float = 0.001  # Regularization parameter
    
    def lasso_regression(self, Theta: List[List[float]], y: List[float]) -> List[float]:
        """Lasso regression: minimize ||y - Θξ||² + α||ξ||₁"""
        n_features = len(Theta[0]) if Theta else 0
        
        # Initialize coefficients
        coeffs = [0.0 for _ in range(n_features)]
        
        # Coordinate descent for Lasso
        for _ in range(100):
            for j in range(n_features):
                # Compute residual without feature j
                residual = [y[i] for i in range(len(y))]
                for k in range(n_features):
                    if k != j:
                        for i in range(len(y)):
                            residual[i] -= coeffs[k] * Theta[i][k]
                
                # Compute correlation
                corr = 0.0
                norm = 0.0
                for i in range(len(y)):
                    corr += residual[i] * Theta[i][j]
                    norm += Theta[i][j] * Theta[i][j]
                
                if norm < 1e-8:
                    coeffs[j] = 0.0
                else:
                    # Soft thresholding
                    if corr > self.alpha:
                        coeffs[j] = (corr - self.alpha) / norm
                    elif corr < -self.alpha:
                        coeffs[j] = (corr + self.alpha) / norm
                    else:
                        coeffs[j] = 0.0
        
        return coeffs
    
    def select_terms(self, coeffs: List[float], term_names: List[str], threshold: float = 0.01) -> Dict[str, float]:
        """Select significant terms (|coeff| > threshold)"""
        selected = {}
        for i, (coeff, name) in enumerate(zip(coeffs, term_names)):
            if abs(coeff) > threshold:
                selected[name] = coeff
        return selected
    
    def discover_pde(self, Theta: List[List[float]], y: List[float], term_names: List[str]) -> Dict[str, Any]:
        """Discover PDE from data using sparse regression"""
        # Perform Lasso regression
        coeffs = self.lasso_regression(Theta, y)
        
        # Select significant terms
        selected_terms = self.select_terms(coeffs, term_names)
        
        # Build PDE string
        pde_terms = []
        for name, coeff in selected_terms.items():
            sign = '+' if coeff > 0 else '-'
            abs_coeff = abs(coeff)
            if abs_coeff > 0.01:
                pde_terms.append(f"{sign} {abs_coeff:.4f}·{name}")
        
        pde_string = "∂u/∂t = " + " ".join(pde_terms) if pde_terms else "∂u/∂t = 0"
        
        return {
            'coefficients': selected_terms,
            'pde_equation': pde_string,
            'num_terms': len(selected_terms),
            'sparsity': 1.0 - len(selected_terms) / len(term_names)
        }


def create_sparse_selector(alpha: float = 0.001) -> SparseSelector:
    """Factory function for sparse selector"""
    return SparseSelector(alpha=alpha)
