#!/usr/bin/env python3
"""Tests for Neural Operator v7.0"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.neural_operator.operator import NeuralOperator, create_neural_operator


class TestNeuralOperatorV7(unittest.TestCase):
    """Test cases for Neural Operator v7.0"""
    
    def setUp(self):
        self.op = NeuralOperator(n=10, learning_rate=0.01)
        self.rho = [[0.5 for _ in range(10)] for __ in range(10)]
        self.target = [[0.0 for _ in range(10)] for __ in range(10)]
        self.target[3][3] = 1.0
        self.gradient = [[0.1 for _ in range(10)] for __ in range(10)]
    
    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.op.n, 10)
        self.assertEqual(len(self.op.Theta), 10)
    
    def test_forward(self):
        """Test forward pass"""
        result = self.op.forward(self.rho)
        self.assertEqual(len(result), 10)
    
    def test_forward_nonlinear(self):
        """Test nonlinear activation"""
        result = self.op.forward(self.rho)
        for i in range(10):
            for j in range(10):
                self.assertGreaterEqual(result[i][j], -1)
                self.assertLessEqual(result[i][j], 1)
    
    def test_update(self):
        """Test parameter update"""
        old_Theta = [row[:] for row in self.op.Theta]
        self.op.update(self.rho, self.target, self.gradient)
        changed = False
        for i in range(10):
            for j in range(10):
                if old_Theta[i][j] != self.op.Theta[i][j]:
                    changed = True
                    break
        self.assertTrue(changed)
    
    def test_parameter_clamping(self):
        """Test parameter clamping"""
        for i in range(10):
            for j in range(10):
                self.op.Theta[i][j] = 2.0
        self.op.update(self.rho, self.target, self.gradient)
        for i in range(10):
            for j in range(10):
                self.assertLessEqual(self.op.Theta[i][j], 0.5)
                self.assertGreaterEqual(self.op.Theta[i][j], -0.5)
    
    def test_reset(self):
        """Test reset"""
        self.op.update(self.rho, self.target, self.gradient)
        old_Theta = [row[:] for row in self.op.Theta]
        self.op.reset()
        different = False
        for i in range(10):
            for j in range(10):
                if old_Theta[i][j] != self.op.Theta[i][j]:
                    different = True
                    break
        self.assertTrue(different)
    
    def test_factory(self):
        """Test factory function"""
        op = create_neural_operator(n=20)
        self.assertEqual(op.n, 20)


if __name__ == '__main__':
    unittest.main()
