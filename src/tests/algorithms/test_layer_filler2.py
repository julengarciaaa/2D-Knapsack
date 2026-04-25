from model.layer import Layer
from model.piece import Piece
from model.warehouse import Warehouse
from model.placement import Placement
from algorithms.layer_filler_ng import LayerFillerNG
from visuals.state_visuals import plot_layer_state

# Define the layer dimensions
layer = Layer(20, 30)

# Define the Layer Defining Piece (LDP)
ldp = Placement(piece=Piece(2, 3), is_rotated=False, p_point=(0, 0))

# Create the initial inventory dictionary
inventory_data = {
    Piece(5, 2): 10, 
    Piece(3, 2): 10,
    Piece(7, 2): 10, 
    Piece(4, 3): 10,
    Piece(6, 3): 10,
    Piece(2, 2): 10, 
    Piece(10, 4): 10,
    ldp.get_piece(): 1 
}

warehouse = Warehouse(inventory_data)

# Proceed with the filler
filler = LayerFillerNG(s_depth=3, s_width=3)
best_state = filler.fill_layer(layer, ldp, warehouse)

# Result Visualization
if best_state is not None:
    plot_layer_state(best_state)
else:
    print("\nSolution not found.")