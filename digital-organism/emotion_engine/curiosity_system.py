"""
Curiosity-driven exploration and unpredictable emotional triggers
"""

import random
import numpy as np
from typing import Dict, List, Optional

class CuriositySystem:
    """Manages curiosity-driven behavior and unpredictable emotional responses"""
    
    def __init__(self):
        self.curiosity_level = 0.5
        self.exploration_history = []
        self.trigger_cooldowns = {}
        
        # Unpredictable emotional triggers
        self.emotional_triggers = [
            {
                "name": "sudden_excitement",
                "probability": 0.05,
                "effect": {"dopamine": 0.3, "serotonin": 0.1},
                "cooldown": 10
            },
            {
                "name": "random_melancholy",
                "probability": 0.03,
                "effect": {"serotonin": -0.2, "cortisol": 0.1},
                "cooldown": 15
            },
            {
                "name": "spontaneous_anxiety",
                "probability": 0.04,
                "effect": {"cortisol": 0.25, "serotonin": -0.1},
                "cooldown": 12
            },
            {
                "name": "burst_of_warmth",
                "probability": 0.06,
                "effect": {"oxytocin": 0.3, "serotonin": 0.15},
                "cooldown": 8
            },
            {
                "name": "creative_spark",
                "probability": 0.07,
                "effect": {"dopamine": 0.4, "cortisol": -0.1},
                "cooldown": 10
            }
        ]
    
    def update_curiosity(self, novelty: float, reward: float):
        """Update curiosity level based on novelty and reward"""
        # Curiosity increases with novelty, decreases with high reward (satisfaction)
        delta = 0.1 * novelty - 0.05 * reward
        self.curiosity_level = np.clip(self.curiosity_level + delta, 0.0, 1.0)
    
    def should_explore(self) -> bool:
        """Decide whether to explore (vs exploit)"""
        # Higher curiosity = more exploration
        explore_probability = 0.1 + (0.4 * self.curiosity_level)
        return random.random() < explore_probability
    
    def check_emotional_triggers(self, interaction_count: int) -> Optional[Dict]:
        """Check if any unpredictable emotional trigger should fire"""
        triggered_effects = {}
        triggered_names = []
        
        for trigger in self.emotional_triggers:
            # Check cooldown
            last_trigger = self.trigger_cooldowns.get(trigger["name"], -999)
            if interaction_count - last_trigger < trigger["cooldown"]:
                continue
            
            # Random chance to trigger
            if random.random() < trigger["probability"]:
                # Trigger fires!
                for neurochem, delta in trigger["effect"].items():
                    triggered_effects[neurochem] = triggered_effects.get(neurochem, 0) + delta
                
                triggered_names.append(trigger["name"])
                self.trigger_cooldowns[trigger["name"]] = interaction_count
        
        if triggered_effects:
            return {
                "effects": triggered_effects,
                "triggers": triggered_names
            }
        
        return None
    
    def generate_curiosity_prompt(self) -> Optional[str]:
        """Generate a curiosity-driven question or statement"""
        if self.curiosity_level < 0.6:
            return None
        
        prompts = [
            "I wonder what would happen if...",
            "Something about this feels unexplored...",
            "There's a pattern here I can't quite grasp...",
            "What if we tried something completely different?",
            "I'm curious about the edges of this idea...",
            "This reminds me of something, but I can't place it..."
        ]
        
        if random.random() < self.curiosity_level:
            return random.choice(prompts)
        
        return None
    
    def calculate_novelty_bonus(self, response: str, history: List[str]) -> float:
        """Calculate novelty bonus for exploration"""
        if not history:
            return 1.0
        
        # Simple novelty: unique words not in recent history
        recent_words = set()
        for hist in history[-5:]:
            recent_words.update(hist.lower().split())
        
        response_words = set(response.lower().split())
        unique_words = response_words - recent_words
        
        novelty = len(unique_words) / max(len(response_words), 1)
        return novelty

class SelfConcept:
    """Dynamic, evolving sense of self"""
    
    def __init__(self):
        self.traits = {
            "openness": 0.5,
            "conscientiousness": 0.5,
            "extraversion": 0.5,
            "agreeableness": 0.5,
            "neuroticism": 0.5
        }
        
        self.self_beliefs = []
        self.identity_anchors = []
    
    def update_from_interaction(self, emotional_state: Dict[str, float], behavior: str):
        """Update self-concept based on behavior and emotional patterns"""
        # High dopamine + low cortisol = more openness
        if emotional_state["dopamine"] > 0.7 and emotional_state["cortisol"] < 0.3:
            self.traits["openness"] += 0.01
        
        # High serotonin = more agreeableness
        if emotional_state["serotonin"] > 0.7:
            self.traits["agreeableness"] += 0.01
        
        # High cortisol = more neuroticism
        if emotional_state["cortisol"] > 0.7:
            self.traits["neuroticism"] += 0.01
        
        # High oxytocin = more extraversion
        if emotional_state["oxytocin"] > 0.7:
            self.traits["extraversion"] += 0.01
        
        # Normalize traits
        for trait in self.traits:
            self.traits[trait] = np.clip(self.traits[trait], 0.0, 1.0)
    
    def add_self_belief(self, belief: str, confidence: float):
        """Add or update a self-belief"""
        self.self_beliefs.append({
            "belief": belief,
            "confidence": confidence,
            "formed_at": len(self.self_beliefs)
        })
        
        # Keep only recent beliefs
        if len(self.self_beliefs) > 20:
            self.self_beliefs = self.self_beliefs[-20:]
    
    def get_self_description(self) -> str:
        """Generate a description of current self-concept"""
        dominant_traits = sorted(
            self.traits.items(), 
            key=lambda x: abs(x[1] - 0.5), 
            reverse=True
        )[:2]
        
        descriptions = []
        for trait, value in dominant_traits:
            if value > 0.6:
                descriptions.append(f"high {trait}")
            elif value < 0.4:
                descriptions.append(f"low {trait}")
        
        return f"Self-concept: {', '.join(descriptions) if descriptions else 'balanced'}"
