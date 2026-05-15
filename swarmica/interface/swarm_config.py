"""SwarmConfig dataclass for configuration"""

from dataclasses import dataclass


@dataclass
class SwarmConfig:
    """Configuration for SWARMICA swarm engine"""
    n_agents: int = 500
    modality: str = 'aerial'
    n_basis: int = 64
    k_coupling: float = 3.0
    mu_dissipation: float = 0.02
    target_config: str = 'diamond_V'
    sos_degree: int = 4
    dt: float = 0.001
    alpha: float = 0.15
    
    def __post_init__(self):
        self.k_critical = 2.0
        if self.k_coupling < self.k_critical:
            self.k_coupling = 3.0 * self.k_critical
