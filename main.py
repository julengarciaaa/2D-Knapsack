import time
import random
from model.container import Container
from model.warehouse import Warehouse
from model.piece import Piece
from algorithms.solver import Solver 

def create_hard_test_data():
    """
    Escenario: 'The Tetris Bottleneck'
    Contenedor largo y estrecho con piezas que tienen dimensiones 
    que NO son múltiplos entre sí, forzando huecos (gaps).
    """
    # Contenedor de 100x13 (El 13 es un número primo, difícil de llenar con piezas estándar)
    container = Container(length=100, width=13)

    inventory = {
        # Piezas tipo 'Lamas': Muy largas pero estrechas
        Piece(20, 2): 10,
        # Piezas 'Obstáculo': Dimensiones primas que rompen la simetría
        Piece(7, 7): 5,
        Piece(11, 3): 8,
        # Piezas de relleno ineficiente
        Piece(5, 4): 12,
        Piece(3, 3): 15,
        # El 'Cebo': Una pieza muy grande que si la usas mal, bloquea todo
        Piece(15, 12): 2,
        # Piezas minúsculas: Generan muchísima búsqueda en el árbol (n1, n2 sufren)
        Piece(1, 1): 50
    }
    warehouse = Warehouse(inventory)
    
    return container, warehouse

def main():
    container, warehouse = create_hard_test_data()
    
    # PARÁMETROS DE ALTO RENDIMIENTO (Hard Mode)
    # Aumentamos n1 y n2 para que el Greedy no sea tan miope.
    # Aumentamos la población y generaciones para que el GA realmente evolucione.
    params = {
        "n1": 3,          # Exploración inicial amplia
        "n2": 2,           # Cada paso del greedy evalúa 5 ramas (búsqueda profunda)
        "s_depth": 4,      # LayerFiller buscará combinaciones de hasta 4 tipos de piezas
        "s_width": 4,
        "npop": 40,        # Población mayor para evitar convergencia prematura
        "ngen": 100,       # Más tiempo para que la mutación haga su magia
        "cxpb": 0.8,       # Cruce agresivo
        "mutpb": 0.4       # Mutación alta: si el problema es difícil, necesitamos desorden
    }

    print("--- [MODO DIFÍCIL] Iniciando Packing Solver ---")
    print(f"Contenedor Hostil: {container.length}x{container.width} (Área: {container.get_area()})")
    print(f"Diversidad de Inventario: {len(warehouse.inventory)} tipos")
    print("-" * 50)

    solver = Solver(
        container, 
        warehouse, 
        params["n1"], 
        params["n2"], 
        params["s_depth"], 
        params["s_width"]
    )

    start_time = time.time()
    
    # Ejecución del GA
    best_solution = solver.solve(
        npop=params["npop"], 
        ngen=params["ngen"], 
        cxpb=params["cxpb"], 
        mutpb=params["mutpb"]
    )
    
    end_time = time.time()

    print("\n" + "!"*50)
    print("ANÁLISIS DE RENDIMIENTO BAJO PRESIÓN")
    print("!"*50)
    print(f"Tiempo total: {end_time - start_time:.2f}s")
    print(f"Filling Rate Alcanzado: {best_solution.container.get_filling_rate() * 100:.4f}%")
    print(f"Eficiencia de Capas: {len(best_solution.container.get_layers())} capas generadas")
    
    # Análisis de fragmentación (Longitud desperdiciada)
    unused_L = container.length - best_solution.container.current_length
    print(f"Longitud perdida al final: {unused_L} unidades")

    if best_solution.container.get_filling_rate() < 0.85:
        print("\nRESULTADO: El algoritmo sufrió. Considera subir n2 o n_pop.")
    else:
        print("\nRESULTADO: Éxito rotundo. El GA superó las incompatibilidades geométricas.")

if __name__ == "__main__":
    main()