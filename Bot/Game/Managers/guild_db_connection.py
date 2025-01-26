from typing import Optional
from Game.Models.Guild import Guild
from Game.Database.database import Database

db = Database()
guilds_collection = db.get_guilds_collection()

def create_guild(guild: Guild):
    guilds_collection.insert_one(guild.to_dict())

def get_guild(id: str) -> Optional[Guild]:
    guild_data = guilds_collection.find_one({"id": id})
    return Guild.from_dict(guild_data) if guild_data else None

def update_guild(guild: Guild):

    guilds_collection.update_one(
        {"id": guild.id},
        {"$set": {
            "name": guild.name,
            "created_at": guild.created_at,
            "description": guild.description,
            "leader_id": guild.leader_id,
            "members": guild.members,
            "join_requests": guild.join_requests
        }}
    )

def delete_guild(id: str):
    guilds_collection.delete_one({"id": id})

def add_member_to_guild(id: str, member_id: str):
    guild = get_guild(id)
    if guild:
        guild.add_member(member_id)
        update_guild(guild)

def add_join_request(id: str, player_id: str):
    guild = get_guild(id)
    if guild:
        guild.add_join_request(player_id)
        update_guild(guild)

