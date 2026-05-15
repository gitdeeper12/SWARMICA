#!/usr/bin/env python3
"""Tests for SwarmicaV8 Core Engine"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.core.engine import SwarmicaV8, create_swarmica_v8


class TestSwarmicaV8(unittest.TestCase):
    """Test cases for SwarmicaV8"""
    
    def setUp(self):
        self.sim = SwarmicaV8(n_agents=50)
    
    def test_initialization(self):
        """Test simulation initialization"""
        self.assertEqual(self.sim.n_agents, 50)
        self.assertEqual(len(self.sim.positions), 50)
        self.assertEqual(len(self.sim.velocities), 50)
    
    def test_attractors(self):
        """Test attractor initialization"""
        self.assertEqual(len(self.sim.attractors), 2)
        self.assertEqual(self.sim.attractors[0], [2.0, 2.0])
        self.assertEqual(self.sim.attractors[1], [-2.0, -2.0])
    
    def test_distance(self):
        """Test distance calculation"""
        p1 = [0.0, 0.0]
        p2 = [3.0, 4.0]
        dist = self.sim._distance(p1, p2)
        self.assertAlmostEqual(dist, 5.0, places=5)
    
    def test_normalize(self):
        """Test vector normalization"""
        vec = [3.0, 4.0]
        norm = self.sim._normalize(vec)
        self.assertAlmostEqual(norm[0], 0.6, places=5)
        self.assertAlmostEqual(norm[1], 0.8, places=5)
    
    def test_field_force(self):
        """Test field force computation"""
        pos = [1.0, 1.0]
        force = self.sim.compute_field_force(pos)
        self.assertEqual(len(force), 2)
    
    def test_cohesion(self):
        """Test cohesion computation"""
        force = self.sim.compute_cohesion(0)
        self.assertEqual(len(force), 2)
    
    def test_csi_range(self):
        """Test CSI is between 0 and 1"""
        csi = self.sim.csi()
        self.assertGreaterEqual(csi, 0)
        self.assertLessEqual(csi, 1)
    
    def test_entropy_non_negative(self):
        """Test entropy is non-negative"""
        entropy = self.sim.entropy()
        self.assertGreaterEqual(entropy, 0)
    
    def test_lyapunov_non_negative(self):
        """Test Lyapunov is non-negative"""
        lyap = self.sim.lyapunov()
        self.assertGreaterEqual(lyap, 0)
    
    def test_step(self):
        """Test single simulation step"""
        result = self.sim.step()
        self.assertIn('csi', result)
        self.assertIn('entropy', result)
        self.assertIn('lyapunov', result)
    
    def test_run(self):
        """Test multiple simulation steps"""
        history = self.sim.run(steps=30)
        self.assertEqual(len(history['csi']), 30)
        self.assertEqual(len(history['entropy']), 30)
    
    def test_reset(self):
        """Test reset functionality"""
        self.sim.run(steps=20)
        old_positions = [p[:] for p in self.sim.positions]
        self.sim.reset()
        # After reset, positions should be different
        different = False
        for i in range(min(10, len(old_positions))):
            if old_positions[i] != self.sim.positions[i]:
                different = True
                break
        self.assertTrue(different)
    
    def test_summary(self):
        """Test summary generation"""
        self.sim.run(steps=30)
        summary = self.sim.get_summary()
        self.assertIn('final_csi', summary)
        self.assertIn('final_entropy', summary)
    
    def test_factory_function(self):
        """Test factory function"""
        sim = create_swarmica_v8(n_agents=100)
        self.assertEqual(sim.n_agents, 100)


if __name__ == '__main__':
    unittest.main()
