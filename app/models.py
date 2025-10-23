"""Data models for the application."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class ChatMessage(BaseModel):
    """Incoming chat message from user."""
    message: str = Field(..., min_length=1, description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")


class Entity(BaseModel):
    """Extracted entity from user message."""
    value: str = Field(..., description="Entity value (e.g., 'coffee', 'large')")
    type: str = Field(..., description="Entity type (e.g., 'beverage', 'size')")


class ChatResponse(BaseModel):
    """Response from the chatbot."""
    response: str = Field(..., description="Bot response message")
    intent: str = Field(..., description="Detected intent (e.g., 'order', 'question')")
    entities: List[Entity] = Field(default_factory=list, description="Extracted entities")
    total_price: float = Field(0.0, description="Current order total")
    session_id: str = Field(..., description="Session ID")


class OrderItem(BaseModel):
    """Single item in an order."""
    name: str
    size: Optional[str] = None
    quantity: int = 1
    price: float


class Session(BaseModel):
    """User session data."""
    session_id: str
    messages: List[str] = Field(default_factory=list)
    order_items: List[OrderItem] = Field(default_factory=list)
    total_price: float = 0.0
    created_at: datetime = Field(default_factory=datetime.now)
