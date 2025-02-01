import re
import interactions
from interactions import SlashContext, Embed, ButtonStyle, ActionRow, Button

from config import DEV_GUILD

from utils.paginator import CustomPaginator
from Game.Managers.equipment_db_connection import get_equipment_by_type, get_equipment_by_id
from Game.Managers.player_db_connection import get_player_by_discord_id, update_player_purchase, update_player_equipment

class ShopCog(interactions.Extension):

    def __init__(self, bot):
        self.bot = bot

    def _create_navigation_buttons(self):
        """Create fresh navigation buttons"""
        return {
            'back': interactions.Button(style=ButtonStyle.SECONDARY, label="Back", custom_id="shop_button"),
            'return': interactions.Button(style=ButtonStyle.SECONDARY, label="Return", custom_id="go_profile")
        }

    @interactions.slash_command(
        "shop", description="Open the game shop"
    )
    async def shop_command(self, ctx: SlashContext):
        embed, components = self._create_shop_display(ctx)
        await ctx.send(embed=embed, components=components)

    @interactions.component_callback("shop_button")
    async def shop_button_callback(self, ctx: interactions.ComponentContext):
        embed, components = self._create_shop_display(ctx)
        await ctx.edit_origin(embed=embed, components=components)

    def _create_shop_display(self, ctx: interactions.contexts):
        buttons = [
            interactions.Button(style=ButtonStyle.PRIMARY, label="Weapons", custom_id="shop_weapons"),
            interactions.Button(style=ButtonStyle.PRIMARY, label="Armor", custom_id="shop_armor"),
            interactions.Button(style=ButtonStyle.PRIMARY, label="Helmets", custom_id="shop_helmets"),
            interactions.Button(style=ButtonStyle.PRIMARY, label="Accessories", custom_id="shop_accessories")
        ]

        component = [
            interactions.ActionRow(buttons[0], buttons[1], buttons[2], buttons[3]),
            interactions.ActionRow(self._create_navigation_buttons()['return'])
            ]


        embed = Embed(
            title="Select a category to browse items",
            description="/shop weapons",
            color=0x00ff00
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        return embed, component

