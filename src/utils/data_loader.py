import json
from src.model.piece import Piece
from src.model.warehouse import Warehouse
from src.model.layer import Layer

def load_warehouse_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    inventory = {}
    
    for item in data["Items"]:
        # Get the properties of the piece
        w = item.get("Length")
        h = item.get("Height")
        val = item.get("Value", 0)
        
        # Create the piece
        p = Piece(length=w, width=h, packed_value=val)
        
        # Demand's logic
        min_qty = item.get("Demand", 0)
        max_qty = item.get("DemandMax")
        
        # If the maximum demand is null, the maximum demand is the same as the minimum demand
        if max_qty is None:
            max_qty = float('inf')
            
        # If the piece already exists, update the inventory
        if p in inventory:
            prev_min, _, prev_max = inventory[p]
            inventory[p] = (prev_min + min_qty, 0, prev_max + max_qty)
        else:
            inventory[p] = (min_qty, 0, max_qty)
            
    return Warehouse(inventory)

def load_layer_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    length = data["Objects"][0].get("Length")
    width = data["Objects"][0].get("Height")


    return Layer(length, width)