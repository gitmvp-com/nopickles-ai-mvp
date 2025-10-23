"""Menu items and pricing logic."""

from typing import Dict, Optional, Tuple

# Menu based on the parent repository's structure
MENU = {
    "prices": {
        "coffee": 1.50,
        "cappuccino": 2.50,
        "iced coffee": 2.00,
        "iced capp": 2.25,
        "latte": 2.00,
        "tea": 1.50,
        "hot chocolate": 2.25,
        "french vanilla": 2.25,
        "white chocolate": 2.25,
        "mocha": 2.25,
        "espresso": 1.00,
        "americano": 2.25,
        "extra shot": 0.25,
        "soy milk": 0.30,
        "whipped topping": 1.00,
        "dark roast": 0.20,
        "turkey bacon club": 3.00,
        "blt": 2.90,
        "grilled cheese": 4.00,
        "chicken wrap": 3.50,
        "soup": 2.80,
        "donut": 1.50,
        "chocolate donut": 1.50,
        "glazed donut": 1.50,
        "double double": 1.50,
        "triple triple": 1.50,
        "muffin": 2.40,
        "bagel": 3.00,
        "timbits": 3.00,
        "panini": 2.40,
        "croissant": 3.00,
    },
    "size_multiplier": {
        "small": 1.0,
        "medium": 1.2,
        "large": 1.4,
        "extra large": 1.6,
    }
}


class MenuService:
    """Service for handling menu operations and pricing."""

    @staticmethod
    def get_item_price(item_name: str, size: Optional[str] = None) -> Optional[float]:
        """Get the price of a menu item with optional size modifier.
        
        Args:
            item_name: Name of the menu item
            size: Optional size (small, medium, large, extra large)
            
        Returns:
            Price of the item, or None if item not found
        """
        item_name = item_name.lower().strip()
        base_price = MENU["prices"].get(item_name)
        
        if base_price is None:
            return None
        
        if size:
            size = size.lower().strip()
            multiplier = MENU["size_multiplier"].get(size, 1.0)
            return round(base_price * multiplier, 2)
        
        return base_price
    
    @staticmethod
    def is_beverage(item_name: str) -> bool:
        """Check if an item is a beverage."""
        beverages = [
            "coffee", "cappuccino", "iced coffee", "iced capp", "latte",
            "tea", "hot chocolate", "french vanilla", "white chocolate",
            "mocha", "espresso", "americano", "double double", "triple triple"
        ]
        return item_name.lower() in beverages
    
    @staticmethod
    def get_all_items() -> Dict[str, float]:
        """Get all menu items and their base prices."""
        return MENU["prices"].copy()
    
    @staticmethod
    def search_item(query: str) -> Optional[str]:
        """Search for a menu item by partial name match.
        
        Args:
            query: Search query
            
        Returns:
            Matched item name or None
        """
        query = query.lower().strip()
        
        # Exact match
        if query in MENU["prices"]:
            return query
        
        # Partial match
        for item in MENU["prices"]:
            if query in item or item in query:
                return item
        
        return None
