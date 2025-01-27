from datetime import datetime
from typing import Dict, List, Optional
import discord
from Game.Managers.equipment_db_connection import get_equipment_by_id

starter_equipment_versions = {
            "Weapon": ["Wooden Sword", "Bronze Sword", "Iron Sword", "Steel Sword"],
            "Armor": ["Leather Armor", "Bronze Armor", "Iron Armor", "Steel Armor"],
            "Helmet": ["Leather Helmet", "Bronze Helmet", "Iron Helmet", "Steel Helmet"],
            "Accessory": ["Wooden Ring", "Bronze Ring", "Iron Ring", "Steel Ring"]
        }


class Player:
    def init(self, discord_id: str, username: str):
        self.discord_id = discord_id
        self.username = username
        self.created_at = datetime.utcnow()
        self.last_active = datetime.utcnow()
        
        # Character Stats
        self.stats = {
            "strength": 10,
            "agility": 10,
            "intelligence": 10,
            "vitality": 10
        }
        
        # Derived Stats
        self.level = 1
        self.experience = 0
        self.gold = 0
        self.max_hp = 100
        self.current_hp = 100
        
        # Equipment slots
        self.equipment = {
            "Weapon": get_equipment_by_id("W000"),
            "Armor": get_equipment_by_id("A000"),
            "Helmet": get_equipment_by_id("H000"),
            "Accessory": get_equipment_by_id("ACC000")
        }
        
        self.inventory = []
        self.inventory_size = 20
        self.character_class = None
        self.current_party_id = None
        self.guild_id = None
        self.tower_level = 1
        
    def __init__(self, discord_id: str, username: str, created_at: datetime = datetime.utcnow(), last_active: datetime = datetime.utcnow(), level: int = 1, experience: int = 0, gold: int = 0, stats: Dict = {"strength": 10, "agility": 10, "intelligence": 10, "vitality": 10}, max_hp: int = 100, current_hp: int = 100, equipment: Dict = {"Weapon": get_equipment_by_id("W000"), "Armor": get_equipment_by_id("A000"), "Helmet": get_equipment_by_id("H000"), "Accessory": get_equipment_by_id("ACC000")}, inventory: List = [], inventory_size: int = 20, character_class: Optional[str] = None, current_party_id: Optional[str] = None, guild_id: Optional[str] = None, tower_level: int = 1):
        self.discord_id = discord_id
        self.username = username
        self.created_at = created_at
        self.last_active = last_active
        self.level = level
        self.experience = experience
        self.gold = gold
        self.stats = stats
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.equipment = equipment
        self.inventory = inventory
        self.inventory_size = inventory_size
        self.character_class = character_class
        self.current_party_id = current_party_id
        self.guild_id = guild_id
        self.tower_level = tower_level

    def to_dict(self) -> Dict:
        """Convert player data to dictionary"""
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
        """Create a Player instance from dictionary"""
        player = cls(data["discord_id"], data["username"])
        
        player.created_at = data.get("created_at", datetime.utcnow())
        player.last_active = data.get("last_active", datetime.utcnow())
        
        player.level = data.get("level", 1)
        player.experience = data.get("experience", 0)
        player.gold = data.get("gold", 0)
        
        player.stats = data.get("stats", {
            "strength": 10,
            "agility": 10,
            "intelligence": 10,
            "vitality": 10
        })
        
        player.max_hp = data.get("max_hp", 100)
        player.current_hp = data.get("current_hp", 100)
        
        player.equipment = data.get("equipment", {
             "Weapon": get_equipment_by_id("W000"),
            "Armor": get_equipment_by_id("A000"),
            "Helmet": get_equipment_by_id("H000"),
            "Accessory": get_equipment_by_id("ACC000")
        })
        
        player.inventory = data.get("inventory", [])
        player.inventory_size = data.get("inventory_size", 20)
        
        player.character_class = data.get("character_class")
        player.current_party_id = data.get("current_party_id")
        player.guild_id = data.get('guild_id')
        player.tower_level = data.get('tower_level')

        return player
    
   
    def calculate_equipment_power(entity):
        power_stats = {
            'strength': 1.0,  # Note: lowercase to match your stats dict
            'agility': 1.0,
            'intelligence': 1.0,
            'vitality': 1.0
        }
        
        equipment_power = 0
        
        for item in entity.equipment.values():
            if item:
                # Calculate power based on individual stat weights
                item_power = sum(
                    item['stats'].get(stat.capitalize(), 0) * weight 
                    for stat, weight in power_stats.items()
                )
                
                # Optional: Add level scaling
                item_power *= (1 + (item.get('level', 1) - 1) * 0.1)
                
                equipment_power += item_power
        
        return equipment_power
    