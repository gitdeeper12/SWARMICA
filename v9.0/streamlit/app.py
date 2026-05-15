# SWARMICA v9.0 — Continuum PDE + Energy Learning Swarm System
# Research-Grade Continuous Field Dynamics

import streamlit as st
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.pde.solver import ContinuumPDESolver

st.set_page_config(page_title="SWARMICA v9.0", layout="wide")
st.title("🔬 SWARMICA v9.0 — Continuum PDE Swarm System")
st.markdown("*Research-Grade Continuous Field Dynamics | Active Matter Physics*")

# Sidebar controls
st.sidebar.header("⚙️ PDE Parameters")

grid_size = st.sidebar.slider("Grid resolution (N x N)", 50, 150, 100)
steps = st.sidebar.slider("Simulation steps", 100, 500, 300)
alpha = st.sidebar.slider("Gradient energy α", 0.5, 2.0, 1.0)
gamma = st.sidebar.slider("Damping γ", 0.1, 0.8, 0.3)
nu = st.sidebar.slider("Viscosity ν", 0.05, 0.5, 0.2)

if st.sidebar.button("🚀 Run PDE Simulation"):
    
    solver = ContinuumPDESolver(N=grid_size, alpha=alpha, gamma=gamma, nu=nu, dt=0.01)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for step in range(steps):
        result = solver.step()
        progress_bar.progress((step + 1) / steps)
        
        if (step + 1) % 50 == 0:
            status_text.write(f"Step {step+1}/{steps} | Coherence: {result['coherence']:.4f} | Entropy: {result['entropy']:.4f}")
    
    # Final density field
    rho = solver.rho
    N = solver.N
    z_data = [[rho[i][j] for j in range(N)] for i in range(N)]
    
    fig = go.Figure(data=go.Heatmap(z=z_data, colorscale="Viridis", zmin=0, zmax=1))
    fig.update_layout(title="Final Density Field ρ(x,y)", width=700, height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Metrics
    st.subheader("📊 System Metrics Evolution")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(y=solver.history['coherence'], name="Coherence Index", line=dict(color="#8B0000", width=2)))
    fig2.add_trace(go.Scatter(y=solver.history['entropy'], name="Entropy", line=dict(color="#FFA500", width=2)))
    fig2.add_trace(go.Scatter(y=solver.history['energy'], name="Energy E[ρ]", line=dict(color="#00CED1", width=2)))
    
    fig2.update_layout(
        title="PDE Evolution Metrics",
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
        st.metric("Final Energy", f"{solver.history['energy'][-1]:.4f}")
    
    st.success("✅ SWARMICA v9.0 PDE Simulation Complete!")
    st.balloons()

st.markdown("""
---
## ⚙️ SWARMICA v9.0 — Mathematical Framework

### Continuity Equation
```

∂ρ/∂t + ∇·(ρv) = 0

```

### Momentum Equation
```

∂v/∂t = -∇E[ρ] - γv + ν∇²v + u(x,t)

```

### Energy Functional
```

E[ρ] = ∫(α|∇ρ|² + V(ρ)) dx

```

---

## 🧬 System Class

**Computational Fluid Dynamics (CFD)**
**Active Matter Physics**
**Reaction-Diffusion Systems**

---

## 🔬 Key Differences from v8.0

| Feature | v8.0 | v9.0 |
|---------|------|------|
| Representation | Agents | **Continuous Field** |
| Dynamics | Discrete | **PDE-based** |
| Physics | Heuristic | **Fluid Dynamics** |
| Scale | N agents | **N² grid** |

---
*SWARMICA v9.0 — From Agents to Fields* 🔬
""")
