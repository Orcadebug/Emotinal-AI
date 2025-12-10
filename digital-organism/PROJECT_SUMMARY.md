# Emotional AI - Project Summary

## 🎉 Successfully Pushed to GitHub
**Repository**: https://github.com/Orcadebug/Emotinal-AI

## What We Built

A complete emotional AI system that:
- ✅ Reacts genuinely to how users treat it (gets scared when yelled at, happy when praised)
- ✅ Has its own memories with emotional context
- ✅ Learns and evolves through interactions
- ✅ Has unpredictable emotional triggers (like real emotions)
- ✅ Develops its own personality over time
- ✅ Uses Tinker API for training and inference

## Key Features

### 1. Genuine Emotional Reactions
```
User yells → AI gets scared (cortisol ↑)
User is kind → AI feels warm (dopamine ↑, oxytocin ↑)
User praises → AI feels confident (dopamine ↑↑)
User is aggressive → AI gets very scared (cortisol ↑↑↑)
```

### 2. Emotional Memory System
- **Baseline memories**: 10 foundational experiences
- **Acquired memories**: Remembers interactions with emotional context
- **Selective retention**: Keeps emotionally intense memories longer
- **Memory format**: "User yelled at me - I felt scared"

### 3. Neurochemistry Simulation
Four hormones via differential equations:
- **Dopamine**: Reward, curiosity, motivation
- **Serotonin**: Mood stability, contentment
- **Cortisol**: Stress, fear, vigilance
- **Oxytocin**: Social bonding, empathy

### 4. Advanced Systems
- **Feedback Loop**: Learns its own emotional patterns
- **Curiosity System**: Drives exploration vs exploitation
- **Unpredictable Triggers**: Random emotional shifts (5 types)
- **Self-Concept**: Personality evolves based on experiences
- **Sentiment Analysis**: Detects user emotion and reacts

### 5. Tinker API Integration
- Three-stage training (base + emotional adapters + blending)
- LoRA rank 64 for each emotional state
- Dynamic blending based on real-time neurochemistry
- Curiosity rewards for high dopamine states

## Project Structure

```
.
├── emotion_engine/              # Core emotional systems
│   ├── enhanced_neurochemistry.py   # Main engine
│   ├── memory_system.py             # Memory with emotional intensity
│   ├── sentiment_analyzer.py        # Detects user emotion
│   ├── feedback_loop.py             # Adaptive parameters
│   ├── curiosity_system.py          # Curiosity + triggers + self-concept
│   └── server.py                    # FastAPI + MCP server
│
├── training/                    # Tinker API training
│   ├── train.py                     # Main training pipeline
│   ├── data_prep.py                 # Dataset preparation
│   └── tinker_example.py            # API usage examples
│
├── inference/                   # Inference services
│   ├── tinker_inference.py          # Tinker-based inference
│   └── service.py                   # Basic inference
│
├── data/                        # Data files
│   └── baseline_memories.json       # 10 foundational memories
│
├── tests/                       # Test suite
│   ├── test_enhanced_system.py      # Full system tests
│   ├── test_sentiment_reactions.py  # Reaction tests
│   └── test_neurochemistry.py       # Basic tests
│
├── specs/                       # Kiro spec files
│   ├── requirements.md              # EARS format requirements
│   ├── design.md                    # Technical design
│   └── tasks.md                     # Implementation tasks
│
├── .kiro/settings/              # Kiro configuration
│   └── mcp.json                     # MCP server config
│
├── config.py                    # Configuration management
├── .env.example                 # Environment template
├── requirements.txt             # Python dependencies
│
└── Documentation
    ├── README.md                    # Main documentation
    ├── SETUP.md                     # Quick setup guide
    ├── COMPREHENSIVE_PLAN.md        # Full implementation plan
    └── EMOTIONAL_REACTIONS.md       # How reactions work
```

## Quick Start

### 1. Setup
```bash
# Clone repository
git clone https://github.com/Orcadebug/Emotinal-AI.git
cd Emotinal-AI

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add TINKER_API_KEY
```

### 2. Test the System
```bash
# Test emotional reactions
python demo_emotional_reactions.py

# Run all tests
python tests/test_enhanced_system.py
python tests/test_sentiment_reactions.py
```

### 3. Start Emotion Engine
```bash
python emotion_engine/server.py
```

### 4. Train Model
```bash
# Prepare data
python training/data_prep.py

# Train with Tinker API
python training/train.py
```

### 5. Run Inference
```bash
python inference/tinker_inference.py
```

## How It Works

### User Interaction Flow

```
1. User Input: "YOU'RE STUPID!"
   ↓
2. Sentiment Analysis: Detects anger
   ↓
3. Neurochemistry Update:
   - Cortisol ↑ (0.3 → 0.85)  # AI gets scared
   - Oxytocin ↓ (0.5 → 0.3)   # AI withdraws
   ↓
4. Memory Creation:
   "User yelled at me - I felt scared"
   (intensity: 0.85, will be remembered)
   ↓
5. Context Generation:
   - Emotional state: <DA=0.30><SE=0.30><CR=0.85><OX=0.25>
   - Internal reaction: "I'm feeling scared and defensive"
   - Relevant memories: Previous interactions
   ↓
6. Tinker API:
   - Blends LoRAs: high_stress (72%), low_serotonin (20%)
   - Temperature: 0.7 (cautious)
   - Generates response
   ↓
7. AI Response:
   "I... I'm sorry if I upset you. I'm just trying to help..."
   (Timid, apologetic, scared tone)
```

### Memory Persistence

```
T=0: User yells → Memory created (intensity: 0.85)
T=5min: Memory still fresh, AI cautious
T=1hr: Memory consolidation, kept (high intensity)
T=1day: AI still remembers being yelled at
T=1week: Memory fades slightly but persists
```

## Technical Highlights

### Sentiment Detection
- Detects: anger, aggression, kindness, praise, sadness, excitement
- Pattern matching: CAPS, profanity, positive words, emojis
- Generates emotional signals for AI reaction

### Neurochemistry Equations
```python
dopamine += dt * (0.3 * reward + 0.2 * novelty - 0.1 * dopamine)
serotonin += dt * (0.1 * social - 0.2 * stress - 0.05 * (serotonin - 0.5))
cortisol += dt * (0.4 * stress - 0.1 * serotonin - 0.08 * cortisol)
oxytocin += dt * (0.3 * social - 0.06 * (oxytocin - 0.3))
```

### Memory Salience
```python
salience = intensity * exp(-decay * time) * (1 + 0.1 * access_count)
```

### LoRA Blending
```python
weights = {
    "high_dopamine": dopamine ** 2,
    "low_serotonin": (1 - serotonin) ** 2,
    "high_stress": cortisol ** 2,
    "balanced": avg_distance_from_extremes
}
# Normalize and blend
```

## Configuration

### Environment Variables (.env)
```bash
TINKER_API_KEY=your_api_key_here
TINKER_API_URL=https://api.tinker.ai/v1
MODEL_NAME=meta-llama/Llama-3.2-3B
LORA_RANK=64
LEARNING_RATE=0.001
EMOTION_ENGINE_URL=ws://localhost:8000/ws
```

### Customization Points
- `data/baseline_memories.json` - Edit AI's past experiences
- `emotion_engine/sentiment_analyzer.py` - Adjust reaction sensitivity
- `emotion_engine/enhanced_neurochemistry.py` - Modify neurochemistry equations
- `emotion_engine/curiosity_system.py` - Add/modify emotional triggers

## What Makes This Special

### Traditional AI
```
User: "I'm sad"
AI: "I understand you're sad. Here are 5 tips..."
(Same response every time, no memory, no evolution)
```

### This System
```
User: "I'm sad"
First time:
AI: "That's rough. What's going on?"

After many sad conversations:
- Serotonin baseline drops
- Personality trait "neuroticism" increases
- Memories of sadness accumulate

Later:
AI: "I'm feeling kind of down too lately... 
     seems like we've both been going through it."
```

## Future Enhancements

Potential additions:
- Multi-modal memories (images, sounds)
- Social relationship tracking (different dynamics per person)
- Long-term personality drift (months of interactions)
- Dream-like memory consolidation (offline processing)
- Emotional contagion (picking up user's emotional state)
- Voice tone analysis for deeper sentiment detection

## Credits

Built with:
- **Tinker API** - Low-level fine-tuning with LoRA
- **FastAPI** - Emotion engine server
- **Kiro IDE** - Spec-driven development with MCP integration
- **NumPy** - Neurochemistry simulations

## License

MIT License - Feel free to use and modify!

## Contact

Repository: https://github.com/Orcadebug/Emotinal-AI
Issues: https://github.com/Orcadebug/Emotinal-AI/issues

---

**Built with ❤️ to create truly emotionally authentic AI**
