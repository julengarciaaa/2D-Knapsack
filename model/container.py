import copy
from model.layer import Layer

class Container:
    __slots__ = ['length', 'width', 'current_length', 'layers', '_cached_hash']

    def __init__(self, length, width, current_length=0, layers=None):
        self.length = length
        self.width = width
        self.current_length = current_length
        self.layers = tuple(layers) if layers is not None else ()
        self._cached_hash = hash((self.length, self.width, self.layers))

    def get_length(self):
        return self.length

    def get_width(self):
        return self.width
    
    def get_current_length(self):
        return self.current_length
    
    def get_layers(self):
        return self.layers
    
    def get_area(self):
        # Total area of the container floor
        return self.width * self.length
    
    def get_covered_area(self):
        return sum(layer.get_covered_area() for layer in self.layers)

    def get_filling_rate(self):
        area = self.get_area()
        if area == 0: return 0
        return self.get_covered_area() / area
    
    def is_feasible_ldp(self, placement):
        p_length = placement.get_length()
        p_width = placement.get_width()

        available_length = self.length - self.current_length
        return p_length <= available_length and p_width <= self.width
    
    def can_add_layer(self, layer):
        length = layer.get_length()

        available_length = self.length - self.current_length
        return length <= available_length
    
    def get_available_length(self):
        return self.length - self.current_length
    
    def add_layer(self, layer):
        new_layers = self.layers + (layer,)
        # Each layer adds its length to the container's occupied length
        new_current_length = self.current_length + layer.get_length()
        
        return Container(
            self.length, 
            self.width, 
            current_length=new_current_length, 
            layers=new_layers
        )
    
    def container_to_dict(container):
        return {
            "length": container.length,
            "width": container.width,
            "current_length": container.current_length,
            "layers": [Layer.layer_to_dict(layer) for layer in container.layers]
        }

    def container_from_dict(d):
        layers = tuple(Layer.layer_from_dict(x) for x in d["layers"])
        return Container(
            length=d["length"],
            width=d["width"],
            current_length=d["current_length"],
            layers=layers
        )



    def __eq__(self, other):
        if not isinstance(other, Container):
            return False
        # Fast comparison using the cached hash
        if self._cached_hash != other._cached_hash:
            return False
        return (self.length == other.length and
                self.width == other.width and
                self.layers == other.layers)

    def __hash__(self):
        return self._cached_hash

    def __repr__(self):
        return f"Container({self.length}x{self.width}, Occupied: {self.current_length}, Layers: {len(self.layers)})"