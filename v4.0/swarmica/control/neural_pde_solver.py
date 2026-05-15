"""Neural PDE Solver for SWARMICA v4.0 - Controlled Reaction-Diffusion System"""

import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field

from ..neural_energy.energy_field import NeuralEnergyField
from ..pde.operators import AdvancedPDEOperators
from ..phase_transition.detector import PhaseTransitionDetector


@dataclass
class NeuralPDESolver:
    """Neural-controlled PDE solver with learnable energy functional"""
    
    n: int = 70
    dt: float = 0.1
    dx: float = 1.0
    alpha: float = 1.0      # Attractor strength
    beta: float = 0.25      # Diffusion coefficient
    noise: float = 0.05     # Stochastic noise
    energy_lr: float = 0.001  # Energy learning rate
    
    def __post_init__(self):
        self.operators = AdvancedPDEOperators(self.n, self.dx)
        self.energy_field = NeuralEnergyField(self.n, self.energy_lr)
        self.phase_detector = PhaseTransitionDetector()
        self._init_fields()
        self.history = {
            'energy': [],
            'order_parameter': [],
            'total_density': []
        }
    
    def _init_fields(self):
        """Initialize density and goal fields"""
        self.rho = [[random.uniform(0, 0.5) for _ in range(self.n)] for __ in range(self.n)]
        
        # Multi-attractor goal field
        self.goal = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        self.goal[self.n // 3][self.n // 3] = 1.0
        self.goal[2 * self.n // 3][2 * self.n // 3] = 1.0
    
    def _add_noise(self, field: List[List[float]]) -> List[List[float]]:
        """Add stochastic noise (Wiener process)"""
        result = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                noise_val = self.noise * random.gauss(0, 1) * math.sqrt(self.dt)
                result[i][j] = field[i][j] + noise_val
        return result
    
    def step(self) -> Dict[str, Any]:
        """Execute one PDE step with neural energy"""
        
        # Compute energy and gradient
        energy = self.energy_field.energy(self.rho, self.goal)
        energy_grad = self.energy_field.compute_gradient(self.rho, self.goal)
        
        # Get gradient of density field
        gx, gy = self.operators.gradient(self.rho)
        
        # Compute diffusion term
        diffusion = self.operators.laplacian(self.rho)
        
        # Compute attractor force
        attractor = [[self.alpha * (self.goal[i][j] - self.rho[i][j]) for j in range(self.n)] for i in range(self.n)]
        
        # PDE evolution: ∂ρ/∂t = -∇E - ∇ρ + D∇²ρ + α(G-ρ) + σ·dW
        new_rho = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                # Negative energy gradient (descent)
                neg_grad = -energy_grad[i][j]
                # Density gradient (advection-like)
                density_grad = -(gx[i][j] + gy[i][j])
                # Total update
                update = (neg_grad + density_grad + 
                         self.beta * diffusion[i][j] + 
                         attractor[i][j])
                
                new_rho[i][j] = self.rho[i][j] + self.dt * update
        
        # Add stochastic perturbation
        new_rho = self._add_noise(new_rho)
        
        # Clamp to physical bounds
        for i in range(self.n):
            for j in range(self.n):
                new_rho[i][j] = max(0.0, min(1.0, new_rho[i][j]))
        
        self.rho = new_rho
        
        # Online learning: adapt energy landscape
        self.energy_field.update(self.rho, self.goal)
        
        # Compute order parameter
        order_param = self.phase_detector.order_parameter(self.rho)
        self.phase_detector.update(order_param, energy)
        
        # Store history
        total_density = sum(sum(row) for row in self.rho)
        self.history['energy'].append(energy)
        self.history['order_parameter'].append(order_param)
        self.history['total_density'].append(total_density)
        
        return {
            'rho': self.rho,
            'energy': energy,
            'order_parameter': order_param,
            'total_density': total_density,
            'phase': self.phase_detector.get_phase(order_param),
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
        self.energy_field.reset()
        self.phase_detector.reset()
        self.history = {'energy': [], 'order_parameter': [], 'total_density': []}
    
    def get_phase_report(self) -> Dict[str, Any]:
        """Get phase transition analysis report"""
        return self.phase_detector.generate_report()


def create_neural_pde_solver(n: int = 70) -> NeuralPDESolver:
    """Factory function for neural PDE solver"""
    return NeuralPDESolver(n=n)
