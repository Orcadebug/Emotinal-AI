"""
Memory system with emotional intensity tracking and retention
"""

import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import numpy as np

@dataclass
class Memory:
    """A single memory with emotional context"""
    content: str
    timestamp: float
    emotional_state: Dict[str, float]
    emotional_intensity: float
    access_count: int = 0
    last_accessed: float = 0.0
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.last_accessed == 0.0:
            self.last_accessed = self.timestamp
    
    def calculate_salience(self, current_time: float, decay_rate: float = 0.1) -> float:
        """Calculate memory salience based on intensity, recency, and access frequency"""
        # Time decay
        time_since_creation = current_time - self.timestamp
        recency_factor = np.exp(-decay_rate * time_since_creation)
        
        # Access frequency boost
        frequency_factor = 1.0 + (0.1 * self.access_count)
        
        # Emotional intensity is the base
        salience = self.emotional_intensity * recency_factor * frequency_factor
        
        return salience
    
    def access(self):
        """Mark memory as accessed"""
        self.access_count += 1
        self.last_accessed = time.time()

class MemorySystem:
    """Manages episodic and emotional memories"""
    
    def __init__(
        self, 
        retention_threshold: float = 0.3,
        max_memories: int = 1000,
        consolidation_interval: int = 100
    ):
        self.memories: List[Memory] = []
        self.retention_threshold = retention_threshold
        self.max_memories = max_memories
        self.consolidation_interval = consolidation_interval
        self.interaction_count = 0
        
        # Baseline memories (implanted experiences)
        self.baseline_memories: List[Memory] = []
    
    def implant_baseline_memories(self, baseline_data: List[Dict]):
        """Implant initial memories as emotional baseline"""
        print(f"Implanting {len(baseline_data)} baseline memories...")
        
        for data in baseline_data:
            memory = Memory(
                content=data["content"],
                timestamp=time.time() - data.get("age_days", 0) * 86400,  # Convert days to seconds
                emotional_state=data["emotional_state"],
                emotional_intensity=data["intensity"],
                tags=data.get("tags", [])
            )
            self.baseline_memories.append(memory)
            self.memories.append(memory)
        
        print(f"✓ Implanted {len(self.baseline_memories)} baseline memories")
    
    def add_memory(
        self, 
        content: str, 
        emotional_state: Dict[str, float],
        tags: Optional[List[str]] = None
    ) -> Memory:
        """Add new memory from interaction"""
        # Calculate emotional intensity
        intensity = self._calculate_emotional_intensity(emotional_state)
        
        memory = Memory(
            content=content,
            timestamp=time.time(),
            emotional_state=emotional_state.copy(),
            emotional_intensity=intensity,
            tags=tags or []
        )
        
        self.memories.append(memory)
        self.interaction_count += 1
        
        # Periodic memory consolidation
        if self.interaction_count % self.consolidation_interval == 0:
            self.consolidate_memories()
        
        return memory
    
    def _calculate_emotional_intensity(self, state: Dict[str, float]) -> float:
        """Calculate overall emotional intensity from state"""
        # High intensity = extreme values (far from neutral 0.5)
        deviations = [abs(v - 0.5) for v in state.values()]
        intensity = np.mean(deviations) * 2  # Scale to 0-1
        
        # Boost for high cortisol (stress makes memories stronger)
        if state.get("cortisol", 0) > 0.7:
            intensity *= 1.3
        
        # Boost for high dopamine (reward makes memories stronger)
        if state.get("dopamine", 0) > 0.7:
            intensity *= 1.2
        
        return min(intensity, 1.0)
    
    def consolidate_memories(self):
        """Remove low-salience memories, keep important ones"""
        current_time = time.time()
        
        # Calculate salience for all memories
        memory_salience = [
            (mem, mem.calculate_salience(current_time))
            for mem in self.memories
        ]
        
        # Always keep baseline memories
        baseline_ids = {id(mem) for mem in self.baseline_memories}
        
        # Filter memories
        kept_memories = []
        for mem, salience in memory_salience:
            # Keep if: baseline, high salience, or recent
            if (id(mem) in baseline_ids or 
                salience >= self.retention_threshold or
                (current_time - mem.timestamp) < 3600):  # Keep last hour
                kept_memories.append(mem)
        
        # If still too many, keep top N by salience
        if len(kept_memories) > self.max_memories:
            kept_memories.sort(key=lambda m: m.calculate_salience(current_time), reverse=True)
            kept_memories = kept_memories[:self.max_memories]
        
        removed_count = len(self.memories) - len(kept_memories)
        self.memories = kept_memories
        
        if removed_count > 0:
            print(f"Memory consolidation: Removed {removed_count} low-salience memories")
    
    def retrieve_relevant_memories(
        self, 
        query: str, 
        emotional_state: Dict[str, float],
        top_k: int = 5
    ) -> List[Memory]:
        """Retrieve memories relevant to current context and emotional state"""
        if not self.memories:
            return []
        
        current_time = time.time()
        scored_memories = []
        
        for mem in self.memories:
            # Base score: salience
            score = mem.calculate_salience(current_time)
            
            # Boost for emotional similarity
            emotional_similarity = self._emotional_similarity(
                mem.emotional_state, 
                emotional_state
            )
            score *= (1.0 + emotional_similarity)
            
            # Boost for content relevance (simple keyword matching)
            query_words = set(query.lower().split())
            memory_words = set(mem.content.lower().split())
            overlap = len(query_words & memory_words)
            if overlap > 0:
                score *= (1.0 + 0.2 * overlap)
            
            scored_memories.append((mem, score))
        
        # Sort by score and return top K
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        top_memories = [mem for mem, score in scored_memories[:top_k]]
        
        # Mark as accessed
        for mem in top_memories:
            mem.access()
        
        return top_memories
    
    def _emotional_similarity(self, state1: Dict[str, float], state2: Dict[str, float]) -> float:
        """Calculate similarity between two emotional states"""
        keys = set(state1.keys()) & set(state2.keys())
        if not keys:
            return 0.0
        
        # Cosine similarity
        differences = [abs(state1[k] - state2[k]) for k in keys]
        similarity = 1.0 - (np.mean(differences))
        return max(similarity, 0.0)
    
    def get_memory_summary(self) -> Dict:
        """Get summary statistics about memory system"""
        if not self.memories:
            return {"total": 0}
        
        current_time = time.time()
        saliences = [mem.calculate_salience(current_time) for mem in self.memories]
        
        return {
            "total": len(self.memories),
            "baseline": len(self.baseline_memories),
            "acquired": len(self.memories) - len(self.baseline_memories),
            "avg_salience": np.mean(saliences),
            "high_salience_count": sum(1 for s in saliences if s > 0.7),
            "total_accesses": sum(mem.access_count for mem in self.memories)
        }
    
    def save_memories(self, filepath: str):
        """Save memories to file"""
        data = [asdict(mem) for mem in self.memories]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_memories(self, filepath: str):
        """Load memories from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.memories = [Memory(**mem_data) for mem_data in data]
        print(f"✓ Loaded {len(self.memories)} memories from {filepath}")
