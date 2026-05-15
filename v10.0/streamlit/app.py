# SWARMICA v10.0 — Neural Field + Inverse Physics System
# Learned Continuum Swarm Dynamics

import streamlit as st
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.pde.neural_solver import NeuralPDESolver

st.set_page_config(page_title="SWARMICA v10.0", layout="wide")
st.title("🧠 SWARMICA v10.0 — Neural Field + Inverse Physics System")
st.markdown("*Learned Continuum Swarm Dynamics | Self-Discovery of Physical Laws*")

# Sidebar controls
st.sidebar.header("⚙️ Neural PDE Parameters")

grid_size = st.sidebar.slider("Grid resolution (N x N)", 50, 120, 80)
steps = st.sidebar.slider("Simulation steps", 100, 500, 250)
nu = st.sidebar.slider("Viscosity ν", 0.05, 0.5, 0.2)
gamma = st.sidebar.slider("Damping γ", 0.1, 0.6, 0.3)
learning = st.sidebar.checkbox("Enable Learning", value=True)

if st.sidebar.button("🚀 Run Neural PDE Simulation"):
    
    solver = NeuralPDESolver(N=grid_size, nu=nu, gamma=gamma, learning=learning)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for step in range(steps):
        result = solver.step()
        progress_bar.progress((step + 1) / steps)
        
        if (step + 1) % 50 == 0:
            status_text.write(f"Step {step+1}/{steps} | Coherence: {result['coherence']:.4f} | Energy Loss: {result['energy_loss']:.4f}")
    
    # Final density field
    rho = solver.rho
    N = solver.N
    z_data = [[rho[i][j] for j in range(N)] for i in range(N)]
    
    fig = go.Figure(data=go.Heatmap(z=z_data, colorscale="Viridis", zmin=0, zmax=1))
    fig.update_layout(title="Final Learned Density Field ρ(x,y)", width=700, height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Learned parameters visualization
    theta = solver.energy_model.get_parameters()
    theta_data = [[theta[i][j] for j in range(N)] for i in range(N)]
    
    fig_t = go.Figure(data=go.Heatmap(z=theta_data, colorscale="RdBu", zmin=-0.2, zmax=0.2))
    fig_t.update_layout(title="Learned Energy Parameters Θ(x,y)", width=700, height=600)
    st.plotly_chart(fig_t, use_container_width=True)
    
    # Metrics
    st.subheader("📊 Neural Physics Evolution")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(y=solver.history['coherence'], name="Coherence", line=dict(color="#8B0000", width=2)))
    fig2.add_trace(go.Scatter(y=solver.history['entropy'], name="Entropy", line=dict(color="#FFA500", width=2)))
    fig2.add_trace(go.Scatter(y=solver.history['energy_loss'], name="Energy Loss E_θ(ρ)", line=dict(color="#00CED1", width=2)))
    
    fig2.update_layout(
        title="Learned Physics Evolution",
        xaxis_title="Step",
        yaxis_title="Value",
        plot_bgcolor="#0d0d0d",
        paper_bgcolor="#050505"
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Final Coherence", f"{solver.history['coherence'][-1]:.4f}")
    with col2:
        st.metric("Final Entropy", f"{solver.history['entropy'][-1]:.4f}")
    with col3:
        st.metric("Final Energy Loss", f"{solver.history['energy_loss'][-1]:.4f}")
    
    st.success("✅ SWARMICA v10.0 Neural PDE Simulation Complete!")
    st.balloons()

st.markdown("""
---
## ⚙️ SWARMICA v10.0 — What Changed?

### 🧠 1. Neural Energy Functional
**E_θ(ρ)** is learned, not designed:
- System discovers its own physics
- Parameters update via Hebbian learning

### 🔬 2. Inverse Physics Problem
From trajectories → discover physical laws:
- No predefined equations
- Emergent dynamics

### 📉 3. Learned PDE
```

∂ρ/∂t = -∇·(ρv)
∂v/∂t = -∇E_θ(ρ) - γv + ν∇²v

```

### 🎯 4. Self-Discovery
The system learns:
- When energy is high/low
- How to minimize energy
- Stable configurations

---

## 🧬 System Class

**Neural PDEs | Energy-Based Models (EBM)**
**Inverse Problems in Physics | Neural Operators**

---

## 🔑 Critical Shift

| v9.0 | v10.0 |
|------|-------|
| Physics is given | **Physics is learned** |
| PDE is fixed | **PDE is emergent** |
| Energy is designed | **Energy is discovered** |

---
*SWARMICA v10.0 — The Machine Learns Its Own Physics* 🧠
""")
