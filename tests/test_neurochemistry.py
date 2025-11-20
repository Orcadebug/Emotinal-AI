import sys
sys.path.append('emotion_engine')

from neurochemistry import NeurochemistryEngine

def test_initialization():
    """Test engine initialization"""
    engine = NeurochemistryEngine()
    state = engine.get_state()
    
    assert state["dopamine"] == 0.5
    assert state["serotonin"] == 0.5
    assert state["cortisol"] == 0.3
    assert state["oxytocin"] == 0.4
    print("✓ Initialization test passed")

def test_reward_update():
    """Test dopamine increase with reward"""
    engine = NeurochemistryEngine()
    initial_da = engine.state["dopamine"]
    
    engine.update(reward=1.0)
    
    assert engine.state["dopamine"] > initial_da
    print("✓ Reward update test passed")

def test_stress_update():
    """Test cortisol increase with stress"""
    engine = NeurochemistryEngine()
    initial_cr = engine.state["cortisol"]
    
    engine.update(stress=1.0)
    
    assert engine.state["cortisol"] > initial_cr
    print("✓ Stress update test passed")

def test_state_bounds():
    """Test that state values stay in [0, 1]"""
    engine = NeurochemistryEngine()
    
    # Extreme updates
    for _ in range(100):
        engine.update(reward=1.0, stress=1.0, social=1.0, novelty=1.0)
    
    state = engine.get_state()
    for key, value in state.items():
        assert 0.0 <= value <= 1.0, f"{key} out of bounds: {value}"
    
    print("✓ State bounds test passed")

def test_conditioning_tokens():
    """Test conditioning token generation"""
    engine = NeurochemistryEngine()
    tokens = engine.get_conditioning_tokens()
    
    assert "<DA=" in tokens
    assert "<SE=" in tokens
    assert "<CR=" in tokens
    assert "<OX=" in tokens
    print("✓ Conditioning tokens test passed")

if __name__ == "__main__":
    test_initialization()
    test_reward_update()
    test_stress_update()
    test_state_bounds()
    test_conditioning_tokens()
    print("\n✓ All tests passed!")
