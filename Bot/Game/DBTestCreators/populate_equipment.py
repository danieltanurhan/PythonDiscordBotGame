# populate_monsters.py
from Game.Database.database import Database

equipment_data = [
  {
    "id": "W000",
    "name": "Wooden Sword",
    "level": 1,
    "type": "Weapon",
    "stats": {
      "Strength": 5,
      "Agility": 2,
      "Intelligence": 0,
      "Vitality": 3
    },
    "price": 100
  },
  {
    "id": "W001",
    "name": "Bronze Saber",
    "level": 2,
    "type": "Weapon",
    "stats": {
      "Strength": 8,
      "Agility": 3,
      "Intelligence": 0,
      "Vitality": 5
    },
    "price": 250
  },
  {
    "id": "W002",
    "name": "Iron Blade",
    "level": 3,
    "type": "Weapon",
    "stats": {
      "Strength": 12,
      "Agility": 4,
      "Intelligence": 0,
      "Vitality": 7
    },
    "price": 500
  },
  {
    "id": "W003",
    "name": "Steel Longsword",
    "level": 4,
    "type": "Weapon",
    "stats": {
      "Strength": 16,
      "Agility": 5,
      "Intelligence": 0,
      "Vitality": 10
    },
    "price": 1000
  },

  {
    "id": "A000",
    "name": "Leather Armor",
    "level": 1,
    "type": "Armor",
    "stats": {
      "Strength": 0,
      "Agility": 2,
      "Intelligence": 0,
      "Vitality": 5
    },
    "price": 120
  },
  {
    "id": "A001",
    "name": "Bronze Chestguard",
    "level": 2,
    "type": "Armor",
    "stats": {
      "Strength": 0,
      "Agility": 3,
      "Intelligence": 0,
      "Vitality": 10
    },
    "price": 300
  },
  {
    "id": "A002",
    "name": "Iron Hauberk",
    "level": 3,
    "type": "Armor",
    "stats": {
      "Strength": 0,
      "Agility": 4,
      "Intelligence": 0,
      "Vitality": 15
    },
    "price": 600
  },
  {
    "id": "A003",
    "name": "Steel Breastplate",
    "level": 4,
    "type": "Armor",
    "stats": {
      "Strength": 0,
      "Agility": 5,
      "Intelligence": 0,
      "Vitality": 21
    },
    "price": 1200
  },

  {
    "id": "H000",
    "name": "Leather Helmet",
    "level": 1,
    "type": "Helmet",
    "stats": {
      "Strength": 0,
      "Agility": 1,
      "Intelligence": 0,
      "Vitality": 3
    },
    "price": 80
  },
  {
    "id": "H001",
    "name": "Bronze Helm",
    "level": 2,
    "type": "Helmet",
    "stats": {
      "Strength": 0,
      "Agility": 2,
      "Intelligence": 0,
      "Vitality": 6
    },
    "price": 200
  },
  {
    "id": "H002",
    "name": "Iron Crown",
    "level": 3,
    "type": "Helmet",
    "stats": {
      "Strength": 0,
      "Agility": 3,
      "Intelligence": 0,
      "Vitality": 10
    },
    "price": 400
  },
  {
    "id": "H003",
    "name": "Steel Visor",
    "level": 4,
    "type": "Helmet",
    "stats": {
      "Strength": 0,
      "Agility": 4,
      "Intelligence": 0,
      "Vitality": 15
    },
    "price": 800
  },

  {
    "id": "ACC000",
    "name": "Wooden Ring",
    "level": 1,
    "type": "Accessory",
    "stats": {
      "Strength": 2,
      "Agility": 1,
      "Intelligence": 0,
      "Vitality": 1
    },
    "price": 50
  },
  {
    "id": "ACC001",
    "name": "Bronze Ring",
    "level": 2,
    "type": "Accessory",
    "stats": {
      "Strength": 4,
      "Agility": 2,
      "Intelligence": 0,
      "Vitality": 2
    },
    "price": 150
  },
  {
    "id": "ACC002",
    "name": "Iron Ring",
    "level": 3,
    "type": "Accessory",
    "stats": {
      "Strength": 6,
      "Agility": 3,
      "Intelligence": 0,
      "Vitality": 3
    },
    "price": 300
  },
  {
    "id": "ACC003",
    "name": "Steel Ring",
    "level": 4,
    "type": "Accessory",
    "stats": {
      "Strength": 8,
      "Agility": 4,
      "Intelligence": 0,
      "Vitality": 4
    },
    "price": 600
  }
]

def populate_equipment():
    db = Database()
    equipment_collection = db.get_equipment_collection()
    
    equipment_collection.insert_many(equipment_data)
    # print(f"Populated {len(monsters)} monsters")

if __name__ == "__main__":
    populate_equipment()