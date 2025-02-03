from Game.Database.database import Database

db = Database()
upgrades_collection = db.get_upgrades_collection()

def get_upgrade_by_id(upgrade_id: str):
    upgrade_data = upgrades_collection.find_one({"upgrade_id": upgrade_id})
    return upgrade_data

def get_all_upgrades():
    upgrade_data = upgrades_collection.find()
    return [upgrade for upgrade in upgrade_data]