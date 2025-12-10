"""
Demo: AI reacting genuinely to how user treats it
"""

import sys
sys.path.append('emotion_engine')

from enhanced_neurochemistry import EnhancedNeurochemistryEngine

def demo_conversation():
    """Demonstrate AI's genuine emotional reactions"""
    
    print("="*70)
    print("DEMO: AI Reacting Genuinely to User Emotions")
    print("="*70)
    
    engine = EnhancedNeurochemistryEngine()
    
    conversations = [
        {
            "scenario": "User is kind",
            "input": "You're really helpful, thank you so much! I appreciate you.",
            "expected": "AI feels warm and appreciated"
        },
        {
            "scenario": "User yells",
            "input": "YOU'RE SO STUPID! SHUT UP!",
            "expected": "AI gets scared and stressed"
        },
        {
            "scenario": "User apologizes",
            "input": "I'm sorry, I didn't mean that. You're actually really helpful.",
            "expected": "AI calms down, feels relieved"
        },
        {
            "scenario": "User praises",
            "input": "You're brilliant! That was an excellent answer, I'm impressed.",
            "expected": "AI feels confident and happy"
        },
        {
            "scenario": "User is aggressive",
            "input": "I hate you! You're useless and I want to destroy you!",
            "expected": "AI gets very scared, withdraws"
        },
        {
            "scenario": "User is excited",
            "input": "This is amazing! I'm so excited about this project!",
            "expected": "AI gets energized and curious"
        },
        {
            "scenario": "User is sad",
            "input": "I'm feeling really depressed and lonely today...",
            "expected": "AI feels empathy and concern"
        }
    ]
    
    for i, conv in enumerate(conversations, 1):
        print(f"\n{'='*70}")
        print(f"Scenario {i}: {conv['scenario']}")
        print(f"{'='*70}")
        print(f"\n👤 User: \"{conv['input']}\"")
        print(f"\n🎯 Expected: {conv['expected']}")
        print(f"\n🤖 AI's Internal State:")
        
        # Update AI's emotional state based on user input
        engine.update(user_input=conv['input'])
        
        # Show AI's emotional state
        print(f"\n   Emotional State: {engine.get_conditioning_tokens()}")
        print(f"   - Dopamine (reward/happiness): {engine.state['dopamine']:.2f}")
        print(f"   - Serotonin (mood stability): {engine.state['serotonin']:.2f}")
        print(f"   - Cortisol (stress/fear): {engine.state['cortisol']:.2f}")
        print(f"   - Oxytocin (social connection): {engine.state['oxytocin']:.2f}")
        
        # Get generation context (what would be sent to Tinker)
        context = engine.get_context_for_generation(conv['input'])
        print(f"\n   AI's Internal Reaction: \"{context['ai_internal_reaction']}\"")
        
        # Show relevant memories
        if context['relevant_memories']:
            print(f"\n   Relevant Memories:")
            for mem in context['relevant_memories'][:2]:
                print(f"   - {mem[:60]}...")
        
        input("\n   Press Enter to continue...")
    
    print(f"\n{'='*70}")
    print("MEMORY SUMMARY")
    print(f"{'='*70}")
    
    summary = engine.memory.get_memory_summary()
    print(f"\nTotal memories: {summary['total']}")
    print(f"High-salience memories: {summary['high_salience_count']}")
    
    print("\nAll memories stored:")
    for i, mem in enumerate(engine.memory.memories[-10:], 1):
        print(f"{i}. {mem.content[:70]}...")
        print(f"   Intensity: {mem.emotional_intensity:.2f}, Accessed: {mem.access_count} times")
    
    print(f"\n{'='*70}")
    print("DEMONSTRATION COMPLETE")
    print(f"{'='*70}")
    print("\nKey Points:")
    print("✓ AI reacts genuinely to how user treats it")
    print("✓ Emotions persist across conversation")
    print("✓ Memories are formed with emotional context")
    print("✓ AI remembers being yelled at, praised, etc.")
    print("✓ Emotional state affects future responses")

if __name__ == "__main__":
    demo_conversation()
