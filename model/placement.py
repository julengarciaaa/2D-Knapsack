import copy

class Placement:
    __slots__ = ['piece', 'p_point', '_is_rotated']

    def __init__(self, piece, is_rotated, p_point):
        self.piece = piece
        self._is_rotated = is_rotated
        self.p_point = p_point

    def get_piece(self):
        return self.piece
    
    def get_p_point(self):
        return self.p_point
    
    def get_width(self):
        return self.piece.get_length() if self._is_rotated else self.piece.get_width()
        
    def get_length(self):
        return self.piece.get_width() if self._is_rotated else self.piece.get_length()
        
    def is_rotated(self):
        return self._is_rotated
    
    def clone(self):
        return copy.copy(self)

    def __eq__(self, other):
        if not isinstance(other, Placement):
            return False
        
        return (self.piece == other.piece and 
                self._is_rotated == other._is_rotated and 
                self.p_point == other.p_point)

    def __hash__(self):
        return hash((self.piece, self._is_rotated, self.p_point))

    def __repr__(self):
        rot = "Rotated" if self._is_rotated else "Normal"
        return f"Placement({self.piece} at {self.p_point}, {rot})"