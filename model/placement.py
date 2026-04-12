import copy

class Placement:
    def __init__(self, piece, p_point, is_rotated):
        self.piece = piece
        self.p_point = p_point
        self._is_rotated = is_rotated

    def get_piece(self):
        return self.piece
    
    def get_p_point(self):
        return self.p_point
    
    def get_width(self):
        if self._is_rotated:
            return self.piece.get_length()
        else:
            return self.piece.get_width()
        
    def get_length(self):
        if self._is_rotated:
            return self.piece.get_width()
        else:
            return self.piece.get_length()
        
    def is_rotated(self):
        return self._is_rotated
    
    def clone(self):
        new_placement = copy.copy(self)
        new_placement.piece = self.piece

    def __eq__(self, other):
        if not isinstance(other, Placement):
            return False
        return (self.piece == other.piece and 
                self._is_rotated == other._is_rotated and 
                self.p_point == other.p_point)

    def __hash__(self):
        return hash((self.piece, self._is_rotated, self.p_point))    
    
