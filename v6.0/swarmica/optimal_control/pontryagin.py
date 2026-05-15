"""Pontryagin Maximum Principle (PMP) for SWARMICA v6.0"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field


@dataclass
class PontryaginController:
    """Optimal control using Pontryagin Maximum Principle"""
    
    n: int = 90
    control_weight: float = 0.8   # λ - control penalty
    adjoint_lr: float = 0.002     # Learning rate for costate
    
    def __post_init__(self):
        self._init_costate()
        self.history = {'control_effort': []}
    
    def _init_costate(self):
        """Initialize costate variable p (adjoint)"""
        self.costate = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
    
    def optimal_control(self) -> List[List[float]]:
        """PMP optimal control law: u* = -(1/λ) * Gᵀ p"""
        control = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        
        for i in range(self.n):
            for j in range(self.n):
                # Simplified: G = identity matrix
                control[i][j] = -(1.0 / (self.control_weight + 1e-6)) * self.costate[i][j]
        
        return control
    
    def update_costate(self, rho: List[List[float]], goal: List[List[float]], 
                       grad_rho: List[List[float]], neural_grad: List[List[float]]) -> List[List[float]]:
        """Update costate using adjoint dynamics: ∂p/∂t = -∂H/∂ρ"""
        new_costate = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        
        for i in range(self.n):
            for j in range(self.n):
                # Hamiltonian gradient with respect to state
                # dH/dρ = (ρ - goal) + ∇²ρ + ∂Fθ/∂ρ
                state_grad = (rho[i][j] - goal[i][j]) + grad_rho[i][j] + neural_grad[i][j]
                new_costate[i][j] = self.costate[i][j] + self.adjoint_lr * (-state_grad)
        
        self.costate = new_costate
        return self.costate
    
    def control_effort(self, control: List[List[float]]) -> float:
        """Compute control effort: ∫‖u‖²"""
        total = 0.0
        for i in range(self.n):
            for j in range(self.n):
                total += control[i][j] ** 2
        return total / (self.n * self.n)
    
    def get_costate(self) -> List[List[float]]:
        """Get current costate for visualization"""
        return self.costate
    
    def reset(self):
        """Reset costate"""
        self._init_costate()
        self.history = {'control_effort': []}


def create_pontryagin_controller(n: int = 90, control_weight: float = 0.8) -> PontryaginController:
    """Factory function for Pontryagin controller"""
    return PontryaginController(n=n, control_weight=control_weight)
