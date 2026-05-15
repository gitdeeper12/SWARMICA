#!/usr/bin/env python3
"""Tests for Continuous Control Operators"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.continuous_control.operators import ContinuousControlOperators, create_continuous_operators


class TestContinuousControlOperators(unittest.TestCase):
    """Test cases for Continuous Control Operators"""
    
    def setUp(self):
        self.ops = ContinuousControlOperators(n=10, dx=1.0)
        self.field = [[0.0 for _ in range(10)] for __ in range(10)]
        self.field[5][5] = 1.0
    
    def test_initialization(self):
        """Test operator initialization"""
        self.assertEqual(self.ops.n, 10)
        self.assertEqual(self.ops.dx, 1.0)
    
    def test_laplacian(self):
        """Test Laplacian computation"""
        lap = self.ops.laplacian(self.field)
        self.assertEqual(len(lap), 10)
        self.assertEqual(len(lap[0]), 10)
    
    def test_gradient(self):
        """Test gradient computation"""
        gx, gy = self.ops.gradient(self.field)
        self.assertEqual(len(gx), 10)
        self.assertEqual(len(gy), 10)
    
    def test_gradient_magnitude(self):
        """Test gradient magnitude"""
        mag = self.ops.gradient_magnitude(self.field)
        self.assertEqual(len(mag), 10)
    
    def test_divergence(self):
        """Test divergence computation"""
        vx = [[1.0 for _ in range(10)] for __ in range(10)]
        vy = [[1.0 for _ in range(10)] for __ in range(10)]
        div = self.ops.divergence(vx, vy)
        self.assertEqual(len(div), 10)
    
    def test_constant_field_laplacian(self):
        """Test Laplacian of constant field is zero"""
        const = [[1.0 for _ in range(10)] for __ in range(10)]
        lap = self.ops.laplacian(const)
        for i in range(10):
            for j in range(10):
                self.assertAlmostEqual(lap[i][j], 0.0, places=5)
    
    def test_factory(self):
        """Test factory function"""
        ops = create_continuous_operators(n=20)
        self.assertEqual(ops.n, 20)


if __name__ == '__main__':
    unittest.main()
