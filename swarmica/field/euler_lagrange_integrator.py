"""Euler-Lagrange integrator for collective swarm dynamics"""

import math
from typing import List, Tuple, Callable, Optional


class EulerLagrangeIntegrator:
    """Numerical integrator for Euler-Lagrange equations"""
    
    def __init__(self, n_basis: int = 64, dt: float = 0.001):
        self.n_basis = n_basis
        self.dt = dt
    
    def rk4_step(self, q: List[float], q_dot: List[float], 
                 acceleration_func: Callable) -> Tuple[List[float], List[float]]:
        """4th order Runge-Kutta integration"""
        
        # k1
        a1 = acceleration_func(q, q_dot)
        k1_q = [v * self.dt for v in q_dot]
        k1_v = [a * self.dt for a in a1]
        
        # k2
        q2 = [q[i] + 0.5 * k1_q[i] for i in range(self.n_basis)]
        v2 = [q_dot[i] + 0.5 * k1_v[i] for i in range(self.n_basis)]
        a2 = acceleration_func(q2, v2)
        k2_q = [v * self.dt for v in v2]
        k2_v = [a * self.dt for a in a2]
        
        # k3
        q3 = [q[i] + 0.5 * k2_q[i] for i in range(self.n_basis)]
        v3 = [q_dot[i] + 0.5 * k2_v[i] for i in range(self.n_basis)]
        a3 = acceleration_func(q3, v3)
        k3_q = [v * self.dt for v in v3]
        k3_v = [a * self.dt for a in a3]
        
        # k4
        q4 = [q[i] + k3_q[i] for i in range(self.n_basis)]
        v4 = [q_dot[i] + k3_v[i] for i in range(self.n_basis)]
        a4 = acceleration_func(q4, v4)
        k4_q = [v * self.dt for v in v4]
        k4_v = [a * self.dt for a in a4]
        
        # Combine
        q_new = [q[i] + (k1_q[i] + 2*k2_q[i] + 2*k3_q[i] + k4_q[i]) / 6.0 for i in range(self.n_basis)]
        v_new = [q_dot[i] + (k1_v[i] + 2*k2_v[i] + 2*k3_v[i] + k4_v[i]) / 6.0 for i in range(self.n_basis)]
        
        return q_new, v_new
    
    def symplectic_euler(self, q: List[float], q_dot: List[float],
                         acceleration_func: Callable) -> Tuple[List[float], List[float]]:
        """Symplectic Euler integrator (energy-conserving for Hamiltonian systems)"""
        # Update velocity first, then position
        a = acceleration_func(q, q_dot)
        q_dot_new = [q_dot[i] + a[i] * self.dt for i in range(self.n_basis)]
        q_new = [q[i] + q_dot_new[i] * self.dt for i in range(self.n_basis)]
        return q_new, q_dot_new
    
    def integrate(self, q0: List[float], q_dot0: List[float], 
                  acceleration_func: Callable, steps: int,
                  method: str = 'rk4') -> Tuple[List[List[float]], List[List[float]]]:
        """Integrate dynamics over multiple steps"""
        q = q0.copy()
        q_dot = q_dot0.copy()
        trajectory = [q.copy()]
        velocities = [q_dot.copy()]
        
        for _ in range(steps):
            if method == 'rk4':
                q, q_dot = self.rk4_step(q, q_dot, acceleration_func)
            else:
                q, q_dot = self.symplectic_euler(q, q_dot, acceleration_func)
            trajectory.append(q.copy())
            velocities.append(q_dot.copy())
        
        return trajectory, velocities
