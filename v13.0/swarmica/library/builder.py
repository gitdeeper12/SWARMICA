"""PDE Library Builder for SWARMICA v13.0 - Symbolic term generation"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class PDELibrary:
    """Build library of candidate PDE terms for symbolic discovery"""
    
    N: int = 64
    
    def gradient_x(self, field: List[List[float]]) -> List[List[float]]:
        """Compute ∂u/∂x"""
        N = self.N
        grad = [[0.0 for _ in range(N)] for __ in range(N)]
        
        for i in range(N):
            for j in range(N):
                right = field[i][j+1] if j < N-1 else field[i][j]
                left = field[i][j-1] if j > 0 else field[i][j]
                grad[i][j] = (right - left) / 2
        
        return grad
    
    def gradient_y(self, field: List[List[float]]) -> List[List[float]]:
        """Compute ∂u/∂y"""
        N = self.N
        grad = [[0.0 for _ in range(N)] for __ in range(N)]
        
        for i in range(N):
            for j in range(N):
                down = field[i+1][j] if i < N-1 else field[i][j]
                up = field[i-1][j] if i > 0 else field[i][j]
                grad[i][j] = (down - up) / 2
        
        return grad
    
    def laplacian(self, field: List[List[float]]) -> List[List[float]]:
        """Compute ∇²u"""
        N = self.N
        lap = [[0.0 for _ in range(N)] for __ in range(N)]
        
        for i in range(N):
            for j in range(N):
                center = field[i][j]
                up = field[i-1][j] if i > 0 else field[i][j]
                down = field[i+1][j] if i < N-1 else field[i][j]
                left = field[i][j-1] if j > 0 else field[i][j]
                right = field[i][j+1] if j < N-1 else field[i][j]
                lap[i][j] = up + down + left + right - 4 * center
        
        return lap
    
    def build_features(self, u: List[List[float]]) -> List[List[float]]:
        """Build feature matrix Θ(u) = [u, u², ∂u/∂x, ∂u/∂y, ∇²u, u∂u/∂x, u∂u/∂y, sin(u)]"""
        N = self.N
        
        ux = self.gradient_x(u)
        uy = self.gradient_y(u)
        lap = self.laplacian(u)
        
        # Flatten each feature
        features = []
        
        # u
        for i in range(N):
            for j in range(N):
                features.append([u[i][j]])
        
        # u²
        for i in range(N):
            for j in range(N):
                features[i*N + j].append(u[i][j] * u[i][j])
        
        # ∂u/∂x
        for i in range(N):
            for j in range(N):
                features[i*N + j].append(ux[i][j])
        
        # ∂u/∂y
        for i in range(N):
            for j in range(N):
                features[i*N + j].append(uy[i][j])
        
        # ∇²u
        for i in range(N):
            for j in range(N):
                features[i*N + j].append(lap[i][j])
        
        # u·∂u/∂x
        for i in range(N):
            for j in range(N):
                features[i*N + j].append(u[i][j] * ux[i][j])
        
        # u·∂u/∂y
        for i in range(N):
            for j in range(N):
                features[i*N + j].append(u[i][j] * uy[i][j])
        
        # sin(u)
        for i in range(N):
            for j in range(N):
                features[i*N + j].append(math.sin(u[i][j]))
        
        return features
    
    def term_names(self) -> List[str]:
        """Get names of PDE terms"""
        return ['u', 'u²', '∂u/∂x', '∂u/∂y', '∇²u', 'u·∂u/∂x', 'u·∂u/∂y', 'sin(u)']


def create_pde_library(N: int = 64) -> PDELibrary:
    """Factory function for PDE library"""
    return PDELibrary(N=N)
