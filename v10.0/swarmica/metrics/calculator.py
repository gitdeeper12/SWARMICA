"""Advanced metrics calculator for SWARMICA v10.0"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class MetricsCalculator:
    """Compute advanced metrics for neural field dynamics"""
    
    N: int = 100
    
    def shannon_entropy(self, rho: List[List[float]]) -> float:
        """Shannon entropy: H = -Σ p log(p)"""
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
    
    def coherence_index(self, rho: List[List[float]]) -> float:
        """Coherence index: C = 1/(1+var(ρ))"""
        # Mean
        mean = 0.0
        for i in range(self.N):
            for j in range(self.N):
                mean += rho[i][j]
        mean /= (self.N * self.N)
        
        # Variance
        variance = 0.0
        for i in range(self.N):
            for j in range(self.N):
                variance += (rho[i][j] - mean) ** 2
        variance /= (self.N * self.N)
        
        return 1.0 / (1.0 + variance)
    
    def energy_density(self, rho: List[List[float]], 
                       grad: List[List[float]]) -> float:
        """Energy density: e = ∫|∇ρ|² dx"""
        energy = 0.0
        for i in range(self.N):
            for j in range(self.N):
                energy += grad[i][j] * grad[i][j]
        return energy / (self.N * self.N)
    
    def total_variation(self, rho: List[List[float]]) -> float:
        """Total variation: TV = ∫|∇ρ| dx"""
        tv = 0.0
        for i in range(self.N):
            for j in range(self.N):
                # x-difference
                if j < self.N - 1:
                    tv += abs(rho[i][j+1] - rho[i][j])
                # y-difference
                if i < self.N - 1:
                    tv += abs(rho[i+1][j] - rho[i][j])
        return tv
    
    def peak_signal_to_noise(self, rho: List[List[float]], 
                              target: List[List[float]]) -> float:
        """PSNR between current and target density"""
        mse = 0.0
        for i in range(self.N):
            for j in range(self.N):
                diff = rho[i][j] - target[i][j]
                mse += diff * diff
        mse /= (self.N * self.N)
        
        if mse < 1e-8:
            return float('inf')
        
        max_val = 1.0
        return 10 * math.log10(max_val * max_val / mse)
    
    def structural_similarity(self, rho1: List[List[float]], 
                               rho2: List[List[float]]) -> float:
        """Simplified SSIM between two density fields"""
        # Means
        mu1 = 0.0
        mu2 = 0.0
        for i in range(self.N):
            for j in range(self.N):
                mu1 += rho1[i][j]
                mu2 += rho2[i][j]
        mu1 /= (self.N * self.N)
        mu2 /= (self.N * self.N)
        
        # Variances and covariance
        var1 = 0.0
        var2 = 0.0
        cov = 0.0
        for i in range(self.N):
            for j in range(self.N):
                d1 = rho1[i][j] - mu1
                d2 = rho2[i][j] - mu2
                var1 += d1 * d1
                var2 += d2 * d2
                cov += d1 * d2
        
        var1 /= (self.N * self.N)
        var2 /= (self.N * self.N)
        cov /= (self.N * self.N)
        
        # SSIM components
        c1 = 0.01 ** 2
        c2 = 0.03 ** 2
        
        l = (2 * mu1 * mu2 + c1) / (mu1 * mu1 + mu2 * mu2 + c1)
        c = (2 * math.sqrt(var1 * var2) + c2) / (var1 + var2 + c2)
        s = (cov + c2/2) / (math.sqrt(var1 * var2) + c2/2)
        
        return l * c * s
    
    def kinetic_energy(self, vx: List[List[float]], vy: List[List[float]]) -> float:
        """Kinetic energy: K = ½∫|v|² dx"""
        ke = 0.0
        for i in range(self.N):
            for j in range(self.N):
                ke += 0.5 * (vx[i][j] * vx[i][j] + vy[i][j] * vy[i][j])
        return ke / (self.N * self.N)
    
    def potential_energy(self, rho: List[List[float]], 
                         theta: List[List[float]]) -> float:
        """Learned potential energy: U = ∫θ·ρ² dx"""
        pe = 0.0
        for i in range(self.N):
            for j in range(self.N):
                pe += theta[i][j] * rho[i][j] * rho[i][j]
        return pe / (self.N * self.N)
    
    def total_energy(self, rho: List[List[float]], 
                      vx: List[List[float]], vy: List[List[float]],
                      theta: List[List[float]]) -> float:
        """Total energy: E = K + U"""
        ke = self.kinetic_energy(vx, vy)
        pe = self.potential_energy(rho, theta)
        return ke + pe
    
    def get_all_metrics(self, rho: List[List[float]], 
                        vx: List[List[float]], vy: List[List[float]],
                        theta: List[List[float]],
                        target: List[List[float]] = None) -> Dict[str, float]:
        """Compute all metrics at once"""
        metrics = {
            'entropy': self.shannon_entropy(rho),
            'coherence': self.coherence_index(rho),
            'kinetic_energy': self.kinetic_energy(vx, vy),
            'potential_energy': self.potential_energy(rho, theta),
            'total_energy': self.total_energy(rho, vx, vy, theta),
            'total_variation': self.total_variation(rho)
        }
        
        if target is not None:
            metrics['psnr'] = self.peak_signal_to_noise(rho, target)
            metrics['ssim'] = self.structural_similarity(rho, target)
        
        return metrics


def create_metrics_calculator(N: int = 100) -> MetricsCalculator:
    """Factory function for metrics calculator"""
    return MetricsCalculator(N=N)
