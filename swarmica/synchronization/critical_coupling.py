"""Critical coupling threshold K_c for Kuramoto phase transition"""

import math
from typing import Tuple


class CriticalCoupling:
    """Computes critical coupling threshold for phase synchronization"""
    
    def __init__(self, distribution_type: str = 'lorentzian'):
        self.distribution_type = distribution_type
    
    def lorentzian_kc(self, delta: float) -> float:
        """K_c = 2Δ for Lorentzian frequency distribution"""
        return 2.0 * delta
    
    def gaussian_kc(self, sigma: float) -> float:
        """K_c = 2/πσ for Gaussian distribution (approximation)"""
        return 2.0 / (math.pi * sigma)
    
    def uniform_kc(self, half_width: float) -> float:
        """K_c = 2/π * half_width for uniform distribution"""
        return 2.0 * half_width / math.pi
    
    def compute(self, width: float, distribution: str = 'lorentzian') -> float:
        """Compute critical coupling for given distribution"""
        if distribution == 'lorentzian':
            return self.lorentzian_kc(width)
        elif distribution == 'gaussian':
            return self.gaussian_kc(width)
        elif distribution == 'uniform':
            return self.uniform_kc(width)
        else:
            return 2.0 * width  # default
    
    def order_parameter_above_kc(self, k: float, k_c: float) -> float:
        """r_∞ = √(1 - K_c/K) for K > K_c"""
        if k <= k_c:
            return 0.0
        return math.sqrt(1.0 - k_c / k)
    
    def is_synchronized(self, k: float, k_c: float) -> bool:
        """Check if coupling exceeds critical threshold"""
        return k > k_c
    
    def get_safety_margin(self, k: float, k_c: float) -> float:
        """Safety margin = (K - K_c) / K_c"""
        if k_c == 0:
            return float('inf')
        return (k - k_c) / k_c


def get_critical_coupling(delta: float = 0.5, distribution: str = 'lorentzian') -> float:
    """Convenience function to get critical coupling"""
    cc = CriticalCoupling(distribution)
    return cc.compute(delta)
