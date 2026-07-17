import portion as P
from collections import defaultdict

class LayerState:
    __slots__ = ["layer", "warehouse"]

    def __init__(self, layer, warehouse):
        self.layer = layer
        self.warehouse = warehouse

    def get_layer(self):
        return self.layer
    
    def get_warehouse(self):
        return self.warehouse
    
    def get_p_points(self):
        return self.get_layer().get_p_points()

    # Commits a placement and updates the warehouse
    def commit_placement(self, placement):

        return LayerState(
            layer=self.get_layer().commit_placement(placement), 
            warehouse=self.get_warehouse().delete_piece(placement.get_piece())
        )
    
    def get_tp(self, placement):
        tp = self.get_layer().get_tp(placement)
        
        return tp
    
    def get_filling_rate(self):
        return self.get_layer().get_filling_rate()
    
    def get_packed_value_rate(self):
        real_packed_value = self.get_layer().get_packed_value()
        max_packed_value = self.get_layer().get_length() * self.get_layer().get_width() * self.get_warehouse().get_max_packed_value_density()

        return real_packed_value / max_packed_value
    
    def get_penalty_rate(self):
        return self.warehouse.get_penalty_rate()
    
    def get_fitness_value(self):
        filling_rate = self.get_filling_rate()
        packed_value_rate = self.get_packed_value_rate()
        penalty_rate = self.get_penalty_rate()

        fitness = (filling_rate + packed_value_rate - penalty_rate + 1) / 3

        return fitness

    def _measure(self, interval):
        return sum(i.upper - i.lower for i in interval) if not interval.empty else 0

    def __eq__(self, other):
        if not isinstance(other, LayerState): return False
        return (self.warehouse == other.warehouse and 
                self.layer == other.layer)