"""SWARMICA v12.0 - Constrained Neural Physics Discovery System"""

__version__ = "12.0.0"
__status__ = "breakthrough"

from swarmica.solver.constrained_solver import ConstrainedNeuralSolver, create_constrained_neural_solver
from swarmica.hamiltonian.network import HamiltonianNetwork, create_hamiltonian_network
from swarmica.conservation.laws import ConservationLaws, create_conservation_laws
from swarmica.constraints.symplectic import SymplecticOperator, create_symplectic_operator
from swarmica.reporting import ConstrainedPhysicsReportGenerator, create_constrained_physics_report_generator

__all__ = [
    "ConstrainedNeuralSolver",
    "create_constrained_neural_solver",
    "HamiltonianNetwork",
    "create_hamiltonian_network",
    "ConservationLaws",
    "create_conservation_laws",
    "SymplecticOperator",
    "create_symplectic_operator",
    "ConstrainedPhysicsReportGenerator",
    "create_constrained_physics_report_generator",
    "__version__"
]
