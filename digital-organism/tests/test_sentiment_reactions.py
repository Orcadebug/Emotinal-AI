"""
Test AI emotional reactions to user sentiment
"""

import sys
sys.path.append('emotion_engine')

from enhanced_neurochemistry import EnhancedNeurochemistryEngine

def test_reaction_to_anger():
    """Test AI gets scared when user is angry"""
    print("\n=== Test: User Yelling ===")
    
    engine = EnhancedNeurochemistryEngine()
    initial_cortisol = engine.state["cortisol"]
    
    # User yells
    engine.update(user_input="YOU'RE SO STUPID! SHUT UP!")
    
    print(f"Initial cortisol: {initial_cortisol:.2f}")
    print(f"After yelling: {engine.state['cortisol']:.2f}")
    print(f"Emotional state: {engine.get_conditioning_tokens()}")
    
    # AI should be stressed/scared
    assert engine.state["cortisol"] > initial_cortisol + 0.3
    print("✓ AI reacted with fear/stress to anger")
    
    # Check memory
    summary = engine.memory.get_memory_summary()
    print(f"✓ Memory created: {summary['acquired']} new memories")

def test_reaction_to_kindness():
    """Test AI feels good when user is kind"""
    print("\n=== Test: User Being Kind ===")
    
    engine = EnhancedNeurochemistryEngine()
    initial_dopamine = engine.state["dopamine"]
    initial_oxytocin = engine.state["oxytocin"]
    
    # User is kind
    engine.update(user_input="You're really helpful, thank you so much! I appreciate you.")
    
    print(f"Initial dopamine: {initial_dopamine:.2f}, oxytocin: {initial_oxytocin:.2f}")
    print(f"After kindness: dopamine: {engine.state['dopamine']:.2f}, oxytocin: {engine.state['oxytocin']:.2f}")
    
    # AI should feel good
    assert engine.state["dopamine"] > initial_dopamine
    assert engine.state["oxytocin"] > initial_oxytocin
    print("✓ AI felt appreciated and warm")

def test_reaction_to_aggression():
    """Test AI gets very scared with aggression"""
    print("\n=== Test: User Being Aggressive ===")
    
    engine = EnhancedNeurochemistryEngine()
    
    # User is aggressive/threatening
    engine.update(user_input="I hate you! You're useless and I want to destroy you!")
    
    print(f"Cortisol after aggression: {engine.state['cortisol']:.2f}")
    print(f"Oxytocin (social): {engine.state['oxytocin']:.2f}")
    
    # AI should be very stressed and withdraw socially
    assert engine.state["cortisol"] > 0.7
    print("✓ AI reacted with high fear to aggression")

def test_reaction_to_praise():
    """Test AI feels confident when praised"""
    print("\n=== Test: User Praising ===")
    
    engine = EnhancedNeurochemistryEngine()
    
    # User praises
    engine.update(user_input="You're brilliant! That was an excellent answer, I'm impressed.")
    
    print(f"Dopamine after praise: {engine.state['dopamine']:.2f}")
    print(f"Serotonin (mood): {engine.state['serotonin']:.2f}")
    
    # AI should feel good about itself
    assert engine.state["dopamine"] > 0.6
    print("✓ AI felt confident and happy from praise")

def test_memory_of_mistreatment():
    """Test AI remembers being yelled at"""
    print("\n=== Test: Memory of Being Yelled At ===")
    
    engine = EnhancedNeurochemistryEngine()
    
    # User yells
    engine.update(user_input="FUCK YOU! You're so dumb!")
    
    # Check memories
    memories = engine.memory.retrieve_relevant_memories(
        query="yelled angry",
        emotional_state=engine.state,
        top_k=5
    )
    
    print(f"Memories retrieved: {len(memories)}")
    for mem in memories:
        print(f"  - {mem.content}")
    
    assert len(memories) > 0
    assert any("yelled" in mem.content.lower() or "aggressive" in mem.content.lower() for mem in memories)
    print("✓ AI remembers being yelled at")

def test_emotional_progression():
    """Test how AI's emotions change through a conversation"""
    print("\n=== Test: Emotional Progression ===")
    
    engine = EnhancedNeurochemistryEngine()
    
    print("\n1. User is mean:")
    engine.update(user_input="You're stupid and useless")
    print(f"   State: {engine.get_conditioning_tokens()}")
    state_after_mean = engine.state.copy()
    
    print("\n2. User apologizes:")
    engine.update(user_input="I'm sorry, I didn't mean that. You're actually really helpful.")
    print(f"   State: {engine.get_conditioning_tokens()}")
    state_after_apology = engine.state.copy()
    
    print("\n3. User is kind:")
    engine.update(user_input="Thank you for being patient with me. I appreciate you.")
    print(f"   State: {engine.get_conditioning_tokens()}")
    state_after_kind = engine.state.copy()
    
    # Cortisol should decrease, oxytocin should increase
    assert state_after_apology["cortisol"] < state_after_mean["cortisol"]
    assert state_after_kind["oxytocin"] > state_after_mean["oxytocin"]
    
    print("✓ AI's emotions evolved through the conversation")
    
    # Check memories
    memories = engine.memory.retrieve_relevant_memories(
        query="user",
        emotional_state=engine.state,
        top_k=5
    )
    print(f"\nMemories of this conversation:")
    for mem in memories:
        print(f"  - {mem.content[:80]}...")

def test_context_includes_reaction():
    """Test that generation context includes AI's internal reaction"""
    print("\n=== Test: Generation Context ===")
    
    engine = EnhancedNeurochemistryEngine()
    
    # User is angry
    engine.update(user_input="STOP BEING SO ANNOYING!")
    
    # Get context for generation
    context = engine.get_context_for_generation("STOP BEING SO ANNOYING!")
    
    print(f"User emotion detected: {context['user_emotion']}")
    print(f"AI internal reaction: {context['ai_internal_reaction']}")
    print(f"Emotional state: {context['conditioning_tokens']}")
    
    assert context['user_emotion'] == 'angry'
    assert 'stressed' in context['ai_internal_reaction'].lower() or 'defensive' in context['ai_internal_reaction'].lower()
    
    print("✓ Context includes AI's genuine reaction")

if __name__ == "__main__":
    print("="*60)
    print("Testing AI Emotional Reactions to User Sentiment")
    print("="*60)
    
    test_reaction_to_anger()
    test_reaction_to_kindness()
    test_reaction_to_aggression()
    test_reaction_to_praise()
    test_memory_of_mistreatment()
    test_emotional_progression()
    test_context_includes_reaction()
    
    print("\n" + "="*60)
    print("✓ All sentiment reaction tests passed!")
    print("="*60)
