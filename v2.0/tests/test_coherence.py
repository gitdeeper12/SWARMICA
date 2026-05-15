#!/usr/bin/env python3
"""Tests for coherence metrics"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from swarmica.coherence.metrics import CoherenceMetrics, create_coherence_metrics


class TestCoherenceMetrics(unittest.TestCase):
    """Test cases for CoherenceMetrics"""
    
    def setUp(self):
        self.metrics = CoherenceMetrics()
        self.positions = [(10, 10), (20, 20), (30, 30), (40, 40), (25, 25)]
        self.velocities = [(1, 0), (0, 1), (-1, 0), (0, -1), (0.5, 0.5)]
    
    def test_entropy(self):
        """Test entropy computation"""
        entropy = self.metrics.entropy(self.positions, grid_size=50)
        self.assertGreaterEqual(entropy, 0)
    
    def test_csi(self):
        """Test CSI computation"""
        csi = self.metrics.csi(self.positions)
        self.assertGreaterEqual(csi, 0)
        self.assertLessEqual(csi, 1)
    
    def test_lyapunov(self):
        """Test Lyapunov computation"""
        lyap = self.metrics.lyapunov(self.velocities)
        self.assertGreaterEqual(lyap, 0)
    
    def test_order_parameter(self):
        """Test order parameter computation"""
        op = self.metrics.order_parameter(self.positions, center=(25, 25))
        self.assertGreaterEqual(op, 0)
        self.assertLessEqual(op, 1)
    
    def test_empty_positions(self):
        """Test edge case: empty positions list"""
        entropy = self.metrics.entropy([], grid_size=50)
        self.assertEqual(entropy, 0.0)
        
        csi = self.metrics.csi([])
        self.assertEqual(csi, 0.0)
    
    def test_empty_velocities(self):
        """Test edge case: empty velocities list"""
        lyap = self.metrics.lyapunov([])
        self.assertEqual(lyap, 0.0)
    
    def test_create_factory(self):
        """Test factory function"""
        metrics = create_coherence_metrics()
        self.assertIsInstance(metrics, CoherenceMetrics)
    
    def test_csi_perfect_stability(self):
        """Test CSI for perfectly clustered agents"""
        perfect_positions = [(25, 25) for _ in range(10)]
        csi = self.metrics.csi(perfect_positions)
        self.assertAlmostEqual(csi, 1.0, places=5)
    
    def test_entropy_maximum(self):
        """Test entropy for uniform distribution"""
        uniform_positions = [(i*5, i*5) for i in range(10)]
        entropy = self.metrics.entropy(uniform_positions, grid_size=50, bins=10)
        self.assertGreaterEqual(entropy, 0)


if __name__ == '__main__':
    unittest.main()
