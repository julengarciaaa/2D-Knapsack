from algorithms.solver_dts import Solver
from model.piece import Piece
from model.warehouse import Warehouse
from model.container import Container
from visuals.state_visuals import plot_container_state

def run_test():
    params = {
        "n_pop": 20, 
        "n_gen": 30,
        "n_rep": 2,
        "cxpb": 0.7,
        "mutpb": 0.3,
        "n1": 1,          
        "n2": 1,           
        "s_depth": 1,      
        "s_width": 1,
    }

    # Definición de piezas (Datos del problema)
    inventory_data = {
        Piece(5, 2): 10,
        Piece(3, 2): 10,
        Piece(7, 2): 10,
        Piece(4, 3): 10,
        Piece(6, 3): 10,
        Piece(2, 2): 10,
        Piece(10, 4): 3
    }

    warehouse = Warehouse(inventory_data)
    container = Container(width=20, length=30)

    # 1. Instanciar el Solver con los parámetros de configuración
    # Usamos **params para "desempaquetar" el diccionario automáticamente
    solver = Solver(**params)

    population = solver.generate_initial_population(n_pop=2, container=container, warehouse=warehouse)

    for individual in population:
        plot_container_state(individual)

    child, _ = solver.crossover(population[0], population[1])
    plot_container_state(child)

if __name__ == "__main__":
    run_test()
