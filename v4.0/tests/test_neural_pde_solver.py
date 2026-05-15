#!/usr/bin/env python3
"""Tests for Neural PDE Solver v4.0"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from swarmica.control.neural_pde_solver import NeuralPDESolver, create_neural_pde_solver


class TestNeuralPDESolver(unittest.TestCase):
    """Test cases for Neural PDE Solver"""
    
    def setUp(self):
        self.solver = NeuralPDESolver(n=20, alpha=1.0, beta=0.25, noise=0.05, energy_lr=0.001)
    
    def test_initialization(self):
        """Test solver initialization"""
        self.assertEqual(self.solver.n, 20)
        self.assertEqual(len(self.solver.rho), 20)
        self.assertEqual(len(self.solver.rho[0]), 20)
    
    def test_goal_field(self):
        """Test goal field initialization"""
        n = self.solver.n
        self.assertEqual(self.solver.goal[n//3][n//3], 1.0)
        self.assertEqual(self.solver.goal[2*n//3][2*n//3], 1.0)
    
    def test_step(self):
        """Test single simulation step"""
        result = self.solver.step()
        self.assertIn('rho', result)
        self.assertIn('energy', result)
        self.assertIn('order_parameter', result)
        self.assertIn('phase', result)
    
    def test_density_bounds(self):
        """Test density remains within [0, 1]"""
        self.solver.run(steps=30)
        for i in range(self.solver.n):
            for j in range(self.solver.n):
                self.assertGreaterEqual(self.solver.rho[i][j], 0)
                self.assertLessEqual(self.solver.rho[i][j], 1)
    
    def test_run(self):
        """Test multiple simulation steps"""
        history = self.solver.run(steps=40)
        self.assertEqual(len(history['energy']), 40)
        self.assertEqual(len(history['order_parameter']), 40)
    
    def test_reset(self):
        """Test reset functionality"""
        self.solver.run(steps=20)
        old_rho = [row[:] for row in self.solver.rho]
        self.solver.reset()
        # After reset, density field should be different
        different = False
        for i in range(self.solver.n):
            for j in range(self.solver.n):
                if old_rho[i][j] != self.solver.rho[i][j]:
                    different = True
                    break
        self.assertTrue(different)
    
    def test_phase_report(self):
        """Test phase report generation"""
        self.solver.run(steps=30)
        report = self.solver.get_phase_report()
        self.assertIn('current_phase', report)
        self.assertIn('current_order_parameter', report)
    
    def test_factory_function(self):
        """Test factory function"""
        solver = create_neural_pde_solver(n=30)
        self.assertEqual(solver.n, 30)


if __name__ == '__main__':
    unittest.main()
