#!/usr/bin/env python3
"""Tests for Neural Energy Model"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.neural_physics.energy_model import NeuralEnergyModel, create_neural_energy_model


class TestNeuralEnergyModel(unittest.TestCase):
    """Test cases for Neural Energy Model"""
    
    def setUp(self):
        self.model = NeuralEnergyModel(N=10)
        self.rho = [[0.5 for _ in range(10)] for __ in range(10)]
    
    def test_initialization(self):
        """Test model initialization"""
        self.assertEqual(self.model.N, 10)
        self.assertEqual(len(self.model.theta), 10)
    
    def test_forward(self):
        """Test forward pass - energy computation"""
        energy = self.model.forward(self.rho)
        self.assertGreaterEqual(energy, 0)
        self.assertLessEqual(energy, 1)
    
    def test_energy_gradient(self):
        """Test energy gradient computation"""
        grad = self.model.energy_gradient(self.rho)
        self.assertEqual(len(grad), 10)
        self.assertEqual(len(grad[0]), 10)
    
    def test_update(self):
        """Test parameter update"""
        old_theta = [row[:] for row in self.model.theta]
        self.model.update(self.rho, target_energy=0.2)
        # Theta should change
        changed = False
        for i in range(10):
            for j in range(10):
                if old_theta[i][j] != self.model.theta[i][j]:
                    changed = True
                    break
        self.assertTrue(changed)
    
    def test_parameter_clamping(self):
        """Test parameter clamping"""
        for i in range(10):
            for j in range(10):
                self.model.theta[i][j] = 2.0
        self.model.update(self.rho, target_energy=0.2)
        for i in range(10):
            for j in range(10):
                self.assertLessEqual(self.model.theta[i][j], 0.5)
                self.assertGreaterEqual(self.model.theta[i][j], -0.5)
    
    def test_reset(self):
        """Test reset"""
        self.model.update(self.rho, target_energy=0.2)
        old_theta = [row[:] for row in self.model.theta]
        self.model.reset()
        different = False
        for i in range(10):
            for j in range(10):
                if old_theta[i][j] != self.model.theta[i][j]:
                    different = True
                    break
        self.assertTrue(different)
    
    def test_factory(self):
        """Test factory function"""
        model = create_neural_energy_model(N=20)
        self.assertEqual(model.N, 20)


if __name__ == '__main__':
    unittest.main()
