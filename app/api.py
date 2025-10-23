"""FastAPI application and routes."""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Dict
import uuid
import os

from app.models import ChatMessage, ChatResponse, Entity, Session, OrderItem
from app.nlp.intent import IntentClassifier
from app.nlp.entities import EntityExtractor
from app.nlp.chatbot import Chatbot
from app.menu import MenuService

# Initialize FastAPI app
app = FastAPI(
    title="NoPickles.ai MVP",
    description="Conversational AI ordering system for fast food",
    version="0.1.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize services
intent_classifier = IntentClassifier()
entity_extractor = EntityExtractor()
menu_service = MenuService()

# Initialize chatbot (only if API key is available)
try:
    chatbot = Chatbot()
except ValueError:
    print("Warning: OpenAI API key not found. Chatbot responses will be limited.")
    chatbot = None

# In-memory session storage (in production, use Redis or database)
sessions: Dict[str, Session] = {}


@app.get("/")
async def root():
    """Serve the main HTML page."""
    return FileResponse("static/index.html")


@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Process a chat message and return a response.
    
    Args:
        message: User's chat message
        
    Returns:
        ChatResponse with bot reply, intent, entities, and price
    """
    # Get or create session
    session_id = message.session_id or str(uuid.uuid4())
    
    if session_id not in sessions:
        sessions[session_id] = Session(
            session_id=session_id,
            messages=[],
            order_items=[],
            total_price=0.0
        )
    
    session = sessions[session_id]
    
    # Classify intent
    intent = intent_classifier.classify(message.message)
    
    # Extract entities
    entities_data = entity_extractor.extract(message.message)
    entities = [Entity(**e) for e in entities_data]
    
    # Process order if intent is order or add_item
    if intent in ["order", "add_item"]:
        items_with_sizes = entity_extractor.get_items_and_sizes(entities_data)
        
        for item_name, size in items_with_sizes:
            price = menu_service.get_item_price(item_name, size)
            if price:
                order_item = OrderItem(
                    name=item_name,
                    size=size,
                    quantity=1,
                    price=price
                )
                session.order_items.append(order_item)
                session.total_price += price
    
    # Generate conversational response
    if chatbot:
        # Build conversation history
        conv_history = []
        for msg in session.messages[-6:]:  # Last 3 exchanges
            role = "user" if len(conv_history) % 2 == 0 else "assistant"
            conv_history.append({"role": role, "content": msg})
        
        context = {
            "intent": intent,
            "entities": entities_data,
            "total_price": session.total_price
        }
        
        response_text = chatbot.generate_response(
            message.message,
            conversation_history=conv_history,
            context=context
        )
    else:
        # Fallback response when chatbot is not available
        response_text = _generate_fallback_response(intent, entities, session.total_price)
    
    # Update session
    session.messages.append(message.message)
    session.messages.append(response_text)
    
    return ChatResponse(
        response=response_text,
        intent=intent,
        entities=entities,
        total_price=session.total_price,
        session_id=session_id
    )


@app.get("/menu")
async def get_menu():
    """Get the full menu with prices."""
    return menu_service.get_all_items()


@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear a session (reset order)."""
    if session_id in sessions:
        del sessions[session_id]
        return {"message": "Session cleared"}
    return {"message": "Session not found"}


def _generate_fallback_response(intent: str, entities: list, total_price: float) -> str:
    """Generate a simple fallback response when chatbot is unavailable."""
    if intent == "greeting":
        return "Hello! Welcome to our kiosk. What would you like to order?"
    elif intent in ["order", "add_item"]:
        if entities:
            items = [e.value for e in entities if e.type in ["beverage", "food"]]
            if items and total_price > 0:
                return f"Got it! Added {', '.join(items)} to your order. Total: ${total_price:.2f}. Anything else?"
        return "What would you like to order?"
    elif intent == "farewell":
        if total_price > 0:
            return f"Thank you! Your total is ${total_price:.2f}. Have a great day!"
        return "Thank you! Have a great day!"
    else:
        return "I'm here to help you order. What would you like?"


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "chatbot_available": chatbot is not None
    }
