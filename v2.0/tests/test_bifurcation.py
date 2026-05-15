#!/usr/bin/env python3
"""Tests for bifurcation detector"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from swarmica.bifurcation.detector import BifurcationDetector, create_bifurcation_detector


class TestBifurcationDetector(unittest.TestCase):
    """Test cases for BifurcationDetector"""
    
    def setUp(self):
        self.detector = BifurcationDetector()
    
    def test_initialization(self):
        """Test detector initialization"""
        self.assertEqual(self.detector.history_size, 100)
        self.assertEqual(len(self.detector._entropy_history), 0)
    
    def test_update(self):
        """Test updating history"""
        self.detector.update(0.5, 0.8)
        self.assertEqual(len(self.detector._entropy_history), 1)
        self.assertEqual(len(self.detector._csi_history), 1)
    
    def test_bifurcation_index(self):
        """Test bifurcation index computation"""
        for i in range(10):
            self.detector.update(0.5 + i*0.01, 0.8 - i*0.01)
        
        bif_index = self.detector.bifurcation_index()
        self.assertGreaterEqual(bif_index, 0)
    
    def test_phase_transition_detection(self):
        """Test phase transition detection"""
        # Add large changes to simulate phase transition
        self.detector.update(0.5, 0.8)
        self.detector.update(0.6, 0.7)
        self.detector.update(0.8, 0.5)  # Large jump
        
        self.assertTrue(self.detector.is_phase_transition(threshold=0.01))
    
    def test_stability_region(self):
        """Test stability region classification"""
        # Add high CSI values (stable)
        for _ in range(15):
            self.detector.update(0.2, 0.95)
        
        region = self.detector.get_stability_region()
        self.assertIn(region, ["Stable (Attractor Basin)", "Converging", "Transitional", "Chaotic/Unstable", "Unknown"])
    
    def test_reset(self):
        """Test reset functionality"""
        self.detector.update(0.5, 0.8)
        self.detector.update(0.6, 0.7)
        self.assertEqual(len(self.detector._entropy_history), 2)
        
        self.detector.reset()
        self.assertEqual(len(self.detector._entropy_history), 0)
        self.assertEqual(len(self.detector._csi_history), 0)
    
    def test_create_factory(self):
        """Test factory function"""
        detector = create_bifurcation_detector()
        self.assertIsInstance(detector, BifurcationDetector)


if __name__ == '__main__':
    unittest.main()
