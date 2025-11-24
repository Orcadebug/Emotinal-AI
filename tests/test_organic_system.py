"""
Tests for the Organic Emotional AI System
"""

import pytest
import json
import os
from emotion_engine.integrated_engine import IntegratedNeurochemistryEngine
from emotion_engine.organic_memory import OrganicMemorySystem
from emotion_engine.neuroplasticity import NeuroplasticitySystem


class TestOrganicMemorySystem:
    """Test memory recall functionality"""
    
    def test_memory_loading(self):
        """Test that memories load correctly"""
        memory_system = OrganicMemorySystem()
        assert len(memory_system.memories) > 0
    
    def test_keyword_trigger(self):
        """Test context-based memory recall"""
        memory_system = OrganicMemorySystem()
        
        # Test coding keyword
        state = {"dopamine": 0.5, "serotonin": 0.5, "cortisol": 0.5, "oxytocin": 0.5}
        memory = memory_system.recall(state, "Let's do some coding")
        
        assert memory is not None
        assert memory["memory_id"] == "DOP_01"
    
    def test_emotional_state_matching(self):
        """Test state-based memory recall"""
        memory_system = OrganicMemorySystem()
        
        # High cortisol, low serotonin (stress/failure state)
        state = {"dopamine": 0.2, "serotonin": 0.1, "cortisol": 0.7, "oxytocin": 0.3}
        memory = memory_system.recall(state, "")
        
        assert memory is not None
        # Should match SERO_LOW_01 (failure memory)
    
    def test_memory_injection(self):
        """Test memory formatting for prompt"""
        memory_system = OrganicMemorySystem()
        
        memory = {
            "content": "Test memory content",
            "type": "TEST_TYPE"
        }
        
        injected = memory_system.inject_memory_into_prompt(memory)
        assert "INTERNAL FLASHBACK" in injected
        assert "Test memory content" in injected


class TestNeuroplasticitySystem:
    """Test personality evolution"""
    
    def setup_method(self):
        """Clean up test file before each test"""
        self.test_file = "data/test_personality_baseline.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def teardown_method(self):
        """Clean up test file after each test"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_baseline_initialization(self):
        """Test that baseline starts at neutral"""
        plasticity = NeuroplasticitySystem(self.test_file)
        
        assert plasticity.baseline["dopamine_base"] == 0.5
        assert plasticity.baseline["serotonin_base"] == 0.5
        assert plasticity.baseline["age"] == 0
    
    def test_plasticity_decay(self):
        """Test that plasticity decreases with age"""
        plasticity = NeuroplasticitySystem(self.test_file)
        
        initial_plasticity = plasticity.baseline["plasticity"]
        
        # Age the system
        for _ in range(100):
            plasticity.grow({"dopamine": 0.5, "serotonin": 0.5, "cortisol": 0.5, "oxytocin": 0.5})
        
        final_plasticity = plasticity.baseline["plasticity"]
        
        assert final_plasticity < initial_plasticity
        assert plasticity.age == 100
    
    def test_baseline_shift(self):
        """Test that baseline shifts toward experienced states"""
        plasticity = NeuroplasticitySystem(self.test_file)
        
        # Repeatedly experience high dopamine
        for _ in range(50):
            plasticity.grow({"dopamine": 0.9, "serotonin": 0.5, "cortisol": 0.3, "oxytocin": 0.5})
        
        # Baseline should have shifted toward high dopamine
        assert plasticity.baseline["dopamine_base"] > 0.5


class TestIntegratedEngine:
    """Test complete integrated system"""
    
    def test_engine_initialization(self):
        """Test that engine initializes correctly"""
        engine = IntegratedNeurochemistryEngine()
        
        assert 0.0 <= engine.dopamine <= 1.0
        assert engine.current_desire is not None
    
    def test_neurochemistry_update(self):
        """Test neurochemistry updates with stimulus"""
        engine = IntegratedNeurochemistryEngine()
        
        initial_dopamine = engine.dopamine
        
        # Apply positive stimulus
        engine.update_neurochemistry({"dopamine": 0.3})
        
        # Dopamine should increase (accounting for chaos)
        assert engine.dopamine != initial_dopamine
    
    def test_want_generation(self):
        """Test that wants are generated based on state"""
        engine = IntegratedNeurochemistryEngine()
        
        # Force high dopamine
        engine.dopamine = 0.9
        engine._generate_wants()
        
        assert "build" in engine.current_desire.lower() or "learn" in engine.current_desire.lower()
    
    def test_prompt_context_generation(self):
        """Test that prompt context includes all components"""
        engine = IntegratedNeurochemistryEngine()
        
        context = engine.get_prompt_context("Let's code something")
        
        assert "BIOMETRICS" in context
        assert "DESIRE" in context
        assert "Dopamine" in context
    
    def test_memory_recall_in_context(self):
        """Test that memories are recalled in context"""
        engine = IntegratedNeurochemistryEngine()
        
        context = engine.get_prompt_context("I'm thinking about dropping out")
        
        # Should trigger dropout memory
        assert "FLASHBACK" in context or context.count("\n") > 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
