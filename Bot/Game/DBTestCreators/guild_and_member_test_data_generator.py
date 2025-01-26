import random

from Game.Database.database import Database
from Game.Managers.guild_db_connection import add_member_to_guild
from Game.Models.Player import Player
from Game.Models.Guild import Guild
from datetime import datetime, timezone

db = Database()
players_collection = db.get_players_collection()
guilds_collection = db.get_guilds_collection()

def create_test_guilds():
    test_guilds = []
    for i in range(5):
        guild_id = f"guild{i+1}"
        guild_name = f"Test Guild {i+1}"
        test_guild = Guild(guild_id, guild_name)
        test_guilds.append(test_guild)
    return test_guilds

async def add_player(player: Player):
    players_collection.insert_one(player.to_dict())
    return

def create_test_players():
    test_players = []
    for _ in range(20):
        discord_id = str(random.randint(1, 1000000000000000000))
        username = f"TestPlayer{random.randint(1, 20)}"
        created_at = datetime.now(timezone.utc)
        last_active = datetime.now(timezone.utc)
        level = random.randint(1, 100)
        experience = random.randint(1, 1000000)
        gold = random.randint(1, 1000000)
        stats = {
            "strength": random.randint(1, 100),
            "agility": random.randint(1, 100),
            "intelligence": random.randint(1, 100),
            "vitality": random.randint(1, 100)
        }
        max_hp = random.randint(1, 1000)
        current_hp = random.randint(1, max_hp)
        equipment = {
            "Weapon": None,
            "Armor": None,
            "Helmet": None,
            "Accessory": None
        }
        inventory = []
        inventory_size = random.randint(1, 100)
        character_class = None
        current_party_id = None
        guild_id = None
        tower_level = random.randint(1, 100)

        test_player = Player(discord_id, username, created_at, last_active, level, experience, gold, stats, max_hp, current_hp, equipment, inventory, inventory_size, character_class, current_party_id, guild_id, tower_level)
        test_players.append(test_player)

    return test_players

def add_test_players_to_guilds(test_players, test_guilds):
    for i, player in enumerate(test_players):
        guild_index = i % len(test_guilds)
        add_member_to_guild(test_guilds[guild_index].id, player.discord_id)

async def add_test_players():
    test_players = create_test_players()
    test_guilds = create_test_guilds()

    for guild in test_guilds:
        guilds_collection.insert_one(guild.to_dict())

    for player in test_players:
        await add_player(player)

    add_test_players_to_guilds(test_players, test_guilds)
    

if __name__ == "__main__":
    import asyncio
    asyncio.run(add_test_players())