# SWARMICA v5.0 — Variational Swarm Control System
# Pure Python (No NumPy) - Optimal Control over PDE Fields

import streamlit as st
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.control.variational_controller import VariationalController

st.set_page_config(page_title="SWARMICA v5.0", layout="wide")
st.title("🎮 SWARMICA v5.0 — Variational Swarm Control System")
st.markdown("*Optimal Control over Stochastic PDE Fields | Pontryagin-Inspired Feedback*")

# Sidebar controls
st.sidebar.header("⚙️ Variational Control Parameters")

grid_size = st.sidebar.slider("Grid resolution (N x N)", 40, 120, 80)
steps = st.sidebar.slider("Simulation steps", 30, 300, 150)
alpha = st.sidebar.slider("Attractor strength α", 0.5, 2.0, 1.2)
beta = st.sidebar.slider("Diffusion β", 0.1, 1.0, 0.3)
sigma = st.sidebar.slider("Noise σ", 0.0, 0.5, 0.08)
control_gain = st.sidebar.slider("Control gain λ", 0.0, 2.0, 0.6)

if st.sidebar.button("🚀 Run Variational Control"):
    
    controller = VariationalController(
        n=grid_size,
        alpha=alpha,
        beta=beta,
        sigma=sigma,
        control_gain=control_gain
    )
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for step in range(steps):
        result = controller.step()
        progress_bar.progress((step + 1) / steps)
        
        if (step + 1) % 30 == 0:
            status_text.write(f"Step {step+1}/{steps} | Total Cost: {result['total_cost']:.4f}")
    
    # Final density field
    rho = controller.rho
    n = controller.n
    z_data = [[rho[i][j] for j in range(n)] for i in range(n)]
    
    fig = go.Figure(data=go.Heatmap(z=z_data, colorscale="Viridis", zmin=0, zmax=1))
    fig.update_layout(title="Final Controlled Swarm Field (v5.0)", width=700, height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Variational metrics
    st.subheader("📉 Variational Cost Evolution")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(y=controller.history['energy'], name="Energy Cost", line=dict(color="#FFA500")))
    fig2.add_trace(go.Scatter(y=controller.history['entropy'], name="Entropy", line=dict(color="#00CED1")))
    fig2.add_trace(go.Scatter(y=controller.history['control_cost'], name="Control Cost", line=dict(color="#8B0000")))
    fig2.add_trace(go.Scatter(y=controller.history['total_cost'], name="Total Cost J", line=dict(color="#FFFFFF", dash="dash")))
    fig2.update_layout(title="Variational System Evolution", xaxis_title="Step")
    st.plotly_chart(fig2, use_container_width=True)
    
    # Final metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Final Energy", f"{controller.history['energy'][-1]:.4f}")
    with col2:
        st.metric("Final Entropy", f"{controller.history['entropy'][-1]:.4f}")
    with col3:
        st.metric("Control Cost", f"{controller.history['control_cost'][-1]:.4f}")
    with col4:
        reduction = (controller.history['total_cost'][0] - controller.history['total_cost'][-1]) / controller.history['total_cost'][0] * 100
        st.metric("Cost Reduction", f"{reduction:.1f}%")
    
    st.success("✅ SWARMICA v5.0 Simulation Complete!")
    st.balloons()

st.markdown("""
---
## ⚙️ SWARMICA v5.0 — What Changed?

### 🧠 1. Control as Optimization
System solves a **continuous control problem**:
- minimize deviation from goal
- minimize control effort
- handle stochastic noise

### 🌊 2. Stochastic PDE Dynamics
Evolution includes:
- diffusion (stability)
- drift (geometry)
- noise (uncertainty)
- optimal control input

### 📉 3. Variational Cost Tracking
We explicitly track:
- **Energy** (objective)
- **Entropy** (disorder)
- **Control Cost** (effort)
- **Total Cost J** (variational functional)

### 📐 Mathematical Formulation
```

min_u ∫(E + λ_s·S + λ_c·C) dt
∂ρ/∂t = -∇ρ + β∇²ρ + α(G-ρ) + u + σ·dW
u = λ·(G - ρ)  [Pontryagin-inspired feedback]

```

---
## 🧬 System Class

**Stochastic Variational PDE Control System**  
(Continuous Optimal Swarm Control)

---
*SWARMICA v5.0 — From Simulation to Control Theory* 🎮
""")
