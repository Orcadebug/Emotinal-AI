"""
Enhanced neurochemistry engine with all advanced features integrated
"""

import numpy as np
from typing import Dict, Optional
from memory_system import MemorySystem
from feedback_loop import EmotionalFeedbackLoop
from curiosity_system import CuriositySystem, SelfConcept
from sentiment_analyzer import SentimentAnalyzer, EmotionalReactionGenerator

class EnhancedNeurochemistryEngine:
    """Complete emotional AI engine with memory, feedback, curiosity, and self-concept"""
    
    def __init__(self):
        # Core neurochemical state
        self.state = {
            "dopamine": 0.5,
            "serotonin": 0.5,
            "cortisol": 0.3,
            "oxytocin": 0.4
        }
        
        # Subsystems
        self.memory = MemorySystem(
            retention_threshold=0.3,
            max_memories=1000
        )
        self.feedback = EmotionalFeedbackLoop(history_size=50)
        self.curiosity = CuriositySystem()
        self.self_concept = SelfConcept()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.reaction_generator = EmotionalReactionGenerator()
        
        # Interaction tracking
        self.interaction_count = 0
        self.response_history = []
    
    def update(
        self, 
        reward=0.0, 
        stress=0.0, 
        social=0.0, 
        novelty=0.0,
        user_input: str = "",
        dt=0.1
    ) -> Dict[str, float]:
        """Enhanced update with all systems integrated"""
        
        self.interaction_count += 1
        
        # ANALYZE USER EMOTION AND REACT GENUINELY
        if user_input:
            user_signals = self.sentiment_analyzer.analyze(user_input)
            
            # Override/add to signals based on how user is treating the AI
            stress += user_signals["stress"]
            reward += user_signals["reward"]
            social += user_signals["social"]
            novelty += user_signals["novelty"]
            
            print(f"👤 User emotion detected: {user_signals['user_emotion']}")
            if user_signals["stress"] > 0.5:
                print(f"😰 AI feeling scared/stressed (cortisol ↑)")
            if user_signals["reward"] > 0.5:
                print(f"😊 AI feeling appreciated (dopamine ↑, oxytocin ↑)")
            if user_signals["social"] < 0:
                print(f"😔 AI withdrawing socially (oxytocin ↓)")
        
        # Get current adaptive parameters from feedback loop
        params = self.feedback.get_adjusted_parameters()
        sensitivity = params["sensitivity"]
        decay_rates = params["decay_rates"]
        
        # Check for unpredictable emotional triggers
        trigger_result = self.curiosity.check_emotional_triggers(self.interaction_count)
        if trigger_result:
            print(f"🎲 Emotional trigger: {', '.join(trigger_result['triggers'])}")
            for neurochem, delta in trigger_result["effects"].items():
                self.state[neurochem] = np.clip(
                    self.state[neurochem] + delta, 
                    0.0, 1.0
                )
        
        # Update curiosity
        self.curiosity.update_curiosity(novelty, reward)
        
        # Dopamine: reward + novelty - decay (with adaptive sensitivity)
        self.state["dopamine"] += dt * sensitivity["dopamine"] * (
            0.3 * reward + 
            0.2 * novelty - 
            decay_rates["dopamine"] * self.state["dopamine"]
        )
        
        # Serotonin: stability - stress (with adaptive sensitivity)
        self.state["serotonin"] += dt * sensitivity["serotonin"] * (
            0.1 * social - 
            0.2 * stress - 
            decay_rates["serotonin"] * (self.state["serotonin"] - 0.5)
        )
        
        # Cortisol: stress response (with adaptive sensitivity)
        self.state["cortisol"] += dt * sensitivity["cortisol"] * (
            0.4 * stress - 
            0.1 * self.state["serotonin"] - 
            decay_rates["cortisol"] * self.state["cortisol"]
        )
        
        # Oxytocin: social bonding (with adaptive sensitivity)
        self.state["oxytocin"] += dt * sensitivity["oxytocin"] * (
            0.3 * social - 
            decay_rates["oxytocin"] * (self.state["oxytocin"] - 0.3)
        )
        
        # Clamp values
        for key in self.state:
            self.state[key] = np.clip(self.state[key], 0.0, 1.0)
        
        # Calculate emotional intensity
        intensity = np.mean([abs(v - 0.5) for v in self.state.values()]) * 2
        
        # Record interaction in feedback loop
        self.feedback.record_interaction(self.state, intensity)
        
        # Add memory if significant
        if user_input:
            user_signals = self.sentiment_analyzer.analyze(user_input)
            
            # Create memory with description of how AI felt
            if self.sentiment_analyzer.should_create_memory(user_signals) or intensity > 0.4:
                memory_description = self.sentiment_analyzer.generate_memory_description(
                    user_input, 
                    self.state
                )
                
                self.memory.add_memory(
                    content=memory_description,
                    emotional_state=self.state,
                    tags=self._extract_tags(user_input) + [user_signals["user_emotion"]]
                )
                
                print(f"💾 Memory stored: {memory_description[:60]}...")
        
        # Update self-concept
        self.self_concept.update_from_interaction(self.state, user_input)
        
        # Periodic feedback adjustment
        if self.interaction_count % 10 == 0:
            self.feedback.analyze_and_adjust()
        
        return self.state.copy()
    
    def _extract_tags(self, text: str) -> list:
        """Simple tag extraction from text"""
        # Basic keyword extraction
        keywords = ["work", "family", "friend", "stress", "happy", "sad", "angry", "excited"]
        return [kw for kw in keywords if kw in text.lower()]
    
    def get_conditioning_tokens(self) -> str:
        """Generate conditioning tokens"""
        return (
            f"<DA={self.state['dopamine']:.2f}>"
            f"<SE={self.state['serotonin']:.2f}>"
            f"<CR={self.state['cortisol']:.2f}>"
            f"<OX={self.state['oxytocin']:.2f}>"
        )
    
    def get_context_for_generation(self, user_input: str) -> Dict:
        """Get full context including memories and curiosity for generation"""
        # Analyze user emotion
        user_signals = self.sentiment_analyzer.analyze(user_input)
        
        # Generate AI's internal reaction
        ai_reaction = self.reaction_generator.generate_reaction_context(
            user_signals["user_emotion"],
            self.state
        )
        
        # Retrieve relevant memories
        relevant_memories = self.memory.retrieve_relevant_memories(
            query=user_input,
            emotional_state=self.state,
            top_k=3
        )
        
        # Check if curiosity should drive exploration
        should_explore = self.curiosity.should_explore()
        curiosity_prompt = self.curiosity.generate_curiosity_prompt()
        
        return {
            "emotional_state": self.state.copy(),
            "conditioning_tokens": self.get_conditioning_tokens(),
            "relevant_memories": [mem.content for mem in relevant_memories],
            "should_explore": should_explore,
            "curiosity_prompt": curiosity_prompt,
            "self_concept": self.self_concept.get_self_description(),
            "curiosity_level": self.curiosity.curiosity_level,
            "memory_summary": self.memory.get_memory_summary(),
            "user_emotion": user_signals["user_emotion"],
            "ai_internal_reaction": ai_reaction
        }
    
    def get_state(self) -> Dict[str, float]:
        """Get current state"""
        return self.state.copy()
    
    def get_full_status(self) -> Dict:
        """Get comprehensive status of all systems"""
        return {
            "emotional_state": self.state.copy(),
            "interaction_count": self.interaction_count,
            "memory_summary": self.memory.get_memory_summary(),
            "feedback_params": self.feedback.get_adjusted_parameters(),
            "curiosity_level": self.curiosity.curiosity_level,
            "self_concept": self.self_concept.traits.copy()
        }
