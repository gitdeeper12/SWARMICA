"""Autonomous Physical Law Discovery Engine for SWARMICA v13.0"""

import math
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field

from ..library.builder import PDELibrary, create_pde_library
from ..sparse.selector import SparseSelector, create_sparse_selector
from ..discovery.estimator import DifferentialEstimator, create_differential_estimator
from ..verifier.constraints import ConstraintVerifier, create_constraint_verifier


@dataclass
class DiscoveryEngine:
    """Autonomous physical law discovery from field observations"""
    
    N: int = 64
    dt: float = 0.01
    alpha: float = 0.001  # Sparsity parameter
    
    def __post_init__(self):
        self.library = PDELibrary(self.N)
        self.selector = SparseSelector(self.alpha)
        self.estimator = DifferentialEstimator(self.N, self.dt)
        self.verifier = ConstraintVerifier(self.N)
        self._init_field()
        self.discovery_history = []
    
    def _init_field(self):
        """Initialize field for observation"""
        N = self.N
        self.u = [[0.0 for _ in range(N)] for __ in range(N)]
        center = N // 2
        for i in range(N):
            for j in range(N):
                dx = i - center
                dy = j - center
                self.u[i][j] = 0.3 * math.exp(-(dx*dx + dy*dy) / (2 * (N/8)**2)) + 0.05 * random.random()
    
    def observe(self, steps: int = 10) -> Tuple[List[List[float]], List[List[float]]]:
        """Generate observed field and temporal derivative"""
        # Simulate simple dynamics
        trajectory = self.estimator.simulate_dynamics(self.u, steps)
        
        if len(trajectory) < 2:
            return self.u, [[0.0 for _ in range(self.N)] for __ in range(self.N)]
        
        u_curr = trajectory[0]
        u_next = trajectory[1] if len(trajectory) > 1 else trajectory[0]
        
        du_dt = self.estimator.temporal_derivative(u_curr, u_next)
        
        return u_curr, du_dt
    
    def discover_physics(self) -> Dict[str, Any]:
        """Discover physical law from observed field"""
        # Observe field dynamics
        u, du_dt = self.observe()
        
        # Build feature library
        Theta = self.library.build_features(u)
        term_names = self.library.term_names()
        
        # Flatten du_dt
        y = [du_dt[i][j] for i in range(self.N) for j in range(self.N)]
        
        # Discover PDE using sparse regression
        discovery = self.selector.discover_pde(Theta, y, term_names)
        
        # Verify discovered physics
        verification = self.verifier.verify_pde(discovery['pde_equation'], discovery['coefficients'])
        
        result = {
            'discovered_pde': discovery['pde_equation'],
            'coefficients': discovery['coefficients'],
            'num_terms': discovery['num_terms'],
            'sparsity': discovery['sparsity'],
            'verification': verification,
            'term_names': term_names
        }
        
        self.discovery_history.append(result)
        return result
    
    def run_discovery(self, iterations: int = 5) -> List[Dict[str, Any]]:
        """Run multiple discovery iterations"""
        results = []
        for i in range(iterations):
            print(f"  Discovery iteration {i+1}/{iterations}")
            result = self.discover_physics()
            results.append(result)
        return results
    
    def get_best_pde(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get the best discovered PDE (simplest with highest sparsity)"""
        if not results:
            return {}
        
        # Prefer simpler PDEs (higher sparsity)
        best = min(results, key=lambda x: x['num_terms'])
        return best


def create_discovery_engine(N: int = 64) -> DiscoveryEngine:
    """Factory function for discovery engine"""
    return DiscoveryEngine(N=N)
