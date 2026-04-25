import portion as P
from collections import defaultdict

class LayerState:
    def __init__(self, layer, warehouse, num_packed=0, packed_value=0, p_points=None, vertical_edges=None, horizontal_edges=None):
        self.num_packed = num_packed    # Number of packed pieces
        self.packed_value = packed_value    # Total area
        self.layer = layer
        self.warehouse = warehouse  # State of the pieces' stock
        self.p_points = list(p_points) if p_points is not None else [(0, 0)] # List of current active placing points

        
        # Initialize the vertical edges' interval dictionary
        if vertical_edges is None:
            self.vertical_edges = defaultdict(lambda: P.empty())
            self.vertical_edges[0] = P.closedopen(0, layer.get_width())
            self.vertical_edges[layer.get_length()] = P.closedopen(0, layer.get_width())
        else:
            self.vertical_edges = vertical_edges.copy()

        # Initialize the horizontal edges' interval dictionary
        if horizontal_edges is None:
            self.horizontal_edges = defaultdict(lambda: P.empty())
            self.horizontal_edges[0] = P.closedopen(0, layer.get_length())
            self.horizontal_edges[layer.get_width()] = P.closedopen(0, layer.get_length())
        else:
            self.horizontal_edges = horizontal_edges.copy()

    def get_layer(self):
        return self.layer
    
    def get_num_packed(self):
        return self.num_packed
    
    def get_packed_value(self):
        return self.packed_value
    
    def get_warehouse(self):
        return self.warehouse
    
    def get_p_points(self):
        return self.p_points
    
    def get_placements(self):
        return self.placements
    
    def is_feasible(self, placement):
        x, y = placement.get_p_point()
        piece = placement.get_piece()
        p_w = placement.get_width()
        p_l = placement.get_length()

        # Boundary Check
        if x < 0 or y < 0:
            return False
        if x + p_l > self.layer.get_length():
            return False
        if y + p_w > self.layer.get_width():
            return False

        # Overlap Check
        # Using AABB (Axis-Aligned Bounding Box) intersection
        for placed in self.layer.get_placements():
            px, py = placed.get_p_point()
            pp_w = placed.get_width()
            pp_l = placed.get_length()

            # If these 4 conditions are met simultaneously, the rectangles overlap
            if (x < px + pp_l and
                x + p_l > px and
                y < py + pp_w and
                y + p_w > py):
                return False 

        return True
    
    def commit_placement(self, placement):
        import copy

        # Extract coordinates and properties from the placement object
        x, y = placement.get_p_point()
        piece = placement.get_piece()
        p_w = placement.get_width()
        p_l = placement.get_length()
        
        # Deep copy the interval dictionaries to avoid modifying the original state
        new_vertical_edges = self.vertical_edges.copy()
        new_horizontal_edges = self.horizontal_edges.copy()
        new_layer = copy.copy(self.layer)
        new_layer.placements = list(self.layer.placements)
        
        # Initial candidate placement points based on the new piece's corners
        p_point1 = (x, y + p_w) # Rear left point
        p_point2 = (x + p_l, y) # Front right point

        # Remove the used point from the list of available placing points
        new_p_points = [p_point for p_point in self.p_points if p_point != (x, y)]

        px1, py1 = p_point1
        px2, py2 = p_point2

        # Check the existance of vertical supports
        p1_has_vertical_support = py1 in new_vertical_edges[x]
        p2_has_vertical_support = py2 in new_vertical_edges[x + p_l]

        # Check the existance of horizontal supports
        p1_has_horizontal_support = px1 in new_horizontal_edges[y + p_w]
        p2_has_horizontal_support = px2 in new_horizontal_edges[y]

        # Check the conditions for being a rear left placement point
        if p1_has_vertical_support and not p1_has_horizontal_support and p_point1 not in new_p_points:
            new_p_points.append(p_point1)

        # Check the conditions for being a front right placement point
        if p2_has_horizontal_support and not p2_has_vertical_support and p_point2 not in new_p_points:
            new_p_points.append(p_point2)

        # Update vertical edges by adding the new piece's edges
        new_vertical_edges[x] = new_vertical_edges[x] | P.closedopen(y, y + p_w)
        new_vertical_edges[x + p_l] = new_vertical_edges[x + p_l] | P.closedopen(y, y + p_w)

        # Update horizontal edges by adding the new piece's edges
        new_horizontal_edges[y] = new_horizontal_edges[y] | P.closedopen(x, x + p_l)
        new_horizontal_edges[y + p_w] = new_horizontal_edges[y + p_w] | P.closedopen(x, x + p_l)

        # Update state's properties
        new_num_packed = self.num_packed + 1
        new_packed_value = self.packed_value + piece.get_area()
        # Create a new warehouse without the placed piece
        new_warehouse = copy.deepcopy(self.warehouse)
        new_warehouse.delete_piece(piece)
        # Update placements
        new_layer.add_placement(placement)

        new_state = LayerState(new_layer, 
                               new_warehouse, 
                               new_num_packed, 
                               new_packed_value, 
                               new_p_points,
                               new_vertical_edges, 
                               new_horizontal_edges)

        return new_state

    def get_interval_length(self, intervals):
        if intervals.empty:
            return 0
        return sum(i.upper - i.lower for i in intervals)

    def get_tp(self, placement):
        x, y = placement.get_p_point()
        
        # Piece's dimensions
        p_w = placement.get_width()
        p_l = placement.get_length()

        tp = 0

        bottom_segment = P.closedopen(x, x + p_l)
        contact_bottom = bottom_segment & self.horizontal_edges[y]
        tp += self.get_interval_length(contact_bottom)

        left_segment = P.closedopen(y, y + p_w)
        contact_left = left_segment & self.vertical_edges[x]
        tp += self.get_interval_length(contact_left)

        top_segment = P.closedopen(x, x + p_l)
        contact_top = top_segment & self.horizontal_edges[y + p_w]
        tp += self.get_interval_length(contact_top)

        right_segment = P.closedopen(y, y + p_w)
        contact_right = right_segment & self.vertical_edges[x + p_l]
        tp += self.get_interval_length(contact_right)

        return tp
    
    def _get_signature(self):
        return frozenset(self.layer.get_placements())

    def __eq__(self, other):
        if not isinstance(other, LayerState):
            return False
        return self._get_signature() == other._get_signature()

    def __hash__(self):
        return hash(self._get_signature())
        


