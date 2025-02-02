import interactions
from interactions import slash_command, SlashContext, Embed, ButtonStyle, slash_option
from typing import Optional

from config import DEV_GUILD
from Game.Managers.player_db_connection import get_player_by_discord_id, update_player_loot
from Game.Managers.loot_db_connection import get_loot_price, get_all_loot

class UtilCog(interactions.Extension):
    def __init__(self, bot):
        self.bot = bot

    def _create_sell_display(self, ctx: interactions.contexts, amount: str, type: Optional[str] = None):
        """Create the display for sell results"""
        player = get_player_by_discord_id(str(ctx.author.id))
        if not player:
            return None, "You need to create a character first!"

        total_gold = 0
        sell_all = amount.lower() == "all"
        error_message = None

        if sell_all:
            # Calculate total value of all items
            for loot_id, quantity in player.loot_inventory.items():
                base_price = get_loot_price(loot_id)
                total_gold += base_price * quantity
            
            # Apply salesman bonus
            salesman_bonus = 1 + (player.get_upgrade_level("salesman") - 1) * 0.1
            total_gold = int(total_gold * salesman_bonus)
            
            # Clear inventory and add gold
            player.gold += total_gold
            player.clear_loot()
            
        else:
            try:
                amount_num = int(amount)
                if not type:
                    return None, "Please specify the type of item to sell!"

                # Find matching loot ID
                all_loot = get_all_loot()
                loot_id = None
                for loot in all_loot:
                    if loot['name'].lower() == type.lower():
                        loot_id = loot['id']
                        break

                if not loot_id:
                    return None, "Invalid item type!"

                if player.get_loot_quantity(loot_id) < amount_num:
                    return None, "You don't have enough of that item!"

                base_price = get_loot_price(loot_id)
                salesman_bonus = 1 + (player.get_upgrade_level("salesman") - 1) * 0.1
                total_gold = int(base_price * amount_num * salesman_bonus)
                
                player.remove_loot(loot_id, amount_num)
                player.gold += total_gold

            except ValueError:
                return None, "Invalid amount! Please use a number or 'all'"

        # Update player in database
        update_player_loot(player)

        # Create response embed
        embed = Embed(
            description=f"✅ You {'sold your entire inventory' if sell_all else f'sold {amount} {type}'} for ${total_gold:,}.\nYou now have ${player.gold:,}!",
            color=0x00ff00
        )
        embed.set_author(name=ctx.author.display_name + "'s profile", icon_url=ctx.author.avatar_url)

        # Create buttons
        buttons = [
            interactions.Button(
                style=ButtonStyle.PRIMARY,
                label="Raid Again",
                custom_id="raid_again"
            ),
            interactions.Button(
                style=ButtonStyle.SECONDARY,
                label="Back",
                custom_id="go_camp"
            )
        ]

        return embed, buttons

    @slash_command(
        name="sell",
        description="Sell items from your inventory",
        scopes=[DEV_GUILD] if DEV_GUILD else None,
    )
    @slash_option(
        name="amount",
        description="Amount to sell (or 'all')",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    @slash_option(
        name="type",
        description="Type of item to sell",
        required=False,
        opt_type=interactions.OptionType.STRING
    )
    async def sell(self, ctx: SlashContext, amount: str, type: Optional[str] = None):
        embed, response = self._create_sell_display(ctx, amount, type)
        if embed:
            await ctx.send(embed=embed, components=response)
        else:
            await ctx.send(response)

    @interactions.component_callback("sell_button")
    async def sell_button_callback(self, ctx: interactions.ComponentContext):
        embed, response = self._create_sell_display(ctx, "all")
        if embed:
            await ctx.edit_origin(embed=embed, components=response)
        else:
            await ctx.edit_origin(content=response)
