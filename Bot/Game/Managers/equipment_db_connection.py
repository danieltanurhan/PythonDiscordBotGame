from Game.Database.database import Database

db = Database()
equipment_collection = db.get_equipment_collection()

def get_equipment_by_id(equipment_id: str) -> dict:
    equipment_data = equipment_collection.find_one({"id": equipment_id})
    return equipment_data

def get_equipment_by_type(equipment_type: str) -> list:
    equipment_data = equipment_collection.find({"type": equipment_type})
    return [equipment for equipment in equipment_data]

