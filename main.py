from model.layer import Layer
from model.piece import Piece
from algorithms.layer_filler_ng import LayerFillerNG
from visuals.state_visuals import plot_layer_state

def main():
    layer = Layer(10, 10)
    ldp = Piece(4, 4, False) 

    pieces = [
        Piece(2, 4, False),
        Piece(4, 2, False),
        Piece(3, 3, False),
        Piece(2, 2, False),
        Piece(6, 6, False)
    ]

    filler = LayerFillerNG()
    best_state = filler.fill_layer(layer, ldp, pieces, s_depth=3, s_width=2)

    if best_state is not None:
        plot_layer_state(best_state)
    else:
        print("\nSolution not found.")

if __name__ == "__main__":
    main()