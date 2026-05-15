"""SWARMICA: Variational and Continuum Mechanics Framework for Collective Stability"""

__version__ = "1.0.0"
__doi__ = "10.5281/zenodo.20168278"
__author__ = "Samir Baladi"
__email__ = "gitdeeper@gmail.com"

from swarmica.control.swarm_engine import SwarmEngine, SwarmConfig
from swarmica.control.csi_monitor import CSIMonitor
from swarmica.field.epfe import EffectivePotentialFieldEngine
from swarmica.synchronization.kpsl import KuramotoPhaseSynchronization
from swarmica.stability.jacobian_analyzer import JacobianAnalyzer

__all__ = [
    "SwarmEngine",
    "SwarmConfig", 
    "CSIMonitor",
    "EffectivePotentialFieldEngine",
    "KuramotoPhaseSynchronization",
    "JacobianAnalyzer",
    "__version__",
    "__doi__",
]
