# 🎯 SWARMICA v6.0

## Neural Optimal Swarm Physics Engine

**Pontryagin Maximum Principle | Neural Operator | Adjoint-Based Learning**

### Quick Start

```bash
cd v6.0
pip install -r requirements.txt
streamlit run streamlit/app.py
```

Mathematical Framework

```
min_u ∫(E(ρ) + λ‖u‖²) dt
∂ρ/∂t = α·Fθ(ρ) - ∇ρ + β∇²ρ + u + σ·dW
u* = -(1/λ) p  [PMP optimal control]
∂p/∂t = -∂H/∂ρ  [Adjoint equation]
```

Key Features

· Pontryagin Maximum Principle for rigorous optimal control
· Neural PDE Operator for learned dynamics
· State-Costate forward-backward coupling
· Adjoint-based variational learning
· Stochastic continuum physics

System Class

Stochastic Neural Optimal Control PDE System with Adjoint-Based Variational Learning
