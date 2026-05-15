# 🧠 SWARMICA v3.0

## PDE Swarm Physics Engine & Neural Energy Fields

[![Version](https://img.shields.io/badge/version-3.0.0-purple.svg)](VERSION)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)](VERSION)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)

---

## 📖 Overview

SWARMICA v3.0 represents a fundamental shift from heuristic vector fields to **physics-grade PDE dynamics**. This version treats the swarm as a continuous density field evolving according to:

- **Reaction-Diffusion PDE** for continuum dynamics
- **Energy Functional Minimization** (Ginzburg-Landau type)
- **Multi-Attractor Field Structure** (not just points)
- **Stochastic Forcing** (Wiener process)

---

## 🎯 Key Features

| Feature | v2.0 | v3.0 |
|---------|------|------|
| Core Dynamics | Vector Field | **PDE (Reaction-Diffusion)** |
| Energy Model | Heuristic | **Functional Minimization** |
| Attractor Type | Points | **Field Structure** |
| Physics Grade | Approximate | **Continuum Mechanics** |
| Mathematical Class | ODE System | **PDE System** |

---

## 📐 Mathematical Framework

### PDE Formulation

```math
∂ρ/∂t = -∇·(ρV) + D∇²ρ + α(G - ρ) + σ·dW
```

Energy Functional

```math
E[ρ] = ∫(ρ² + (ρ - G)²) dΩ
```

Evolution

```math
∂ρ/∂t = -δE/δρ + D∇²ρ + σ·dW
```

---

🚀 Quick Start

Installation

```bash
cd SWARMICA/v3.0
pip install -r requirements.txt
```

Run Streamlit App

```bash
streamlit run streamlit/app.py
```

Run CLI Demo

```bash
python examples/cli_demo.py
```

Basic Usage

```python
from swarmica import PDESolver

solver = PDESolver(n=60, alpha=1.0, beta=0.2, noise=0.05)

for step in range(100):
    result = solver.step()
    print(f"Energy: {result['energy']:.4f}")
```

---

📊 Sample Output

```
============================================================
🧠 SWARMICA v3.0 - PDE Swarm Physics Engine
============================================================
Grid size: 50x50
Time step: dt=0.1

Running PDE simulation...
----------------------------------------
Step  20: Energy=125.34, Total Density=12.45
Step  40: Energy=98.76, Total Density=11.23
Step  60: Energy=76.54, Total Density=10.87
Step  80: Energy=62.34, Total Density=10.45
Step 100: Energy=51.23, Total Density=10.12
----------------------------------------

📊 Final Results:
  Final Energy:     51.23
  Initial Energy:   156.78
  Energy Reduction: 67.3%
```

---

🔬 System Class

Nonlinear Stochastic Reaction-Diffusion System
(Active Matter Physics Approximation)

This places SWARMICA v3.0 in the same mathematical class as:

· Ginzburg-Landau equations
· Fisher-KPP equations
· Active matter hydrodynamics

---

🚀 Next: SWARMICA v4.0

Planned features:

· Finite Element Method (FEM)
· Learnable energy functional (Neural PDE)
· Bifurcation detection
· Real robotics deployment

---

📝 Citation

```bibtex
@software{swarmica2026v3,
  author = {Samir Baladi},
  title = {SWARMICA v3.0: PDE Swarm Physics Engine},
  year = {2026},
  version = {3.0.0}
}
```

---

SWARMICA v3.0 — From Heuristics to Physics 🧠
