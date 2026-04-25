from src.model.piece import Piece
import copy

class Warehouse:
    __slots__ = ['original_inventory', 'inventory', '_cached_hash']

    def __init__(self, inventory=None, original_inventory=None):
        self.inventory = inventory.copy() if inventory is not None else {}
        self.original_inventory = original_inventory.copy() if original_inventory is not None else inventory.copy() if inventory is not None else {}
        self._cached_hash = hash(frozenset(self.inventory.items()))

    def get_pieces(self):
        return self.inventory.keys()
    
    def get_max_demand(self, piece):
        return self.inventory.get(piece)[1]
    
    def get_demand(self, piece):
        return self.inventory.get(piece)[0]

    def delete_piece(self, piece):
        if piece not in self.inventory:
            return self
            
        new_inventory = self.inventory.copy()
        new_original_inventory = self.original_inventory.copy()
        new_inventory[piece] = (max(0, new_inventory[piece][0] - 1), new_inventory[piece][1] - 1)
        
        # If count reaches zero delete the piece from the inventory
        if new_inventory[piece][1] <= 0:
            del new_inventory[piece]
            
        return Warehouse(inventory=new_inventory, original_inventory=new_original_inventory)
    
    def warehouse_from_placements(placements):
        inventory = {}
        for pl in placements:
            piece = pl.get_piece()
            inventory[piece] = (1, inventory.get(piece, (0, 0))[1] + 1)

        return Warehouse(inventory)

    def can_fulfill(self, warehouse):
        pieces = warehouse.get_pieces()

        for piece in pieces:
            if warehouse.get_max_demand(piece) > self.get_max_demand(piece):
                return False
            
        return True
    
    def warehouse_to_dict(warehouse):
        return {
            "inventory": [
                {"piece": Piece.piece_to_dict(piece), "values": values}
                for piece, values in warehouse.inventory.items()
            ]
        }

    def warehouse_from_dict(d):
        inventory = {}
        for entry in d["inventory"]:
            piece = Piece.piece_from_dict(entry["piece"])
            values = entry["values"]
            inventory[piece] = values
        return Warehouse(inventory)



    def __eq__(self, other):
        if not isinstance(other, Warehouse):
            return False
        if self._cached_hash != other._cached_hash:
            return False
        return self.inventory == other.inventory
    
    def __hash__(self):
        return self._cached_hash

    def __repr__(self):
        return f"Warehouse(Unique types: {len(self.inventory)}, Total: {self.get_num_pieces()})"