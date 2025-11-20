# Emotional AI System

A research project exploring neurochemistry-based emotional modeling for AI systems using Tinker API's LoRA fine-tuning and real-time state management.

## Architecture

- **Emotion Engine**: FastAPI service managing neurochemical state via ODE simulation
- **Training Pipeline**: Tinker API integration for LoRA-based fine-tuning
- **Base Model**: Llama-3.2-3B
- **Real-time Updates**: WebSocket for state synchronization
- **MCP Integration**: Kiro IDE integration for emotion state access

## Project Structure

```
.
├── specs/                     # Kiro spec files (requirements, design, tasks)
├── emotion_engine/            # Neurochemistry service
│   ├── server.py             # FastAPI + MCP server
│   └── neurochemistry.py     # ODE-based state simulation
├── training/                  # Training scripts
│   ├── train.py              # Main Tinker training pipeline
│   ├── data_prep.py          # Dataset preparation
│   └── tinker_example.py     # Tinker API usage examples
├── inference/                 # Inference service
│   ├── service.py            # Basic inference
│   └── tinker_inference.py   # Tinker-based inference with emotion
├── tests/                     # Test suite
├── config.py                  # Configuration management
├── .env.example              # Environment variables template
└── .kiro/settings/mcp.json   # MCP server configuration
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Tinker API

Create a `.env` file with your Tinker API credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```bash
TINKER_API_KEY=your_tinker_api_key_here
TINKER_API_URL=https://api.tinker.ai/v1

MODEL_NAME=meta-llama/Llama-3.2-3B
LORA_RANK=64
LEARNING_RATE=0.001

EMOTION_ENGINE_URL=ws://localhost:8000/ws
```

### 3. Prepare Training Data

```bash
python training/data_prep.py
```

This creates `training_data.jsonl` with emotional state annotations.

### 4. Start Emotion Engine

In one terminal:

```bash
python emotion_engine/server.py
```

The emotion engine will run on `http://localhost:8000` with:
- REST API for MCP tools
- WebSocket endpoint at `/ws`

### 5. Run Training

In another terminal:

```bash
python training/train.py
```

This will:
1. Train base model with emotional conditioning
2. Train separate LoRA adapters for each emotional state
3. Save checkpoints to `checkpoints/`
4. Save LoRA adapters to `loras/`

### 6. Run Inference

```bash
python inference/tinker_inference.py
```

## Tinker API Usage

The system uses Tinker's low-level training primitives:

```python
from tinker import TinkerClient

# Initialize with API key
client = TinkerClient(
    api_key="your_api_key",
    model="meta-llama/Llama-3.2-3B",
    lora_rank=64
)

# Training loop
loss = client.forward_backward(input_ids=input_text, labels=target_text)
client.backward(loss)
client.optim_step()

# Multiple LoRA adapters
client.init_lora(name="high_dopamine")
# ... train ...
client.save_lora("high_dopamine", "loras/high_dopamine.pt")

# Dynamic blending
client.blend_loras(
    lora_weights={"high_dopamine": 0.7, "balanced": 0.3},
    lora_adapters={"high_dopamine": "loras/high_dopamine.pt", ...}
)

# Generation
output = client.sample(prompt=text, max_tokens=200, temperature=0.9)
```

## Kiro MCP Integration

The emotion engine is configured as an MCP server in `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "emotion_engine": {
      "command": "python",
      "args": ["emotion_engine/server.py"],
      "autoApprove": ["get_emotional_state", "update_emotion"]
    }
  }
}
```

Available MCP tools:
- `get_emotional_state` - Get current neurochemistry
- `update_emotion` - Update emotional state based on interaction

## Neurochemistry Model

Four neurochemical variables (0.0-1.0):

- **Dopamine**: Reward/curiosity - affects exploration and creativity
- **Serotonin**: Mood stability - affects emotional baseline
- **Cortisol**: Stress/vigilance - affects caution and anxiety
- **Oxytocin**: Social bonding - affects empathy and connection

State updates via differential equations with decay rates and interaction signals.

## Testing

```bash
# Test neurochemistry engine
python tests/test_neurochemistry.py

# Test Tinker API integration
python training/tinker_example.py
```

## Development Workflow

1. **Spec-driven**: Update specs in `specs/` directory
2. **Train**: Modify training pipeline in `training/train.py`
3. **Test**: Run emotion engine and inference service
4. **Iterate**: Adjust neurochemistry parameters and LoRA blending weights

## Notes

- The system uses conditioning tokens like `<DA=0.75><SE=0.60>` to influence model behavior
- LoRA adapters are dynamically blended based on real-time neurochemical state
- Temperature is adjusted based on dopamine levels (higher = more creative)
- Curiosity rewards are applied during training for high dopamine states
