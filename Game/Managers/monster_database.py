from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class Monster:
    monster_id: str
    name: str
    level: int
    rarity: str  # E, D, C, B, A, S
    monster_type: str
    hp: int
    damage: int
    defense: int
    experience_reward: int
    gold_reward: int
    loot_table: List[Dict[str, float]] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert Monster data to dictionary."""
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

class MonsterDatabase:
    def __init__(self):
        self.monsters: Dict[str, Monster] = {}
        self._initialize_monsters()

    def _initialize_monsters(self):
        """Initialize all 50 monsters and add them to the database."""
        monster_data = [
            # **E Rank**
            {
                "monster_id": "E001",
                "name": "Goblin Scout",
                "level": 1,
                "rarity": "E",
                "monster_type": "Humanoid",
                "hp": 30,
                "damage": 4,
                "defense": 1,
                "experience_reward": 10,
                "gold_reward": 5,
                "loot_table": [
                    {"item": "Scout's Bandana", "probability": 0.6},
                    {"item": "Goblin Dagger", "probability": 0.4}
                ]
            },
            {
                "monster_id": "E002",
                "name": "Goblin Grunt",
                "level": 2,
                "rarity": "E",
                "monster_type": "Humanoid",
                "hp": 35,
                "damage": 5,
                "defense": 2,
                "experience_reward": 12,
                "gold_reward": 6,
                "loot_table": [
                    {"item": "Goblin Ear", "probability": 0.7},
                    {"item": "Small Coin", "probability": 0.3}
                ]
            },
            {
                "monster_id": "E003",
                "name": "Goblin Warrior",
                "level": 3,
                "rarity": "E",
                "monster_type": "Humanoid",
                "hp": 40,
                "damage": 6,
                "defense": 3,
                "experience_reward": 15,
                "gold_reward": 7,
                "loot_table": [
                    {"item": "Goblin Axe", "probability": 0.5},
                    {"item": "Warrior Shield", "probability": 0.5}
                ]
            },
            {
                "monster_id": "E004",
                "name": "Forest Rat",
                "level": 4,
                "rarity": "E",
                "monster_type": "Beast",
                "hp": 25,
                "damage": 2,
                "defense": 1,
                "experience_reward": 8,
                "gold_reward": 4,
                "loot_table": [
                    {"item": "Rat Tail", "probability": 0.6},
                    {"item": "Claw", "probability": 0.4}
                ]
            },
            {
                "monster_id": "E005",
                "name": "Cave Bat",
                "level": 5,
                "rarity": "E",
                "monster_type": "Beast",
                "hp": 30,
                "damage": 3,
                "defense": 1,
                "experience_reward": 9,
                "gold_reward": 5,
                "loot_table": [
                    {"item": "Bat Wing", "probability": 0.5},
                    {"item": "Echo Dust", "probability": 0.5}
                ]
            },
            {
                "monster_id": "E006",
                "name": "Slime Pup",
                "level": 6,
                "rarity": "E",
                "monster_type": "Elemental",
                "hp": 28,
                "damage": 3,
                "defense": 1,
                "experience_reward": 7,
                "gold_reward": 3,
                "loot_table": [
                    {"item": "Slime Gel", "probability": 0.7},
                    {"item": "Small Coin", "probability": 0.3}
                ]
            },
            {
                "monster_id": "E007",
                "name": "Ember Sprite",
                "level": 7,
                "rarity": "E",
                "monster_type": "Elemental",
                "hp": 32,
                "damage": 4,
                "defense": 2,
                "experience_reward": 10,
                "gold_reward": 5,
                "loot_table": [
                    {"item": "Ember Stone", "probability": 0.6},
                    {"item": "Sprite Dust", "probability": 0.4}
                ]
            },
            {
                "monster_id": "E008",
                "name": "Swamp Lizard",
                "level": 8,
                "rarity": "E",
                "monster_type": "Reptile",
                "hp": 34,
                "damage": 5,
                "defense": 2,
                "experience_reward": 11,
                "gold_reward": 6,
                "loot_table": [
                    {"item": "Lizard Scale", "probability": 0.6},
                    {"item": "Venom Sac", "probability": 0.4}
                ]
            },
            {
                "monster_id": "E009",
                "name": "Skeleton Archer",
                "level": 9,
                "rarity": "E",
                "monster_type": "Undead",
                "hp": 36,
                "damage": 6,
                "defense": 2,
                "experience_reward": 13,
                "gold_reward": 7,
                "loot_table": [
                    {"item": "Bone Arrow", "probability": 0.5},
                    {"item": "Skeleton Bow", "probability": 0.5}
                ]
            },
            {
                "monster_id": "E010",
                "name": "Dire Wolf",
                "level": 10,
                "rarity": "E",
                "monster_type": "Beast",
                "hp": 38,
                "damage": 7,
                "defense": 3,
                "experience_reward": 14,
                "gold_reward": 8,
                "loot_table": [
                    {"item": "Wolf Pelt", "probability": 0.7},
                    {"item": "Fang", "probability": 0.3}
                ]
            },
            # **D Rank**
            {
                "monster_id": "D001",
                "name": "Goblin Thief",
                "level": 11,
                "rarity": "D",
                "monster_type": "Humanoid",
                "hp": 45,
                "damage": 8,
                "defense": 4,
                "experience_reward": 20,
                "gold_reward": 10,
                "loot_table": [
                    {"item": "Thief's Cloak", "probability": 0.5},
                    {"item": "Silver Coin", "probability": 0.5}
                ]
            },
            {
                "monster_id": "D002",
                "name": "Fire Imp",
                "level": 12,
                "rarity": "D",
                "monster_type": "Elemental",
                "hp": 50,
                "damage": 9,
                "defense": 5,
                "experience_reward": 22,
                "gold_reward": 11,
                "loot_table": [
                    {"item": "Imp Horn", "probability": 0.5},
                    {"item": "Fire Stone", "probability": 0.5}
                ]
            },
            {
                "monster_id": "D003",
                "name": "Swamp Troll",
                "level": 13,
                "rarity": "D",
                "monster_type": "Humanoid",
                "hp": 55,
                "damage": 10,
                "defense": 6,
                "experience_reward": 25,
                "gold_reward": 12,
                "loot_table": [
                    {"item": "Troll Hide", "probability": 0.6},
                    {"item": "Mossy Club", "probability": 0.4}
                ]
            },
            {
                "monster_id": "D004",
                "name": "Ice Sprite",
                "level": 14,
                "rarity": "D",
                "monster_type": "Elemental",
                "hp": 48,
                "damage": 9,
                "defense": 4,
                "experience_reward": 21,
                "gold_reward": 10,
                "loot_table": [
                    {"item": "Ice Crystal", "probability": 0.5},
                    {"item": "Sprite Dust", "probability": 0.5}
                ]
            },
            {
                "monster_id": "D005",
                "name": "Bone Collector",
                "level": 15,
                "rarity": "D",
                "monster_type": "Undead",
                "hp": 52,
                "damage": 10,
                "defense": 5,
                "experience_reward": 23,
                "gold_reward": 11,
                "loot_table": [
                    {"item": "Bone Shard", "probability": 0.5},
                    {"item": "Collector's Robe", "probability": 0.5}
                ]
            },
            {
                "monster_id": "D006",
                "name": "Dark Wolf",
                "level": 16,
                "rarity": "D",
                "monster_type": "Beast",
                "hp": 60,
                "damage": 12,
                "defense": 5,
                "experience_reward": 27,
                "gold_reward": 13,
                "loot_table": [
                    {"item": "Dark Fur", "probability": 0.6},
                    {"item": "Fang", "probability": 0.4}
                ]
            },
            {
                "monster_id": "D007",
                "name": "Venomous Snake",
                "level": 17,
                "rarity": "D",
                "monster_type": "Reptile",
                "hp": 58,
                "damage": 11,
                "defense": 5,
                "experience_reward": 24,
                "gold_reward": 12,
                "loot_table": [
                    {"item": "Snake Fang", "probability": 0.6},
                    {"item": "Venom Sac", "probability": 0.4}
                ]
            },
            {
                "monster_id": "D008",
                "name": "Shadow Assassin",
                "level": 18,
                "rarity": "D",
                "monster_type": "Undead",
                "hp": 62,
                "damage": 13,
                "defense": 6,
                "experience_reward": 28,
                "gold_reward": 14,
                "loot_table": [
                    {"item": "Shadow Blade", "probability": 0.5},
                    {"item": "Assassin's Hood", "probability": 0.5}
                ]
            },
            {
                "monster_id": "D009",
                "name": "Frost Wraith",
                "level": 19,
                "rarity": "D",
                "monster_type": "Undead",
                "hp": 65,
                "damage": 14,
                "defense": 6,
                "experience_reward": 30,
                "gold_reward": 15,
                "loot_table": [
                    {"item": "Frost Essence", "probability": 0.6},
                    {"item": "Wraith Cloak", "probability": 0.4}
                ]
            },
            {
                "monster_id": "D010",
                "name": "Thunder Roc",
                "level": 20,
                "rarity": "D",
                "monster_type": "Beast",
                "hp": 68,
                "damage": 15,
                "defense": 7,
                "experience_reward": 32,
                "gold_reward": 16,
                "loot_table": [
                    {"item": "Roc Feather", "probability": 0.5},
                    {"item": "Thunder Stone", "probability": 0.5}
                ]
            },
            # **C Rank**
            {
                "monster_id": "C001",
                "name": "Goblin Warrior",
                "level": 21,
                "rarity": "C",
                "monster_type": "Humanoid",
                "hp": 75,
                "damage": 18,
                "defense": 8,
                "experience_reward": 50,
                "gold_reward": 25,
                "loot_table": [
                    {"item": "Warrior's Sword", "probability": 0.5},
                    {"item": "Goblin Armor", "probability": 0.5}
                ]
            },
            {
                "monster_id": "C002",
                "name": "Stone Sentinel",
                "level": 22,
                "rarity": "C",
                "monster_type": "Elemental",
                "hp": 80,
                "damage": 19,
                "defense": 9,
                "experience_reward": 55,
                "gold_reward": 28,
                "loot_table": [
                    {"item": "Stone Shard", "probability": 0.6},
                    {"item": "Sentinel Core", "probability": 0.4}
                ]
            },
            {
                "monster_id": "C003",
                "name": "Venomous Basilisk",
                "level": 23,
                "rarity": "C",
                "monster_type": "Reptile",
                "hp": 85,
                "damage": 20,
                "defense": 10,
                "experience_reward": 60,
                "gold_reward": 30,
                "loot_table": [
                    {"item": "Basilisk Fang", "probability": 0.6},
                    {"item": "Venom Gland", "probability": 0.4}
                ]
            },
            {
                "monster_id": "C004",
                "name": "Undead Knight",
                "level": 24,
                "rarity": "C",
                "monster_type": "Undead",
                "hp": 90,
                "damage": 21,
                "defense": 11,
                "experience_reward": 65,
                "gold_reward": 32,
                "loot_table": [
                    {"item": "Knight's Shield", "probability": 0.5},
                    {"item": "Undead Armor", "probability": 0.5}
                ]
            },
            {
                "monster_id": "C005",
                "name": "Ember Fox",
                "level": 25,
                "rarity": "C",
                "monster_type": "Beast",
                "hp": 78,
                "damage": 19,
                "defense": 9,
                "experience_reward": 58,
                "gold_reward": 29,
                "loot_table": [
                    {"item": "Ember Tail", "probability": 0.6},
                    {"item": "Fox Fur", "probability": 0.4}
                ]
            },
            {
                "monster_id": "C006",
                "name": "Dark Mage",
                "level": 26,
                "rarity": "C",
                "monster_type": "Humanoid",
                "hp": 95,
                "damage": 22,
                "defense": 12,
                "experience_reward": 70,
                "gold_reward": 35,
                "loot_table": [
                    {"item": "Magic Tome", "probability": 0.5},
                    {"item": "Mage Robe", "probability": 0.5}
                ]
            },
            {
                "monster_id": "C007",
                "name": "Iron Golem",
                "level": 27,
                "rarity": "C",
                "monster_type": "Elemental",
                "hp": 100,
                "damage": 23,
                "defense": 13,
                "experience_reward": 75,
                "gold_reward": 38,
                "loot_table": [
                    {"item": "Iron Nugget", "probability": 0.6},
                    {"item": "Golem Core", "probability": 0.4}
                ]
            },
            {
                "monster_id": "C008",
                "name": "Swamp Hydra",
                "level": 28,
                "rarity": "C",
                "monster_type": "Beast",
                "hp": 105,
                "damage": 24,
                "defense": 14,
                "experience_reward": 80,
                "gold_reward": 40,
                "loot_table": [
                    {"item": "Hydra Scale", "probability": 0.5},
                    {"item": "Venom Drip", "probability": 0.5}
                ]
            },
            {
                "monster_id": "C009",
                "name": "Frost Wraith",
                "level": 29,
                "rarity": "C",
                "monster_type": "Undead",
                "hp": 110,
                "damage": 25,
                "defense": 15,
                "experience_reward": 85,
                "gold_reward": 42,
                "loot_table": [
                    {"item": "Frost Essence", "probability": 0.6},
                    {"item": "Wraith Cloak", "probability": 0.4}
                ]
            },
            {
                "monster_id": "C010",
                "name": "Thunder Roc",
                "level": 30,
                "rarity": "C",
                "monster_type": "Beast",
                "hp": 115,
                "damage": 26,
                "defense": 16,
                "experience_reward": 90,
                "gold_reward": 45,
                "loot_table": [
                    {"item": "Roc Feather", "probability": 0.5},
                    {"item": "Thunder Stone", "probability": 0.5}
                ]
            },
            # **B Rank**
            {
                "monster_id": "B001",
                "name": "Lava Drake",
                "level": 31,
                "rarity": "B",
                "monster_type": "Dragon",
                "hp": 130,
                "damage": 35,
                "defense": 18,
                "experience_reward": 120,
                "gold_reward": 60,
                "loot_table": [
                    {"item": "Drake Scale", "probability": 0.5},
                    {"item": "Lava Gem", "probability": 0.5}
                ]
            },
            {
                "monster_id": "B002",
                "name": "Shadow Knight",
                "level": 32,
                "rarity": "B",
                "monster_type": "Humanoid",
                "hp": 140,
                "damage": 36,
                "defense": 19,
                "experience_reward": 125,
                "gold_reward": 62,
                "loot_table": [
                    {"item": "Shadow Armor", "probability": 0.5},
                    {"item": "Knight's Sword", "probability": 0.5}
                ]
            },
            {
                "monster_id": "B003",
                "name": "Toxic Sludge",
                "level": 33,
                "rarity": "B",
                "monster_type": "Elemental",
                "hp": 150,
                "damage": 38,
                "defense": 20,
                "experience_reward": 130,
                "gold_reward": 65,
                "loot_table": [
                    {"item": "Sludge Core", "probability": 0.6},
                    {"item": "Toxic Residue", "probability": 0.4}
                ]
            },
            {
                "monster_id": "B004",
                "name": "Bone Collector",
                "level": 34,
                "rarity": "B",
                "monster_type": "Undead",
                "hp": 160,
                "damage": 40,
                "defense": 21,
                "experience_reward": 135,
                "gold_reward": 68,
                "loot_table": [
                    {"item": "Bone Shard", "probability": 0.5},
                    {"item": "Collector's Robe", "probability": 0.5}
                ]
            },
            {
                "monster_id": "B005",
                "name": "Venom Titan",
                "level": 35,
                "rarity": "B",
                "monster_type": "Reptile",
                "hp": 170,
                "damage": 42,
                "defense": 22,
                "experience_reward": 140,
                "gold_reward": 70,
                "loot_table": [
                    {"item": "Titan Fang", "probability": 0.6},
                    {"item": "Venom Gland", "probability": 0.4}
                ]
            },
            {
                "monster_id": "B006",
                "name": "Ice Colossus",
                "level": 36,
                "rarity": "B",
                "monster_type": "Elemental",
                "hp": 180,
                "damage": 44,
                "defense": 23,
                "experience_reward": 145,
                "gold_reward": 73,
                "loot_table": [
                    {"item": "Colossus Heart", "probability": 0.5},
                    {"item": "Ice Crystal", "probability": 0.5}
                ]
            },
            {
                "monster_id": "B007",
                "name": "Dread Sorcerer",
                "level": 37,
                "rarity": "B",
                "monster_type": "Humanoid",
                "hp": 190,
                "damage": 46,
                "defense": 24,
                "experience_reward": 150,
                "gold_reward": 75,
                "loot_table": [
                    {"item": "Sorcerer's Staff", "probability": 0.5},
                    {"item": "Dark Scroll", "probability": 0.5}
                ]
            },
            {
                "monster_id": "B008",
                "name": "Abyssal Kraken",
                "level": 38,
                "rarity": "B",
                "monster_type": "Sea Monster",
                "hp": 200,
                "damage": 48,
                "defense": 25,
                "experience_reward": 155,
                "gold_reward": 78,
                "loot_table": [
                    {"item": "Kraken Tentacle", "probability": 0.5},
                    {"item": "Abyssal Pearl", "probability": 0.5}
                ]
            },
            {
                "monster_id": "B009",
                "name": "Fire Phoenix",
                "level": 39,
                "rarity": "B",
                "monster_type": "Mythical",
                "hp": 210,
                "damage": 50,
                "defense": 26,
                "experience_reward": 160,
                "gold_reward": 80,
                "loot_table": [
                    {"item": "Phoenix Feather", "probability": 0.5},
                    {"item": "Fire Essence", "probability": 0.5}
                ]
            },
            {
                "monster_id": "B010",
                "name": "Venomous Basilisk",
                "level": 40,
                "rarity": "B",
                "monster_type": "Reptile",
                "hp": 220,
                "damage": 52,
                "defense": 27,
                "experience_reward": 165,
                "gold_reward": 82,
                "loot_table": [
                    {"item": "Basilisk Fang", "probability": 0.6},
                    {"item": "Venom Gland", "probability": 0.4}
                ]
            },
            # **A Rank**
            {
                "monster_id": "A001",
                "name": "Celestial Dragon",
                "level": 41,
                "rarity": "A",
                "monster_type": "Dragon",
                "hp": 300,
                "damage": 60,
                "defense": 35,
                "experience_reward": 300,
                "gold_reward": 150,
                "loot_table": [
                    {"item": "Celestial Scale", "probability": 0.4},
                    {"item": "Dragon Claw", "probability": 0.6}
                ]
            },
            {
                "monster_id": "A002",
                "name": "Necrotic Lich",
                "level": 42,
                "rarity": "A",
                "monster_type": "Undead",
                "hp": 320,
                "damage": 62,
                "defense": 36,
                "experience_reward": 310,
                "gold_reward": 155,
                "loot_table": [
                    {"item": "Lich's Phylactery", "probability": 0.3},
                    {"item": "Necrotic Staff", "probability": 0.7}
                ]
            },
            {
                "monster_id": "A003",
                "name": "Thunder Titan",
                "level": 43,
                "rarity": "A",
                "monster_type": "Elemental",
                "hp": 340,
                "damage": 64,
                "defense": 38,
                "experience_reward": 320,
                "gold_reward": 160,
                "loot_table": [
                    {"item": "Thunder Core", "probability": 0.5},
                    {"item": "Titanic Gem", "probability": 0.5}
                ]
            },
            {
                "monster_id": "A004",
                "name": "Mystic Unicorn",
                "level": 44,
                "rarity": "A",
                "monster_type": "Mythical",
                "hp": 360,
                "damage": 66,
                "defense": 40,
                "experience_reward": 330,
                "gold_reward": 165,
                "loot_table": [
                    {"item": "Unicorn Horn", "probability": 0.4},
                    {"item": "Pure Essence", "probability": 0.6}
                ]
            },
            {
                "monster_id": "A005",
                "name": "Abyssal Leviathan",
                "level": 45,
                "rarity": "A",
                "monster_type": "Sea Monster",
                "hp": 380,
                "damage": 68,
                "defense": 42,
                "experience_reward": 340,
                "gold_reward": 170,
                "loot_table": [
                    {"item": "Leviathan Scale", "probability": 0.5},
                    {"item": "Abyssal Pearl", "probability": 0.5}
                ]
            },
            {
                "monster_id": "A006",
                "name": "Dark Overlord",
                "level": 46,
                "rarity": "A",
                "monster_type": "Humanoid",
                "hp": 400,
                "damage": 70,
                "defense": 44,
                "experience_reward": 350,
                "gold_reward": 175,
                "loot_table": [
                    {"item": "Overlord's Crown", "probability": 0.4},
                    {"item": "Dark Armor", "probability": 0.6}
                ]
            },
            {
                "monster_id": "A007",
                "name": "Serpent Queen",
                "level": 47,
                "rarity": "A",
                "monster_type": "Reptile",
                "hp": 420,
                "damage": 72,
                "defense": 46,
                "experience_reward": 360,
                "gold_reward": 180,
                "loot_table": [
                    {"item": "Serpent Crown", "probability": 0.5},
                    {"item": "Queen's Scale", "probability": 0.5}
                ]
            },
            {
                "monster_id": "A008",
                "name": "Arcane Phoenix",
                "level": 48,
                "rarity": "A",
                "monster_type": "Mythical",
                "hp": 440,
                "damage": 74,
                "defense": 48,
                "experience_reward": 370,
                "gold_reward": 185,
                "loot_table": [
                    {"item": "Arcane Feather", "probability": 0.5},
                    {"item": "Fire Essence", "probability": 0.5}
                ]
            },
            {
                "monster_id": "A009",
                "name": "Shadow Behemoth",
                "level": 49,
                "rarity": "A",
                "monster_type": "Undead",
                "hp": 460,
                "damage": 76,
                "defense": 50,
                "experience_reward": 380,
                "gold_reward": 190,
                "loot_table": [
                    {"item": "Behemoth Heart", "probability": 0.4},
                    {"item": "Shadow Blade", "probability": 0.6}
                ]
            },
            {
                "monster_id": "A010",
                "name": "Frost Titan",
                "level": 50,
                "rarity": "A",
                "monster_type": "Elemental",
                "hp": 480,
                "damage": 78,
                "defense": 52,
                "experience_reward": 390,
                "gold_reward": 195,
                "loot_table": [
                    {"item": "Frost Core", "probability": 0.5},
                    {"item": "Titanic Gem", "probability": 0.5}
                ]
            },
            # **S Rank**
            {
                "monster_id": "S001",
                "name": "Celestial Phoenix",
                "level": 51,
                "rarity": "S",
                "monster_type": "Mythical",
                "hp": 600,
                "damage": 90,
                "defense": 60,
                "experience_reward": 800,
                "gold_reward": 400,
                "loot_table": [
                    {"item": "Celestial Feather", "probability": 0.5},
                    {"item": "Rebirth Stone", "probability": 0.5}
                ]
            },
            {
                "monster_id": "S002",
                "name": "Ancient Dragon",
                "level": 52,
                "rarity": "S",
                "monster_type": "Dragon",
                "hp": 620,
                "damage": 92,
                "defense": 62,
                "experience_reward": 820,
                "gold_reward": 410,
                "loot_table": [
                    {"item": "Ancient Scale", "probability": 0.4},
                    {"item": "Dragon Claw", "probability": 0.6}
                ]
            },
            {
                "monster_id": "S003",
                "name": "Eternal Lich",
                "level": 53,
                "rarity": "S",
                "monster_type": "Undead",
                "hp": 640,
                "damage": 94,
                "defense": 64,
                "experience_reward": 840,
                "gold_reward": 420,
                "loot_table": [
                    {"item": "Eternal Phylactery", "probability": 0.3},
                    {"item": "Necrotic Staff", "probability": 0.7}
                ]
            },
            {
                "monster_id": "S004",
                "name": "Thunder Overlord",
                "level": 54,
                "rarity": "S",
                "monster_type": "Elemental",
                "hp": 660,
                "damage": 96,
                "defense": 66,
                "experience_reward": 860,
                "gold_reward": 430,
                "loot_table": [
                    {"item": "Overlord's Crown", "probability": 0.5},
                    {"item": "Thunder Core", "probability": 0.5}
                ]
            },
            {
                "monster_id": "S005",
                "name": "Serpent Emperor",
                "level": 55,
                "rarity": "S",
                "monster_type": "Reptile",
                "hp": 680,
                "damage": 98,
                "defense": 68,
                "experience_reward": 880,
                "gold_reward": 440,
                "loot_table": [
                    {"item": "Emperor's Crown", "probability": 0.5},
                    {"item": "Serpent Fang", "probability": 0.5}
                ]
            },
            {
                "monster_id": "S006",
                "name": "Abyssal Leviathan",
                "level": 56,
                "rarity": "S",
                "monster_type": "Sea Monster",
                "hp": 700,
                "damage": 100,
                "defense": 70,
                "experience_reward": 900,
                "gold_reward": 450,
                "loot_table": [
                    {"item": "Leviathan Heart", "probability": 0.5},
                    {"item": "Abyssal Pearl", "probability": 0.5}
                ]
            },
            {
                "monster_id": "S007",
                "name": "Arcane Behemoth",
                "level": 57,
                "rarity": "S",
                "monster_type": "Mythical",
                "hp": 720,
                "damage": 102,
                "defense": 72,
                "experience_reward": 920,
                "gold_reward": 460,
                "loot_table": [
                    {"item": "Arcane Core", "probability": 0.5},
                    {"item": "Behemoth Heart", "probability": 0.5}
                ]
            },
            {
                "monster_id": "S008",
                "name": "Shadow Emperor",
                "level": 58,
                "rarity": "S",
                "monster_type": "Undead",
                "hp": 740,
                "damage": 104,
                "defense": 74,
                "experience_reward": 940,
                "gold_reward": 470,
                "loot_table": [
                    {"item": "Emperor's Cloak", "probability": 0.4},
                    {"item": "Shadow Blade", "probability": 0.6}
                ]
            },
            {
                "monster_id": "S009",
                "name": "Frost Dragon",
                "level": 59,
                "rarity": "S",
                "monster_type": "Elemental",
                "hp": 760,
                "damage": 106,
                "defense": 76,
                "experience_reward": 960,
                "gold_reward": 480,
                "loot_table": [
                    {"item": "Frost Scale", "probability": 0.5},
                    {"item": "Titanic Gem", "probability": 0.5}
                ]
            },
            {
                "monster_id": "S010",
                "name": "Celestial Overlord",
                "level": 60,
                "rarity": "S",
                "monster_type": "Mythical",
                "hp": 800,
                "damage": 110,
                "defense": 80,
                "experience_reward": 1000,
                "gold_reward": 500,
                "loot_table": [
                    {"item": "Overlord's Crown", "probability": 0.6},
                    {"item": "Rebirth Stone", "probability": 0.4}
                ]
            },
        ]

        for data in monster_data:
            monster = Monster(
                monster_id=data["monster_id"],
                name=data["name"],
                level=data["level"],
                rarity=data["rarity"],
                monster_type=data["monster_type"],
                hp=data["hp"],
                damage=data["damage"],
                defense=data["defense"],
                experience_reward=data["experience_reward"],
                gold_reward=data["gold_reward"],
                loot_table=data["loot_table"]
            )
            self.monsters[monster.monster_id] = monster

    def get_monster_by_id(self, monster_id: str) -> Optional[Monster]:
        """Retrieve a monster by its ID."""
        return self.monsters.get(monster_id)

    def get_monsters_by_rank(self, rarity: str) -> List[Monster]:
        """Retrieve all monsters of a specific rank."""
        return [monster for monster in self.monsters.values() if monster.rarity.upper() == rarity.upper()]

    def get_monsters_by_type(self, monster_type: str) -> List[Monster]:
        """Retrieve all monsters of a specific type."""
        return [monster for monster in self.monsters.values() if monster.monster_type.lower() == monster_type.lower()]

    def list_all_monsters(self) -> List[Monster]:
        """List all monsters in the database."""
        return list(self.monsters.values())

# Example Usage
if __name__ == "__main__":
    # Initialize the Monster Database
    db = MonsterDatabase()

    # Retrieve a monster by ID
    monster_id = "A001"
    monster = db.get_monster_by_id(monster_id)
    if monster:
        print(f"Monster ID: {monster.monster_id}")
        print(f"Name: {monster.name}")
        print(f"Level: {monster.level}")
        print(f"Rarity: {monster.rarity}")
        print(f"Type: {monster.monster_type}")
        print(f"HP: {monster.hp}")
        print(f"Damage: {monster.damage}")
        print(f"Defense: {monster.defense}")
        print(f"Experience Reward: {monster.experience_reward}")
        print(f"Gold Reward: {monster.gold_reward}")
        print("Loot Table:")
        for loot in monster.loot_table:
            print(f"  - {loot['item']} (Probability: {loot['probability']})")
    else:
        print(f"Monster with ID {monster_id} not found.")

    print("\n" + "-"*50 + "\n")

    # Retrieve all S Rank monsters
    s_rank_monsters = db.get_monsters_by_rank("S")
    print(f"Total S Rank Monsters: {len(s_rank_monsters)}")
    for m in s_rank_monsters:
        print(f"{m.monster_id}: {m.name} (Level {m.level})")

    print("\n" + "-"*50 + "\n")

    # Retrieve all Elemental type monsters
    elemental_monsters = db.get_monsters_by_type("Elemental")
    print(f"Total Elemental Monsters: {len(elemental_monsters)}")
    for m in elemental_monsters:
        print(f"{m.monster_id}: {m.name} (Rank {m.rarity})")

    print("\n" + "-"*50 + "\n")

    # List all monsters
    all_monsters = db.list_all_monsters()
    print(f"Total Monsters in Database: {len(all_monsters)}")
    # Uncomment the following lines to print all monsters
    for m in all_monsters:
        print(f"{m.monster_id}: {m.name} (Rank {m.rarity}, Type {m.monster_type})")
