from src.model.piece import Piece
import copy

class Warehouse:
    __slots__ = ["original_inventory", "inventory", "_max_value_density", "_cached_hash"]

    def __init__(self, inventory, original_inventory, max_value_density=None):
        self.inventory = inventory.copy() 
        self.original_inventory = original_inventory.copy()
        self._max_value_density = self._get_max_packed_value_density() if max_value_density is None else max_value_density
        self._cached_hash = hash(frozenset(self.inventory.items()))

    def get_pieces(self):
        return self.inventory.keys()
    
    def get_original_pieces(self):
        return self.original_inventory.keys()
    
    def get_min_demand(self, piece):
        return self.inventory.get(piece)[0]
    
    def get_max_demand(self, piece):
        return self.inventory.get(piece)[2]
    
    def get_current_cuantity(self, piece):
        return self.inventory.get(piece)[1]
    
    def get_current_availability(self, piece):
        return self.get_max_demand(piece) - self.get_current_cuantity(piece)
    
    def _get_max_packed_value_density(self):
        pieces = self.get_original_pieces()
        best_piece = max(pieces, key=lambda p : p.get_packed_value() / p.get_area())

        return best_piece.get_packed_value() / best_piece.get_area()
    
    def get_max_packed_value_density(self):
        return self._get_max_packed_value_density()

    def delete_piece(self, piece):
        if piece not in self.inventory:
            return self
        
        # Prepare the new inventories
        new_inventory = self.inventory.copy()
        new_original_inventory = self.original_inventory.copy()
        # Update the state of the inventory
        new_inventory[piece] = (new_inventory[piece][0], 
                                new_inventory[piece][1] + 1,
                                new_inventory[piece][2])
        
        # Remove the piece from selection if its current quantity matches the maximum demand.
        if new_inventory[piece][1] == new_inventory[piece][2]:
            del new_inventory[piece]
            
        return Warehouse(inventory=new_inventory, original_inventory=new_original_inventory, max_value_density=self._max_value_density)
    
    def warehouse_from_placements(placements):
        inventory = {}
        for pl in placements:
            piece = pl.get_piece()
            inventory[piece] = (0, 
                                inventory.get(piece, (0, 0))[1] + 1, 
                                inventory.get(piece, (0, 0))[1] + 1)

        return Warehouse(inventory=inventory, original_inventory=inventory.copy())

    def can_fulfill(self, warehouse):
        pieces = warehouse.get_pieces()

        for piece in pieces:
            if warehouse.get_current_quantity(piece) > self.get_current_availability(piece):
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

        return Warehouse(inventory=inventory, original_inventory=inventory.copy())

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