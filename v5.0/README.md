# 🎮 SWARMICA v5.0

## Variational Swarm Control System

**Optimal Control over Stochastic PDE Fields | Pontryagin-Inspired Feedback**

### Quick Start

```bash
cd v5.0
pip install -r requirements.txt
streamlit run streamlit/app.py
```

Mathematical Framework

```
min_u ∫(E + λ_s·S + λ_c·C) dt
∂ρ/∂t = -∇ρ + β∇²ρ + α(G-ρ) + u + σ·dW
u = λ·(G - ρ)
```

Key Features

· Variational Optimal Control over PDE fields
· Stochastic dynamics with Wiener noise
· Cost functional tracking (Energy + Entropy + Control)
· Pontryagin-inspired feedback law
· Real-time variational metrics

System Class

Stochastic Variational PDE Control System
(Continuous Optimal Swarm Control)
