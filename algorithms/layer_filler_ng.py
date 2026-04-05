from model.state import State
from model.placement import Placement
from pprint import pprint

class LayerFillerNG:

    def fill_layer(self, layer, ldp, pieces, s_depth, s_width):
        import copy
        s_0 = State(layer, pieces)
        pl = Placement(ldp, (0, 0))
        s_set = [s_0]
        s_best_vp = 0
        s_best = None

        while len(s_set) != 0:
            # Choose the state with the highest number of packed pieces
            s = max(s_set, key=lambda s: s.num_packed)
            # Remove it from the states' set
            s_set.remove(s)

            if s == s_0:
                pl = Placement(ldp, (0, 0))
                if s.is_feasible(pl):
                    s_1 = s.commit_placement(pl)
                    s_set.append(s_1)
                else:
                    return None
            else:
                candidate_successors = []
                for p in s.get_pieces():
                    for p_point in s.get_p_points():
                        p1 = copy.deepcopy(p)
                        p1.set_ov(True)
                        pl1 = Placement(p1, p_point)
                        if s.is_feasible(pl1):
                            candidate_successors.append((pl1, s.get_tp(pl1)))

                        p2 = copy.deepcopy(p)
                        p2.set_ov(False)
                        pl2 = Placement(p2, p_point)
                        if s.is_feasible(pl2):
                            candidate_successors.append((pl2, s.get_tp(pl2)))
                
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
                    candidate_successors.sort(key=lambda x: x[1], reverse=True)
                    
                    # Choose the n_succ placements with the highest touching perimeter
                    best_successors = candidate_successors[:n_succ]
                    
                    # Commit the placements and create the new states
                    for pl, _ in best_successors:
                        s_next = s.commit_placement(pl)
                        if s_next not in s_set:
                            s_set.append(s_next)

        return s_best

