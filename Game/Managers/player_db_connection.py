from Game.Database.database import Database
from Game.Models.Player import Player
import pymongo
import random

db = Database()
players_collection = db.get_players_collection()

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

def update_player_rewards(player: Player, gold: int, experience: int) -> dict:
    player.gold += gold
    player.experience += experience
    
    base_xp = 100
    level_multiplier = 1.5
    new_level = int((player.experience / base_xp) ** (1 / level_multiplier)) + 1
    
    update_result = {
        "gold_gained": gold,
        "experience_gained": experience,
        "leveled_up": new_level > player.level
    }
    
    if update_result["leveled_up"]:
        player.level = new_level
        update_result["new_level"] = new_level
    
    players_collection.update_one(
        {"discord_id": player.discord_id}, 
        {"$set": {
            "current_hp": player.current_hp,
            "gold": player.gold,
            "experience": player.experience,
            "level": player.level
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
    
    # Drop equipped items
    for slot, item in player.equipment.items():
        if item and random.random() < 0.3:
            death_summary["dropped_items"].append({
                "slot": slot,
                "item": item
            })
            player.equipment[slot] = None
    
    # Calculate gold loss
    gold_loss = int(player.gold * 0.2)
    player.gold -= gold_loss
    death_summary["gold_lost"] = gold_loss
    
    # Reset player state
    player.current_hp = int(player.max_hp * 0.1)  # 10% HP
    death_summary["hp_restored"] = player.current_hp
    player.current_party_id = None
    
    # Update database with new player state
    players_collection.update_one(
        {"discord_id": player.discord_id},
        {"$set": {
            "current_hp": player.current_hp,
            "gold": player.gold,
            "equipment": player.equipment,
            "current_party_id": player.current_party_id
        }}
    )
    
    return death_summary