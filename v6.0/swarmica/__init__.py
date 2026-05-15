"""SWARMICA v6.0 - Neural Optimal Swarm Physics Engine"""

__version__ = "6.0.0"
__status__ = "alpha"

from swarmica.control.optimal_swarm_controller import OptimalSwarmController, create_optimal_swarm_controller
from swarmica.neural_operator.operator import NeuralOperator, create_neural_operator
from swarmica.optimal_control.pontryagin import PontryaginController, create_pontryagin_controller
from swarmica.pde.operators import PDEOperators, create_pde_operators
from swarmica.reporting import OptimalControlReportGenerator, create_optimal_control_report_generator

__all__ = [
    "OptimalSwarmController",
    "create_optimal_swarm_controller",
    "NeuralOperator",
    "create_neural_operator",
    "PontryaginController",
    "create_pontryagin_controller",
    "PDEOperators",
    "create_pde_operators",
    "OptimalControlReportGenerator",
    "create_optimal_control_report_generator",
    "__version__"
]
