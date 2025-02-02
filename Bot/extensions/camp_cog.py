import interactions
from interactions import slash_command, SlashContext, Embed, ButtonStyle
from typing import Optional

from config import DEV_GUILD
from Game.Managers.player_db_connection import get_player_by_discord_id
from Game.Managers.loot_db_connection import get_loot_by_id, get_loot_price

class CampCog(interactions.Extension):
    def __init__(self, bot):
        self.bot = bot

    def _create_camp_display(self, ctx: interactions.contexts):
        """Create the display for camp"""
        discord_id = str(ctx.author.id)
        player = get_player_by_discord_id(discord_id)

        if not player:
            return None, "You need to create a character first. Use the `/start` command to begin your adventure!"

        player_data = player.to_dict()

        # Calculate XP to next level
        base_xp = 100
        level_multiplier = 1.5
        current_level_xp = int(((player.level) ** level_multiplier) * base_xp)
        next_level_xp = int(((player.level + 1) ** level_multiplier) * base_xp)


        # Combine clan, balance, level, and tower info into one field
        clan_name = player_data.get('guild_id', 'None')
        combined_info = (
            f"❤️ HP: **{player_data['current_hp']}/{player_data['max_hp']}** "
            f" 🛡️ Class: **{player_data['character_class']}**\n"
            f"Clan: **{clan_name}**\n"
            f"Balance: **${player_data['gold']:,}**\n"
            f"Level **{player_data['level']}**, **{player_data['experience']:,}**/**{next_level_xp:,}** XP to next level\n"
            f"Current Tower Level: 🗼 **{player_data['tower_level']}**"
        )

        # Create embed
        embed = Embed(title=f"Inventory", color=0x00ff00, description=combined_info)

        equipments = player_data['equipment']
        emoji_eq = {
            "weapon": "⚔️",
            "armor": "🛡️",
            "helmet": "🪖",
            "accessory": "💍"
        }

        equipment_str = ""
        for slot, item in equipments.items():
            if item:
                emoji = emoji_eq.get(slot.lower(), '')
                name = item.get('name', 'None')
                level = item.get('level', 0)
                level_str = f"(Lvl {level})" if level > 0 else ""
                equipment_str += f"{emoji} {slot.capitalize()}: {name} {level_str}\n"
            else:
                equipment_str += f"{emoji_eq.get(slot.lower(), '')} {slot.capitalize()}: None\n"

        equipment_str = equipment_str.rstrip()
        if not equipment_str:
            equipment_str = "No equipment"

        embed.add_field(name="Equipment", value=equipment_str, inline=False)

        # Loot section
        total_value = 0
        if not player_data['loot_inventory']:
            embed.add_field(
                name="Loot",
                value="You don't have any loot! Get some with /raid!",
                inline=False
            )
        else:
            loot_str = ""
            for loot_id, quantity in player_data['loot_inventory'].items():
                loot_data = get_loot_by_id(loot_id)
                if loot_data:
                    name = loot_data['name']
                    price = get_loot_price(loot_id)
                    total_value += price * quantity
                    loot_str += f"🎁 {name} x{quantity}\n"
            loot_str += f"\nLoot Value: **${total_value:,}**"
            embed.add_field(name="Loot", value=loot_str, inline=False)

        embed.set_author(name=ctx.author.display_name + "'s camp", icon_url=ctx.author.avatar_url)

        buttons = [
            interactions.Button(style=ButtonStyle.PRIMARY, label="Raid", custom_id="raid_again"),
            interactions.Button(style=ButtonStyle.PRIMARY, label="Sell", custom_id="sell_button"),
            interactions.Button(style=ButtonStyle.PRIMARY, label="Shop", custom_id="shop_button"),
            interactions.Button(style=ButtonStyle.SECONDARY, label="Profile", custom_id="go_profile")
        ]

        return embed, buttons

    @interactions.slash_command(
        "camp", description="Go back to camp", scopes=[DEV_GUILD] if DEV_GUILD else None
    )
    async def go_camp(self, ctx: SlashContext):
        embed, buttons = self._create_camp_display(ctx)
        if embed:
            await ctx.send(embed=embed, components=buttons)
        else:
            await ctx.send(buttons)  # In this case, buttons contains error message
    
    @interactions.component_callback("go_camp")
    async def go_camp_callback(self, ctx: interactions.ComponentContext):
        embed, buttons = self._create_camp_display(ctx)
        if embed:
            await ctx.edit_origin(embed=embed, components=buttons)
        else:
            await ctx.edit_origin(content=buttons)
