#!/usr/bin/env python3
"""Tests for Fourier Spectral Layer"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.spectral.fourier import FourierSpectralLayer, create_fourier_spectral_layer


class TestFourierSpectralLayer(unittest.TestCase):
    """Test cases for Fourier Spectral Layer"""
    
    def setUp(self):
        self.spectral = FourierSpectralLayer(N=10, n_modes=5)
        self.field = [[0.5 for _ in range(10)] for __ in range(10)]
        self.field[5][5] = 1.0
    
    def test_initialization(self):
        """Test spectral layer initialization"""
        self.assertEqual(self.spectral.N, 10)
        self.assertEqual(self.spectral.n_modes, 5)
        self.assertEqual(len(self.spectral.filters), 5)
    
    def test_fft_2d(self):
        """Test 2D FFT"""
        transformed = self.spectral._fft_2d(self.field)
        self.assertEqual(len(transformed), 10)
        self.assertEqual(len(transformed[0]), 10)
    
    def test_ifft_2d(self):
        """Test 2D IFFT"""
        transformed = self.spectral._fft_2d(self.field)
        reconstructed = self.spectral._ifft_2d(transformed)
        self.assertEqual(len(reconstructed), 10)
    
    def test_forward(self):
        """Test forward spectral transform"""
        result = self.spectral.forward(self.field)
        self.assertEqual(len(result), 10)
    
    def test_get_spectrum(self):
        """Test spectrum retrieval"""
        spectrum = self.spectral.get_spectrum()
        self.assertEqual(len(spectrum), 5)
    
    def test_factory(self):
        """Test factory function"""
        spectral = create_fourier_spectral_layer(N=20, n_modes=8)
        self.assertEqual(spectral.N, 20)
        self.assertEqual(spectral.n_modes, 8)


if __name__ == '__main__':
    unittest.main()
