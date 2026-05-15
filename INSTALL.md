# 📦 Installation Guide for SWARMICA v1.0.0

## Quick Install (PyPI)

```bash
pip install swarmica-engine
```

Install from Source

```bash
git clone https://github.com/gitedeeper12/SWARMICA.git
cd SWARMICA
pip install -e .
```

Verify Installation

```python
from swarmica import SwarmEngine, SwarmConfig

print("SWARMICA v1.0.0 ready")

# Quick test
cfg = SwarmConfig(
    n_agents=100,
    modality='aerial',
    n_basis=32,
    k_coupling=3.0,
    mu_dissipation=0.02,
    target_config='diamond_V'
)
print(f"Config created: {cfg.target_config}")
```

```bash
python -c "from swarmica import __version__; print(__version__)"  # 1.0.0
```

Requirements

Package Version
Python ≥ 3.11
torch ≥ 2.4.0
jax ≥ 0.4.0
numpy ≥ 2.0.0
scipy ≥ 1.14.0
cvxpy ≥ 1.4.0

Platform Support

Platform Support
Linux ✅ Fully tested
macOS ✅ Compatible
Windows ✅ Compatible
Termux (Android) ✅ Compatible
NVIDIA Jetson Orin ✅ Supported
Xilinx Versal FPGA ✅ Supported (v2.0)

Docker Installation

```bash
docker pull gitedeeper12/swarmica:latest
docker run --rm swarmica --help
```

Uninstall

```bash
pip uninstall swarmica-engine
```

---

For issues, open a ticket on GitHub/GitLab.
