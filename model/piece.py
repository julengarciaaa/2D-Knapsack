class Piece:
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    def get_length(self):
        return self.length
        
    def get_width(self):
        return self.width
        
    def get_area(self):
        return self.length * self.width
    
    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return (self.length == other.length and self.width == other.width or
                self.length == other.width and self.width == other.length)
    
    def __hash__(self):
        # We normalize dimensions.
        dimensions = (min(self.length, self.width), max(self.length, self.width))
        return hash(dimensions)