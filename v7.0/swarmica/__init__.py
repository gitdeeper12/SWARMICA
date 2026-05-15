"""SWARMICA v7.0 - Continuous Neural Control PDE System"""

__version__ = "7.0.0"
__status__ = "alpha"

from swarmica.control.continuous_controller import ContinuousController, create_continuous_controller
from swarmica.neural_operator.operator import NeuralOperator, create_neural_operator
from swarmica.continuous_control.operators import ContinuousControlOperators, create_continuous_operators
from swarmica.stability.lyapunov import LyapunovStability, create_lyapunov_stability
from swarmica.reporting import ContinuousControlReportGenerator, create_continuous_control_report_generator

__all__ = [
    "ContinuousController",
    "create_continuous_controller",
    "NeuralOperator",
    "create_neural_operator",
    "ContinuousControlOperators",
    "create_continuous_operators",
    "LyapunovStability",
    "create_lyapunov_stability",
    "ContinuousControlReportGenerator",
    "create_continuous_control_report_generator",
    "__version__"
]
