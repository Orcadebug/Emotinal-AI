# Quick Setup Guide

## Where to Put Your Tinker API Key

### Option 1: Environment File (Recommended)

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Tinker API key:
   ```bash
   TINKER_API_KEY=your_actual_api_key_here
   ```

3. The system will automatically load it when you run training or inference

### Option 2: Environment Variable

Set it in your shell:

```bash
export TINKER_API_KEY="your_actual_api_key_here"
```

Or add to your `~/.bashrc` or `~/.zshrc`:

```bash
echo 'export TINKER_API_KEY="your_actual_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### Option 3: Pass Directly in Code

```python
from training.train import EmotionalLLMTrainer

trainer = EmotionalLLMTrainer(api_key="your_actual_api_key_here")
```

## Configuration Options

Edit `.env` to customize:

```bash
# Required
TINKER_API_KEY=your_key_here

# Optional (defaults shown)
TINKER_API_URL=https://api.tinker.ai/v1
MODEL_NAME=meta-llama/Llama-3.2-3B
LORA_RANK=64
LEARNING_RATE=0.001
EMOTION_ENGINE_URL=ws://localhost:8000/ws
```

## Verify Setup

Run this to check your configuration:

```bash
python -c "from config import TinkerConfig; TinkerConfig.validate(); print('✓ Configuration valid!')"
```

If you see an error, make sure your `.env` file exists and contains `TINKER_API_KEY`.

## Getting a Tinker API Key

1. Visit the Tinker API website
2. Sign up for an account
3. Navigate to API settings
4. Generate a new API key
5. Copy it to your `.env` file

## Next Steps

Once configured:

1. **Prepare data**: `python training/data_prep.py`
2. **Start emotion engine**: `python emotion_engine/server.py`
3. **Run training**: `python training/train.py`
4. **Test inference**: `python inference/tinker_inference.py`
