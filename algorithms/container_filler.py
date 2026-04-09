from model.container_state import ContainerState
from model.layer import Layer
from model.placement import Placement
from algorithms.layer_filler_ng import LayerFillerNG

class ContainerFiller:

    def __init__(self, n1, n2, s_depth, s_width):
        self.n1 = n1
        self.n2 = n2
        self.s_depth = s_depth
        self.s_width = s_width

    def get_best_ldps(self, container, warehouse, n):
        # Get pieces and sort them by area in descending order
        pieces = sorted(warehouse.get_pieces(), key=lambda p: p.get_area(), reverse=True)
        best_ldps = []

        for piece in pieces:
            # Check both orientations unless the piece is a square
            orientations = [False, True]
            if piece.width == piece.length:
                orientations = [False]

            for is_rotated in orientations:
                # Create a placement at the origin (0,0)
                pl = Placement(piece, is_rotated, (0, 0))

                # Check if this placement is valid for the current container
                if container.is_feasible_ldp(pl):
                    best_ldps.append(pl)
                    n -= 1
                    
                    # Stop once we have reached the required number of candidates
                    if n <= 0:
                        return best_ldps

        return best_ldps

            
         

    def fill_container(self, container, warehouse, n1, n2):
        best_initial_ldps = self.get_best_ldps(container, warehouse, n1)

        s_best_fr = 0
        s_best = None

        for initial_ldp in best_initial_ldps:
            # Initialize the state
            s_0 = ContainerState(container, warehouse)
            # Fill the layer
            s_0 = s_0.fill_layer(initial_ldp, self.s_depth, self.s_width)
            s_set = [s_0]
            visited = set()
            visited.add(s_0)

            while len(s_set) != 0:
                s = s_set.pop()
                container = s.get_container()
                warehouse = s.get_warehouse()

                # Obtain the best layer defining placements
                best_ldps = self.get_best_ldps(container, warehouse, n2)

                if len(best_ldps) == 0:
                    s_fr = s.get_container().get_filling_rate()
                    if s_fr > s_best_fr:
                        s_best_fr = s_fr
                        s_best = s

                for best_ldp in best_ldps:
                    s_next = s.fill_layer(best_ldp, self.s_depth, self.s_width)
                    if s_next not in visited:
                        visited.add(s_next)
                        s_set.append(s_next)

            return s_best 




                


        












        return None