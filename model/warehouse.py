from model.piece import Piece

class Warehouse:
    def __init__(self):
        self.idx2piece = {}
        self.piece2idx = {}
        self.quantities = {}

    def add_piece(self, piece):
        p1 = Piece(piece.length, piece.width)
        p2 = Piece(piece.width, piece.length)

        idx = max(self.idx2piece, default=-1) + 1

        # Check if the piece exists
        if self.piece2idx.get(p1, -1) != -1:
            idx = self.piece2idx.get(p1)
        elif self.piece2idx.get(p2, -1) != -1:
            idx = self.piece2idx.get(p2)
        else: # If it is new
            self.idx2piece[idx] = p1
            self.piece2idx[p1] = idx
        
        self.quantities[idx] = self.quantities.get(idx, 0) + 1

    def delete_piece(self, piece):
        p1 = Piece(piece.length, piece.width)
        p2 = Piece(piece.width, piece.length)
        p = None
        idx = None

        # Check if the piece exists
        if self.piece2idx.get(p1, -1) != -1:
            idx = self.piece2idx.get(p1)
            p = p1
        elif self.piece2idx.get(p2, -1) != -1:
            idx = self.piece2idx.get(p2)
            p = p2

        # If the piece exists, we update the state of the warehouse
        if p is not None:
            self.quantities[idx] -= 1
            if self.quantities[idx] == 0:
                del self.idx2piece[idx]
                del self.piece2idx[p]
                del self.quantities[idx]

    def get_pieces(self):
        return self.idx2piece.values()
    
    def print_inventory(self):
        print("--- Warehouse Inventory ---")
        if not self.quantities:
            print("The warehouse is currently empty.")
        else:
            for idx, quantity in self.quantities.items():
                piece = self.idx2piece[idx]
                print(f"ID: {idx} | Dimensions: {piece.length}x{piece.width} | Quantity: {quantity}")
        print("---------------------------")
    
    def __eq__(self, other):
        if not isinstance(other, Warehouse):
            return False
        
        # We check if both warehouses have the same number of unique pieces
        if len(self.quantities) != len(other.quantities):
            return False

        # Compare piece by piece based on their physical properties, not their IDs
        for idx_self, qty_self in self.quantities.items():
            piece_self = self.idx2piece[idx_self]
            
            # Find the index of the same piece in the other warehouse
            # We look for it by the piece object itself (p1 or p2 logic inside piece2idx)
            idx_other = other.piece2idx.get(piece_self)
            
            if idx_other is None or other.quantities[idx_other] != qty_self:
                return False
                
        return True
    
    def __hash__(self):
        # We create a frozenset of (piece, quantity) pairs
        # Since pieces are normalized in Piece.__eq__, the hash will be consistent
        inventory_items = []
        for idx, qty in self.quantities.items():
            inventory_items.append((self.idx2piece[idx], qty))
            
        return hash(frozenset(inventory_items))
