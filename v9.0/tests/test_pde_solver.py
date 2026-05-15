#!/usr/bin/env python3
"""Tests for Continuum PDE Solver"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.pde.solver import ContinuumPDESolver, create_continuum_pde_solver


class TestContinuumPDESolver(unittest.TestCase):
    """Test cases for Continuum PDE Solver"""
    
    def setUp(self):
        self.solver = ContinuumPDESolver(N=20, alpha=1.0, gamma=0.3, nu=0.2)
    
    def test_initialization(self):
        """Test solver initialization"""
        self.assertEqual(self.solver.N, 20)
        self.assertEqual(len(self.solver.rho), 20)
        self.assertEqual(len(self.solver.vx), 20)
    
    def test_laplacian(self):
        """Test Laplacian computation"""
        field = [[0.0 for _ in range(20)] for __ in range(20)]
        field[10][10] = 1.0
        lap = self.solver._laplacian(field)
        self.assertEqual(len(lap), 20)
        self.assertEqual(len(lap[0]), 20)
    
    def test_gradient_field(self):
        """Test gradient field computation"""
        gx, gy = self.solver._gradient_field(self.solver.rho)
        self.assertEqual(len(gx), 20)
        self.assertEqual(len(gy), 20)
    
    def test_energy_gradient(self):
        """Test energy gradient computation"""
        grad = self.solver._energy_gradient()
        self.assertEqual(len(grad), 20)
    
    def test_energy_functional(self):
        """Test energy functional computation"""
        energy = self.solver._energy_functional()
        self.assertGreaterEqual(energy, 0)
    
    def test_entropy(self):
        """Test entropy computation"""
        entropy = self.solver._entropy()
        self.assertGreaterEqual(entropy, 0)
    
    def test_coherence(self):
        """Test coherence computation"""
        coherence = self.solver._coherence()
        self.assertGreaterEqual(coherence, 0)
        self.assertLessEqual(coherence, 1)
    
    def test_divergence(self):
        """Test divergence computation"""
        flux_x = [[1.0 for _ in range(20)] for __ in range(20)]
        flux_y = [[1.0 for _ in range(20)] for __ in range(20)]
        div = self.solver._divergence(flux_x, flux_y)
        self.assertEqual(len(div), 20)
    
    def test_step(self):
        """Test single simulation step"""
        result = self.solver.step()
        self.assertIn('rho', result)
        self.assertIn('entropy', result)
        self.assertIn('coherence', result)
        self.assertIn('energy', result)
    
    def test_density_bounds(self):
        """Test density remains within [0, 1]"""
        self.solver.run(steps=20)
        for i in range(self.solver.N):
            for j in range(self.solver.N):
                self.assertGreaterEqual(self.solver.rho[i][j], 0)
                self.assertLessEqual(self.solver.rho[i][j], 1)
    
    def test_run(self):
        """Test multiple simulation steps"""
        history = self.solver.run(steps=30)
        self.assertEqual(len(history['entropy']), 30)
        self.assertEqual(len(history['coherence']), 30)
    
    def test_reset(self):
        """Test reset functionality"""
        self.solver.run(steps=20)
        old_rho = [row[:] for row in self.solver.rho]
        self.solver.reset()
        # After reset, density field should be different
        different = False
        for i in range(min(5, self.solver.N)):
            for j in range(min(5, self.solver.N)):
                if old_rho[i][j] != self.solver.rho[i][j]:
                    different = True
                    break
        self.assertTrue(different)
    
    def test_factory_function(self):
        """Test factory function"""
        solver = create_continuum_pde_solver(N=30)
        self.assertEqual(solver.N, 30)


if __name__ == '__main__':
    unittest.main()
