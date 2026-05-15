# 🔬 SWARMICA v7.0

## Continuous Neural Control PDE System

**Neural Controlled Stochastic PDE | Variational Stability Structure**

### Mathematical Framework

```

∂ρ/∂t = Nθ(ρ) - K∇Φ(ρ) + βΔρ + σξ(x,t)
E[ρ] = ∫(ρ - ρ)² dx + λ∫‖∇ρ‖² dx
V[ρ] = ∫(ρ - ρ)² dx + ∫|∇ρ|² dx

```

### Key Features
- **Continuous-Time Formulation** - Full PDE evolution
- **Variational Stability Structure** - Lyapunov function
- **Neural Operator Dynamics** - Learned Nθ(ρ)
- **Rigorous Stability Observable** - Energy decay tracking

### Quick Start

```bash
cd v7.0
pip install -r requirements.txt
streamlit run streamlit/app.py
```

System Class

Neural Controlled Stochastic PDE with Variational Stability Structure
