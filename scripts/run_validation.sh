#!/bin/bash
# Run full validation suite

echo "🐝 SWARMICA Validation Suite"
echo "============================"

python3 benchmarks/run_all_scenarios.py --scenarios S1,S2,S3,S4 --n-monte-carlo 5

echo ""
python3 benchmarks/ablation_study.py

echo ""
python3 bin/swarmica_benchmark.py
