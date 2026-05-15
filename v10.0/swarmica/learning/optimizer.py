"""Learning optimizer for SWARMICA v10.0 - Neural physics discovery"""

import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field


@dataclass
class NeuralPhysicsLearner:
    """Learn physical laws from swarm trajectories"""
    
    N: int = 100
    learning_rate: float = 0.01
    momentum: float = 0.9
    
    def __post_init__(self):
        self._init_weights()
        self.history = {'loss': [], 'energy_error': []}
    
    def _init_weights(self):
        """Initialize learnable weights"""
        self.weights = [[random.uniform(-0.1, 0.1) for _ in range(self.N)] for __ in range(self.N)]
        self.velocity = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
    
    def compute_energy(self, rho: List[List[float]]) -> float:
        """Learned energy functional E_θ(ρ)"""
        # Energy = linear + quadratic terms with learned weights
        linear = 0.0
        quadratic = 0.0
        
        for i in range(self.N):
            for j in range(self.N):
                linear += self.weights[i][j] * rho[i][j]
                quadratic += self.weights[i][j] * rho[i][j] * rho[i][j]
        
        linear /= (self.N * self.N)
        quadratic /= (self.N * self.N)
        
        return math.tanh(linear) + 0.5 * quadratic
    
    def energy_gradient(self, rho: List[List[float]]) -> List[List[float]]:
        """Compute ∇E_θ(ρ) for learning"""
        grad = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        
        for i in range(self.N):
            for j in range(self.N):
                # Derivative of energy w.r.t density
                grad[i][j] = self.weights[i][j] * (1 + 2 * rho[i][j])
        
        return grad
    
    def update(self, rho: List[List[float]], target_energy: float):
        """Update weights using gradient descent with momentum"""
        current_energy = self.compute_energy(rho)
        error = target_energy - current_energy
        
        loss = error * error
        self.history['loss'].append(loss)
        self.history['energy_error'].append(error)
        
        # Update weights with momentum
        for i in range(self.N):
            for j in range(self.N):
                gradient = 2 * error * rho[i][j] * (1 + rho[i][j])
                self.velocity[i][j] = self.momentum * self.velocity[i][j] - self.learning_rate * gradient
                self.weights[i][j] += self.velocity[i][j]
                # Clamp
                self.weights[i][j] = max(-0.5, min(0.5, self.weights[i][j]))
    
    def predict_force(self, rho: List[List[float]]) -> List[List[float]]:
        """Predict force field from learned physics"""
        force = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        grad = self.energy_gradient(rho)
        
        for i in range(self.N):
            for j in range(self.N):
                force[i][j] = -grad[i][j]
        
        return force
    
    def get_weights(self) -> List[List[float]]:
        """Get learned weights"""
        return self.weights
    
    def reset(self):
        """Reset learner state"""
        self._init_weights()
        self.history = {'loss': [], 'energy_error': []}
    
    def get_learning_curve(self) -> Dict[str, List[float]]:
        """Get learning curve data"""
        return self.history


class PhysicsDiscovery:
    """Discover physical laws from swarm trajectories"""
    
    def __init__(self, N: int = 100):
        self.N = N
        self.learner = NeuralPhysicsLearner(N)
        self.trajectories = []
    
    def record_trajectory(self, rho: List[List[float]], step: int):
        """Record density trajectory for learning"""
        # Store compressed representation
        snapshot = []
        for i in range(min(10, self.N)):
            for j in range(min(10, self.N)):
                snapshot.append(rho[i][j])
        self.trajectories.append({
            'step': step,
            'snapshot': snapshot,
            'entropy': self._compute_entropy(rho)
        })
        
        # Keep only recent trajectories
        if len(self.trajectories) > 100:
            self.trajectories.pop(0)
    
    def _compute_entropy(self, rho: List[List[float]]) -> float:
        total = 0.0
        for i in range(self.N):
            for j in range(self.N):
                total += rho[i][j]
        
        if total < 1e-8:
            return 0.0
        
        entropy = 0.0
        for i in range(self.N):
            for j in range(self.N):
                p = rho[i][j] / total
                if p > 1e-8:
                    entropy -= p * math.log(p)
        return entropy
    
    def discover_physics(self, target_stability: float = 0.8):
        """Discover physical laws from recorded trajectories"""
        if len(self.trajectories) < 10:
            return {'status': 'Insufficient data'}
        
        # Analyze trajectory patterns
        recent_entropy = [t['entropy'] for t in self.trajectories[-20:]]
        entropy_trend = recent_entropy[-1] - recent_entropy[0]
        
        # Determine physics type
        if entropy_trend < -0.1:
            physics_type = "Dissipative - Energy decreasing"
            discovered_law = "∂E/∂t = -γE"
        elif entropy_trend > 0.1:
            physics_type = "Explosive - Energy increasing"
            discovered_law = "∂E/∂t = +αE"
        else:
            physics_type = "Conservative - Energy stable"
            discovered_law = "∂E/∂t = 0"
        
        # Update learner based on discovered physics
        if target_stability > 0.7:
            self.learner.update(recent_entropy, target_stability)
        
        return {
            'status': physics_type,
            'discovered_law': discovered_law,
            'entropy_trend': entropy_trend,
            'trajectories_analyzed': len(self.trajectories),
            'learning_active': True
        }
    
    def get_discovered_physics(self) -> Dict[str, Any]:
        """Get discovered physical laws"""
        return {
            'learned_weights': self.learner.get_weights(),
            'learning_history': self.learner.get_learning_curve(),
            'trajectory_count': len(self.trajectories)
        }


def create_neural_physics_learner(N: int = 100) -> NeuralPhysicsLearner:
    """Factory function for neural physics learner"""
    return NeuralPhysicsLearner(N=N)


def create_physics_discovery(N: int = 100) -> PhysicsDiscovery:
    """Factory function for physics discovery"""
    return PhysicsDiscovery(N=N)
