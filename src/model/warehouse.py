from src.model.piece import Piece
import copy

class Warehouse:
    __slots__ = ["original_inventory", "inventory", "_max_packed_value_density", "_unfulfilled_demand_area", "_mandatory_demand_area","_cached_hash"]

    def __init__(self, inventory, original_inventory, max_packed_value_density=None, unfulfilled_demand_area=None, mandatory_demand_area=None):
        self.inventory = inventory.copy() 
        self.original_inventory = original_inventory.copy()
        self._max_packed_value_density = self._get_max_packed_value_density() if max_packed_value_density is None else max_packed_value_density
        self._unfulfilled_demand_area = self._get_unfulfilled_demand_area() if unfulfilled_demand_area is None else unfulfilled_demand_area
        self._mandatory_demand_area = self._get_mandatory_demand_area() if mandatory_demand_area is None else mandatory_demand_area
        self._cached_hash = hash(frozenset(self.inventory.items()))

    def get_pieces(self):
        return self.inventory.keys()
    
    def get_original_pieces(self):
        return self.original_inventory.keys()
    
    def get_min_demand(self, piece):
        if piece not in self.original_inventory:
            return 0
        return self.original_inventory.get(piece)[0]
    
    def get_max_demand(self, piece):
        if piece not in self.original_inventory:
            return 0
        return self.original_inventory.get(piece)[2]
    
    def get_current_quantity(self, piece):
        if piece not in self.inventory:
            if piece in self.original_inventory:
                return self.get_max_demand(piece)
            return 0
        return self.inventory.get(piece)[1]
    
    def get_current_availability(self, piece):
        if piece not in self.inventory:
            return 0
        return self.get_max_demand(piece) - self.get_current_quantity(piece)
    
    def get_current_demand(self, piece):
        if piece not in self.inventory:
            return 0
        min_demand = self.get_min_demand(piece)
        current_quantity = self.get_current_quantity(piece)

        return max(0, min_demand - current_quantity)
    
    # Auxiliary function to calculate the maximum packed value density for the first time.
    def _get_max_packed_value_density(self):
        pieces = self.get_original_pieces()
        best_piece = max(pieces, key=lambda p : p.get_packed_value() / p.get_area())

        return best_piece.get_packed_value() / best_piece.get_area()
    
    def get_max_packed_value_density(self):
        return self._max_packed_value_density
    
    # Auxiliary function to calculate the unfulfilled demand area for the first time.
    def _get_unfulfilled_demand_area(self):
        unfulfilled_demand_area = 0
        
        for piece, values in self.inventory.items():
            # Get the information about the piece
            min_demand = values[0]
            current_quantity = values[1]
            current_demand = max(0, min_demand - current_quantity)

            # Calculate the unfulfilled demand area of the piece
            unfulfilled_demand_area += current_demand * piece.get_area()

        return unfulfilled_demand_area
    
    def get_unfulfilled_demand_area(self):
        return self._unfulfilled_demand_area
    
    def _get_mandatory_demand_area(self):
        mandatory_demand_area = 0
        
        for piece, values in self.original_inventory.items():
            # Get the information about the piece
            min_demand = values[0]

            # Calculate the mandatory demand area of the piece
            mandatory_demand_area += min_demand * piece.get_area()

        return mandatory_demand_area
    
    def get_mandatory_demand_area(self):
        return self._mandatory_demand_area

    def delete_piece(self, piece):
        if piece not in self.inventory:
            return self
        
        # Prepare the new inventories
        new_inventory = self.inventory.copy()
        # Update the state of the inventory
        new_inventory[piece] = (new_inventory[piece][0], 
                                new_inventory[piece][1] + 1,
                                new_inventory[piece][2])
        
        # Remove the piece from selection if its current quantity matches the maximum demand.
        if new_inventory[piece][1] == new_inventory[piece][2]:
            del new_inventory[piece]

        # Update the demand related values
        new_unfulfilled_demand_area = self.get_unfulfilled_demand_area() - min(self.get_current_demand(piece), 1) * piece.get_area()
            
        return Warehouse(inventory=new_inventory, 
            original_inventory=self.original_inventory, 
            max_packed_value_density=self.get_max_packed_value_density(),
            unfulfilled_demand_area=new_unfulfilled_demand_area,
            mandatory_demand_area=self.get_mandatory_demand_area()
        )
    
    @staticmethod
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
            if piece not in self.inventory:
                return False
            if warehouse.get_current_quantity(piece) > self.get_current_availability(piece):
                return False
            
        return True
    
    @staticmethod
    def warehouse_to_dict(warehouse):
        return {
            "inventory": [
                {"piece": Piece.piece_to_dict(piece), "values": values}
                for piece, values in warehouse.inventory.items()
            ],
            "original_inventory": [
                {"piece": Piece.piece_to_dict(piece), "values": values}
                for piece, values in warehouse.original_inventory.items()
            ],
            "max_packed_value_density": warehouse.get_max_packed_value_density(),
            "unfulfilled_demand_area": warehouse.get_unfulfilled_demand_area(),
            "mandatory_demand_area": warehouse.get_mandatory_demand_area()
        }

    @staticmethod
    def warehouse_from_dict(d):
        inventory = {}
        for entry in d["inventory"]:
            piece = Piece.piece_from_dict(entry["piece"])
            values = entry["values"]
            inventory[piece] = values

        original_inventory = {}
        for entry in d["original_inventory"]:
            piece = Piece.piece_from_dict(entry["piece"])
            values = entry["values"]
            original_inventory[piece] = values

        return Warehouse(inventory=inventory, 
            original_inventory=original_inventory,
            max_packed_value_density=d["max_packed_value_density"],
            unfulfilled_demand_area=d["unfulfilled_demand_area"],
            mandatory_demand_area=d["mandatory_demand_area"]
        )

    def __eq__(self, other):
        if not isinstance(other, Warehouse):
            return False
        if self._cached_hash != other._cached_hash:
            return False
        return self.inventory == other.inventory
    
    def __hash__(self):
        return self._cached_hash

    def __repr__(self):
        return f"Warehouse(Unique types: {len(self.inventory)})"