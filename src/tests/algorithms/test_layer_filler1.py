from model.layer import Layer
from model.piece import Piece
from model.placement import Placement
from model.warehouse import Warehouse
from algorithms.layer_filler_ng import LayerFillerNG
from visuals.state_visuals import plot_layer_state

layer = Layer(10, 10)
ldp = Placement(piece=Piece(4, 4), is_rotated=True, p_point=(0, 0))

initial_inventory = {
    ldp.get_piece(): 1,
    Piece(2, 4): 1,
    Piece(4, 2): 1,
    Piece(3, 3): 1,
    Piece(2, 2): 1,
    Piece(6, 6): 1
}

# Create the warehouse directly with the dictionary
warehouse = Warehouse(initial_inventory)

# Proceed with the filler
filler = LayerFillerNG(s_depth=3, s_width=2)
best_state = filler.fill_layer(layer, ldp, warehouse)

# Result Visualization
if best_state is not None:
    plot_layer_state(best_state)
else:
    print("\nSolution not found.")