"""
This file provides a template for future commands.
This file will not be loaded as a cog or module
"""
import os

import interactions
from interactions import slash_command, SlashContext, Embed

from config import DEV_GUILD

"Highly recommended - we suggest providing proper debug logging"
from src import logutil
import random

"Change this if you'd like - this labels log messages for debug mode"
logger = logutil.init_logger(os.path.basename(__file__))


class TemplateCog(interactions.Extension):
    @interactions.slash_command(
        "profile", description="profile command", scopes=[DEV_GUILD] if DEV_GUILD else None
    )
    async def profile_cmd(self, ctx: interactions.SlashContext):
        """Show the player's profile in a Discord embed"""
        # Example data to populate the Player class (replace with actual database retrieval if necessary)
        discord_id = str(ctx.author.id)
        username = ctx.author.username

        # Instantiate the player (this would typically be retrieved from a database)
        player = username
        player = {
            "username": username,
            "level": "15",
            "experience": "2850",
            "gold": "7243",
            "stats": {
            "strength": 25,
            "agility": 20,
            "intelligence": 18,
            "vitality": 30
            },
            "max_hp": 300,
            "current_hp": 220,
            "character_class": "Warrior",
            "equipment": {
            "weapon": "Iron Sword",
            "armor": "Leather Armor",
            "helmet": "Iron Helmet",
            "accessory": "Silver Ring"
            },
            "inventory": [
            "Healing Potion",
            "Mana Potion",
            "Steel Dagger",
            "Magic Scroll",
            "Rainbow Gem",
            "Fire Bomb",
            "Thunder Orb"
            ]
        }

        # Create the embed for the profile
        embed = Embed(
            title=f"Profile of {player['username']}",
            color=0x1E90FF
        )
        embed.add_field(name="Clan", value="Lone Wolf", inline=False)
        embed.add_field(name="Balance", value=f"\ud83d\udcb0 {player['gold']} Gold", inline=True)
        embed.add_field(name="Level", value=f"\ud83c\udf96\ufe0f {player['level']}", inline=True)
        embed.add_field(
            name="XP",
            value=f"\ud83c\udf1f {player['experience']}/{(int(player['level']) + 1) * 200}",  # Example XP threshold logic
            inline=True
        )
        embed.add_field(name="Current HP", value=f"\u2764\ufe0f {player['current_hp']}/{player['max_hp']}", inline=True)
        embed.add_field(name="Character Class", value=f"\ud83d\udde8\ufe0f {player['character_class']}", inline=True)
        embed.add_field(name="Stats", value=(
            f"**\ud83d\udcaa Strength**: {player['stats']['strength']}\n"
            f"**\ud83c\udfca Agility**: {player['stats']['agility']}\n"
            f"**\ud83e\uddec Intelligence**: {player['stats']['intelligence']}\n"
            f"**\ud83e\uddd1 Vitality**: {player['stats']['vitality']}"
        ), inline=False)

        # Equipment
        embed.add_field(name="Equipment", value=(
            f"**Weapon**: {player['equipment']['weapon']}\n"
            f"**Armor**: {player['equipment']['armor']}\n"
            f"**Helmet**: {player['equipment']['helmet']}\n"
            f"**Accessory**: {player['equipment']['accessory']}"
        ), inline=False)

        # Inventory
        inventory_text = "\n".join(player['inventory'])
        embed.add_field(name="Inventory", value=inventory_text if inventory_text else "\ud83d\udcdd Empty", inline=False)

        # Send the embed
        await ctx.send(embed=embed)

