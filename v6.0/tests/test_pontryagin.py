#!/usr/bin/env python3
"""Tests for Pontryagin Controller"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from swarmica.optimal_control.pontryagin import PontryaginController, create_pontryagin_controller


class TestPontryaginController(unittest.TestCase):
    """Test cases for Pontryagin Controller"""
    
    def setUp(self):
        self.pmp = PontryaginController(n=10, control_weight=0.8, adjoint_lr=0.002)
        self.rho = [[0.5 for _ in range(10)] for __ in range(10)]
        self.goal = [[0.0 for _ in range(10)] for __ in range(10)]
        self.grad_rho = [[0.1 for _ in range(10)] for __ in range(10)]
        self.neural_grad = [[0.05 for _ in range(10)] for __ in range(10)]
    
    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.pmp.n, 10)
        self.assertEqual(self.pmp.control_weight, 0.8)
    
    def test_optimal_control(self):
        """Test optimal control law"""
        control = self.pmp.optimal_control()
        self.assertEqual(len(control), 10)
    
    def test_update_costate(self):
        """Test costate update"""
        new_costate = self.pmp.update_costate(self.rho, self.goal, self.grad_rho, self.neural_grad)
        self.assertEqual(len(new_costate), 10)
    
    def test_control_effort(self):
        """Test control effort computation"""
        control = [[0.1 for _ in range(10)] for __ in range(10)]
        effort = self.pmp.control_effort(control)
        self.assertGreater(effort, 0)
    
    def test_reset(self):
        """Test reset"""
        self.pmp.update_costate(self.rho, self.goal, self.grad_rho, self.neural_grad)
        self.pmp.reset()
        costate = self.pmp.get_costate()
        for i in range(10):
            for j in range(10):
                self.assertEqual(costate[i][j], 0.0)
    
    def test_factory(self):
        """Test factory function"""
        pmp = create_pontryagin_controller(n=20, control_weight=1.0)
        self.assertEqual(pmp.n, 20)
        self.assertEqual(pmp.control_weight, 1.0)


if __name__ == '__main__':
    unittest.main()
