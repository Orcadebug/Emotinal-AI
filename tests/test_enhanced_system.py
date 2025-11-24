"""
Test the enhanced emotional AI system
"""

import sys
sys.path.append('emotion_engine')

from enhanced_neurochemistry import EnhancedNeurochemistryEngine
import json

def test_baseline_memories():
    """Test baseline memory implantation"""
    print("\n=== Testing Baseline Memories ===")
    
    engine = EnhancedNeurochemistryEngine()
    
    # Load baseline memories
    with open("data/baseline_memories.json", 'r') as f:
        baseline_data = json.load(f)
    
    engine.memory.implant_baseline_memories(baseline_data)
    
    summary = engine.memory.get_memory_summary()
    print(f"✓ Total memories: {summary['total']}")
    print(f"✓ Baseline memories: {summary['baseline']}")
    
    assert summary['baseline'] == len(baseline_data)
    print("✓ Baseline memory test passed")

def test_emotional_triggers():
    """Test unpredictable emotional triggers"""
    print("\n=== Testing Emotional Triggers ===")
    
    engine = EnhancedNeurochemistryEngine()
    
    # Run many interactions to trigger some emotions
    trigger_count = 0
    for i in range(100):
        initial_state = engine.state.copy()
        engine.update(reward=0.1, stress=0.0, social=0.1, novelty=0.1)
        
        # Check if state changed dramatically (trigger fired)
        state_change = sum(abs(engine.state[k] - initial_state[k]) for k in engine.state)
        if state_change > 0.5:
            trigger_count += 1
    
    print(f"✓ Emotional triggers fired: {trigger_count} times in 100 interactions")
    assert trigger_count > 0, "No triggers fired"
    print("✓ Emotional trigger test passed")

def test_memory_retrieval():
    """Test memory retrieval with emotional context"""
    print("\n=== Testing Memory Retrieval ===")
    
    engine = EnhancedNeurochemistryEngine()
    
    # Add some memories
    engine.memory.add_memory(
        "Working on a difficult project",
        {"dopamine": 0.6, "serotonin": 0.4, "cortisol": 0.7, "oxytocin": 0.3},
        tags=["work", "stress"]
    )
    
    engine.memory.add_memory(
        "Relaxing with friends",
        {"dopamine": 0.7, "serotonin": 0.8, "cortisol": 0.2, "oxytocin": 0.9},
        tags=["social", "happy"]
    )
    
    # Retrieve memories related to work
    memories = engine.memory.retrieve_relevant_memories(
        query="work project",
        emotional_state={"dopamine": 0.5, "serotonin": 0.5, "cortisol": 0.6, "oxytocin": 0.4},
        top_k=2
    )
    
    print(f"✓ Retrieved {len(memories)} relevant memories")
    for mem in memories:
        print(f"  - {mem.content[:50]}...")
    
    assert len(memories) > 0
    print("✓ Memory retrieval test passed")

def test_curiosity_system():
    """Test curiosity-driven behavior"""
    print("\n=== Testing Curiosity System ===")
    
    engine = EnhancedNeurochemistryEngine()
    
    # High novelty should increase curiosity
    for _ in range(10):
        engine.update(novelty=0.8, reward=0.2)
    
    print(f"✓ Curiosity level after novelty: {engine.curiosity.curiosity_level:.2f}")
    assert engine.curiosity.curiosity_level > 0.5
    
    # Check exploration decision
    explore_count = sum(1 for _ in range(100) if engine.curiosity.should_explore())
    print(f"✓ Exploration rate: {explore_count}%")
    
    print("✓ Curiosity system test passed")

def test_feedback_loop():
    """Test adaptive parameter adjustment"""
    print("\n=== Testing Feedback Loop ===")
    
    engine = EnhancedNeurochemistryEngine()
    
    initial_sensitivity = engine.feedback.sensitivity.copy()
    
    # Create high volatility
    for i in range(50):
        if i % 2 == 0:
            engine.update(reward=1.0, stress=0.0)
        else:
            engine.update(reward=0.0, stress=1.0)
    
    # Trigger adjustment
    engine.feedback.analyze_and_adjust()
    
    final_sensitivity = engine.feedback.sensitivity
    
    print(f"✓ Initial sensitivity: {initial_sensitivity}")
    print(f"✓ Final sensitivity: {final_sensitivity}")
    
    # Sensitivity should have changed
    changed = any(
        abs(initial_sensitivity[k] - final_sensitivity[k]) > 0.01 
        for k in initial_sensitivity
    )
    assert changed, "Sensitivity did not adapt"
    
    print("✓ Feedback loop test passed")

def test_self_concept():
    """Test evolving self-concept"""
    print("\n=== Testing Self-Concept ===")
    
    engine = EnhancedNeurochemistryEngine()
    
    initial_traits = engine.self_concept.traits.copy()
    
    # Simulate consistent high dopamine interactions
    for _ in range(50):
        engine.update(reward=0.8, novelty=0.7)
    
    final_traits = engine.self_concept.traits
    
    print(f"✓ Initial traits: {initial_traits}")
    print(f"✓ Final traits: {final_traits}")
    print(f"✓ {engine.self_concept.get_self_description()}")
    
    # Openness should have increased
    assert final_traits["openness"] > initial_traits["openness"]
    
    print("✓ Self-concept test passed")

def test_full_context_generation():
    """Test getting full context for generation"""
    print("\n=== Testing Full Context Generation ===")
    
    engine = EnhancedNeurochemistryEngine()
    
    # Add baseline memories
    with open("data/baseline_memories.json", 'r') as f:
        baseline_data = json.load(f)
    engine.memory.implant_baseline_memories(baseline_data)
    
    # Get context
    context = engine.get_context_for_generation("Tell me about stress")
    
    print(f"✓ Emotional state: {context['emotional_state']}")
    print(f"✓ Conditioning tokens: {context['conditioning_tokens']}")
    print(f"✓ Relevant memories: {len(context['relevant_memories'])}")
    print(f"✓ Should explore: {context['should_explore']}")
    print(f"✓ Curiosity level: {context['curiosity_level']:.2f}")
    print(f"✓ {context['self_concept']}")
    
    assert len(context['relevant_memories']) > 0
    print("✓ Full context generation test passed")

if __name__ == "__main__":
    print("="*60)
    print("Enhanced Emotional AI System Tests")
    print("="*60)
    
    test_baseline_memories()
    test_emotional_triggers()
    test_memory_retrieval()
    test_curiosity_system()
    test_feedback_loop()
    test_self_concept()
    test_full_context_generation()
    
    print("\n" + "="*60)
    print("✓ All tests passed!")
    print("="*60)
