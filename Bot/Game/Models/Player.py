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
        
         # Base Stats with Emojis
        self.stats = {
            "💪Strength": 10,
            "🏃Agility": 10,
            "🧠Intelligence": 10,
            "❤️Vitality": 10
        }
        
        # Derived Stats (calculated from base stats + equipment)
        self.max_hp = 100
        self.current_hp = 100
        
        # Equipment slots
        self.equipment = {
            "⚔️Weapon": None,
            "🛡️Armor": None,
            "🪖Helmet": None,
            "💍Accessory": None
        }
        
        # Inventory (limited slots)
        self.inventory = []
        self.inventory_size = 20
        
        # Class type
        self.character_class = None  # Tank, DPS, Healer, etc.
        
        # Party info
        self.current_party_id = None

        #Guild info
        self.guild_id = None

        self.tower_level = 1

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
            "current_party_id": self.current_party_id,
            "guild_id": self.guild_id,
            "tower_level": self.tower_level
        }

    @classmethod
    def from_dict(cls, data: Dict):
        """Create a Player instance from MongoDB document"""
        player = cls(data["discord_id"], data["username"])
        
        # Populate all fields from data
        player.created_at = data.get("created_at", datetime.utcnow())
        player.last_active = data.get("last_active", datetime.utcnow())
        
        player.level = data.get("level", 1)
        player.experience = data.get("experience", 0)
        player.gold = data.get("gold", 0)
        
        player.stats = data.get("stats", {
            "💪Strength": 10,
            "🏃Agility": 10,
            "🧠Intelligence": 10,
            "❤️Vitality": 10
        })
        
        player.max_hp = data.get("max_hp", 100)
        player.current_hp = data.get("current_hp", 100)
        
        player.equipment = data.get("equipment", {
            "⚔️Weapon": None,
            "🛡️Armor": None,
            "🪖Helmet": None,
            "💍Accessory": None
        })
        
        player.inventory = data.get("inventory", [])
        player.inventory_size = data.get("inventory_size", 20)
        
        player.character_class = data.get("character_class")
        player.current_party_id = data.get("current_party_id")
        player.guild_id = data.get('guild_id')
        player.tower_level = data.get('tower_level')

        return player
    
   