#!/usr/bin/env python3
"""Tests for PDE Library Builder"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.library.builder import PDELibrary, create_pde_library


class TestPDELibrary(unittest.TestCase):
    """Test cases for PDE Library"""
    
    def setUp(self):
        self.lib = PDELibrary(N=10)
        self.u = [[0.5 for _ in range(10)] for __ in range(10)]
        self.u[5][5] = 1.0
    
    def test_initialization(self):
        """Test library initialization"""
        self.assertEqual(self.lib.N, 10)
    
    def test_gradient_x(self):
        """Test x-gradient computation"""
        grad = self.lib.gradient_x(self.u)
        self.assertEqual(len(grad), 10)
    
    def test_gradient_y(self):
        """Test y-gradient computation"""
        grad = self.lib.gradient_y(self.u)
        self.assertEqual(len(grad), 10)
    
    def test_laplacian(self):
        """Test Laplacian computation"""
        lap = self.lib.laplacian(self.u)
        self.assertEqual(len(lap), 10)
    
    def test_build_features(self):
        """Test feature matrix building"""
        features = self.lib.build_features(self.u)
        self.assertEqual(len(features), 100)  # N*N = 100
        self.assertEqual(len(features[0]), 8)  # 8 features
    
    def test_term_names(self):
        """Test term names"""
        names = self.lib.term_names()
        self.assertEqual(len(names), 8)
        self.assertIn('u', names)
        self.assertIn('∇²u', names)
    
    def test_factory(self):
        """Test factory function"""
        lib = create_pde_library(N=20)
        self.assertEqual(lib.N, 20)


if __name__ == '__main__':
    unittest.main()
