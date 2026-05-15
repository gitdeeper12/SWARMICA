"""Basis expansion for continuum density field"""

import math
from typing import List, Tuple, Callable


class BasisExpansion:
    """Fourier basis expansion for continuum density field ρ(x,t)"""
    
    def __init__(self, n_basis: int = 64, dim: int = 3):
        self.n_basis = n_basis
        self.dim = dim
        self.basis_functions = []
        self._generate_basis()
    
    def _generate_basis(self):
        """Generate Fourier basis functions"""
        for i in range(self.n_basis):
            kx = (i % 3) + 1
            ky = ((i // 3) % 3) + 1
            kz = ((i // 9) % 3) + 1
            typ = 'sin' if (i // 27) % 2 == 0 else 'cos'
            self.basis_functions.append((kx, ky, kz, typ))
    
    def evaluate(self, x: Tuple[float, float, float], coefficients: List[float]) -> float:
        """Evaluate density field at point x"""
        rho = 0.0
        for idx, (kx, ky, kz, typ) in enumerate(self.basis_functions):
            if idx < len(coefficients):
                if typ == 'sin':
                    val = math.sin(kx * x[0]) * math.sin(ky * x[1]) * math.sin(kz * x[2])
                else:
                    val = math.cos(kx * x[0]) * math.cos(ky * x[1]) * math.cos(kz * x[2])
                rho += coefficients[idx] * val
        return max(0.0, rho)
    
    def integrate_density(self, coefficients: List[float], domain_size: Tuple[float, float, float]) -> float:
        """∫ ρ dx over domain (simplified)"""
        total = 0.0
        for coeff in coefficients:
            total += abs(coeff)
        return total * (domain_size[0] * domain_size[1] * domain_size[2]) / self.n_basis
    
    def get_gradient(self, x: Tuple[float, float, float], coefficients: List[float]) -> Tuple[float, float, float]:
        """Compute gradient ∇ρ"""
        grad_x = 0.0
        grad_y = 0.0
        grad_z = 0.0
        
        for idx, (kx, ky, kz, typ) in enumerate(self.basis_functions):
            if idx < len(coefficients):
                c = coefficients[idx]
                if typ == 'sin':
                    grad_x += c * kx * math.cos(kx * x[0]) * math.sin(ky * x[1]) * math.sin(kz * x[2])
                    grad_y += c * ky * math.sin(kx * x[0]) * math.cos(ky * x[1]) * math.sin(kz * x[2])
                    grad_z += c * kz * math.sin(kx * x[0]) * math.sin(ky * x[1]) * math.cos(kz * x[2])
                else:
                    grad_x -= c * kx * math.sin(kx * x[0]) * math.cos(ky * x[1]) * math.cos(kz * x[2])
                    grad_y -= c * ky * math.cos(kx * x[0]) * math.sin(ky * x[1]) * math.cos(kz * x[2])
                    grad_z -= c * kz * math.cos(kx * x[0]) * math.cos(ky * x[1]) * math.sin(kz * x[2])
        
        return (grad_x, grad_y, grad_z)
