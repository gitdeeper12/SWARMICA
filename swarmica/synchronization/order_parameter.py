"""Kuramoto order parameter tracking"""

import math
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class OrderParameter:
    """Tracks Kuramoto order parameter r(t) and mean phase φ(t)"""
    
    n_agents: int = 500
    history: List[Tuple[float, float]] = None
    
    def __post_init__(self):
        self.history = []
    
    @staticmethod
    def compute(phases: List[float]) -> Tuple[float, float]:
        """Compute r = |(1/N) Σ e^{iθ}|, φ = arg(Σ e^{iθ})"""
        sum_cos = 0.0
        sum_sin = 0.0
        n = len(phases)
        
        for theta in phases:
            sum_cos += math.cos(theta)
            sum_sin += math.sin(theta)
        
        r = math.sqrt(sum_cos * sum_cos + sum_sin * sum_sin) / n
        phi = math.atan2(sum_sin, sum_cos)
        return r, phi
    
    def update(self, phases: List[float]) -> Tuple[float, float]:
        """Update and store order parameter"""
        r, phi = self.compute(phases)
        self.history.append((r, phi))
        return r, phi
    
    @property
    def current_r(self) -> float:
        """Current order parameter value"""
        if not self.history:
            return 0.0
        return self.history[-1][0]
    
    @property
    def current_phi(self) -> float:
        """Current mean phase"""
        if not self.history:
            return 0.0
        return self.history[-1][1]
    
    @property
    def mean_r(self) -> float:
        """Mean order parameter over history"""
        if not self.history:
            return 0.0
        return sum(r for r, _ in self.history) / len(self.history)
    
    @property
    def synchronization_level(self) -> float:
        """Synchronization level ∈ [0, 1]"""
        return self.current_r
    
    def is_synchronized(self, threshold: float = 0.95) -> bool:
        """Check if swarm is synchronized above threshold"""
        return self.current_r >= threshold
    
    def reset(self):
        """Reset history"""
        self.history = []
