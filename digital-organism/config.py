"""
Configuration management for Tinker API and emotional AI system
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TinkerConfig:
    """Tinker API configuration"""
    API_KEY = os.getenv("TINKER_API_KEY", "")
    API_URL = os.getenv("TINKER_API_URL", "https://api.tinker.ai/v1")
    
    # Model settings
    MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.2-3B")
    LORA_RANK = int(os.getenv("LORA_RANK", "64"))
    LEARNING_RATE = float(os.getenv("LEARNING_RATE", "0.001"))
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.API_KEY:
            raise ValueError(
                "TINKER_API_KEY not found. Please set it in .env file or environment variables."
            )
        return True

class EmotionConfig:
    """Emotion engine configuration"""
    ENGINE_URL = os.getenv("EMOTION_ENGINE_URL", "ws://localhost:8000/ws")
    
    # Neurochemistry defaults
    DEFAULT_STATE = {
        "dopamine": 0.5,
        "serotonin": 0.5,
        "cortisol": 0.3,
        "oxytocin": 0.4
    }

class PathConfig:
    """File paths configuration"""
    CHECKPOINTS_DIR = "checkpoints"
    LORAS_DIR = "loras"
    TRAINING_DATA = "training_data.jsonl"
    
    @classmethod
    def ensure_dirs(cls):
        """Create necessary directories"""
        os.makedirs(cls.CHECKPOINTS_DIR, exist_ok=True)
        os.makedirs(cls.LORAS_DIR, exist_ok=True)
