## Overview

Dungeon Tower is a Discord-based game where players collaborate to hunt monsters, progress through a series of tower levels, and compete with other servers for leaderboard supremacy. The game combines strategic resource management with automated combat and community-driven challenges, aiming to create an engaging and competitive experience.

## Project Structure

```plaintext
dungeon_tower/
│
├── main.py                  # Main bot entry point
├── config.py                # Configuration settings (database, Discord tokens, etc.) 
├── requirements.txt         # Project dependencies
│
├── game/
│   ├── __init__.py
│   ├── models/              # Core game classes
│   │   ├── __init__.py
│   │   ├── player.py
│   │   ├── monster.py
│   │   ├── party.py
│   │   ├── item.py
│   │   └── combat.py
│   │
│   ├── managers/            # Game state and resource managers
│   │   ├── __init__.py
│   │   ├── game_state.py
│   │   ├── party_manager.py
│   │   └── tower_manager.py
│   │
│   ├── utils/               # Utility functions and helpers
│   │   ├── __init__.py
│   │   ├── calculations.py
│   │   └── validators.py
│   │
│   └── data/                # Static game data
│       ├── monsters.json
│       ├── items.json
│       └── levels.json
│
├── database/
│   ├── __init__.py
│   ├── mongodb.py           # Database connection and operations
│   └── schemas/             # MongoDB schema definitions
│       └── __init__.py
│
├── cogs/                    # Discord command modules
│   ├── __init__.py
│   ├── player_commands.py
│   ├── party_commands.py
│   ├── combat_commands.py
│   └── admin_commands.py
│
└── tests/                   # Unit tests
    ├── __init__.py
    ├── test_player.py
    ├── test_combat.py
    └── test_party.py
```

## Features

- **Automated Combat**: Engage in battles with monsters using automated combat mechanics.
- **Resource Management**: Manage your resources strategically to progress through the game.
- **Community Challenges**: Participate in community-driven challenges and events.
- **Leaderboard**: Compete with other servers for the top spot on the leaderboard.

## Getting Started

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/dungeon_tower.git
    cd dungeon_tower
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    Create a `.env` file in the project root and add your MongoDB connection string and Discord token:
    ```plaintext
    MONGODB_CONNECTION_STRING=your_actual_connection_string
    DISCORD_TOKEN=your_discord_token
    ```

4. **Run the bot**:
    ```sh
    python main.py
    ```

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to all contributors and the open-source community for their invaluable support.
