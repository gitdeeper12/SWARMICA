"""Continuum PDE Solver for SWARMICA v9.0 - Research Grade"""

import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field


@dataclass
class ContinuumPDESolver:
    """Research-grade PDE solver for continuum swarm dynamics"""
    
    N: int = 100          # Grid resolution
    dt: float = 0.01      # Time step
    dx: float = 1.0       # Spatial step
    
    # Parameters
    alpha: float = 1.0    # Gradient energy coefficient
    gamma: float = 0.3    # Damping coefficient
    nu: float = 0.2       # Viscosity
    
    def __post_init__(self):
        self._init_fields()
        self.history = {
            'entropy': [],
            'coherence': [],
            'energy': []
        }
    
    def _init_fields(self):
        """Initialize density and velocity fields"""
        # Density field ρ(x,y)
        self.rho = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        for i in range(self.N):
            for j in range(self.N):
                # Gaussian-like initial density
                x = i - self.N/2
                y = j - self.N/2
                self.rho[i][j] = 0.5 * math.exp(-(x*x + y*y) / (2 * (self.N/8)**2))
        
        # Velocity fields vx, vy
        self.vx = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        self.vy = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        
        # Target density field ρ*
        self.rho_star = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        self.rho_star[self.N//4][self.N//4] = 1.0
        self.rho_star[3*self.N//4][3*self.N//4] = 1.0
    
    def _laplacian(self, field: List[List[float]]) -> List[List[float]]:
        """Compute discrete Laplacian: ∇²f"""
        result = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        
        for i in range(self.N):
            for j in range(self.N):
                center = field[i][j]
                up = field[i-1][j] if i > 0 else field[i][j]
                down = field[i+1][j] if i < self.N-1 else field[i][j]
                left = field[i][j-1] if j > 0 else field[i][j]
                right = field[i][j+1] if j < self.N-1 else field[i][j]
                
                result[i][j] = up + down + left + right - 4 * center
        
        return result
    
    def _gradient_field(self, field: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
        """Compute gradient ∇f = (∂f/∂x, ∂f/∂y)"""
        gx = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        gy = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        
        for i in range(self.N):
            for j in range(self.N):
                # x-gradient
                right = field[i][j+1] if j < self.N-1 else field[i][j]
                left = field[i][j-1] if j > 0 else field[i][j]
                gx[i][j] = (right - left) / 2
                
                # y-gradient
                down = field[i+1][j] if i < self.N-1 else field[i][j]
                up = field[i-1][j] if i > 0 else field[i][j]
                gy[i][j] = (down - up) / 2
        
        return gx, gy
    
    def _energy_gradient(self) -> List[List[float]]:
        """Compute gradient of energy functional: ∇E = α∇ρ"""
        gx, gy = self._gradient_field(self.rho)
        grad = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        
        for i in range(self.N):
            for j in range(self.N):
                grad[i][j] = self.alpha * (gx[i][j] + gy[i][j])
        
        return grad
    
    def _energy_functional(self) -> float:
        """Energy functional E[ρ] = ∫|∇ρ|² dx"""
        gx, gy = self._gradient_field(self.rho)
        energy = 0.0
        
        for i in range(self.N):
            for j in range(self.N):
                energy += gx[i][j] * gx[i][j] + gy[i][j] * gy[i][j]
        
        return energy
    
    def _entropy(self) -> float:
        """Shannon entropy of density field"""
        total = 0.0
        for i in range(self.N):
            for j in range(self.N):
                total += self.rho[i][j]
        
        if total < 1e-8:
            return 0.0
        
        entropy_val = 0.0
        for i in range(self.N):
            for j in range(self.N):
                p = self.rho[i][j] / total
                if p > 1e-8:
                    entropy_val -= p * math.log(p)
        
        return entropy_val
    
    def _coherence(self) -> float:
        """Coherence index: 1/(1+var(ρ))"""
        # Compute mean
        mean = 0.0
        for i in range(self.N):
            for j in range(self.N):
                mean += self.rho[i][j]
        mean /= (self.N * self.N)
        
        # Compute variance
        variance = 0.0
        for i in range(self.N):
            for j in range(self.N):
                variance += (self.rho[i][j] - mean) ** 2
        variance /= (self.N * self.N)
        
        return 1.0 / (1.0 + variance)
    
    def _divergence(self, flux_x: List[List[float]], flux_y: List[List[float]]) -> List[List[float]]:
        """Compute divergence: ∇·F = ∂Fx/∂x + ∂Fy/∂y"""
        div = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        
        for i in range(self.N):
            for j in range(self.N):
                # ∂Fx/∂x
                fx_right = flux_x[i][j+1] if j < self.N-1 else flux_x[i][j]
                fx_left = flux_x[i][j-1] if j > 0 else flux_x[i][j]
                dfx_dx = fx_right - fx_left
                
                # ∂Fy/∂y
                fy_down = flux_y[i+1][j] if i < self.N-1 else flux_y[i][j]
                fy_up = flux_y[i-1][j] if i > 0 else flux_y[i][j]
                dfy_dy = fy_down - fy_up
                
                div[i][j] = dfx_dx + dfy_dy
        
        return div
    
    def step(self) -> Dict[str, Any]:
        """Execute one PDE step"""
        
        # 1. Compute forces from energy gradient
        dE = self._energy_gradient()
        
        # 2. Compute Laplacian of velocity
        lap_vx = self._laplacian(self.vx)
        lap_vy = self._laplacian(self.vy)
        
        # 3. Update velocity (momentum PDE)
        # ∂v/∂t = -∇E - γv + ν∇²v
        new_vx = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        new_vy = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        
        for i in range(self.N):
            for j in range(self.N):
                new_vx[i][j] = self.vx[i][j] + (-dE[i][j] - self.gamma * self.vx[i][j] + self.nu * lap_vx[i][j]) * self.dt
                new_vy[i][j] = self.vy[i][j] + (-dE[i][j] - self.gamma * self.vy[i][j] + self.nu * lap_vy[i][j]) * self.dt
        
        self.vx = new_vx
        self.vy = new_vy
        
        # 4. Compute flux: F = ρ·v
        flux_x = [[self.rho[i][j] * self.vx[i][j] for j in range(self.N)] for i in range(self.N)]
        flux_y = [[self.rho[i][j] * self.vy[i][j] for j in range(self.N)] for i in range(self.N)]
        
        # 5. Compute divergence of flux
        div_flux = self._divergence(flux_x, flux_y)
        
        # 6. Update density (continuity equation)
        # ∂ρ/∂t + ∇·(ρv) = 0
        new_rho = [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        for i in range(self.N):
            for j in range(self.N):
                new_rho[i][j] = self.rho[i][j] - div_flux[i][j] * self.dt
                new_rho[i][j] = max(0.0, min(1.0, new_rho[i][j]))
        
        self.rho = new_rho
        
        # 7. Compute metrics
        entropy_val = self._entropy()
        coherence_val = self._coherence()
        energy_val = self._energy_functional()
        
        self.history['entropy'].append(entropy_val)
        self.history['coherence'].append(coherence_val)
        self.history['energy'].append(energy_val)
        
        return {
            'rho': self.rho,
            'vx': self.vx,
            'vy': self.vy,
            'entropy': entropy_val,
            'coherence': coherence_val,
            'energy': energy_val,
            'step': len(self.history['entropy']) - 1
        }
    
    def run(self, steps: int = 300) -> Dict[str, List[float]]:
        """Run simulation for multiple steps"""
        for _ in range(steps):
            self.step()
        return self.history
    
    def reset(self):
        """Reset solver state"""
        self._init_fields()
        self.history = {'entropy': [], 'coherence': [], 'energy': []}
    
    def get_final_field(self) -> List[List[float]]:
        """Get final density field"""
        return self.rho


def create_continuum_pde_solver(N: int = 100) -> ContinuumPDESolver:
    """Factory function for continuum PDE solver"""
    return ContinuumPDESolver(N=N)
