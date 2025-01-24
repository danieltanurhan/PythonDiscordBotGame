from typing import List, Dict
from Game.Database.database import Database

class Monster:
    def __init__(self, monster_id, name, level, rarity, monster_type, hp, damage, defense, 
                 experience_reward, gold_reward, loot_table):
        self.monster_id = monster_id
        self.name = name
        self.level = level
        self.rarity = rarity  # Add this line
        self.monster_type = monster_type
        self.hp = hp
        self.damage = damage
        self.defense = defense
        self.experience_reward = experience_reward
        self.gold_reward = gold_reward
        self.loot_table = loot_table

    def to_dict(self) -> Dict:
        """Convert Monster data to dictionary for MongoDB storage"""
        return {
            "monster_id": self.monster_id,
            "name": self.name,
            "level": self.level,
            "rarity": self.rarity,
            "monster_type": self.monster_type,
            "hp": self.hp,
            "damage": self.damage,
            "defense": self.defense,
            "experience_reward": self.experience_reward,
            "gold_reward": self.gold_reward,
            "loot_table": self.loot_table
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)

    @classmethod
    def get_by_id(cls, monster_id: str):
        db = Database()
        monster_data = db.get_monsters_collection().find_one({"monster_id": monster_id})
        return cls.from_dict(monster_data) if monster_data else None

    @classmethod
    def get_by_rank(cls, rarity: str):
        db = Database()
        monsters_data = db.get_monsters_collection().find({"rarity": rarity.upper()})
        return [cls.from_dict(data) for data in monsters_data]

    def save_to_database(self):
        db = Database()
        db.get_monsters_collection().update_one(
            {"monster_id": self.monster_id},
            {"$set": self.to_dict()},
            upsert=True
        )