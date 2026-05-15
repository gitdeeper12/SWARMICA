# SWARMICA v12.0 — Constrained Neural Physics Discovery System
# Hamiltonian + Conservation Law Learning

import streamlit as st
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.solver.constrained_solver import ConstrainedNeuralSolver

st.set_page_config(page_title="SWARMICA v12.0", layout="wide")
st.title("🔬 SWARMICA v12.0 — Constrained Neural Physics Discovery")
st.markdown("*Hamiltonian Dynamics | Mass Conservation | Symplectic Structure*")

# Sidebar controls
st.sidebar.header("⚙️ Constrained Physics Parameters")

grid_size = st.sidebar.slider("Grid resolution (N x N)", 40, 100, 64)
steps = st.sidebar.slider("Simulation steps", 100, 400, 200)
learning = st.sidebar.checkbox("Learn Hamiltonian", value=True)

if st.sidebar.button("🚀 Run Constrained Physics Simulation"):
    
    solver = ConstrainedNeuralSolver(N=grid_size, learning=learning)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for step in range(steps):
        result = solver.step()
        progress_bar.progress((step + 1) / steps)
        
        if (step + 1) % 50 == 0:
            status_text.write(f"Step {step+1}/{steps} | Energy: {result['energy']:.4f} | Mass: {result['mass']:.4f}")
    
    # Final density field
    rho = solver.rho
    N = solver.N
    z_data = [[rho[i][j] for j in range(N)] for i in range(N)]
    
    fig = go.Figure(data=go.Heatmap(z=z_data, colorscale="Viridis", zmin=0, zmax=1))
    fig.update_layout(title="Final Constrained Density Field ρ(x,y)", width=700, height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Metrics
    st.subheader("📊 Constrained Physics Evolution")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(y=solver.history['coherence'], name="Coherence", line=dict(color="#8B0000", width=2)))
    fig2.add_trace(go.Scatter(y=solver.history['energy'], name="Hamiltonian H", line=dict(color="#FFA500", width=2)))
    fig2.add_trace(go.Scatter(y=solver.history['mass'], name="Mass (conserved)", line=dict(color="#00CED1", width=2)))
    
    fig2.update_layout(title="Constrained Physics Evolution", xaxis_title="Step", plot_bgcolor="#0d0d0d", paper_bgcolor="#050505")
    st.plotly_chart(fig2, use_container_width=True)
    
    # Conservation report
    st.subheader("📜 Conservation Law Verification")
    cons_report = solver.get_conservation_report()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mass Conserved", "✅ Yes" if cons_report['mass_conserved'] else "❌ No")
    with col2:
        st.metric("Energy Variation", f"{cons_report['energy_variation']:.6f}")
    with col3:
        st.metric("Symplectic Structure", cons_report['symplectic_structure'])
    
    st.success("✅ SWARMICA v12.0 Constrained Physics Complete!")
    st.balloons()

st.markdown("""
---
## ⚙️ SWARMICA v12.0 — What Changed?

### 🧠 1. Hamiltonian Dynamics
- Learns energy Hθ(ρ, v)
- Preserves symplectic structure

### 🔬 2. Conservation Laws
- **Mass conservation**: ∫ρ dx = constant
- **Symplectic structure**: J ∇H flow
- **Entropy constraint**: dS/dt ≥ 0

### 📐 Mathematical Formulation
```

∂u/∂t = J ∇Hθ(u)
∫ρ dx = constant
dS/dt ≥ 0

```

### 🧬 System Class
**Hamiltonian Neural Networks | Symplectic Learning Systems**
**Scientific ML with Constraints | Conservation Law Discovery**

---
*SWARMICA v12.0 — Learning Physically Valid Universes* 🔬
""")
