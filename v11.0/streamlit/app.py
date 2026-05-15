# SWARMICA v11.0 — Neural Operator Swarm Physics
# Scientific-grade Neural Field System

import streamlit as st
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.integrator.solver import NeuralOperatorSolver

st.set_page_config(page_title="SWARMICA v11.0", layout="wide")
st.title("🧠 SWARMICA v11.0 — Neural Operator Swarm Physics")
st.markdown("*Learning the Laws of Collective Motion | Scientific-grade Neural Field System*")

# Sidebar controls
st.sidebar.header("⚙️ Neural Operator Parameters")

grid_size = st.sidebar.slider("Grid resolution (N x N)", 40, 100, 64)
steps = st.sidebar.slider("Simulation steps", 100, 500, 250)
learning = st.sidebar.checkbox("Enable Operator Learning", value=True)

if st.sidebar.button("🚀 Run Neural Operator Simulation"):
    
    solver = NeuralOperatorSolver(N=grid_size, learning=learning)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for step in range(steps):
        result = solver.step()
        progress_bar.progress((step + 1) / steps)
        
        if (step + 1) % 50 == 0:
            status_text.write(f"Step {step+1}/{steps} | Coherence: {result['coherence']:.4f} | Loss: {result['operator_loss']:.4f}")
    
    # Final density field
    rho = solver.rho
    N = solver.N
    z_data = [[rho[i][j] for j in range(N)] for i in range(N)]
    
    fig = go.Figure(data=go.Heatmap(z=z_data, colorscale="Viridis", zmin=0, zmax=1))
    fig.update_layout(title="Final Learned Density Field ρ(x,y)", width=700, height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Metrics
    st.subheader("📊 Neural Operator Evolution")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(y=solver.history['coherence'], name="Coherence", line=dict(color="#8B0000", width=2)))
    fig2.add_trace(go.Scatter(y=solver.history['entropy'], name="Entropy", line=dict(color="#FFA500", width=2)))
    fig2.add_trace(go.Scatter(y=solver.history['energy'], name="Energy", line=dict(color="#00CED1", width=2)))
    
    if solver.history['operator_loss']:
        fig2.add_trace(go.Scatter(y=solver.history['operator_loss'], name="Operator Loss", line=dict(color="#FFFFFF", dash="dash")))
    
    fig2.update_layout(title="Learned Physics Evolution", xaxis_title="Step", plot_bgcolor="#0d0d0d", paper_bgcolor="#050505")
    st.plotly_chart(fig2, use_container_width=True)
    
    # Operator info
    op_info = solver.get_operator_info()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Final Coherence", f"{solver.history['coherence'][-1]:.4f}")
    with col2:
        st.metric("Operator Norm", f"{op_info['operator_norm']:.4f}")
    with col3:
        st.metric("Learning Active", "Yes" if learning else "No")
    
    st.success("✅ SWARMICA v11.0 Neural Operator Simulation Complete!")
    st.balloons()

st.markdown("""
---
## ⚙️ SWARMICA v11.0 — What Changed?

### 🧠 1. Neural Operator Learning
**Fθ: (ρ, v) → (∂ρ/∂t, ∂v/∂t)**
- Learns the complete physics operator
- No predefined PDE equations

### 🔬 2. Spectral Layer
- Fourier-like transforms for global interactions
- Captures wave-number dynamics

### 📉 3. Operator Discovery
The system learns:
- How density should evolve
- How velocity fields change
- The physical law itself

---

## 🧬 System Class

**Neural Operators (DeepONet / FNO)**
**Scientific Machine Learning (SciML)**
**Data-driven PDE discovery**

---

## 🔑 The Critical Shift

| v10.0 | v11.0 |
|-------|-------|
| Learns energy | **Learns the operator** |
| Eθ(ρ) | **Fθ(ρ, v)** |
| Physics proxy | **Physics itself** |

---
*SWARMICA v11.0 — The Machine Learns the Laws of Physics* 🧠
""")
