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
import pickle

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
    set_name = "set4"
    subset_name = "HOPPER"
    data_path = f"src/data/{set_name}/{subset_name}/"
    csv_path = "src/tests/algorithms/results/layer_filler_rts_statistics.csv"
    results_path = "src/tests/algorithms/results/"
    total_runs = 30

    # Create the CSV file in case it does not exist
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    headers = [
        "Instance Name", "Total Runs", 
        "T_Mean", "T_Max", "T_Min", "T_Std", 
        "Fit_Mean", "Fit_Max", "Fit_Min", "Fit_Std"
    ]
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
    
    for i in range(1, 5):
        # Generate the name of the instance
        instance_name = subset_name + "_" + str(i)
        # Generate the path of the instance
        instance_path = data_path + str(i) + ".json"
        # Load the data
        layer = load_layer_from_json(instance_path)
        warehouse = load_warehouse_from_json(instance_path)

        run_times = []
        fitnesses = []
        solutions = []
        for j in range(total_runs):
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
            fitnesses.append(best_state.get_fitness_value())
            solutions.append(best_state)

        # Calculate time statistics
        mean_time = statistics.mean(run_times)
        max_time = max(run_times)
        min_time = min(run_times)
        std_time = statistics.stdev(run_times)

        # Calculate fitness statistics
        mean_fit = statistics.mean(fitnesses)
        max_fit = max(fitnesses)
        min_fit = min(fitnesses)
        std_fit = statistics.stdev(fitnesses)

        # Obtain the best solution
        best_solution = solutions[np.argmax(fitnesses)]

        # Save the best solution
        pkl_filename = f"rts_best_sol_{instance_name}.pkl"
        pkl_path = os.path.join(results_path, pkl_filename)
        
        with open(pkl_path, "wb") as sf:
            pickle.dump(best_solution, sf)

        # Save the statistics
        with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                instance_name, total_runs, 
                mean_time, max_time, min_time, std_time,
                mean_fit, max_fit, min_fit, std_fit
            ])




if __name__ == "__main__":
    main()