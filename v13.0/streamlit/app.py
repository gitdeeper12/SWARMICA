# SWARMICA v13.0 — Autonomous Physical Law Discovery System
# Symbolic PDE Discovery + Neural Field Inference

import streamlit as st
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from swarmica.core.discovery_engine import DiscoveryEngine

st.set_page_config(page_title="SWARMICA v13.0", layout="wide")
st.title("🔬 SWARMICA v13.0 — Autonomous Physical Law Discovery")
st.markdown("*Symbolic PDE Discovery | Sparse Identification of Nonlinear Dynamics*")

# Sidebar controls
st.sidebar.header("⚙️ Discovery Parameters")

grid_size = st.sidebar.slider("Grid resolution (N x N)", 40, 80, 64)
alpha = st.sidebar.slider("Sparsity parameter α", 0.0001, 0.01, 0.001)
iterations = st.sidebar.slider("Discovery iterations", 1, 10, 3)

if st.sidebar.button("🚀 Discover Physical Law"):
    
    engine = DiscoveryEngine(N=grid_size, alpha=alpha)
    
    st.subheader("📡 Observing Field Dynamics...")
    
    progress_bar = st.progress(0)
    
    results = engine.run_discovery(iterations=iterations)
    best_pde = engine.get_best_pde(results)
    
    progress_bar.progress(1.0)
    
    # Display discovered PDE
    st.subheader("📜 Discovered Physical Law")
    st.markdown(f"```\n{best_pde.get('discovered_pde', 'No PDE discovered')}\n```")
    
    # Display coefficients
    st.subheader("📊 Discovered Coefficients")
    coeffs = best_pde.get('coefficients', {})
    if coeffs:
        coeff_data = {"Term": [], "Coefficient": []}
        for term, coeff in coeffs.items():
            coeff_data["Term"].append(term)
            coeff_data["Coefficient"].append(f"{coeff:.4f}")
        st.dataframe(coeff_data)
    else:
        st.write("No significant coefficients discovered")
    
    # Verification
    st.subheader("✅ Physics Verification")
    ver = best_pde.get('verification', {})
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Diffusion Term", "✓ Present" if ver.get('has_diffusion') else "✗ Absent")
    with col2:
        st.metric("Advection Term", "✓ Present" if ver.get('has_advection') else "✗ Absent")
    with col3:
        st.metric("PDE Complexity", f"{best_pde.get('num_terms', 0)} terms")
    
    if ver.get('warnings'):
        st.warning(f"⚠️ {', '.join(ver['warnings'])}")
    else:
        st.success("✅ Discovered PDE satisfies physical constraints")
    
    st.balloons()

st.markdown("""
---
## ⚙️ SWARMICA v13.0 — What Changed?

### 🧠 1. Symbolic PDE Discovery
- Builds library of candidate terms
- Sparse regression selects relevant terms
- Discovers governing equations from data

### 🔬 2. Sparse Identification (SINDy)
```

∂u/∂t = Θ(u)·ξ
min ||y - Θξ||² + α||ξ||₁

```

### 📐 3. Term Library
- u, u², ∂u/∂x, ∂u/∂y, ∇²u, u·∂u/∂x, u·∂u/∂y, sin(u)

### 🧬 System Class
**PDE Discovery | Symbolic AI for Physics**
**Sparse Dynamical Systems Identification**

---
*SWARMICA v13.0 — Discovering Physical Laws from Data* 🔬
""")
