"""Energy functional for SWARMICA v3.0"""

import math
from typing import List, Tuple


class EnergyFunctional:
    """Energy functional for continuum swarm dynamics"""
    
    def __init__(self, n: int = 60):
        self.n = n
    
    def compute(self, rho: List[List[float]], goal: List[List[float]]) -> float:
        """Compute total energy: E = ∫(ρ² + (ρ - goal)²) dΩ"""
        energy = 0.0
        
        for i in range(self.n):
            for j in range(self.n):
                # Internal energy (density squared)
                internal = rho[i][j] * rho[i][j]
                # Potential energy (distance from goal)
                potential = (rho[i][j] - goal[i][j]) ** 2
                energy += internal + potential
        
        return energy
    
    def compute_gradient(self, rho: List[List[float]], goal: List[List[float]]) -> List[List[float]]:
        """Compute gradient of energy functional: δE/δρ = 2ρ + 2(ρ - goal)"""
        grad = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        
        for i in range(self.n):
            for j in range(self.n):
                grad[i][j] = 2.0 * rho[i][j] + 2.0 * (rho[i][j] - goal[i][j])
        
        return grad
    
    def compute_free_energy(self, rho: List[List[float]], temperature: float = 1.0) -> float:
        """Compute free energy: F = E - T·S"""
        energy = self.compute(rho, [[0.0 for _ in range(self.n)] for __ in range(self.n)])
        entropy = self._compute_entropy(rho)
        return energy - temperature * entropy
    
    def _compute_entropy(self, rho: List[List[float]]) -> float:
        """Compute Shannon entropy of density field"""
        flat = []
        for i in range(self.n):
            for j in range(self.n):
                flat.append(max(rho[i][j], 1e-8))
        
        total = sum(flat)
        if total == 0:
            return 0.0
        
        entropy = 0.0
        for val in flat:
            p = val / total
            entropy -= p * math.log(p)
        
        return entropy


def create_energy_functional(n: int = 60) -> EnergyFunctional:
    """Factory function for energy functional"""
    return EnergyFunctional(n=n)
