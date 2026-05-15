"""Continuous Controller for SWARMICA v7.0 - Neural Controlled PDE System"""

import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field

from ..continuous_control.operators import ContinuousControlOperators
from ..neural_operator.operator import NeuralOperator
from ..stability.lyapunov import LyapunovStability


@dataclass
class ContinuousController:
    """Continuous-time optimal control for PDE swarm dynamics"""
    
    n: int = 100
    dt: float = 0.05
    dx: float = 1.0
    beta: float = 0.3      # Diffusion coefficient
    sigma: float = 0.1     # Noise strength
    K_gain: float = 1.2    # Control gain
    lambda_reg: float = 0.5  # Regularization parameter
    
    def __post_init__(self):
        self.operators = ContinuousControlOperators(self.n, self.dx)
        self.neural_op = NeuralOperator(self.n)
        self.stability = LyapunovStability(self.n, self.lambda_reg)
        self._init_fields()
        self.history = {
            'energy': [],
            'stability_metric': [],
            'lyapunov': []
        }
    
    def _init_fields(self):
        """Initialize density and target fields"""
        self.rho = [[random.uniform(0, 0.4) for _ in range(self.n)] for __ in range(self.n)]
        
        # Multi-attractor target field ρ*
        self.target = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        self.target[self.n // 4][self.n // 4] = 1.0
        self.target[3 * self.n // 4][3 * self.n // 4] = 1.0
    
    def _control_law(self) -> List[List[float]]:
        """Continuous control law: u*(x,t) = -K ∇Φ(ρ)"""
        grad_mag = self.operators.gradient_magnitude(self.rho)
        control = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        
        for i in range(self.n):
            for j in range(self.n):
                control[i][j] = -self.K_gain * grad_mag[i][j]
        
        return control
    
    def _add_noise(self) -> List[List[float]]:
        """Stochastic forcing: σ·ξ(x,t)"""
        noise = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                noise[i][j] = self.sigma * random.gauss(0, 1) * math.sqrt(self.dt)
        return noise
    
    def step(self) -> Dict[str, Any]:
        """Execute one continuous-time PDE step"""
        
        # 1. Neural operator: Nθ(ρ)
        F_theta = self.neural_op.forward(self.rho)
        
        # 2. Control law: u*(x,t)
        control = self._control_law()
        
        # 3. Diffusion term: βΔρ
        diffusion = self.operators.laplacian(self.rho)
        for i in range(self.n):
            for j in range(self.n):
                diffusion[i][j] = self.beta * diffusion[i][j]
        
        # 4. Stochastic forcing
        noise = self._add_noise()
        
        # 5. PDE evolution (continuous system)
        # ∂ρ/∂t = Nθ(ρ) + u* + βΔρ + σξ
        new_rho = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                update = (F_theta[i][j] + control[i][j] + 
                         diffusion[i][j] + noise[i][j])
                new_rho[i][j] = self.rho[i][j] + self.dt * update
        
        # Clamp to physical bounds
        for i in range(self.n):
            for j in range(self.n):
                new_rho[i][j] = max(0.0, min(1.0, new_rho[i][j]))
        
        self.rho = new_rho
        
        # 6. Compute metrics
        lap = self.operators.laplacian(self.rho)
        grad_mag = self.operators.gradient_magnitude(self.rho)
        
        energy = self.stability.energy_functional(self.rho, self.target, lap)
        stability_metric = self.stability.stability_metric(self.rho)
        lyapunov = self.stability.lyapunov_function(self.rho, self.target, grad_mag)
        
        self.history['energy'].append(energy)
        self.history['stability_metric'].append(stability_metric)
        self.history['lyapunov'].append(lyapunov)
        
        # 7. Update neural operator parameters
        self.neural_op.update(self.rho, self.target, grad_mag)
        
        return {
            'rho': self.rho,
            'control': control,
            'energy': energy,
            'stability_metric': stability_metric,
            'lyapunov': lyapunov,
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
        self.history = {'energy': [], 'stability_metric': [], 'lyapunov': []}
    
    def get_stability_certificate(self) -> Dict[str, Any]:
        """Generate stability certificate based on Lyapunov analysis"""
        if len(self.history['lyapunov']) < 10:
            return {'certified': False, 'reason': 'Insufficient data'}
        
        lyapunov_final = self.history['lyapunov'][-1]
        lyapunov_initial = self.history['lyapunov'][0]
        lyapunov_decay = (lyapunov_initial - lyapunov_final) / (lyapunov_initial + 1e-8)
        
        stability_final = self.history['stability_metric'][-1]
        
        certified = (lyapunov_decay > 0.1 and stability_final > 0.7)
        
        return {
            'certified': certified,
            'lyapunov_decay': lyapunov_decay,
            'final_stability': stability_final,
            'energy_reduction': (self.history['energy'][0] - self.history['energy'][-1]) / (self.history['energy'][0] + 1e-8) * 100
        }


def create_continuous_controller(n: int = 100) -> ContinuousController:
    """Factory function for continuous controller"""
    return ContinuousController(n=n)
