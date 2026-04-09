from model.layer_state import LayerState
from model.placement import Placement
from pprint import pprint

class LayerFillerNG:

    def fill_layer(self, layer, ldp, is_rotated, warehouse, s_depth, s_width):
        import copy

        s_0 = LayerState(layer, warehouse)
        s_set = [s_0]
        visited = set()
        visited.add(s_0)

        s_best_vp = 0
        s_best = None

        while len(s_set) != 0:
            s = s_set.pop()

            if s == s_0:
                pl = Placement(ldp, is_rotated, (0, 0))
                if s.is_feasible(pl):
                    s_1 = s.commit_placement(pl)
                    s_set.append(s_1)
                else:
                    return None
            else:
                candidate_successors = []
                free_pieces = s.get_warehouse().get_pieces()
                p_points = s.get_p_points()

                for p in free_pieces:
                    is_square = (p.length == p.width)
                    
                    for p_point in p_points:
                        # Non-rotated piece
                        pl2 = Placement(p, False, p_point)
                        if s.is_feasible(pl2):
                            candidate_successors.append((pl2, s.get_tp(pl2)))

                        # Rotated piece, only if it is not a square
                        if not is_square:
                            pl1 = Placement(p, True, p_point)
                            if s.is_feasible(pl1):
                                candidate_successors.append((pl1, s.get_tp(pl1)))
                
                if len(candidate_successors) == 0:
                    if s.get_packed_value() > s_best_vp:
                        s_best_vp = s.get_packed_value()
                        s_best = s
                else:
                    if s.get_num_packed() <= s_depth:
                        n_succ = s_width
                    else:
                        n_succ = 1

                    # Sort the candidate placements based on the touching perimeter
                    candidate_successors.sort(key=lambda x: x[1], reverse=False)
                    
                    # Choose the n_succ placements with the highest touching perimeter
                    best_successors = candidate_successors[-n_succ:]
                    
                    # Commit the placements and create the new states
                    for pl, _ in best_successors:
                        s_next = s.commit_placement(pl)

                        # We only add the new state if it is not visited yet
                        if s_next not in visited:
                            visited.add(s_next)
                            s_set.append(s_next)

        return s_best

