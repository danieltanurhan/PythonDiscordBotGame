from Game.Database.database import Database

loot_data = [
    {
        "id": "L001",
        "name": "Monster Hide",
        "base_price": 10,
        "description": "Common hide from monsters, used in crafting"
    },
    {
        "id": "L002",
        "name": "Shiny Crystal",
        "base_price": 20,
        "description": "A valuable crystal that merchants desire"
    },
    {
        "id": "L003",
        "name": "Ancient Relic",
        "base_price": 30,
        "description": "Mysterious artifact from ancient times"
    },
    {
        "id": "L004",
        "name": "Dragon Scale",
        "base_price": 40,
        "description": "Rare scale from powerful dragons"
    },
    {
        "id": "L005",
        "name": "Magic Essence",
        "base_price": 50,
        "description": "Crystallized magical energy"
    },
    {
        "id": "L006",
        "name": "Golden Feather",
        "base_price": 60,
        "description": "Beautiful feather with golden shine"
    }
]

def populate_loot():
    db = Database()
    loot_collection = db.get_loot_collection()
    print("Populating loot items...")
    
    loot_collection.insert_many(loot_data)
    print(f"Populated {len(loot_data)} loot items")

if __name__ == "__main__":
    populate_loot()
