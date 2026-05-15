#!/usr/bin/env python3
"""Tests for Lyapunov Stability"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.stability.lyapunov import LyapunovStability, create_lyapunov_stability


class TestLyapunovStability(unittest.TestCase):
    """Test cases for Lyapunov Stability"""
    
    def setUp(self):
        self.lyap = LyapunovStability(n=10, lambda_reg=0.5)
        self.rho = [[0.5 for _ in range(10)] for __ in range(10)]
        self.target = [[0.0 for _ in range(10)] for __ in range(10)]
        self.target[3][3] = 1.0
        self.laplacian = [[0.1 for _ in range(10)] for __ in range(10)]
        self.grad_rho = [[0.2 for _ in range(10)] for __ in range(10)]
    
    def test_energy_functional(self):
        """Test energy functional computation"""
        energy = self.lyap.energy_functional(self.rho, self.target, self.laplacian)
        self.assertGreaterEqual(energy, 0)
    
    def test_lyapunov_function(self):
        """Test Lyapunov function"""
        V = self.lyap.lyapunov_function(self.rho, self.target, self.grad_rho)
        self.assertGreaterEqual(V, 0)
    
    def test_stability_metric(self):
        """Test stability metric"""
        metric = self.lyap.stability_metric(self.rho)
        self.assertGreaterEqual(metric, 0)
        self.assertLessEqual(metric, 1)
    
    def test_energy_decay_rate(self):
        """Test energy decay rate"""
        energy_history = [100, 80, 60, 40, 20]
        decay = self.lyap.energy_decay_rate(energy_history)
        self.assertGreaterEqual(decay, 0)
        self.assertLessEqual(decay, 1)
    
    def test_is_stable(self):
        """Test stability check"""
        self.assertTrue(self.lyap.is_stable(0.9))
        self.assertFalse(self.lyap.is_stable(0.5))
    
    def test_lyapunov_derivative(self):
        """Test Lyapunov derivative"""
        derivative = self.lyap.lyapunov_derivative(10, 12, 0.1)
        self.assertEqual(derivative, -20.0)
    
    def test_factory(self):
        """Test factory function"""
        lyap = create_lyapunov_stability(n=20)
        self.assertEqual(lyap.n, 20)


if __name__ == '__main__':
    unittest.main()
