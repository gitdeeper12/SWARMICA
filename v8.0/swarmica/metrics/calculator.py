"""Metrics calculator for SWARMICA v8.0"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class MetricsCalculator:
    """Calculate swarm metrics: CSI, Entropy, Lyapunov"""
    
    @staticmethod
    def distance(p1: List[float], p2: List[float]) -> float:
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return math.sqrt(dx * dx + dy * dy)
    
    @staticmethod
    def csi(positions: List[List[float]]) -> float:
        """Collective Stability Index ∈ [0,1]"""
        if not positions:
            return 0.0
        
        n = len(positions)
        # Centroid
        center_x = sum(p[0] for p in positions) / n
        center_y = sum(p[1] for p in positions) / n
        
        # Dispersion
        dispersion = 0.0
        for p in positions:
            dispersion += MetricsCalculator.distance(p, [center_x, center_y])
        dispersion /= n
        
        return 1.0 / (1.0 + dispersion)
    
    @staticmethod
    def entropy(positions: List[List[float]]) -> float:
        """Structural entropy"""
        if not positions:
            return 0.0
        
        n = len(positions)
        # Centroid
        center_x = sum(p[0] for p in positions) / n
        center_y = sum(p[1] for p in positions) / n
        
        # Distances to centroid
        distances = [MetricsCalculator.distance(p, [center_x, center_y]) for p in positions]
        
        total = sum(distances)
        if total < 1e-8:
            return 0.0
        
        entropy_val = 0.0
        for d in distances:
            p = d / total
            if p > 1e-8:
                entropy_val -= p * math.log(p)
        
        return entropy_val
    
    @staticmethod
    def lyapunov(velocities: List[List[float]]) -> float:
        """Lyapunov-like kinetic energy"""
        kinetic = 0.0
        for v in velocities:
            kinetic += 0.5 * (v[0] * v[0] + v[1] * v[1])
        return kinetic
    
    @staticmethod
    def kinetic_energy(velocities: List[List[float]]) -> float:
        """Total kinetic energy"""
        total = 0.0
        for v in velocities:
            total += v[0] * v[0] + v[1] * v[1]
        return 0.5 * total
    
    @staticmethod
    def potential_energy(positions: List[List[float]], attractors: List[List[float]]) -> float:
        """Potential energy from attractors"""
        total = 0.0
        for pos in positions:
            for att in attractors:
                total += MetricsCalculator.distance(pos, att)
        return total


def create_metrics_calculator() -> MetricsCalculator:
    """Factory function for metrics calculator"""
    return MetricsCalculator()
