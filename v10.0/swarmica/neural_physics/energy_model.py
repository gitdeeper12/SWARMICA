"""Neural Energy Functional E_θ(ρ) - Learnable physics"""

import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field


@dataclass
class NeuralEnergyModel:
    """Learnable energy functional E_θ(ρ) - approximates physics from data"""
    
    N: int = 100
    learning_rate: float = 0.01
    
    def __post_init__(self):
        self._init_parameters()
        self.history = []
    
    def _init_parameters(self):
        """Initialize learnable parameters"""
        # Neural energy parameters (simplified learnable field)
        self.theta = [[random.uniform(-0.1, 0.1) for _ in range(self.N)] for __ in range(self.N)]
    
    def forward(self, rho: List[List[float]]) -> float:
        """Compute learned energy E_θ(ρ) = tanh(mean(ρ)) + var(ρ) + θ·mean(ρ²)"""
        # Compute mean
        total = 0.0
        for i in range(self.N):
            for j in range(self.N):
                total += rho[i][j]
        mean_rho = total / (self.N * self.N)
        
        # Compute variance
        variance = 0.0
        for i in range(self.N):
            for j in range(self.N):
                variance += (rho[i][j] - mean_rho) ** 2
        variance /= (self.N * self.N)
        
        # Compute learned term
        learned = 0.0
        for i in range(self.N):
            for j in range(self.N):
                learned += self.theta[i][j] * rho[i][j] * rho[i][j]
        learned /= (self.N * self.N)
        
        # Energy = nonlinear activation + variance + learned term
        energy = math.tanh(mean_rho) + variance + 0.1 * learned
        
        return max(0.0, min(1.0, energy))
    
    def energy_gradient(self, rho: List[List[float]]) -> List[List[float]]:
        """Compute ∇E_θ(ρ) - gradient of learned energy"""
        # Compute mean
        total = 0.0
        for i in range(self.N):
            for j in range(self.N):
                total += rho[i][j]
        mean_rho = total / (self.N * self.N)
        
        grad = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        
        # Derivative of tanh(mean) w.r.t ρ
        dtanh = (1 - math.tanh(mean_rho) ** 2) / (self.N * self.N)
        
        for i in range(self.N):
            for j in range(self.N):
                # Gradient from variance term
                dvar = 2 * (rho[i][j] - mean_rho) / (self.N * self.N)
                
                # Gradient from learned term
                dlearned = 2 * self.theta[i][j] * rho[i][j] / (self.N * self.N)
                
                grad[i][j] = dtanh + dvar + 0.1 * dlearned
        
        return grad
    
    def update(self, rho: List[List[float]], target_energy: float):
        """Update parameters based on energy error"""
        current_energy = self.forward(rho)
        error = target_energy - current_energy
        
        # Simple Hebbian-like update
        for i in range(self.N):
            for j in range(self.N):
                self.theta[i][j] += self.learning_rate * error * rho[i][j] * rho[i][j]
                # Clamp parameters
                self.theta[i][j] = max(-0.5, min(0.5, self.theta[i][j]))
    
    def get_parameters(self) -> List[List[float]]:
        """Get current parameters"""
        return self.theta
    
    def reset(self):
        """Reset parameters"""
        self._init_parameters()
        self.history = []


def create_neural_energy_model(N: int = 100) -> NeuralEnergyModel:
    """Factory function for neural energy model"""
    return NeuralEnergyModel(N=N)
