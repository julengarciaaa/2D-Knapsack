from model.layer import Layer
from model.piece import Piece
from algorithms.layer_filler_ng import LayerFillerNG
from visuals.state_visuals import plot_state

layer = Layer(6, 11)
ldp = Piece(2, 3, False) 

pieces = [
    Piece(2, 2, False),
    Piece(2, 4, False),
    Piece(2, 1, False),
    Piece(4, 1, False),
    Piece(1, 1, False),
    Piece(4, 1, False),
    Piece(5, 1, False),
    Piece(2, 2, False),
    Piece(2, 3, False),
    Piece(3, 2, False)
]

filler = LayerFillerNG()
best_state = filler.fill_layer(layer, ldp, pieces, s_depth=2, s_width=3)

if best_state is not None:
    plot_state(best_state)
else:
    print("\nSolution not found.")