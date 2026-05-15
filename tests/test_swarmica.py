"""Basic tests for SWARMICA framework"""

import sys
sys.path.insert(0, '.')

def test_import():
    """Test importing main modules"""
    from swarmica import SwarmEngine, SwarmConfig
    from swarmica.control.csi_monitor import CSIMonitor
    from swarmica.field.epfe import EffectivePotentialFieldEngine
    from swarmica.synchronization.kpsl import KuramotoPhaseSynchronization
    from swarmica.stability.jacobian_analyzer import JacobianAnalyzer
    print("✅ All imports successful")


def test_swarm_engine():
    """Test SwarmEngine initialization and step"""
    from swarmica import SwarmEngine, SwarmConfig
    
    config = SwarmConfig(n_agents=100, modality='aerial')
    engine = SwarmEngine(config)
    
    control = engine.step()
    csi = engine.get_csi()
    entropy = engine.get_structural_entropy()
    
    print(f"✅ SwarmEngine: CSI={csi:.4f}, Entropy={entropy:.4f}")
    assert 0 <= csi <= 1, "CSI out of range"
    assert control is not None


def test_kpsl():
    """Test Kuramoto phase synchronization"""
    from swarmica.synchronization.kpsl import KuramotoPhaseSynchronization
    
    kpsl = KuramotoPhaseSynchronization(n_agents=100, k_coupling=3.0)
    r, phi = kpsl.compute_order_parameter()
    
    print(f"✅ KPSL: r={r:.4f}, K_c={kpsl.critical_coupling:.4f}")
    assert 0 <= r <= 1, "Order parameter out of range"


def test_epfe():
    """Test Effective Potential Field Engine"""
    from swarmica.field.epfe import EffectivePotentialFieldEngine
    
    epfe = EffectivePotentialFieldEngine(n_basis=32)
    q = [0.5] * 32
    v = epfe.compute_potential(q)
    
    print(f"✅ EPFE: V_eff={v:.4f}")
    assert v >= 0, "Potential should be non-negative"


def test_jacobian():
    """Test Jacobian stability analyzer"""
    from swarmica.stability.jacobian_analyzer import JacobianAnalyzer
    
    analyzer = JacobianAnalyzer(n_basis=32)
    hessian = [2.0] * 32
    metric_inv = [[1.0] * 32 for _ in range(32)]
    
    is_stable, result = analyzer.certificate(hessian, metric_inv, mu=0.02)
    
    print(f"✅ Jacobian: stable={is_stable}, sigma_min={result['sigma_min']:.4f}")


if __name__ == '__main__':
    print("=" * 50)
    print("Running SWARMICA tests")
    print("=" * 50)
    
    test_import()
    test_swarm_engine()
    test_kpsl()
    test_epfe()
    test_jacobian()
    
    print("=" * 50)
    print("✅ All tests passed!")
    print("=" * 50)
