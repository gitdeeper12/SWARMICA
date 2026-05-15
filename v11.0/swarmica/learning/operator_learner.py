"""Operator learning for SWARMICA v11.0 - Neural operator training"""

import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field


@dataclass
class OperatorLearner:
    """Learn the neural operator Fθ from trajectory data"""
    
    N: int = 64
    learning_rate: float = 0.01
    momentum: float = 0.9
    
    def __post_init__(self):
        self._init_weights()
        self.trajectory_buffer = []
        self.history = {
            'training_loss': [],
            'validation_loss': [],
            'operator_norm': []
        }
    
    def _init_weights(self):
        """Initialize operator weights"""
        self.W_real = [[random.uniform(-0.1, 0.1) for _ in range(self.N)] for __ in range(self.N)]
        self.W_imag = [[random.uniform(-0.1, 0.1) for _ in range(self.N)] for __ in range(self.N)]
        self.velocity_real = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        self.velocity_imag = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
    
    def forward(self, rho: List[List[float]], vx: List[List[float]], vy: List[List[float]]) -> Tuple[List[List[float]], List[List[float]], List[List[float]]]:
        """Forward pass: predict dynamics"""
        drho = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        dvx = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        dvy = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        
        for i in range(self.N):
            for j in range(self.N):
                w = self.W_real[i][j] * math.cos(rho[i][j]) + self.W_imag[i][j] * math.sin(rho[i][j])
                drho[i][j] = w * rho[i][j] * (1 - rho[i][j])
                dvx[i][j] = w * (vx[i][j] + vy[i][j]) - 0.1 * vx[i][j]
                dvy[i][j] = w * (vx[i][j] + vy[i][j]) - 0.1 * vy[i][j]
        
        return drho, dvx, dvy
    
    def compute_loss(self, pred_drho: List[List[float]], true_drho: List[List[float]],
                     pred_dvx: List[List[float]], true_dvx: List[List[float]]) -> float:
        """Compute MSE loss"""
        loss = 0.0
        for i in range(self.N):
            for j in range(self.N):
                loss += (pred_drho[i][j] - true_drho[i][j]) ** 2
                loss += (pred_dvx[i][j] - true_dvx[i][j]) ** 2
        return loss / (2 * self.N * self.N)
    
    def update(self, rho: List[List[float]], vx: List[List[float]], vy: List[List[float]],
               target_drho: List[List[float]], target_dvx: List[List[float]], target_dvy: List[List[float]]) -> float:
        """Update operator weights using gradient descent with momentum"""
        
        # Forward pass
        pred_drho, pred_dvx, pred_dvy = self.forward(rho, vx, vy)
        
        # Compute loss
        loss = self.compute_loss(pred_drho, target_drho, pred_dvx, target_dvx)
        self.history['training_loss'].append(loss)
        
        # Update weights (simplified gradient descent)
        for i in range(self.N):
            for j in range(self.N):
                error_rho = target_drho[i][j] - pred_drho[i][j]
                error_v = target_dvx[i][j] - pred_dvx[i][j]
                
                # Gradient w.r.t weights
                grad_real = error_rho * math.cos(rho[i][j]) + error_v * math.cos(rho[i][j])
                grad_imag = error_rho * math.sin(rho[i][j]) + error_v * math.sin(rho[i][j])
                
                # Momentum update
                self.velocity_real[i][j] = self.momentum * self.velocity_real[i][j] + self.learning_rate * grad_real
                self.velocity_imag[i][j] = self.momentum * self.velocity_imag[i][j] + self.learning_rate * grad_imag
                
                self.W_real[i][j] += self.velocity_real[i][j]
                self.W_imag[i][j] += self.velocity_imag[i][j]
                
                # Clamp
                self.W_real[i][j] = max(-0.5, min(0.5, self.W_real[i][j]))
                self.W_imag[i][j] = max(-0.5, min(0.5, self.W_imag[i][j]))
        
        # Compute operator norm
        op_norm = 0.0
        for i in range(self.N):
            for j in range(self.N):
                op_norm += self.W_real[i][j] ** 2 + self.W_imag[i][j] ** 2
        self.history['operator_norm'].append(math.sqrt(op_norm / (self.N * self.N)))
        
        return loss
    
    def add_trajectory(self, rho: List[List[float]], drho: List[List[float]], step: int):
        """Add trajectory data for training"""
        # Store compressed snapshot
        snapshot = []
        for i in range(min(10, self.N)):
            for j in range(min(10, self.N)):
                snapshot.append(rho[i][j])
        
        self.trajectory_buffer.append({
            'step': step,
            'snapshot': snapshot,
            'drho_sample': drho[0][0] if drho else 0
        })
        
        if len(self.trajectory_buffer) > 200:
            self.trajectory_buffer.pop(0)
    
    def validate(self, rho: List[List[float]], vx: List[List[float]], vy: List[List[float]],
                 true_drho: List[List[float]], true_dvx: List[List[float]]) -> float:
        """Validate operator on test data"""
        pred_drho, pred_dvx, _ = self.forward(rho, vx, vy)
        val_loss = self.compute_loss(pred_drho, true_drho, pred_dvx, true_dvx)
        self.history['validation_loss'].append(val_loss)
        return val_loss
    
    def get_operator_weights(self) -> Tuple[List[List[float]], List[List[float]]]:
        """Get current operator weights"""
        return self.W_real, self.W_imag
    
    def get_learning_curve(self) -> Dict[str, List[float]]:
        """Get learning curve data"""
        return self.history
    
    def reset(self):
        """Reset learner state"""
        self._init_weights()
        self.trajectory_buffer = []
        self.history = {'training_loss': [], 'validation_loss': [], 'operator_norm': []}


class PhysicsLawDiscovery:
    """Discover the physical law from learned operator"""
    
    def __init__(self, N: int = 64):
        self.N = N
    
    def discover_law(self, W_real: List[List[float]], W_imag: List[List[float]]) -> Dict[str, Any]:
        """Analyze learned operator to discover physical law"""
        
        # Compute statistics
        real_mean = 0.0
        imag_mean = 0.0
        real_std = 0.0
        imag_std = 0.0
        
        for i in range(self.N):
            for j in range(self.N):
                real_mean += W_real[i][j]
                imag_mean += W_imag[i][j]
        
        real_mean /= (self.N * self.N)
        imag_mean /= (self.N * self.N)
        
        for i in range(self.N):
            for j in range(self.N):
                real_std += (W_real[i][j] - real_mean) ** 2
                imag_std += (W_imag[i][j] - imag_mean) ** 2
        
        real_std = math.sqrt(real_std / (self.N * self.N))
        imag_std = math.sqrt(imag_std / (self.N * self.N))
        
        # Discover law type based on weight distribution
        if real_std < 0.05 and imag_std < 0.05:
            law_type = "Homogeneous Linear PDE"
            law_equation = "∂ρ/∂t = κ∇²ρ + f(x)"
        elif real_std > 0.2:
            law_type = "Nonlinear Reaction-Diffusion"
            law_equation = "∂ρ/∂t = D∇²ρ + R(ρ)"
        elif imag_std > 0.2:
            law_type = "Wave-like Dynamics"
            law_equation = "∂²ρ/∂t² = c²∇²ρ"
        else:
            law_type = "Mixed (Conservation + Dissipation)"
            law_equation = "∂ρ/∂t = -∇·(ρv) + D∇²ρ"
        
        # Determine system behavior
        if real_mean > 0:
            behavior = "Source-dominant (Energy increasing)"
        elif real_mean < 0:
            behavior = "Sink-dominant (Energy decreasing)"
        else:
            behavior = "Conservative (Energy preserving)"
        
        return {
            'discovered_law': law_type,
            'law_equation': law_equation,
            'system_behavior': behavior,
            'operator_mean': real_mean,
            'operator_std': real_std,
            'complexity': real_std + imag_std
        }


def create_operator_learner(N: int = 64) -> OperatorLearner:
    """Factory function for operator learner"""
    return OperatorLearner(N=N)


def create_physics_law_discovery(N: int = 64) -> PhysicsLawDiscovery:
    """Factory function for physics law discovery"""
    return PhysicsLawDiscovery(N=N)
