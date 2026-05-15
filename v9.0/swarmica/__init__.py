"""SWARMICA v9.0 - Continuum PDE + Energy Learning Swarm System"""

__version__ = "9.0.0"
__status__ = "research"

from swarmica.pde.solver import ContinuumPDESolver, create_continuum_pde_solver
from swarmica.reporting import PDEReportGenerator, create_pde_report_generator

__all__ = [
    "ContinuumPDESolver",
    "create_continuum_pde_solver",
    "PDEReportGenerator",
    "create_pde_report_generator",
    "__version__"
]
