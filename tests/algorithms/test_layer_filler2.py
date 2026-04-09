from model.layer import Layer
from model.piece import Piece
from model.warehouse import Warehouse
from algorithms.layer_filler_ng import LayerFillerNG
from visuals.state_visuals import plot_layer_state

layer = Layer(6, 11)
ldp = Piece(2, 3) 

warehouse = Warehouse()
warehouse.add_piece(ldp)
warehouse.add_piece(Piece(2, 2))
warehouse.add_piece(Piece(2, 4))
warehouse.add_piece(Piece(2, 1))
warehouse.add_piece(Piece(4, 1))
warehouse.add_piece(Piece(1, 1))
warehouse.add_piece(Piece(4, 1))
warehouse.add_piece(Piece(5, 1))
warehouse.add_piece(Piece(2, 2))
warehouse.add_piece(Piece(2, 3))
warehouse.add_piece(Piece(3, 2))

filler = LayerFillerNG()
best_state = filler.fill_layer(layer, ldp, False, warehouse, s_depth=2, s_width=3)

if best_state is not None:
    plot_layer_state(best_state)
else:
    print("\nSolution not found.")