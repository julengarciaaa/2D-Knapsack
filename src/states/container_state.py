from src.model.layer import Layer
from src.model.warehouse import Warehouse

class ContainerState:
    __slots__ = ['container', 'warehouse', 'layer_filler', '_cached_hash']

    def __init__(self, container, warehouse, layer_filler):
        self.container = container
        self.warehouse = warehouse
        self.layer_filler = layer_filler

        self._cached_hash = hash((self.container, self.warehouse))

    def get_container(self):
        return self.container
    
    def get_warehouse(self):
        return self.warehouse

    def fill_layer(self, ldp):
        # Check if the piece fits in the remaining container length
        if not self.container.is_feasible_ldp(ldp):
            return None

        # Prepare the environment for the new layer
        layer_length = ldp.get_length()
        layer = Layer(layer_length, self.container.width)
    
        # Call the filler
        solution_state = self.layer_filler.fill_layer(
            layer, 
            ldp, 
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
                self.layer_filler
            )
            
        return None
    
    # Check if the layer physically fits the container and the warehouse 
    # has enough stock for its pieces.
    def can_add_layer(self, layer):
        layer_warehouse = Warehouse.warehouse_from_placements(layer.get_placements())

        return self.container.can_add_layer(layer) and self.warehouse.contains(layer_warehouse)
        
    def __eq__(self, other):
        if not isinstance(other, ContainerState):
            return False
        return self._cached_hash == other._cached_hash
    
    def __hash__(self):
        return self._cached_hash