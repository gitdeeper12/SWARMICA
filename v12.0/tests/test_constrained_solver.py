#!/usr/bin/env python3
"""Tests for Constrained Neural Solver"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.solver.constrained_solver import ConstrainedNeuralSolver, create_constrained_neural_solver


class TestConstrainedNeuralSolver(unittest.TestCase):
    """Test cases for Constrained Neural Solver"""
    
    def setUp(self):
        self.solver = ConstrainedNeuralSolver(N=20, learning=True)
    
    def test_initialization(self):
        """Test solver initialization"""
        self.assertEqual(self.solver.N, 20)
        self.assertEqual(len(self.solver.rho), 20)
    
    def test_entropy(self):
        """Test entropy computation"""
        entropy = self.solver._entropy(self.solver.rho)
        self.assertGreaterEqual(entropy, 0)
    
    def test_coherence(self):
        """Test coherence computation"""
        coherence = self.solver._coherence(self.solver.rho)
        self.assertGreaterEqual(coherence, 0)
        self.assertLessEqual(coherence, 1)
    
    def test_step(self):
        """Test single simulation step"""
        result = self.solver.step()
        self.assertIn('rho', result)
        self.assertIn('energy', result)
        self.assertIn('mass', result)
        self.assertIn('coherence', result)
    
    def test_mass_conservation(self):
        """Test mass conservation over steps"""
        self.solver.run(steps=10)
        mass_initial = self.solver.history['mass'][0]
        mass_final = self.solver.history['mass'][-1]
        self.assertAlmostEqual(mass_initial, mass_final, places=5)
    
    def test_run(self):
        """Test multiple simulation steps"""
        history = self.solver.run(steps=20)
        self.assertEqual(len(history['energy']), 20)
        self.assertEqual(len(history['mass']), 20)
    
    def test_reset(self):
        """Test reset functionality"""
        self.solver.run(steps=10)
        old_rho = [row[:] for row in self.solver.rho]
        self.solver.reset()
        different = False
        for i in range(min(5, self.solver.N)):
            for j in range(min(5, self.solver.N)):
                if old_rho[i][j] != self.solver.rho[i][j]:
                    different = True
                    break
        self.assertTrue(different)
    
    def test_conservation_report(self):
        """Test conservation report generation"""
        self.solver.run(steps=15)
        report = self.solver.get_conservation_report()
        self.assertIn('mass_conserved', report)
        self.assertIn('symplectic_structure', report)
    
    def test_factory(self):
        """Test factory function"""
        solver = create_constrained_neural_solver(N=30)
        self.assertEqual(solver.N, 30)


if __name__ == '__main__':
    unittest.main()
