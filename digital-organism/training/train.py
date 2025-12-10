"""
Training script for emotional AI using Tinker API
"""

import json
import sys
from typing import Dict, List
from tinker import TinkerClient
import torch
import numpy as np

# Add parent directory to path for config import
sys.path.append('..')
from config import TinkerConfig, PathConfig

class EmotionalLLMTrainer:
    """Trainer for emotional AI with multiple LoRA adapters using Tinker API"""
    
    def __init__(self, model_name: str = None, lora_rank: int = None, api_key: str = None):
        # Validate and load config
        TinkerConfig.validate()
        PathConfig.ensure_dirs()
        
        self.model_name = model_name or TinkerConfig.MODEL_NAME
        self.lora_rank = lora_rank or TinkerConfig.LORA_RANK
        self.emotional_loras = {}
        
        # Initialize Tinker client with API key
        self.client = TinkerClient(
            api_key=api_key or TinkerConfig.API_KEY,
            api_url=TinkerConfig.API_URL,
            model=self.model_name,
            lora_rank=self.lora_rank,
            learning_rate=TinkerConfig.LEARNING_RATE
        )
        
        print(f"✓ Initializing Tinker trainer for {self.model_name}")
        print(f"✓ LoRA rank: {self.lora_rank}")
        print(f"✓ API URL: {TinkerConfig.API_URL}")
    
    def train_base_model(self, dataset: List[Dict], epochs: int = 3):
        """Stage 1: Train base model with emotional conditioning using Tinker"""
        print("\n=== Stage 1: Base Model Training ===")
        print(f"Training on {len(dataset)} examples for {epochs} epochs")
        
        for epoch in range(epochs):
            print(f"\nEpoch {epoch + 1}/{epochs}")
            total_loss = 0
            
            for idx, batch in enumerate(dataset):
                # Add emotional conditioning tokens to input
                conditioning = batch["conditioning_tokens"]
                input_text = f"{conditioning}\nUser: {batch.get('input', '')}\nAssistant:"
                target_text = batch.get('target', '')
                
                # Tinker forward_backward pass
                loss = self.client.forward_backward(
                    input_ids=input_text,
                    labels=target_text
                )
                
                # Add curiosity reward for high dopamine states
                if batch["emotional_state"]["dopamine"] > 0.7:
                    # Sample output to calculate novelty
                    with torch.no_grad():
                        output = self.client.sample(
                            prompt=input_text,
                            max_tokens=50,
                            temperature=1.2
                        )
                        
                        # Calculate novelty reward
                        unique_tokens = len(set(output.split()))
                        total_tokens = len(output.split())
                        novelty_reward = unique_tokens / total_tokens if total_tokens > 0 else 0
                        
                        # Modify loss with curiosity bonus
                        loss = loss - 0.1 * novelty_reward
                
                # Backward pass
                self.client.backward(loss)
                
                # Optimization step every 4 batches (gradient accumulation)
                if (idx + 1) % 4 == 0:
                    self.client.optim_step()
                
                total_loss += loss.item() if hasattr(loss, 'item') else loss
                
                if (idx + 1) % 10 == 0:
                    avg_loss = total_loss / (idx + 1)
                    print(f"  Batch {idx + 1}/{len(dataset)}, Avg Loss: {avg_loss:.4f}")
            
            # Save checkpoint after each epoch
            checkpoint_path = f"{PathConfig.CHECKPOINTS_DIR}/emotional_base_epoch_{epoch}.pt"
            self.client.save_state(checkpoint_path)
            print(f"  Saved checkpoint: {checkpoint_path}")
    
    def train_emotional_adapters(self, dataset: List[Dict], epochs: int = 2):
        """Stage 2: Train separate LoRA adapters for emotional states using Tinker"""
        print("\n=== Stage 2: Emotional Adapter Training ===")
        
        emotional_states = {
            "high_dopamine": lambda d: d["dopamine"] > 0.7,
            "low_serotonin": lambda d: d["serotonin"] < 0.3,
            "high_stress": lambda d: d["cortisol"] > 0.7,
            "balanced": lambda d: all(0.4 <= d[k] <= 0.6 for k in d)
        }
        
        for state_name, filter_fn in emotional_states.items():
            print(f"\nTraining {state_name} adapter...")
            
            # Filter dataset for this emotional state
            state_data = [d for d in dataset if filter_fn(d["emotional_state"])]
            print(f"  Examples: {len(state_data)}")
            
            if len(state_data) == 0:
                print(f"  Skipping {state_name} - no training data")
                continue
            
            # Initialize new LoRA adapter for this emotional state
            self.client.init_lora(name=state_name)
            
            # Train this specific adapter
            for epoch in range(epochs):
                total_loss = 0
                
                for idx, batch in enumerate(state_data):
                    conditioning = batch["conditioning_tokens"]
                    input_text = f"{conditioning}\nUser: {batch.get('input', '')}\nAssistant:"
                    target_text = batch.get('target', '')
                    
                    # Tinker forward_backward
                    loss = self.client.forward_backward(
                        input_ids=input_text,
                        labels=target_text
                    )
                    
                    self.client.backward(loss)
                    
                    if (idx + 1) % 4 == 0:
                        self.client.optim_step()
                    
                    total_loss += loss.item() if hasattr(loss, 'item') else loss
                
                avg_loss = total_loss / len(state_data)
                print(f"    Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.4f}")
            
            # Save this emotional LoRA adapter
            lora_path = f"{PathConfig.LORAS_DIR}/lora_{state_name}.pt"
            self.client.save_lora(state_name, lora_path)
            self.emotional_loras[state_name] = lora_path
            print(f"  Saved LoRA: {lora_path}")
    
    def blend_loras(self, neurochemistry_state: Dict[str, float]):
        """Blend LoRA adapters based on current emotional state using Tinker"""
        
        # Calculate weights for each adapter
        weights = {
            "high_dopamine": neurochemistry_state["dopamine"] ** 2,
            "low_serotonin": (1 - neurochemistry_state["serotonin"]) ** 2,
            "high_stress": neurochemistry_state["cortisol"] ** 2,
            "balanced": sum([
                1 - abs(neurochemistry_state[k] - 0.5) 
                for k in neurochemistry_state
            ]) / 4
        }
        
        # Normalize weights
        total = sum(weights.values())
        if total > 0:
            weights = {k: v/total for k, v in weights.items()}
        
        print(f"LoRA blend weights: {weights}")
        
        # Use Tinker to blend LoRA adapters
        blended_lora = self.client.blend_loras(
            lora_weights=weights,
            lora_adapters=self.emotional_loras
        )
        
        return blended_lora
    
    def generate_with_emotion(self, prompt: str, neurochemistry_state: Dict[str, float], 
                             max_tokens: int = 200) -> str:
        """Generate response with emotional conditioning using Tinker"""
        
        # Blend LoRAs based on current emotional state
        self.blend_loras(neurochemistry_state)
        
        # Create conditioning tokens
        conditioning = (
            f"<DA={neurochemistry_state['dopamine']:.2f}>"
            f"<SE={neurochemistry_state['serotonin']:.2f}>"
            f"<CR={neurochemistry_state['cortisol']:.2f}>"
            f"<OX={neurochemistry_state['oxytocin']:.2f}>"
        )
        
        # Generate with Tinker
        full_prompt = f"{conditioning}\nUser: {prompt}\nAssistant:"
        
        # Adjust temperature based on dopamine (higher dopamine = more creative)
        temperature = 0.8 + 0.4 * neurochemistry_state["dopamine"]
        
        output = self.client.sample(
            prompt=full_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=0.9
        )
        
        return output

def main():
    """Main training pipeline"""
    
    print("=== Emotional AI Training Pipeline ===\n")
    
    # Load training data
    try:
        with open(PathConfig.TRAINING_DATA, 'r') as f:
            dataset = [json.loads(line) for line in f]
        print(f"✓ Loaded {len(dataset)} training examples")
    except FileNotFoundError:
        print(f"Error: Training data not found at {PathConfig.TRAINING_DATA}")
        print("Run 'python training/data_prep.py' first to generate training data")
        return
    
    # Initialize trainer (will use config from .env)
    try:
        trainer = EmotionalLLMTrainer()
    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        print("\nPlease create a .env file with your Tinker API key:")
        print("  cp .env.example .env")
        print("  # Then edit .env and add your TINKER_API_KEY")
        return
    
    # Run training stages
    trainer.train_base_model(dataset)
    trainer.train_emotional_adapters(dataset)
    
    print("\n=== Training Complete ===")
    print(f"✓ Emotional LoRAs: {list(trainer.emotional_loras.keys())}")
    print(f"✓ Checkpoints saved to: {PathConfig.CHECKPOINTS_DIR}/")
    print(f"✓ LoRAs saved to: {PathConfig.LORAS_DIR}/")

if __name__ == "__main__":
    main()
