#!/usr/bin/env python3
"""Tests for Neural Energy Field"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from swarmica.neural_energy.energy_field import NeuralEnergyField, create_neural_energy_field


class TestNeuralEnergyField(unittest.TestCase):
    """Test cases for Neural Energy Field"""
    
    def setUp(self):
        self.nef = NeuralEnergyField(n=10, learning_rate=0.001)
        self.rho = [[0.5 for _ in range(10)] for __ in range(10)]
        self.goal = [[0.0 for _ in range(10)] for __ in range(10)]
        self.goal[3][3] = 1.0
    
    def test_initialization(self):
        """Test neural energy field initialization"""
        self.assertEqual(self.nef.n, 10)
        self.assertEqual(len(self.nef.W), 10)
        self.assertEqual(len(self.nef.W[0]), 10)
    
    def test_energy_computation(self):
        """Test energy computation"""
        energy = self.nef.energy(self.rho, self.goal)
        self.assertGreater(energy, 0)
    
    def test_gradient_computation(self):
        """Test gradient computation"""
        grad = self.nef.compute_gradient(self.rho, self.goal)
        self.assertEqual(len(grad), 10)
        self.assertEqual(len(grad[0]), 10)
    
    def test_update_weights(self):
        """Test online learning update"""
        old_W = [row[:] for row in self.nef.W]
        self.nef.update(self.rho, self.goal)
        # W should change after update
        changed = False
        for i in range(10):
            for j in range(10):
                if old_W[i][j] != self.nef.W[i][j]:
                    changed = True
                    break
        self.assertTrue(changed)
    
    def test_parameter_clamping(self):
        """Test W parameters are clamped to [-1, 1]"""
        # Force large update
        for i in range(10):
            for j in range(10):
                self.nef.W[i][j] = 2.0
        self.nef.update(self.rho, self.goal)
        for i in range(10):
            for j in range(10):
                self.assertLessEqual(self.nef.W[i][j], 1.0)
                self.assertGreaterEqual(self.nef.W[i][j], -1.0)
    
    def test_factory_function(self):
        """Test factory function"""
        nef = create_neural_energy_field(n=20, lr=0.01)
        self.assertEqual(nef.n, 20)
        self.assertEqual(nef.learning_rate, 0.01)
    
    def test_reset(self):
        """Test reset functionality"""
        self.nef.update(self.rho, self.goal)
        old_W = [row[:] for row in self.nef.W]
        self.nef.reset()
        # After reset, W should be different
        different = False
        for i in range(10):
            for j in range(10):
                if old_W[i][j] != self.nef.W[i][j]:
                    different = True
                    break
        self.assertTrue(different)
    
    def test_parameter_field_getter(self):
        """Test getting parameter field"""
        W_field = self.nef.get_parameter_field()
        self.assertEqual(len(W_field), 10)


if __name__ == '__main__':
    unittest.main()
