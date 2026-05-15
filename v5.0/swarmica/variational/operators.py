"""Variational operators for SWARMICA v5.0 - PDE calculus of variations"""

import math
from typing import List, Tuple


class VariationalOperators:
    """PDE operators for variational calculus and optimal control"""
    
    def __init__(self, n: int = 80, dx: float = 1.0):
        self.n = n
        self.dx = dx
    
    def laplacian(self, field: List[List[float]]) -> List[List[float]]:
        """Compute discrete Laplacian: ∇²Z"""
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
    
    def gradient(self, field: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
        """Compute gradient ∇Z = (∂Z/∂x, ∂Z/∂y)"""
        gx = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        gy = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        
        for i in range(self.n):
            for j in range(self.n):
                right = field[i][j+1] if j < self.n-1 else field[i][j]
                left = field[i][j-1] if j > 0 else field[i][j]
                gx[i][j] = (right - left) / (2 * self.dx)
                
                down = field[i+1][j] if i < self.n-1 else field[i][j]
                up = field[i-1][j] if i > 0 else field[i][j]
                gy[i][j] = (down - up) / (2 * self.dx)
        
        return gx, gy
    
    def divergence(self, vx: List[List[float]], vy: List[List[float]]) -> List[List[float]]:
        """Compute divergence: ∇·V = ∂vx/∂x + ∂vy/∂y"""
        div = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        
        for i in range(self.n):
            for j in range(self.n):
                vx_right = vx[i][j+1] if j < self.n-1 else vx[i][j]
                vx_left = vx[i][j-1] if j > 0 else vx[i][j]
                dvx_dx = (vx_right - vx_left) / (2 * self.dx)
                
                vy_down = vy[i+1][j] if i < self.n-1 else vy[i][j]
                vy_up = vy[i-1][j] if i > 0 else vy[i][j]
                dvy_dy = (vy_down - vy_up) / (2 * self.dx)
                
                div[i][j] = dvx_dx + dvy_dy
        
        return div


def create_variational_operators(n: int = 80) -> VariationalOperators:
    return VariationalOperators(n=n)
