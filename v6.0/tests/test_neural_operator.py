#!/usr/bin/env python3
"""Tests for Neural Operator"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.neural_operator.operator import NeuralOperator, create_neural_operator


class TestNeuralOperator(unittest.TestCase):
    """Test cases for Neural Operator"""
    
    def setUp(self):
        self.op = NeuralOperator(n=10, learning_rate=0.002)
        self.rho = [[0.5 for _ in range(10)] for __ in range(10)]
        self.goal = [[0.0 for _ in range(10)] for __ in range(10)]
        self.goal[3][3] = 1.0
        self.adjoint = [[0.1 for _ in range(10)] for __ in range(10)]
    
    def test_initialization(self):
        """Test neural operator initialization"""
        self.assertEqual(self.op.n, 10)
        self.assertEqual(len(self.op.W), 10)
    
    def test_forward(self):
        """Test forward pass"""
        result = self.op.forward(self.rho)
        self.assertEqual(len(result), 10)
        self.assertEqual(len(result[0]), 10)
    
    def test_gradient_wrt_rho(self):
        """Test gradient computation"""
        grad = self.op.gradient_wrt_rho(self.rho)
        self.assertEqual(len(grad), 10)
    
    def test_update(self):
        """Test parameter update"""
        old_W = [row[:] for row in self.op.W]
        self.op.update(self.rho, self.goal, self.adjoint)
        # W should change
        changed = False
        for i in range(10):
            for j in range(10):
                if old_W[i][j] != self.op.W[i][j]:
                    changed = True
                    break
        self.assertTrue(changed)
    
    def test_parameter_clamping(self):
        """Test W parameters are clamped"""
        for i in range(10):
            for j in range(10):
                self.op.W[i][j] = 2.0
        self.op.update(self.rho, self.goal, self.adjoint)
        for i in range(10):
            for j in range(10):
                self.assertLessEqual(self.op.W[i][j], 1.0)
                self.assertGreaterEqual(self.op.W[i][j], -1.0)
    
    def test_reset(self):
        """Test reset"""
        self.op.update(self.rho, self.goal, self.adjoint)
        old_W = [row[:] for row in self.op.W]
        self.op.reset()
        different = False
        for i in range(10):
            for j in range(10):
                if old_W[i][j] != self.op.W[i][j]:
                    different = True
                    break
        self.assertTrue(different)
    
    def test_factory(self):
        """Test factory function"""
        op = create_neural_operator(n=20, lr=0.001)
        self.assertEqual(op.n, 20)
        self.assertEqual(op.learning_rate, 0.001)


if __name__ == '__main__':
    unittest.main()
