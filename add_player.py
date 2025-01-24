# add_player.py
from Game.Database.database import Database
from Game.Models.Player import Player

def add_player(discord_id: str, username: str):
    """
    Register a new player in the database
    
    Args:
        discord_id (str): Unique Discord user ID
        username (str): Player's username
    
    Returns:
        Player: Newly created player object
    """
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

def main():
    # Example usage
    discord_id = input("Enter Discord ID: ")
    username = input("Enter Username: ")
    
    player = add_player(0000000, 'dancando')
    
    if player:
        print(f"Player {player.username} registered successfully!")
    else:
        print("Player already exists.")

if __name__ == "__main__":
    main()