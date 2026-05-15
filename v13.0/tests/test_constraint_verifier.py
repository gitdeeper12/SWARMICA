#!/usr/bin/env python3
"""Tests for Constraint Verifier"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import math
from swarmica.verifier.constraints import ConstraintVerifier, create_constraint_verifier


class TestConstraintVerifier(unittest.TestCase):
    """Test cases for Constraint Verifier"""
    
    def setUp(self):
        self.verifier = ConstraintVerifier(N=10)
        self.u = [[0.5 for _ in range(10)] for __ in range(10)]
    
    def test_initialization(self):
        """Test verifier initialization"""
        self.assertEqual(self.verifier.N, 10)
    
    def test_check_mass_conservation(self):
        """Test mass conservation check"""
        mass = self.verifier.check_mass_conservation(self.u)
        self.assertGreater(mass, 0)
    
    def test_check_positivity(self):
        """Test positivity check"""
        is_positive = self.verifier.check_positivity(self.u)
        self.assertTrue(is_positive)
    
    def test_check_boundedness(self):
        """Test boundedness check"""
        is_bounded = self.verifier.check_boundedness(self.u)
        self.assertTrue(is_bounded)
    
    def test_verify_pde(self):
        """Test PDE verification"""
        coeffs = {'u': 0.5, '∇²u': 0.1}
        result = self.verifier.verify_pde("∂u/∂t = 0.5·u + 0.1·∇²u", coeffs)
        self.assertIn('verified', result)
        self.assertIn('has_diffusion', result)
    
    def test_factory(self):
        """Test factory function"""
        verifier = create_constraint_verifier(N=20)
        self.assertEqual(verifier.N, 20)


if __name__ == '__main__':
    unittest.main()
