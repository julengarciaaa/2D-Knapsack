class Layer:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.placements = []
    
    def get_covered_area(self):
        return sum(placement.get_piece().get_area() for placement in self.placements)
    
    def get_area(self):
        return self.width * self.length
    
    def get_filling_rate(self):
        total_area = self.get_area()
        if total_area == 0 or not self.placements:
            return 0
        return self.get_covered_area() / total_area
    
    def get_length(self):
        return self.length
    
    def get_width(self):
         return self.width
    
    def get_placements(self):
        return self.placements
    
    def get_num_placements(self):
        return len(self.placements)
    
    def add_placement(self, placement):
        self.placements.append(placement)

    def __eq__(self, other):
        # Check if the other object is a Layer
        if not isinstance(other, Layer):
            return False
        
        # Two layers are equal if they have the same dimensions and placements
        return (self.length == other.length and 
                self.width == other.width and 
                set(self.placements) == set(other.placements))
    
    def __hash__(self):
        # We hash the dimensions and a frozenset of placements
        return hash((self.length, self.width, frozenset(self.placements)))


    def print_layer(self):
        """
        Imprime un resumen detallado de la capa en la consola.
        """
        area_total = self.get_area()
        area_cubierta = self.get_covered_area()
        filling_rate = self.get_filling_rate()

        print(f"\n{'='*50}")
        print(f" LOG DE CAPA: {self.length}x{self.width}")
        print(f"{'='*50}")
        print(f" > Piezas colocadas: {self.get_num_placements()}")
        print(f" > Espacio ocupado:  {area_cubierta} / {area_total} u²")
        print(f" > Eficiencia:       {filling_rate * 100:.2f}%")
        print(f"{'-'*50}")
        
        if not self.placements:
            print(" [!] La capa está actualmente vacía.")
        else:
            print(f"{'ID':<4} | {'Posición (X,Y)':<15} | {'Dimensiones':<12} | {'Área'}")
            print(f"{'-'*50}")
            for i, p in enumerate(self.placements):
                x, y = p.get_p_point()
                l, w = p.get_length(), p.get_width()
                area = l * w
                print(f"{i+1:<4} | ({x:>2}, {y:>2}){' ':<8} | {l:>2} x {w:>2}{' ':<5} | {area:>4}")
        
        print(f"{'='*50}\n")
