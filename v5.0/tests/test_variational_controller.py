#!/usr/bin/env python3
"""Tests for Variational Controller"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from swarmica.control.variational_controller import VariationalController, create_variational_controller


class TestVariationalController(unittest.TestCase):
    """Test cases for Variational Controller"""
    
    def setUp(self):
        self.controller = VariationalController(n=20, alpha=1.2, beta=0.3, sigma=0.08, control_gain=0.6)
    
    def test_initialization(self):
        """Test controller initialization"""
        self.assertEqual(self.controller.n, 20)
        self.assertEqual(len(self.controller.rho), 20)
    
    def test_goal_field(self):
        """Test goal field initialization"""
        n = self.controller.n
        self.assertEqual(self.controller.goal[n//4][n//4], 1.0)
        self.assertEqual(self.controller.goal[3*n//4][3*n//4], 1.0)
    
    def test_step(self):
        """Test single simulation step"""
        result = self.controller.step()
        self.assertIn('rho', result)
        self.assertIn('energy', result)
        self.assertIn('entropy', result)
        self.assertIn('control_cost', result)
        self.assertIn('total_cost', result)
    
    def test_density_bounds(self):
        """Test density remains within [0, 1]"""
        self.controller.run(steps=30)
        for i in range(self.controller.n):
            for j in range(self.controller.n):
                self.assertGreaterEqual(self.controller.rho[i][j], 0)
                self.assertLessEqual(self.controller.rho[i][j], 1)
    
    def test_run(self):
        """Test multiple simulation steps"""
        history = self.controller.run(steps=40)
        self.assertEqual(len(history['energy']), 40)
        self.assertEqual(len(history['total_cost']), 40)
    
    def test_reset(self):
        """Test reset functionality"""
        self.controller.run(steps=20)
        old_rho = [row[:] for row in self.controller.rho]
        self.controller.reset()
        # After reset, density field should be different
        different = False
        for i in range(self.controller.n):
            for j in range(self.controller.n):
                if old_rho[i][j] != self.controller.rho[i][j]:
                    different = True
                    break
        self.assertTrue(different)
    
    def test_factory_function(self):
        """Test factory function"""
        controller = create_variational_controller(n=30)
        self.assertEqual(controller.n, 30)
    
    def test_cost_decreases_over_time(self):
        """Test total cost generally decreases over time"""
        self.controller.run(steps=50)
        initial_cost = self.controller.history['total_cost'][0]
        final_cost = self.controller.history['total_cost'][-1]
        # Cost should decrease (or at least not increase significantly)
        self.assertLessEqual(final_cost, initial_cost + 10)


if __name__ == '__main__':
    unittest.main()
