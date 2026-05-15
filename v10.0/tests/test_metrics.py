#!/usr/bin/env python3
"""Tests for Metrics Calculator"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.metrics import MetricsCalculator, create_metrics_calculator


class TestMetricsCalculator(unittest.TestCase):
    """Test cases for Metrics Calculator"""
    
    def setUp(self):
        self.calc = MetricsCalculator(N=10)
        self.rho = [[0.5 for _ in range(10)] for __ in range(10)]
        self.vx = [[1.0 for _ in range(10)] for __ in range(10)]
        self.vy = [[1.0 for _ in range(10)] for __ in range(10)]
        self.theta = [[0.1 for _ in range(10)] for __ in range(10)]
        self.grad = [[0.2 for _ in range(10)] for __ in range(10)]
    
    def test_shannon_entropy(self):
        """Test Shannon entropy"""
        entropy = self.calc.shannon_entropy(self.rho)
        self.assertGreaterEqual(entropy, 0)
    
    def test_coherence_index(self):
        """Test coherence index"""
        coherence = self.calc.coherence_index(self.rho)
        self.assertGreaterEqual(coherence, 0)
        self.assertLessEqual(coherence, 1)
    
    def test_kinetic_energy(self):
        """Test kinetic energy"""
        ke = self.calc.kinetic_energy(self.vx, self.vy)
        self.assertGreaterEqual(ke, 0)
    
    def test_potential_energy(self):
        """Test potential energy"""
        pe = self.calc.potential_energy(self.rho, self.theta)
        self.assertGreaterEqual(pe, 0)
    
    def test_total_energy(self):
        """Test total energy"""
        te = self.calc.total_energy(self.rho, self.vx, self.vy, self.theta)
        self.assertGreaterEqual(te, 0)
    
    def test_total_variation(self):
        """Test total variation"""
        tv = self.calc.total_variation(self.rho)
        self.assertGreaterEqual(tv, 0)
    
    def test_psnr(self):
        """Test PSNR"""
        target = [[0.5 for _ in range(10)] for __ in range(10)]
        psnr = self.calc.peak_signal_to_noise(self.rho, target)
        self.assertGreaterEqual(psnr, 0)
    
    def test_structural_similarity(self):
        """Test SSIM"""
        target = [[0.5 for _ in range(10)] for __ in range(10)]
        ssim = self.calc.structural_similarity(self.rho, target)
        self.assertGreaterEqual(ssim, 0)
        self.assertLessEqual(ssim, 1)
    
    def test_get_all_metrics(self):
        """Test all metrics at once"""
        metrics = self.calc.get_all_metrics(self.rho, self.vx, self.vy, self.theta)
        self.assertIn('entropy', metrics)
        self.assertIn('coherence', metrics)
        self.assertIn('kinetic_energy', metrics)
    
    def test_factory(self):
        """Test factory function"""
        calc = create_metrics_calculator(N=20)
        self.assertEqual(calc.N, 20)


if __name__ == '__main__':
    unittest.main()
