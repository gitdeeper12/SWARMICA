# SWARMICA v2.0 — Streamlit Interface
# Pure Python (No NumPy) - Vector Field Swarm Physics

import streamlit as st
import plotly.graph_objects as go
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.control.swarm_controller import SwarmControllerV2

# Page config
st.set_page_config(
    page_title="SWARMICA v2.0 — Vector Field Swarm Physics",
    page_icon="🌊",
    layout="wide"
)

st.title("🌊 SWARMICA v2.0 — Vector Field Swarm Physics")
st.markdown("*Stochastic Continuum Dynamics + Multi-Attractor System + Real-time Metrics*")

# Sidebar controls
st.sidebar.header("⚙️ Control Parameters")

n_agents = st.sidebar.slider("Number of agents", 10, 300, 80)
steps = st.sidebar.slider("Simulation steps", 50, 500, 200)
alpha = st.sidebar.slider("Cohesion strength (α)", 0.1, 2.0, 0.8)
beta = st.sidebar.slider("Attractor strength (β)", 0.1, 3.0, 1.2)
noise = st.sidebar.slider("Stochastic noise (η)", 0.0, 1.0, 0.25)
inertia = st.sidebar.slider("Velocity inertia", 0.5, 0.98, 0.85)

if st.sidebar.button("🚀 Run Simulation"):
    
    # Create controller
    controller = SwarmControllerV2(
        n_agents=n_agents,
        alpha=alpha,
        beta=beta,
        noise=noise,
        inertia=inertia
    )
    
    # Run simulation
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for step in range(steps):
        result = controller.step()
        progress_bar.progress((step + 1) / steps)
        status_text.write(f"Step {step+1}/{steps} | CSI: {result['csi']:.4f}")
    
    # Extract data
    positions = controller.positions
    history_csi = controller.history['csi']
    history_entropy = controller.history['entropy']
    history_lyap = controller.history['lyapunov']
    
    # Final visualization
    st.subheader("🐝 Final Swarm Field State")
    
    # Extract positions for plotting
    pos_x = [p[0] for p in positions]
    pos_y = [p[1] for p in positions]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=pos_x, y=pos_y,
        mode="markers",
        marker=dict(size=8, color="#8B0000", opacity=0.7),
        name="Agents"
    ))
    
    fig.add_trace(go.Scatter(
        x=[controller.A1[0], controller.A2[0]],
        y=[controller.A1[1], controller.A2[1]],
        mode="markers",
        marker=dict(size=18, color="#FF4444", symbol="star", line=dict(width=2, color="white")),
        name="Attractors"
    ))
    
    fig.update_layout(
        title="Swarm Field State (v2.0)",
        xaxis_title="X Position",
        yaxis_title="Y Position",
        xaxis_range=[0, controller.grid_size],
        yaxis_range=[0, controller.grid_size],
        width=800,
        height=600,
        plot_bgcolor="#0d0d0d",
        paper_bgcolor="#050505",
        font=dict(color="#F5F0F0")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Metrics plots
    st.subheader("📊 System Metrics Evolution")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(y=history_entropy, name="Entropy", line=dict(color="#FFA500", width=2)))
    fig2.add_trace(go.Scatter(y=history_csi, name="CSI", line=dict(color="#8B0000", width=2)))
    fig2.add_trace(go.Scatter(y=history_lyap, name="Lyapunov", line=dict(color="#00CED1", width=2)))
    
    fig2.update_layout(
        title="Metric Evolution Over Time",
        xaxis_title="Simulation Step",
        yaxis_title="Value",
        plot_bgcolor="#0d0d0d",
        paper_bgcolor="#050505",
        font=dict(color="#F5F0F0")
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Summary
    st.subheader("📈 Final Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Final CSI", f"{history_csi[-1]:.4f}")
    with col2:
        st.metric("Final Entropy", f"{history_entropy[-1]:.4f}")
    with col3:
        st.metric("CSI Improvement", f"{(history_csi[-1] - history_csi[0])*100:.1f}%")
    
    st.success("✅ SWARMICA v2.0 Simulation Complete!")
    st.balloons()

# Documentation
st.markdown("""
---
## 📊 SWARMICA v2.0

**System Type:** Nonlinear Vector Field Multi-Attractor System

**Key Metrics:**
- **CSI**: Collective Stability Index (0-1, higher = more stable)
- **Entropy**: Spatial disorder (lower = more organized)
- **Lyapunov**: Kinetic energy measure (lower = more stable)

**Mathematical Framework:**
```

F_total = α·(cohesion) + β·(A₁ + A₂) + η·dW
v(t+1) = γ·v(t) + F_total
x(t+1) = x(t) + dt·v(t+1)

```
""")
