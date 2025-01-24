from typing import Optional
from Game.Models.Guild import Guild
from Game.Database.database import Database

class GuildManager:
    def __init__(self, db_manager: Database):
        self.db_manager = db_manager
        self.collection_name = "guilds"

    async def create_guild(self, guild: Guild):
        await self.db_manager.insert_one(self.collection_name, guild.to_dict())

    async def get_guild(self, discord_server_id: str) -> Optional[Guild]:
        guild_data = await self.db_manager.find_one(self.collection_name, {"discord_server_id": discord_server_id})
        return Guild.from_dict(guild_data) if guild_data else None

    async def update_guild(self, guild: Guild):
        await self.db_manager.update_one(
            self.collection_name,
            {"discord_server_id": guild.discord_server_id},
            guild.to_dict()
        )

    async def delete_guild(self, discord_server_id: str):
        await self.db_manager.delete_one(self.collection_name, {"discord_server_id": discord_server_id})

    # Add more methods as needed, such as:
    async def add_member_to_guild(self, discord_server_id: str, member_id: str):
        guild = await self.get_guild(discord_server_id)
        if guild:
            guild.add_member(member_id)
            await self.update_guild(guild)

    async def add_join_request(self, discord_server_id: str, player_id: str):
        guild = await self.get_guild(discord_server_id)
        if guild:
            guild.add_join_request(player_id)
            await self.update_guild(guild)