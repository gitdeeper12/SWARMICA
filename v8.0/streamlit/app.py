# SWARMICA v8.0 — Unified Field Control Engine
# Agent-based Continuum Approximation

import streamlit as st
import plotly.graph_objects as go
import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.core.engine import SwarmicaV8

st.set_page_config(page_title="SWARMICA v8.0", layout="wide")
st.title("⚙️ SWARMICA v8.0 — Unified Field Control Engine")
st.markdown("*Vector Field Swarm + Multi-Attractor + Lyapunov Monitor*")

# Sidebar controls
st.sidebar.header("⚙️ Control Parameters")

n_agents = st.sidebar.slider("Number of agents", 50, 500, 200)
steps = st.sidebar.slider("Simulation steps", 100, 1000, 500)
alpha = st.sidebar.slider("Cohesion strength α", 0.5, 3.0, 1.2)
beta = st.sidebar.slider("Attractor strength β", 0.5, 4.0, 2.0)
gamma = st.sidebar.slider("Damping γ", 0.1, 1.0, 0.5)
sigma = st.sidebar.slider("Noise σ", 0.0, 0.5, 0.1)

if st.sidebar.button("🚀 Run Simulation"):
    
    sim = SwarmicaV8(
        n_agents=n_agents,
        alpha=alpha,
        beta=beta,
        gamma=gamma,
        sigma=sigma,
        dt=0.01
    )
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for step in range(steps):
        result = sim.step()
        progress_bar.progress((step + 1) / steps)
        
        if (step + 1) % 100 == 0:
            status_text.write(f"Step {step+1}/{steps} | CSI: {result['csi']:.4f} | Entropy: {result['entropy']:.4f}")
    
    # Final positions visualization
    positions = sim.positions
    pos_x = [p[0] for p in positions]
    pos_y = [p[1] for p in positions]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=pos_x, y=pos_y,
        mode="markers",
        marker=dict(size=8, color="#8B0000", opacity=0.7),
        name="Agents"
    ))
    
    # Attractors
    att_x = [a[0] for a in sim.attractors]
    att_y = [a[1] for a in sim.attractors]
    
    fig.add_trace(go.Scatter(
        x=att_x, y=att_y,
        mode="markers",
        marker=dict(size=18, color="#FF4444", symbol="star", line=dict(width=2, color="white")),
        name="Attractors"
    ))
    
    fig.update_layout(
        title=f"Swarm Field State - Final (N={n_agents})",
        xaxis_title="X",
        yaxis_title="Y",
        width=700, height=600,
        plot_bgcolor="#0d0d0d",
        paper_bgcolor="#050505"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Metrics
    st.subheader("📊 System Metrics Evolution")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(y=sim.history['csi'], name="CSI", line=dict(color="#8B0000", width=2)))
    fig2.add_trace(go.Scatter(y=sim.history['entropy'], name="Entropy", line=dict(color="#FFA500", width=2)))
    fig2.add_trace(go.Scatter(y=sim.history['lyapunov'], name="Lyapunov", line=dict(color="#00CED1", width=2)))
    
    fig2.update_layout(
        title="Metric Evolution Over Time",
        xaxis_title="Step",
        yaxis_title="Value",
        plot_bgcolor="#0d0d0d",
        paper_bgcolor="#050505"
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Summary
    summary = sim.get_summary()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Final CSI", f"{summary['final_csi']:.4f}", 
                  delta=f"{summary['csi_improvement']:.1f}%")
    with col2:
        st.metric("Final Entropy", f"{summary['final_entropy']:.4f}",
                  delta=f"-{summary['entropy_reduction']:.1f}%")
    with col3:
        st.metric("Final Lyapunov", f"{summary['final_lyapunov']:.4f}")
    
    st.success("✅ SWARMICA v8.0 Simulation Complete!")
    st.balloons()

st.markdown("""
---
## ⚙️ SWARMICA v8.0 — What Changed?

### 🧠 1. Unified Field Control
- Vector field swarm dynamics
- Multi-attractor potential field

### 🌊 2. Complete Metrics Suite
- **CSI**: Collective Stability Index (0-1)
- **Entropy**: Structural disorder
- **Lyapunov**: Kinetic energy monitor

### 🎯 3. Multi-Attractor System
- Competing attractors (2 points)
- Adaptive field forces

### 📐 Mathematical Framework
```

F_total = α·cohesion + β·(A₁ + A₂) - γ·v + σ·dW
v(t+1) = v(t) + F_total·dt
x(t+1) = x(t) + v(t+1)·dt

```

---
## 🧬 System Class

**Agent-based Continuum Approximation with Multi-Potential Energy Field**

*SWARMICA v8.0 — Unified Field Control Engine* ⚙️
""")
