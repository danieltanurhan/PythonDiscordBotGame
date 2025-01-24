# from dataclasses import dataclass, field
# from typing import List, Dict, Optional

# @dataclass
# class Monster:
#     monster_id: str
#     name: str
#     level: int
#     rarity: str  # E, D, C, B, A, S
#     monster_type: str
#     hp: int
#     damage: int
#     defense: int
#     experience_reward: int
#     gold_reward: int
#     loot_table: List[Dict[str, float]] = field(default_factory=list)

#     def to_dict(self) -> Dict:
#         """Convert Monster data to dictionary."""
#         return {
#             "monster_id": self.monster_id,
#             "name": self.name,
#             "level": self.level,
#             "rarity": self.rarity,
#             "monster_type": self.monster_type,
#             "hp": self.hp,
#             "damage": self.damage,
#             "defense": self.defense,
#             "experience_reward": self.experience_reward,
#             "gold_reward": self.gold_reward,
#             "loot_table": self.loot_table
#         }

# class MonsterDatabase:
#     def __init__(self):
#         self.monsters: Dict[str, Monster] = {}
#         self._initialize_monsters()

#     def _initialize_monsters(self):
#         """Initialize all 50 monsters and add them to the database."""
        

#         for data in monster_data:
#             monster = Monster(
#                 monster_id=data["monster_id"],
#                 name=data["name"],
#                 level=data["level"],
#                 rarity=data["rarity"],
#                 monster_type=data["monster_type"],
#                 hp=data["hp"],
#                 damage=data["damage"],
#                 defense=data["defense"],
#                 experience_reward=data["experience_reward"],
#                 gold_reward=data["gold_reward"],
#                 loot_table=data["loot_table"]
#             )
#             self.monsters[monster.monster_id] = monster

#     def get_monster_by_id(self, monster_id: str) -> Optional[Monster]:
#         """Retrieve a monster by its ID."""
#         return self.monsters.get(monster_id)

#     def get_monsters_by_rank(self, rarity: str) -> List[Monster]:
#         """Retrieve all monsters of a specific rank."""
#         return [monster for monster in self.monsters.values() if monster.rarity.upper() == rarity.upper()]

#     def get_monsters_by_type(self, monster_type: str) -> List[Monster]:
#         """Retrieve all monsters of a specific type."""
#         return [monster for monster in self.monsters.values() if monster.monster_type.lower() == monster_type.lower()]

#     def list_all_monsters(self) -> List[Monster]:
#         """List all monsters in the database."""
#         return list(self.monsters.values())

# # Example Usage
# if __name__ == "__main__":
#     # Initialize the Monster Database
#     db = MonsterDatabase()

#     # Retrieve a monster by ID
#     monster_id = "A001"
#     monster = db.get_monster_by_id(monster_id)
#     if monster:
#         print(f"Monster ID: {monster.monster_id}")
#         print(f"Name: {monster.name}")
#         print(f"Level: {monster.level}")
#         print(f"Rarity: {monster.rarity}")
#         print(f"Type: {monster.monster_type}")
#         print(f"HP: {monster.hp}")
#         print(f"Damage: {monster.damage}")
#         print(f"Defense: {monster.defense}")
#         print(f"Experience Reward: {monster.experience_reward}")
#         print(f"Gold Reward: {monster.gold_reward}")
#         print("Loot Table:")
#         for loot in monster.loot_table:
#             print(f"  - {loot['item']} (Probability: {loot['probability']})")
#     else:
#         print(f"Monster with ID {monster_id} not found.")

#     print("\n" + "-"*50 + "\n")

#     # Retrieve all S Rank monsters
#     s_rank_monsters = db.get_monsters_by_rank("S")
#     print(f"Total S Rank Monsters: {len(s_rank_monsters)}")
#     for m in s_rank_monsters:
#         print(f"{m.monster_id}: {m.name} (Level {m.level})")

#     print("\n" + "-"*50 + "\n")

#     # Retrieve all Elemental type monsters
#     elemental_monsters = db.get_monsters_by_type("Elemental")
#     print(f"Total Elemental Monsters: {len(elemental_monsters)}")
#     for m in elemental_monsters:
#         print(f"{m.monster_id}: {m.name} (Rank {m.rarity})")

#     print("\n" + "-"*50 + "\n")

#     # List all monsters
#     all_monsters = db.list_all_monsters()
#     print(f"Total Monsters in Database: {len(all_monsters)}")
#     # Uncomment the following lines to print all monsters
#     for m in all_monsters:
#         print(f"{m.monster_id}: {m.name} (Rank {m.rarity}, Type {m.monster_type})")
