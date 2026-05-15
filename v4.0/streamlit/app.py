# SWARMICA v4.0 — Neural Energy PDE Swarm Engine
# Pure Python (No NumPy) - Learnable Energy Functional

import streamlit as st
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.control.neural_pde_solver import NeuralPDESolver

st.set_page_config(page_title="SWARMICA v4.0", layout="wide")
st.title("🧠 SWARMICA v4.0 — Neural Energy PDE Swarm Engine")
st.markdown("*Learnable Energy Functional | Controlled Reaction-Diffusion | Phase Transition Detection*")

# Sidebar controls
st.sidebar.header("⚙️ PDE Parameters")

grid_size = st.sidebar.slider("Grid resolution (N x N)", 30, 100, 70)
steps = st.sidebar.slider("Simulation steps", 20, 200, 100)
alpha = st.sidebar.slider("Attractor strength α", 0.1, 2.0, 1.0)
beta = st.sidebar.slider("Diffusion β", 0.01, 1.0, 0.25)
noise = st.sidebar.slider("Noise σ", 0.0, 0.5, 0.05)
energy_lr = st.sidebar.slider("Energy learning rate", 0.0001, 0.01, 0.001)

if st.sidebar.button("🚀 Run Neural PDE Simulation"):
    
    solver = NeuralPDESolver(
        n=grid_size,
        alpha=alpha,
        beta=beta,
        noise=noise,
        energy_lr=energy_lr
    )
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for step in range(steps):
        result = solver.step()
        progress_bar.progress((step + 1) / steps)
        
        if (step + 1) % 20 == 0:
            status_text.write(f"Step {step+1}/{steps} | Energy: {result['energy']:.4f} | Phase: {result['phase']}")
    
    # Final density field
    rho = solver.rho
    n = solver.n
    z_data = [[rho[i][j] for j in range(n)] for i in range(n)]
    
    fig = go.Figure(data=go.Heatmap(z=z_data, colorscale="Viridis", zmin=0, zmax=1))
    fig.update_layout(title="Final Swarm Density Field (v4.0)", width=700, height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Metrics
    st.subheader("📉 System Evolution")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(y=solver.history['energy'], name="Energy E(ρ)", line=dict(color="#FFA500")))
    fig2.add_trace(go.Scatter(y=solver.history['order_parameter'], name="Order Parameter", line=dict(color="#8B0000")))
    fig2.update_layout(title="Energy & Order Parameter Evolution", xaxis_title="Step")
    st.plotly_chart(fig2, use_container_width=True)
    
    # Phase analysis
    st.subheader("🔬 Phase Transition Analysis")
    phase_report = solver.get_phase_report()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Phase", phase_report.get('current_phase', 'N/A'))
    with col2:
        st.metric("Order Parameter", f"{phase_report.get('current_order_parameter', 0):.4f}")
    with col3:
        st.metric("Phase Transition", "Detected" if phase_report.get('phase_transition_detected') else "Not Detected")
    
    # Energy field visualization
    W = solver.energy_field.get_parameter_field()
    w_data = [[W[i][j] for j in range(n)] for i in range(n)]
    
    fig3 = go.Figure(data=go.Heatmap(z=w_data, colorscale="RdBu", zmin=-0.5, zmax=0.5))
    fig3.update_layout(title="Learned Energy Parameter Field W(x,y)", width=700, height=600)
    st.plotly_chart(fig3, use_container_width=True)
    
    st.success("✅ SWARMICA v4.0 Simulation Complete!")
    st.balloons()

st.markdown("""
---
## ⚙️ SWARMICA v4.0 — What Changed?

### 🧠 1. Learnable Physics
Energy is now parameterized: **E_θ(ρ) = Σ(W·ρ²) + Σ((ρ - goal)²)**
- W evolves over time
- System adapts its own dynamics

### 🌊 2. Reaction-Diffusion + Control Hybrid
Combines: diffusion smoothing + attractor forcing + learned deformation

### 🔬 3. Phase Transition Tracking
Order parameter detects: disorder → structure emergence, clustering transitions

---

## 🧬 System Class

**Neural Controlled Reaction-Diffusion System with Adaptive Energy Landscape**

---
*SWARMICA v4.0 — Physics Becomes Learnable* 🧠
""")
