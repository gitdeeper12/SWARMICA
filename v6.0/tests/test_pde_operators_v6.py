#!/usr/bin/env python3
"""Tests for PDE Operators v6.0"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.pde.operators import PDEOperators, create_pde_operators


class TestPDEOperatorsV6(unittest.TestCase):
    """Test cases for PDE Operators v6.0"""
    
    def setUp(self):
        self.ops = PDEOperators(n=10, dx=1.0)
        self.field = [[0.0 for _ in range(10)] for __ in range(10)]
        self.field[5][5] = 1.0
    
    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.ops.n, 10)
        self.assertEqual(self.ops.dx, 1.0)
    
    def test_laplacian(self):
        """Test Laplacian"""
        lap = self.ops.laplacian(self.field)
        self.assertEqual(len(lap), 10)
    
    def test_gradient_field(self):
        """Test gradient field"""
        grad = self.ops.gradient_field(self.field)
        self.assertEqual(len(grad), 10)
    
    def test_divergence(self):
        """Test divergence"""
        vx = [[1.0 for _ in range(10)] for __ in range(10)]
        vy = [[1.0 for _ in range(10)] for __ in range(10)]
        div = self.ops.divergence(vx, vy)
        self.assertEqual(len(div), 10)
    
    def test_constant_field_laplacian(self):
        """Test Laplacian of constant field"""
        const = [[1.0 for _ in range(10)] for __ in range(10)]
        lap = self.ops.laplacian(const)
        for i in range(10):
            for j in range(10):
                self.assertAlmostEqual(lap[i][j], 0.0, places=5)
    
    def test_factory(self):
        """Test factory function"""
        ops = create_pde_operators(n=20)
        self.assertEqual(ops.n, 20)


if __name__ == '__main__':
    unittest.main()
