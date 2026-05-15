"""SWARMICA v11.0 - Neural Operator Swarm Physics"""

__version__ = "11.0.0"
__status__ = "frontier"

from swarmica.integrator.solver import NeuralOperatorSolver, create_neural_operator_solver
from swarmica.neural_operator.operator import NeuralOperator, create_neural_operator
from swarmica.spectral.fourier import FourierSpectralLayer, create_fourier_spectral_layer
from swarmica.metrics import MetricsCalculator, create_metrics_calculator
from swarmica.learning import OperatorLearner, PhysicsLawDiscovery, create_operator_learner, create_physics_law_discovery
from swarmica.reporting import NeuralOperatorReportGenerator, create_neural_operator_report_generator

__all__ = [
    "NeuralOperatorSolver",
    "create_neural_operator_solver",
    "NeuralOperator",
    "create_neural_operator",
    "FourierSpectralLayer",
    "create_fourier_spectral_layer",
    "MetricsCalculator",
    "create_metrics_calculator",
    "OperatorLearner",
    "PhysicsLawDiscovery",
    "create_operator_learner",
    "create_physics_law_discovery",
    "NeuralOperatorReportGenerator",
    "create_neural_operator_report_generator",
    "__version__"
]
