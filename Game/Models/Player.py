from datetime import datetime
from typing import Dict, List

class Player:
    def __init__(self, discord_id: str, username: str):
        # Basic Info - maps to MongoDB documents
        self.discord_id = discord_id  # Unique identifier
        self.username = username
        self.created_at = datetime.utcnow()
        self.last_active = datetime.utcnow()
        
        # Character Stats
        self.level = 1
        self.experience = 0
        self.gold = 0
        
        # Base Stats
        self.stats = {
            "strength": 10,
            "agility": 10,
            "intelligence": 10,
            "vitality": 10
        }
        
        # Derived Stats (calculated from base stats + equipment)
        self.max_hp = 100
        self.current_hp = 100
        
        # Equipment slots
        self.equipment = {
            "weapon": None,
            "armor": None,
            "helmet": None,
            "accessory": None
        }
        
        # Inventory (limited slots)
        self.inventory = []
        self.inventory_size = 20
        
        # Class type
        self.character_class = None  # Tank, DPS, Healer, etc.
        
        # Party info
        self.current_party_id = None

    def to_dict(self) -> Dict:
        """Convert player data to dictionary for MongoDB storage"""
        return {
            "discord_id": self.discord_id,
            "username": self.username,
            "created_at": self.created_at,
            "last_active": self.last_active,
            "level": self.level,
            "experience": self.experience,
            "gold": self.gold,
            "stats": self.stats,
            "max_hp": self.max_hp,
            "current_hp": self.current_hp,
            "equipment": self.equipment,
            "inventory": self.inventory,
            "character_class": self.character_class,
            "current_party_id": self.current_party_id
        }

    @classmethod
    def from_dict(cls, data: Dict):
        """Create a Player instance from MongoDB document"""
        player = cls(data["discord_id"], data["username"])
        # Populate all fields from data
        # ... implementation here
        return player