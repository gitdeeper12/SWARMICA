#!/usr/bin/env python3
"""Tests for Conservation Laws"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.conservation.laws import ConservationLaws, create_conservation_laws


class TestConservationLaws(unittest.TestCase):
    """Test cases for Conservation Laws"""
    
    def setUp(self):
        self.cons = ConservationLaws(N=10)
        self.rho = [[0.5 for _ in range(10)] for __ in range(10)]
        self.vx = [[0.1 for _ in range(10)] for __ in range(10)]
        self.vy = [[0.1 for _ in range(10)] for __ in range(10)]
    
    def test_mass_conservation(self):
        """Test mass conservation enforcement"""
        result = self.cons.enforce_mass_conservation(self.rho)
        mass = self.cons.total_mass(result)
        self.assertAlmostEqual(mass, 1.0, places=5)
    
    def test_entropy_constraint(self):
        """Test entropy constraint"""
        result = self.cons.entropy_constraint(self.rho, self.rho)
        self.assertEqual(len(result), 10)
    
    def test_total_mass(self):
        """Test total mass computation"""
        mass = self.cons.total_mass(self.rho)
        self.assertGreater(mass, 0)
    
    def test_check_conservation(self):
        """Test conservation checking"""
        result = self.cons.check_conservation(self.rho, self.rho)
        self.assertIn('mass_conserved', result)
    
    def test_symplectic_step(self):
        """Test symplectic integration step"""
        dH_dx = [[0.1 for _ in range(10)] for __ in range(10)]
        dH_dy = [[0.1 for _ in range(10)] for __ in range(10)]
        new_rho, new_vx, new_vy = self.cons.symplectic_step(
            self.rho, self.vx, self.vy, dH_dx, dH_dy, dt=0.01
        )
        self.assertEqual(len(new_rho), 10)
    
    def test_factory(self):
        """Test factory function"""
        cons = create_conservation_laws(N=20)
        self.assertEqual(cons.N, 20)


if __name__ == '__main__':
    unittest.main()
