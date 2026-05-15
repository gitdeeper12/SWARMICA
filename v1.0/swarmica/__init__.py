"""SWARMICA v1.0.0 - Classical Variational Mechanics Framework"""

__version__ = "1.0.0"
__doi__ = "10.5281/zenodo.20168278"

from swarmica.control.swarm_engine import SwarmEngine
from swarmica.interface.swarm_config import SwarmConfig

__all__ = ["SwarmEngine", "SwarmConfig", "__version__", "__doi__"]
