"""Formation controller for different swarm modalities"""

import math
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class FormationController:
    """Computes actuator commands for formation maintenance"""
    
    n_agents: int = 500
    modality: str = 'aerial'  # aerial, ground, underwater, mixed
    target_config: str = 'diamond_V'
    
    def compute_aerial_commands(self, positions: List[Tuple[float, float, float]],
                                 velocities: List[Tuple[float, float, float]],
                                 target_forces: List[Tuple[float, float, float]]) -> List[Dict]:
        """Compute quadrotor thrust and torque commands"""
        commands = []
        
        for i in range(min(self.n_agents, len(positions), len(target_forces))):
            cmd = {
                'agent_id': i,
                'thrust': target_forces[i][2] if len(target_forces[i]) > 2 else 0.0,  # z-thrust
                'roll': target_forces[i][0] * 0.1,   # roll moment
                'pitch': target_forces[i][1] * 0.1,  # pitch moment
                'yaw_rate': 0.0,
            }
            commands.append(cmd)
        
        return commands
    
    def compute_ground_commands(self, positions: List[Tuple[float, float, float]],
                                 velocities: List[Tuple[float, float, float]],
                                 target_forces: List[Tuple[float, float, float]]) -> List[Dict]:
        """Compute UGV velocity and steering commands"""
        commands = []
        
        for i in range(min(self.n_agents, len(positions), len(target_forces))):
            speed = math.sqrt(target_forces[i][0]**2 + target_forces[i][1]**2)
            steering = math.atan2(target_forces[i][1], target_forces[i][0]) if speed > 0 else 0.0
            
            cmd = {
                'agent_id': i,
                'linear_velocity': min(5.0, speed),
                'steering_angle': steering,
                'brake': 0.0,
            }
            commands.append(cmd)
        
        return commands
    
    def compute_underwater_commands(self, positions: List[Tuple[float, float, float]],
                                     velocities: List[Tuple[float, float, float]],
                                     target_forces: List[Tuple[float, float, float]]) -> List[Dict]:
        """Compute AUV thruster and fin commands"""
        commands = []
        
        for i in range(min(self.n_agents, len(positions), len(target_forces))):
            cmd = {
                'agent_id': i,
                'thruster': math.sqrt(target_forces[i][0]**2 + target_forces[i][1]**2 + target_forces[i][2]**2),
                'rudder': target_forces[i][1] * 0.05,   # yaw
                'elevator': target_forces[i][0] * 0.05, # pitch
                'ballast': target_forces[i][2] * 0.1,   # depth
            }
            commands.append(cmd)
        
        return commands
    
    def compute_mixed_commands(self, positions: List[Tuple[float, float, float]],
                                velocities: List[Tuple[float, float, float]],
                                target_forces: List[Tuple[float, float, float]],
                                agent_types: List[str]) -> List[Dict]:
        """Compute commands for heterogeneous swarm"""
        commands = []
        
        for i in range(min(self.n_agents, len(positions), len(target_forces), len(agent_types))):
            if agent_types[i] == 'aerial':
                cmd = self.compute_aerial_commands([positions[i]], [velocities[i]], [target_forces[i]])[0]
            else:
                cmd = self.compute_ground_commands([positions[i]], [velocities[i]], [target_forces[i]])[0]
            
            cmd['agent_id'] = i
            cmd['type'] = agent_types[i]
            commands.append(cmd)
        
        return commands
    
    def dispatch(self, target_forces: List[Tuple[float, float, float]],
                 positions: List[Tuple[float, float, float]],
                 velocities: List[Tuple[float, float, float]],
                 agent_types: List[str] = None) -> List[Dict]:
        """Dispatch commands based on modality"""
        if self.modality == 'aerial':
            return self.compute_aerial_commands(positions, velocities, target_forces)
        elif self.modality == 'ground':
            return self.compute_ground_commands(positions, velocities, target_forces)
        elif self.modality == 'underwater':
            return self.compute_underwater_commands(positions, velocities, target_forces)
        elif self.modality == 'mixed' and agent_types:
            return self.compute_mixed_commands(positions, velocities, target_forces, agent_types)
        else:
            return []


def create_formation_controller(n_agents: int = 500, modality: str = 'aerial') -> FormationController:
    """Factory function to create formation controller"""
    return FormationController(n_agents=n_agents, modality=modality)
