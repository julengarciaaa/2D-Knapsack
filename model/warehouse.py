class Warehouse:
    __slots__ = ['inventory', '_cached_hash']

    def __init__(self, inventory=None):
        self.inventory = inventory if inventory is not None else {}
        self._cached_hash = hash(frozenset(self.inventory.items()))

    def get_pieces(self):
        return self.inventory.keys()
    
    def get_num_pieces(self):
        return sum(self.inventory.values())

    def add_piece(self, piece, qty=1):
        new_inventory = self.inventory.copy()
        new_inventory[piece] = new_inventory.get(piece, 0) + qty
        
        return Warehouse(new_inventory)

    def delete_piece(self, piece):
        if piece not in self.inventory:
            return self
            
        new_inventory = self.inventory.copy()
        new_inventory[piece] -= 1
        
        # If count reaches zero delete the piece from the inventory
        if new_inventory[piece] <= 0:
            del new_inventory[piece]
            
        return Warehouse(new_inventory)

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