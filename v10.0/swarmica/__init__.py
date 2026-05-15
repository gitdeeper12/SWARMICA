"""SWARMICA v10.0 - Neural Field + Inverse Physics System"""

__version__ = "10.0.0"
__status__ = "breakthrough"

from swarmica.pde.neural_solver import NeuralPDESolver, create_neural_pde_solver
from swarmica.neural_physics.energy_model import NeuralEnergyModel, create_neural_energy_model
from swarmica.metrics import MetricsCalculator, create_metrics_calculator
from swarmica.learning import NeuralPhysicsLearner, PhysicsDiscovery, create_neural_physics_learner, create_physics_discovery
from swarmica.reporting import NeuralPhysicsReportGenerator, create_neural_physics_report_generator

__all__ = [
    "NeuralPDESolver",
    "create_neural_pde_solver",
    "NeuralEnergyModel",
    "create_neural_energy_model",
    "MetricsCalculator",
    "create_metrics_calculator",
    "NeuralPhysicsLearner",
    "PhysicsDiscovery",
    "create_neural_physics_learner",
    "create_physics_discovery",
    "NeuralPhysicsReportGenerator",
    "create_neural_physics_report_generator",
    "__version__"
]
