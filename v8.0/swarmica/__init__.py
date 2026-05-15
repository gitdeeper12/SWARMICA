"""SWARMICA v8.0 - Unified Field Control Engine"""

__version__ = "8.0.0"
__status__ = "stable"

from swarmica.core.engine import SwarmicaV8, create_swarmica_v8
from swarmica.metrics.calculator import MetricsCalculator, create_metrics_calculator
from swarmica.reporting import SwarmReportGenerator, create_swarm_report_generator

__all__ = [
    "SwarmicaV8",
    "create_swarmica_v8",
    "MetricsCalculator",
    "create_metrics_calculator",
    "SwarmReportGenerator",
    "create_swarm_report_generator",
    "__version__"
]
