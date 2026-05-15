"""SWARMICA v13.0 - Autonomous Physical Law Discovery System"""

__version__ = "13.0.0"
__status__ = "research_frontier"

from swarmica.core.discovery_engine import DiscoveryEngine, create_discovery_engine
from swarmica.library.builder import PDELibrary, create_pde_library
from swarmica.sparse.selector import SparseSelector, create_sparse_selector
from swarmica.discovery.estimator import DifferentialEstimator, create_differential_estimator
from swarmica.verifier.constraints import ConstraintVerifier, create_constraint_verifier
from swarmica.reporting import DiscoveryReportGenerator, create_discovery_report_generator

__all__ = [
    "DiscoveryEngine",
    "create_discovery_engine",
    "PDELibrary",
    "create_pde_library",
    "SparseSelector",
    "create_sparse_selector",
    "DifferentialEstimator",
    "create_differential_estimator",
    "ConstraintVerifier",
    "create_constraint_verifier",
    "DiscoveryReportGenerator",
    "create_discovery_report_generator",
    "__version__"
]
