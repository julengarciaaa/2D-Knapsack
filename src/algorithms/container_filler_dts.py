from src.states.container_state import ContainerState
from src.model.layer import Layer
from src.model.placement import Placement
from src.model.container import Container
from src.model.warehouse import Warehouse
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
import heapq
from src.visuals.state_visuals import plot_container_state

def worker(args):
    container_dict, placement_dict, warehouse_dict, n_solutions, params = args

    container = Container.container_from_dict(container_dict)
    placement = Placement.placement_from_dict(placement_dict)
    warehouse = Warehouse.warehouse_from_dict(warehouse_dict)

    filler = ContainerFillerDTS(*params)

    return filler._fill_container(container, placement, warehouse, n_solutions)

class ContainerFillerDTS:
    def __init__(self, n1, n2, layer_filler):
        self.n1 = n1
        self.n2 = n2
        self.layer_filler = layer_filler

    def get_best_ldps(self, container, warehouse, n):
        # Sort by packed value to prioritize high packed values
        pieces = sorted(warehouse.get_pieces(), key=lambda p: p.get_packed_value(), reverse=True)
        best_ldps = []

        for piece in pieces:
            # Skip if we don't even have 1 unit left
            if warehouse.get_max_demand(piece) <= 0:
                continue

            orientations = [False] if piece.width == piece.length else [False, True]
            for is_rotated in orientations:
                pl = Placement(piece, is_rotated, (0, 0))
                if container.is_feasible_ldp(pl):
                    best_ldps.append(pl)
                    if len(best_ldps) >= n:
                        return best_ldps
        return best_ldps

    def _fill_container(self, container, initial_ldp, warehouse, n_solutions=1):
        # Create initial state with the first chosen LDP
        s_start = ContainerState(container, warehouse, self.layer_filler)
        s_0 = s_start.fill_layer(initial_ldp)

        if s_0 is None: return None
        
        solutions = []
        s_best_fr = s_0.get_container().get_filling_rate()
        s_set = [s_0]
        visited = {s_0}
            
        while s_set:
            s = s_set.pop()

            current_warehouse = s.get_warehouse()
            current_container = s.get_container()
            
            best_ldps = self.get_best_ldps(current_container, current_warehouse, self.n2)
            
            # Leaf node
            if not best_ldps:
                solutions.append(s)
            else:
                for ldp in best_ldps:
                    s_next = s.fill_layer(ldp)
                    
                    if s_next is not None and s_next not in visited:
                        visited.add(s_next)
                        s_set.append(s_next)

        
        return heapq.nlargest(max(1, n_solutions), visited, key=lambda x: x.get_container().get_filling_rate())

    def fill_container(self, container, warehouse, n_solutions=1):
        placements = self.get_best_ldps(container, warehouse, self.n1)

        container_dict = Container.container_to_dict(container)
        warehouse_dict = Warehouse.warehouse_to_dict(warehouse)
        placement_dicts = [Placement.placement_to_dict(pl) for pl in placements]

        params = (self.n1, self.n2, self.layer_filler)

        args = [
            (container_dict, pl_dict, warehouse_dict, n_solutions, params)
            for pl_dict in placement_dicts
        ]

        with ProcessPoolExecutor() as executor:
            results = executor.map(worker, args)

        solutions = [ContainerState(container, warehouse, self.layer_filler)]
        solutions.extend([solution for result in results for solution in result])
        solutions.sort(key=lambda x: x.get_container().get_filling_rate(), reverse=True)

        return solutions[:max(1, n_solutions)]




