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
    
    def get_guilds_collection(self):
        return self.db['guilds']

    def get_equipment_collection(self):
        return self.db['equipment']

    def get_loot_collection(self):
        return self.db['loot_items']