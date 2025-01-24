# database.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables

class Database:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        connection_string = os.getenv('MONGODB_CONNECTION_STRING')
        self.client = MongoClient(connection_string)
        self.db = self.client['game_world_database']

    def get_monsters_collection(self):
        return self.db['monsters']

    def get_players_collection(self):
        return self.db['players']

# Optional: Create .env file in project root
# MONGODB_CONNECTION_STRING=your_actual_connection_string