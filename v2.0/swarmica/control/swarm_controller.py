"""Main swarm controller for SWARMICA v2.0 - Pure Python (No NumPy)"""

import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field


@dataclass
class SwarmControllerV2:
    """Main controller for SWARMICA v2.0 - Vector Field Swarm Physics"""
    
    n_agents: int = 80
    grid_size: int = 50
    alpha: float = 0.8      # Cohesion strength
    beta: float = 1.2       # Attractor strength
    noise: float = 0.2      # Stochastic noise
    inertia: float = 0.85   # Velocity inertia
    dt: float = 0.1         # Time step
    
    def __post_init__(self):
        self._init_state()
        self.history = {
            'entropy': [],
            'csi': [],
            'lyapunov': []
        }
    
    def _init_state(self):
        """Initialize positions and velocities"""
        random.seed(42)
        self.positions = []
        self.velocities = []
        
        for _ in range(self.n_agents):
            x = random.uniform(0, self.grid_size)
            y = random.uniform(0, self.grid_size)
            self.positions.append((x, y))
            self.velocities.append((0.0, 0.0))
        
        # Multi-attractors
        self.A1 = (15, 15)
        self.A2 = (35, 35)
    
    def _distance(self, x1, y1, x2, y2) -> float:
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    
    def _compute_entropy(self) -> float:
        """Shannon entropy of spatial distribution"""
        bins = 10
        hist = [0] * bins
        
        for x, _ in self.positions:
            bin_idx = int(x / self.grid_size * bins)
            bin_idx = min(bin_idx, bins - 1)
            hist[bin_idx] += 1
        
        total = sum(hist)
        if total == 0:
            return 0.0
        
        entropy = 0.0
        for count in hist:
            if count > 0:
                prob = count / total
                entropy -= prob * math.log(prob)
        return entropy
    
    def _compute_csi(self) -> float:
        """Collective Stability Index ∈ [0,1]"""
        n = self.n_agents
        center_x = sum(p[0] for p in self.positions) / n
        center_y = sum(p[1] for p in self.positions) / n
        
        distances = [self._distance(x, y, center_x, center_y) for x, y in self.positions]
        mean_dist = sum(distances) / n
        variance = sum((d - mean_dist) ** 2 for d in distances) / n
        
        return 1.0 / (1.0 + variance)
    
    def _compute_lyapunov(self) -> float:
        """Lyapunov-like kinetic energy measure"""
        total_speed = 0.0
        for vx, vy in self.velocities:
            total_speed += math.sqrt(vx * vx + vy * vy)
        return total_speed / self.n_agents
    
    def step(self) -> Dict[str, Any]:
        """Execute one simulation step"""
        # Compute center of mass
        center_x = sum(p[0] for p in self.positions) / self.n_agents
        center_y = sum(p[1] for p in self.positions) / self.n_agents
        
        new_positions = []
        new_velocities = []
        
        for i, (px, py) in enumerate(self.positions):
            vx, vy = self.velocities[i]
            
            # Cohesion force
            cohesion_x = center_x - px
            cohesion_y = center_y - py
            
            # Attractor A1
            dx1 = self.A1[0] - px
            dy1 = self.A1[1] - py
            norm1 = math.sqrt(dx1 * dx1 + dy1 * dy1)
            if norm1 > 1e-8:
                a1_x = dx1 / norm1
                a1_y = dy1 / norm1
            else:
                a1_x = a1_y = 0.0
            
            # Attractor A2
            dx2 = self.A2[0] - px
            dy2 = self.A2[1] - py
            norm2 = math.sqrt(dx2 * dx2 + dy2 * dy2)
            if norm2 > 1e-8:
                a2_x = dx2 / norm2
                a2_y = dy2 / norm2
            else:
                a2_x = a2_y = 0.0
            
            # Total force
            force_x = self.alpha * cohesion_x + self.beta * (a1_x + a2_x)
            force_y = self.alpha * cohesion_y + self.beta * (a1_y + a2_y)
            
            # Stochastic noise
            noise_x = self.noise * random.gauss(0, 1)
            noise_y = self.noise * random.gauss(0, 1)
            
            # Update velocity and position
            new_vx = self.inertia * vx + force_x + noise_x
            new_vy = self.inertia * vy + force_y + noise_y
            new_px = px + self.dt * new_vx
            new_py = py + self.dt * new_vy
            
            # Boundary reflection
            if new_px < 0:
                new_px = -new_px
                new_vx = -new_vx
            if new_px > self.grid_size:
                new_px = 2 * self.grid_size - new_px
                new_vx = -new_vx
            if new_py < 0:
                new_py = -new_py
                new_vy = -new_vy
            if new_py > self.grid_size:
                new_py = 2 * self.grid_size - new_py
                new_vy = -new_vy
            
            new_positions.append((new_px, new_py))
            new_velocities.append((new_vx, new_vy))
        
        self.positions = new_positions
        self.velocities = new_velocities
        
        # Compute metrics
        entropy = self._compute_entropy()
        csi = self._compute_csi()
        lyapunov = self._compute_lyapunov()
        
        self.history['entropy'].append(entropy)
        self.history['csi'].append(csi)
        self.history['lyapunov'].append(lyapunov)
        
        return {
            'positions': self.positions,
            'velocities': self.velocities,
            'entropy': entropy,
            'csi': csi,
            'lyapunov': lyapunov,
            'step': len(self.history['csi']) - 1
        }
    
    def run(self, steps: int) -> Dict[str, List[float]]:
        """Run simulation for multiple steps"""
        for _ in range(steps):
            self.step()
        return self.history
    
    def reset(self):
        """Reset simulation state"""
        self._init_state()
        self.history = {'entropy': [], 'csi': [], 'lyapunov': []}
    
    def get_summary(self) -> Dict[str, float]:
        """Get simulation summary"""
        return {
            'final_csi': self.history['csi'][-1] if self.history['csi'] else 0,
            'final_entropy': self.history['entropy'][-1] if self.history['entropy'] else 0,
            'final_lyapunov': self.history['lyapunov'][-1] if self.history['lyapunov'] else 0,
            'csi_improvement': ((self.history['csi'][-1] - self.history['csi'][0]) * 100) if len(self.history['csi']) > 1 else 0
        }


def create_controller_v2(n_agents: int = 80) -> SwarmControllerV2:
    """Factory function for SWARMICA v2.0 controller"""
    return SwarmControllerV2(n_agents=n_agents)
