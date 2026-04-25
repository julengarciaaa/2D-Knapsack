import copy

class Piece:
    __slots__ = ['length', 'width', 'packed_value']

    def __init__(self, length, width, packed_value=None):
        self.length = length
        self.width = width
        self.packed_value = packed_value if packed_value is not None else length * width
    
    def get_length(self):
        return self.length
        
    def get_width(self):
        return self.width
    
    def get_packed_value(self):
        return self.packed_value
        
    def get_area(self):
        return self.length * self.width
    
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
        dimensions = (min(self.length, self.width), max(self.length, self.width))
        return hash((dimensions, self.packed_value))

    def __repr__(self):
        return f"Piece({self.length}x{self.width})"