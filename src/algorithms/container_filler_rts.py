from src.states.container_state import ContainerState
from src.model.layer import Layer
from src.model.placement import Placement
from src.model.container import Container
from src.model.warehouse import Warehouse
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
import heapq
from src.visuals.state_visuals import plot_container_state
import numpy as np

def worker(args):
    container_dict, placement_dict, warehouse_dict, n_solutions, params = args

    container = Container.container_from_dict(container_dict)
    placement = Placement.placement_from_dict(placement_dict)
    warehouse = Warehouse.warehouse_from_dict(warehouse_dict)

    filler = ContainerFillerRTS(*params)

    return filler._fill_container(container, placement, warehouse, n_solutions)

class ContainerFillerRTS:
    def __init__(self, n1, n2, layer_filler):
        self.n1 = n1
        self.n2 = n2
        self.layer_filler = layer_filler

    def choose_random_ldp(self, container, warehouse, n):
        # Obtain the feasible placements
        placements = []
        for piece in warehouse.get_pieces():
            orientations = [False] if piece.width == piece.length else [False, True]
            for is_rotated in orientations:
                pl = Placement(piece, is_rotated, (0, 0))
                if container.is_feasible_ldp(pl):
                    placements.append((pl, piece.get_packed_value()))
        
        if len(placements) == 0:
            return []
        else:
            # Obtain the weights
            weights = np.array([t[1] for t in placements])
            probabilities = weights / weights.sum()

            # Get the random placements
            indexes = np.random.choice(len(placements), size=min(n, len(placements)), replace=False, p=probabilities)

            return [placements[i][0] for i in indexes]
        

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
            
            best_ldps = self.choose_random_ldp(current_container, current_warehouse, self.n2)
            
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
        placements = self.choose_random_ldp(container, warehouse, self.n1)

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




