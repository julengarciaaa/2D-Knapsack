from model.container import Container
from model.piece import Piece
from model.warehouse import Warehouse
from algorithms.container_filler import ContainerFiller
from visuals.state_visuals import plot_container_state

# 1. Initialize the container dimensions
# We define a container where multiple layers can be stacked
container = Container(width=6, length=20)

# 2. Setup the warehouse and add pieces
warehouse = Warehouse()
# Adding various pieces to test the filling logic
warehouse.add_piece(Piece(2, 3))
warehouse.add_piece(Piece(2, 2))
warehouse.add_piece(Piece(2, 4))
warehouse.add_piece(Piece(2, 1))
warehouse.add_piece(Piece(4, 1))
warehouse.add_piece(Piece(1, 1))
warehouse.add_piece(Piece(4, 1))
warehouse.add_piece(Piece(5, 1))
warehouse.add_piece(Piece(2, 2))
warehouse.add_piece(Piece(2, 3))
warehouse.add_piece(Piece(3, 2))
warehouse.add_piece(Piece(6, 2)) # Wide piece to test layer filling
warehouse.add_piece(Piece(3, 3))

# 3. Initialize the ContainerFiller with search parameters
# n1: candidates for the first layer
# n2: candidates for subsequent layers
# s_depth/s_width: parameters for the internal LayerFillerNG
filler = ContainerFiller(n1=3, n2=2, s_depth=2, s_width=3)

# 4. Run the container filling algorithm
# This will search for the best combination of layers
best_state = filler.fill_container(container, warehouse, n1=5, n2=4)

# 5. Check results and visualize
if best_state is not None:
    print(f"Best solution found!")
    print(f"Final Filling Rate: {best_state.get_container().get_filling_rate() * 100:.2f}%")
    # Visualize the final state (container with all its layers)
    plot_container_state(best_state)
else:
    print("\nCould not find a valid solution for the container.")