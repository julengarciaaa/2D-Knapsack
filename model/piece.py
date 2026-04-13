import copy

class Piece:
    __slots__ = ['length', 'width']

    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    def get_length(self):
        return self.length
        
    def get_width(self):
        return self.width
        
    def get_area(self):
        return self.length * self.width
    
    def clone(self):
        return copy.copy(self)
    
    def piece_to_dict(piece):
        return {
            "length": piece.length,
            "width": piece.width
        }

    def piece_from_dict(d):
        return Piece(
            length=d["length"],
            width=d["width"]
        )

    
    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        
        return (self.length == other.length and self.width == other.width or
                self.length == other.width and self.width == other.length)
    
    def __hash__(self):
        dimensions = (min(self.length, self.width), max(self.length, self.width))
        return hash(dimensions)

    def __repr__(self):
        return f"Piece({self.length}x{self.width})"