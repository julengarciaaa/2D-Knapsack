from model.layer import Layer

class Placement:
    def __init__(self, piece, orientation, p_point):
        self.piece = piece
        self.orientation = orientation
        self.p_point = p_point  # Placing point

    def get_piece(self):
        return self.piece
    
    def get_orientation(self):
        return self.orientation
    
    def get_p_point(self):
        return self.p_point
    
