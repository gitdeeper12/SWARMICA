#!/usr/bin/env python3
"""Tests for Energy Functional"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from swarmica.energy.functional import EnergyFunctional, create_energy_functional


class TestEnergyFunctional(unittest.TestCase):
    """Test cases for Energy Functional"""
    
    def setUp(self):
        self.ef = EnergyFunctional(n=10)
        self.rho = [[0.5 for _ in range(10)] for __ in range(10)]
        self.goal = [[0.0 for _ in range(10)] for __ in range(10)]
        self.goal[3][3] = 1.0
    
    def test_energy_computation(self):
        """Test energy computation"""
        energy = self.ef.compute(self.rho, self.goal)
        self.assertGreater(energy, 0)
    
    def test_gradient_computation(self):
        """Test gradient computation"""
        grad = self.ef.compute_gradient(self.rho, self.goal)
        self.assertEqual(len(grad), 10)
        self.assertEqual(len(grad[0]), 10)
    
    def test_free_energy(self):
        """Test free energy computation"""
        free_energy = self.ef.compute_free_energy(self.rho, temperature=1.0)
        self.assertGreaterEqual(free_energy, 0)
    
    def test_entropy(self):
        """Test entropy computation"""
        entropy = self.ef._compute_entropy(self.rho)
        self.assertGreaterEqual(entropy, 0)
    
    def test_factory_function(self):
        """Test factory function"""
        ef = create_energy_functional(n=20)
        self.assertEqual(ef.n, 20)
    
    def test_energy_decreases_with_goal(self):
        """Test energy decreases when density matches goal"""
        rho_match = [[self.goal[i][j] for j in range(10)] for i in range(10)]
        energy_match = self.ef.compute(rho_match, self.goal)
        energy_random = self.ef.compute(self.rho, self.goal)
        self.assertLessEqual(energy_match, energy_random)


if __name__ == '__main__':
    unittest.main()
