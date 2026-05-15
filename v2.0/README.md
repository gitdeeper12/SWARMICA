# 🌊 SWARMICA v2.0

## Stochastic Continuum Dynamics & Adaptive Field Control

[![Version](https://img.shields.io/badge/version-2.0.0-red.svg)](VERSION)
[![Status](https://img.shields.io/badge/status-beta-orange.svg)](VERSION)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-crimson.svg)](LICENSE)

---

## 📖 Overview

SWARMICA v2.0 represents a fundamental evolution from classical variational mechanics to **stochastic continuum dynamics**. Unlike v1.0 which treated swarms as deterministic active matter fields, v2.0 introduces:

- **Vector Field Dynamics**: Density + velocity fields (not just scalar density)
- **Multi-Attractor System**: Competing attractors A₁ and A₂
- **Stochastic Perturbations**: Brownian noise for environmental uncertainty
- **Real-time Metrics**: CSI, Entropy, Lyapunov tracking
- **Pure Python**: No NumPy required - runs on Termux

---

## 🎯 Key Features

| Feature | Description | v1.0 | v2.0 |
|---------|-------------|------|------|
| Field Type | Representation | Scalar | **Vector** |
| Dynamics | Evolution | Deterministic | **Stochastic (SDE)** |
| Attractors | Target points | Single | **Multi (A₁+A₂)** |
| Metrics | Stability | CSI only | **CSI + Entropy + Lyapunov** |
| Control | Adaptation | Fixed | **Adaptive** |

---

## 📐 Mathematical Framework

### Core Equations

```math
F_total = α·(cohesion) + β·(A₁ + A₂) + η·dW
v(t+1) = γ·v(t) + F_total
x(t+1) = x(t) + dt·v(t+1)
```

Metrics

Metric Formula Interpretation
CSI 1/(1+σ²) Collective Stability Index (0-1)
Entropy -Σ p·log(p) Spatial disorder
Lyapunov ⟨‖v‖⟩ Kinetic energy proxy

---

🚀 Quick Start

Installation

```bash
# Clone the repository
git clone https://github.com/gitedeeper12/SWARMICA.git
cd SWARMICA/v2.0

# Install dependencies (no NumPy!)
pip install -r requirements.txt

# Run Streamlit app
streamlit run streamlit/app.py

# Or run CLI demo
python examples/cli_demo.py

# Generate simulation report
python examples/generate_report.py
```

Basic Usage

```python
from swarmica import SwarmControllerV2, ReportGenerator

# Create controller
controller = SwarmControllerV2(
    n_agents=80,      # Number of agents
    alpha=0.8,        # Cohesion strength
    beta=1.2,         # Attractor strength
    noise=0.2,        # Stochastic noise
    inertia=0.85      # Velocity inertia
)

# Run simulation
controller.run(steps=200)

# Access results
print(f"Final CSI: {controller.history['csi'][-1]:.4f}")
print(f"Final Entropy: {controller.history['entropy'][-1]:.4f}")

# Generate report
report_gen = ReportGenerator()
report = report_gen.generate_from_controller(controller)
report_gen.save_markdown(report)
```

---

📊 Metrics Interpretation

CSI Value Meaning Action
0.95 Excellent Stable - reduce control gain
0.90 - 0.95 Good Nominal operation
0.80 - 0.90 Fair Increase cohesion
0.70 - 0.80 Poor Increase α and β
< 0.70 Unstable Reduce noise, increase gains

---

🧪 Running Tests

```bash
# Run all tests
python tests/run_tests.py

# Run specific test
python tests/test_controller.py
python tests/test_bifurcation.py
python tests/test_coherence.py
python tests/test_report_generator.py
```

Test Results:

```
Ran 28 tests in 0.173s
OK
```

---

📁 Project Structure

```
v2.0/
├── README.md                 # This file
├── VERSION                   # Version info
├── requirements.txt          # Dependencies
│
├── swarmica/                 # Core library
│   ├── __init__.py
│   ├── control/              # SwarmControllerV2
│   ├── coherence/            # CSI, Entropy, Lyapunov
│   ├── bifurcation/          # Phase transition detection
│   ├── stochastic/           # SDE dynamics
│   ├── adaptive/             # Adaptive control
│   └── report_generator.py   # Simulation reports
│
├── streamlit/                # Web interface
│   └── app.py               # Streamlit dashboard
│
├── examples/                 # Usage examples
│   ├── cli_demo.py          # Command-line demo
│   └── generate_report.py   # Report generation
│
└── tests/                    # Unit tests (28 tests)
    ├── test_controller.py
    ├── test_bifurcation.py
    ├── test_coherence.py
    └── test_report_generator.py
```

---

🖥️ Running the Dashboard

```bash
streamlit run streamlit/app.py
```

The dashboard provides:

· Interactive parameter tuning
· Real-time swarm visualization
· CSI, Entropy, Lyapunov plots
· Final metrics summary

---

📈 Reports

SWARMICA v2.0 includes a comprehensive reporting system:

```python
from swarmica import ReportGenerator

report_gen = ReportGenerator()
report = report_gen.generate_from_controller(controller)

# Export formats
report_gen.save_json(report)      # JSON format
report_gen.save_markdown(report)  # Markdown format
report_gen.save_csv(report)       # CSV data
report_gen.print_summary(report)  # Console output
```

---

🔬 Bifurcation Detection

The bifurcation detector identifies phase transitions:

```python
from swarmica import BifurcationDetector

detector = BifurcationDetector()
detector.update(entropy, csi)

if detector.is_phase_transition():
    print("Phase transition detected!")
    
region = detector.get_stability_region()
# Returns: "Stable", "Converging", "Transitional", "Chaotic"
```

---

📊 Sample Output

Console Demo

```
============================================================
🐝 SWARMICA v2.0 - CLI Demo
============================================================
Agents: 80
Grid size: 50x50
Attractors: A1=(15, 15), A2=(35, 35)

Running simulation...
----------------------------------------
Step  20: CSI=0.8234, Entropy=2.1456
Step  40: CSI=0.8912, Entropy=1.9876
Step  60: CSI=0.9234, Entropy=1.8234
Step  80: CSI=0.9456, Entropy=1.7123
Step 100: CSI=0.9567, Entropy=1.6345
----------------------------------------

📊 Final Results:
  Final CSI:      0.9567
  Final Entropy:  1.6345
  CSI Improvement: +15.2%
```

---

🚀 Next: SWARMICA v3.0

Planned features:

· Neural Energy Fields: Learnable potential landscapes
· Persistent Homology: Topological stability analysis
· Adaptive Attractor Reshaping: Dynamic target modification
· PDE Solver Integration: Advanced numerical methods

---

📝 Citation

```bibtex
@software{swarmica2026v2,
  author = {Samir Baladi},
  title = {SWARMICA v2.0: Stochastic Continuum Dynamics for Swarm Intelligence},
  year = {2026},
  version = {2.0.0},
  doi = {10.5281/zenodo.20168278}
}
```

---

📧 Contact

· Author: Samir Baladi
· Email: gitdeeper@gmail.com
· ORCID: 0009-0003-8903-0029
· GitHub: gitedeeper12/SWARMICA

---

📄 License

MIT License - see LICENSE file for details.

---

SWARMICA v2.0 — From Deterministic Fields to Stochastic Intelligence 🐝
