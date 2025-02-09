# File: Bot/Game/Config/balance_config.py

# Combat System Constants
STAT_WEIGHTS = {
    'strength': 1.2,    # Increased weight for damage stats
    'agility': 1.0,
    'intelligence': 1.0,
    'vitality': 1.5     # Increased weight for survival stats
}

# Level and Equipment Scaling
BASE_LEVEL_POWER = 5.0        # Power gained per level
EQUIPMENT_LEVEL_SCALE = 0.1   # 10% power increase per equipment level

# Monster Power Constants
MONSTER_LEVEL_POWER = 6.0     # Base power per monster level
MONSTER_DAMAGE_WEIGHT = 1.3   # Multiplier for monster damage
MONSTER_DEFENSE_WEIGHT = 1.0  # Multiplier for monster defense

# Monster Rarity Multipliers
MONSTER_RARITY_MULTIPLIERS = {
    "E": 1.0,  # Common
    "D": 1.3,  # Uncommon
    "C": 1.6,  # Rare
    "B": 2.0,  # Elite
    "A": 2.5,  # Boss
    "S": 3.0   # Legendary
}

# Combat RNG
MIN_MINDSET_FACTOR = 0.0   # Minimum random factor
MAX_MINDSET_FACTOR = 10.0  # Maximum random factor
MINDSET_IMPACT = 0.05      # How much mindset affects final power (5% per point)