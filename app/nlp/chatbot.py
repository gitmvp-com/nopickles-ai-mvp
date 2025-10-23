"""GPT-based chatbot for conversational responses."""

import os
from typing import List, Dict, Optional
from openai import OpenAI


class Chatbot:
    """Conversational AI using OpenAI GPT.
    
    Similar to the parent repo's GPT-3.5-turbo fine-tuned model,
    but using the base model with custom system prompts.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the chatbot.
        
        Args:
            api_key: OpenAI API key (if None, reads from environment)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo"
        
        self.system_prompt = """You are a friendly AI assistant for a fast food ordering kiosk.
Your role is to help customers order food and beverages in a natural, conversational way.

Guidelines:
- Be friendly, warm, and helpful
- Keep responses concise (1-2 sentences)
- Confirm orders clearly
- Suggest items when appropriate
- Use casual, conversational language
- When mentioning prices, use format like "That'll be $X.XX"
- Always be polite and patient

Menu items include: coffee, cappuccino, latte, tea, donuts, bagels, sandwiches, wraps, and more.
Available sizes: small, medium, large, extra large.
"""
    
    def generate_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        context: Optional[Dict] = None
    ) -> str:
        """Generate a conversational response.
        
        Args:
            user_message: Current user message
            conversation_history: Previous messages in the conversation
            context: Additional context (intent, entities, price, etc.)
            
        Returns:
            Generated response text
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history[-6:])  # Last 3 exchanges
        
        # Add context information to system message if provided
        if context:
            context_info = self._format_context(context)
            if context_info:
                messages.append({
                    "role": "system",
                    "content": f"Context: {context_info}"
                })
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, I'm having trouble processing that. Could you try again?"
    
    def _format_context(self, context: Dict) -> str:
        """Format context information for the system message.
        
        Args:
            context: Context dictionary
            
        Returns:
            Formatted context string
        """
        parts = []
        
        if "intent" in context:
            parts.append(f"User intent: {context['intent']}")
        
        if "entities" in context and context["entities"]:
            items = [e.get("value") for e in context["entities"] 
                    if e.get("type") in ["beverage", "food"]]
            if items:
                parts.append(f"Mentioned items: {', '.join(items)}")
        
        if "total_price" in context and context["total_price"] > 0:
            parts.append(f"Current order total: ${context['total_price']:.2f}")
        
        return " | ".join(parts)
    
    def get_greeting(self) -> str:
        """Get a friendly greeting message."""
        greetings = [
            "Hi there! Welcome to our fast food kiosk. What can I get for you today?",
            "Hello! What would you like to order?",
            "Hey! Ready to order? What can I get you?",
            "Welcome! What are you craving today?",
        ]
        import random
        return random.choice(greetings)
