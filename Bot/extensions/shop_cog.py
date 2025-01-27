from asyncio import Timeout
import asyncio
import interactions
from interactions import slash_command, SlashContext, Embed, ButtonStyle, ActionRow, Button
from interactions import spread_to_rows

from discord import app_commands
import discord

from config import DEV_GUILD
# from bot_support import Pagination
from interactions.ext.paginators import Page, Paginator
from Game.Managers.equipment_db_connection import get_equipment_by_type
# Other necessary imports
back_button = interactions.Button(style=ButtonStyle.SECONDARY, label="Back", custom_id="shop_button")
wu1_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Buy First Upgrade", custom_id="weapon_upgrade_1")
wu2_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Buy Second Upgrade", custom_id="weapon_upgrade_2")
wu3_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Buy Third Upgrade", custom_id="weapon_upgrade_3")
wu4_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Buy Fourth Upgrade", custom_id="weapon_upgrade_4")

wu_buttons = [wu1_button, wu2_button, wu3_button, wu4_button]

au1_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Buy First Upgrade", custom_id="armor_upgrade_1")
au2_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Buy Second Upgrade", custom_id="armor_upgrade_2")
au3_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Buy Third Upgrade", custom_id="armor_upgrade_3")
au4_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Buy Fourth Upgrade", custom_id="armor_upgrade_4")

au_buttons = [au1_button, au2_button, au3_button, au4_button]


class CustomPaginator(Paginator):
    # custom_buttons = None
    def __init__(self, *args, custom_buttons = [], **kwargs):
        super().__init__(*args , **kwargs)
        # self.custom_buttons
        self.custom_buttons = custom_buttons if custom_buttons is not None else []

    def to_dict(self):
        paginator_dict = super().to_dict()
        if self.custom_buttons and paginator_dict["components"]:
            if self.page_index == 0:
                custom_row = self.custom_buttons[self.page_index+1]
                paginator_dict["components"].append(custom_row.to_dict())

            elif self.page_index == 1:
                custom_row = self.custom_buttons[self.page_index+1]
                paginator_dict["components"].append(custom_row.to_dict())

            # Visible on all paginated pages            
            custom_row = self.custom_buttons[0]
            paginator_dict["components"].append(custom_row.to_dict())
        return paginator_dict
    
class ShopCog(interactions.Extension):


    def __init__(self, bot):
        self.bot = bot
        self.current_paginator = None

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
        
        #make function to check player level in db
        player_level = 3

        sorted_weapons = sorted(weapons, key=lambda x: x['level'])
        embeds = []
        for i in range(0, len(sorted_weapons), 3):  # 3 armor items per page
            embed = Embed(title="Weapons Shop", color=0x00ff00)
            
            for weapons_item in sorted_weapons[i:i+3]: 
                name = weapons_item['name']
                level_req = f"(Lvl {weapons_item['level']})" if weapons_item['level'] > player_level else ""
                price = f"{weapons_item['price']} gold"
                description = weapons_item.get('description', 'No description available.')
                
                # Combine top and bottom parts for each item
                item_info = f"{name} {level_req} | {price}\n{description}"
                
                embed.add_field(name="\u200b", value=item_info, inline=False)
            
            embeds.append(embed)


        paginator = CustomPaginator.create_from_embeds(self.bot, *embeds)
        paginator.custom_buttons = [
            interactions.ActionRow(
                    back_button
                ), 
                interactions.ActionRow(
                    wu1_button, wu2_button, wu3_button
                ), 
                interactions.ActionRow(
                    wu4_button
                )
            ]
        paginator.show_first_button = False
        paginator.show_last_button = False

        self.current_paginator = paginator
        
        await ctx.send(**paginator.to_dict())
        paginator._author_id = ctx.author.id

    # @interactions.slash_command("shop")
    @interactions.subcommand(description="View armor in the shop", base="shop")
    async def armor(self, ctx: SlashContext):
        await self.display_armor_shop(ctx)

    @interactions.component_callback("shop_armor")
    async def shop_armor_callback(self, ctx: interactions.ComponentContext):
        await self.display_armor_shop(ctx)
        
    async def display_armor_shop(self, ctx: interactions.ComponentContext):
        armor = get_equipment_by_type("Armor")

        #make function to check player level in db
        player_level = 3

        sorted_armor = sorted(armor, key=lambda x: x['level'])
        embeds = []
        for i in range(0, len(sorted_armor), 3):  # 3 armor items per page
            embed = Embed(title="Armor Shop", color=0x00ff00)
            
            for armor_item in sorted_armor[i:i+3]:
                name = armor_item['name']
                level_req = f"(Lvl {armor_item['level']})" if armor_item['level'] > player_level else ""
                price = f"{armor_item['price']} gold"
                description = armor_item.get('description', 'No description available.')
                
                # Combine top and bottom parts for each item
                item_info = f"{name} {level_req} | {price}\n{description}"
                
                embed.add_field(name="\u200b", value=item_info, inline=False)
            
            embeds.append(embed)


        paginator = CustomPaginator.create_from_embeds(self.bot, *embeds)
        paginator.custom_buttons = [
            interactions.ActionRow(
                    back_button
                ), 
                interactions.ActionRow(
                    au1_button, au2_button, au3_button
                ), 
                interactions.ActionRow(
                    au4_button
                )
            ]
        paginator.show_first_button = False
        paginator.show_last_button = False

        self.current_paginator = paginator
        
        await ctx.send(**paginator.to_dict())
        paginator._author_id = ctx.author.id

    def update_button_state(self, buttons):
        for button in buttons:
            if button.disabled:
                button.disabled = False
                button.style = ButtonStyle.PRIMARY
        
        
    
    @interactions.component_callback("weapon_upgrade_1")
    async def weapon_upgrade_1_callback(self, ctx: interactions.ComponentContext):
        self.update_button_state(wu_buttons)
        wu1_button.disabled = True
        wu1_button.style = ButtonStyle.SUCCESS
        
        if self.current_paginator:
            paginator_dict = self.current_paginator.to_dict()
            await ctx.edit_origin(**paginator_dict)
    
    
    @interactions.component_callback("weapon_upgrade_2")
    async def weapon_upgrade_2_callback(self, ctx: interactions.ComponentContext):
        self.update_button_state(wu_buttons)
        wu2_button.disabled = True
        wu2_button.style = ButtonStyle.SUCCESS

        if self.current_paginator:
            paginator_dict = self.current_paginator.to_dict()
            await ctx.edit_origin(**paginator_dict)
    
    @interactions.component_callback("weapon_upgrade_3")
    async def weapon_upgrade_3_callback(self, ctx: interactions.ComponentContext):
        self.update_button_state(wu_buttons)
        wu3_button.disabled = True
        wu3_button.style = ButtonStyle.SUCCESS

        if self.current_paginator:
            paginator_dict = self.current_paginator.to_dict()
            await ctx.edit_origin(**paginator_dict)
    
    @interactions.component_callback("weapon_upgrade_4")
    async def weapon_upgrade_4_callback(self, ctx: interactions.ComponentContext):
        self.update_button_state(wu_buttons)
        wu4_button.disabled = True
        wu4_button.style = ButtonStyle.SUCCESS

        if self.current_paginator:
            paginator_dict = self.current_paginator.to_dict()
            await ctx.edit_origin(**paginator_dict)

    @interactions.component_callback("armor_upgrade_1")
    async def armor_upgrade_1_callback(self, ctx: interactions.ComponentContext):
        self.update_button_state(au_buttons)
        au1_button.disabled = True
        au1_button.style = ButtonStyle.SUCCESS

        if self.current_paginator:
            paginator_dict = self.current_paginator.to_dict()
            await ctx.edit_origin(**paginator_dict)
    
    @interactions.component_callback("armor_upgrade_2")
    async def armor_upgrade_2_callback(self, ctx: interactions.ComponentContext):
        self.update_button_state(au_buttons)
        au2_button.disabled = True
        au2_button.style = ButtonStyle.SUCCESS

        if self.current_paginator:
            paginator_dict = self.current_paginator.to_dict()
            await ctx.edit_origin(**paginator_dict)
        
    @interactions.component_callback("armor_upgrade_3")
    async def armor_upgrade_3_callback(self, ctx: interactions.ComponentContext):
        self.update_button_state(au_buttons)
        au3_button.disabled = True
        au3_button.style = ButtonStyle.SUCCESS

        if self.current_paginator:
            paginator_dict = self.current_paginator.to_dict()
            await ctx.edit_origin(**paginator_dict)
        
    @interactions.component_callback("armor_upgrade_4")
    async def armor_upgrade_4_callback(self, ctx: interactions.ComponentContext):
        self.update_button_state(au_buttons)
        au4_button.disabled = True
        au4_button.style = ButtonStyle.SUCCESS

        if self.current_paginator:
            paginator_dict = self.current_paginator.to_dict()
            await ctx.edit_origin(**paginator_dict)