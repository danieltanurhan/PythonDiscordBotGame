import re
import interactions
from interactions import slash_command, SlashContext, Embed, ButtonStyle, ActionRow, Button

from config import DEV_GUILD
from utils.paginator import CustomPaginator
from Game.Managers.upgrades_db_connection import get_all_upgrades
from Game.Managers.player_db_connection import get_player_by_discord_id, update_player_upgrades

class ShopUpgradesCog(interactions.Extension):
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

    def _create_upgrade_buttons(self, player, upgrades, start_idx=0):
        buttons = []
        for i in range(len(upgrades)):
            if start_idx + i >= len(upgrades):
                break
                
            upgrade = upgrades[start_idx + i]
            current_level = player.get_upgrade_level(upgrade['name'].lower())
            price = upgrade['price'] * current_level  # Price increases with level
            
            button = interactions.Button(
                style=ButtonStyle.PRIMARY,
                label=f"Upgrade {i+1}",
                custom_id=f"upgrade_{i+1}"
            )
            
            can_afford = player.can_afford(price)
            
            button.disabled = not can_afford
            button.style = ButtonStyle.PRIMARY
            button.label = f"${price}"
                
            buttons.append(button)

        return buttons

    async def _create_upgrades_display(self, ctx, page_number=None):
        if page_number is not None:
            self.current_page = page_number
            
        upgrades = get_all_upgrades()
        player = get_player_by_discord_id(str(ctx.author.id))
        
        embeds = []
        for i in range(0, len(upgrades), 3):
            embed = Embed(title="Upgrades Shop", color=0x00ff00)
            
            for upgrade in upgrades[i:i+3]:
                current_level = player.get_upgrade_level(upgrade['name'].lower())
                price = upgrade['price'] * current_level
                can_afford = player.can_afford(price)
                
                name = upgrade['name']
                description = upgrade['description']
                
                requirements = []
                if not can_afford:
                    requirements.append("❌ Cannot afford")
                req_text = " - " + ", ".join(requirements) if requirements else ""
                
                upgrade_info = f"{name} (Level {current_level})\n{description}\nNext Level: {price} gold{req_text}"
                embed.add_field(name="\u200b", value=upgrade_info, inline=False)
            
            embeds.append(embed)

        nav_buttons = self._create_navigation_buttons()
        upgrade_buttons = self._create_upgrade_buttons(player, upgrades)

        paginator = CustomPaginator.create_from_embeds(
            self.bot, 
            *embeds,
            page_index=self.current_page
        )

        paginator.page_index = self.current_page

        buttons_per_row = 3
        button_rows = []
        for i in range(0, len(upgrade_buttons), buttons_per_row):
            row_buttons = upgrade_buttons[i:i + buttons_per_row]
            if row_buttons:
                button_rows.append(interactions.ActionRow(*row_buttons))

        paginator.custom_buttons = [interactions.ActionRow(nav_buttons['back'])] + button_rows
        
        paginator.show_first_button = False
        paginator.show_last_button = False

        self.current_paginator = paginator
        paginator._author_id = ctx.author.id
        
        return paginator.to_dict()

    async def _handle_upgrade_purchase(self, ctx):
        try:
            button_num = int(ctx.custom_id.split('_')[-1])
            
            player = get_player_by_discord_id(str(ctx.author.id))
            upgrades = get_all_upgrades()
            
            self.current_page = self.current_paginator.page_index
            items_per_page = 3
            start_idx = self.current_page * items_per_page
            visible_upgrades = upgrades[start_idx:start_idx + items_per_page]
            
            upgrade_idx = (button_num - 1) % items_per_page
            
            if upgrade_idx >= len(visible_upgrades):
                await ctx.send("That upgrade slot is empty!", ephemeral=True)
                return
                
            upgrade = visible_upgrades[upgrade_idx]
            current_level = player.get_upgrade_level(upgrade['name'].lower())
            price = upgrade['price'] * current_level
            
            message = ""
            if player.can_afford(price):
                player.gold -= price
                player.upgrade(upgrade['name'].lower())
                update_player_upgrades(player)
                message = f"Successfully upgraded {upgrade['name']} to level {current_level + 1}!"
            else:
                message = "Upgrade failed! Not enough gold."
            
            paginator_dict = await self._create_upgrades_display(ctx, self.current_page)
            paginator_dict['content'] = message
            await ctx.edit_origin(**paginator_dict)
            
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}", ephemeral=True)

    @interactions.subcommand(description="View available upgrades", base="shop")
    async def upgrades(self, ctx: SlashContext):
        paginator_dict = await self._create_upgrades_display(ctx)
        await ctx.send(**paginator_dict)

    @interactions.component_callback("shop_upgrades")
    async def shop_upgrades_callback(self, ctx: interactions.ComponentContext):
        paginator_dict = await self._create_upgrades_display(ctx)
        await ctx.edit_origin(**paginator_dict)

    @interactions.component_callback(re.compile("^upgrade_[1-9]$"))
    async def upgrade_callback(self, ctx: interactions.ComponentContext):
        await self._handle_upgrade_purchase(ctx)
