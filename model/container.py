class Container:

    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.layers = []
        self.next_layer_start = 0

    def get_width(self):
        return self.width
    
    def get_length(self):
        return self.length
    
    def get_layers(self):
        return self.layers
    
    def is_feasible_ldp(self, placement):
        return placement.get_length() <= self.length - self.next_layer_start and placement.get_width() <= self.width
    
    def add_layer(self, layer):
        self.layers.append(layer)
        self.next_layer_start += layer.get_length()

    def get_covered_area(self):
        covered_area = 0
        for layer in self.layers:
            covered_area += layer.get_covered_area()

        return covered_area
    
    def get_area(self):
        return self.width * self.length

    def get_filling_rate(self):
        area = self.get_area()
        covered_area = self.get_covered_area()

        return covered_area / area
    
    def __eq__(self, other):
        if not isinstance(other, Container):
            return False
        
        # We do not care if the layers are in different order
        # but they have the same pieces.
        return (self.length == other.length and
                self.width == other.width and
                set(self.layers) == set(other.layers))

    def __hash__(self):
        return hash((self.length, self.width, frozenset(self.layers)))