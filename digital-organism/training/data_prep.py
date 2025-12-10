from datasets import load_dataset
import json
from typing import List, Dict

def prepare_emotional_training_data() -> List[Dict]:
    """Prepare training data with emotional state annotations"""
    
    training_examples = []
    
    # Example emotional state configurations
    emotional_configs = [
        {
            "state": {"dopamine": 0.8, "serotonin": 0.6, "cortisol": 0.2, "oxytocin": 0.7},
            "label": "high_dopamine",
            "description": "Curious, energetic, optimistic"
        },
        {
            "state": {"dopamine": 0.3, "serotonin": 0.3, "cortisol": 0.7, "oxytocin": 0.3},
            "label": "high_stress",
            "description": "Anxious, cautious, vigilant"
        },
        {
            "state": {"dopamine": 0.5, "serotonin": 0.8, "cortisol": 0.3, "oxytocin": 0.6},
            "label": "balanced",
            "description": "Calm, stable, thoughtful"
        },
        {
            "state": {"dopamine": 0.4, "serotonin": 0.2, "cortisol": 0.6, "oxytocin": 0.3},
            "label": "low_serotonin",
            "description": "Melancholic, introspective, uncertain"
        }
    ]
    
    # Generate conditioning tokens
    for config in emotional_configs:
        state = config["state"]
        tokens = (
            f"<DA={state['dopamine']:.2f}>"
            f"<SE={state['serotonin']:.2f}>"
            f"<CR={state['cortisol']:.2f}>"
            f"<OX={state['oxytocin']:.2f}>"
        )
        config["tokens"] = tokens
    
    return emotional_configs

def create_training_dataset(output_path: str = "training_data.jsonl"):
    """Create JSONL training dataset"""
    
    configs = prepare_emotional_training_data()
    
    # Example training pairs
    examples = []
    for config in configs:
        example = {
            "emotional_state": config["state"],
            "conditioning_tokens": config["tokens"],
            "label": config["label"],
            "description": config["description"]
        }
        examples.append(example)
    
    # Save to JSONL
    with open(output_path, 'w') as f:
        for example in examples:
            f.write(json.dumps(example) + '\n')
    
    print(f"Created training dataset: {output_path}")
    print(f"Total examples: {len(examples)}")
    
    return examples

if __name__ == "__main__":
    create_training_dataset()
