#!/usr/bin/env python3
"""Tests for Neural Operator Solver"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.integrator.solver import NeuralOperatorSolver, create_neural_operator_solver


class TestNeuralOperatorSolver(unittest.TestCase):
    """Test cases for Neural Operator Solver"""
    
    def setUp(self):
        self.solver = NeuralOperatorSolver(N=20, learning=True)
    
    def test_initialization(self):
        """Test solver initialization"""
        self.assertEqual(self.solver.N, 20)
        self.assertEqual(len(self.solver.rho), 20)
    
    def test_entropy(self):
        """Test entropy computation"""
        entropy = self.solver._entropy()
        self.assertGreaterEqual(entropy, 0)
    
    def test_energy(self):
        """Test energy computation"""
        energy = self.solver._energy()
        self.assertGreaterEqual(energy, 0)
    
    def test_coherence(self):
        """Test coherence computation"""
        coherence = self.solver._coherence()
        self.assertGreaterEqual(coherence, 0)
        self.assertLessEqual(coherence, 1)
    
    def test_true_dynamics(self):
        """Test true dynamics computation"""
        drho, dvx, dvy = self.solver._true_dynamics()
        self.assertEqual(len(drho), 20)
    
    def test_step(self):
        """Test single simulation step"""
        result = self.solver.step()
        self.assertIn('rho', result)
        self.assertIn('entropy', result)
        self.assertIn('coherence', result)
        self.assertIn('operator_loss', result)
    
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
        different = False
        for i in range(min(5, self.solver.N)):
            for j in range(min(5, self.solver.N)):
                if old_rho[i][j] != self.solver.rho[i][j]:
                    different = True
                    break
        self.assertTrue(different)
    
    def test_get_operator_info(self):
        """Test operator info retrieval"""
        info = self.solver.get_operator_info()
        self.assertIn('real_mean', info)
        self.assertIn('operator_norm', info)
    
    def test_factory(self):
        """Test factory function"""
        solver = create_neural_operator_solver(N=30)
        self.assertEqual(solver.N, 30)


if __name__ == '__main__':
    unittest.main()
