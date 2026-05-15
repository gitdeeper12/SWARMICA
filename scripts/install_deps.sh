#!/bin/bash
# Install dependencies for SWARMICA

echo "📦 Installing SWARMICA dependencies"

# Install using pip
pip install --upgrade pip

# Core dependencies (pure Python, no NumPy)
pip install typing-extensions dataclasses

echo "✅ Dependencies installed"
echo ""
echo "To install SWARMICA: pip install -e ."
