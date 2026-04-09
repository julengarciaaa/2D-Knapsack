# from model.state import State

class Layer:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.placements = []
    
    def get_covered_area(self):
        return sum(placement.get_piece().get_area() for placement in self.placements)
    
    def get_filling_rate(self):
        total_area = self.length * self.width
        if total_area == 0 or not self.placements:
            return 0
        return self.get_covered_area() / total_area
    
    def get_length(self):
        return self.length
    
    def get_width(self):
         return self.width
    
    def get_placements(self):
        return self.placements
    
    def get_num_placements(self):
        return len(self.placements)
    
    def add_placement(self, placement):
        self.placements.append(placement)

    def __eq__(self, other):
        # Check if the other object is a Layer
        if not isinstance(other, Layer):
            return False
        
        # Two layers are equal if they have the same dimensions and placements
        return (self.length == other.length and 
                self.width == other.width and 
                set(self.placements) == set(other.placements))
    
    def __hash__(self):
        # We hash the dimensions and a frozenset of placements
        return hash((self.length, self.width, frozenset(self.placements)))



