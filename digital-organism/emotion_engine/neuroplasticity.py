"""
Neuroplasticity System - Allows AI personality to evolve based on experiences
"""

import json
import math
from typing import Dict


class NeuroplasticitySystem:
    """
    Manages personality baseline evolution through neuroplasticity.
    The AI's baseline personality shifts based on repeated emotional experiences.
    """
    
    def __init__(self, save_file: str = "data/personality_baseline.json"):
        self.save_file = save_file
        self.baseline = self._load_baseline()
        self.age = self.baseline.get("age", 0)
    
    def _load_baseline(self) -> Dict:
        """Load personality baseline from file or create default"""
        try:
            with open(self.save_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # STARTING PERSONALITY (Blank Slate)
            return {
                "dopamine_base": 0.5,
                "serotonin_base": 0.5,
                "cortisol_base": 0.5,
                "oxytocin_base": 0.5,
                "plasticity": 0.1,
                "age": 0
            }
    
    def save_baseline(self):
        """Persist baseline to disk"""
        with open(self.save_file, 'w') as f:
            json.dump(self.baseline, f, indent=2)
    
    def grow(self, current_state: Dict[str, float]) -> Dict:
        """
        Update personality baseline based on current emotional state.
        Plasticity decreases over time (child -> adult).
        
        Args:
            current_state: Current neurochemical levels
            
        Returns:
            Updated baseline dictionary
        """
        self.age += 1
        
        # Plasticity decays over time (Child -> Adult)
        # Uses exponential decay: starts at 0.1, approaches 0.005
        current_plasticity = max(0.005, 0.1 * math.exp(-self.age / 500))
        self.baseline["plasticity"] = current_plasticity
        self.baseline["age"] = self.age
        
        # Shift the Baseline towards the Current State
        for hormone in ["dopamine", "serotonin", "cortisol", "oxytocin"]:
            base_key = f"{hormone}_base"
            current_val = current_state.get(hormone, 0.5)
            old_base = self.baseline[base_key]
            
            # Formula: New = Old + (Difference * Plasticity)
            # This gradually shifts baseline toward frequently experienced states
            new_base = old_base + (current_val - old_base) * current_plasticity
            self.baseline[base_key] = new_base
        
        self.save_baseline()
        return self.baseline
    
    def get_baseline_state(self) -> Dict[str, float]:
        """Get current baseline neurochemical levels"""
        return {
            "dopamine": self.baseline["dopamine_base"],
            "serotonin": self.baseline["serotonin_base"],
            "cortisol": self.baseline["cortisol_base"],
            "oxytocin": self.baseline["oxytocin_base"]
        }
    
    def get_plasticity_info(self) -> Dict:
        """Get information about current plasticity state"""
        return {
            "age": self.age,
            "plasticity": self.baseline["plasticity"],
            "baseline": self.get_baseline_state()
        }
