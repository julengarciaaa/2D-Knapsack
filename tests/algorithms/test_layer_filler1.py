from model.layer import Layer
from model.piece import Piece
from model.warehouse import Warehouse
from algorithms.layer_filler_ng import LayerFillerNG
from visuals.state_visuals import plot_layer_state

layer = Layer(10, 10)
ldp = Piece(4, 4) 

warehouse = Warehouse()
warehouse.add_piece(ldp)
warehouse.add_piece(Piece(2, 4))
warehouse.add_piece(Piece(4, 2))
warehouse.add_piece(Piece(3, 3))
warehouse.add_piece(Piece(2, 2))
warehouse.add_piece(Piece(6, 6))

filler = LayerFillerNG()
best_state = filler.fill_layer(layer, ldp, True, warehouse, s_depth=3, s_width=2)

if best_state is not None:
    plot_layer_state(best_state)
else:
    print("\nSolution not found.")