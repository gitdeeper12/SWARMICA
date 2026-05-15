#!/usr/bin/env python3
"""Tests for report generator"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import json
from swarmica.control.swarm_controller import SwarmControllerV2
from swarmica.report_generator import ReportGenerator, create_report_generator


class TestReportGenerator(unittest.TestCase):
    """Test cases for ReportGenerator"""
    
    def setUp(self):
        self.controller = SwarmControllerV2(n_agents=30)
        self.controller.run(steps=50)
        self.report_gen = ReportGenerator()
        self.config = {'n_agents': 30, 'alpha': 0.8}
    
    def test_generate_report(self):
        """Test report generation from controller"""
        report = self.report_gen.generate_from_controller(self.controller, self.config)
        self.assertIsNotNone(report)
        self.assertIn('csi', report.metrics)
        self.assertIn('final_csi', report.summary)
    
    def test_save_json(self):
        """Test saving JSON report"""
        report = self.report_gen.generate_from_controller(self.controller, self.config)
        filepath = self.report_gen.save_json(report, "test_report.json")
        self.assertTrue(os.path.exists(filepath))
        # Clean up
        os.remove(filepath)
    
    def test_print_summary(self):
        """Test print summary (no assertion, just run)"""
        report = self.report_gen.generate_from_controller(self.controller, self.config)
        self.report_gen.print_summary(report)
    
    def test_factory_function(self):
        """Test factory function"""
        rg = create_report_generator()
        self.assertIsInstance(rg, ReportGenerator)
    
    def test_variance_calculation(self):
        """Test variance calculation"""
        data = [1, 2, 3, 4, 5]
        variance = self.report_gen._variance(data)
        self.assertGreater(variance, 0)
    
    def test_convergence_detection(self):
        """Test convergence step detection"""
        csi_history = [0.1, 0.3, 0.5, 0.7, 0.85, 0.92, 0.94, 0.95]
        step = self.report_gen._find_convergence_step(csi_history, threshold=0.9)
        self.assertEqual(step, 5)


if __name__ == '__main__':
    unittest.main()
