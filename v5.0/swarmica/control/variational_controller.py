"""Variational controller for SWARMICA v5.0"""

import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field

from ..variational.operators import VariationalOperators
from ..variational.cost_functional import CostFunctional


@dataclass
class VariationalController:
    n: int = 80
    dt: float = 0.1
    dx: float = 1.0
    alpha: float = 1.2
    beta: float = 0.3
    sigma: float = 0.08
    control_gain: float = 0.6
    
    def __post_init__(self):
        self.operators = VariationalOperators(self.n, self.dx)
        self.cost = CostFunctional(self.n)
        self._init_fields()
        self.history = {
            'energy': [],
            'entropy': [],
            'control_cost': [],
            'total_cost': []
        }
    
    def _init_fields(self):
        self.rho = [[random.uniform(0, 0.4) for _ in range(self.n)] for __ in range(self.n)]
        
        self.goal = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        self.goal[self.n // 4][self.n // 4] = 1.0
        self.goal[3 * self.n // 4][3 * self.n // 4] = 1.0
        
        self.control = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
    
    def _add_noise(self, field: List[List[float]]) -> List[List[float]]:
        result = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                noise_val = self.sigma * random.gauss(0, 1) * math.sqrt(self.dt)
                result[i][j] = field[i][j] + noise_val
        return result
    
    def _compute_optimal_control(self) -> List[List[float]]:
        control = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                control[i][j] = self.control_gain * (self.goal[i][j] - self.rho[i][j])
        return control
    
    def step(self) -> Dict[str, Any]:
        gx, gy = self.operators.gradient(self.rho)
        
        drift = [[-(gx[i][j] + gy[i][j]) for j in range(self.n)] for i in range(self.n)]
        
        diffusion = self.operators.laplacian(self.rho)
        for i in range(self.n):
            for j in range(self.n):
                diffusion[i][j] = self.beta * diffusion[i][j]
        
        error = [[self.goal[i][j] - self.rho[i][j] for j in range(self.n)] for i in range(self.n)]
        
        self.control = self._compute_optimal_control()
        
        new_rho = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                update = (drift[i][j] + diffusion[i][j] + 
                         self.alpha * error[i][j] + self.control[i][j])
                new_rho[i][j] = self.rho[i][j] + self.dt * update
        
        new_rho = self._add_noise(new_rho)
        
        for i in range(self.n):
            for j in range(self.n):
                new_rho[i][j] = max(0.0, min(1.0, new_rho[i][j]))
        
        self.rho = new_rho
        
        energy_cost = self.cost.energy(self.rho, self.goal)
        entropy_cost = self.cost.entropy(self.rho)
        control_cost = self.cost.control_cost(self.control)
        total_cost = self.cost.total_cost(self.rho, self.goal, self.control)
        
        self.history['energy'].append(energy_cost)
        self.history['entropy'].append(entropy_cost)
        self.history['control_cost'].append(control_cost)
        self.history['total_cost'].append(total_cost)
        
        return {
            'rho': self.rho,
            'energy': energy_cost,
            'entropy': entropy_cost,
            'control_cost': control_cost,
            'total_cost': total_cost,
            'step': len(self.history['energy']) - 1
        }
    
    def run(self, steps: int) -> Dict[str, List[float]]:
        for _ in range(steps):
            self.step()
        return self.history
    
    def reset(self):
        self._init_fields()
        self.history = {
            'energy': [],
            'entropy': [],
            'control_cost': [],
            'total_cost': []
        }


def create_variational_controller(n: int = 80) -> VariationalController:
    return VariationalController(n=n)
