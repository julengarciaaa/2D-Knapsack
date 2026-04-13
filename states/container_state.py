from algorithms.layer_filler_ng import LayerFillerNG
from model.layer import Layer

class ContainerState:
    __slots__ = ['container', 'warehouse', 'layer_filler', '_cached_hash']

    def __init__(self, container, warehouse, s_depth=3, s_width=3):
        self.container = container
        self.warehouse = warehouse
        self.layer_filler = LayerFillerNG(s_depth=s_depth, s_width=s_width)

        self._cached_hash = hash((self.container, self.warehouse))

    def get_container(self):
        return self.container
    
    def get_warehouse(self):
        return self.warehouse

    def fill_layer(self, placement):
        # Check if the piece fits in the remaining container length
        if not self.container.is_feasible_ldp(placement):
            return None

        # Prepare the environment for the new layer
        layer_length = placement.get_length()
        layer_area_template = Layer(layer_length, self.container.width)
    
        # Call the filler
        solution_state = self.layer_filler.fill_layer(
            layer_area_template, 
            placement, 
            self.warehouse
        )
        
        if solution_state is not None:
            # Build the next state
            new_layer = solution_state.get_layer()
            new_container = self.container.add_layer(new_layer)
            new_warehouse = solution_state.get_warehouse()
            
            # Return the next node in the global search tree
            return ContainerState(
                new_container, 
                new_warehouse, 
                s_depth=self.layer_filler.s_depth, 
                s_width=self.layer_filler.s_width
            )
            
        return None
        
    def __eq__(self, other):
        if not isinstance(other, ContainerState):
            return False
        return self._cached_hash == other._cached_hash
    
    def __hash__(self):
        return self._cached_hash