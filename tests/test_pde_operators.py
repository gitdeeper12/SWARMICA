#!/usr/bin/env python3
"""Tests for PDE operators"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from swarmica.pde.operators import PDEOperators, create_pde_operators


class TestPDEOperators(unittest.TestCase):
    """Test cases for PDE operators"""
    
    def setUp(self):
        self.ops = PDEOperators(n=10, dx=1.0)
        self.field = [[0.0 for _ in range(10)] for __ in range(10)]
        self.field[5][5] = 1.0
    
    def test_laplacian(self):
        """Test Laplacian computation"""
        lap = self.ops.laplacian(self.field)
        self.assertEqual(len(lap), 10)
        self.assertEqual(len(lap[0]), 10)
    
    def test_gradient_x(self):
        """Test x-gradient computation"""
        grad = self.ops.gradient_x(self.field)
        self.assertEqual(len(grad), 10)
    
    def test_gradient_y(self):
        """Test y-gradient computation"""
        grad = self.ops.gradient_y(self.field)
        self.assertEqual(len(grad), 10)
    
    def test_divergence(self):
        """Test divergence computation"""
        vx = [[1.0 for _ in range(10)] for __ in range(10)]
        vy = [[1.0 for _ in range(10)] for __ in range(10)]
        div = self.ops.divergence(vx, vy)
        self.assertEqual(len(div), 10)
    
    def test_constant_field_laplacian(self):
        """Test Laplacian of constant field should be zero"""
        const_field = [[1.0 for _ in range(10)] for __ in range(10)]
        lap = self.ops.laplacian(const_field)
        for i in range(10):
            for j in range(10):
                self.assertAlmostEqual(lap[i][j], 0.0, places=5)
    
    def test_factory_function(self):
        """Test factory function"""
        ops = create_pde_operators(n=20, dx=0.5)
        self.assertEqual(ops.n, 20)
        self.assertEqual(ops.dx, 0.5)


if __name__ == '__main__':
    unittest.main()
