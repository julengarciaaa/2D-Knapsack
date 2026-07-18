import copy
from collections import defaultdict
import portion as P
from src.model.placement import Placement

class Layer:
    __slots__ = ["length", "width", "placements", "p_points", "vertical_edges", "horizontal_edges", "_covered_area", "_packed_value", "_cached_hash"]

    def __init__(self, length, width, placements=None, p_points=None, vertical_edges=None, horizontal_edges=None, covered_area=0, packed_value=0):
        self.length = length
        self.width = width
        self.placements = placements if placements is not None else ()
        self._covered_area = covered_area
        self._packed_value = packed_value

        # Store as tuple to ensure immutability
        self.p_points = p_points if p_points is not None else ((0, 0),)

        # Initialize or copy edge dictionaries
        if vertical_edges is None:
            self.vertical_edges = defaultdict(lambda: P.empty())
            self.vertical_edges[0] = P.closedopen(0, self.width)
            self.vertical_edges[self.length] = P.closedopen(0, self.width)
        else:
            self.vertical_edges = vertical_edges

        if horizontal_edges is None:
            self.horizontal_edges = defaultdict(lambda: P.empty())
            self.horizontal_edges[0] = P.closedopen(0, self.length)
            self.horizontal_edges[self.width] = P.closedopen(0, self.length)
        else:
            self.horizontal_edges = horizontal_edges
        
        # Cache the hash because the state never changes
        self._cached_hash = hash(frozenset(self.get_placements()))

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
        # Update the placements
        new_placements = self.placements + (placement,)
        # Update the covered area
        new_covered_area = self._covered_area + piece.get_area()
        # Update the packed value
        new_packed_value = self._packed_value + piece.get_packed_value()

        x, y = placement.get_p_point()
        p_l, p_w = placement.get_length(), placement.get_width()

        # Update edges (creating fresh copies for the new state)
        new_v_edges = self.vertical_edges.copy()
        new_h_edges = self.horizontal_edges.copy()

        # Calculate the new placing points
        active_points = [p for p in self.p_points if p != (x, y)]
        
        p1, p2 = (x, y + p_w), (x + p_l, y)
        # Check the existance of supports
        p1_has_v_support = p1[1] in new_v_edges[p1[0]]
        p2_has_v_support = p2[1] in new_v_edges[p2[0]]
        p1_has_h_support = p1[0] in new_h_edges[p1[1]]
        p2_has_h_support = p2[0] in new_h_edges[p2[1]]

        # Check the conditions for being a rear left placement point
        if p1_has_v_support and not p1_has_h_support and p1 not in active_points:
            active_points.append(p1)

        # Check the conditions for being a front right placement point
        if p2_has_h_support and not p2_has_v_support and p2 not in active_points:
            active_points.append(p2)


        new_v_edges[x] |= P.closedopen(y, y + p_w)
        new_v_edges[x + p_l] |= P.closedopen(y, y + p_w)
        new_h_edges[y] |= P.closedopen(x, x + p_l)
        new_h_edges[y + p_w] |= P.closedopen(x, x + p_l)
        
        return Layer(self.length, 
            self.width, 
            placements=new_placements, 
            p_points=tuple(active_points),
            vertical_edges=new_v_edges,
            horizontal_edges=new_h_edges,
            covered_area=new_covered_area, 
            packed_value=new_packed_value
        )
    
    def get_tp(self, placement):
        x, y = placement.get_p_point()
        p_w, p_l = placement.get_width(), placement.get_length()
        tp = 0

        # Calculate interval intersections
        tp += self._measure(P.closedopen(x, x + p_l) & self.horizontal_edges[y])
        tp += self._measure(P.closedopen(y, y + p_w) & self.vertical_edges[x])
        tp += self._measure(P.closedopen(x, x + p_l) & self.horizontal_edges[y + p_w])
        tp += self._measure(P.closedopen(y, y + p_w) & self.vertical_edges[x + p_l])
        
        return tp
    
    def _measure(self, interval):
        return sum(i.upper - i.lower for i in interval) if not interval.empty else 0

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
        # Convert the tuple to a set to ignore the order of placements during comparison
        return (self.length == other.length and 
                self.width == other.width and 
                set(self.placements) == set(other.placements))
    
    def __hash__(self):
        return hash((self.length, self.width, self.placements))

    def __repr__(self):
        return f"Layer({self.length}x{self.width}, Items: {len(self.placements)})"