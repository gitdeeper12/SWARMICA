"""Bifurcation detection for SWARMICA v2.0"""

import math
from typing import List, Tuple
from dataclasses import dataclass, field


@dataclass
class BifurcationDetector:
    """Detect phase transitions and bifurcation points"""
    
    history_size: int = 100
    _entropy_history: List[float] = field(default_factory=list)
    _csi_history: List[float] = field(default_factory=list)
    
    def update(self, entropy: float, csi: float):
        """Update history with new values"""
        self._entropy_history.append(entropy)
        self._csi_history.append(csi)
        
        if len(self._entropy_history) > self.history_size:
            self._entropy_history.pop(0)
            self._csi_history.pop(0)
    
    def bifurcation_index(self) -> float:
        """Detect phase transitions via entropy and CSI derivatives"""
        if len(self._entropy_history) < 3 or len(self._csi_history) < 3:
            return 0.0
        
        d_entropy = abs(self._entropy_history[-1] - self._entropy_history[-2])
        d_csi = abs(self._csi_history[-1] - self._csi_history[-2])
        
        return d_entropy * d_csi
    
    def is_phase_transition(self, threshold: float = 0.01) -> bool:
        """Check if system is undergoing phase transition"""
        return self.bifurcation_index() > threshold
    
    def get_stability_region(self) -> str:
        """Classify current stability region"""
        if len(self._csi_history) < 10:
            return "Unknown"
        
        recent_csi = self._csi_history[-10:]
        mean_csi = sum(recent_csi) / len(recent_csi)
        csi_variance = sum((c - mean_csi) ** 2 for c in recent_csi) / len(recent_csi)
        
        if mean_csi > 0.9 and csi_variance < 0.01:
            return "Stable (Attractor Basin)"
        elif mean_csi > 0.7:
            return "Converging"
        elif mean_csi > 0.5:
            return "Transitional"
        else:
            return "Chaotic/Unstable"
    
    def reset(self):
        """Reset history"""
        self._entropy_history = []
        self._csi_history = []


def create_bifurcation_detector() -> BifurcationDetector:
    """Factory function for bifurcation detector"""
    return BifurcationDetector()
