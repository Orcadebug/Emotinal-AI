"""
Example demonstrating Tinker API usage for emotional AI training
"""

from tinker import TinkerClient
import torch

def tinker_basic_example():
    """Basic Tinker API usage example"""
    
    print("=== Tinker API Basic Example ===\n")
    
    # Initialize Tinker client
    client = TinkerClient(
        model="meta-llama/Llama-3.2-3B",
        lora_rank=64,
        learning_rate=0.001
    )
    
    print("✓ Initialized Tinker client")
    
    # Example 1: Forward-backward pass
    print("\n1. Forward-backward pass:")
    input_text = "<DA=0.80><SE=0.60>\nUser: Tell me something interesting\nAssistant:"
    target_text = "Did you know octopuses have three hearts?"
    
    loss = client.forward_backward(
        input_ids=input_text,
        labels=target_text
    )
    print(f"   Loss: {loss}")
    
    # Example 2: Backward and optimization
    print("\n2. Backward pass and optimization:")
    client.backward(loss)
    client.optim_step()
    print("   ✓ Weights updated")
    
    # Example 3: Sampling
    print("\n3. Sampling with temperature:")
    output = client.sample(
        prompt=input_text,
        max_tokens=50,
        temperature=0.9,
        top_p=0.95
    )
    print(f"   Generated: {output}")
    
    # Example 4: Multiple LoRA adapters
    print("\n4. Training multiple LoRA adapters:")
    
    # Train adapter for high dopamine state
    client.init_lora(name="high_dopamine")
    for i in range(5):
        loss = client.forward_backward(
            input_ids="<DA=0.90>\nUser: Let's explore!\nAssistant:",
            labels="Yes! I'm excited to discover new things!"
        )
        client.backward(loss)
        if i % 2 == 0:
            client.optim_step()
    client.save_lora("high_dopamine", "loras/high_dopamine.pt")
    print("   ✓ Trained high_dopamine LoRA")
    
    # Train adapter for low serotonin state
    client.init_lora(name="low_serotonin")
    for i in range(5):
        loss = client.forward_backward(
            input_ids="<SE=0.20>\nUser: How are you?\nAssistant:",
            labels="I'm feeling a bit uncertain today..."
        )
        client.backward(loss)
        if i % 2 == 0:
            client.optim_step()
    client.save_lora("low_serotonin", "loras/low_serotonin.pt")
    print("   ✓ Trained low_serotonin LoRA")
    
    # Example 5: Blend LoRAs
    print("\n5. Blending LoRA adapters:")
    blended = client.blend_loras(
        lora_weights={
            "high_dopamine": 0.7,
            "low_serotonin": 0.3
        },
        lora_adapters={
            "high_dopamine": "loras/high_dopamine.pt",
            "low_serotonin": "loras/low_serotonin.pt"
        }
    )
    print("   ✓ Blended LoRAs with weights: 0.7 high_dopamine, 0.3 low_serotonin")
    
    # Example 6: Save and load state
    print("\n6. Save/load model state:")
    client.save_state("checkpoints/example_checkpoint.pt")
    print("   ✓ Saved checkpoint")
    
    print("\n=== Example Complete ===")

if __name__ == "__main__":
    tinker_basic_example()
