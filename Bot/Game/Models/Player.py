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
        self.loot_inventory = {}  # Dictionary to store loot_id: quantity
        self.upgrades = {
            "salesman": 1,
            "worker": 1,
            "mount": 1
        }
        self.last_raid_time = datetime.utcnow()
        
    def __init__(self, discord_id: str, username: str, created_at: datetime = datetime.utcnow(), last_active: datetime = datetime.utcnow(), level: int = 1, experience: int = 0, gold: int = 0, stats: Dict = {"strength": 10, "agility": 10, "intelligence": 10, "vitality": 10}, max_hp: int = 100, current_hp: int = 100, equipment: Dict = {"Weapon": get_equipment_by_id("W000"), "Armor": get_equipment_by_id("A000"), "Helmet": get_equipment_by_id("H000"), "Accessory": get_equipment_by_id("ACC000")}, inventory: List = [], inventory_size: int = 20, character_class: Optional[str] = None, current_party_id: Optional[str] = None, guild_id: Optional[str] = None, tower_level: int = 1, loot_inventory: Dict = None, upgrades: Dict = None):
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
        self.loot_inventory = loot_inventory if loot_inventory is not None else {}
        self.upgrades = upgrades if upgrades is not None else {
            "salesman": 1,
            "worker": 1,
            "mount": 1
        }
        self.last_raid_time = datetime.utcnow()

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
            "tower_level": self.tower_level,
            "loot_inventory": self.loot_inventory,
            "upgrades": self.upgrades,
            "last_raid_time": self.last_raid_time,  # Add this line
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
        player.loot_inventory = data.get("loot_inventory", {})
        player.upgrades = data.get("upgrades", {
            "salesman": 1,
            "worker": 1,
            "mount": 1
        })
        player.last_raid_time = data.get("last_raid_time", datetime.utcnow())  # Add this line

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

    def has_equipment(self, equipment_id: str) -> bool:
        """Check if player owns specific equipment"""
        return equipment_id in self.inventory

    def has_equipped(self, equipment_id: str) -> bool:
        """Check if player has specific equipment equipped"""
        for item in self.equipment.values():
            # Handle both dictionary and string cases
            if isinstance(item, dict):
                if item.get('id') == equipment_id:
                    return True
            elif isinstance(item, str):
                if item == equipment_id:
                    return True
        return False

    def can_afford(self, price: int) -> bool:
        """Check if player has enough gold"""
        return self.gold >= price

    def can_equip(self, level_requirement: int) -> bool:
        """Check if player meets level requirement"""
        return self.level >= level_requirement

    def equip_item(self, new_item: dict, slot_type: str) -> None:
        """
        Equip new item to specified slot and move current item to inventory
        slot_type should be "Weapon", "Armor", "Helmet", or "Accessory"
        """
        current_item = self.equipment.get(slot_type)
        if current_item:
            # Add current item's ID to inventory if not already there
            if isinstance(current_item, dict) and current_item.get('id') not in self.inventory:
                self.inventory.append(current_item['id'])
            elif isinstance(current_item, str) and current_item not in self.inventory:
                self.inventory.append(current_item)
        
        # Equip new item
        self.equipment[slot_type] = new_item

    def purchase_equipment(self, equipment_id: str, price: int, slot_type: str) -> bool:
        """
        Purchase equipment and add to inventory
        Returns True if purchase successful
        """
        if not self.can_afford(price):
            return False

        self.gold -= price
        self.inventory.append(equipment_id)
        self.equip_item(get_equipment_by_id(equipment_id), slot_type)
        return True

    # Mark old functions as deprecated or remove them
    def equip_new_weapon(self, new_weapon: dict) -> None:
        """Deprecated: Use equip_item instead"""
        self.equip_item(new_weapon, "Weapon")

    # Add new methods for loot management
    def add_loot(self, loot_id: str, quantity: int = 1) -> None:
        """Add loot to the player's loot inventory"""
        if loot_id in self.loot_inventory:
            self.loot_inventory[loot_id] += quantity
        else:
            self.loot_inventory[loot_id] = quantity

    def remove_loot(self, loot_id: str = None, quantity: int = None) -> bool:
        """
        Remove loot from the player's loot inventory
        If no loot_id is provided, clears entire inventory
        If no quantity is provided, removes all of the specified loot
        Returns True if successful, False if not enough loot or invalid loot_id
        """
        # Clear entire inventory if no loot_id provided
        if loot_id is None:
            self.loot_inventory.clear()
            return True
            
        # Check if loot exists in inventory
        if loot_id not in self.loot_inventory:
            return False
            
        # Remove all of specific loot if no quantity provided
        if quantity is None:
            del self.loot_inventory[loot_id]
            return True
            
        # Remove specific quantity if provided
        if self.loot_inventory[loot_id] >= quantity:
            self.loot_inventory[loot_id] -= quantity
            if self.loot_inventory[loot_id] == 0:
                del self.loot_inventory[loot_id]
            return True
            
        return False

    def clear_loot(self) -> None:
        """Clear all loot from inventory"""
        self.loot_inventory.clear()

    def get_loot_quantity(self, loot_id: str) -> int:
        """Get the quantity of a specific loot item"""
        return self.loot_inventory.get(loot_id, 0)

    # Add new methods for upgrade management
    def get_upgrade_level(self, upgrade_type: str) -> int:
        """Get the level of a specific upgrade"""
        return self.upgrades.get(upgrade_type, 1)

    def upgrade(self, upgrade_type: str) -> bool:
        """
        Increment the level of a specific upgrade
        Returns True if successful, False if upgrade_type doesn't exist
        """
        if upgrade_type in self.upgrades:
            self.upgrades[upgrade_type] += 1
            return True
        return False

    def check_raid_cooldown(self) -> tuple[bool, float, float]:
        """
        Check if player can raid based on mount level and last raid time
        Returns tuple of (can_raid: bool, remaining_cooldown: float)
        """
        mount_level = self.upgrades.get("mount", 1)
        base_cooldown = 3.5  # Base cooldown in seconds
        
        # Reduce cooldown based on mount level (15% reduction per level)
        cooldown_reduction = (mount_level - 1) * 0.15
        actual_cooldown = max(0.5, base_cooldown * (1 - cooldown_reduction))
        
        current_time = datetime.utcnow()
        time_since_last_raid = (current_time - self.last_raid_time).total_seconds()
        
        if time_since_last_raid >= actual_cooldown:
            return True, 0, 0
        
        return False, actual_cooldown - time_since_last_raid, actual_cooldown
