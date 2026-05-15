# API Reference

## SwarmEngine

Main controller class for swarm dynamics.

### Methods

- `step(dt, obs)`: Execute one control step
- `get_csi()`: Get Collective Stability Index
- `get_structural_entropy()`: Get S_struct
- `get_eri()`: Get Entropy Reduction Index

## SwarmConfig

Configuration dataclass.

### Parameters

- `n_agents`: Number of agents (default: 500)
- `modality`: 'aerial', 'ground', 'underwater', 'mixed'
- `n_basis`: Basis dimension (default: 64)
- `k_coupling`: Kuramoto coupling (default: 3.0)
- `mu_dissipation`: Drag coefficient (default: 0.02)
