from src.model.layer import Layer
from src.model.piece import Piece
from src.model.placement import Placement
from src.model.warehouse import Warehouse
from src.states.layer_state import LayerState
from src.algorithms.layer_filler_rts import LayerFillerRTS
from src.visuals.state_visuals import plot_layer_state
from src.utils.data_loader import load_warehouse_from_json, load_layer_from_json

import numpy as np
import statistics
import time
import csv
import os

def get_possible_placements(layer, warehouse):
    layer_state = LayerState(layer, warehouse)
    pieces = warehouse.get_pieces()

    possible_placements = []
    for piece in pieces:
        is_square = (piece.length == piece.width)
        # Try both orientations
        orientations = [False] if is_square else [False, True]
        
        for rot in orientations:
            pl = Placement(piece, rot, (0, 0))

            if layer.is_feasible(pl):
                # Touching Perimeter (TP) is our heuristic
                possible_placements.append((pl, layer_state.get_tp(pl)))
            
        return possible_placements

def select_random_ldp(layer, warehouse):
    possible_placements = get_possible_placements(layer, warehouse)
    weights = np.array([t[1] for t in possible_placements])
    probabilities = weights / weights.sum()

    index = np.random.choice(len(possible_placements), size=1, replace=False, p=probabilities)[0]

    return possible_placements[index][0]

def main():
    # Load the required data
    data_path = "src/data/set1/BEASLEY/1.json"
    total_runs = 30
    layer = load_layer_from_json(data_path)
    warehouse = load_warehouse_from_json(data_path)

    run_times = []
    for i in range(30):
        # Select randomly the layer defining placement (LDP)
        ldp = select_random_ldp(layer, warehouse)

        # Proceed with the filler
        filler = LayerFillerRTS(s_depth=3, s_width=2)
        # Start the counter
        start_time = time.perf_counter()
        # Execute the filler
        best_state = filler.fill_layer(layer, ldp, warehouse)
        # Stop the counter 
        end_time = time.perf_counter()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time
        run_times.append(elapsed_time)

    # Calculate statistics
    mean_time = statistics.mean(run_times)
    std_dev = statistics.stdev(run_times)

    # Save statistics in a CSV file
    csv_filename = "layer_filler_rts_time_statistics.csv"
    file_exists = os.path.isfile(csv_filename)

    headers = ["Evaluated instance", "Total runs", "Mean time", "Standard Deviation"]

    with open(csv_filename, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(headers)

        writer.writerow([data_path, total_runs, mean_time, std_dev])




if __name__ == "__main__":
    main()