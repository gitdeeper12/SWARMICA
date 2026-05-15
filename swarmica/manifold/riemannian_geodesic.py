"""Riemannian geodesic solver on the Physical Coupling Manifold"""

import math
from typing import List, Tuple, Callable


class RiemannianGeodesic:
    """Geodesic solver on manifold M with metric G(Q)"""
    
    def __init__(self, n_basis: int = 64):
        self.n_basis = n_basis
    
    def geodesic_equation(self, q: List[float], q_dot: List[float], 
                          christoffel: List[List[List[float]]]) -> List[float]:
        """Geodesic equation: q̈^k + Γ^k_ij q̇^i q̇^j = 0"""
        acceleration = [0.0] * self.n_basis
        
        for k in range(self.n_basis):
            total = 0.0
            for i in range(self.n_basis):
                for j in range(self.n_basis):
                    if i < len(q_dot) and j < len(q_dot):
                        total += christoffel[i][j][k] * q_dot[i] * q_dot[j]
            acceleration[k] = -total
        
        return acceleration
    
    def integrate_geodesic(self, q0: List[float], q_dot0: List[float], 
                           christoffel_func: Callable, dt: float, steps: int) -> Tuple[List[List[float]], List[List[float]]]:
        """Integrate geodesic using Euler method"""
        q = q0.copy()
        q_dot = q_dot0.copy()
        trajectory = [q.copy()]
        velocities = [q_dot.copy()]
        
        for _ in range(steps):
            # Compute Christoffel at current point
            christoffel = christoffel_func(q)
            
            # Compute acceleration from geodesic equation
            accel = self.geodesic_equation(q, q_dot, christoffel)
            
            # Euler integration
            for i in range(self.n_basis):
                q_dot[i] += accel[i] * dt
                q[i] += q_dot[i] * dt
            
            trajectory.append(q.copy())
            velocities.append(q_dot.copy())
        
        return trajectory, velocities
    
    def geodesic_distance(self, q1: List[float], q2: List[float], metric: List[List[float]]) -> float:
        """Approximate geodesic distance between two points (simplified)"""
        distance = 0.0
        for i in range(min(self.n_basis, len(q1), len(q2))):
            diff = q1[i] - q2[i]
            g_ii = metric[i][i] if i < len(metric) else 1.0
            distance += g_ii * diff * diff
        return math.sqrt(distance)
