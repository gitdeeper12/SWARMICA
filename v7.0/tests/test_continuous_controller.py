#!/usr/bin/env python3
"""Tests for Continuous Controller"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from swarmica.control.continuous_controller import ContinuousController, create_continuous_controller


class TestContinuousController(unittest.TestCase):
    """Test cases for Continuous Controller"""
    
    def setUp(self):
        self.controller = ContinuousController(n=20, beta=0.3, sigma=0.1, K_gain=1.2, lambda_reg=0.5)
    
    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.controller.n, 20)
        self.assertEqual(len(self.controller.rho), 20)
    
    def test_control_law(self):
        """Test control law"""
        control = self.controller._control_law()
        self.assertEqual(len(control), 20)
    
    def test_step(self):
        """Test single step"""
        result = self.controller.step()
        self.assertIn('rho', result)
        self.assertIn('energy', result)
        self.assertIn('stability_metric', result)
        self.assertIn('lyapunov', result)
    
    def test_density_bounds(self):
        """Test density bounds"""
        self.controller.run(steps=30)
        for i in range(self.controller.n):
            for j in range(self.controller.n):
                self.assertGreaterEqual(self.controller.rho[i][j], 0)
                self.assertLessEqual(self.controller.rho[i][j], 1)
    
    def test_run(self):
        """Test multiple steps"""
        history = self.controller.run(steps=40)
        self.assertEqual(len(history['energy']), 40)
        self.assertEqual(len(history['stability_metric']), 40)
    
    def test_reset(self):
        """Test reset"""
        self.controller.run(steps=20)
        old_rho = [row[:] for row in self.controller.rho]
        self.controller.reset()
        different = False
        for i in range(self.controller.n):
            for j in range(self.controller.n):
                if old_rho[i][j] != self.controller.rho[i][j]:
                    different = True
                    break
        self.assertTrue(different)
    
    def test_stability_certificate(self):
        """Test stability certificate"""
        self.controller.run(steps=50)
        cert = self.controller.get_stability_certificate()
        self.assertIn('certified', cert)
        self.assertIn('lyapunov_decay', cert)
    
    def test_factory(self):
        """Test factory function"""
        controller = create_continuous_controller(n=30)
        self.assertEqual(controller.n, 30)


if __name__ == '__main__':
    unittest.main()
