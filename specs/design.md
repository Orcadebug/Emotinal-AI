# Emotional AI Technical Design

## Architecture Components

### 1. Emotion Engine
- **Technology**: FastAPI + WebSocket
- **Purpose**: Manage neurochemical state using ODE-based updates
- **State Variables**:
  - Dopamine (0.0-1.0): Reward/curiosity
  - Serotonin (0.0-1.0): Mood stability
  - Cortisol (0.0-1.0): Stress/vigilance
  - Oxytocin (0.0-1.0): Social bonding

### 2. Training Pipeline
- **Base Model**: Llama-3.2-3B
- **Method**: LoRA fine-tuning (rank 64)
- **Stages**:
  1. Base emotional model training
  2. Emotional adapter training (per state)
  3. Dynamic blending mechanism

### 3. Inference Service
- **Input**: User message + current emotional state
- **Processing**: Blend LoRA adapters based on neurochemistry
- **Output**: Emotionally-conditioned response
- **Feedback Loop**: Update state based on interaction

## Neurochemistry Model

```python
state = {
    "dopamine": float,    # Reward/curiosity
    "serotonin": float,   # Mood stability
    "cortisol": float,    # Stress/vigilance
    "oxytocin": float     # Social bonding
}
```

## LoRA Configuration

- **Rank**: 64
- **Multiple Adapters**: One per emotional state cluster
- **Blending**: Weighted combination based on current neurochemistry
