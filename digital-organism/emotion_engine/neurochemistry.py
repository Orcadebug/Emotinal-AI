import numpy as np
from typing import Dict

class NeurochemistryEngine:
    """ODE-based neurochemistry simulation"""
    
    def __init__(self):
        self.state = {
            "dopamine": 0.5,
            "serotonin": 0.5,
            "cortisol": 0.3,
            "oxytocin": 0.4
        }
        
        self.decay_rates = {
            "dopamine": 0.1,
            "serotonin": 0.05,
            "cortisol": 0.08,
            "oxytocin": 0.06
        }
    
    def update(self, reward=0.0, stress=0.0, social=0.0, novelty=0.0, dt=0.1) -> Dict[str, float]:
        """Update neurochemical state using differential equations"""
        
        # Dopamine: reward + novelty - decay
        self.state["dopamine"] += dt * (
            0.3 * reward + 
            0.2 * novelty - 
            self.decay_rates["dopamine"] * self.state["dopamine"]
        )
        
        # Serotonin: stability - stress
        self.state["serotonin"] += dt * (
            0.1 * social - 
            0.2 * stress - 
            self.decay_rates["serotonin"] * (self.state["serotonin"] - 0.5)
        )
        
        # Cortisol: stress response
        self.state["cortisol"] += dt * (
            0.4 * stress - 
            0.1 * self.state["serotonin"] - 
            self.decay_rates["cortisol"] * self.state["cortisol"]
        )
        
        # Oxytocin: social bonding
        self.state["oxytocin"] += dt * (
            0.3 * social - 
            self.decay_rates["oxytocin"] * (self.state["oxytocin"] - 0.3)
        )
        
        # Clamp values to [0, 1]
        for key in self.state:
            self.state[key] = np.clip(self.state[key], 0.0, 1.0)
        
        return self.state.copy()
    
    def get_conditioning_tokens(self) -> str:
        """Generate conditioning tokens for LLM"""
        return (
            f"<DA={self.state['dopamine']:.2f}>"
            f"<SE={self.state['serotonin']:.2f}>"
            f"<CR={self.state['cortisol']:.2f}>"
            f"<OX={self.state['oxytocin']:.2f}>"
        )
    
    def get_state(self) -> Dict[str, float]:
        """Get current state"""
        return self.state.copy()
