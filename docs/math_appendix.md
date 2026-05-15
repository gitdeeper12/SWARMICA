# Mathematical Appendix

## Core Equations

### 1. Physical Coupling Manifold
$$p(t) = (\rho(x,t), v(x,t)) \in M$$

### 2. Collective Lagrangian
$$L[Q, \dot{Q}] = T[\dot{Q}] - V_{\text{eff}}[Q]$$

### 3. Euler-Lagrange Field Equations
$$G(Q)\ddot{Q} + C(Q,\dot{Q})\dot{Q} + \nabla_Q V_{\text{eff}}(Q) = F_{\text{ctrl}}$$

### 4. SOS Potential Field
$$V_{\text{eff}}(Q) = p(Q)^T P p(Q) + \alpha \|Q - Q^*\|^2_G$$

### 5. Kuramoto Phase Dynamics
$$\frac{d\theta_i}{dt} = \omega_i + \frac{K}{N} \sum_j \sin(\theta_j - \theta_i) + F_{\text{ext},i}$$

### 6. Critical Coupling
$$K_c = 2\Delta, \quad r_{\infty} = \sqrt{1 - \frac{K_c}{K}}$$

### 7. Stability Certificate
$$\text{Re}(\lambda_i) < -\sigma_{\min} < 0$$

### 8. Convergence Bound
$$\|Q(t) - Q^*\| \leq C e^{-\sigma_{\min} t} \|Q(0) - Q^*\|$$
