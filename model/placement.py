class Placement:
    def __init__(self, piece, is_rotated, p_point):
        self.piece = piece
        self._is_rotated = is_rotated
        self.p_point = p_point

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

    def __eq__(self, other):
        # 2 placements are the same if they consist of the same piece, same rotation and same placemente point.
        if not isinstance(other, Placement):
            return False
        return (self.piece == other.piece and 
                self._is_rotated == other._is_rotated and 
                self.p_point == other.p_point)

    def __hash__(self):
        return hash((self.piece, self._is_rotated, self.p_point))    
    
