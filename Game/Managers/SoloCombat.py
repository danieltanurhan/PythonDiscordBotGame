import random
from datetime import datetime
from typing import Dict, List, Tuple
from Game.Models.Monster import Monster
from Game.Models.Player import Player

class CombatSystem:
    @staticmethod
    def calculate_power_score(entity: Player | Monster, is_player: bool = True) -> float:
        """Calculate power score for either player or monster"""
        base_score = 0
        
        if is_player:
            # Base stats contribution
            base_score += entity.stats["strength"] * 1.5
            base_score += entity.stats["agility"] * 1.2
            base_score += entity.stats["vitality"] * 1.0
            base_score += entity.level * 5
            
            # Equipment bonus (we can expand this later)
            equipment_bonus = 0
            for item in entity.equipment.values():
                if item:
                    equipment_bonus += item.get('power', 0)
            base_score += equipment_bonus
        else:
            # Monster power calculation
            base_score += entity.level * 8
            base_score += entity.damage * 2
            base_score += entity.defense
            
            # Rarity multipliers
            rarity_multipliers = {
                "common": 1.0,
                "rare": 1.3,
                "epic": 1.6,
                "legendary": 2.0
            }
            base_score *= rarity_multipliers.get(entity.rarity, 1.0)
        
        # Add randomness factor (mindset variable)
        mindset = random.uniform(0, 10)
        final_score = base_score * (1 + (mindset / 20))  # Mindset can affect up to ±50%
        
        return final_score

class RaidManager:
    def __init__(self):
        self.combat_system = CombatSystem()

    async def generate_monsters(self, tower_level: int, player_level: int) -> List[Monster]:
        """
        Generate monsters based on tower and player level
        - Base monsters: 3-7 per raid
        - Higher tower levels increase monster count and level
        - Monster level ranges from (player_level - 2) to (player_level + 2)
        """
        # Calculate number of monsters based on tower level
        base_monster_count = random.randint(3, 7)
        bonus_monsters = tower_level // 5  # Every 5 tower levels add potential for 1 more monster
        max_monsters = min(base_monster_count + bonus_monsters, 10)  # Cap at 10 monsters
        num_monsters = random.randint(base_monster_count, max_monsters)
        
        monsters = []
        
        # Tower level influences monster rarity chances
        rarity_chances = {
            "legendary": min(0.05 + (tower_level * 0.005), 0.15),  # Caps at 15%
            "epic": min(0.15 + (tower_level * 0.01), 0.25),        # Caps at 25%
            "rare": min(0.25 + (tower_level * 0.015), 0.35),       # Caps at 35%
            # Common fills the remainder
        }
        
        for _ in range(num_monsters):
            # Determine monster level
            level_variance = random.randint(-2, 2)
            monster_level = max(1, player_level + level_variance + (tower_level // 10))
            
            # Determine rarity
            roll = random.random()
            if roll < rarity_chances["legendary"]:
                rarity = "legendary"
                level_bonus = 4
            elif roll < rarity_chances["legendary"] + rarity_chances["epic"]:
                rarity = "epic"
                level_bonus = 2
            elif roll < rarity_chances["legendary"] + rarity_chances["epic"] + rarity_chances["rare"]:
                rarity = "rare"
                level_bonus = 1
            else:
                rarity = "common"
                level_bonus = 0
                
            # Create monster with scaled stats
            monster = Monster(
                monster_id=f"MON_{datetime.utcnow().timestamp()}_{_}",
                name=f"{rarity.title()} Tower Beast",
                level=monster_level + level_bonus
            )
            
            # Set monster stats based on level and rarity
            rarity_multipliers = {
                "common": 1.0,
                "rare": 1.3,
                "epic": 1.6,
                "legendary": 2.0
            }
            
            multiplier = rarity_multipliers[rarity]
            
            # Base stats calculation
            monster.hp = int((monster_level * 50) * multiplier)
            monster.damage = int((monster_level * 5) * multiplier)
            monster.defense = int((monster_level * 3) * multiplier)
            
            # Set rewards based on level and rarity
            monster.gold_reward = int((monster_level * 10) * multiplier)
            monster.experience_reward = int((monster_level * 15) * multiplier)
            monster.rarity = rarity
            
            monsters.append(monster)
        
        return monsters
    
    async def process_raid(self, player: Player, tower_level: int) -> Dict:
        monsters = await self.generate_monsters(tower_level, player.level)
        
        raid_results = {
            "monsters_defeated": {"common": 0, "rare": 0, "epic": 0, "legendary": 0},
            "total_rewards": {"gold": 0, "experience": 0},
            "battles": [],
            "raid_complete": False,
            "player_survived": True
        }
        
        for monster in monsters:
            if player.current_hp <= 0:
                raid_results["player_survived"] = False
                break
                
            battle_result = await self.process_battle(player, monster)
            raid_results["battles"].append(battle_result)
            
            if battle_result["player_won"]:
                raid_results["monsters_defeated"][battle_result["monster_rarity"]] += 1
                raid_results["total_rewards"]["gold"] += battle_result["rewards"]["gold"]
                raid_results["total_rewards"]["experience"] += battle_result["rewards"]["experience"]
            else:
                # Player lost this battle
                player.current_hp -= battle_result["damage_taken"]
                break
        
        raid_results["raid_complete"] = raid_results["monsters_defeated"] == len(monsters)
        return raid_results

    async def process_battle(self, player: Player, monster: Monster) -> Dict:
        """Process a single battle between player and monster"""
        player_wins = 0
        monster_wins = 0
        
        player_power = self.combat_system.calculate_power_score(player, True)
        monster_power = self.combat_system.calculate_power_score(monster, False)
            
        if player_power > monster_power:
            player_wins += 1
        else:
            monster_wins += 1
                
        player_won = player_wins > monster_wins
        
        # Calculate rewards and damage
        rewards = {
            "gold": monster.gold_reward * (player_wins),
            "experience": monster.experience_reward * (player_wins)
        }
        
        damage_taken = monster_wins * monster.damage
        
        return {
            "player_won": player_won,
            "damage_taken": damage_taken,
            "rewards": rewards,
            "monster_rarity": monster.rarity,
        }

def handle_player_death(player: Player) -> List[Dict]:
    """
    Handle player death consequences - drop items and return to camp
    Returns list of dropped items
    """
    dropped_items = []
    
    # Chance to drop equipped items (30% chance per item)
    for slot, item in player.equipment.items():
        if item and random.random() < 0.3:
            dropped_items.append({
                "slot": slot,
                "item": item
            })
            player.equipment[slot] = None
    
    # Drop 20% of gold
    gold_loss = int(player.gold * 0.2)
    player.gold -= gold_loss
    
    # Reset player state
    player.current_hp = player.max_hp * 0.1  # Return with 10% HP
    player.current_party_id = None  # Remove from party if in one
    
    return dropped_items

def create_raid_summary(results: Dict) -> str:
    """
    Create a detailed summary of the raid results
    """
    # Organize monsters by rarity
    monster_kills = {
        "common": 0,
        "rare": 0,
        "epic": 0,
        "legendary": 0
    }

    total_damage_taken = 0
    for battle in results["battles"]:
        if battle["player_won"]:
            monster_type = battle.get("monster_rarity", "common")
            monster_kills[monster_type] += 1
        total_damage_taken += battle["damage_taken"]
    
    # Create summary text
    summary = "🗡️ **Raid Summary** 🗡️"

    summary += f"\n❤️ **Health Lost:** {total_damage_taken:.0f}\n"
    # Monster kills section
    summary += "**Monsters Defeated:**"
    for rarity, count in monster_kills.items():
        if count > 0:
            rarity_icons = {
                "common": "⚪",
                "rare": "🔵",
                "epic": "🟣",
                "legendary": "🟡"
            }
            summary += f"{rarity_icons[rarity]} {rarity.title()}: {count}\n"
    
    # Rewards section
    summary += "\n**Rewards:**\n"
    summary += f"💰 Gold: {results['total_rewards']['gold']:.0f}\n"
    summary += f"✨ Experience: {results['total_rewards']['experience']:.0f}\n"
    
    # Raid status
    if results["raid_complete"]:
        summary += "\n🏆 Raid Complete! 🏆"
    elif results["player_survived"]:
        summary += "\n⚠️ Raid Abandoned - Retreated safely"
    else:
        summary += "\n💀 Raid Failed - Player Defeated"
        
        # Add dropped items if player died
        if "dropped_items" in results:
            summary += "\n\n**Items Lost:**\n"
            for item in results["dropped_items"]:
                summary += f"❌ {item['slot'].title()}: {item['item']['name']}\n"
    
    return summary

# Example usage in a Discord command
async def handle_raid_command(player: Player, tower_level: int):
    raid_manager = RaidManager()
    results = await raid_manager.process_raid(player, tower_level)
    
    # Update player based on results
    player.gold += results["total_rewards"]["gold"]
    player.experience += results["total_rewards"]["experience"]
    
    if not results["player_survived"]:
        # Handle player death (drop items, return to camp, etc.)
        dropped_items = handle_player_death(player)
    
    # Generate raid summary
    summary = create_raid_summary(results)
    return summary