"""Collective Stability Index (CSI) Monitor"""

import math
from dataclasses import dataclass
from typing import List


@dataclass
class CSIMonitor:
    """Monitors Collective Stability Index over time"""
    
    history: List[float] = None
    
    def __post_init__(self):
        self.history = []
    
    def update(self, csi: float):
        self.history.append(csi)
    
    @property
    def current(self) -> float:
        return self.history[-1] if self.history else 0.0
    
    @property
    def mean(self) -> float:
        if not self.history:
            return 0.0
        return sum(self.history) / len(self.history)
    
    @property
    def variance(self) -> float:
        if len(self.history) < 2:
            return 0.0
        m = self.mean
        return sum((v - m) ** 2 for v in self.history) / len(self.history)
    
    def reset(self):
        self.history = []
