class Piece:
    def __init__(self, length, width, ov=None):
        self.length = length
        self.width = width
        self.ov = ov
    
    def get_length(self):
        if self.ov:
            return self.width
        else:
            return self.length
        
    def get_width(self):
        if self.ov:
            return self.length
        else:
            return self.width
        
    def set_ov(self, ov):
        self.ov = ov

    def get_ov(self):
        return self.ov
        
    def get_area(self):
        return self.length * self.width