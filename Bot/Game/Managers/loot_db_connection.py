from Game.Database.database import Database

db = Database()
loot_collection = db.get_loot_collection()

def get_loot_by_id(loot_id: str) -> dict:
    loot_data = loot_collection.find_one({"id": loot_id})
    return loot_data

def get_all_loot() -> list:
    loot_data = loot_collection.find()
    return [loot for loot in loot_data]

def get_loot_price(loot_id: str) -> int:
    """Get the base price of a loot item"""
    loot_data = get_loot_by_id(loot_id)
    return loot_data.get('base_price', 0) if loot_data else 0
