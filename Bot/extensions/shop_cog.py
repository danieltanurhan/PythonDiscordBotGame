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
from Game.Managers.equipment_db_connection import get_equipment_by_type, get_equipment_by_id
from Game.Managers.player_db_connection import get_player_by_discord_id, update_player_purchase, update_player_equipment

# Other necessary imports
back_button = interactions.Button(style=ButtonStyle.SECONDARY, label="Back", custom_id="shop_button")
return_button = interactions.Button(style=ButtonStyle.SECONDARY, label="Return", custom_id="go_profile")

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

hu1_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Buy First Upgrade", custom_id="helmet_upgrade_1")
hu2_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Buy Second Upgrade", custom_id="helmet_upgrade_2")
hu3_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Buy Third Upgrade", custom_id="helmet_upgrade_3")
hu4_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Buy Fourth Upgrade", custom_id="helmet_upgrade_4")

hu_buttons = [hu1_button, hu2_button, hu3_button, hu4_button]

acc1_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Buy First Upgrade", custom_id="accessory_upgrade_1")
acc2_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Buy Second Upgrade", custom_id="accessory_upgrade_2")
acc3_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Buy Third Upgrade", custom_id="accessory_upgrade_3")
acc4_button = interactions.Button(style=ButtonStyle.PRIMARY, label="Buy Fourth Upgrade", custom_id="accessory_upgrade_4")

acc_buttons = [acc1_button, acc2_button, acc3_button, acc4_button]


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
            interactions.Button(style=ButtonStyle.PRIMARY, label="Helmets", custom_id="shop_helmets"),
            interactions.Button(style=ButtonStyle.PRIMARY, label="Accessories", custom_id="shop_accessories")
        ]

        component = [
            interactions.ActionRow(buttons[0], buttons[1], buttons[2], buttons[3]),
            interactions.ActionRow(return_button)
            ]


        embed = Embed(
            title="Select a category to browse items",
            description="/shop weapons",
            color=0x00ff00
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed, components=component)

    @interactions.subcommand(description="View weapons in the shop", base="shop")
    async def weapons(self, ctx: SlashContext):
        await self.display_weapons_shop(ctx)

    @interactions.component_callback("shop_weapons")
    async def shop_weapons_callback(self, ctx: interactions.ComponentContext):
        await self.display_weapons_shop(ctx)
        
    async def display_weapons_shop(self, ctx: interactions.ComponentContext):
        weapons = get_equipment_by_type("Weapon")
        player = get_player_by_discord_id(str(ctx.author.id))
        
        sorted_weapons = sorted(weapons, key=lambda x: x['level'])
        embeds = []
        for i in range(0, len(sorted_weapons), 3):
            embed = Embed(title="Weapons Shop", color=0x00ff00)
            
            for weapon in sorted_weapons[i:i+3]:
                is_equipped = player.has_equipped(weapon['id'])
                is_owned = player.has_equipment(weapon['id'])
                can_afford = player.can_afford(weapon['price'])
                meets_level = player.can_equip(weapon['level'])
                
                name = weapon['name']
                description = weapon.get('description', 'No description available.')
                
                if is_equipped:
                    item_info = f"{name} - EQUIPPED\n{description}"
                elif is_owned:
                    item_info = f"{name} - OWNED\n{description}"
                else:
                    level_req = f"(Lvl {weapon['level']})"
                    price = f"{weapon['price']} gold"
                    requirements = []
                    if not meets_level:
                        requirements.append("🔒 Level too low")
                    if not can_afford:
                        requirements.append("❌ Cannot afford")
                    req_text = " - " + ", ".join(requirements) if requirements else ""
                    item_info = f"{name} {level_req} | {price}\n{description}{req_text}"
                
                embed.add_field(name="\u200b", value=item_info, inline=False)
            
            embeds.append(embed)

        # Update button states based on first page items
        for i, weapon in enumerate(sorted_weapons[:4]):
            button = wu_buttons[i]
            is_equipped = player.has_equipped(weapon['id'])
            is_owned = player.has_equipment(weapon['id'])
            can_afford = player.can_afford(weapon['price'])
            meets_level = player.can_equip(weapon['level'])
            
            button.disabled = is_equipped or (not is_owned and (not can_afford or not meets_level))
            if is_equipped:
                button.style = ButtonStyle.SUCCESS
                button.label = "Equipped"
            elif is_owned:
                button.style = ButtonStyle.SUCCESS
                button.label = "Equip"
            else:
                button.style = ButtonStyle.PRIMARY
                button.label = f"${weapon['price']}"

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
        player = get_player_by_discord_id(str(ctx.author.id))
        
        sorted_armor = sorted(armor, key=lambda x: x['level'])
        embeds = []
        for i in range(0, len(sorted_armor), 3):
            embed = Embed(title="Armor Shop", color=0x00ff00)
            
            for armor_item in sorted_armor[i:i+3]:
                is_equipped = player.has_equipped(armor_item['id'])
                is_owned = player.has_equipment(armor_item['id'])
                can_afford = player.can_afford(armor_item['price'])
                meets_level = player.can_equip(armor_item['level'])
                
                name = armor_item['name']
                description = armor_item.get('description', 'No description available.')
                
                if is_equipped:
                    item_info = f"{name} - EQUIPPED\n{description}"
                elif is_owned:
                    item_info = f"{name} - OWNED\n{description}"
                else:
                    level_req = f"(Lvl {armor_item['level']})"
                    price = f"{armor_item['price']} gold"
                    requirements = []
                    if not meets_level:
                        requirements.append("🔒 Level too low")
                    if not can_afford:
                        requirements.append("❌ Cannot afford")
                    req_text = " - " + ", ".join(requirements) if requirements else ""
                    item_info = f"{name} {level_req} | {price}\n{description}{req_text}"
                
                embed.add_field(name="\u200b", value=item_info, inline=False)
            
            embeds.append(embed)

        # Update button states for armor buttons
        for i, armor_item in enumerate(sorted_armor[:4]):
            button = au_buttons[i]
            is_equipped = player.has_equipped(armor_item['id'])
            is_owned = player.has_equipment(armor_item['id'])
            can_afford = player.can_afford(armor_item['price'])
            meets_level = player.can_equip(armor_item['level'])
            
            button.disabled = is_equipped or (not is_owned and (not can_afford or not meets_level))
            if is_equipped:
                button.style = ButtonStyle.SUCCESS
                button.label = "Equipped"
            elif is_owned:
                button.style = ButtonStyle.SUCCESS
                button.label = "Equip"
            else:
                button.style = ButtonStyle.PRIMARY
                button.label = f"${armor_item['price']}"

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

    @interactions.subcommand(description="View helmets in the shop", base="shop")
    async def helmets(self, ctx: SlashContext):
        await self.display_helmets_shop(ctx)

    @interactions.component_callback("shop_helmets")
    async def shop_helmets_callback(self, ctx: interactions.ComponentContext):
        await self.display_helmets_shop(ctx)

    async def display_helmets_shop(self, ctx: interactions.ComponentContext):
        helmets = get_equipment_by_type("Helmet")
        player = get_player_by_discord_id(str(ctx.author.id))
        
        sorted_helmets = sorted(helmets, key=lambda x: x['level'])
        embeds = []
        for i in range(0, len(sorted_helmets), 3):
            embed = Embed(title="Helmets Shop", color=0x00ff00)
            
            for helmet in sorted_helmets[i:i+3]:
                is_equipped = player.has_equipped(helmet['id'])
                is_owned = player.has_equipment(helmet['id'])
                can_afford = player.can_afford(helmet['price'])
                meets_level = player.can_equip(helmet['level'])
                
                name = helmet['name']
                description = helmet.get('description', 'No description available.')
                
                if is_equipped:
                    item_info = f"{name} - EQUIPPED\n{description}"
                elif is_owned:
                    item_info = f"{name} - OWNED\n{description}"
                else:
                    level_req = f"(Lvl {helmet['level']})"
                    price = f"{helmet['price']} gold"
                    requirements = []
                    if not meets_level:
                        requirements.append("🔒 Level too low")
                    if not can_afford:
                        requirements.append("❌ Cannot afford")
                    req_text = " - " + ", ".join(requirements) if requirements else ""
                    item_info = f"{name} {level_req} | {price}\n{description}{req_text}"
                
                embed.add_field(name="\u200b", value=item_info, inline=False)
            
            embeds.append(embed)

        # Update button states based on first page items
        for i, helmet in enumerate(sorted_helmets[:4]):
            button = hu_buttons[i]
            is_equipped = player.has_equipped(helmet['id'])
            is_owned = player.has_equipment(helmet['id'])
            can_afford = player.can_afford(helmet['price'])
            meets_level = player.can_equip(helmet['level'])
            
            button.disabled = is_equipped or (not is_owned and (not can_afford or not meets_level))
            if is_equipped:
                button.style = ButtonStyle.SUCCESS
                button.label = "Equipped"
            elif is_owned:
                button.style = ButtonStyle.SUCCESS
                button.label = "Equip"
            else:
                button.style = ButtonStyle.PRIMARY
                button.label = f"${helmet['price']}"

        paginator = CustomPaginator.create_from_embeds(self.bot, *embeds)
        paginator.custom_buttons = [
            interactions.ActionRow(
                    back_button
                ), 
                interactions.ActionRow(
                    hu1_button, hu2_button, hu3_button
                ), 
                interactions.ActionRow(
                    hu4_button
                )
            ]
        paginator.show_first_button = False
        paginator.show_last_button = False

        self.current_paginator = paginator
        
        await ctx.send(**paginator.to_dict())
        paginator._author_id = ctx.author.id

    @interactions.subcommand(description="View accessories in the shop", base="shop")
    async def accessories(self, ctx: SlashContext):
        await self.display_accessories_shop(ctx)

    @interactions.component_callback("shop_accessories")
    async def shop_accessories_callback(self, ctx: interactions.ComponentContext):
        await self.display_accessories_shop(ctx)

    async def display_accessories_shop(self, ctx: interactions.ComponentContext):
        accessories = get_equipment_by_type("Accessory")
        player = get_player_by_discord_id(str(ctx.author.id))
        
        sorted_accessories = sorted(accessories, key=lambda x: x['level'])
        embeds = []
        for i in range(0, len(sorted_accessories), 3):
            embed = Embed(title="Accessories Shop", color=0x00ff00)
            
            for accessory in sorted_accessories[i:i+3]:
                is_equipped = player.has_equipped(accessory['id'])
                is_owned = player.has_equipment(accessory['id'])
                can_afford = player.can_afford(accessory['price'])
                meets_level = player.can_equip(accessory['level'])
                
                name = accessory['name']
                description = accessory.get('description', 'No description available.')
                
                if is_equipped:
                    item_info = f"{name} - EQUIPPED\n{description}"
                elif is_owned:
                    item_info = f"{name} - OWNED\n{description}"
                else:
                    level_req = f"(Lvl {accessory['level']})"
                    price = f"{accessory['price']} gold"
                    requirements = []
                    if not meets_level:
                        requirements.append("🔒 Level too low")
                    if not can_afford:
                        requirements.append("❌ Cannot afford")
                    req_text = " - " + ", ".join(requirements) if requirements else ""
                    item_info = f"{name} {level_req} | {price}\n{description}{req_text}"
                
                embed.add_field(name="\u200b", value=item_info, inline=False)
            
            embeds.append(embed)

        # Update button states based on first page items
        for i, accessory in enumerate(sorted_accessories[:4]):
            button = acc_buttons[i]
            is_equipped = player.has_equipped(accessory['id'])
            is_owned = player.has_equipment(accessory['id'])
            can_afford = player.can_afford(accessory['price'])
            meets_level = player.can_equip(accessory['level'])
            
            button.disabled = is_equipped or (not is_owned and (not can_afford or not meets_level))
            if is_equipped:
                button.style = ButtonStyle.SUCCESS
                button.label = "Equipped"
            elif is_owned:
                button.style = ButtonStyle.SUCCESS
                button.label = "Equip"
            else:
                button.style = ButtonStyle.PRIMARY
                button.label = f"${accessory['price']}"

        paginator = CustomPaginator.create_from_embeds(self.bot, *embeds)
        paginator.custom_buttons = [
            interactions.ActionRow(
                    back_button
                ), 
                interactions.ActionRow(
                    acc1_button, acc2_button, acc3_button
                ), 
                interactions.ActionRow(
                    acc4_button
                )
            ]
        paginator.show_first_button = False
        paginator.show_last_button = False

        self.current_paginator = paginator
        
        await ctx.send(**paginator.to_dict())
        paginator._author_id = ctx.author.id

    @interactions.component_callback("weapon_upgrade_1")
    async def weapon_upgrade_1_callback(self, ctx: interactions.ComponentContext):
        player = get_player_by_discord_id(str(ctx.author.id))
        weapons = get_equipment_by_type("Weapon")
        weapon = sorted(weapons, key=lambda x: x['level'])[0]

        if player.has_equipment(weapon['id']):
            # Equip the owned weapon
            update_player_equipment(player, weapon['id'], "Weapon")
            await ctx.send(f"Successfully equipped {weapon['name']}!")
        else:
            # Purchase and equip the weapon
            if update_player_purchase(player, weapon['id'], weapon['price'], "Weapon"):
                await ctx.send(f"Successfully purchased and equipped {weapon['name']}!")
            else:
                await ctx.send("Purchase failed! Check your gold and requirements.")

        # Refresh the shop display
        await self.display_weapons_shop(ctx)

    @interactions.component_callback("weapon_upgrade_2")
    async def weapon_upgrade_2_callback(self, ctx: interactions.ComponentContext):
        player = get_player_by_discord_id(str(ctx.author.id))
        weapons = get_equipment_by_type("Weapon")
        weapon = sorted(weapons, key=lambda x: x['level'])[1]  # Second weapon

        if player.has_equipment(weapon['id']):
            # Equip the owned weapon
            update_player_equipment(player, weapon['id'], "Weapon")
            await ctx.send(f"Successfully equipped {weapon['name']}!")
        else:
            # Purchase and equip the weapon
            if update_player_purchase(player, weapon['id'], weapon['price'], "Weapon"):
                await ctx.send(f"Successfully purchased and equipped {weapon['name']}!")
            else:
                await ctx.send("Purchase failed! Check your gold and requirements.")

        # Refresh the shop display
        await self.display_weapons_shop(ctx)

    @interactions.component_callback("weapon_upgrade_3")
    async def weapon_upgrade_3_callback(self, ctx: interactions.ComponentContext):
        # Same pattern as above but with index [2]
        player = get_player_by_discord_id(str(ctx.author.id))
        weapons = get_equipment_by_type("Weapon")
        weapon = sorted(weapons, key=lambda x: x['level'])[2]

        if player.has_equipment(weapon['id']):
            update_player_equipment(player, weapon['id'], "Weapon")
            await ctx.send(f"Successfully equipped {weapon['name']}!")
        else:
            if update_player_purchase(player, weapon['id'], weapon['price'], "Weapon"):
                await ctx.send(f"Successfully purchased and equipped {weapon['name']}!")
            else:
                await ctx.send("Purchase failed! Check your gold and requirements.")

        await self.display_weapons_shop(ctx)

    @interactions.component_callback("weapon_upgrade_4")
    async def weapon_upgrade_4_callback(self, ctx: interactions.ComponentContext):
        # Same pattern as above but with index [3]
        player = get_player_by_discord_id(str(ctx.author.id))
        weapons = get_equipment_by_type("Weapon")
        weapon = sorted(weapons, key=lambda x: x['level'])[3]

        if player.has_equipment(weapon['id']):
            update_player_equipment(player, weapon['id'], "Weapon")
            await ctx.send(f"Successfully equipped {weapon['name']}!")
        else:
            if update_player_purchase(player, weapon['id'], weapon['price'], "Weapon"):
                await ctx.send(f"Successfully purchased and equipped {weapon['name']}!")
            else:
                await ctx.send("Purchase failed! Check your gold and requirements.")

        await self.display_weapons_shop(ctx)

    @interactions.component_callback("armor_upgrade_1")
    async def armor_upgrade_1_callback(self, ctx: interactions.ComponentContext):
        player = get_player_by_discord_id(str(ctx.author.id))
        armor_items = get_equipment_by_type("Armor")
        armor = sorted(armor_items, key=lambda x: x['level'])[0]

        if player.has_equipment(armor['id']):
            # Equip the owned armor
            update_player_equipment(player, armor['id'], "Armor")
            await ctx.send(f"Successfully equipped {armor['name']}!")
        else:
            # Purchase and equip the armor
            if update_player_purchase(player, armor['id'], armor['price'], "Armor"):
                await ctx.send(f"Successfully purchased and equipped {armor['name']}!")
            else:
                await ctx.send("Purchase failed! Check your gold and requirements.")

        # Refresh the shop display
        await self.display_armor_shop(ctx)

    @interactions.component_callback("armor_upgrade_2")
    async def armor_upgrade_2_callback(self, ctx: interactions.ComponentContext):
        player = get_player_by_discord_id(str(ctx.author.id))
        armor_items = get_equipment_by_type("Armor")
        armor = sorted(armor_items, key=lambda x: x['level'])[1]  # Second armor

        if player.has_equipment(armor['id']):
            # Equip the owned armor
            update_player_equipment(player, armor['id'], "Armor")
            await ctx.send(f"Successfully equipped {armor['name']}!")
        else:
            # Purchase and equip the armor
            if update_player_purchase(player, armor['id'], armor['price'], "Armor"):
                await ctx.send(f"Successfully purchased and equipped {armor['name']}!")
            else:
                await ctx.send("Purchase failed! Check your gold and requirements.")

        # Refresh the shop display
        await self.display_armor_shop(ctx)

    @interactions.component_callback("armor_upgrade_3")
    async def armor_upgrade_3_callback(self, ctx: interactions.ComponentContext):
        player = get_player_by_discord_id(str(ctx.author.id))
        armor_items = get_equipment_by_type("Armor")
        armor = sorted(armor_items, key=lambda x: x['level'])[2]  # Third armor

        if player.has_equipment(armor['id']):
            # Equip the owned armor
            update_player_equipment(player, armor['id'], "Armor")
            await ctx.send(f"Successfully equipped {armor['name']}!")
        else:
            # Purchase and equip the armor
            if update_player_purchase(player, armor['id'], armor['price'], "Armor"):
                await ctx.send(f"Successfully purchased and equipped {armor['name']}!")
            else:
                await ctx.send("Purchase failed! Check your gold and requirements.")

        # Refresh the shop display
        await self.display_armor_shop(ctx)

    @interactions.component_callback("armor_upgrade_4")
    async def armor_upgrade_4_callback(self, ctx: interactions.ComponentContext):
        player = get_player_by_discord_id(str(ctx.author.id))
        armor_items = get_equipment_by_type("Armor")
        armor = sorted(armor_items, key=lambda x: x['level'])[3]  # Fourth armor

        if player.has_equipment(armor['id']):
            # Equip the owned armor
            update_player_equipment(player, armor['id'], "Armor")
            await ctx.send(f"Successfully equipped {armor['name']}!")
        else:
            # Purchase and equip the armor
            if update_player_purchase(player, armor['id'], armor['price'], "Armor"):
                await ctx.send(f"Successfully purchased and equipped {armor['name']}!")
            else:
                await ctx.send("Purchase failed! Check your gold and requirements.")

        # Refresh the shop display
        await self.display_armor_shop(ctx)

    @interactions.component_callback("helmet_upgrade_1")
    async def helmet_upgrade_1_callback(self, ctx: interactions.ComponentContext):
        player = get_player_by_discord_id(str(ctx.author.id))
        helmets = get_equipment_by_type("Helmet")
        helmet = sorted(helmets, key=lambda x: x['level'])[0]

        if player.has_equipment(helmet['id']):
            update_player_equipment(player, helmet['id'], "Helmet")
            await ctx.send(f"Successfully equipped {helmet['name']}!")
        else:
            if update_player_purchase(player, helmet['id'], helmet['price'], "Helmet"):
                await ctx.send(f"Successfully purchased and equipped {helmet['name']}!")
            else:
                await ctx.send("Purchase failed! Check your gold and requirements.")

        await self.display_helmets_shop(ctx)

    @interactions.component_callback("helmet_upgrade_2")
    async def helmet_upgrade_2_callback(self, ctx: interactions.ComponentContext):
        player = get_player_by_discord_id(str(ctx.author.id))
        helmets = get_equipment_by_type("Helmet")
        helmet = sorted(helmets, key=lambda x: x['level'])[1]  # Second helmet

        if player.has_equipment(helmet['id']):
            update_player_equipment(player, helmet['id'], "Helmet")
            await ctx.send(f"Successfully equipped {helmet['name']}!")
        else:
            if update_player_purchase(player, helmet['id'], helmet['price'], "Helmet"):
                await ctx.send(f"Successfully purchased and equipped {helmet['name']}!")
            else:
                await ctx.send("Purchase failed! Check your gold and requirements.")

        await self.display_helmets_shop(ctx)

    @interactions.component_callback("helmet_upgrade_3")
    async def helmet_upgrade_3_callback(self, ctx: interactions.ComponentContext):
        player = get_player_by_discord_id(str(ctx.author.id))
        helmets = get_equipment_by_type("Helmet")
        helmet = sorted(helmets, key=lambda x: x['level'])[2]  # Third helmet

        if player.has_equipment(helmet['id']):
            update_player_equipment(player, helmet['id'], "Helmet")
            await ctx.send(f"Successfully equipped {helmet['name']}!")
        else:
            if update_player_purchase(player, helmet['id'], helmet['price'], "Helmet"):
                await ctx.send(f"Successfully purchased and equipped {helmet['name']}!")
            else:
                await ctx.send("Purchase failed! Check your gold and requirements.")

        await self.display_helmets_shop(ctx)

    @interactions.component_callback("helmet_upgrade_4")
    async def helmet_upgrade_4_callback(self, ctx: interactions.ComponentContext):
        player = get_player_by_discord_id(str(ctx.author.id))
        helmets = get_equipment_by_type("Helmet")
        helmet = sorted(helmets, key=lambda x: x['level'])[3]  # Fourth helmet

        if player.has_equipment(helmet['id']):
            update_player_equipment(player, helmet['id'], "Helmet")
            await ctx.send(f"Successfully equipped {helmet['name']}!")
        else:
            if update_player_purchase(player, helmet['id'], helmet['price'], "Helmet"):
                await ctx.send(f"Successfully purchased and equipped {helmet['name']}!")
            else:
                await ctx.send("Purchase failed! Check your gold and requirements.")

        await self.display_helmets_shop(ctx)

    @interactions.component_callback("accessory_upgrade_1")
    async def accessory_upgrade_1_callback(self, ctx: interactions.ComponentContext):
        player = get_player_by_discord_id(str(ctx.author.id))
        accessories = get_equipment_by_type("Accessory")
        accessory = sorted(accessories, key=lambda x: x['level'])[0]

        if player.has_equipment(accessory['id']):
            update_player_equipment(player, accessory['id'], "Accessory")
            await ctx.send(f"Successfully equipped {accessory['name']}!")
        else:
            if update_player_purchase(player, accessory['id'], accessory['price'], "Accessory"):
                await ctx.send(f"Successfully purchased and equipped {accessory['name']}!")
            else:
                await ctx.send("Purchase failed! Check your gold and requirements.")

        await self.display_accessories_shop(ctx)

    @interactions.component_callback("accessory_upgrade_2")
    async def accessory_upgrade_2_callback(self, ctx: interactions.ComponentContext):
        player = get_player_by_discord_id(str(ctx.author.id))
        accessories = get_equipment_by_type("Accessory")
        accessory = sorted(accessories, key=lambda x: x['level'])[1]  # Second accessory

        if player.has_equipment(accessory['id']):
            update_player_equipment(player, accessory['id'], "Accessory")
            await ctx.send(f"Successfully equipped {accessory['name']}!")
        else:
            if update_player_purchase(player, accessory['id'], accessory['price'], "Accessory"):
                await ctx.send(f"Successfully purchased and equipped {accessory['name']}!")
            else:
                await ctx.send("Purchase failed! Check your gold and requirements.")

        await self.display_accessories_shop(ctx)

    @interactions.component_callback("accessory_upgrade_3")
    async def accessory_upgrade_3_callback(self, ctx: interactions.ComponentContext):
        player = get_player_by_discord_id(str(ctx.author.id))
        accessories = get_equipment_by_type("Accessory")
        accessory = sorted(accessories, key=lambda x: x['level'])[2]  # Third accessory

        if player.has_equipment(accessory['id']):
            update_player_equipment(player, accessory['id'], "Accessory")
            await ctx.send(f"Successfully equipped {accessory['name']}!")
        else:
            if update_player_purchase(player, accessory['id'], accessory['price'], "Accessory"):
                await ctx.send(f"Successfully purchased and equipped {accessory['name']}!")
            else:
                await ctx.send("Purchase failed! Check your gold and requirements.")

        await self.display_accessories_shop(ctx)

    @interactions.component_callback("accessory_upgrade_4")
    async def accessory_upgrade_4_callback(self, ctx: interactions.ComponentContext):
        player = get_player_by_discord_id(str(ctx.author.id))
        accessories = get_equipment_by_type("Accessory")
        accessory = sorted(accessories, key=lambda x: x['level'])[3]  # Fourth accessory

        if player.has_equipment(accessory['id']):
            update_player_equipment(player, accessory['id'], "Accessory")
            await ctx.send(f"Successfully equipped {accessory['name']}!")
        else:
            if update_player_purchase(player, accessory['id'], accessory['price'], "Accessory"):
                await ctx.send(f"Successfully purchased and equipped {accessory['name']}!")
            else:
                await ctx.send("Purchase failed! Check your gold and requirements.")

        await self.display_accessories_shop(ctx)