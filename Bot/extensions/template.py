"""
This file provides a template for future commands.
This file will not be loaded as a cog or module
"""
import os

import interactions
from interactions import slash_command, SlashContext, Embed, ButtonStyle

from config import DEV_GUILD

"Highly recommended - we suggest providing proper debug logging"
from src import logutil
import random

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Game.Managers.SoloCombat import handle_raid_command, handle_camp_command
from Game.Managers.player_db_connection import get_player_by_discord_id, add_player, player_exists, handle_gypsy_debuff

"Change this if you'd like - this labels log messages for debug mode"
logger = logutil.init_logger(os.path.basename(__file__))


class TemplateCog(interactions.Extension):
    @interactions.slash_command(
        "profile", description="Show your player profile", scopes=[DEV_GUILD] if DEV_GUILD else None
    )
    async def profile(self, ctx: interactions.SlashContext):
        await self.profile_cmd(ctx)
    
    @interactions.component_callback("go_profile")
    async def go_profile(self, ctx: interactions.ComponentContext):
        await self.profile_cmd(ctx)
    
    async def profile_cmd(self, ctx: interactions.contexts):
        """Show the player's profile in a Discord embed"""
        discord_id = str(ctx.author.id)

        buttons = [
            interactions.Button(style=ButtonStyle.PRIMARY, label="Go Camp", custom_id="go_camp"),
            interactions.Button(style=ButtonStyle.PRIMARY, label="Raid", custom_id="raid_again")
        ]

        if not player_exists(discord_id):
            await add_player(discord_id, ctx.author.username)

            embed = Embed(title="Welcome to the game", color=0x00ff00)
            embed.description = (
                f"Welcome, {ctx.author.username}! Your adventure begins now. "
                "Here's what you can do next:\n\n"
                "• Use `/profile` to view your character stats\n"
                "• Use `/raid` to go on a raid (requires level 5)\n"
                "• Explore more commands to level up and grow stronger!"
            )
            embed.add_field(
                name="Getting Started",
                value=(
                    "1. Check your initial stats with `/profile`\n"
                    "2. Start gaining experience and gold\n"
                    "3. Reach level 5 to unlock raids"
                ),
                inline=False
            )
            embed.add_field(
                name="Need Help?",
                value="Use `/help` to see all available commands and their descriptions.",
                inline=False
            )
            await ctx.send(embed=embed, components=buttons)
        else:
            player_data = get_player_by_discord_id(discord_id).to_dict()

            # Create an embed with the player's information
            embed = Embed(title=f"{player_data['username']}'s Profile", color=0x00ff00)
            
            embed.add_field(name="Level", value=str(player_data['level']), inline=True)
            embed.add_field(name="Experience", value=str(player_data['experience']), inline=True)
            embed.add_field(name="Gold", value=str(player_data['gold']), inline=True)
            
            # Add stats
            stats = player_data['stats']
            stats_str = "\n".join([f"{stat.capitalize()}: {value}" for stat, value in stats.items()])
            embed.add_field(name="Stats", value=stats_str, inline=False)
            
            embed.add_field(name="HP", value=f"{player_data['current_hp']}/{player_data['max_hp']}", inline=True)
            embed.add_field(name="Class", value=player_data['character_class'], inline=True)
            
            # Add equipment
            equipment = player_data['equipment']
            equipment_str = "\n".join([f"{slot.capitalize()}: {item}" for slot, item in equipment.items()])
            embed.add_field(name="Equipment", value=equipment_str, inline=False)
            
            # Add tower level if it exists
            if 'tower_level' in player_data:
                embed.add_field(name="Tower Level", value=str(player_data['tower_level']), inline=True)

            await ctx.send(embed=embed, components=buttons)

    @interactions.slash_command(
        "raid", description="Start a raid", scopes=[DEV_GUILD] if DEV_GUILD else None
    )
    async def handle_raid(self, ctx: interactions.SlashContext):
        await self._handle_raid(ctx)

    @interactions.component_callback("raid_again")
    async def handle_raid_again(self, ctx: interactions.ComponentContext):
        await self._handle_raid(ctx)
    
    async def _handle_raid(self, ctx: interactions.contexts):
        self.game_state = {
            "player_alive": True,
            "status": "ongoing"
        }
        """Handle the raid command"""
        discord_id = str(ctx.author.id)
        player = get_player_by_discord_id(discord_id)


        buttons = [
            interactions.Button(style=ButtonStyle.PRIMARY, label="Raid Again", custom_id="raid_again"),
            interactions.Button(style=ButtonStyle.PRIMARY, label="Go Camp", custom_id="go_camp")
        ]

        if not player:
            await ctx.send("You need to create a character first. Use the `/start` command to begin your adventure!")
            return

        # Process the raid using the handle_raid_command function
        if player.current_hp <= 0:
            await ctx.send("You cannot raid while defeated! Use /camp to heal first.")
        else:
            raid_summary = await handle_raid_command(player)

            # Create an embed with the raid results
            embed = Embed(
                title="Raid Results",
                description=raid_summary,
                color=0x00ff00
            )

        await ctx.send(embed=embed, components=buttons)


    @interactions.slash_command(
        "camp", description="Go back to camp", scopes=[DEV_GUILD] if DEV_GUILD else None
    )
    async def go_camp(self, ctx: interactions.SlashContext):
        await self._go_camp(ctx)
    
    
    @interactions.component_callback("go_camp")
    async def go_camp_callback(self, ctx: interactions.ComponentContext):
        await self._go_camp(ctx)
    
    async def _go_camp(self, ctx: interactions.contexts):
        """Handle the camp command"""
        discord_id = str(ctx.author.id)
        player = get_player_by_discord_id(discord_id)

        buttons = [
            interactions.Button(style=ButtonStyle.PRIMARY, label="Raid", custom_id="raid_again"),
            interactions.Button(style=ButtonStyle.PRIMARY, label="Gypsy Debuff", custom_id="gypsy_debuff")
        ]

        if not player:
            await ctx.send("You need to create a character first. Use the `/start` command to begin your adventure!")
            return

        # Process the camp using the handle_camp_command function
        camp_summary = await handle_camp_command(player)

        # Create an embed with the camp results
        embed = Embed(
            title="Camp Results",
            description=camp_summary,
            color=0x00ff00
        )

        await ctx.send(embed=embed, components=buttons)
    
    @interactions.component_callback("gypsy_debuff")
    async def gypsy_debuff_callback(self, ctx: interactions.ComponentContext):
        discord_id = str(ctx.author.id)
        player = get_player_by_discord_id(discord_id)

        buttons = [
            interactions.Button(style=ButtonStyle.PRIMARY, label="Raid", custom_id="raid_again"),
            interactions.Button(style=ButtonStyle.PRIMARY, label="Go Camp", custom_id="go_camp"),
            interactions.Button(style=ButtonStyle.PRIMARY, label="Profile", custom_id="go_profile")
        ]

        if not player:
            await ctx.send("You need to create a character first. Use the `/start` command to begin your adventure!")
            return

        await handle_gypsy_debuff(player)

        embed = Embed(
                title="Gypsy Buff Applied!",
                description="Gypsy BUFF applied! Good luck out there my car loving golden friend!",
                color=0x00ff00
            )

        await ctx.send(embed=embed, components=buttons)

    @interactions.slash_command(
        "blackjack", description="Play Blackjack game", scopes=[DEV_GUILD] if DEV_GUILD else None
    )
    async def blackjack_cmd(self, ctx: interactions.SlashContext):
        """Start a blackjack game with buttons for actions"""
        # Initialize game state
        self.game_state = {
            "player_hand": [],
            "dealer_hand": [],
            "status": "ongoing"
        }
        # Save self.game_state associated with ctx.user.id

        embed = Embed(
            title="Blackjack Game",
            description="Choose an action below",
            color=0x1E90FF
        )
        buttons = [
            interactions.Button(style=ButtonStyle.PRIMARY, label="Hit", custom_id="hit_button"),
            interactions.Button(style=ButtonStyle.SECONDARY, label="Stand", custom_id="stand_button")
        ]
        await ctx.send(embed=embed, components=buttons)

    @interactions.component_callback("hit_button")
    async def hit_button_callback(self, ctx: interactions.ComponentContext):
        """Handle the Hit action"""
        await ctx.defer(edit_origin=True)  # Acknowledge the context

        # Draw a card for the player
        card = random.choice(["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"])
        self.game_state["player_hand"].append(card)

        # Calculate the new hand value
        player_score = self.calculate_hand_value(self.game_state["player_hand"])

        # Check if the player has busted
        if player_score > 21:
            result = "You busted! Dealer wins!"
            self.game_state["status"] = "finished"
        else:
            result = "Choose an action below"

        # Update the embed with the new hand and status
        embed = Embed(
            title="Blackjack Game",
            description=f"**Player's Hand**: {', '.join(self.game_state['player_hand'])} (Value: {player_score})\n\n"
                        f"{result}",
            color=0x1E90FF
        )

        # If the game is still ongoing, show the action buttons again
        if self.game_state["status"] == "ongoing":
            buttons = [
                interactions.Button(style=ButtonStyle.PRIMARY, label="Hit", custom_id="hit_button"),
                interactions.Button(style=ButtonStyle.SECONDARY, label="Stand", custom_id="stand_button")
            ]
            await ctx.edit_origin(embed=embed, components=buttons)
        else:
            await ctx.edit_origin(embed=embed)

    @interactions.component_callback("stand_button")
    async def stand_button_callback(self, ctx: interactions.ComponentContext):
        """Handle the Stand action and dealer's turn"""
        await ctx.defer_update(edit_origin=True)  # Acknowledge the context

        # Dealer drawing logic
        while self.calculate_hand_value(self.game_state["dealer_hand"]) < 17:
            card = random.choice(["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"])
            self.game_state["dealer_hand"].append(card)

        # Compare scores and determine outcome
        player_score = self.calculate_hand_value(self.game_state["player_hand"])
        dealer_score = self.calculate_hand_value(self.game_state["dealer_hand"])

        if dealer_score > 21 or player_score > dealer_score:
            result = "You win!"
        elif player_score < dealer_score:
            result = "Dealer wins!"
        else:
            result = "It's a tie!"

        # Update embed with final hands and result
        embed = Embed(
            title="Blackjack Game - Result",
            description=f"**Player's Hand**: {', '.join(self.game_state['player_hand'])} (Value: {player_score})\n"
                        f"**Dealer's Hand**: {', '.join(self.game_state['dealer_hand'])} (Value: {dealer_score})\n\n"
                        f"**Result**: {result}",
            color=0x1E90FF
        )

        # Update self.game_state["status"]
        self.game_state["status"] = "finished"
        await ctx.edit_origin(embed=embed)

    def calculate_hand_value(self, hand):
        """Calculate the value of a blackjack hand"""
        value = 0
        ace_count = 0
        card_values = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
            "J": 10, "Q": 10, "K": 10, "A": 11
        }

        for card in hand:
            value += card_values[card]
            if card == "A":
                ace_count += 1

        while value > 21 and ace_count:
            value -= 10
            ace_count -= 1

        return value