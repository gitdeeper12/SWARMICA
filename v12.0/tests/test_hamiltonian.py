#!/usr/bin/env python3
"""Tests for Hamiltonian Network"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.hamiltonian.network import HamiltonianNetwork, create_hamiltonian_network


class TestHamiltonianNetwork(unittest.TestCase):
    """Test cases for Hamiltonian Network"""
    
    def setUp(self):
        self.h = HamiltonianNetwork(N=10)
        self.rho = [[0.5 for _ in range(10)] for __ in range(10)]
        self.vx = [[0.1 for _ in range(10)] for __ in range(10)]
        self.vy = [[0.1 for _ in range(10)] for __ in range(10)]
    
    def test_initialization(self):
        """Test network initialization"""
        self.assertEqual(self.h.N, 10)
        self.assertEqual(len(self.h.W_rho), 10)
    
    def test_energy(self):
        """Test energy computation"""
        energy = self.h.energy(self.rho, self.vx, self.vy)
        self.assertGreaterEqual(energy, -1)
    
    def test_energy_gradient_rho(self):
        """Test density gradient"""
        grad = self.h.energy_gradient_rho(self.rho)
        self.assertEqual(len(grad), 10)
    
    def test_energy_gradient_v(self):
        """Test velocity gradient"""
        grad_vx, grad_vy = self.h.energy_gradient_v(self.vx, self.vy)
        self.assertEqual(len(grad_vx), 10)
        self.assertEqual(len(grad_vy), 10)
    
    def test_update(self):
        """Test parameter update"""
        self.h.update(self.rho, self.vx, self.vy, target_energy=0.2)
        self.assertGreater(len(self.h.history['energy']), 0)
    
    def test_reset(self):
        """Test reset"""
        self.h.update(self.rho, self.vx, self.vy, target_energy=0.2)
        self.h.reset()
        self.assertEqual(len(self.h.history['energy']), 0)
    
    def test_factory(self):
        """Test factory function"""
        h = create_hamiltonian_network(N=20)
        self.assertEqual(h.N, 20)


if __name__ == '__main__':
    unittest.main()
