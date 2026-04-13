from model.container import Container
from model.piece import Piece
from model.warehouse import Warehouse
from algorithms.container_filler import ContainerFiller
from visuals.state_visuals import plot_container_state

# Container configuration (Dimensions: 20x30)
container = Container(width=20, length=30)

# Create the initial inventory dictionary
inventory_data = {
    Piece(5, 2): 10,
    Piece(3, 2): 10,
    Piece(7, 2): 10,
    Piece(4, 3): 10,
    Piece(6, 3): 10,
    Piece(2, 2): 10,
    
    # Large base pieces for layer structure
    Piece(10, 4): 3
}

warehouse = Warehouse(inventory_data)
# Configure Filler
filler = ContainerFiller(n1=4, n2=3, s_depth=2, s_width=3)

# Execute the multi-layer filling algorithm
best_state = filler.fill_container(container, warehouse)

# Result analysis and visualization
if best_state is not None:
    final_container = best_state.get_container()
    plot_container_state(best_state)
else:
    print("\nSolution not found.")