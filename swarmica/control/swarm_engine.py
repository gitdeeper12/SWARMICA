"""SwarmEngine - main API class for SWARMICA framework"""

import math
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple


@dataclass
class SwarmConfig:
    """Configuration for SWARMICA swarm engine"""
    n_agents: int = 500
    modality: str = 'aerial'  # 'aerial' | 'ground' | 'underwater' | 'mixed'
    n_basis: int = 64
    k_coupling: float = 3.0
    mu_dissipation: float = 0.02
    target_config: str = 'diamond_V'
    sos_degree: int = 4
    dt: float = 0.001
    alpha: float = 0.15
    
    def __post_init__(self):
        self.k_critical = 2.0  # K_c = 2Δ
        if self.k_coupling < self.k_critical:
            self.k_coupling = 3.0 * self.k_critical  # enforce overcritical


class SwarmEngine:
    """Main SWARMICA engine - controls swarm collective dynamics"""
    
    def __init__(self, config: SwarmConfig):
        self.config = config
        self._step_count = 0
        self._csi_history = []
        self._entropy_history = []
        self._order_parameter_history = []
        self._q = [0.0] * config.n_basis  # generalized coordinates
        self._q_dot = [0.0] * config.n_basis  # generalized velocities
        self._q_star = None  # target attractor Q*
        self._init_target()
    
    def _init_target(self):
        """Initialize target configuration Q* based on formation type"""
        self._q_star = []
        for i in range(self.config.n_basis):
            # Simplified target: Gaussian-like distribution
            val = math.exp(-(i - self.config.n_basis/2) ** 2 / (2 * (self.config.n_basis/8) ** 2))
            self._q_star.append(val)
    
    def _compute_kinetic_coherence(self) -> float:
        """Compute collective kinetic energy T_coh"""
        t = 0.0
        for v in self._q_dot:
            t += 0.5 * v * v
        return t
    
    def _compute_potential_force(self) -> List[float]:
        """Compute -∇V_eff"""
        forces = []
        for i in range(self.config.n_basis):
            if i < len(self._q_star):
                diff = self._q[i] - self._q_star[i]
                force = -2.0 * self.config.alpha * diff
            else:
                force = -2.0 * self.config.alpha * self._q[i]
            forces.append(force)
        return forces
    
    def _compute_damping(self) -> List[float]:
        """Compute -μ Q̇"""
        return [-self.config.mu_dissipation * v for v in self._q_dot]
    
    def _update_dynamics(self, external_force: Optional[List[float]] = None):
        """Euler integration of collective dynamics"""
        # Compute forces
        pot_force = self._compute_potential_force()
        damp = self._compute_damping()
        
        # Total acceleration
        q_ddot = []
        for i in range(self.config.n_basis):
            f_total = pot_force[i] + damp[i]
            if external_force and i < len(external_force):
                f_total += external_force[i]
            q_ddot.append(f_total)
        
        # Euler integration
        for i in range(self.config.n_basis):
            self._q_dot[i] += q_ddot[i] * self.config.dt
            self._q[i] += self._q_dot[i] * self.config.dt
    
    def _compute_csi(self) -> float:
        """Collective Stability Index ∈ [0,1]"""
        # Based on distance to target Q*
        if not self._q_star:
            return 0.0
        
        distance = 0.0
        max_dist = 0.0
        for i in range(self.config.n_basis):
            diff = self._q[i] - self._q_star[i]
            distance += diff * diff
            max_dist += self._q_star[i] * self._q_star[i] if self._q_star[i] > 0 else 1.0
        
        if max_dist == 0:
            max_dist = 1.0
        
        csi = math.exp(-distance / max_dist)
        return max(0.0, min(1.0, csi))
    
    def _compute_structural_entropy(self) -> float:
        """S_struct = -Σ p_i log p_i (Shannon entropy)"""
        total = sum(abs(v) for v in self._q)
        if total == 0:
            return 0.0
        
        entropy = 0.0
        for v in self._q:
            p = abs(v) / total
            if p > 0:
                entropy -= p * math.log(p)
        
        # Normalize to [0, 1]
        max_entropy = math.log(self.config.n_basis)
        if max_entropy > 0:
            return entropy / max_entropy
        return 0.0
    
    def step(self, dt: float = None, obs: Dict = None) -> Dict[str, Any]:
        """Single control step"""
        if dt is not None:
            self.config.dt = dt
        
        # Update dynamics
        self._update_dynamics()
        
        # Compute metrics
        csi = self._compute_csi()
        entropy = self._compute_structural_entropy()
        t_coh = self._compute_kinetic_coherence()
        
        # Store history
        self._csi_history.append(csi)
        self._entropy_history.append(entropy)
        self._step_count += 1
        
        # Generate control commands
        control = {
            'forces': [-v for v in self._q_dot],  # simple proportional control
            'csi': csi,
            'entropy': entropy,
            'kinetic_coherence': t_coh,
            'step': self._step_count,
        }
        
        return control
    
    def get_csi(self) -> float:
        """Get current Collective Stability Index"""
        return self._compute_csi()
    
    def get_structural_entropy(self) -> float:
        """Get current structural entropy S_struct"""
        return self._compute_structural_entropy()
    
    def get_order_parameter(self) -> float:
        """Get Kuramoto order parameter r(t) (simplified)"""
        # Simplified: based on kinetic coherence
        t_coh = self._compute_kinetic_coherence()
        return min(1.0, t_coh / 10.0)
    
    def get_eri(self) -> float:
        """Entropy Reduction Index = 1 - S_final / S_initial"""
        if len(self._entropy_history) < 2:
            return 0.0
        s_initial = self._entropy_history[0] if self._entropy_history else 1.0
        s_final = self._entropy_history[-1] if self._entropy_history else 0.0
        if s_initial == 0:
            return 1.0
        return max(0.0, min(1.0, 1.0 - s_final / s_initial))
    
    def reset(self):
        """Reset engine state"""
        self._step_count = 0
        self._csi_history = []
        self._entropy_history = []
        self._order_parameter_history = []
        self._q = [0.0] * self.config.n_basis
        self._q_dot = [0.0] * self.config.n_basis
        self._init_target()


def create_engine(config: SwarmConfig = None) -> SwarmEngine:
    """Factory function to create SwarmEngine"""
    if config is None:
        config = SwarmConfig()
    return SwarmEngine(config)
