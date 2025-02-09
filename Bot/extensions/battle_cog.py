import interactions
from interactions import slash_command, SlashContext, Embed, ButtonStyle
from datetime import datetime

from config import DEV_GUILD
from Game.Managers.SoloCombat import RaidManager, handle_raid_command
from Game.Managers.player_db_connection import (
    get_player_by_discord_id, 
    update_player_rewards,
    handle_player_death
)

class BattleCog(interactions.Extension):
    def __init__(self, client) -> None:
        self.client = client
        self.raid_manager = RaidManager()

    def _create_battle_display(self, ctx: interactions.contexts):
        """Create the battle menu display"""
        buttons = [
            interactions.Button(style=ButtonStyle.PRIMARY, label="Single Battle", custom_id="battle_single"),
            interactions.Button(style=ButtonStyle.PRIMARY, label="Raid", custom_id="battle_raid"),
            interactions.Button(style=ButtonStyle.SECONDARY, label="Back", custom_id="go_camp")
        ]

        component = [
            interactions.ActionRow(buttons[0], buttons[1]),
            interactions.ActionRow(buttons[2])
        ]

        embed = Embed(
            title="Choose Your Battle",
            description="Select a battle type:\n\n"
                       "🗡️ **Single Battle** - Fight one monster\n"
                       "⚔️ **Raid** - Face multiple monsters for better rewards",
            color=0x00ff00
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        return embed, component

    @slash_command(
        "battle", 
        description="Combat commands",
        scopes=[DEV_GUILD] if DEV_GUILD else None
    )
    async def battle_command(self, ctx: SlashContext):
        """Base battle command - shows battle options"""
        embed, components = self._create_battle_display(ctx)
        await ctx.send(embed=embed, components=components)

    @interactions.component_callback("battle_button")
    async def battle_button_callback(self, ctx: interactions.ComponentContext):
        """Handle the battle button press from camp"""
        embed, components = self._create_battle_display(ctx)
        await ctx.edit_origin(embed=embed, components=components)

    @interactions.subcommand(
        base="battle",
        name="single",
        description="Fight a single monster"
    )
    async def single_battle(self, ctx: SlashContext) -> None:
        """Handle single battle command"""
        discord_id = str(ctx.author.id)
        player = get_player_by_discord_id(discord_id)
        
        if not player:
            await ctx.send("You need to create a character first. Use the `/start` command!")
            return

        buttons = [
            interactions.Button(style=ButtonStyle.PRIMARY, label="Battle Again", custom_id="battle_again"),
            interactions.Button(style=ButtonStyle.SECONDARY, label="Back", custom_id="battle_button")
        ]

        if player.current_hp <= 0:
            await ctx.send("You cannot battle while defeated! Use /camp to heal first.")
            return

        # Generate a single monster using RaidManager's monster generation
        monsters = await self.raid_manager.generate_monsters(player.tower_level, player.level)
        if not monsters:
            await ctx.send("No suitable monsters found for your level!")
            return
            
        monster = monsters[0]  # Take first monster since we only need one
        
        # Process the battle
        battle_result = await self.raid_manager.process_battle(player, monster)
        
        # Create battle summary
        summary = await self.create_battle_summary(battle_result, player, monster)
        
        # Handle rewards and death if necessary
        if player.current_hp <= 0:
            death_summary = handle_player_death(player)
            summary += "\n\n**Death Consequences:**"
            summary += f"\n💀 HP Restored: {death_summary['hp_restored']}"
            summary += f"\n💰 Gold Lost: {death_summary['gold_lost']}"
       
        # Process rewards
        reward_update = update_player_rewards(
            player,
            battle_result["rewards"]["experience"],
            {"total_rewards": battle_result["rewards"]}
        )
            
        if reward_update["leveled_up"]:
            summary += f"\n🎉 **Level Up!** You are now level {reward_update['new_level']}! 🎉"

        # Create and send embed
        embed = Embed(
            title="Battle Results",
            description=summary,
            color=0x00ff00 if battle_result["player_won"] else 0xff0000
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        
        await ctx.send(embed=embed, components=buttons)

    @staticmethod
    async def create_battle_summary(battle_result: dict, player, monster) -> str:
        """Create a detailed summary of a single battle"""
        summary = "⚔️ **Battle Summary** ⚔️\n\n"
        
        # Monster Information
        summary += f"**🎯 Target:** Level {monster.level} {monster.name}\n"
        summary += f"**📊 Monster Stats:**\n"
        summary += f"- 💪 Damage: {monster.damage}\n"
        summary += f"- 🛡️ Defense: {monster.defense}\n"
        summary += f"- 🎨 Rarity: {monster.rarity}\n\n"
        
        # Battle Outcome
        if battle_result["player_won"]:
            summary += "**🏆 Victory!**\n"
            summary += f"✨ Experience Gained: {battle_result['rewards']['experience']}\n"
            
            # Loot Summary
            if battle_result["rewards"]["loot"]:
                summary += "\n**🎁 Loot Acquired:**\n"
                for loot_id, loot_info in battle_result["rewards"]["loot"].items():
                    summary += f"- {loot_info['name']}: {loot_info['quantity']}x\n"
        else:
            summary += "**💀 Defeat!**\n"
            summary += f"💔 Damage Taken: {battle_result['damage_taken']}\n"
        
        # Player Status
        summary += f"\n**❤️ Health:** {player.current_hp}/{player.max_hp}\n"
        
        return summary

    @interactions.subcommand(
        base="battle",
        name="raid",
        description="Start a raid against multiple monsters"
    )
    async def raid_battle(self, ctx: SlashContext):
        """Handle raid battle command"""
        await self._handle_raid(ctx)
    
    async def _handle_raid(self, ctx: interactions.contexts):
        """Handle the raid command"""
        discord_id = str(ctx.author.id)
        player = get_player_by_discord_id(discord_id)
        if not player:
            await ctx.send("You need to create a character first. Use the `/profile` command!")
            return

        buttons = [
            interactions.Button(style=ButtonStyle.PRIMARY, label="Raid Again", custom_id="raid_again"),
            interactions.Button(style=ButtonStyle.SECONDARY, label="Back", custom_id="battle_button")
        ]

        if player.current_hp <= 0:
            await ctx.send("You cannot raid while defeated! Use /camp to heal first.")
        else:
            raid_summary = await handle_raid_command(player, ctx)
            if raid_summary:  # Only send raid results if raid was actually performed
                embed = Embed(            
                    title="Raid Results",
                    description=raid_summary,
                    color=0x00ff00
                )
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed, components=buttons)

    @interactions.component_callback("battle_single")
    async def battle_single_callback(self, ctx: interactions.ComponentContext):
        await self.single_battle(ctx)

    @interactions.component_callback("battle_raid")
    async def battle_raid_callback(self, ctx: interactions.ComponentContext):
        await self.raid_battle(ctx)

    @interactions.component_callback("battle_again")
    async def handle_battle_again(self, ctx: interactions.ComponentContext):
        await self.single_battle(ctx)

    @interactions.component_callback("raid_again")
    async def handle_raid_again(self, ctx: interactions.ComponentContext):
        await self.raid_battle(ctx)

def setup(client) -> None:
    BattleCog(client)