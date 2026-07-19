import copy
from src.model.placement import Placement

class Layer:
    __slots__ = ["length", "width", "placements", "_covered_area", "_packed_value", "_cached_hash"]

    def __init__(self, length, width, placements=None, covered_area=0, packed_value=0):
        self.length = length
        self.width = width
        self.placements = tuple(placements) if placements is not None else ()
        self._covered_area = covered_area
        self._packed_value = packed_value

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
        return self._covered_area
    
    def get_filling_rate(self):
        total_area = self.get_area()
        covered_area = self.get_covered_area()

        if total_area == 0 or not self.placements:
            return 0
        return covered_area / total_area
    
    def get_packed_value(self):
        return self._packed_value
    
    def get_num_placements(self):
        return len(self.placements)
    
    def commit_placement(self, placement):
        piece = placement.get_piece()
        # Update the placements
        new_placements = self.placements + (placement,)
        # Update the covered area
        new_covered_area = self._covered_area + piece.get_area()
        # Update the packed value
        new_packed_value = self._packed_value + piece.get_packed_value()
        
        return Layer(self.length, 
            self.width, 
            placements=new_placements, 
            covered_area=new_covered_area, 
            packed_value=new_packed_value
        )

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
    
    @staticmethod
    def layer_to_dict(layer):
        return {
            "length": layer.get_length(),
            "width": layer.get_width(),
            "placements": [Placement.placement_to_dict(p) for p in layer.placements],
            "covered_area": layer.get_covered_area(),
            "packed_value": layer.get_packed_value()
        }

    @staticmethod
    def layer_from_dict(d):
        placements = tuple(Placement.placement_from_dict(p) for p in d["placements"])
        return Layer(
            length=d["length"],
            width=d["width"],
            placements=placements,
            covered_area=d["covered_area"],
            packed_value=d["packed_value"]
        )

    def __eq__(self, other):
        if not isinstance(other, Layer):
            return False
        # Since placements is a tuple, we can compare directly
        return (self.length == other.length and 
                self.width == other.width and 
                set(self.placements) == set(other.placements))
    
    def __hash__(self):
        return self._cached_hash

    def __repr__(self):
        return f"Layer({self.length}x{self.width}, Items: {len(self.placements)})"