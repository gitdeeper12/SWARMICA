#!/usr/bin/env python3
"""Tests for Phase Transition Detector"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.phase_transition.detector import PhaseTransitionDetector, create_phase_transition_detector


class TestPhaseTransitionDetector(unittest.TestCase):
    """Test cases for Phase Transition Detector"""
    
    def setUp(self):
        self.detector = PhaseTransitionDetector()
        # Create a simple density field
        self.rho = [[0.5 for _ in range(10)] for __ in range(10)]
        self.rho[5][5] = 0.9
    
    def test_initialization(self):
        """Test detector initialization"""
        self.assertEqual(self.detector.history_size, 100)
        self.assertEqual(len(self.detector._order_history), 0)
    
    def test_order_parameter(self):
        """Test order parameter computation"""
        order = self.detector.order_parameter(self.rho)
        self.assertGreaterEqual(order, 0)
    
    def test_update(self):
        """Test updating history"""
        self.detector.update(0.5, 10.0)
        self.assertEqual(len(self.detector._order_history), 1)
        self.assertEqual(len(self.detector._energy_history), 1)
    
    def test_susceptibility(self):
        """Test susceptibility computation"""
        for i in range(20):
            self.detector.update(0.3 + i * 0.01, 10.0)
        susc = self.detector.susceptibility()
        self.assertGreaterEqual(susc, 0)
    
    def test_phase_transition_detection(self):
        """Test phase transition detection"""
        # Simulate a jump in order parameter
        for i in range(10):
            self.detector.update(0.3, 10.0)
        for i in range(5):
            self.detector.update(0.8, 10.0)  # Jump!
        
        self.assertTrue(self.detector.is_phase_transition(threshold=0.05))
    
    def test_get_phase(self):
        """Test phase classification"""
        self.assertEqual(self.detector.get_phase(0.1), "Disordered (Gas-like)")
        self.assertEqual(self.detector.get_phase(0.25), "Transitional (Liquid-like)")
        self.assertEqual(self.detector.get_phase(0.45), "Partially Ordered (Gel-like)")
        self.assertEqual(self.detector.get_phase(0.6), "Ordered (Crystal-like)")
    
    def test_generate_report(self):
        """Test report generation"""
        for i in range(20):
            self.detector.update(0.3 + i * 0.01, 10.0)
        
        report = self.detector.generate_report()
        self.assertIn('current_order_parameter', report)
        self.assertIn('current_phase', report)
        self.assertIn('phase_transition_detected', report)
    
    def test_critical_temperature_estimate(self):
        """Test critical temperature estimation"""
        for i in range(50):
            order = 0.3 + math.sin(i * 0.5) * 0.2
            self.detector.update(order, 10.0)
        
        crit = self.detector.critical_temperature_estimate()
        self.assertGreaterEqual(crit, 0)
    
    def test_factory_function(self):
        """Test factory function"""
        detector = create_phase_transition_detector()
        self.assertIsInstance(detector, PhaseTransitionDetector)
    
    def test_reset(self):
        """Test reset functionality"""
        self.detector.update(0.5, 10.0)
        self.detector.update(0.6, 10.0)
        self.assertEqual(len(self.detector._order_history), 2)
        self.detector.reset()
        self.assertEqual(len(self.detector._order_history), 0)


if __name__ == '__main__':
    unittest.main()
