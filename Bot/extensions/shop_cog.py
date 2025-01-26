import interactions
from interactions import slash_command, SlashContext, Embed, ButtonStyle, ActionRow, Button
from interactions import spread_to_rows

from discord import app_commands
import discord

from config import DEV_GUILD
# from bot_support import Pagination
from interactions.ext.paginators import Paginator
from Game.Managers.equipment_db_connection import get_equipment_by_type
# Other necessary imports

class ShopCog(interactions.Extension):

    def __init__(self, bot):
        self.bot = bot

    @interactions.slash_command(
        "shop", description="Open the game shop"
    )
    async def shop_command(self, ctx: SlashContext):
        await self._display_shop(ctx)

    @interactions.component_callback("shop_button")
    async def shop_button_callback(self, ctx: interactions.ComponentContext):
        await self._display_shop(ctx)

    async def _display_shop(self, ctx: interactions.contexts):
        buttons = [
            interactions.Button(style=ButtonStyle.PRIMARY, label="Weapons", custom_id="shop_weapons"),
            interactions.Button(style=ButtonStyle.PRIMARY, label="Armor", custom_id="shop_armor"),
        ]

        embed = Embed(
            title="Select a category to browse items",
            description="/shop weapons",
            color=0x00ff00
        )
        

        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed, components=buttons)

    @interactions.subcommand(description="View weapons in the shop", base="shop")
    async def weapons(self, ctx: SlashContext):
        await self.display_weapons_shop(ctx)

    @interactions.component_callback("shop_weapons")
    async def shop_weapons_callback(self, ctx: interactions.ComponentContext):
        await self.display_weapons_shop(ctx)
        
    async def display_weapons_shop(self, ctx: interactions.ComponentContext):
        weapons = get_equipment_by_type("Weapon")
        
        embeds = []
        for i in range(0, len(weapons), 2):  # 5 weapons per page
            embed = Embed(title="Weapons Shop", color=0x00ff00)
            for weapon in weapons[i:i+2]:
                stats_str = "\n".join([f"{stat}: {value}" for stat, value in weapon['stats'].items()])
                value = f"Price: {weapon['price']}\nLevel: {weapon['level']}\nStats:\n{stats_str}"
                embed.add_field(name=weapon['name'], value=value, inline=False)
            embeds.append(embed)
        
        paginator = Paginator.create_from_embeds(self.bot, *embeds)
        await paginator.send(ctx)

    # @interactions.slash_command("shop")
    @interactions.subcommand(description="View armor in the shop", base="shop")
    async def armor(self, ctx: SlashContext):
        await self.display_armor_shop(ctx)
    
    @interactions.component_callback("shop_armor")
    async def shop_armor_callback(self, ctx: interactions.ComponentContext):
        await self.display_armor_shop(ctx)
        
    async def display_armor_shop(self, ctx: interactions.ComponentContext):
        armor = get_equipment_by_type("Armor")

        back_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Back", custom_id="shop_button")
        buy_first_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Buy First Upgrade", custom_id="buy_first_armor")
        embeds = []
        for i in range(0, len(armor), 3):  # 5 armor per page
            embed = Embed(title="Armor Shop", color=0x00ff00)
            for armor_item in armor[i:i+3]:
                stats_str = "\n".join([f"{stat}: {value}" for stat, value in armor_item['stats'].items()])
                value = f"Price: {armor_item['price']}\nLevel: {armor_item['level']}\nStats:\n{stats_str}"
                embed.add_field(name=armor_item['name'], value=value, inline=False)
            embeds.append(embed)
        
        paginator = Paginator.create_from_embeds(self.bot, *embeds)
        paginator.show_first_button = False
        paginator.show_last_button = False

        comp = paginator.to_dict()["components"]
        embeds = paginator.to_dict()["embeds"]

        # components = [
        #     interactions.ActionRow(back_button, buy_first_button).to_dict(),
        #     comp  # Pagination buttons
        # ]
        spread_to_rows(back_button, buy_first_button)
        components: list[ActionRow] = [
            ActionRow(
                back_button,
                buy_first_button
            ), comp
        ]

        await ctx.send(embeds=embeds, components=components)
        
        # await ctx.send(paginator.pages, components=all_components)
        # await paginator.send(ctx)