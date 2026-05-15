"""PDE Solver for SWARMICA v3.0 - Reaction-Diffusion System"""

import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field

from ..pde.operators import PDEOperators
from ..energy.functional import EnergyFunctional


@dataclass
class PDESolver:
    """PDE solver for continuum swarm dynamics"""
    
    n: int = 60
    dt: float = 0.1
    dx: float = 1.0
    alpha: float = 1.0      # Attraction strength
    beta: float = 0.2       # Diffusion coefficient
    noise: float = 0.05     # Stochastic noise
    
    def __post_init__(self):
        self.operators = PDEOperators(self.n, self.dx)
        self.energy_func = EnergyFunctional(self.n)
        self._init_fields()
        self.history = {
            'energy': [],
            'total_density': []
        }
    
    def _init_fields(self):
        """Initialize density field with random values"""
        self.rho = [[random.uniform(0, 0.5) for _ in range(self.n)] for __ in range(self.n)]
        self.vx = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        self.vy = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        
        # Multi-attractor goal field
        self.goal = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        self.goal[self.n // 3][self.n // 3] = 1.0
        self.goal[2 * self.n // 3][2 * self.n // 3] = 1.0
    
    def _compute_force_field(self) -> List[List[float]]:
        """Compute total force field: -∇E + diffusion + attractor"""
        # Gradient of energy functional
        grad = self.energy_func.compute_gradient(self.rho, self.goal)
        
        # Negative gradient (descent)
        force = [[-grad[i][j] for j in range(self.n)] for i in range(self.n)]
        
        # Diffusion term
        laplacian = self.operators.laplacian(self.rho)
        for i in range(self.n):
            for j in range(self.n):
                force[i][j] += self.beta * laplacian[i][j]
        
        # Attractor force
        for i in range(self.n):
            for j in range(self.n):
                force[i][j] += self.alpha * (self.goal[i][j] - self.rho[i][j])
        
        return force
    
    def _add_noise(self, field: List[List[float]]) -> List[List[float]]:
        """Add stochastic noise (Wiener process)"""
        result = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                noise_val = self.noise * random.gauss(0, 1) * math.sqrt(self.dt)
                result[i][j] = field[i][j] + noise_val
        return result
    
    def step(self) -> Dict[str, Any]:
        """Execute one PDE step"""
        # Compute force field
        force = self._compute_force_field()
        
        # Update density field (continuum evolution)
        new_rho = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                new_rho[i][j] = self.rho[i][j] + self.dt * force[i][j]
        
        # Add stochastic perturbation
        new_rho = self._add_noise(new_rho)
        
        # Clamp to physical bounds
        for i in range(self.n):
            for j in range(self.n):
                new_rho[i][j] = max(0.0, min(1.0, new_rho[i][j]))
        
        self.rho = new_rho
        
        # Compute metrics
        energy = self.energy_func.compute(self.rho, self.goal)
        total_density = sum(sum(row) for row in self.rho)
        
        self.history['energy'].append(energy)
        self.history['total_density'].append(total_density)
        
        return {
            'rho': self.rho,
            'energy': energy,
            'total_density': total_density,
            'step': len(self.history['energy']) - 1
        }
    
    def run(self, steps: int) -> Dict[str, List[float]]:
        """Run simulation for multiple steps"""
        for _ in range(steps):
            self.step()
        return self.history
    
    def reset(self):
        """Reset solver state"""
        self._init_fields()
        self.history = {'energy': [], 'total_density': []}
    
    def get_energy_functional(self) -> float:
        """Get current energy value"""
        return self.energy_func.compute(self.rho, self.goal)


def create_pde_solver(n: int = 60, alpha: float = 1.0, beta: float = 0.2) -> PDESolver:
    """Factory function for PDE solver"""
    return PDESolver(n=n, alpha=alpha, beta=beta)
