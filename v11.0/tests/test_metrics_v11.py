#!/usr/bin/env python3
"""Tests for Metrics Calculator v11.0"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.metrics import MetricsCalculator, create_metrics_calculator


class TestMetricsCalculatorV11(unittest.TestCase):
    """Test cases for Metrics Calculator v11.0"""
    
    def setUp(self):
        self.calc = MetricsCalculator(N=10)
        self.rho = [[0.5 for _ in range(10)] for __ in range(10)]
        self.vx = [[1.0 for _ in range(10)] for __ in range(10)]
        self.vy = [[1.0 for _ in range(10)] for __ in range(10)]
        self.W_real = [[0.1 for _ in range(10)] for __ in range(10)]
        self.W_imag = [[0.1 for _ in range(10)] for __ in range(10)]
    
    def test_shannon_entropy(self):
        """Test Shannon entropy"""
        entropy = self.calc.shannon_entropy(self.rho)
        self.assertGreaterEqual(entropy, 0)
    
    def test_coherence_index(self):
        """Test coherence index"""
        coherence = self.calc.coherence_index(self.rho)
        self.assertGreaterEqual(coherence, 0)
        self.assertLessEqual(coherence, 1)
    
    def test_total_energy(self):
        """Test total energy"""
        energy = self.calc.total_energy(self.rho, self.vx, self.vy)
        self.assertGreaterEqual(energy, 0)
    
    def test_operator_gain(self):
        """Test operator gain"""
        gain = self.calc.operator_gain(self.W_real, self.W_imag)
        self.assertGreaterEqual(gain, 0)
    
    def test_operator_stability(self):
        """Test operator stability classification"""
        stability = self.calc.operator_stability(self.W_real, self.W_imag)
        self.assertIsInstance(stability, str)
    
    def test_learning_progress(self):
        """Test learning progress analysis"""
        # Use longer loss history to avoid "Insufficient data"
        loss_history = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
        progress = self.calc.learning_progress(loss_history)
        self.assertIn('status', progress)
        self.assertIn('loss_reduction', progress)
        self.assertIn('converged', progress)
    
    def test_learning_progress_short_history(self):
        """Test learning progress with short history"""
        loss_history = [1.0, 0.9]
        progress = self.calc.learning_progress(loss_history)
        self.assertEqual(progress['status'], 'Insufficient data')
    
    def test_get_all_metrics(self):
        """Test all metrics at once"""
        metrics = self.calc.get_all_metrics(self.rho, self.vx, self.vy, self.W_real, self.W_imag)
        self.assertIn('entropy', metrics)
        self.assertIn('coherence', metrics)
        self.assertIn('operator_gain', metrics)
    
    def test_get_all_metrics_with_loss(self):
        """Test all metrics with loss history"""
        loss_history = [1.0, 0.8, 0.6, 0.4, 0.2]
        metrics = self.calc.get_all_metrics(self.rho, self.vx, self.vy, 
                                           self.W_real, self.W_imag, loss_history)
        self.assertIn('learning', metrics)
        self.assertIn('status', metrics['learning'])
    
    def test_spectral_entropy(self):
        """Test spectral entropy"""
        spectrum = [0.5, 0.3, 0.2]
        entropy = self.calc.spectral_entropy(spectrum)
        self.assertGreaterEqual(entropy, 0)
        self.assertLessEqual(entropy, 1)
    
    def test_prediction_error(self):
        """Test prediction error"""
        pred = [[0.5 for _ in range(10)] for __ in range(10)]
        target = [[0.5 for _ in range(10)] for __ in range(10)]
        error = self.calc.prediction_error(pred, target)
        self.assertAlmostEqual(error, 0.0, places=5)
    
    def test_factory(self):
        """Test factory function"""
        calc = create_metrics_calculator(N=20)
        self.assertEqual(calc.N, 20)


if __name__ == '__main__':
    unittest.main()
