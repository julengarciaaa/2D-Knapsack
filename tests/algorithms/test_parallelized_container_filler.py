import time
from model.container import Container
from model.piece import Piece
from model.warehouse import Warehouse
from algorithms.container_filler import ContainerFiller

def run_test(n1_value, container, warehouse):
    print(f"\n--- Testing with n1 = {n1_value} ---")
    filler = ContainerFiller(n1=n1_value, n2=3, s_depth=2, s_width=3)
    
    start_time = time.time()
    best_state = filler.fill_container(container, warehouse)[0]
    end_time = time.time()
    
    duration = end_time - start_time
    if best_state:
        fr = best_state.get_container().get_filling_rate()
        print(f"Time taken: {duration:.4f} seconds")
        print(f"Best Filling Rate: {fr:.2%}")
    else:
        print("No solution found.")
    return duration

def main():
    # Setup inicial
    container = Container(width=20, length=30)
    inventory_data = {
        Piece(5, 2): 10, Piece(3, 2): 10, Piece(7, 2): 10,
        Piece(4, 3): 10, Piece(6, 3): 10, Piece(2, 2): 10,
        Piece(10, 4): 3
    }
    warehouse = Warehouse(inventory_data)

    time_2 = run_test(n1_value=2, container=container, warehouse=warehouse)

    time_8 = run_test(n1_value=8, container=container, warehouse=warehouse)

    print(f"\nResumen: n1=8 tardó {time_8/time_2:.2f}x veces lo que tardó n1=2")

if __name__ == "__main__":
    main()