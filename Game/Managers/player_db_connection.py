from Game.Database.database import Database
from Game.Models.Player import Player
import pymongo

# Connect to MongoDB
db = Database()
players_collection = db.get_players_collection()

def get_player_by_discord_id(discord_id: str) -> Player:
    player_data = players_collection.find_one({"discord_id": discord_id})
    return Player.from_dict(player_data)
