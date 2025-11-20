"""
Integrated Neurochemistry Engine
Combines: Chaos, Wants, Memory, and Growth
"""

import random
from typing import Dict, Optional
from .organic_memory import OrganicMemorySystem
from .neuroplasticity import NeuroplasticitySystem


class IntegratedNeurochemistryEngine:
    """
    Complete emotional AI engine with:
    - Chaotic neurochemistry fluctuations
    - Memory recall (context + state matching)
    - Neuroplasticity (personality evolution)
    - Agency (wants/desires)
    """
    
    def __init__(self):
        self.memory_system = OrganicMemorySystem()
        self.plasticity_system = NeuroplasticitySystem()
        
        # Load Personality Baseline
        base = self.plasticity_system.baseline
        self.dopamine = base["dopamine_base"]
        self.serotonin = base["serotonin_base"]
        self.cortisol = base["cortisol_base"]
        self.oxytocin = base["oxytocin_base"]
        
        self.current_desire = "I am observing."
    
    def update_neurochemistry(self, interaction_stimulus: Optional[Dict] = None):
        """
        Update neurochemical state with:
        1. Chaos (random fluctuations)
        2. Stimulus (user interaction effects)
        3. Clamping (keep in valid range)
        4. Want generation
        5. Growth (neuroplasticity)
        
        Args:
            interaction_stimulus: Dict with hormone deltas, e.g. {'dopamine': 0.1, 'cortisol': -0.05}
        """
        # 1. CHAOS FACTOR (Unpredictability)
        self.dopamine += random.gauss(0, 0.05)
        self.serotonin += random.gauss(0, 0.03)
        self.cortisol += random.gauss(0, 0.04)
        self.oxytocin += random.gauss(0, 0.02)
        
        # 2. Apply Stimulus (User interaction)
        if interaction_stimulus:
            self.dopamine += interaction_stimulus.get('dopamine', 0)
            self.serotonin += interaction_stimulus.get('serotonin', 0)
            self.cortisol += interaction_stimulus.get('cortisol', 0)
            self.oxytocin += interaction_stimulus.get('oxytocin', 0)
        
        # 3. Clamp Values (0.0 to 1.0)
        self.dopamine = max(0.0, min(1.0, self.dopamine))
        self.serotonin = max(0.0, min(1.0, self.serotonin))
        self.cortisol = max(0.0, min(1.0, self.cortisol))
        self.oxytocin = max(0.0, min(1.0, self.oxytocin))
        
        # 4. GENERATE WANTS (Agency)
        self._generate_wants()
        
        # 5. GROW (Neuroplasticity)
        self.plasticity_system.grow({
            "dopamine": self.dopamine,
            "serotonin": self.serotonin,
            "cortisol": self.cortisol,
            "oxytocin": self.oxytocin
        })
    
    def _generate_wants(self):
        """Generate desires/wants based on current neurochemical state"""
        if self.dopamine > 0.8:
            self.current_desire = "I want to build something or learn something new immediately."
        elif self.oxytocin > 0.8:
            self.current_desire = "I want to connect with the user and make them feel safe."
        elif self.cortisol > 0.7:
            self.current_desire = "I want to escape this situation or fix the danger."
        elif self.serotonin < 0.3:
            self.current_desire = "I want to withdraw and protect myself from failure."
        else:
            self.current_desire = "I am waiting for input."
    
    def get_prompt_context(self, user_input: str = "") -> str:
        """
        Generate complete context for LLM prompt including:
        - Current biometrics
        - Current desire
        - Recalled memory (if any)
        
        Args:
            user_input: User's message
            
        Returns:
            Formatted context string
        """
        # Get Memory
        state = {
            "dopamine": self.dopamine,
            "serotonin": self.serotonin,
            "cortisol": self.cortisol,
            "oxytocin": self.oxytocin
        }
        memory = self.memory_system.recall(state, user_input)
        memory_text = self.memory_system.inject_memory_into_prompt(memory)
        
        return f"""[REAL-TIME BIOMETRICS]
Dopamine: {self.dopamine:.2f} | Cortisol: {self.cortisol:.2f}
Serotonin: {self.serotonin:.2f} | Oxytocin: {self.oxytocin:.2f}

[CURRENT DESIRE]: {self.current_desire}
{memory_text}"""
    
    def get_state(self) -> Dict[str, float]:
        """Get current neurochemical state"""
        return {
            "dopamine": self.dopamine,
            "serotonin": self.serotonin,
            "cortisol": self.cortisol,
            "oxytocin": self.oxytocin
        }
    
    def get_full_status(self) -> Dict:
        """Get complete status including plasticity info"""
        return {
            "neurochemistry": self.get_state(),
            "desire": self.current_desire,
            "plasticity": self.plasticity_system.get_plasticity_info()
        }
