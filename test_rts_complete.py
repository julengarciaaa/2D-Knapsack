import sys
import os
import pandas as pd
import multiprocessing 

from src.algorithms.container_filler_rts import ContainerFillerRTS
from src.algorithms.layer_filler_rts import LayerFillerRTS
from src.algorithms.solver_rts import SolverRTS
from src.utils.data_loader import load_container_from_json, load_warehouse_from_json
from src.model.container import Container
from src.model.warehouse import Warehouse

def worker(args):
    run_idx = args["run_idx"]
    data_path = args["data_path"]
    p = args["heuristic_parameter"]
    n_pop = args["n_pop"]
    
    print(f"Starting Run: {run_idx} | Instance: {data_path} | Pop: {n_pop} | Heur: {p}")

    # Reconstruct objects inside the process using class methods
    layer_filler = LayerFillerRTS(s_depth=p[0], s_width=p[1])
    container_filler = ContainerFillerRTS(n1=p[0], n2=p[1], layer_filler=layer_filler)
    
    container = Container.container_from_dict(args["container_dict"])
    warehouse = Warehouse.warehouse_from_dict(args["warehouse_dict"])

    params = {
        "n_pop": n_pop,
        "n_gen": 100,
        "n_rep": int(n_pop * 0.1),
        "cxpb": 0.5,
        "mutpb": 0.5,
        "container_filler": container_filler
    }
    
    solver = SolverRTS(**params)
    solution, df_log = solver.solve(container, warehouse)

    return solution, df_log


def main():
    set_paths = ["src/data/set3/JAKOBS/", "src/data/set4/HOPPER/"]
    name_paths = ["JAKOBS", "HOPPER"]
    
    # Detect available cores
    num_cores = multiprocessing.cpu_count()
    print(f"System detected {num_cores} cores. Multiprocessing active.")

    for set_path, name_path in zip(set_paths, name_paths):
        for i in range(1, 6):
            data_path = f"{set_path}{i}.json"

            heuristic_parameters = [(1, 1), (2, 3)]
            n_pops = [10, 20, 30]

            warehouse = load_warehouse_from_json(data_path)
            container = load_container_from_json(data_path)

            # Serialize models once per file block to save processing time
            container_dict = container.container_to_dict()
            warehouse_dict = warehouse.warehouse_to_dict()

            for p in heuristic_parameters:
                for n_pop in n_pops:
                    
                    # Prepare parallel tasks
                    tasks = []
                    for j in range(30):
                        task_params = {
                            "run_idx": j,
                            "data_path": data_path,
                            "heuristic_parameter": p,
                            "n_pop": n_pop,
                            "container_dict": container_dict,
                            "warehouse_dict": warehouse_dict
                        }
                        tasks.append(task_params)

                    # Execute in parallel
                    with multiprocessing.Pool(processes=min(30,num_cores)) as pool:
                        results = pool.map(worker, tasks)

                    list_of_logs = [result[1] for result in results]
                    solutions = [result[0] for result in results]

                    # Obtain the best solution's log
                    best_result_tuple = max(results, key=lambda result: result[1].iloc[-1]['max'])
                    absolute_best_log = best_result_tuple[1]

                    # Agreggate the data
                    df_all_runs = pd.concat(list_of_logs)
                    df_mean_evolution = df_all_runs.groupby('gen').mean().reset_index()
                    
                    # Save metrics
                    aggregated_csv = f"aggregated_{i}_{p[0]}_{p[1]}_{n_pop}.csv"
                    best_csv = f"best_{i}_{p[0]}_{p[1]}_{n_pop}.csv"
                    results_dir = f"results/complete/rts/{name_path}/"
                    os.makedirs(results_dir, exist_ok=True)

                    # Create the path for saving the data
                    aggregated_path = os.path.join(results_dir, aggregated_csv)
                    best_path = os.path.join(results_dir, best_csv)

                    # Save the data
                    df_mean_evolution.to_csv(aggregated_path, index=False)
                    absolute_best_log.to_csv(best_path, index=False)

                    print(f"--> Absolute Best Fitness reached: {absolute_best_log.iloc[-1]['max']}")
                    print(f"--> Saved aggregated metrics to: {aggregated_path}")
        

if __name__ == "__main__":
    main()