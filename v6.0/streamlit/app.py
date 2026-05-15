# SWARMICA v6.0 — Optimal Control + Neural PDE Engine
# Pontryagin Maximum Principle + Neural Operator

import streamlit as st
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.control.optimal_swarm_controller import OptimalSwarmController

st.set_page_config(page_title="SWARMICA v6.0", layout="wide")
st.title("🎯 SWARMICA v6.0 — Optimal Control + Neural PDE Engine")
st.markdown("*Pontryagin Maximum Principle | Neural Operator | Adjoint-Based Learning*")

# Sidebar controls
st.sidebar.header("⚙️ Optimal Control Parameters")

grid_size = st.sidebar.slider("Grid resolution (N x N)", 50, 120, 90)
steps = st.sidebar.slider("Simulation steps", 50, 300, 140)
alpha = st.sidebar.slider("Drift strength α", 0.5, 2.0, 1.0)
beta = st.sidebar.slider("Diffusion β", 0.1, 1.0, 0.25)
sigma = st.sidebar.slider("Noise σ", 0.0, 0.5, 0.1)
control_weight = st.sidebar.slider("Control penalty λ", 0.1, 3.0, 0.8)
adjoint_lr = st.sidebar.slider("Adjoint learning rate", 0.0005, 0.01, 0.002)

if st.sidebar.button("🚀 Run Optimal Control Simulation"):
    
    controller = OptimalSwarmController(
        n=grid_size,
        alpha=alpha,
        beta=beta,
        sigma=sigma,
        control_weight=control_weight,
        adjoint_lr=adjoint_lr
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
    fig.update_layout(title="Final Swarm Field (v6.0)", width=700, height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Costate field (adjoint)
    costate = controller.pmp.get_costate()
    c_data = [[costate[i][j] for j in range(n)] for i in range(n)]
    
    fig_c = go.Figure(data=go.Heatmap(z=c_data, colorscale="RdBu", zmin=-0.5, zmax=0.5))
    fig_c.update_layout(title="Costate Field p(x,y) (Adjoint Variable)", width=700, height=600)
    st.plotly_chart(fig_c, use_container_width=True)
    
    # Metrics
    st.subheader("📉 PMP Optimization Dynamics")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(y=controller.history['energy'], name="Energy E(ρ)", line=dict(color="#FFA500")))
    fig2.add_trace(go.Scatter(y=controller.history['control_effort'], name="Control Effort ∫‖u‖²", line=dict(color="#8B0000")))
    fig2.add_trace(go.Scatter(y=controller.history['total_cost'], name="Total Cost J", line=dict(color="#FFFFFF", dash="dash")))
    fig2.update_layout(title="Optimal Control Evolution", xaxis_title="Step")
    st.plotly_chart(fig2, use_container_width=True)
    
    # Final metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Final Energy", f"{controller.history['energy'][-1]:.4f}")
    with col2:
        st.metric("Control Effort", f"{controller.history['control_effort'][-1]:.4f}")
    with col3:
        reduction = (controller.history['total_cost'][0] - controller.history['total_cost'][-1]) / controller.history['total_cost'][0] * 100
        st.metric("Cost Reduction", f"{reduction:.1f}%")
    
    st.success("✅ SWARMICA v6.0 Simulation Complete!")
    st.balloons()

st.markdown("""
---
## ⚙️ SWARMICA v6.0 — What Changed?

### 🧠 1. Pontryagin Maximum Principle (PMP)
- **State variable**: ρ (density field)
- **Costate variable**: p (adjoint)
- **Optimal control**: u* = -(1/λ) p

### 🌊 2. Neural PDE Operator
- Learns internal dynamics: **Fθ(ρ) = W·ρ + tanh(ρ)**
- Parameters updated via adjoint feedback

### 📉 3. Forward-Backward Coupling
- Forward: PDE evolution for ρ
- Backward: Adjoint dynamics for p
- Optimality: Hamiltonian minimization

### 📐 Mathematical Formulation
```

min_u ∫(E(ρ) + λ‖u‖²) dt
∂ρ/∂t = α·Fθ(ρ) - ∇ρ + β∇²ρ + u + σ·dW
u* = -(1/λ) p  [PMP optimal control]
∂p/∂t = -∂H/∂ρ  [Adjoint equation]

```

---
## 🧬 System Class

**Stochastic Neural Optimal Control PDE System with Adjoint-Based Variational Learning**

---
*SWARMICA v6.0 — Rigorous Optimal Control Theory* 🎯
""")
