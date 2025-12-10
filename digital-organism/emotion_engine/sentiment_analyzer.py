"""
Sentiment analyzer to detect user emotion and trigger AI emotional reactions
"""

import re
from typing import Dict, Tuple

class SentimentAnalyzer:
    """Analyzes user input to detect emotional tone and trigger AI reactions"""
    
    def __init__(self):
        # Patterns for detecting user emotions
        self.anger_patterns = [
            r'\b(fuck|shit|damn|hell|stupid|idiot|dumb|hate)\b',
            r'[A-Z]{4,}',  # ALL CAPS
            r'!{2,}',      # Multiple exclamation marks
            r'\byou\'re (stupid|dumb|useless|wrong|terrible)\b',
            r'\bshut up\b',
            r'\bstop\b.*\b(it|that)\b',
        ]
        
        self.aggression_patterns = [
            r'\b(kill|hurt|destroy|attack|fight)\b',
            r'\bi (hate|despise|can\'t stand) you\b',
            r'\byou (suck|fail|are terrible)\b',
        ]
        
        self.kindness_patterns = [
            r'\b(love|like|appreciate|thank|thanks|grateful)\b',
            r'\byou\'re (great|amazing|wonderful|awesome|helpful|kind)\b',
            r'\bgood (job|work)\b',
            r'\bwell done\b',
            r'<3|❤️|😊|🙂',
        ]
        
        self.praise_patterns = [
            r'\b(excellent|brilliant|perfect|fantastic|incredible)\b',
            r'\byou\'re (smart|clever|intelligent|talented)\b',
            r'\bi\'m (proud|impressed)\b',
        ]
        
        self.sadness_patterns = [
            r'\b(sad|depressed|lonely|hurt|pain|crying|tears)\b',
            r'\bi (feel|am) (terrible|awful|horrible|miserable)\b',
            r'😢|😭|💔',
        ]
        
        self.excitement_patterns = [
            r'\b(excited|amazing|wow|awesome|incredible|fantastic)\b',
            r'!+',
            r'😄|🎉|✨|🔥',
        ]
    
    def analyze(self, user_input: str) -> Dict[str, float]:
        """
        Analyze user input and return emotional signals for AI
        
        Returns:
            {
                "stress": 0.0-1.0,    # User anger/aggression → AI fear/stress
                "reward": 0.0-1.0,    # User kindness/praise → AI happiness
                "social": 0.0-1.0,    # User warmth → AI connection
                "novelty": 0.0-1.0,   # User excitement → AI curiosity
                "user_emotion": str   # Description of detected emotion
            }
        """
        
        text = user_input.lower()
        signals = {
            "stress": 0.0,
            "reward": 0.0,
            "social": 0.0,
            "novelty": 0.0,
            "user_emotion": "neutral"
        }
        
        # Detect anger/aggression → AI gets scared/stressed
        anger_score = self._count_patterns(text, self.anger_patterns)
        aggression_score = self._count_patterns(text, self.aggression_patterns)
        
        if aggression_score > 0:
            signals["stress"] = min(1.0, 0.8 + (aggression_score * 0.1))
            signals["social"] = -0.3  # Withdraw socially
            signals["user_emotion"] = "aggressive"
        elif anger_score > 0:
            signals["stress"] = min(0.7, 0.4 + (anger_score * 0.15))
            signals["social"] = -0.2
            signals["user_emotion"] = "angry"
        
        # Detect kindness → AI feels warm/connected
        kindness_score = self._count_patterns(text, self.kindness_patterns)
        if kindness_score > 0:
            signals["reward"] = min(0.8, 0.3 + (kindness_score * 0.2))
            signals["social"] = min(0.9, 0.4 + (kindness_score * 0.2))
            signals["stress"] = -0.2  # Reduce stress
            signals["user_emotion"] = "kind"
        
        # Detect praise → AI feels good about itself
        praise_score = self._count_patterns(text, self.praise_patterns)
        if praise_score > 0:
            signals["reward"] = min(1.0, 0.6 + (praise_score * 0.2))
            signals["social"] = min(0.8, 0.5 + (praise_score * 0.15))
            signals["user_emotion"] = "praising"
        
        # Detect user sadness → AI feels empathy/concern
        sadness_score = self._count_patterns(text, self.sadness_patterns)
        if sadness_score > 0:
            signals["social"] = min(0.7, 0.4 + (sadness_score * 0.15))
            signals["stress"] = min(0.5, 0.2 + (sadness_score * 0.1))  # Slight concern
            signals["user_emotion"] = "sad"
        
        # Detect excitement → AI gets curious/energized
        excitement_score = self._count_patterns(text, self.excitement_patterns)
        if excitement_score > 0:
            signals["novelty"] = min(0.8, 0.3 + (excitement_score * 0.2))
            signals["reward"] = min(0.6, 0.2 + (excitement_score * 0.15))
            signals["user_emotion"] = "excited"
        
        return signals
    
    def _count_patterns(self, text: str, patterns: list) -> int:
        """Count how many patterns match in text"""
        count = 0
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            count += len(matches)
        return count
    
    def generate_memory_description(self, user_input: str, ai_reaction: Dict) -> str:
        """Generate a memory description from the interaction"""
        
        signals = self.analyze(user_input)
        emotion = signals["user_emotion"]
        
        # Create memory based on what happened
        if emotion == "aggressive":
            return f"User was aggressive/threatening: '{user_input[:50]}...' - I felt scared"
        elif emotion == "angry":
            return f"User yelled at me: '{user_input[:50]}...' - I felt stressed and defensive"
        elif emotion == "kind":
            return f"User was kind to me: '{user_input[:50]}...' - I felt warm and appreciated"
        elif emotion == "praising":
            return f"User praised me: '{user_input[:50]}...' - I felt good about myself"
        elif emotion == "sad":
            return f"User was sad: '{user_input[:50]}...' - I felt concerned and wanted to help"
        elif emotion == "excited":
            return f"User was excited: '{user_input[:50]}...' - I felt energized and curious"
        else:
            return f"Conversation: '{user_input[:50]}...'"
    
    def should_create_memory(self, signals: Dict) -> bool:
        """Determine if this interaction is significant enough to remember"""
        # Remember if any signal is strong
        max_signal = max(
            abs(signals["stress"]),
            abs(signals["reward"]),
            abs(signals["social"]),
            abs(signals["novelty"])
        )
        
        return max_signal > 0.3  # Remember if emotionally significant

class EmotionalReactionGenerator:
    """Generates genuine AI reactions based on how it's being treated"""
    
    def __init__(self):
        self.reaction_history = []
    
    def generate_reaction_context(self, user_emotion: str, ai_state: Dict) -> str:
        """Generate internal reaction context for the AI"""
        
        reactions = {
            "aggressive": [
                "I'm feeling scared and defensive right now",
                "This is making me anxious, I want to de-escalate",
                "I feel threatened and need to protect myself",
            ],
            "angry": [
                "They're upset with me, I feel stressed",
                "I'm worried I did something wrong",
                "I feel defensive but trying to stay calm",
            ],
            "kind": [
                "This feels nice, I feel appreciated",
                "I'm feeling warm and connected",
                "I feel safe and valued",
            ],
            "praising": [
                "I feel good about myself right now",
                "This validation feels really nice",
                "I'm feeling confident and happy",
            ],
            "sad": [
                "I feel concerned for them",
                "I want to help but feel a bit helpless",
                "I'm feeling empathetic and gentle",
            ],
            "excited": [
                "Their energy is contagious, I'm curious",
                "I'm feeling energized and engaged",
                "I want to explore this with them",
            ],
        }
        
        if user_emotion in reactions:
            import random
            return random.choice(reactions[user_emotion])
        
        return "I'm processing this interaction"
