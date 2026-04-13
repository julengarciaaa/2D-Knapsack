from states.container_state import ContainerState
from model.layer import Layer
from model.placement import Placement
from algorithms.layer_filler_ng import LayerFillerNG
from visuals.state_visuals import plot_layer_state

class ContainerFiller:
    def __init__(self, n1, n2, s_depth, s_width):
        self.n1 = n1
        self.n2 = n2
        self.s_depth = s_depth
        self.s_width = s_width

    def get_best_ldps(self, container, warehouse, n):
        # Sort by area to prioritize large "base" pieces
        pieces = sorted(warehouse.get_pieces(), key=lambda p: p.get_area(), reverse=True)
        best_ldps = []

        for piece in pieces:
            # Skip if we don't even have 1 unit left
            if warehouse.inventory.get(piece, 0) <= 0:
                continue

            orientations = [False] if piece.width == piece.length else [False, True]
            for is_rotated in orientations:
                pl = Placement(piece, is_rotated, (0, 0))
                if container.is_feasible_ldp(pl):
                    best_ldps.append(pl)
                    if len(best_ldps) >= n:
                        return best_ldps
        return best_ldps

    def _fill_container(self, container, initial_ldp, initial_warehouse):
        # Create initial state with the first chosen LDP
        s_start = ContainerState(container, initial_warehouse, self.s_depth, self.s_width)
        s_0 = s_start.fill_layer(initial_ldp)

        if s_0 is None: return None
        
        s_best = s_0
        s_best_fr = s_0.get_container().get_filling_rate()
        s_set = [s_0]
        visited = {s_0}
            
        while s_set:
            s = s_set.pop()

            current_warehouse = s.get_warehouse()
            current_container = s.get_container()
            
            best_ldps = self.get_best_ldps(current_container, current_warehouse, self.n2)

            if not best_ldps:
                # Leaf node: check if it's the best container overall
                fr = current_container.get_filling_rate()
                if fr > s_best_fr:
                    s_best = s
                    s_best_fr = fr
            else:
                for ldp in best_ldps:
                    s_next = s.fill_layer(ldp)
                    
                    if s_next is not None and s_next not in visited:
                        visited.add(s_next)
                        s_set.append(s_next)
        return s_best 
         
    def fill_container(self, container, warehouse):
        # Obtain the best layer defining placements
        best_ldps = self.get_best_ldps(container, warehouse, self.n1)

        s_best = None
        s_best_fr = 0

        for best_ldp in best_ldps:
            s = self._fill_container(container, best_ldp, warehouse)

            if s is not None and s.get_container().get_filling_rate() > s_best_fr:
                s_best = s
                s_best_fr = s.get_container().get_filling_rate()
 
        return s_best 



