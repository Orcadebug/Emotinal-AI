"""
Inference service using Tinker API with real-time emotional state
"""

import asyncio
import websockets
import json
import sys
from typing import Dict
from tinker import TinkerClient

# Add parent directory to path for config import
sys.path.append('..')
from config import TinkerConfig, EmotionConfig, PathConfig

class TinkerEmotionalInference:
    """Inference service using Tinker API"""
    
    def __init__(
        self, 
        model_path: str = None,
        emotion_engine_url: str = None,
        api_key: str = None
    ):
        # Validate config
        TinkerConfig.validate()
        
        self.emotion_engine_url = emotion_engine_url or EmotionConfig.ENGINE_URL
        self.emotion_ws = None
        self.current_state = {}
        
        # Use default checkpoint path if not provided
        if model_path is None:
            model_path = f"{PathConfig.CHECKPOINTS_DIR}/emotional_base_final.pt"
        
        # Initialize Tinker client
        print("Loading Tinker model...")
        self.client = TinkerClient.load(
            model_path,
            api_key=api_key or TinkerConfig.API_KEY,
            api_url=TinkerConfig.API_URL
        )
        
        # Load emotional LoRA adapters
        self.lora_adapters = {
            "high_dopamine": f"{PathConfig.LORAS_DIR}/lora_high_dopamine.pt",
            "low_serotonin": f"{PathConfig.LORAS_DIR}/lora_low_serotonin.pt",
            "high_stress": f"{PathConfig.LORAS_DIR}/lora_high_stress.pt",
            "balanced": f"{PathConfig.LORAS_DIR}/lora_balanced.pt"
        }
        print("✓ Tinker model loaded")
        print(f"✓ Using emotion engine: {self.emotion_engine_url}")
    
    async def connect(self):
        """Connect to emotion engine"""
        self.emotion_ws = await websockets.connect(self.emotion_engine_url)
        print(f"✓ Connected to emotion engine")
    
    async def get_emotional_state(self) -> Dict:
        """Get current emotional state from engine"""
        await self.emotion_ws.send(json.dumps({"action": "get_state"}))
        response = await self.emotion_ws.recv()
        data = json.loads(response)
        self.current_state = data["state"]
        return data
    
    async def update_emotions(self, reward=0.0, stress=0.0, social=0.0, novelty=0.0):
        """Update emotional state"""
        await self.emotion_ws.send(json.dumps({
            "action": "update",
            "reward": reward,
            "stress": stress,
            "social": social,
            "novelty": novelty
        }))
        response = await self.emotion_ws.recv()
        data = json.loads(response)
        self.current_state = data["state"]
        return data
    
    def calculate_lora_weights(self, state: Dict[str, float]) -> Dict[str, float]:
        """Calculate LoRA blend weights from emotional state"""
        weights = {
            "high_dopamine": state["dopamine"] ** 2,
            "low_serotonin": (1 - state["serotonin"]) ** 2,
            "high_stress": state["cortisol"] ** 2,
            "balanced": sum([1 - abs(state[k] - 0.5) for k in state]) / 4
        }
        
        # Normalize
        total = sum(weights.values())
        if total > 0:
            weights = {k: v/total for k, v in weights.items()}
        
        return weights
    
    async def generate_response(self, user_input: str, max_tokens: int = 200) -> str:
        """Generate emotionally-conditioned response using Tinker"""
        
        # Get current emotional state
        emotion_data = await self.get_emotional_state()
        state = emotion_data["state"]
        conditioning = emotion_data["tokens"]
        
        print(f"\nCurrent emotional state: {state}")
        print(f"Conditioning tokens: {conditioning}")
        
        # Calculate and blend LoRA adapters
        lora_weights = self.calculate_lora_weights(state)
        print(f"LoRA weights: {lora_weights}")
        
        self.client.blend_loras(
            lora_weights=lora_weights,
            lora_adapters=self.lora_adapters
        )
        
        # Prepare prompt with conditioning
        full_prompt = f"{conditioning}\nUser: {user_input}\nAssistant:"
        
        # Adjust temperature based on dopamine (higher = more creative)
        temperature = 0.7 + 0.5 * state["dopamine"]
        
        # Generate with Tinker
        response = self.client.sample(
            prompt=full_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=0.9
        )
        
        # Update emotions based on interaction
        # Simple heuristics for demo
        novelty_score = len(set(response.split())) / len(response.split()) if response else 0
        
        await self.update_emotions(
            reward=0.1,
            stress=0.0,
            social=0.15 if any(word in user_input.lower() for word in ["we", "us", "together"]) else 0.0,
            novelty=novelty_score * 0.2
        )
        
        return response

async def main():
    """Test Tinker inference service"""
    
    print("=== Tinker Emotional Inference Test ===\n")
    
    service = TinkerEmotionalInference()
    await service.connect()
    
    # Test interactions
    test_prompts = [
        "Tell me something interesting!",
        "I'm feeling stressed about work",
        "Let's work on this together"
    ]
    
    for prompt in test_prompts:
        print(f"\n{'='*60}")
        print(f"User: {prompt}")
        response = await service.generate_response(prompt)
        print(f"Assistant: {response}")
        print(f"{'='*60}")
        
        # Wait a bit between interactions
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
