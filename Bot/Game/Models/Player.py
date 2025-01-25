from datetime import datetime
from typing import Dict, List, Optional
import discord

class Player:
    def __init__(self, discord_id: str, username: str):
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
            "Weapon": None,
            "Armor": None,
            "Helmet": None,
            "Accessory": None
        }
        
        self.inventory = []
        self.inventory_size = 20
        self.character_class = None
        self.current_party_id = None
        self.guild_id = None
        self.tower_level = 1

    def create_stats_embed(self) -> discord.Embed:
        """Create an embed displaying player stats with emojis"""
        embed = discord.Embed(
            title=f"{self.username}'s Stats",
            color=discord.Color.blue()
        )
        
        # Stats section
        stats_value = (
            f"💪 Strength: {self.stats['strength']}\n"
            f"🏃 Agility: {self.stats['agility']}\n"
            f"🧠 Intelligence: {self.stats['intelligence']}\n"
            f"❤️ Vitality: {self.stats['vitality']}"
        )
        embed.add_field(name="Base Stats", value=stats_value, inline=False)
        
        # Character Info section
        char_info = (
            f"📊 Level: {self.level}\n"
            f"💰 Gold: {self.gold}\n"
            f"✨ Experience: {self.experience}\n"
            f"🏰 Tower Level: {self.tower_level}"
        )
        embed.add_field(name="Character Info", value=char_info, inline=False)
        
        # HP section
        embed.add_field(
            name="Health", 
            value=f"❤️ {self.current_hp}/{self.max_hp}", 
            inline=False
        )
        
        return embed

    def create_equipment_embed(self) -> discord.Embed:
        """Create an embed displaying player equipment with emojis"""
        embed = discord.Embed(
            title=f"{self.username}'s Equipment",
            color=discord.Color.green()
        )
        
        # Equipment section
        equipment_value = (
            f"⚔️ Weapon: {self.equipment['Weapon'] or 'None'}\n"
            f"🛡️ Armor: {self.equipment['Armor'] or 'None'}\n"
            f"🪖 Helmet: {self.equipment['Helmet'] or 'None'}\n"
            f"💍 Accessory: {self.equipment['Accessory'] or 'None'}"
        )
        embed.add_field(name="Equipped Items", value=equipment_value, inline=False)
        
        return embed

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
            "Weapon": None,
            "Armor": None,
            "Helmet": None,
            "Accessory": None
        })
        
        player.inventory = data.get("inventory", [])
        player.inventory_size = data.get("inventory_size", 20)
        
        player.character_class = data.get("character_class")
        player.current_party_id = data.get("current_party_id")
        player.guild_id = data.get('guild_id')
        player.tower_level = data.get('tower_level')

        return player
    