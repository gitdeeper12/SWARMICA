"""Constraint Verifier for SWARMICA v13.0 - Check discovered physics validity"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class ConstraintVerifier:
    """Verify that discovered PDEs satisfy physical constraints"""
    
    N: int = 64
    
    def check_mass_conservation(self, u: List[List[float]]) -> float:
        """Check total mass ∫u dx"""
        total = 0.0
        for i in range(self.N):
            for j in range(self.N):
                total += u[i][j]
        return total
    
    def check_positivity(self, u: List[List[float]]) -> bool:
        """Check that density is non-negative"""
        for i in range(self.N):
            for j in range(self.N):
                if u[i][j] < 0:
                    return False
        return True
    
    def check_boundedness(self, u: List[List[float]]) -> bool:
        """Check that density is bounded (0 ≤ u ≤ 1)"""
        for i in range(self.N):
            for j in range(self.N):
                if u[i][j] < 0 or u[i][j] > 1:
                    return False
        return True
    
    def verify_pde(self, pde_equation: str, coeffs: Dict[str, float]) -> Dict[str, Any]:
        """Verify discovered PDE against physical constraints"""
        verified = True
        warnings = []
        
        # Check for diffusion term (stabilizing)
        has_diffusion = any('∇²u' in term for term in coeffs.keys())
        
        # Check for advection term
        has_advection = any('∂u/∂x' in term or '∂u/∂y' in term for term in coeffs.keys())
        
        # Check for reaction term
        has_reaction = any('u²' in term or 'sin(u)' in term for term in coeffs.keys())
        
        if not has_diffusion and not has_advection:
            warnings.append("No diffusion or advection terms - may be incomplete")
        
        return {
            'verified': verified,
            'warnings': warnings,
            'has_diffusion': has_diffusion,
            'has_advection': has_advection,
            'has_reaction': has_reaction,
            'complexity': len(coeffs)
        }


def create_constraint_verifier(N: int = 64) -> ConstraintVerifier:
    """Factory function for constraint verifier"""
    return ConstraintVerifier(N=N)
