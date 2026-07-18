import copy
from src.model.placement import Placement

class Layer:
    __slots__ = ["length", "width", "placements", "_cached_hash"]

    def __init__(self, length, width, placements=None):
        self.length = length
        self.width = width
        self.placements = tuple(placements) if placements is not None else ()

        # Cache the hash because the state never changes
        self._cached_hash = hash((self.length, self.width, frozenset(self.placements)))

    def get_length(self):
        return self.length
    
    def get_width(self):
         return self.width
    
    def get_placements(self):
        return self.placements
    
    def get_area(self):
        return self.width * self.length
    
    def get_covered_area(self):
        return sum(p.get_piece().get_area() for p in self.placements)
    
    def get_filling_rate(self):
        total_area = self.get_area()
        covered_area = self.get_covered_area()

        if total_area == 0 or not self.placements:
            return 0
        return covered_area / total_area
    
    def get_packed_value(self):
        packed_value = 0
        for pl in self.placements:
            piece = pl.get_piece()
            packed_value += piece.get_packed_value()

        return packed_value
    
    def get_num_placements(self):
        return len(self.placements)
    
    def commit_placement(self, placement):
        new_placements = self.placements + (placement,)
        
        return Layer(self.length, self.width, new_placements)

    def is_feasible(self, placement):
        x, y = placement.get_p_point()
        p_l = placement.get_length()
        p_w = placement.get_width()

        # Layer boundary check
        if x < 0 or y < 0 or x + p_l > self.length or y + p_w > self.width:
            return False

        # Overlap check against existing placements
        for pl in self.placements:
            px, py = pl.get_p_point()
            pp_l, pp_w = pl.get_length(), pl.get_width()

            # Collision detected if all 4 conditions are true
            if (x < px + pp_l and
                x + p_l > px and
                y < py + pp_w and
                y + p_w > py):
                return False 

        return True
    
    def layer_to_dict(layer):
        return {
            "length": layer.length,
            "width": layer.width,
            "placements": [Placement.placement_to_dict(p) for p in layer.placements]
        }

    def layer_from_dict(d):
        placements = tuple(Placement.placement_from_dict(p) for p in d["placements"])
        return Layer(
            length=d["length"],
            width=d["width"],
            placements=placements
        )


    def __eq__(self, other):
        if not isinstance(other, Layer):
            return False
        # Since placements is a tuple, we can compare directly
        return (self.length == other.length and 
                self.width == other.width and 
                self.placements == other.placements)
    
    def __hash__(self):
        # Immutability makes hashing very fast and reliable
        return self._cached_hash

    def __repr__(self):
        return f"Layer({self.length}x{self.width}, Items: {len(self.placements)})"