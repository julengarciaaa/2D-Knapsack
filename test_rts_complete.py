import sys
import os
import pandas as pd

from src.algorithms.container_filler_rts import ContainerFillerRTS
from src.algorithms.layer_filler_rts import LayerFillerRTS
from src.algorithms.solver_rts import SolverRTS
from src.visuals.state_visuals import plot_container_state
from src.utils.data_loader import load_container_from_json, load_warehouse_from_json

def main():
    set_paths = ["src/data/set3/JAKOBS/", "src/data/set4/HOPPER/"]
    name_paths = ["JAKOBS", "HOPPER"]

    for set_path, name_path in zip(set_paths, name_paths):
        for i in range(1, 6):
            data_path = set_path + str(i) + ".json"

            heuristic_parameters = [(1, 1), (3, 2)]
            n_pops = [10, 30, 50]

            warehouse = load_warehouse_from_json(data_path)
            container = load_container_from_json(data_path)

            for p in heuristic_parameters:
                for n_pop in n_pops:
                    list_of_logs = []
                    for j in range(30):
                        print("Execution: " + str(j))
                        print("Problem: " + data_path)
                        print("Heuristic parameters: " + str(p))
                        print("Population size: " + str(n_pop))
                        print("N_rep: " + str(int(n_pop * 0.1)))

                        layer_filler = LayerFillerRTS(s_depth=p[0], s_width=p[1])
                        container_filler = ContainerFillerRTS(n1=p[0], n2=p[1], layer_filler=layer_filler)

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

                        list_of_logs.append(df_log)

                        df_all_runs = pd.concat(list_of_logs)
                        df_mean_evolution = df_all_runs.groupby('gen').mean().reset_index()
                    

                    name_csv = str(i) + "_" + str(p[0]) + "_" + str(p[1]) + "_" + str(n_pop) + ".csv"
                    results_path = "results/complete/rts/" + name_path + "/" + name_csv
                    df_mean_evolution.to_csv(results_path, index=False)
        

if __name__ == "__main__":
    main()