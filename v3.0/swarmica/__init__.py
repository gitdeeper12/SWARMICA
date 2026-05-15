"""SWARMICA v3.0 - PDE Swarm Physics Engine & Neural Energy Fields"""

__version__ = "3.0.0"
__status__ = "alpha"

from swarmica.pde.solver import PDESolver, create_pde_solver
from swarmica.pde.operators import PDEOperators
from swarmica.energy.functional import EnergyFunctional

__all__ = [
    "PDESolver",
    "create_pde_solver",
    "PDEOperators",
    "EnergyFunctional",
    "__version__"
]
