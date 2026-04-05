class Layer:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.pieces = []
    
    def get_covered_area(self):
        return sum(piece.get_area() for piece in self.pieces)
    
    def get_filling_rate(self):
        total_area = self.length * self.width
        if total_area == 0 or not self.pieces:
            return 0
        return self.get_covered_area() / total_area
    
    def get_length(self):
        return self.length
    
    def get_width(self):
         return self.width
    
    def get_pieces(self):
        return self.pieces
    
    def get_num_pieces(self):
        return len(self.pieces)
    
    def fill_layer_ng(self, ldp, ov, pieces, sdepth, swidth):
        S0 = State(0, 0, pieces, [(0, 0)], [])
        Sset = [S0]
        Sbest_vp = 0

    #   while len(Sset) != 0:
    #       # We choose the state with the maximum number of packed pieces
    #       S = max(Sset, key=lambda s: s.num_packed)

    #       if S == S0:
    #           pl = Placement(self, ldp, ov, (0, 0))
    #           S1 =



