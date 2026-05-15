#!/usr/bin/env python3
"""Tests for Symplectic Operator"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.constraints.symplectic import SymplecticOperator, create_symplectic_operator


class TestSymplecticOperator(unittest.TestCase):
    """Test cases for Symplectic Operator"""
    
    def setUp(self):
        self.symp = SymplecticOperator(N=10)
        self.field = [[0.5 for _ in range(10)] for __ in range(10)]
    
    def test_gradient_rho(self):
        """Test density gradient"""
        gx, gy = self.symp.gradient_rho(self.field)
        self.assertEqual(len(gx), 10)
        self.assertEqual(len(gy), 10)
    
    def test_symplectic_flow(self):
        """Test symplectic flow"""
        dH_dx = [[0.1 for _ in range(10)] for __ in range(10)]
        dH_dy = [[0.1 for _ in range(10)] for __ in range(10)]
        flow_x, flow_y = self.symp.symplectic_flow(dH_dx, dH_dy)
        self.assertEqual(len(flow_x), 10)
    
    def test_poisson_bracket(self):
        """Test Poisson bracket"""
        g1x = [[0.1 for _ in range(10)] for __ in range(10)]
        g1y = [[0.1 for _ in range(10)] for __ in range(10)]
        g2x = [[0.1 for _ in range(10)] for __ in range(10)]
        g2y = [[0.1 for _ in range(10)] for __ in range(10)]
        bracket = self.symp.poisson_bracket(g1x, g1y, g2x, g2y)
        self.assertEqual(len(bracket), 10)
    
    def test_hamiltonian_equations(self):
        """Test Hamilton's equations"""
        dH_drho = [[0.1 for _ in range(10)] for __ in range(10)]
        dH_dvx = [[0.1 for _ in range(10)] for __ in range(10)]
        dH_dvy = [[0.1 for _ in range(10)] for __ in range(10)]
        drho, dvx, dvy = self.symp.hamiltonian_equations(dH_drho, dH_dvx, dH_dvy, 0.01)
        self.assertEqual(len(drho), 10)
    
    def test_symplectic_integrator(self):
        """Test symplectic integrator"""
        rho = [[0.5 for _ in range(10)] for __ in range(10)]
        vx = [[0.1 for _ in range(10)] for __ in range(10)]
        vy = [[0.1 for _ in range(10)] for __ in range(10)]
        drho = [[0.1 for _ in range(10)] for __ in range(10)]
        dvx = [[0.1 for _ in range(10)] for __ in range(10)]
        dvy = [[0.1 for _ in range(10)] for __ in range(10)]
        new_rho, new_vx, new_vy = self.symp.symplectic_integrator(
            rho, vx, vy, drho, dvx, dvy, 0.01
        )
        self.assertEqual(len(new_rho), 10)
    
    def test_factory(self):
        """Test factory function"""
        symp = create_symplectic_operator(N=20)
        self.assertEqual(symp.N, 20)


if __name__ == '__main__':
    unittest.main()
