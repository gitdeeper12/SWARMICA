#!/usr/bin/env python3
"""Tests for Optimal Swarm Controller"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from swarmica.control.optimal_swarm_controller import OptimalSwarmController, create_optimal_swarm_controller


class TestOptimalSwarmController(unittest.TestCase):
    """Test cases for Optimal Swarm Controller"""
    
    def setUp(self):
        self.controller = OptimalSwarmController(n=20, alpha=1.0, beta=0.25, sigma=0.1,
                                                  control_weight=0.8, adjoint_lr=0.002)
    
    def test_initialization(self):
        """Test initialization"""
        self.assertEqual(self.controller.n, 20)
        self.assertEqual(len(self.controller.rho), 20)
    
    def test_energy(self):
        """Test energy computation"""
        energy = self.controller._energy(self.controller.rho)
        self.assertGreaterEqual(energy, 0)
    
    def test_step(self):
        """Test single step"""
        result = self.controller.step()
        self.assertIn('rho', result)
        self.assertIn('energy', result)
        self.assertIn('control_effort', result)
        self.assertIn('total_cost', result)
    
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
    
    def test_optimality_gap(self):
        """Test optimality gap"""
        self.controller.run(steps=30)
        gap = self.controller.get_optimality_gap()
        self.assertGreaterEqual(gap, 0)
    
    def test_factory(self):
        """Test factory function"""
        controller = create_optimal_swarm_controller(n=30)
        self.assertEqual(controller.n, 30)


if __name__ == '__main__':
    unittest.main()
