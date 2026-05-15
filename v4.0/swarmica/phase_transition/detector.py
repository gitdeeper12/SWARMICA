"""Phase transition detection for SWARMICA v4.0"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field


@dataclass
class PhaseTransitionDetector:
    """Detect phase transitions and critical points in swarm dynamics"""
    
    history_size: int = 100
    _order_history: List[float] = field(default_factory=list)
    _energy_history: List[float] = field(default_factory=list)
    
    def update(self, order_parameter: float, energy: float):
        """Update history with new values"""
        self._order_history.append(order_parameter)
        self._energy_history.append(energy)
        
        if len(self._order_history) > self.history_size:
            self._order_history.pop(0)
            self._energy_history.pop(0)
    
    def order_parameter(self, rho: List[List[float]]) -> float:
        """Compute order parameter: standard deviation of density field"""
        if not rho:
            return 0.0
        
        n = len(rho)
        values = [rho[i][j] for i in range(n) for j in range(n)]
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        
        return math.sqrt(variance)
    
    def susceptibility(self) -> float:
        """Compute susceptibility: variance of order parameter"""
        if len(self._order_history) < 10:
            return 0.0
        
        recent = self._order_history[-20:]
        mean = sum(recent) / len(recent)
        variance = sum((x - mean) ** 2 for x in recent) / len(recent)
        
        return variance
    
    def is_phase_transition(self, threshold: float = 0.05) -> bool:
        """Detect phase transition via order parameter jump"""
        if len(self._order_history) < 5:
            return False
        
        recent = self._order_history[-5:]
        max_jump = max(abs(recent[i] - recent[i-1]) for i in range(1, len(recent)))
        
        return max_jump > threshold
    
    def get_phase(self, order_param: float) -> str:
        """Classify current phase based on order parameter"""
        if order_param < 0.15:
            return "Disordered (Gas-like)"
        elif order_param < 0.35:
            return "Transitional (Liquid-like)"
        elif order_param < 0.55:
            return "Partially Ordered (Gel-like)"
        else:
            return "Ordered (Crystal-like)"
    
    def critical_temperature_estimate(self) -> float:
        """Estimate critical temperature from susceptibility peak"""
        if len(self._order_history) < 20:
            return 0.0
        
        # Find peak in order parameter variance
        susceptibilities = []
        for i in range(10, len(self._order_history)):
            window = self._order_history[i-10:i]
            mean = sum(window) / len(window)
            var = sum((x - mean) ** 2 for x in window) / len(window)
            susceptibilities.append(var)
        
        if susceptibilities:
            return max(susceptibilities)
        return 0.0
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate phase transition analysis report"""
        if len(self._order_history) < 10:
            return {'status': 'Insufficient data'}
        
        current_order = self._order_history[-1]
        current_phase = self.get_phase(current_order)
        
        return {
            'current_order_parameter': current_order,
            'current_phase': current_phase,
            'phase_transition_detected': self.is_phase_transition(),
            'susceptibility': self.susceptibility(),
            'critical_estimate': self.critical_temperature_estimate(),
            'order_history_length': len(self._order_history)
        }
    
    def reset(self):
        """Reset history"""
        self._order_history = []
        self._energy_history = []


def create_phase_transition_detector() -> PhaseTransitionDetector:
    """Factory function for phase transition detector"""
    return PhaseTransitionDetector()
