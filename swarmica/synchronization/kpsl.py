"""Kuramoto Phase Synchronization Layer (KPSL) - modified Kuramoto model for swarm phase coherence"""

import math
import random
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class KuramotoPhaseSynchronization:
    """KPSL: dθ_i/dt = ω_i + (K/N) Σ sin(θ_j - θ_i) + F_ext,i"""
    
    n_agents: int = 500
    k_coupling: float = 3.0  # K = 3 * K_c (overcritical)
    delta_freq: float = 0.5  # half-width of Lorentzian distribution
    dt: float = 0.001
    
    def __post_init__(self):
        """Initialize agent natural frequencies"""
        self.omega = []  # natural frequencies ω_i
        self.theta = []  # current phases θ_i
        self._init_frequencies()
        self._init_phases()
    
    def _init_frequencies(self):
        """Initialize ω_i from Lorentzian distribution: g(ω) = (Δ/π) / ((ω-ω₀)² + Δ²)"""
        for _ in range(self.n_agents):
            # Simplified Lorentzian sampling using Cauchy distribution
            u = random.uniform(0, 1)
            # Inverse CDF of Cauchy: ω = ω₀ + Δ * tan(π(u - 0.5))
            omega = self.delta_freq * math.tan(math.pi * (u - 0.5))
            self.omega.append(omega)
    
    def _init_phases(self):
        """Initialize random phases θ_i ∈ [0, 2π)"""
        for _ in range(self.n_agents):
            self.theta.append(random.uniform(0, 2 * math.pi))
    
    @property
    def critical_coupling(self) -> float:
        """K_c = 2Δ for Lorentzian distribution"""
        return 2.0 * self.delta_freq
    
    @property
    def order_parameter_theoretical(self) -> float:
        """r_∞ = √(1 - K_c/K) for K > K_c"""
        kc = self.critical_coupling
        if self.k_coupling <= kc:
            return 0.0
        return math.sqrt(1.0 - kc / self.k_coupling)
    
    def compute_order_parameter(self) -> Tuple[float, float]:
        """r(t) = |(1/N) Σ e^{iθ_i}|, φ(t) = arg(Σ e^{iθ_i})"""
        sum_cos = 0.0
        sum_sin = 0.0
        for theta in self.theta:
            sum_cos += math.cos(theta)
            sum_sin += math.sin(theta)
        
        r = math.sqrt(sum_cos * sum_cos + sum_sin * sum_sin) / self.n_agents
        phi = math.atan2(sum_sin, sum_cos)
        return r, phi
    
    def step(self, external_forces: List[float] = None) -> List[float]:
        """Update phases using modified Kuramoto dynamics"""
        # Compute mean field
        mean_cos = 0.0
        mean_sin = 0.0
        for theta in self.theta:
            mean_cos += math.cos(theta)
            mean_sin += math.sin(theta)
        mean_cos /= self.n_agents
        mean_sin /= self.n_agents
        
        # Update each agent
        new_theta = []
        for i, theta in enumerate(self.theta):
            # Mean field coupling term
            coupling = self.k_coupling * (mean_sin * math.cos(theta) - mean_cos * math.sin(theta))
            # External force
            ext = external_forces[i] if external_forces and i < len(external_forces) else 0.0
            # Euler integration
            dtheta_dt = self.omega[i] + coupling + ext
            new_theta_i = theta + self.dt * dtheta_dt
            # Wrap to [0, 2π)
            new_theta.append(new_theta_i % (2 * math.pi))
        
        self.theta = new_theta
        return self.theta
    
    def reset(self):
        """Reset phases to random values"""
        self._init_phases()


def create_kpsl(n_agents: int = 500, k_coupling: float = 3.0, delta: float = 0.5) -> KuramotoPhaseSynchronization:
    """Factory function to create Kuramoto Phase Synchronization Layer"""
    return KuramotoPhaseSynchronization(n_agents=n_agents, k_coupling=k_coupling, delta_freq=delta)
