"""SWARMICA v5.0 - Variational Swarm Control System"""

__version__ = "5.0.0"
__status__ = "alpha"

from swarmica.control.variational_controller import VariationalController, create_variational_controller
from swarmica.variational.cost_functional import CostFunctional, create_cost_functional
from swarmica.variational.operators import VariationalOperators, create_variational_operators
from swarmica.reporting import VariationalReportGenerator, create_variational_report_generator

__all__ = [
    "VariationalController",
    "create_variational_controller",
    "CostFunctional",
    "create_cost_functional",
    "VariationalOperators",
    "create_variational_operators",
    "VariationalReportGenerator",
    "create_variational_report_generator",
    "__version__"
]
