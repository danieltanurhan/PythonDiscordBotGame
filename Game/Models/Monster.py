from typing import Dict

class Monster:
    def __init__(self, monster_id: str, name: str, level: int):
        # Basic Info
        self.monster_id = monster_id
        self.name = name
        self.level = level
        
        # Combat Stats
        self.hp = 0
        self.damage = 0
        self.defense = 0
        
        # Rewards
        self.experience_reward = 0
        self.gold_reward = 0
        self.loot_table = []  # List of possible drops with probabilities
        
        # Monster Type
        self.rarity = "common"  # common, rare, epic, legendary
        self.monster_type = None  # for resistance/weakness system

    def to_dict(self) -> Dict:
        """Convert Monster data to dictionary for MongoDB storage"""
        return {
            "monster_id": self.monster_id,
            "name": self.name,
            "level": self.level,
            "hp": self.hp,
            "damage": self.damage,
            "defense": self.defense,
            "experience_reward": self.experience_reward,
            "gold_reward": self.gold_reward,
            "loot_table": self.loot_table,
            "rarity": self.rarity,
            "monster_type": self.monster_type
        }