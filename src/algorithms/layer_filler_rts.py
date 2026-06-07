from src.model.placement import Placement
from src.states.layer_state import LayerState
from src.visuals.state_visuals import plot_layer_state
import numpy as np

class LayerFillerRTS:
    def __init__(self, s_depth, s_width):
        self.s_depth = s_depth
        self.s_width = s_width

    def choose_random_candidates(self, candidates, n):
        weights = np.array([t[1] for t in candidates])
        probabilities = weights / weights.sum()

        indexes = np.random.choice(len(candidates), size=min(n, len(candidates)), replace=False, p=probabilities)

        return [candidates[i][0] for i in indexes]

    def fill_layer(self, layer, ldp, warehouse):
        # Starting state with the Layer Defining Placement (LDP)
        s_0 = LayerState(layer, warehouse)
        s_1 = s_0.commit_placement(ldp)
        
        if s_1 is None: # Safety check
            return None

        s_set = [s_1]
        visited = {s_1}

        s_best_vp = 0
        s_best = s_1

        while s_set:
            s = s_set.pop()
            # Generate candidates
            candidate_successors = []
            free_pieces = s.get_warehouse().get_pieces()
            p_points = s.get_p_points()

            for p in free_pieces:
                is_square = (p.length == p.width)
                for p_point in p_points:
                    # Try both orientations
                    orientations = [False] if is_square else [False, True]
                    
                    for rot in orientations:
                        pl = Placement(p, rot, p_point)

                        if s.layer.is_feasible(pl):
                            # Touching Perimeter (TP) is our heuristic
                            candidate_successors.append((pl, s.get_tp(pl)))

            # Continue searching or save best result
            if not candidate_successors:
                current_value = s.layer.get_filling_rate()
                if current_value > s_best_vp:
                    s_best_vp = current_value
                    s_best = s
            else:
                # Beam width logic
                n_succ = self.s_width if s.layer.get_num_placements() <= self.s_depth else 1
                
                # Take the best n_succ (highest TP)
                best_candidates = self.choose_random_candidates(candidate_successors, n_succ)
                
                for pl in best_candidates:
                    s_next = s.commit_placement(pl)
                    
                    if s_next not in visited:
                        visited.add(s_next)
                        s_set.append(s_next)

        return s_best
