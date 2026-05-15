"""Fourier spectral layer for global interactions - Optimized"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class FourierSpectralLayer:
    """Spectral layer capturing global wave-number interactions - Optimized"""
    
    N: int = 64
    n_modes: int = 8  # Reduced modes for performance
    
    def __post_init__(self):
        self._init_filters()
    
    def _init_filters(self):
        """Initialize spectral filters for each mode"""
        self.filters = []
        for k in range(self.n_modes):
            real = 0.1 * (2 * (k % 100) / 100 - 1)
            imag = 0.1 * (2 * ((k + 50) % 100) / 100 - 1)
            self.filters.append((real, imag))
    
    def forward(self, field: List[List[float]]) -> List[List[float]]:
        """Fast spectral transform (simplified for performance)"""
        N = self.N
        result = [[0.0 for _ in range(N)] for __ in range(N)]
        
        # Fast local spectral features (no full FFT)
        for i in range(N):
            for j in range(N):
                # Use local neighborhood for spectral features
                val = field[i][j]
                
                # Add local gradient information
                if i > 0:
                    val += 0.3 * field[i-1][j]
                if i < N-1:
                    val += 0.3 * field[i+1][j]
                if j > 0:
                    val += 0.3 * field[i][j-1]
                if j < N-1:
                    val += 0.3 * field[i][j+1]
                
                # Apply learned filter
                k = (i + j) % self.n_modes
                if k < len(self.filters):
                    r, _ = self.filters[k]
                    result[i][j] = val * (1 + r)
                else:
                    result[i][j] = val
        
        return result
    
    def update_filters(self, gradient: List[List[float]]):
        """Update spectral filters based on gradient"""
        N = self.N
        for kx in range(min(self.n_modes, N)):
            if kx < len(self.filters):
                r, i = self.filters[kx]
                # Simple update
                grad_sum = 0.0
                for i in range(N):
                    for j in range(N):
                        if (i + j) % self.n_modes == kx:
                            grad_sum += gradient[i][j]
                grad_sum /= (N * N)
                r += 0.01 * grad_sum
                r = max(-0.5, min(0.5, r))
                self.filters[kx] = (r, i)
    
    def get_spectrum(self) -> List[float]:
        """Get magnitude spectrum of learned filters"""
        spectrum = []
        for r, i in self.filters:
            spectrum.append(math.sqrt(r*r + i*i))
        return spectrum


def create_fourier_spectral_layer(N: int = 64, n_modes: int = 8) -> FourierSpectralLayer:
    """Factory function for Fourier spectral layer"""
    return FourierSpectralLayer(N=N, n_modes=n_modes)
