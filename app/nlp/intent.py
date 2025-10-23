"""Intent classification logic."""

from typing import Dict, List
import re


class IntentClassifier:
    """Simple rule-based intent classifier.
    
    In production, this would use a trained BERT model like in the parent repo,
    but for MVP we use pattern matching.
    """
    
    def __init__(self):
        self.intent_patterns = {
            "greeting": [
                r"\b(hi|hello|hey|good morning|good afternoon|good evening)\b",
            ],
            "order": [
                r"\b(want|like|get|have|order|i'll have|give me|can i get)\b",
                r"\b(coffee|tea|donut|bagel|sandwich|wrap|soup|muffin)\b",
            ],
            "add_item": [
                r"\b(add|also|and|plus|another)\b.*\b(coffee|tea|donut|bagel)\b",
            ],
            "question": [
                r"\b(what|how|when|where|which|do you|can you|is there)\b",
                r"\?",
            ],
            "confirmation": [
                r"\b(yes|yeah|yep|sure|okay|ok|correct|right)\b",
            ],
            "negation": [
                r"\b(no|nope|nah|nothing|that's all|i'm good)\b",
            ],
            "farewell": [
                r"\b(bye|goodbye|see you|thanks|thank you)\b",
            ],
        }
    
    def classify(self, text: str) -> str:
        """Classify the intent of the user's message.
        
        Args:
            text: User's message
            
        Returns:
            Intent label (greeting, order, question, etc.)
        """
        text = text.lower()
        
        # Score each intent
        scores = {intent: 0 for intent in self.intent_patterns}
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    scores[intent] += 1
        
        # Return intent with highest score
        max_intent = max(scores, key=scores.get)
        
        # Default to 'order' if no clear intent and message contains item words
        if scores[max_intent] == 0:
            return "unknown"
        
        return max_intent
    
    def get_confidence(self, text: str, intent: str) -> float:
        """Get confidence score for a specific intent.
        
        Args:
            text: User's message
            intent: Intent to check
            
        Returns:
            Confidence score (0-1)
        """
        if intent not in self.intent_patterns:
            return 0.0
        
        text = text.lower()
        matches = 0
        total_patterns = len(self.intent_patterns[intent])
        
        for pattern in self.intent_patterns[intent]:
            if re.search(pattern, text, re.IGNORECASE):
                matches += 1
        
        return matches / total_patterns if total_patterns > 0 else 0.0
