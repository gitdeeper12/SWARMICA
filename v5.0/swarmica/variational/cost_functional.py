"""Cost functional for SWARMICA v5.0 - Variational optimal control"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class CostFunctional:
    """Cost functional J = ∫(E + λ_s·S + λ_c·C) dt"""
    
    n: int = 80
    lambda_entropy: float = 0.1
    lambda_control: float = 0.01
    
    def energy(self, rho: List[List[float]], goal: List[List[float]]) -> float:
        total = 0.0
        for i in range(self.n):
            for j in range(self.n):
                total += (rho[i][j] - goal[i][j]) ** 2
        return total
    
    def entropy(self, rho: List[List[float]]) -> float:
        total_density = 0.0
        for i in range(self.n):
            for j in range(self.n):
                total_density += rho[i][j]
        
        if total_density < 1e-8:
            return 0.0
        
        entropy_val = 0.0
        for i in range(self.n):
            for j in range(self.n):
                p = rho[i][j] / total_density
                if p > 1e-8:
                    entropy_val -= p * math.log(p)
        return entropy_val
    
    def control_cost(self, control: List[List[float]]) -> float:
        total = 0.0
        for i in range(self.n):
            for j in range(self.n):
                total += control[i][j] ** 2
        return total
    
    def total_cost(self, rho: List[List[float]], goal: List[List[float]], 
                   control: List[List[float]]) -> float:
        e = self.energy(rho, goal)
        s = self.entropy(rho)
        c = self.control_cost(control)
        return e + self.lambda_entropy * s + self.lambda_control * c
    
    def energy_gradient(self, rho: List[List[float]], goal: List[List[float]]) -> List[List[float]]:
        grad = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                grad[i][j] = 2.0 * (rho[i][j] - goal[i][j])
        return grad


def create_cost_functional(n: int = 80) -> CostFunctional:
    return CostFunctional(n=n)
