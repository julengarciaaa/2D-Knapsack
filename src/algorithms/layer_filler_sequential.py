from src.model.placement import Placement
from src.states.layer_state import LayerState
import numpy as np

class LayerFillerSequential:
    def __init__(self):
        pass

    def fill_layer(self, layer, ldp, warehouse):
        s = LayerState(layer, warehouse)
        s = s.commit_placement(ldp)

        possible_placements = self.get_possible_placements(s)
        while possible_placements:
            next_placement = self.select_random_placement(possible_placements)
            s = s.commit_placement(next_placement)

            possible_placements = self.get_possible_placements(s)

        return s

        
    def select_random_placement(self, possible_placements):
        weights = np.array([t[1] for t in possible_placements])
        total_weight = weights.sum()

        # Avoid division by zero.
        if total_weight == 0:
            probabilities = np.ones(len(possible_placements)) / len(possible_placements)
        else:
            probabilities = weights / total_weight

        # Normalise the vector to avoid floating point issues.
        probabilities /= probabilities.sum()

        index = np.random.choice(len(possible_placements), size=1, replace=False, p=probabilities)[0]

        return possible_placements[index][0]

    def get_possible_placements(self, layer_state):
        pieces = layer_state.get_warehouse().get_pieces()
        p_points = layer_state.get_p_points()
        layer = layer_state.get_layer()

        possible_placements = []
        for piece in pieces:
            is_square = (piece.length == piece.width)
            for p_point in p_points:
                    # Try both orientations
                    orientations = [False] if is_square else [False, True]
                    
                    for rot in orientations:
                        pl = Placement(piece, rot, p_point)

                        if layer.is_feasible(pl):
                            # Touching Perimeter (TP) is our heuristic
                            possible_placements.append((pl, layer_state.get_tp(pl)))
            
        return possible_placements