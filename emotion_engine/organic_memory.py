"""
Organic Memory System - Context-triggered memory recall
Simpler, more direct memory system focused on keyword triggers and emotional state matching
"""

import json
import random
from typing import Dict, List, Optional


class OrganicMemorySystem:
    """
    Memory recall based on:
    1. Context triggers (keywords in user input)
    2. Emotional state matching (similar hormone levels)
    """
    
    def __init__(self, memory_file_path: str = "data/emotional_memories.json"):
        self.memories = self._load_memories(memory_file_path)
    
    def _load_memories(self, path: str) -> List[Dict]:
        """Load memories from JSON file"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[System] Warning: Memory file at {path} not found.")
            return []
    
    def recall(
        self, 
        current_neurochemistry: Dict[str, float], 
        user_input_text: str = ""
    ) -> Optional[Dict]:
        """
        Recall a memory based on context or emotional state.
        
        Priority:
        1. Context trigger (keyword match)
        2. Emotional state match
        
        Args:
            current_neurochemistry: Current hormone levels
            user_input_text: User's message
            
        Returns:
            Memory dict or None
        """
        # 1. Context Trigger (If you mention specific keywords)
        if user_input_text:
            for memory in self.memories:
                for keyword in memory.get("trigger_keywords", []):
                    if keyword.lower() in user_input_text.lower():
                        return memory
        
        # 2. State Match (If the AI's hormones match the memory's vibe)
        relevant_memories = []
        for memory in self.memories:
            impact = memory.get("hormonal_impact", {})
            score = 0
            
            # Match memory if hormones are within 0.2 range of current state
            for hormone, level in impact.items():
                current_level = current_neurochemistry.get(hormone, 0.5)
                if abs(current_level - level) < 0.2:
                    score += 1
            
            if score >= 1:
                relevant_memories.append(memory)
        
        if relevant_memories:
            return random.choice(relevant_memories)
        
        return None
    
    def inject_memory_into_prompt(self, memory: Optional[Dict]) -> str:
        """
        Format memory for injection into system prompt.
        
        Args:
            memory: Memory dict or None
            
        Returns:
            Formatted memory string
        """
        if not memory:
            return ""
        
        return (
            f"\n[INTERNAL FLASHBACK]: {memory['content']}\n"
            f"(This flashback makes you feel: {memory['type']})"
        )
