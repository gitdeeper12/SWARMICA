#!/usr/bin/env python3
"""Tests for Cost Functional"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from swarmica.variational.cost_functional import CostFunctional, create_cost_functional


class TestCostFunctional(unittest.TestCase):
    """Test cases for Cost Functional"""
    
    def setUp(self):
        self.cost = CostFunctional(n=10)
        self.rho = [[0.5 for _ in range(10)] for __ in range(10)]
        self.goal = [[0.0 for _ in range(10)] for __ in range(10)]
        self.goal[3][3] = 1.0
        self.control = [[0.1 for _ in range(10)] for __ in range(10)]
    
    def test_energy(self):
        """Test energy computation"""
        energy = self.cost.energy(self.rho, self.goal)
        self.assertGreater(energy, 0)
    
    def test_entropy(self):
        """Test entropy computation"""
        entropy = self.cost.entropy(self.rho)
        self.assertGreaterEqual(entropy, 0)
    
    def test_control_cost(self):
        """Test control cost computation"""
        cost = self.cost.control_cost(self.control)
        self.assertGreater(cost, 0)
    
    def test_total_cost(self):
        """Test total cost computation"""
        total = self.cost.total_cost(self.rho, self.goal, self.control)
        self.assertGreater(total, 0)
    
    def test_energy_gradient(self):
        """Test energy gradient"""
        grad = self.cost.energy_gradient(self.rho, self.goal)
        self.assertEqual(len(grad), 10)
    
    def test_factory_function(self):
        """Test factory function"""
        cost = create_cost_functional(n=20)
        self.assertEqual(cost.n, 20)


if __name__ == '__main__':
    unittest.main()
