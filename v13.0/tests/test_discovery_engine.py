#!/usr/bin/env python3
"""Tests for Discovery Engine"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.core.discovery_engine import DiscoveryEngine, create_discovery_engine


class TestDiscoveryEngine(unittest.TestCase):
    """Test cases for Discovery Engine"""
    
    def setUp(self):
        self.engine = DiscoveryEngine(N=20, alpha=0.001)
    
    def test_initialization(self):
        """Test engine initialization"""
        self.assertEqual(self.engine.N, 20)
    
    def test_observe(self):
        """Test observation generation"""
        u, du_dt = self.engine.observe()
        self.assertEqual(len(u), 20)
        self.assertEqual(len(du_dt), 20)
    
    def test_discover_physics(self):
        """Test physics discovery"""
        result = self.engine.discover_physics()
        self.assertIn('discovered_pde', result)
        self.assertIn('coefficients', result)
    
    def test_run_discovery(self):
        """Test multiple discovery iterations"""
        results = self.engine.run_discovery(iterations=2)
        self.assertEqual(len(results), 2)
    
    def test_get_best_pde(self):
        """Test best PDE selection"""
        results = self.engine.run_discovery(iterations=2)
        best = self.engine.get_best_pde(results)
        self.assertIsNotNone(best)
    
    def test_factory(self):
        """Test factory function"""
        engine = create_discovery_engine(N=30)
        self.assertEqual(engine.N, 30)


if __name__ == '__main__':
    unittest.main()
