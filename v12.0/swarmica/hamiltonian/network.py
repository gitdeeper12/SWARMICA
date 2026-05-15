"""Hamiltonian Neural Network for SWARMICA v12.0 - Learnable Energy Hθ(ρ, v)"""

import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field


@dataclass
class HamiltonianNetwork:
    """Learnable Hamiltonian energy function Hθ(ρ, v) with symplectic structure"""
    
    N: int = 64
    learning_rate: float = 0.01
    
    def __post_init__(self):
        self._init_parameters()
        self.history = {'energy': [], 'hamiltonian': []}
    
    def _init_parameters(self):
        """Initialize learnable Hamiltonian parameters"""
        self.W_rho = [[random.uniform(-0.1, 0.1) for _ in range(self.N)] for __ in range(self.N)]
        self.W_v = [[random.uniform(-0.1, 0.1) for _ in range(self.N)] for __ in range(self.N)]
        self.bias = random.uniform(-0.05, 0.05)
    
    def energy(self, rho: List[List[float]], vx: List[List[float]], vy: List[List[float]]) -> float:
        """Compute Hamiltonian Hθ(ρ, v) = H_ρ(ρ) + H_v(v)"""
        N = self.N
        
        # Potential energy from density
        potential = 0.0
        for i in range(N):
            for j in range(N):
                potential += self.W_rho[i][j] * rho[i][j] * rho[i][j]
        
        # Kinetic energy from velocity
        kinetic = 0.0
        for i in range(N):
            for j in range(N):
                kinetic += self.W_v[i][j] * (vx[i][j] * vx[i][j] + vy[i][j] * vy[i][j])
        
        return (potential + kinetic) / (N * N) + self.bias
    
    def energy_gradient_rho(self, rho: List[List[float]]) -> List[List[float]]:
        """Compute ∂H/∂ρ for symplectic dynamics"""
        N = self.N
        grad = [[0.0 for _ in range(N)] for __ in range(N)]
        
        for i in range(N):
            for j in range(N):
                grad[i][j] = 2.0 * self.W_rho[i][j] * rho[i][j]
        
        return grad
    
    def energy_gradient_v(self, vx: List[List[float]], vy: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
        """Compute ∂H/∂v for symplectic dynamics"""
        N = self.N
        grad_vx = [[0.0 for _ in range(N)] for __ in range(N)]
        grad_vy = [[0.0 for _ in range(N)] for __ in range(N)]
        
        for i in range(N):
            for j in range(N):
                grad_vx[i][j] = 2.0 * self.W_v[i][j] * vx[i][j]
                grad_vy[i][j] = 2.0 * self.W_v[i][j] * vy[i][j]
        
        return grad_vx, grad_vy
    
    def update(self, rho: List[List[float]], vx: List[List[float]], vy: List[List[float]], 
               target_energy: float):
        """Update Hamiltonian parameters"""
        N = self.N
        current_energy = self.energy(rho, vx, vy)
        error = target_energy - current_energy
        
        self.history['energy'].append(current_energy)
        self.history['hamiltonian'].append(current_energy)
        
        # Simple Hebbian update
        for i in range(N):
            for j in range(N):
                self.W_rho[i][j] += self.learning_rate * error * rho[i][j] * rho[i][j]
                self.W_v[i][j] += self.learning_rate * error * (vx[i][j] * vx[i][j] + vy[i][j] * vy[i][j])
                # Clamp
                self.W_rho[i][j] = max(-0.5, min(0.5, self.W_rho[i][j]))
                self.W_v[i][j] = max(-0.5, min(0.5, self.W_v[i][j]))
        
        self.bias += self.learning_rate * error
        self.bias = max(-0.5, min(0.5, self.bias))
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get Hamiltonian parameters"""
        N = self.N
        rho_mean = 0.0
        v_mean = 0.0
        
        for i in range(N):
            for j in range(N):
                rho_mean += self.W_rho[i][j]
                v_mean += self.W_v[i][j]
        
        return {
            'rho_potential_mean': rho_mean / (N * N),
            'kinetic_mean': v_mean / (N * N),
            'bias': self.bias
        }
    
    def reset(self):
        """Reset Hamiltonian parameters"""
        self._init_parameters()
        self.history = {'energy': [], 'hamiltonian': []}


def create_hamiltonian_network(N: int = 64) -> HamiltonianNetwork:
    """Factory function for Hamiltonian network"""
    return HamiltonianNetwork(N=N)
