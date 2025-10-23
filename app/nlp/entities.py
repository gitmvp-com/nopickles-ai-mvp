"""Named Entity Recognition for menu items and attributes."""

from typing import List, Tuple, Dict
import re
from app.menu import MENU


class EntityExtractor:
    """Extract entities (menu items, sizes, quantities) from text.
    
    In production, this would use a trained BERT-based NER model,
    but for MVP we use pattern matching and menu lookup.
    """
    
    def __init__(self):
        self.sizes = list(MENU["size_multiplier"].keys())
        self.menu_items = list(MENU["prices"].keys())
        
        # Common quantity patterns
        self.quantity_patterns = [
            (r"\b(\d+)\b", lambda m: int(m.group(1))),
            (r"\b(a|an|one)\b", lambda m: 1),
            (r"\btwo\b", lambda m: 2),
            (r"\bthree\b", lambda m: 3),
            (r"\bfour\b", lambda m: 4),
            (r"\bfive\b", lambda m: 5),
        ]
    
    def extract(self, text: str) -> List[Dict[str, str]]:
        """Extract entities from text.
        
        Args:
            text: User's message
            
        Returns:
            List of entities with their types
        """
        entities = []
        text_lower = text.lower()
        
        # Extract sizes
        for size in self.sizes:
            if size in text_lower:
                entities.append({
                    "value": size,
                    "type": "size"
                })
        
        # Extract menu items (longest match first to handle multi-word items)
        sorted_items = sorted(self.menu_items, key=len, reverse=True)
        found_items = set()
        
        for item in sorted_items:
            # Use word boundaries for better matching
            pattern = r"\b" + re.escape(item) + r"\b"
            if re.search(pattern, text_lower) and item not in found_items:
                found_items.add(item)
                
                # Determine if it's a beverage or food
                entity_type = "beverage" if self._is_beverage(item) else "food"
                
                entities.append({
                    "value": item,
                    "type": entity_type
                })
        
        # Extract quantities
        for pattern, converter in self.quantity_patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    qty = converter(match)
                    entities.append({
                        "value": str(qty),
                        "type": "quantity"
                    })
                    break  # Only take first quantity match
                except:
                    pass
        
        return entities
    
    def _is_beverage(self, item: str) -> bool:
        """Check if an item is a beverage."""
        beverages = [
            "coffee", "cappuccino", "iced coffee", "iced capp", "latte",
            "tea", "hot chocolate", "french vanilla", "white chocolate",
            "mocha", "espresso", "americano", "double double", "triple triple"
        ]
        return any(bev in item.lower() for bev in beverages)
    
    def get_items_and_sizes(self, entities: List[Dict[str, str]]) -> List[Tuple[str, str]]:
        """Pair items with their sizes from entity list.
        
        Args:
            entities: List of extracted entities
            
        Returns:
            List of (item, size) tuples
        """
        items = [e["value"] for e in entities if e["type"] in ["beverage", "food"]]
        sizes = [e["value"] for e in entities if e["type"] == "size"]
        
        # Pair items with sizes (if multiple items, use sizes in order)
        paired = []
        for i, item in enumerate(items):
            size = sizes[i] if i < len(sizes) else None
            paired.append((item, size))
        
        return paired
