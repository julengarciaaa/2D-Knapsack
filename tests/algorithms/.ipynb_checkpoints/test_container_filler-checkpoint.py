from model.container import Container
from model.piece import Piece
from model.warehouse import Warehouse
from algorithms.container_filler import ContainerFiller
from visuals.state_visuals import plot_container_state

# Container configuration (Dimensions: 20x30)
container = Container(width=20, length=30)

# Initialize Warehouse with diverse stock
warehouse = Warehouse()

# Pieces designed to complement dimensions (summing to 10)
for _ in range(10):
    warehouse.add_piece(Piece(5, 2))  # (5+5) fills the width
    warehouse.add_piece(Piece(3, 2))  
    warehouse.add_piece(Piece(7, 2))  # (3+7) fills the width
    warehouse.add_piece(Piece(4, 3))
    warehouse.add_piece(Piece(6, 3))  # (4+6) fills the width
    warehouse.add_piece(Piece(2, 2))  # Small fillers

# Large base pieces for layer structure
for _ in range(3):
    warehouse.add_piece(Piece(10, 4)) 

# Configure Filler
filler = ContainerFiller(n1=2, n2=1, s_depth=2, s_width=3)

# Execute the multi-layer filling algorithm
best_state = filler.fill_container(container, warehouse, n1=5, n2=3)

# Result analysis and visualization
if best_state is not None:
    final_container = best_state.get_container()
    plot_container_state(best_state)
else:
    print("\nSolution not found.")