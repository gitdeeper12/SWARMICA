"""Neural Operator Solver for SWARMICA v11.0 - Optimized"""

import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field

from ..neural_operator.operator import NeuralOperator
from ..spectral.fourier import FourierSpectralLayer


@dataclass
class NeuralOperatorSolver:
    """Neural operator solver - Optimized for performance"""
    
    N: int = 64
    dt: float = 0.01
    learning: bool = True
    
    def __post_init__(self):
        self.operator = NeuralOperator(self.N)
        self.spectral = FourierSpectralLayer(self.N, n_modes=8)
        self._init_fields()
        self.history = {
            'entropy': [],
            'energy': [],
            'operator_loss': [],
            'coherence': []
        }
    
    def _init_fields(self):
        """Initialize density and velocity fields"""
        N = self.N
        self.rho = [[0.0 for _ in range(N)] for __ in range(N)]
        center = N // 2
        for i in range(N):
            for j in range(N):
                dx = i - center
                dy = j - center
                self.rho[i][j] = 0.3 * math.exp(-(dx*dx + dy*dy) / (2 * (N/8)**2)) + 0.05 * random.random()
        
        self.vx = [[0.0 for _ in range(N)] for __ in range(N)]
        self.vy = [[0.0 for _ in range(N)] for __ in range(N)]
        
        # Target field
        self.target = [[0.0 for _ in range(N)] for __ in range(N)]
        self.target[N//4][N//4] = 1.0
        self.target[3*N//4][3*N//4] = 1.0
    
    def _entropy(self) -> float:
        """Shannon entropy"""
        N = self.N
        total = 0.0
        for i in range(N):
            for j in range(N):
                total += self.rho[i][j]
        
        if total < 1e-8:
            return 0.0
        
        entropy = 0.0
        for i in range(N):
            for j in range(N):
                p = self.rho[i][j] / total
                if p > 1e-8:
                    entropy -= p * math.log(p)
        return entropy
    
    def _energy(self) -> float:
        """Total energy"""
        N = self.N
        energy = 0.0
        for i in range(N):
            for j in range(N):
                energy += self.rho[i][j] * self.rho[i][j]
        return energy / (N * N)
    
    def _coherence(self) -> float:
        """Coherence index"""
        N = self.N
        mean = 0.0
        for i in range(N):
            for j in range(N):
                mean += self.rho[i][j]
        mean /= (N * N)
        
        variance = 0.0
        for i in range(N):
            for j in range(N):
                variance += (self.rho[i][j] - mean) ** 2
        variance /= (N * N)
        
        return 1.0 / (1.0 + variance)
    
    def _true_dynamics(self) -> Tuple[List[List[float]], List[List[float]], List[List[float]]]:
        """Compute true dynamics for learning"""
        N = self.N
        drho_true = [[0.0 for _ in range(N)] for __ in range(N)]
        dvx_true = [[0.0 for _ in range(N)] for __ in range(N)]
        dvy_true = [[0.0 for _ in range(N)] for __ in range(N)]
        
        for i in range(N):
            for j in range(N):
                drho_true[i][j] = 0.5 * (self.target[i][j] - self.rho[i][j])
                dvx_true[i][j] = -0.3 * self.vx[i][j]
                dvy_true[i][j] = -0.3 * self.vy[i][j]
        
        return drho_true, dvx_true, dvy_true
    
    def step(self) -> Dict[str, Any]:
        """Execute one neural operator step"""
        N = self.N
        
        # Apply spectral transform
        rho_spectral = self.spectral.forward(self.rho)
        
        # Neural operator predicts dynamics
        drho_pred, dvx_pred, dvy_pred = self.operator.forward(self.rho, self.vx, self.vy)
        
        # Mix with spectral features
        for i in range(N):
            for j in range(N):
                drho_pred[i][j] = 0.7 * drho_pred[i][j] + 0.3 * (rho_spectral[i][j] - self.rho[i][j])
        
        # Learning
        if self.learning:
            drho_true, dvx_true, dvy_true = self._true_dynamics()
            loss = self.operator.update(self.rho, self.vx, self.vy, 
                                        drho_true, dvx_true, dvy_true)
            self.history['operator_loss'].append(loss)
        
        # Integrate dynamics
        new_rho = [[0.0 for _ in range(N)] for __ in range(N)]
        new_vx = [[0.0 for _ in range(N)] for __ in range(N)]
        new_vy = [[0.0 for _ in range(N)] for __ in range(N)]
        
        for i in range(N):
            for j in range(N):
                new_rho[i][j] = self.rho[i][j] + self.dt * drho_pred[i][j]
                new_vx[i][j] = self.vx[i][j] + self.dt * dvx_pred[i][j]
                new_vy[i][j] = self.vy[i][j] + self.dt * dvy_pred[i][j]
                new_rho[i][j] = max(0.0, min(1.0, new_rho[i][j]))
        
        self.rho = new_rho
        self.vx = new_vx
        self.vy = new_vy
        
        # Metrics
        entropy_val = self._entropy()
        energy_val = self._energy()
        coherence_val = self._coherence()
        
        self.history['entropy'].append(entropy_val)
        self.history['energy'].append(energy_val)
        self.history['coherence'].append(coherence_val)
        
        return {
            'rho': self.rho,
            'entropy': entropy_val,
            'energy': energy_val,
            'coherence': coherence_val,
            'operator_loss': self.history['operator_loss'][-1] if self.history['operator_loss'] else 0,
            'step': len(self.history['entropy']) - 1
        }
    
    def run(self, steps: int = 200) -> Dict[str, List[float]]:
        """Run simulation for multiple steps"""
        for _ in range(steps):
            self.step()
            # Print progress every 50 steps
            if (_ + 1) % 50 == 0:
                print(f"  Progress: {_+1}/{steps} steps")
        return self.history
    
    def reset(self):
        """Reset solver state"""
        self._init_fields()
        self.operator.reset()
        self.history = {'entropy': [], 'energy': [], 'operator_loss': [], 'coherence': []}
    
    def get_operator_info(self) -> Dict[str, Any]:
        """Get neural operator information"""
        return self.operator.get_operator_spectrum()


def create_neural_operator_solver(N: int = 64) -> NeuralOperatorSolver:
    """Factory function for neural operator solver"""
    return NeuralOperatorSolver(N=N)
