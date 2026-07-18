import copy
from src.model.piece import Piece

class Placement:
    __slots__ = ["piece", "p_point", "_is_rotated", "_cached_hash"]

    def __init__(self, piece, is_rotated, p_point):
        self.piece = piece
        self._is_rotated = is_rotated
        self.p_point = p_point

        # Cache the hash because the state never changes
        self._cached_hash = hash((self.piece, self._is_rotated, self.p_point))
    def get_piece(self):
        return self.piece
    
    def get_p_point(self):
        return self.p_point
    
    def get_width(self):
        return self.piece.get_length() if self._is_rotated else self.piece.get_width()
        
    def get_length(self):
        return self.piece.get_width() if self._is_rotated else self.piece.get_length()
        
    def get_area(self):
        return self.get_length() * self.get_width()

    def is_rotated(self):
        return self._is_rotated
    
    def clone(self):
        return copy.copy(self)
    
    def placement_to_dict(pl):
        return {
            "piece": Piece.piece_to_dict(pl.piece),
            "p_point": tuple(pl.p_point),
            "is_rotated": pl._is_rotated
        }
    
    def placement_from_dict(d):
        piece = Piece.piece_from_dict(d["piece"])
        p_point = tuple(d["p_point"])
        is_rotated = d["is_rotated"]
        return Placement(piece, is_rotated, p_point)

    def __eq__(self, other):
        if not isinstance(other, Placement):
            return False
        
        return (self.piece == other.piece and 
                self._is_rotated == other._is_rotated and 
                self.p_point == other.p_point)

    def __hash__(self):
        return self._cached_hash

    def __repr__(self):
        rot = "Rotated" if self._is_rotated else "Normal"
        return f"Placement({self.piece} at {self.p_point}, {rot})"