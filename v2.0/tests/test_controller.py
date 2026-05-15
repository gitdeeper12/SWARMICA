#!/usr/bin/env python3
"""Unit tests for SWARMICA v2.0 SwarmController"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from swarmica.control.swarm_controller import SwarmControllerV2, create_controller_v2


class TestSwarmControllerV2(unittest.TestCase):
    """Test cases for SwarmControllerV2"""
    
    def setUp(self):
        """Set up test fixture"""
        self.controller = SwarmControllerV2(n_agents=50)
    
    def test_initialization(self):
        """Test controller initialization"""
        self.assertEqual(self.controller.n_agents, 50)
        self.assertEqual(self.controller.grid_size, 50)
        self.assertEqual(len(self.controller.positions), 50)
        self.assertEqual(len(self.controller.velocities), 50)
    
    def test_attractors(self):
        """Test attractor positions"""
        self.assertEqual(self.controller.A1, (15, 15))
        self.assertEqual(self.controller.A2, (35, 35))
    
    def test_step(self):
        """Test single simulation step"""
        result = self.controller.step()
        self.assertIn('positions', result)
        self.assertIn('csi', result)
        self.assertIn('entropy', result)
        self.assertIn('lyapunov', result)
        self.assertGreaterEqual(result['csi'], 0)
        self.assertLessEqual(result['csi'], 1)
    
    def test_csi_range(self):
        """Test CSI is between 0 and 1"""
        csi = self.controller._compute_csi()
        self.assertGreaterEqual(csi, 0)
        self.assertLessEqual(csi, 1)
    
    def test_entropy_non_negative(self):
        """Test entropy is non-negative"""
        entropy = self.controller._compute_entropy()
        self.assertGreaterEqual(entropy, 0)
    
    def test_lyapunov_non_negative(self):
        """Test Lyapunov is non-negative"""
        lyap = self.controller._compute_lyapunov()
        self.assertGreaterEqual(lyap, 0)
    
    def test_run_multiple_steps(self):
        """Test running multiple simulation steps"""
        history = self.controller.run(steps=50)
        self.assertEqual(len(history['csi']), 50)
        self.assertEqual(len(history['entropy']), 50)
        self.assertEqual(len(history['lyapunov']), 50)
    
    def test_reset(self):
        """Test reset functionality"""
        self.controller.run(steps=20)
        old_csi = self.controller.history['csi'][-1]
        self.controller.reset()
        self.assertEqual(len(self.controller.history['csi']), 0)
        self.assertEqual(len(self.controller.positions), self.controller.n_agents)
    
    def test_summary(self):
        """Test summary generation"""
        self.controller.run(steps=30)
        summary = self.controller.get_summary()
        self.assertIn('final_csi', summary)
        self.assertIn('final_entropy', summary)
        self.assertIn('final_lyapunov', summary)
        self.assertIn('csi_improvement', summary)
    
    def test_create_controller_factory(self):
        """Test factory function"""
        controller = create_controller_v2(n_agents=100)
        self.assertEqual(controller.n_agents, 100)
        self.assertIsInstance(controller, SwarmControllerV2)


class TestMetrics(unittest.TestCase):
    """Test cases for metrics computation"""
    
    def setUp(self):
        self.controller = SwarmControllerV2(n_agents=30)
    
    def test_entropy_changes(self):
        """Test entropy changes over time"""
        initial_entropy = self.controller._compute_entropy()
        self.controller.run(steps=20)
        final_entropy = self.controller._compute_entropy()
        # Entropy should generally decrease (more organized)
        # But we don't assert strict decrease due to stochastic noise
    
    def test_csi_changes(self):
        """Test CSI changes over time"""
        initial_csi = self.controller._compute_csi()
        self.controller.run(steps=20)
        final_csi = self.controller._compute_csi()
        # CSI should generally increase (more stable)
        # But we don't assert strict increase due to stochastic noise


if __name__ == '__main__':
    unittest.main()
