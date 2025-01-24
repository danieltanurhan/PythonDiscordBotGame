import asyncio
from Game.Models.Player import Player
from Game.Managers.SoloCombat import handle_raid_command
from Game.Managers.player_db_connection import get_player_by_discord_id

async def main():
    # Initialize a test player
    player = get_player_by_discord_id(0000000)
    
    # Current tower level (we can make this dynamic later)
    tower_level = 1
    
    print(f"Welcome, {player.username}!")
    print("Current Stats:")
    print(f"Level: {player.level}")
    print(f"HP: {player.current_hp}/{player.max_hp}")
    print(f"Gold: {player.gold}")
    
    while True:
        print("\nAvailable commands:")
        print("/raid - Start a new raid")
        print("/camp - Return to camp and heal")
        print("/quit - Exit game")
        
        command = input("\nEnter command: ").strip().lower()
        
        if command == "/raid":
            if player.current_hp <= 0:
                print("\n❌ You cannot raid while defeated! Use /camp to heal first.")
                continue
                
            print("\n⚔️ Starting raid...")
            summary = await handle_raid_command(player, tower_level)
            print("\n" + summary)
            
            # # Update player state
            # if not results["player_survived"]:
            #     dropped_items = handle_player_death(player)
            #     print("\nYou have been defeated!")
            #     if dropped_items:
            #         print("Items lost:")
            #         for item in dropped_items:
            #             print(f"- {item['item']['name']} from {item['slot']}")
            
            print(f"Current HP: {player.current_hp}/{player.max_hp}")
            print(f"Gold: {player.gold}")
            
        elif command == "/camp":
            # Heal player to full
            old_hp = player.current_hp
            player.current_hp = player.max_hp
            print(f"\n🏕️ Resting at camp...")
            print(f"Healed for {player.max_hp - old_hp} HP")
            print(f"Current HP: {player.current_hp}/{player.max_hp}")
            
        elif command == "/quit":
            print("\nThanks for playing!")
            break
            
        else:
            print("\n❌ Invalid command!")

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())