import copy

class Piece:
    __slots__ = ["length", "width", "packed_value", "_cached_hash"]

    def __init__(self, length, width, packed_value):
        self.length = length
        self.width = width
        self.packed_value = packed_value

        # Cache the hash because the state never changes
        dimensions = (min(self.length, self.width), max(self.length, self.width))
        self._cached_hash = hash((dimensions, self.packed_value))
    
    def get_length(self):
        return self.length
        
    def get_width(self):
        return self.width
    
    def get_area(self):
        return self.length * self.width
    
    def get_packed_value(self):
        return self.packed_value
    
    def clone(self):
        return copy.copy(self)
    
    @staticmethod
    def piece_to_dict(piece):
        return {
            "length": piece.length,
            "width": piece.width,
            "packed_value": piece.packed_value
        }

    @staticmethod
    def piece_from_dict(d):
        return Piece(
            length=d["length"],
            width=d["width"],
            packed_value=d["packed_value"]
        )

    
    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        
        return ((self.length == other.length and self.width == other.width or
                self.length == other.width and self.width == other.length) and 
                self.packed_value == other.packed_value)
    
    def __hash__(self):
        return self._cached_hash

    def __repr__(self):
        return f"Piece({self.length}x{self.width})"