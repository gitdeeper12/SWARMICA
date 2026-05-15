"""SWARMICA v8.0 - Unified Field Control Engine Core"""

import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field


@dataclass
class SwarmicaV8:
    """Unified Field Control Engine - Agent-based continuum approximation"""
    
    n_agents: int = 100
    dim: int = 2
    dt: float = 0.01
    
    # Parameters
    alpha: float = 1.2   # Cohesion strength
    beta: float = 2.0    # Attractor strength
    gamma: float = 0.5   # Damping
    sigma: float = 0.1   # Noise
    
    def __post_init__(self):
        self._init_state()
        self._init_attractors()
        self.history = {
            'csi': [],
            'entropy': [],
            'lyapunov': [],
            'positions': []
        }
    
    def _init_state(self):
        """Initialize positions and velocities"""
        random.seed(42)
        self.positions = []
        self.velocities = []
        
        for _ in range(self.n_agents):
            x = random.gauss(0, 1)
            y = random.gauss(0, 1)
            self.positions.append([x, y])
            self.velocities.append([0.0, 0.0])
    
    def _init_attractors(self):
        """Initialize multi-attractor targets"""
        self.attractors = [
            [2.0, 2.0],
            [-2.0, -2.0]
        ]
    
    def _distance(self, p1: List[float], p2: List[float]) -> float:
        """Euclidean distance between two points"""
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return math.sqrt(dx * dx + dy * dy)
    
    def _normalize(self, vec: List[float]) -> List[float]:
        """Normalize a vector"""
        mag = math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])
        if mag < 1e-8:
            return [0.0, 0.0]
        return [vec[0] / mag, vec[1] / mag]
    
    def compute_field_force(self, pos: List[float]) -> List[float]:
        """Compute multi-attractor potential field force"""
        force = [0.0, 0.0]
        
        for g in self.attractors:
            diff = [g[0] - pos[0], g[1] - pos[1]]
            dist = self._distance(g, pos)
            if dist > 1e-8:
                # Force magnitude decays with distance
                mag = self.beta / (dist + 0.5)
                dir_vec = self._normalize(diff)
                force[0] += mag * dir_vec[0]
                force[1] += mag * dir_vec[1]
        
        return force
    
    def compute_cohesion(self, idx: int) -> List[float]:
        """Compute cohesion force toward center of mass"""
        # Compute center of mass
        center = [0.0, 0.0]
        for pos in self.positions:
            center[0] += pos[0]
            center[1] += pos[1]
        center[0] /= self.n_agents
        center[1] /= self.n_agents
        
        # Cohesion force
        diff = [center[0] - self.positions[idx][0], 
                center[1] - self.positions[idx][1]]
        return [self.alpha * diff[0], self.alpha * diff[1]]
    
    def lyapunov(self) -> float:
        """Lyapunov function: kinetic + potential energy"""
        # Kinetic energy
        kinetic = 0.0
        for v in self.velocities:
            kinetic += 0.5 * (v[0] * v[0] + v[1] * v[1])
        
        # Potential energy (distance to attractors)
        potential = 0.0
        for pos in self.positions:
            for g in self.attractors:
                potential += self._distance(pos, g)
        
        return kinetic + potential
    
    def entropy(self) -> float:
        """Structural entropy of swarm"""
        # Compute centroid
        center = [0.0, 0.0]
        for pos in self.positions:
            center[0] += pos[0]
            center[1] += pos[1]
        center[0] /= self.n_agents
        center[1] /= self.n_agents
        
        # Compute distances to centroid
        distances = []
        for pos in self.positions:
            d = self._distance(pos, center)
            distances.append(d)
        
        # Probability distribution
        total = sum(distances)
        if total < 1e-8:
            return 0.0
        
        entropy_val = 0.0
        for d in distances:
            p = d / total
            if p > 1e-8:
                entropy_val -= p * math.log(p)
        
        return entropy_val
    
    def csi(self) -> float:
        """Collective Stability Index"""
        # Compute centroid
        center = [0.0, 0.0]
        for pos in self.positions:
            center[0] += pos[0]
            center[1] += pos[1]
        center[0] /= self.n_agents
        center[1] /= self.n_agents
        
        # Compute dispersion
        dispersion = 0.0
        for pos in self.positions:
            dispersion += self._distance(pos, center)
        dispersion /= self.n_agents
        
        # CSI = 1/(1+dispersion) ∈ [0,1]
        return 1.0 / (1.0 + dispersion)
    
    def step(self) -> Dict[str, Any]:
        """Execute one simulation step"""
        noise = []
        for _ in range(self.n_agents):
            noise.append([self.sigma * random.gauss(0, 1), 
                          self.sigma * random.gauss(0, 1)])
        
        new_velocities = []
        new_positions = []
        
        for i in range(self.n_agents):
            # Compute forces
            field_force = self.compute_field_force(self.positions[i])
            cohesion = self.compute_cohesion(i)
            
            # Acceleration = forces - damping + noise
            acc_x = field_force[0] + cohesion[0] - self.gamma * self.velocities[i][0] + noise[i][0]
            acc_y = field_force[1] + cohesion[1] - self.gamma * self.velocities[i][1] + noise[i][1]
            
            # Update velocity and position
            new_vx = self.velocities[i][0] + acc_x * self.dt
            new_vy = self.velocities[i][1] + acc_y * self.dt
            new_px = self.positions[i][0] + new_vx * self.dt
            new_py = self.positions[i][1] + new_vy * self.dt
            
            new_velocities.append([new_vx, new_vy])
            new_positions.append([new_px, new_py])
        
        self.positions = new_positions
        self.velocities = new_velocities
        
        # Compute metrics
        csi_val = self.csi()
        entropy_val = self.entropy()
        lyapunov_val = self.lyapunov()
        
        self.history['csi'].append(csi_val)
        self.history['entropy'].append(entropy_val)
        self.history['lyapunov'].append(lyapunov_val)
        self.history['positions'].append([pos[:] for pos in self.positions])
        
        return {
            'positions': self.positions,
            'velocities': self.velocities,
            'csi': csi_val,
            'entropy': entropy_val,
            'lyapunov': lyapunov_val,
            'step': len(self.history['csi']) - 1
        }
    
    def run(self, steps: int = 1000) -> Dict[str, List]:
        """Run simulation for multiple steps"""
        for _ in range(steps):
            self.step()
        return self.history
    
    def reset(self):
        """Reset simulation state"""
        self._init_state()
        self.history = {
            'csi': [],
            'entropy': [],
            'lyapunov': [],
            'positions': []
        }
    
    def get_summary(self) -> Dict[str, float]:
        """Get simulation summary"""
        if not self.history['csi']:
            return {}
        
        return {
            'final_csi': self.history['csi'][-1],
            'initial_csi': self.history['csi'][0],
            'csi_improvement': (self.history['csi'][-1] - self.history['csi'][0]) * 100,
            'final_entropy': self.history['entropy'][-1],
            'initial_entropy': self.history['entropy'][0],
            'entropy_reduction': (self.history['entropy'][0] - self.history['entropy'][-1]) / (self.history['entropy'][0] + 1e-8) * 100,
            'final_lyapunov': self.history['lyapunov'][-1],
            'initial_lyapunov': self.history['lyapunov'][0]
        }


def create_swarmica_v8(n_agents: int = 100) -> SwarmicaV8:
    """Factory function for SWARMICA v8.0"""
    return SwarmicaV8(n_agents=n_agents)
