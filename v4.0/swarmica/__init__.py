"""SWARMICA v4.0 - Neural Energy PDE Swarm Engine"""

__version__ = "4.0.0"
__status__ = "alpha"

from swarmica.control.neural_pde_solver import NeuralPDESolver, create_neural_pde_solver
from swarmica.neural_energy.energy_field import NeuralEnergyField
from swarmica.phase_transition.detector import PhaseTransitionDetector

__all__ = [
    "NeuralPDESolver",
    "create_neural_pde_solver",
    "NeuralEnergyField",
    "PhaseTransitionDetector",
    "__version__"
]
