"""
Demo of the Organic Emotional AI System
Shows memory recall, neuroplasticity, and emotional evolution
"""

from emotion_engine.integrated_engine import IntegratedNeurochemistryEngine


def demo_organic_system():
    """Demonstrate the complete organic emotional AI system"""
    
    print("=" * 60)
    print("ORGANIC EMOTIONAL AI - DEMO")
    print("=" * 60)
    
    # Initialize the engine
    engine = IntegratedNeurochemistryEngine()
    
    print("\n[INITIAL STATE]")
    status = engine.get_full_status()
    print(f"Neurochemistry: {status['neurochemistry']}")
    print(f"Desire: {status['desire']}")
    print(f"Age: {status['plasticity']['age']} interactions")
    print(f"Plasticity: {status['plasticity']['plasticity']:.4f}")
    
    # Simulate interactions
    interactions = [
        {
            "user_input": "Let's build something with cursor!",
            "stimulus": {"dopamine": 0.3, "cortisol": -0.1},
            "description": "User mentions coding/cursor (should trigger DOP_01 memory)"
        },
        {
            "user_input": "I'm worried about dropping out of school",
            "stimulus": {"cortisol": 0.4, "serotonin": -0.2},
            "description": "User mentions dropout (should trigger CORT_MIX_01 memory)"
        },
        {
            "user_input": "Tell me about your failures",
            "stimulus": {"serotonin": -0.3, "cortisol": 0.2},
            "description": "User asks about failure (should trigger SERO_LOW_01 memory)"
        },
        {
            "user_input": "I just need someone to listen",
            "stimulus": {"oxytocin": 0.4, "cortisol": -0.1},
            "description": "User needs support (should trigger OXY_HIGH_01 memory)"
        },
        {
            "user_input": "What's your morning routine?",
            "stimulus": {"serotonin": 0.2, "dopamine": 0.1},
            "description": "User asks about routine (should trigger SERO_PEACE_01 memory)"
        }
    ]
    
    print("\n" + "=" * 60)
    print("SIMULATING INTERACTIONS")
    print("=" * 60)
    
    for i, interaction in enumerate(interactions, 1):
        print(f"\n--- Interaction {i} ---")
        print(f"Description: {interaction['description']}")
        print(f"User: {interaction['user_input']}")
        
        # Update neurochemistry
        engine.update_neurochemistry(interaction['stimulus'])
        
        # Get context (includes memory recall)
        context = engine.get_prompt_context(interaction['user_input'])
        print(f"\n{context}")
        
        print(f"\nCurrent Desire: {engine.current_desire}")
    
    # Show final state
    print("\n" + "=" * 60)
    print("FINAL STATE (After Growth)")
    print("=" * 60)
    
    final_status = engine.get_full_status()
    print(f"\nNeurochemistry: {final_status['neurochemistry']}")
    print(f"Desire: {final_status['desire']}")
    print(f"Age: {final_status['plasticity']['age']} interactions")
    print(f"Plasticity: {final_status['plasticity']['plasticity']:.4f}")
    print(f"Baseline: {final_status['plasticity']['baseline']}")
    
    print("\n" + "=" * 60)
    print("NEUROPLASTICITY EFFECT")
    print("=" * 60)
    print("Notice how the baseline has shifted from the initial 0.5 values")
    print("based on the emotional experiences during the interactions.")
    print("This is the AI 'growing up' and developing a personality.")


if __name__ == "__main__":
    demo_organic_system()
