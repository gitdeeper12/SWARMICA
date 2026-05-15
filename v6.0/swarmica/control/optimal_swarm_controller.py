"""Optimal Swarm Controller for SWARMICA v6.0 - PMP + Neural Operator"""

import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field

from ..neural_operator.operator import NeuralOperator
from ..optimal_control.pontryagin import PontryaginController
from ..pde.operators import PDEOperators


@dataclass
class OptimalSwarmController:
    """Optimal controller using Pontryagin Maximum Principle and Neural Operators"""
    
    n: int = 90
    dt: float = 0.05
    dx: float = 1.0
    alpha: float = 1.0      # Drift strength
    beta: float = 0.25      # Diffusion coefficient
    sigma: float = 0.1      # Noise strength
    control_weight: float = 0.8   # Control penalty λ
    adjoint_lr: float = 0.002     # Adjoint learning rate
    
    def __post_init__(self):
        self.pde_ops = PDEOperators(self.n, self.dx)
        self.neural_op = NeuralOperator(self.n, self.adjoint_lr)
        self.pmp = PontryaginController(self.n, self.control_weight, self.adjoint_lr)
        self._init_fields()
        self.history = {
            'energy': [],
            'control_effort': [],
            'total_cost': []
        }
    
    def _init_fields(self):
        """Initialize density and goal fields"""
        self.rho = [[random.uniform(0, 0.3) for _ in range(self.n)] for __ in range(self.n)]
        
        # Multi-attractor goal field
        self.goal = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        self.goal[self.n // 3][self.n // 3] = 1.0
        self.goal[2 * self.n // 3][2 * self.n // 3] = 1.0
    
    def _energy(self, rho: List[List[float]]) -> float:
        """Energy functional: E = Σ(ρ - goal)²"""
        total = 0.0
        for i in range(self.n):
            for j in range(self.n):
                total += (rho[i][j] - self.goal[i][j]) ** 2
        return total
    
    def _add_noise(self, field: List[List[float]]) -> List[List[float]]:
        """Add stochastic noise (Wiener process)"""
        result = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                noise_val = self.sigma * random.gauss(0, 1) * math.sqrt(self.dt)
                result[i][j] = field[i][j] + noise_val
        return result
    
    def step(self) -> Dict[str, Any]:
        """Execute one optimal control step"""
        
        # 1. Neural operator: Fθ(ρ)
        F_theta = self.neural_op.forward(self.rho)
        
        # 2. Spatial gradients
        grad_rho = self.pde_ops.gradient_field(self.rho)
        
        # 3. Diffusion term
        diffusion = self.pde_ops.laplacian(self.rho)
        
        # 4. PMP optimal control law
        control = self.pmp.optimal_control()
        
        # 5. Stochastic noise
        noise = self._add_noise([[0.0 for _ in range(self.n)] for __ in range(self.n)])
        
        # 6. PDE evolution: ∂ρ/∂t = α·Fθ(ρ) - ∇ρ + β∇²ρ + u + σ·dW
        new_rho = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                update = (self.alpha * F_theta[i][j] - grad_rho[i][j] + 
                         self.beta * diffusion[i][j] + control[i][j] + noise[i][j])
                new_rho[i][j] = self.rho[i][j] + self.dt * update
        
        # Clamp to physical bounds
        for i in range(self.n):
            for j in range(self.n):
                new_rho[i][j] = max(0.0, min(1.0, new_rho[i][j]))
        
        self.rho = new_rho
        
        # 7. Compute neural operator gradient for adjoint
        neural_grad = self.neural_op.gradient_wrt_rho(self.rho)
        
        # 8. Update costate (adjoint) using PMP
        self.pmp.update_costate(self.rho, self.goal, grad_rho, neural_grad)
        
        # 9. Update neural operator parameters using adjoint feedback
        self.neural_op.update(self.rho, self.goal, self.pmp.get_costate())
        
        # 10. Compute metrics
        energy_cost = self._energy(self.rho)
        control_effort = self.pmp.control_effort(control)
        total_cost = energy_cost + self.control_weight * control_effort
        
        self.history['energy'].append(energy_cost)
        self.history['control_effort'].append(control_effort)
        self.history['total_cost'].append(total_cost)
        
        return {
            'rho': self.rho,
            'control': control,
            'costate': self.pmp.get_costate(),
            'energy': energy_cost,
            'control_effort': control_effort,
            'total_cost': total_cost,
            'step': len(self.history['energy']) - 1
        }
    
    def run(self, steps: int) -> Dict[str, List[float]]:
        """Run simulation for multiple steps"""
        for _ in range(steps):
            self.step()
        return self.history
    
    def reset(self):
        """Reset controller state"""
        self._init_fields()
        self.neural_op.reset()
        self.pmp.reset()
        self.history = {'energy': [], 'control_effort': [], 'total_cost': []}
    
    def get_optimality_gap(self) -> float:
        """Estimate optimality gap from costate norm"""
        costate = self.pmp.get_costate()
        norm = 0.0
        for i in range(self.n):
            for j in range(self.n):
                norm += costate[i][j] ** 2
        return math.sqrt(norm / (self.n * self.n))


def create_optimal_swarm_controller(n: int = 90) -> OptimalSwarmController:
    """Factory function for optimal swarm controller"""
    return OptimalSwarmController(n=n)
