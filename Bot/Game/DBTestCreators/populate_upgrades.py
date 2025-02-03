from Game.Database.database import Database



upgrades_data = [
    {
        "upgrade_id": "1",
        "name": "Salesman",
        "description": "Increase loot price by 5%",
        "price": 100
    },
    {
        "upgrade_id": "2",
        "name": "Worker",
        "description": "Increase loot drop rate by 5%",
        "price": 150
    },
    {
        "upgrade_id": "3",
        "name": "Mount",
        "description": "Increase raid cooldown by 5%",
        "price": 200
    },  
]

def populate_upgrades():
    db = Database()
    upgrades_collection = db.get_upgrades_collection()
    print("Populating upgrades...")
    upgrades_collection.insert_many(upgrades_data)
    print(f"Populated {len(upgrades_data)} upgrades")

if __name__ == "__main__":
    populate_upgrades()