"""PDE operators for SWARMICA v3.0 - Pure Python (No NumPy)"""

import math
from typing import List, Tuple, Callable


class PDEOperators:
    """Partial Differential Equation operators for continuum swarm dynamics"""
    
    def __init__(self, n: int = 60, dx: float = 1.0):
        self.n = n
        self.dx = dx
    
    def laplacian(self, field: List[List[float]]) -> List[List[float]]:
        """Compute discrete Laplacian: ∇²Z = (∂²Z/∂x² + ∂²Z/∂y²)"""
        result = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        
        for i in range(self.n):
            for j in range(self.n):
                center = field[i][j]
                up = field[i-1][j] if i > 0 else field[i][j]
                down = field[i+1][j] if i < self.n-1 else field[i][j]
                left = field[i][j-1] if j > 0 else field[i][j]
                right = field[i][j+1] if j < self.n-1 else field[i][j]
                
                result[i][j] = (up + down + left + right - 4 * center) / (self.dx * self.dx)
        
        return result
    
    def gradient_x(self, field: List[List[float]]) -> List[List[float]]:
        """Compute gradient in x direction: ∂Z/∂x"""
        result = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        
        for i in range(self.n):
            for j in range(self.n):
                right = field[i][j+1] if j < self.n-1 else field[i][j]
                left = field[i][j-1] if j > 0 else field[i][j]
                result[i][j] = (right - left) / (2 * self.dx)
        
        return result
    
    def gradient_y(self, field: List[List[float]]) -> List[List[float]]:
        """Compute gradient in y direction: ∂Z/∂y"""
        result = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        
        for i in range(self.n):
            for j in range(self.n):
                down = field[i+1][j] if i < self.n-1 else field[i][j]
                up = field[i-1][j] if i > 0 else field[i][j]
                result[i][j] = (down - up) / (2 * self.dx)
        
        return result
    
    def divergence(self, vx: List[List[float]], vy: List[List[float]]) -> List[List[float]]:
        """Compute divergence: ∇·V = ∂vx/∂x + ∂vy/∂y"""
        div_x = self.gradient_x(vx)
        div_y = self.gradient_y(vy)
        
        result = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                result[i][j] = div_x[i][j] + div_y[i][j]
        
        return result
    
    def advection(self, rho: List[List[float]], vx: List[List[float]], vy: List[List[float]]) -> List[List[float]]:
        """Compute advection term: ∇·(ρV)"""
        flux_x = [[rho[i][j] * vx[i][j] for j in range(self.n)] for i in range(self.n)]
        flux_y = [[rho[i][j] * vy[i][j] for j in range(self.n)] for i in range(self.n)]
        
        return self.divergence(flux_x, flux_y)


def create_pde_operators(n: int = 60, dx: float = 1.0) -> PDEOperators:
    """Factory function for PDE operators"""
    return PDEOperators(n=n, dx=dx)
