from model.placement import Placement
from model.layer import Layer
import portion as P
from collections import defaultdict

class State:
    def __init__(self, layer, pieces):
        self.num_packed = 0    # Number of packed pieces
        self.packed_value = 0    # Total area
        self.layer = layer
        self.pieces = pieces  # Still free pieces
        self.p_points = [(0, 0)]  # List of current active placing points
        self.placements = []    # History of placements

        # Initialize the vertical edges' interval dictionary
        self.vertical_edges = defaultdict(lambda: P.empty())
        self.vertical_edges[0] = P.closedopen(0, layer.get_width())
        self.vertical_edges[layer.get_length()] = P.closedopen(0, layer.get_width())

        # Initialize the horizontal edges' interval dictionary
        self.horizontal_edges = defaultdict(lambda: P.empty())
        self.horizontal_edges[0] = P.closedopen(0, layer.get_length())
        self.horizontal_edges[layer.get_width()] = P.closedopen(0, layer.get_length())

    def get_layer(self):
        return self.layer
    
    def get_num_packed(self):
        return self.num_packed
    
    def get_packed_value(self):
        return self.packed_value
    
    def get_pieces(self):
        return self.pieces
    
    def get_p_points(self):
        return self.p_points
    
    def get_placements(self):
        return self.placements
    
    def commit_placement(self, placement):
        # Extract coordinates and properties from the placement object
        x, y = placement.get_p_point()
        piece = placement.get_piece()
        layer = self.layer

        # Dimensions of the current piece being placed
        p_w = piece.get_width()
        p_l = piece.get_length()

        # Initial candidate placement points based on the new piece's corners
        p_point1 = (x, y + p_w) # Rear left point
        p_point2 = (x + p_l, y) # Front right point

        # Remove the used point from the list of available placing points
        new_p_points = [p_point for p_point in self.p_points if p_point != (x, y)]

        px1, py1 = p_point1
        px2, py2 = p_point2

        # Check the existance of vertical supports
        p1_has_vertical_support = py1 in self.vertical_edges[px1]
        p2_has_vertical_support = py2 in self.vertical_edges[px2]

        # Check the existance of horizontal supports
        p1_has_horizontal_support = px1 in self.horizontal_edges[py1]
        p2_has_horizontal_support = px2 in self.horizontal_edges[py2]

        # Check the conditions for being a rear left placement point
        if p1_has_vertical_support and not p1_has_horizontal_support and p_point1 not in new_p_points:
            new_p_points.append(p_point1)

        # Check the conditions for being a front right placement point
        if p2_has_horizontal_support and not p2_has_vertical_support and p_point2 not in new_p_points:
            new_p_points.append(p_point2)

        # Update vertical edges by adding the new piece's edges
        self.vertical_edges[x] = self.vertical_edges[x] | P.closedopen(y, y + p_w)
        self.vertical_edges[x + p_l] = self.vertical_edges[x + p_l] | P.closedopen(y, y + p_w)

        # Update horizontal edges by adding the new piece's edges
        self.horizontal_edges[y] = self.horizontal_edges[y] | P.closedopen(x, x + p_l)
        self.horizontal_edges[y + p_w] = self.horizontal_edges[y + p_w] | P.closedopen(x, x + p_l)

        # Update state's properties
        self.num_packed += 1
        self.packed_value += piece.get_area()
        self.pieces.append(piece)
        self.p_points = new_p_points
        self.placements.append(placement)
            
        


