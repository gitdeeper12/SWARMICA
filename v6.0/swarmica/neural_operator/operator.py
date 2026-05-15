"""Neural Operator for SWARMICA v6.0 - Learnable PDE dynamics Fθ(ρ)"""

import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field


@dataclass
class NeuralOperator:
    """Learnable neural operator approximating PDE dynamics Fθ(ρ)"""
    
    n: int = 90
    learning_rate: float = 0.002
    
    def __post_init__(self):
        self._init_parameters()
        self.history = []
    
    def _init_parameters(self):
        """Initialize learnable parameters W"""
        self.W = [[random.uniform(-0.01, 0.01) for _ in range(self.n)] for __ in range(self.n)]
    
    def forward(self, rho: List[List[float]]) -> List[List[float]]:
        """Neural operator: Fθ(ρ) = W·ρ + tanh(ρ)"""
        result = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        
        for i in range(self.n):
            for j in range(self.n):
                # Linear part: W * ρ
                linear = self.W[i][j] * rho[i][j]
                # Nonlinear activation: tanh(ρ)
                nonlinear = math.tanh(rho[i][j])
                result[i][j] = linear + nonlinear
        
        return result
    
    def gradient_wrt_rho(self, rho: List[List[float]]) -> List[List[float]]:
        """Compute ∂Fθ/∂ρ = W + sech²(ρ)"""
        grad = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        
        for i in range(self.n):
            for j in range(self.n):
                # Derivative of W*ρ is W
                # Derivative of tanh(ρ) is sech²(ρ) = 1 - tanh²(ρ)
                sech2 = 1.0 - math.tanh(rho[i][j]) ** 2
                grad[i][j] = self.W[i][j] + sech2
        
        return grad
    
    def update(self, rho: List[List[float]], goal: List[List[float]], adjoint: List[List[float]]):
        """Update parameters using adjoint feedback"""
        for i in range(self.n):
            for j in range(self.n):
                # Simplified learning rule based on adjoint
                delta = adjoint[i][j] * (rho[i][j] - goal[i][j])
                self.W[i][j] += self.learning_rate * delta
                # Clamp to prevent explosion
                self.W[i][j] = max(-1.0, min(1.0, self.W[i][j]))
    
    def get_parameters(self) -> List[List[float]]:
        """Get current parameters W"""
        return self.W
    
    def reset(self):
        """Reset parameters"""
        self._init_parameters()
        self.history = []


def create_neural_operator(n: int = 90, lr: float = 0.002) -> NeuralOperator:
    """Factory function for neural operator"""
    return NeuralOperator(n=n, learning_rate=lr)
