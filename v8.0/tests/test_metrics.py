#!/usr/bin/env python3
"""Tests for Metrics Calculator"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.metrics.calculator import MetricsCalculator, create_metrics_calculator


class TestMetricsCalculator(unittest.TestCase):
    """Test cases for Metrics Calculator"""
    
    def setUp(self):
        self.calc = MetricsCalculator()
        self.positions = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
        self.velocities = [[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0], [0.0, -1.0]]
        self.attractors = [[2.0, 2.0], [-2.0, -2.0]]
    
    def test_distance(self):
        """Test distance calculation"""
        dist = self.calc.distance([0.0, 0.0], [3.0, 4.0])
        self.assertAlmostEqual(dist, 5.0, places=5)
    
    def test_csi(self):
        """Test CSI computation"""
        csi = self.calc.csi(self.positions)
        self.assertGreaterEqual(csi, 0)
        self.assertLessEqual(csi, 1)
    
    def test_csi_perfect_cluster(self):
        """Test CSI for perfectly clustered agents"""
        clustered = [[0.0, 0.0] for _ in range(10)]
        csi = self.calc.csi(clustered)
        self.assertAlmostEqual(csi, 1.0, places=5)
    
    def test_entropy(self):
        """Test entropy computation"""
        entropy = self.calc.entropy(self.positions)
        self.assertGreaterEqual(entropy, 0)
    
    def test_entropy_empty(self):
        """Test entropy for empty list"""
        entropy = self.calc.entropy([])
        self.assertEqual(entropy, 0.0)
    
    def test_lyapunov(self):
        """Test Lyapunov computation"""
        lyap = self.calc.lyapunov(self.velocities)
        self.assertGreaterEqual(lyap, 0)
    
    def test_kinetic_energy(self):
        """Test kinetic energy"""
        ke = self.calc.kinetic_energy(self.velocities)
        self.assertGreaterEqual(ke, 0)
    
    def test_potential_energy(self):
        """Test potential energy"""
        pe = self.calc.potential_energy(self.positions, self.attractors)
        self.assertGreaterEqual(pe, 0)
    
    def test_factory_function(self):
        """Test factory function"""
        calc = create_metrics_calculator()
        self.assertIsInstance(calc, MetricsCalculator)


if __name__ == '__main__':
    unittest.main()
