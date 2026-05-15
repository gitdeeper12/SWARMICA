#!/usr/bin/env python3
"""Tests for Sparse Selector"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.sparse.selector import SparseSelector, create_sparse_selector


class TestSparseSelector(unittest.TestCase):
    """Test cases for Sparse Selector"""
    
    def setUp(self):
        self.selector = SparseSelector(alpha=0.001)
        self.Theta = [[1.0, 2.0, 3.0], [2.0, 3.0, 4.0], [3.0, 4.0, 5.0]]
        self.y = [6.0, 9.0, 12.0]
        self.term_names = ['term1', 'term2', 'term3']
    
    def test_initialization(self):
        """Test selector initialization"""
        self.assertEqual(self.selector.alpha, 0.001)
    
    def test_lasso_regression(self):
        """Test Lasso regression"""
        coeffs = self.selector.lasso_regression(self.Theta, self.y)
        self.assertEqual(len(coeffs), 3)
    
    def test_select_terms(self):
        """Test term selection"""
        coeffs = [0.5, 0.001, 0.02]
        selected = self.selector.select_terms(coeffs, self.term_names, threshold=0.01)
        self.assertEqual(len(selected), 2)
    
    def test_discover_pde(self):
        """Test PDE discovery"""
        result = self.selector.discover_pde(self.Theta, self.y, self.term_names)
        self.assertIn('coefficients', result)
        self.assertIn('pde_equation', result)
        self.assertIn('num_terms', result)
    
    def test_factory(self):
        """Test factory function"""
        selector = create_sparse_selector(alpha=0.01)
        self.assertEqual(selector.alpha, 0.01)


if __name__ == '__main__':
    unittest.main()
