from Game.Database.database import Database
from Game.Models.Player import Player
from Game.Managers.equipment_db_connection import get_equipment_by_id
import pymongo
import random

db = Database()
players_collection = db.get_players_collection()

def player_exists(discord_id: str) -> bool:
    player_data = players_collection.find_one({"discord_id": discord_id})
    return player_data is not None

async def add_player(discord_id: str, username: str):
    db = Database()
    players_collection = db.get_players_collection()
    
    # Check if player already exists
    existing_player = players_collection.find_one({"discord_id": discord_id})
    if existing_player:
        return None
    
    # Create new player
    new_player = Player(discord_id, username)
    
    # Insert player into database
    players_collection.insert_one(new_player.to_dict())
    
    return new_player

def get_player_by_discord_id(discord_id: str) -> Player:
    player_data = players_collection.find_one({"discord_id": discord_id})
    return Player.from_dict(player_data)

def update_player_hp(player: Player) -> None:
    players_collection.update_one(
        {"discord_id": player.discord_id}, 
        {"$set": {
            "current_hp": player.current_hp
        }}
    )

def update_player_rewards(player: Player, experience: int, raid_results: dict) -> dict:
    """
    Update player's experience and loot inventory after a raid
    Args:
        player: Player object
        experience: Experience gained
        raid_results: Dictionary containing raid results including loot
    Returns:
        Dictionary with update results
    """
    player.experience += experience
    
    # Calculate level up
    base_xp = 100
    level_multiplier = 1.5
    new_level = int((player.experience / base_xp) ** (1 / level_multiplier)) + 1
    
    update_result = {
        "experience_gained": experience,
        "leveled_up": new_level > player.level,
        "loot_gained": raid_results.get("total_rewards", {}).get("loot", {})
    }
    
    if update_result["leveled_up"]:
        player.level = new_level
        update_result["new_level"] = new_level

    # if raid_results["damage_taken"] > 0:
    #     player.current_hp -= raid_results["damage_taken"]
    
    # Update database with new player state
    players_collection.update_one(
        {"discord_id": player.discord_id}, 
        {"$set": {
            "current_hp": player.current_hp,
            "experience": player.experience,
            "level": player.level,
            "loot_inventory": player.loot_inventory,
            "last_raid_time": player.last_raid_time
        }}
    )
    
    return update_result

def handle_player_death(player: Player) -> dict:
    """
    Handle player death consequences and database updates
    
    Returns a summary of lost items and state changes
    """
    death_summary = {
        "dropped_items": [],
        "gold_lost": 0,
        "hp_restored": 0
    }

    
    # Calculate gold loss
    gold_loss = int(player.gold * 0.2)
    player.gold -= gold_loss
    death_summary["gold_lost"] = gold_loss
    
    # Update database with new player state
    players_collection.update_one(
        {"discord_id": player.discord_id},
        {"$set": {
            "current_hp": player.current_hp,
            "gold": player.gold,
        }}
    )
    
    return death_summary

async def handle_gypsy_debuff(player: Player):
    player.current_hp = 69
    player.level = 1
    player.experience = 0
    player.gold += 6969

    players_collection.update_one(
        {"discord_id": player.discord_id},
        {"$set": {
            "current_hp": player.current_hp,
            "level": player.level,
            "experience": player.experience,
            "gold": player.gold
        }}
    )

    return

def update_player_purchase(player: Player, equipment_id: str, price: int, slot_type: str) -> bool:
    """
    Update player's gold, inventory, and equipment after purchase
    Returns True if update successful
    """
    if player.purchase_equipment(equipment_id, price, slot_type):
        players_collection.update_one(
            {"discord_id": player.discord_id},
            {
                "$set": {
                    "gold": player.gold,
                    "equipment": player.equipment,
                    "inventory": player.inventory
                }
            }
        )
        return True
    return False

def update_player_equipment(player: Player, equipment_id: str, slot_type: str) -> bool:
    """
    Update player's equipment and inventory
    Returns True if update successful
    """
    equipment_data = get_equipment_by_id(equipment_id)
    if equipment_data:
        player.equip_item(equipment_data, slot_type)
        players_collection.update_one(
            {"discord_id": player.discord_id},
            {
                "$set": {
                    "equipment": player.equipment,
                    "inventory": player.inventory
                }
            }
        )
        return True
    return False

def update_player_loot(player: Player) -> None:
    """Update player's loot inventory in the database"""
    players_collection.update_one(
        {"discord_id": player.discord_id},
        {
            "$set": {
                "loot_inventory": player.loot_inventory,
                "gold": player.gold
            }
        }
    )

def update_player_upgrades(player: Player) -> None:
    """Update player's upgrades in the database"""
    players_collection.update_one(
        {"discord_id": player.discord_id},
        {
            "$set": {
                "upgrades": player.upgrades,
                "gold": player.gold
            }
        }
    )

def update_player_upgrade(player: Player, upgrade_type: str) -> bool:
    """
    Update a specific player upgrade
    Returns True if successful
    """
    if player.upgrade(upgrade_type):
        update_player_upgrades(player)
        return True
    return False
