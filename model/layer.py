import copy

class Layer:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.placements = []
    
    def get_covered_area(self):
        return sum(placement.get_piece().get_area() for placement in self.placements)
    
    def get_area(self):
        return self.width * self.length
    
    def get_filling_rate(self):
        total_area = self.get_area()
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

    def clone(self):
        new_layer = copy.copy(self)
        new_layer.placements = list(self.placements)

    def __eq__(self, other):
        if not isinstance(other, Layer):
            return False
        
        return (self.length == other.length and 
                self.width == other.width and 
                set(self.placements) == set(other.placements))
    
    def __hash__(self):
        return hash((self.length, self.width, frozenset(self.placements)))