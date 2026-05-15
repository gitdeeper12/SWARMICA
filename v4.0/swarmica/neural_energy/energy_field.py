"""Neural Energy Field for SWARMICA v4.0 - Learnable Energy Functional E_θ(ρ)"""

import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field


@dataclass
class NeuralEnergyField:
    """Learnable energy functional E_θ(ρ) with parameterized field W"""
    
    n: int = 70
    learning_rate: float = 0.001
    
    def __post_init__(self):
        self._init_parameters()
        self.history = []
    
    def _init_parameters(self):
        """Initialize learnable parameters W"""
        self.W = [[random.uniform(-0.01, 0.01) for _ in range(self.n)] for __ in range(self.n)]
    
    def energy(self, rho: List[List[float]], goal: List[List[float]]) -> float:
        """Compute energy: E_θ(ρ) = Σ(W·ρ²) + Σ((ρ - goal)²)"""
        total = 0.0
        
        for i in range(self.n):
            for j in range(self.n):
                # Learned term: W * ρ²
                learned = self.W[i][j] * rho[i][j] * rho[i][j]
                # Attractor term: (ρ - goal)²
                attractor = (rho[i][j] - goal[i][j]) ** 2
                total += learned + attractor
        
        return total
    
    def compute_gradient(self, rho: List[List[float]], goal: List[List[float]]) -> List[List[float]]:
        """Compute gradient of energy functional: δE/δρ = 2W·ρ + 2(ρ - goal)"""
        grad = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        
        for i in range(self.n):
            for j in range(self.n):
                grad[i][j] = 2.0 * self.W[i][j] * rho[i][j] + 2.0 * (rho[i][j] - goal[i][j])
        
        return grad
    
    def update(self, rho: List[List[float]], goal: List[List[float]]):
        """Online learning: W ← W + η·(ρ - goal)·ρ"""
        for i in range(self.n):
            for j in range(self.n):
                delta = (rho[i][j] - goal[i][j]) * rho[i][j]
                self.W[i][j] += self.learning_rate * delta
                # Clamp to prevent explosion
                self.W[i][j] = max(-1.0, min(1.0, self.W[i][j]))
    
    def get_parameter_field(self) -> List[List[float]]:
        """Get current parameter field W for visualization"""
        return self.W
    
    def reset(self):
        """Reset parameters"""
        self._init_parameters()
        self.history = []


def create_neural_energy_field(n: int = 70, lr: float = 0.001) -> NeuralEnergyField:
    """Factory function for neural energy field"""
    return NeuralEnergyField(n=n, learning_rate=lr)
