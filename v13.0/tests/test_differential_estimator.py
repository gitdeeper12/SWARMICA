#!/usr/bin/env python3
"""Tests for Differential Estimator"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.discovery.estimator import DifferentialEstimator, create_differential_estimator


class TestDifferentialEstimator(unittest.TestCase):
    """Test cases for Differential Estimator"""
    
    def setUp(self):
        self.estimator = DifferentialEstimator(N=10, dt=0.01)
        self.u = [[0.5 for _ in range(10)] for __ in range(10)]
        self.u_next = [[0.55 for _ in range(10)] for __ in range(10)]
    
    def test_initialization(self):
        """Test estimator initialization"""
        self.assertEqual(self.estimator.N, 10)
        self.assertEqual(self.estimator.dt, 0.01)
    
    def test_temporal_derivative(self):
        """Test temporal derivative computation"""
        du_dt = self.estimator.temporal_derivative(self.u, self.u_next)
        self.assertEqual(len(du_dt), 10)
    
    def test_gradient_x(self):
        """Test x-gradient"""
        grad = self.estimator.gradient_x(self.u)
        self.assertEqual(len(grad), 10)
    
    def test_gradient_y(self):
        """Test y-gradient"""
        grad = self.estimator.gradient_y(self.u)
        self.assertEqual(len(grad), 10)
    
    def test_simulate_dynamics(self):
        """Test dynamics simulation"""
        trajectory = self.estimator.simulate_dynamics(self.u, steps=5)
        self.assertEqual(len(trajectory), 5)
    
    def test_factory(self):
        """Test factory function"""
        estimator = create_differential_estimator(N=20)
        self.assertEqual(estimator.N, 20)


if __name__ == '__main__':
    unittest.main()
