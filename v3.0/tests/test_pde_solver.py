#!/usr/bin/env python3
"""Tests for PDE Solver"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from swarmica.pde.solver import PDESolver, create_pde_solver


class TestPDESolver(unittest.TestCase):
    """Test cases for PDE Solver"""
    
    def setUp(self):
        self.solver = PDESolver(n=20, alpha=1.0, beta=0.2, noise=0.05)
    
    def test_initialization(self):
        """Test solver initialization"""
        self.assertEqual(self.solver.n, 20)
        self.assertEqual(len(self.solver.rho), 20)
        self.assertEqual(len(self.solver.rho[0]), 20)
    
    def test_goal_field(self):
        """Test goal field initialization"""
        self.assertEqual(self.solver.goal[self.solver.n//3][self.solver.n//3], 1.0)
        self.assertEqual(self.solver.goal[2*self.solver.n//3][2*self.solver.n//3], 1.0)
    
    def test_step(self):
        """Test single simulation step"""
        result = self.solver.step()
        self.assertIn('rho', result)
        self.assertIn('energy', result)
        self.assertIn('total_density', result)
        self.assertGreaterEqual(result['energy'], 0)
    
    def test_run(self):
        """Test multiple simulation steps"""
        history = self.solver.run(steps=30)
        self.assertEqual(len(history['energy']), 30)
        self.assertEqual(len(history['total_density']), 30)
    
    def test_reset(self):
        """Test reset functionality"""
        self.solver.run(steps=20)
        old_energy = self.solver.get_energy_functional()
        self.solver.reset()
        new_energy = self.solver.get_energy_functional()
        # After reset, energy should be different (usually higher)
        self.assertNotEqual(old_energy, new_energy)
    
    def test_factory_function(self):
        """Test factory function"""
        solver = create_pde_solver(n=30, alpha=0.8, beta=0.15)
        self.assertEqual(solver.n, 30)
        self.assertEqual(solver.alpha, 0.8)
        self.assertEqual(solver.beta, 0.15)
    
    def test_density_bounds(self):
        """Test density remains within [0, 1]"""
        self.solver.run(steps=50)
        for i in range(self.solver.n):
            for j in range(self.solver.n):
                self.assertGreaterEqual(self.solver.rho[i][j], 0)
                self.assertLessEqual(self.solver.rho[i][j], 1)
    
    def test_energy_decreases_over_time(self):
        """Test energy generally decreases over time"""
        self.solver.run(steps=40)
        initial_energy = self.solver.history['energy'][0]
        final_energy = self.solver.history['energy'][-1]
        # Energy should decrease (or at least not increase significantly)
        self.assertLessEqual(final_energy, initial_energy + 10)


if __name__ == '__main__':
    unittest.main()
