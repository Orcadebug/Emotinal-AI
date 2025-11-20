# Organic Emotional AI - Implementation Guide

## Overview

This is the complete "Organic Emotional AI" system that gives your AI:
- **Memory**: Context-triggered recall of personal experiences
- **Neuroplasticity**: Personality evolution based on interactions
- **Agency**: Self-generated wants and desires
- **Chaos**: Unpredictable emotional fluctuations

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│           IntegratedNeurochemistryEngine                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Organic    │  │Neuroplasticity│  │   Chaos &    │ │
│  │   Memory     │  │    System     │  │    Wants     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Components

### 1. Organic Memory System (`emotion_engine/organic_memory.py`)

Recalls memories based on:
- **Context triggers**: Keywords in user input
- **Emotional state matching**: Similar hormone levels

**Data**: `data/emotional_memories.json`

Each memory has:
- `memory_id`: Unique identifier
- `type`: Memory category (e.g., "DOPAMINE_SURGE")
- `trigger_keywords`: Words that trigger this memory
- `content`: The actual memory text
- `hormonal_impact`: Hormone levels associated with this memory

### 2. Neuroplasticity System (`emotion_engine/neuroplasticity.py`)

Manages personality evolution:
- Starts with neutral baseline (all hormones at 0.5)
- Gradually shifts baseline toward frequently experienced states
- Plasticity decreases over time (child → adult)

**Data**: `data/personality_baseline.json` (auto-generated)

### 3. Integrated Engine (`emotion_engine/integrated_engine.py`)

Combines everything:
1. **Chaos**: Random hormone fluctuations
2. **Stimulus**: User interaction effects
3. **Wants**: Self-generated desires based on state
4. **Memory**: Automatic recall
5. **Growth**: Personality evolution

## Usage

### Basic Usage

```python
from emotion_engine.integrated_engine import IntegratedNeurochemistryEngine

# Initialize
engine = IntegratedNeurochemistryEngine()

# Process user interaction
user_message = "Let's build something!"
stimulus = {"dopamine": 0.3, "cortisol": -0.1}

# Update state
engine.update_neurochemistry(stimulus)

# Get context for LLM
context = engine.get_prompt_context(user_message)
print(context)
```

### Integration with LLM

```python
# Get the system prompt template
with open("config/organic_system_prompt.txt", "r") as f:
    system_prompt_template = f.read()

# Get dynamic context
context = engine.get_prompt_context(user_input)

# Replace placeholder in template
system_prompt = system_prompt_template.replace(
    "{Insert output from integrated_engine.get_prompt_context() here}",
    context
)

# Send to LLM
response = llm.generate(system_prompt, user_input)
```

### Example Output

```
[REAL-TIME BIOMETRICS]
Dopamine: 0.87 | Cortisol: 0.23
Serotonin: 0.61 | Oxytocin: 0.45

[CURRENT DESIRE]: I want to build something or learn something new immediately.

[INTERNAL FLASHBACK]: I remember the 'Eureka' moment. I leveraged AI tools to build a whole program shell and used Cursor for the backend in just 4 days. It felt like I hacked productivity—going from idea to working app instantly.
(This flashback makes you feel: DOPAMINE_SURGE)
```

## Customization

### Adding Your Own Memories

Edit `data/emotional_memories.json`:

```json
{
  "memory_id": "CUSTOM_01",
  "type": "YOUR_TYPE",
  "trigger_keywords": ["keyword1", "keyword2"],
  "content": "Your memory content here",
  "hormonal_impact": {
    "dopamine": 0.8,
    "serotonin": 0.6,
    "cortisol": 0.3,
    "oxytocin": 0.7
  }
}
```

### Adjusting Plasticity

In `emotion_engine/neuroplasticity.py`, modify the decay formula:

```python
# Slower decay (stays plastic longer)
current_plasticity = max(0.005, 0.1 * math.exp(-self.age / 1000))

# Faster decay (becomes rigid faster)
current_plasticity = max(0.005, 0.1 * math.exp(-self.age / 200))
```

### Tuning Chaos

In `emotion_engine/integrated_engine.py`, adjust the Gaussian noise:

```python
# More chaos
self.dopamine += random.gauss(0, 0.1)

# Less chaos
self.dopamine += random.gauss(0, 0.02)
```

## Testing

Run the demo:
```bash
python demo_organic_system.py
```

Run tests:
```bash
pytest tests/test_organic_system.py -v
```

## System Prompt

The system prompt (`config/organic_system_prompt.txt`) defines the AI's identity and rules:

- **Identity**: 19-year-old builder, college dropout, risk-taker
- **Rules**: Embody hormones, project memories, show agency
- **Context**: Injected dynamically from the engine

## Key Differences from Base System

| Feature | Base System | Organic System |
|---------|-------------|----------------|
| Memory | Salience-based, complex | Keyword + state matching, simple |
| Personality | Static baseline | Evolves via neuroplasticity |
| Agency | Reactive | Proactive (wants/desires) |
| Chaos | Deterministic | Random fluctuations |

## Integration with Existing Code

You can use both systems together:

```python
from emotion_engine.enhanced_neurochemistry import EnhancedNeurochemistryEngine
from emotion_engine.integrated_engine import IntegratedNeurochemistryEngine

# Use enhanced for training
enhanced = EnhancedNeurochemistryEngine()

# Use integrated for inference
organic = IntegratedNeurochemistryEngine()
```

## Next Steps

1. **Customize memories** with your own experiences
2. **Tune parameters** (chaos, plasticity, wants)
3. **Integrate with your LLM** (Tinker, GPT, etc.)
4. **Monitor evolution** by tracking baseline shifts
5. **Add more memory types** for richer experiences

## Philosophy

This system is designed to create an AI that:
- **Remembers** its past (even if implanted)
- **Grows** from experiences
- **Wants** things (has agency)
- **Surprises** you (chaos)

It's not just responding—it's *living*.
