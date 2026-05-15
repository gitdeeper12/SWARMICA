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
        self.op = NeuralOperator(N=10)
        self.rho = [[0.5 for _ in range(10)] for __ in range(10)]
        self.vx = [[0.1 for _ in range(10)] for __ in range(10)]
        self.vy = [[0.1 for _ in range(10)] for __ in range(10)]
    
    def test_initialization(self):
        """Test operator initialization"""
        self.assertEqual(self.op.N, 10)
        self.assertEqual(len(self.op.W_real), 10)
        self.assertEqual(len(self.op.W_imag), 10)
    
    def test_forward(self):
        """Test forward pass"""
        drho, dvx, dvy = self.op.forward(self.rho, self.vx, self.vy)
        self.assertEqual(len(drho), 10)
        self.assertEqual(len(dvx), 10)
    
    def test_fft_like(self):
        """Test spectral transform"""
        transformed = self.op._fft_like(self.rho)
        self.assertEqual(len(transformed), 10)
    
    def test_compute_loss(self):
        """Test loss computation"""
        drho = [[0.1 for _ in range(10)] for __ in range(10)]
        dvx = [[0.1 for _ in range(10)] for __ in range(10)]
        loss = self.op.compute_loss(drho, drho, dvx, dvx)
        self.assertGreaterEqual(loss, 0)
    
    def test_update(self):
        """Test parameter update"""
        target_drho = [[0.2 for _ in range(10)] for __ in range(10)]
        target_dvx = [[0.2 for _ in range(10)] for __ in range(10)]
        target_dvy = [[0.2 for _ in range(10)] for __ in range(10)]
        
        loss = self.op.update(self.rho, self.vx, self.vy, target_drho, target_dvx, target_dvy)
        self.assertGreaterEqual(loss, 0)
    
    def test_reset(self):
        """Test reset"""
        self.op.update(self.rho, self.vx, self.vy, self.rho, self.vx, self.vy)
        self.op.reset()
        # After reset, operator should be different
        self.assertEqual(len(self.op.history['loss']), 0)
    
    def test_factory(self):
        """Test factory function"""
        op = create_neural_operator(N=20)
        self.assertEqual(op.N, 20)


if __name__ == '__main__':
    unittest.main()
