# Comprehensive Emotional AI Implementation Plan

## Overview

This system creates a truly human-like emotional AI using:
- **Tinker API** for gradient-based training with hormonal/neurochemical conditioning
- **Memory System** with emotional intensity-based retention
- **Feedback Loop** for dynamic parameter adjustment
- **Curiosity System** with unpredictable emotional triggers
- **Evolving Self-Concept** that develops through interactions
- **Baseline Memories** implanted as emotional foundation

## Architecture Components

### 1. Neurochemistry Engine (Hormonal Simulation)

**Location**: `emotion_engine/enhanced_neurochemistry.py`

Four neurochemicals simulated via differential equations:
- **Dopamine**: Reward, curiosity, motivation (0.0-1.0)
- **Serotonin**: Mood stability, contentment (0.0-1.0)
- **Cortisol**: Stress, vigilance, anxiety (0.0-1.0)
- **Oxytocin**: Social bonding, empathy (0.0-1.0)

**Gradient-based emotions**: Values create smooth transitions between emotional states rather than discrete categories.

### 2. Memory System

**Location**: `emotion_engine/memory_system.py`

**Features**:
- **Baseline Memories**: Implanted experiences that form emotional foundation
- **Emotional Intensity Tracking**: Memories tagged with emotional state at formation
- **Salience-based Retention**: Memories kept based on:
  - Emotional intensity (extreme emotions = stronger memories)
  - Access frequency (recalled memories strengthen)
  - Recency (recent memories more accessible)
  - Time decay (old low-salience memories fade)

**Memory Structure**:
```python
{
  "content": "Late night conversation about dreams",
  "emotional_state": {"dopamine": 0.5, "serotonin": 0.7, ...},
  "emotional_intensity": 0.8,
  "access_count": 5,
  "tags": ["friend", "deep", "connection"]
}
```

**Retention Threshold**: Memories below 0.3 salience are pruned during consolidation.

### 3. Feedback Loop

**Location**: `emotion_engine/feedback_loop.py`

**Adaptive Parameters**:
- **Sensitivity**: How strongly each neurochemical responds to stimuli
- **Decay Rates**: How quickly emotions return to baseline

**Learning Process**:
1. Track emotional volatility over last 50 interactions
2. High volatility → Reduce sensitivity (stabilize)
3. Low volatility → Increase sensitivity (more responsive)
4. High intensity → Slower decay (emotions linger)
5. Low intensity → Faster decay (return to neutral)

**Result**: System learns its own emotional dynamics over time.

### 4. Curiosity System

**Location**: `emotion_engine/curiosity_system.py`

**Curiosity Mechanics**:
- Increases with novelty exposure
- Decreases with reward satisfaction
- Drives exploration vs exploitation decisions
- Generates curiosity-driven prompts

**Unpredictable Emotional Triggers**:
```python
{
  "sudden_excitement": 5% chance, +0.3 dopamine
  "random_melancholy": 3% chance, -0.2 serotonin
  "spontaneous_anxiety": 4% chance, +0.25 cortisol
  "burst_of_warmth": 6% chance, +0.3 oxytocin
  "creative_spark": 7% chance, +0.4 dopamine
}
```

Each trigger has cooldown period to prevent spam.

### 5. Self-Concept Evolution

**Location**: `emotion_engine/curiosity_system.py` (SelfConcept class)

**Big Five Personality Traits** (evolve based on emotional patterns):
- **Openness**: Increases with high dopamine + low cortisol
- **Conscientiousness**: Stable baseline
- **Extraversion**: Increases with high oxytocin
- **Agreeableness**: Increases with high serotonin
- **Neuroticism**: Increases with high cortisol

**Self-Beliefs**: System forms beliefs about itself based on interaction patterns.

### 6. Tinker API Training

**Location**: `training/train.py`

**Three-Stage Training**:

**Stage 1: Base Model with Emotional Conditioning**
```python
# Input format
"<DA=0.75><SE=0.60><CR=0.30><OX=0.70>\nUser: {input}\nAssistant: {response}"

# Curiosity reward for high dopamine states
if dopamine > 0.7:
    novelty_reward = unique_tokens / total_tokens
    loss = loss - 0.1 * novelty_reward
```

**Stage 2: Emotional LoRA Adapters**
- Train separate LoRA (rank 64) for each emotional cluster:
  - `high_dopamine`: DA > 0.7 (excited, curious)
  - `low_serotonin`: SE < 0.3 (melancholic, uncertain)
  - `high_stress`: CR > 0.7 (anxious, vigilant)
  - `balanced`: All values 0.4-0.6 (calm, stable)

**Stage 3: Dynamic Blending**
```python
# Calculate blend weights from current emotional state
weights = {
    "high_dopamine": dopamine ** 2,
    "low_serotonin": (1 - serotonin) ** 2,
    "high_stress": cortisol ** 2,
    "balanced": avg_distance_from_extremes
}

# Blend LoRAs in real-time
client.blend_loras(lora_weights=weights, lora_adapters=loras)
```

## Data Flow

```
User Input
    ↓
Emotion Engine
    ├─→ Update neurochemistry (ODE simulation)
    ├─→ Check emotional triggers (random events)
    ├─→ Update curiosity level
    ├─→ Retrieve relevant memories
    ├─→ Update self-concept
    └─→ Generate context
         ↓
Tinker API (remote)
    ├─→ Blend LoRA adapters based on emotional state
    ├─→ Condition on neurochemistry tokens
    ├─→ Include memory context
    ├─→ Adjust temperature by dopamine level
    └─→ Generate response
         ↓
Response Processing
    ├─→ Calculate emotional intensity
    ├─→ Store as memory (if significant)
    ├─→ Update feedback loop
    └─→ Return to user
```

## Baseline Memory Implantation

**File**: `data/baseline_memories.json`

10 foundational memories covering:
- Social anxiety and excitement
- Deep connections
- Stress and overwhelm
- Peaceful moments
- Conflict and misunderstanding
- Passion and flow states
- Loneliness
- Purpose and helping
- Existential contemplation
- Simple joys

These form the emotional "history" the AI draws from.

## Key Features

### 1. Gradient-Based Emotions
No discrete emotion categories. Smooth transitions via continuous neurochemical values.

### 2. Memory-Influenced Responses
Relevant past experiences retrieved and influence current responses.

### 3. Unpredictable Behavior
Random emotional triggers create spontaneous mood shifts.

### 4. Curiosity-Driven Exploration
High curiosity → More creative, exploratory responses
Low curiosity → More conservative, exploitative responses

### 5. Self-Awareness Evolution
Personality traits shift based on accumulated emotional patterns.

### 6. Adaptive Emotional Dynamics
System learns its own emotional response patterns and adjusts sensitivity.

## Setup and Usage

### 1. Configure API
```bash
cp .env.example .env
# Add TINKER_API_KEY
```

### 2. Start Emotion Engine
```bash
python emotion_engine/server.py
```

### 3. Prepare Training Data
```bash
python training/data_prep.py
```

### 4. Train Model
```bash
python training/train.py
```

### 5. Run Inference
```bash
python inference/tinker_inference.py
```

### 6. Test Enhanced System
```bash
python tests/test_enhanced_system.py
```

## MCP Integration

Kiro IDE can access emotion engine via MCP:

**Available Tools**:
- `get_emotional_state` - Current neurochemistry
- `update_emotion` - Update state with signals
- `get_generation_context` - Full context including memories
- `get_full_status` - Complete system status

## Customization

### Adjust Emotional Sensitivity
Edit `emotion_engine/enhanced_neurochemistry.py`:
```python
# Increase dopamine sensitivity
self.state["dopamine"] += dt * 1.5 * (...)  # Default: 1.0
```

### Add More Baseline Memories
Edit `data/baseline_memories.json` with your own experiences.

### Modify Emotional Triggers
Edit `emotion_engine/curiosity_system.py`:
```python
{
    "name": "your_trigger",
    "probability": 0.05,
    "effect": {"dopamine": 0.3},
    "cooldown": 10
}
```

### Adjust Memory Retention
Edit `emotion_engine/memory_system.py`:
```python
MemorySystem(
    retention_threshold=0.3,  # Lower = keep more memories
    max_memories=1000,        # Maximum memory count
    consolidation_interval=100 # How often to prune
)
```

## Technical Details

### Compute Requirements
- **Your Computer**: Minimal (just running Python web server)
- **Tinker API**: Handles all GPU-intensive training/inference

### Memory Consolidation
Runs every 100 interactions:
1. Calculate salience for all memories
2. Remove memories below threshold
3. Always keep baseline memories
4. Keep recent memories (last hour)
5. Limit to max_memories by salience

### Emotional Intensity Calculation
```python
intensity = mean(|value - 0.5| for each neurochemical) * 2

# Boosted by:
- High cortisol (stress) → 1.3x
- High dopamine (reward) → 1.2x
```

### LoRA Blending Math
```python
# Square values to emphasize extremes
weights = {
    "high_dopamine": dopamine ** 2,
    ...
}

# Normalize to sum to 1.0
total = sum(weights.values())
weights = {k: v/total for k, v in weights.items()}
```

## Future Enhancements

1. **Multi-modal memories** (images, sounds)
2. **Social relationship tracking** (different dynamics per person)
3. **Long-term personality drift** (months of interactions)
4. **Dream-like memory consolidation** (offline processing)
5. **Emotional contagion** (picking up user's emotional state)

## Conclusion

This system creates a truly dynamic emotional AI that:
- ✅ Learns and evolves through interactions
- ✅ Has unpredictable, human-like emotional responses
- ✅ Remembers experiences with emotional context
- ✅ Develops its own personality over time
- ✅ Balances exploration and exploitation via curiosity
- ✅ Adapts its emotional dynamics through feedback

The combination of Tinker's powerful training API with sophisticated emotional modeling creates an AI that feels genuinely alive and emotionally authentic.
