"""PDE operators for SWARMICA v4.0 - Advanced continuum dynamics"""

import math
from typing import List, Tuple


class AdvancedPDEOperators:
    """Advanced PDE operators for continuum swarm dynamics"""
    
    def __init__(self, n: int = 70, dx: float = 1.0):
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
        """Compute gradient (gx, gy) = ∇Z"""
        gx = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        gy = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        
        for i in range(self.n):
            for j in range(self.n):
                # x-gradient
                right = field[i][j+1] if j < self.n-1 else field[i][j]
                left = field[i][j-1] if j > 0 else field[i][j]
                gx[i][j] = (right - left) / (2 * self.dx)
                
                # y-gradient
                down = field[i+1][j] if i < self.n-1 else field[i][j]
                up = field[i-1][j] if i > 0 else field[i][j]
                gy[i][j] = (down - up) / (2 * self.dx)
        
        return gx, gy
    
    def divergence(self, vx: List[List[float]], vy: List[List[float]]) -> List[List[float]]:
        """Compute divergence: ∇·V"""
        div = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        
        for i in range(self.n):
            for j in range(self.n):
                # ∂vx/∂x
                vx_right = vx[i][j+1] if j < self.n-1 else vx[i][j]
                vx_left = vx[i][j-1] if j > 0 else vx[i][j]
                dvx_dx = (vx_right - vx_left) / (2 * self.dx)
                
                # ∂vy/∂y
                vy_down = vy[i+1][j] if i < self.n-1 else vy[i][j]
                vy_up = vy[i-1][j] if i > 0 else vy[i][j]
                dvy_dy = (vy_down - vy_up) / (2 * self.dx)
                
                div[i][j] = dvx_dx + dvy_dy
        
        return div


def create_advanced_pde_operators(n: int = 70) -> AdvancedPDEOperators:
    """Factory function for PDE operators"""
    return AdvancedPDEOperators(n=n)
