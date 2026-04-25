from algorithms.layer_filler_ng import LayerFillerNG
from model.layer import Layer
from visuals.state_visuals import plot_layer_state

class ContainerState:

    def __init__(self, container, warehouse):
        self.container = container
        self.warehouse = warehouse
        self.layer_filler = LayerFillerNG()

    def get_container(self):
        return self.container
    
    def get_warehouse(self):
        return self.warehouse

    def fill_layer(self, placement, s_depth, s_width):
        import copy
         
        if self.container.is_feasible_ldp(placement):
            # Create a copy of the warehouse to avoid modifying the original one
            temp_warehouse = copy.deepcopy(self.warehouse)
            
            # Create the layer we are filling 
            piece_length = placement.get_length()
            layer = Layer(piece_length, self.container.width)
        
            solution = self.layer_filler.fill_layer(layer, 
                                        placement.get_piece(), 
                                        placement.is_rotated(), 
                                        temp_warehouse, 
                                        s_depth, 
                                        s_width)
            
            
            if solution is not None:
                # Create a copy of the container and add the new layer
                new_container = copy.deepcopy(self.container)
                new_container.add_layer(solution.get_layer())
                
                # Return a new instance with the updated container and warehouse
                return self.__class__(new_container, solution.get_warehouse())
                
        return None
        
    def get_successors(self, placement):
        return None
    
    def __eq__(self, other):
        if not isinstance(other, ContainerState):
            return False
        
        return (self.container == other.container and
                self.warehouse == other.warehouse)
    
    def __hash__(self):
        return hash((self.container, self.warehouse))
            
