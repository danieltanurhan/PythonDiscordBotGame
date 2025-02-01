import re
import interactions
from interactions import slash_command, SlashContext, Embed, ButtonStyle, ActionRow, Button

from config import DEV_GUILD
from utils.paginator import CustomPaginator
from Game.Managers.equipment_db_connection import get_equipment_by_type, get_equipment_by_id
from Game.Managers.player_db_connection import get_player_by_discord_id, update_player_purchase, update_player_equipment

class ShopEquipmentUpgradeCog(interactions.Extension):
    def __init__(self, bot):
        self.bot = bot
        self._current_page = 0
        self._current_paginator = None

    @property
    def current_paginator(self):
        return self._current_paginator
        
    @current_paginator.setter
    def current_paginator(self, value):
        self._current_paginator = value

    @property
    def current_page(self):
        return self._current_page
        
    @current_page.setter 
    def current_page(self, value):
        self._current_page = value

    def _create_navigation_buttons(self):
        return {
            'back': interactions.Button(style=ButtonStyle.SECONDARY, label="Back", custom_id="shop_button"),
            'return': interactions.Button(style=ButtonStyle.SECONDARY, label="Return", custom_id="go_profile")
        }

    def _create_equipment_buttons(self, player, items, equipment_type, start_idx=0):
        """Generic button creator for equipment types"""
        buttons = []
        for i in range(len(items)):
            if start_idx + i >= len(items):
                break
                
            item = items[start_idx + i]
            button = interactions.Button(
                style=ButtonStyle.PRIMARY,
                label=f"Upgrade {i+1}",
                custom_id=f"{equipment_type.lower()}_upgrade_{i+1}"
            )
            
            is_equipped = player.has_equipped(item['id'])
            is_owned = player.has_equipment(item['id'])
            can_afford = player.can_afford(item['price'])
            meets_level = player.can_equip(item['level'])
            
            button.disabled = is_equipped or (not is_owned and (not can_afford or not meets_level))
            if is_equipped:
                button.style = ButtonStyle.SUCCESS
                button.label = "Equipped"
            elif is_owned:
                button.style = ButtonStyle.SUCCESS
                button.label = "Equip"
            else:
                button.style = ButtonStyle.PRIMARY
                button.label = f"${item['price']}"
                
            buttons.append(button)

        return buttons

    async def _create_equipment_display(self, ctx, equipment_type, page_number=None):
        """Generic display creator for equipment types"""
        if page_number is not None:
            self.current_page = page_number
            
        items = get_equipment_by_type(equipment_type)
        player = get_player_by_discord_id(str(ctx.author.id))
        
        sorted_items = sorted(items, key=lambda x: x['level'])
        embeds = []
        for i in range(0, len(sorted_items), 3):
            embed = Embed(title=f"{equipment_type} Shop", color=0x00ff00)
            
            for item in sorted_items[i:i+3]:
                is_equipped = player.has_equipped(item['id'])
                is_owned = player.has_equipment(item['id'])
                can_afford = player.can_afford(item['price'])
                meets_level = player.can_equip(item['level'])
                
                name = item['name']
                description = item.get('description', 'No description available.')
                
                if is_equipped:
                    item_info = f"{name} - EQUIPPED\n{description}"
                elif is_owned:
                    item_info = f"{name} - OWNED\n{description}"
                else:
                    level_req = f"(Lvl {item['level']})"
                    price = f"{item['price']} gold"
                    requirements = []
                    if not meets_level:
                        requirements.append("🔒 Level too low")
                    if not can_afford:
                        requirements.append("❌ Cannot afford")
                    req_text = " - " + ", ".join(requirements) if requirements else ""
                    item_info = f"{name} {level_req} | {price}\n{description}{req_text}"
                
                embed.add_field(name="\u200b", value=item_info, inline=False)
            
            embeds.append(embed)

        nav_buttons = self._create_navigation_buttons()
        equipment_buttons = self._create_equipment_buttons(player, sorted_items, equipment_type)

        paginator = CustomPaginator.create_from_embeds(
            self.bot, 
            *embeds,
            page_index=self.current_page
        )

        paginator.page_index = self.current_page

        buttons_per_row = 3
        button_rows = []
        for i in range(0, len(equipment_buttons), buttons_per_row):
            row_buttons = equipment_buttons[i:i + buttons_per_row]
            if row_buttons:  # Only create row if there are buttons
                button_rows.append(interactions.ActionRow(*row_buttons))

        paginator.custom_buttons = [interactions.ActionRow(nav_buttons['back'])] + button_rows
        
        paginator.show_first_button = False
        paginator.show_last_button = False

        self.current_paginator = paginator
        paginator._author_id = ctx.author.id
        
        return paginator.to_dict()

    async def _handle_equipment_upgrade(self, ctx, equipment_type):
        """Generic handler for equipment upgrades"""
        try:
            button_num = int(ctx.custom_id.split('_')[-1])
            
            player = get_player_by_discord_id(str(ctx.author.id))
            items = get_equipment_by_type(equipment_type)
            sorted_items = sorted(items, key=lambda x: x['level'])
            
            self.current_page = self.current_paginator.page_index
            items_per_page = 3
            start_idx = self.current_page * items_per_page
            visible_items = sorted_items[start_idx:start_idx + items_per_page]
            
            item_idx = (button_num - 1) % items_per_page
            
            if item_idx >= len(visible_items):
                await ctx.send(f"That {equipment_type.lower()} slot is empty!", ephemeral=True)
                return
                
            item = visible_items[item_idx]
            
            message = ""
            if player.has_equipment(item['id']):
                update_player_equipment(player, item['id'], equipment_type)
                message = f"Successfully equipped {item['name']}!"
            else:
                if update_player_purchase(player, item['id'], item['price'], equipment_type):
                    message = f"Successfully purchased and equipped {item['name']}!"
                else:
                    message = "Purchase failed! Check your gold and requirements."
            
            paginator_dict = await self._create_equipment_display(ctx, equipment_type, self.current_page)
            paginator_dict['content'] = message
            await ctx.edit_origin(**paginator_dict)
            
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}", ephemeral=True)

    # Armor commands
    @interactions.subcommand(description="View armor in the shop", base="shop")
    async def armor(self, ctx: SlashContext):
        paginator_dict = await self._create_equipment_display(ctx, "Armor")
        await ctx.send(**paginator_dict)

    @interactions.component_callback("shop_armor")
    async def shop_armor_callback(self, ctx: interactions.ComponentContext):
        paginator_dict = await self._create_equipment_display(ctx, "Armor")
        await ctx.edit_origin(**paginator_dict)

    @interactions.component_callback(re.compile("^armor_upgrade_[1-9]$"))
    async def armor_upgrade_callback(self, ctx: interactions.ComponentContext):
        await self._handle_equipment_upgrade(ctx, "Armor")

    # Helmet commands
    @interactions.subcommand(description="View helmets in the shop", base="shop")
    async def helmets(self, ctx: SlashContext):
        paginator_dict = await self._create_equipment_display(ctx, "Helmet")
        await ctx.send(**paginator_dict)

    @interactions.component_callback("shop_helmets")
    async def shop_helmets_callback(self, ctx: interactions.ComponentContext):
        paginator_dict = await self._create_equipment_display(ctx, "Helmet")
        await ctx.edit_origin(**paginator_dict)

    @interactions.component_callback(re.compile("^helmet_upgrade_[1-9]$"))
    async def helmet_upgrade_callback(self, ctx: interactions.ComponentContext):
        await self._handle_equipment_upgrade(ctx, "Helmet")

    # Accessory commands
    @interactions.subcommand(description="View accessories in the shop", base="shop")
    async def accessories(self, ctx: SlashContext):
        paginator_dict = await self._create_equipment_display(ctx, "Accessory")
        await ctx.send(**paginator_dict)

    @interactions.component_callback("shop_accessories")
    async def shop_accessories_callback(self, ctx: interactions.ComponentContext):
        paginator_dict = await self._create_equipment_display(ctx, "Accessory")
        await ctx.edit_origin(**paginator_dict)

    @interactions.component_callback(re.compile("^accessory_upgrade_[1-9]$"))
    async def accessory_upgrade_callback(self, ctx: interactions.ComponentContext):
        await self._handle_equipment_upgrade(ctx, "Accessory")

    # Weapon commands
    @interactions.subcommand(description="View weapons in the shop", base="shop")
    async def weapons(self, ctx: SlashContext):
        paginator_dict = await self._create_equipment_display(ctx, "Weapon")
        await ctx.send(**paginator_dict)

    @interactions.component_callback("shop_weapons")
    async def shop_weapons_callback(self, ctx: interactions.ComponentContext):
        paginator_dict = await self._create_equipment_display(ctx, "Weapon")
        await ctx.edit_origin(**paginator_dict)

    @interactions.component_callback(re.compile("^weapon_upgrade_[1-9]$"))
    async def weapon_upgrade_callback(self, ctx: interactions.ComponentContext):
        await self._handle_equipment_upgrade(ctx, "Weapon")