"""SWARMICA v2.0 - Stochastic Continuum Dynamics & Adaptive Field Control"""

__version__ = "2.0.0"
__status__ = "beta"

from swarmica.control.swarm_controller import SwarmControllerV2, create_controller_v2
from swarmica.coherence.metrics import CoherenceMetrics, create_coherence_metrics
from swarmica.bifurcation.detector import BifurcationDetector, create_bifurcation_detector
from swarmica.report_generator import ReportGenerator, create_report_generator

__all__ = [
    "SwarmControllerV2",
    "create_controller_v2",
    "CoherenceMetrics",
    "create_coherence_metrics",
    "BifurcationDetector",
    "create_bifurcation_detector",
    "ReportGenerator",
    "create_report_generator",
    "__version__"
]
