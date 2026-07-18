import copy
import numpy as np
from collections import defaultdict
import portion as P
from src.model.placement import Placement

class Layer:
    __slots__ = ["length", "width", "placements", "p_points", "_grid", "_covered_area", "_packed_value", "_cached_hash"]

    def __init__(self, length, width, placements=None, grid=None, p_points=None, covered_area=0, packed_value=0):
        self.length = length
        self.width = width
        self.placements = placements if placements is not None else ()
        self._grid = grid if grid is not None else np.zeros((length, width), dtype=bool)
        self._covered_area = covered_area
        self._packed_value = packed_value

        # Store as tuple to ensure immutability
        self.p_points = p_points if p_points is not None else ((0, 0),)
        
        # Cache the hash because the state never changes
        self._cached_hash = hash((self.length, self.width, frozenset(self.placements)))

    def get_length(self):
        return self.length
    
    def get_width(self):
        return self.width
    
    def get_placements(self):
        return self.placements
    
    def get_p_points(self):
        return self.p_points
    
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
        x, y = placement.get_p_point()
        p_l, p_w = placement.get_length(), placement.get_width()

        # Update the placements
        new_placements = self.placements + (placement,)
        new_grid = self._grid.copy()
        new_grid[x : x + p_l, y : y + p_w] = True
        # Update the covered area
        new_covered_area = self._covered_area + piece.get_area()
        # Update the packed value
        new_packed_value = self._packed_value + piece.get_packed_value()

        # Calculate the new placing points
        active_points = [p for p in self.p_points if p != (x, y)]
        
        p1, p2 = (x, y + p_w), (x + p_l, y)
        # Check the existance of supports
        p1_has_v_support = p1[0] == 0 or (p1[1] < self.width and self._grid[p1[0] - 1, p1[1]])
        p2_has_h_support = p2[1] == 0 or (p2[0] < self.length and self._grid[p2[0], p2[1] - 1])

        # Check the conditions for being a rear left placement point
        if p1_has_v_support and p1 not in active_points:
            active_points.append(p1)

        # Check the conditions for being a front right placement point
        if p2_has_h_support and p2 not in active_points:
            active_points.append(p2)
        
        return Layer(self.length, 
            self.width, 
            placements=new_placements, 
            grid=new_grid,
            p_points=tuple(active_points),
            covered_area=new_covered_area, 
            packed_value=new_packed_value
        )
    
    def get_tp(self, placement):
        x, y = placement.get_p_point()
        p_w, p_l = placement.get_width(), placement.get_length()
        tp = 0

        # Left side (x - 1)
        if x == 0:
            tp += p_w  # Touches the left container wall
        else:
            tp += np.sum(self._grid[x - 1, y : y + p_w])

        # Bottom side (y - 1)
        if y == 0:
            tp += p_l  # Touches the container floor
        else:
            tp += np.sum(self._grid[x : x + p_l, y - 1])

        # Right side (x + p_l)
        if x + p_l == self.length:
            tp += p_w  # Touches the right container wall
        else:
            tp += np.sum(self._grid[x + p_l, y : y + p_w])

        # Top side (y + p_w)
        if y + p_w == self.width:
            tp += p_l  # Touches the container ceiling
        else:
            tp += np.sum(self._grid[x : x + p_l, y + p_w])
        
        return tp

    def is_feasible(self, placement):
        x, y = placement.get_p_point()
        p_l = placement.get_length()
        p_w = placement.get_width()

        # Layer boundary check
        if x < 0 or y < 0 or x + p_l > self.length or y + p_w > self.width:
            return False

        # Overlap check against existing placements
        return not np.any(self._grid[x : x + p_l, y : y + p_w])
    
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
        # Convert the tuple to a set to ignore the order of placements during comparison
        return (self.length == other.length and 
                self.width == other.width and 
                set(self.placements) == set(other.placements))
    
    def __hash__(self):
        return self._cached_hash

    def __repr__(self):
        return f"Layer({self.length}x{self.width}, Items: {len(self.placements)})"