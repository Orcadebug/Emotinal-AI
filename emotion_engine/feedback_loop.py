"""
Feedback loop for dynamic parameter adjustment based on emotional intensity
"""

import numpy as np
from typing import Dict, List
from collections import deque

class EmotionalFeedbackLoop:
    """Adjusts neurochemistry parameters based on interaction patterns"""
    
    def __init__(self, history_size: int = 50):
        self.history_size = history_size
        self.interaction_history = deque(maxlen=history_size)
        
        # Adaptive parameters
        self.sensitivity = {
            "dopamine": 1.0,
            "serotonin": 1.0,
            "cortisol": 1.0,
            "oxytocin": 1.0
        }
        
        self.decay_rates = {
            "dopamine": 0.1,
            "serotonin": 0.05,
            "cortisol": 0.08,
            "oxytocin": 0.06
        }
        
        # Learning rates for adaptation
        self.learning_rate = 0.01
    
    def record_interaction(
        self, 
        emotional_state: Dict[str, float],
        intensity: float,
        user_feedback: str = None
    ):
        """Record interaction for feedback analysis"""
        self.interaction_history.append({
            "state": emotional_state.copy(),
            "intensity": intensity,
            "feedback": user_feedback,
            "timestamp": len(self.interaction_history)
        })
    
    def analyze_and_adjust(self) -> Dict[str, float]:
        """Analyze recent interactions and adjust parameters"""
        if len(self.interaction_history) < 10:
            return self.sensitivity
        
        recent = list(self.interaction_history)[-20:]
        
        # Calculate emotional volatility
        volatility = self._calculate_volatility(recent)
        
        # Adjust sensitivity based on volatility
        for neurochem in self.sensitivity:
            if volatility[neurochem] > 0.3:
                # High volatility - reduce sensitivity (stabilize)
                self.sensitivity[neurochem] *= (1.0 - self.learning_rate)
            elif volatility[neurochem] < 0.1:
                # Low volatility - increase sensitivity (more responsive)
                self.sensitivity[neurochem] *= (1.0 + self.learning_rate)
            
            # Keep in reasonable bounds
            self.sensitivity[neurochem] = np.clip(self.sensitivity[neurochem], 0.5, 2.0)
        
        # Adjust decay rates based on intensity patterns
        avg_intensity = np.mean([i["intensity"] for i in recent])
        
        if avg_intensity > 0.7:
            # High intensity - slower decay (emotions linger)
            for key in self.decay_rates:
                self.decay_rates[key] *= 0.95
        elif avg_intensity < 0.3:
            # Low intensity - faster decay (more neutral)
            for key in self.decay_rates:
                self.decay_rates[key] *= 1.05
        
        # Keep decay rates in bounds
        for key in self.decay_rates:
            self.decay_rates[key] = np.clip(self.decay_rates[key], 0.01, 0.3)
        
        return self.sensitivity
    
    def _calculate_volatility(self, interactions: List[Dict]) -> Dict[str, float]:
        """Calculate emotional volatility for each neurochemical"""
        volatility = {}
        
        for neurochem in ["dopamine", "serotonin", "cortisol", "oxytocin"]:
            values = [i["state"][neurochem] for i in interactions]
            # Standard deviation as measure of volatility
            volatility[neurochem] = np.std(values)
        
        return volatility
    
    def get_adjusted_parameters(self) -> Dict:
        """Get current adjusted parameters"""
        return {
            "sensitivity": self.sensitivity.copy(),
            "decay_rates": self.decay_rates.copy(),
            "interaction_count": len(self.interaction_history)
        }
