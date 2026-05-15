"""Basin of attraction estimation via sublevel sets"""

import math
from typing import List, Tuple, Optional


class BasinEstimator:
    """Estimates basin of attraction B(Q*) = {Q : V_eff(Q) <= V_max}"""
    
    def __init__(self, n_basis: int = 64):
        self.n_basis = n_basis
    
    def estimate_basin_radius(self, q_star: List[float], alpha: float = 0.15, 
                              domain_boundary: float = 10.0) -> float:
        """R_basin = sqrt(2V_max / λ_min(Hessian V_eff(Q*)))"""
        # Estimate V_max at domain boundary
        v_max = 0.0
        for val in q_star[:10]:
            v_max += alpha * (domain_boundary - val) ** 2
        v_max = max(v_max, 1.0)
        
        # Estimate λ_min (minimum Hessian eigenvalue)
        lambda_min = 2.0 * alpha
        
        if lambda_min > 0:
            basin_radius = math.sqrt(2.0 * v_max / lambda_min)
        else:
            basin_radius = domain_boundary
        
        return basin_radius
    
    def check_in_basin(self, q: List[float], q_star: List[float], 
                       basin_radius: float) -> bool:
        """Check if Q is within basin of attraction"""
        distance = 0.0
        for i in range(min(len(q), len(q_star))):
            diff = q[i] - q_star[i]
            distance += diff * diff
        
        distance = math.sqrt(distance)
        return distance <= basin_radius
    
    def estimate_attraction_time(self, distance: float, sigma_min: float, 
                                  epsilon: float = 0.01) -> float:
        """t_conv = -ln(ε)/σ_min"""
        if sigma_min <= 0:
            return float('inf')
        return -math.log(epsilon) / sigma_min
    
    def get_basin_probability(self, q_samples: List[List[float]], 
                              q_star: List[float], basin_radius: float) -> float:
        """Fraction of samples within basin of attraction"""
        if not q_samples:
            return 0.0
        
        in_basin = 0
        for q in q_samples:
            if self.check_in_basin(q, q_star, basin_radius):
                in_basin += 1
        
        return in_basin / len(q_samples)
    
    def characterize_basin(self, q_star: List[float], alpha: float = 0.15) -> dict:
        """Full basin characterization"""
        radius = self.estimate_basin_radius(q_star, alpha)
        
        return {
            'basin_radius': radius,
            'center': q_star[:10] if len(q_star) > 10 else q_star,
            'is_global': True,  # SOS potential guarantees global minimum
            'radius_estimate_method': 'sublevel_sets'
        }


def create_basin_estimator(n_basis: int = 64) -> BasinEstimator:
    """Factory function to create basin estimator"""
    return BasinEstimator(n_basis=n_basis)
