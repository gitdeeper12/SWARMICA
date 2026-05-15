"""Coherence metrics for SWARMICA v2.0"""

import math
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class CoherenceMetrics:
    """Real-time coherence and stability metrics"""
    
    @staticmethod
    def entropy(positions: List[Tuple[float, float]], grid_size: int, bins: int = 10) -> float:
        """Shannon entropy of spatial distribution"""
        hist = [0] * bins
        for x, _ in positions:
            bin_idx = int(x / grid_size * bins)
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
    
    @staticmethod
    def csi(positions: List[Tuple[float, float]]) -> float:
        """Collective Stability Index ∈ [0,1]"""
        if not positions:
            return 0.0
        
        n = len(positions)
        center_x = sum(p[0] for p in positions) / n
        center_y = sum(p[1] for p in positions) / n
        
        def distance(x1, y1, x2, y2):
            return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        
        distances = [distance(x, y, center_x, center_y) for x, y in positions]
        mean_dist = sum(distances) / n
        variance = sum((d - mean_dist) ** 2 for d in distances) / n
        
        return 1.0 / (1.0 + variance)
    
    @staticmethod
    def lyapunov(velocities: List[Tuple[float, float]]) -> float:
        """Lyapunov-like kinetic energy measure"""
        if not velocities:
            return 0.0
        total_speed = sum(math.sqrt(vx * vx + vy * vy) for vx, vy in velocities)
        return total_speed / len(velocities)
    
    @staticmethod
    def order_parameter(positions: List[Tuple[float, float]], center: Tuple[float, float]) -> float:
        """Kuramoto-like order parameter"""
        if not positions:
            return 0.0
        cx, cy = center
        distances = [math.sqrt((x - cx) ** 2 + (y - cy) ** 2) for x, y in positions]
        mean_dist = sum(distances) / len(distances)
        variance = sum((d - mean_dist) ** 2 for d in distances) / len(distances)
        return 1.0 / (1.0 + variance)


def create_coherence_metrics() -> CoherenceMetrics:
    """Factory function for coherence metrics"""
    return CoherenceMetrics()
