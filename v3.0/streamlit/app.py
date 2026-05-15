# SWARMICA v3.0 — PDE Swarm Physics Engine
# Pure Python (No NumPy) - Reaction-Diffusion System

import streamlit as st
import plotly.graph_objects as go
import sys
import os
import math

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.pde.solver import PDESolver

# Page config
st.set_page_config(
    page_title="SWARMICA v3.0 — PDE Swarm Physics Engine",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 SWARMICA v3.0 — PDE Swarm Physics Engine")
st.markdown("*Nonlinear Stochastic Reaction-Diffusion System | Active Matter Physics*")

# Sidebar controls
st.sidebar.header("⚙️ PDE Parameters")

grid_size = st.sidebar.slider("Grid resolution (N x N)", 20, 100, 60)
steps = st.sidebar.slider("Simulation steps", 20, 300, 100)
alpha = st.sidebar.slider("Attraction strength α", 0.1, 2.5, 1.0)
beta = st.sidebar.slider("Diffusion coefficient β", 0.01, 1.0, 0.2)
noise = st.sidebar.slider("Stochastic noise σ", 0.0, 0.5, 0.05)

if st.sidebar.button("🚀 Run PDE Simulation"):
    
    # Create solver
    solver = PDESolver(
        n=grid_size,
        alpha=alpha,
        beta=beta,
        noise=noise,
        dt=0.1
    )
    
    # Run simulation
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for step in range(steps):
        result = solver.step()
        progress_bar.progress((step + 1) / steps)
        
        if (step + 1) % 20 == 0:
            status_text.write(f"Step {step+1}/{steps} | Energy: {result['energy']:.4f}")
    
    status_text.write("✅ Simulation complete!")
    
    # Create heatmap for visualization
    rho = solver.rho
    n = solver.n
    
    # Convert to list for plotting
    z_data = [[rho[i][j] for j in range(n)] for i in range(n)]
    
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        colorscale="Viridis",
        zmin=0, zmax=1,
        colorbar=dict(title="Density ρ")
    ))
    
    fig.update_layout(
        title="Final Swarm Density Field (v3.0)",
        xaxis_title="X",
        yaxis_title="Y",
        width=700,
        height=600,
        plot_bgcolor="#0d0d0d",
        paper_bgcolor="#050505"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Energy evolution
    st.subheader("📉 System Energy Evolution")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        y=solver.history['energy'],
        mode="lines",
        name="Energy Functional E(ρ)",
        line=dict(color="#FFA500", width=2)
    ))
    
    fig2.update_layout(
        title="Energy Minimization Over Time",
        xaxis_title="Simulation Step",
        yaxis_title="Energy",
        plot_bgcolor="#0d0d0d",
        paper_bgcolor="#050505"
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Final Energy", f"{solver.history['energy'][-1]:.4f}")
    with col2:
        st.metric("Initial Energy", f"{solver.history['energy'][0]:.4f}")
    with col3:
        reduction = (solver.history['energy'][0] - solver.history['energy'][-1]) / solver.history['energy'][0] * 100
        st.metric("Energy Reduction", f"{reduction:.1f}%")
    
    st.success("✅ SWARMICA v3.0 Simulation Complete!")
    st.balloons()

# Documentation
st.markdown("""
---
## ⚙️ SWARMICA v3.0 — What Changed?

### 🔬 1. From Agents → Fields
We no longer simulate particles. We solve a **density PDE**.

### 📉 2. Energy Functional
System evolves by minimizing:
- internal disorder (ρ²)
- distance from goal field

### 🌊 3. Diffusion Physics
Laplacian term introduces:
- smoothing
- stability
- physical continuity

### 🎯 4. Multi-Attractor Field
Goal is no longer a point → it's a **field structure**

---

## 🧠 System Class

**Nonlinear Stochastic Reaction-Diffusion System**  
(Active Matter Physics Approximation)

### PDE Formulation:
```

∂ρ/∂t = -∇·(ρV) + D∇²ρ + α(G - ρ) + σ·dW

```

Where:
- ρ = density field
- V = velocity field
- D = diffusion coefficient
- G = goal field (multi-attractor)
- σ = noise strength
- dW = Wiener process

---

## 🚀 Next: SWARMICA v4.0

Planned features:
- Finite Element Method (FEM solver)
- Learnable energy functional (Neural PDE)
- Bifurcation & phase transition detection
- Real robotics swarm deployment

---
*SWARMICA v3.0 — From Heuristics to Physics* 🧠
""")
