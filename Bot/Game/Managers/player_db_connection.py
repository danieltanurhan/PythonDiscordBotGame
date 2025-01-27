from Game.Database.database import Database
from Game.Models.Player import Player
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

    print(new_player.to_dict())
    
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
