from model.layer import Layer
from model.piece import Piece
from model.warehouse import Warehouse
from algorithms.layer_filler_ng import LayerFillerNG
from visuals.state_visuals import plot_layer_state

layer = Layer(20, 30)
ldp = Piece(2, 3) 

warehouse = Warehouse()

# Add multiple units of pieces that fit well together (sum to 10)
for _ in range(10):
    warehouse.add_piece(Piece(5, 2))  # Two of these fill the width (5+5=10)
    warehouse.add_piece(Piece(3, 2))  
    warehouse.add_piece(Piece(7, 2))  # (3+7=10)
    warehouse.add_piece(Piece(4, 3))
    warehouse.add_piece(Piece(6, 3))  # (4+6=10)
    warehouse.add_piece(Piece(2, 2))  # Fillers

for _ in range(10):
    warehouse.add_piece(Piece(10, 4)) # Full width piece

filler = LayerFillerNG()
best_state = filler.fill_layer(layer, ldp, False, warehouse, s_depth=3, s_width=3)

if best_state is not None:
    plot_layer_state(best_state)
else:
    print("\nSolution not found.")