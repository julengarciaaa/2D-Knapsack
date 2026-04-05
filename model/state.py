from model.placement import Placement
from model.layer import Layer

class State:
    def __init__(self, num_packed, packed_value, layer, pieces, p_points, placements):
        self.num_packed = num_packed    # Number of packed pieces
        self.packed_value = packed_value    # Total area/value packed
        self.layer = layer
        self.pieces = pieces  # Still free pieces
        self.p_points = p_points  # List of current active placing points
        self.placements = placements    # History of placements
        self.vertical_edges = None
        self.horizontal_edges = None

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
        
        # Initialize boundaries if this is the first piece in the layer
        if self.vertical_edges is None and self.horizontal_edges is None:
            # Vertical edges with the layer boundaries
            self.vertical_edges = [((0, 0), (0, layer.get_width())),
                                   ((layer.get_length(), 0), (layer.get_length(), layer.get_width()))]
            # Horizontal edges with the layer boundaries
            self.horizontal_edges = [((0, 0), (layer.get_length(), 0)),
                                     ((0, layer.get_width()), (layer.get_length(), layer.get_width()))]

        # Remove the used point from the list of available placing points
        new_p_points = [p_point for p_point in self.p_points if p_point != (x, y)]

        # Check that p1 has a vertical support
        px1, py1 = p_point1
        px2, py2 = p_point2
        p1_has_vertical_support = False
        p2_has_vertical_support = False

        for (v_x, v_y_start), (_, v_y_end) in self.vertical_edges:
            if v_x == px1 and min(v_y_start, v_y_end) <= py1 < max(v_y_start, v_y_end):
                p1_has_vertical_support = True

            if v_x == px2 and min(v_y_start, v_y_end) <= py2 <= max(v_y_start, v_y_end):
                p2_has_vertical_support = True
            
            if p1_has_vertical_support and p2_has_vertical_support:
                break

        # Check that p1 has not an horizontal support
        p1_has_horizontal_support = False
        p2_has_horizontal_support = False

        for (v_x_start, v_y), (v_x_end, _) in self.horizontal_edges:
            if v_y == py1 and min(v_x_start, v_x_end) <= px1 <= max(v_x_start, v_x_end):
                p1_has_horizontal_support = True
                break

            if v_y == py2 and min(v_x_start, v_x_end) <= px2 < max(v_x_start, v_x_end):
                p2_has_horizontal_support = True
                break

            if p1_has_horizontal_support and p2_has_horizontal_support:
                break

        if p1_has_vertical_support and not p1_has_horizontal_support and p_point1 not in new_p_points:
            new_p_points.append(p_point1)

        if p2_has_horizontal_support and not p2_has_vertical_support and p_point2 not in new_p_points:
            new_p_points.append(p_point2)
            

        # Update vertical edges by adding the new piece's edges
        self.vertical_edges.extend([
            ((x, y), (x, y + p_w)),   
            ((x + p_l, y), (x + p_l, y + p_w))
        ])

        # Update horizontal edges by adding the new piece's edges
        self.horizontal_edges.extend([
            ((x, y), (x + p_l, y)),
            ((x, y + p_w), (x + p_l, y + p_w)) 
        ])

        # Update state's properties
        self.num_packed += 1
        self.packed_value += piece.get_area()
        self.pieces.append(piece)
        self.p_points = new_p_points
        self.placements.append(placement)
            
        


