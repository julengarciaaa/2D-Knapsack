import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_layer_state(state):
    """Dibuja el contenedor, las piezas y los puntos de inserción (históricos y activos)."""
    layer = state.get_layer()
    layer_l = layer.get_length()
    layer_w = layer.get_width()

    fig, ax = plt.subplots(figsize=(8, 8))
    
    # 1. Configurar límites y cuadrícula
    ax.set_xlim(0, layer_l)
    ax.set_ylim(0, layer_w)
    ax.set_xticks(range(layer_l + 1))
    ax.set_yticks(range(layer_w + 1))
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_aspect('equal')

    # 2. Dibujar las piezas colocadas
    placements = state.get_placements()
    colores = plt.cm.get_cmap('Pastel1', max(len(placements), 1))

    for i, placement in enumerate(placements):
        x, y = placement.get_p_point()
        p_l = placement.get_length()
        p_w = placement.get_width()
        
        rect = patches.Rectangle((x, y), p_l, p_w, linewidth=1.5,
                                 edgecolor='black', facecolor=colores(i), alpha=0.8)
        ax.add_patch(rect)
        
        cx = x + p_l / 2
        cy = y + p_w / 2
        rot = " (R)" if placement.is_rotated() else ""
        ax.text(cx, cy, f"#{i+1}\n{p_l}x{p_w}{rot}", 
                color='black', weight='bold', fontsize=9,
                ha='center', va='center')

    # 3. Dibujar Puntos Históricos (los que ya no están activos)
    # Usamos set para evitar dibujar puntos duplicados si los hubiera
    active_points = set(state.get_p_points())
    # Nota: asegúrate de que en LayerState usas 'historic_p_points' (como en commit_placement)
    # o 'p_points_historic' (como en __init__). He usado historic_p_points por coherencia con tu commit.
    historic_all = getattr(state, 'historic_p_points', []) 
    
    for h_point in historic_all:
        if h_point not in active_points:
            ax.plot(h_point[0], h_point[1], 'x', color='gray', markersize=8, alpha=0.5)

    # 4. Dibujar Puntos Activos (donde el algoritmo buscará ahora)
    for a_point in active_points:
        ax.plot(a_point[0], a_point[1], 'o', markerfacecolor='red', 
                markeredgecolor='black', markersize=10, label='Active P-Point' if a_point == list(active_points)[0] else "")

    # 5. Título e información
    area_total = layer_l * layer_w
    plt.title(f"Covered area: {state.get_packed_value()} / {area_total} ({state.get_num_packed()} pieces)")
    plt.xlabel("Length (X) - Red dots: Active P-Points")
    plt.ylabel("Width (Y)")
    
    # Añadir una pequeña leyenda para los puntos
    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], marker='o', color='w', label='Active Point',
                              markerfacecolor='red', markersize=10, markeredgecolor='black'),
                       Line2D([0], [0], marker='x', color='gray', label='Used/Inactive',
                              markersize=8, linestyle='None')]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.show()

def plot_container_state(state):
    """
    Plots the entire container showing all its stacked layers.
    """
    container = state.get_container()
    cont_l = container.get_length()
    cont_w = container.get_width()
    layers = container.get_layers()

    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Set container boundaries
    ax.set_xlim(0, cont_l)
    ax.set_ylim(0, cont_w)
    
    # Draw grid
    ax.set_xticks(range(cont_l + 1))
    ax.set_yticks(range(cont_w + 1))
    ax.grid(True, linestyle=':', alpha=0.4)
    ax.set_aspect('equal')

    # X-axis offset to place each layer after the previous one
    current_x_offset = 0
    
    # Color map for the pieces
    cmap = plt.cm.get_cmap('Set3')

    for l_idx, layer in enumerate(layers):
        layer_l = layer.get_length()
        layer_w = layer.get_width()

        # Draw layer boundary (highlighting the layer itself)
        layer_rect = patches.Rectangle((current_x_offset, 0), layer_l, layer_w, 
                                     linewidth=2, edgecolor='red', facecolor='none', 
                                     linestyle='--', label=f'Layer {l_idx}' if l_idx == 0 else "")
        ax.add_patch(layer_rect)

        # Draw each placement inside the current layer
        for p_idx, placement in enumerate(layer.get_placements()):
            # Local coordinates within the layer
            lx, ly = placement.get_p_point()
            # Global coordinates within the container
            gx = current_x_offset + lx
            gy = ly
            
            p_l = placement.get_length()
            p_w = placement.get_width()
            
            # Unique color for each piece based on its index
            color = cmap((l_idx + p_idx) % 12)
            
            rect = patches.Rectangle((gx, gy), p_l, p_w, linewidth=1,
                                     edgecolor='black', facecolor=color, alpha=0.8)
            ax.add_patch(rect)
            
            # Add text with piece info
            ax.text(gx + p_l/2, gy + p_w/2, f"{p_l}x{p_w}", 
                    color='black', fontsize=7, ha='center', va='center')

        # Update offset for the next layer
        current_x_offset += layer_l

    plt.title(f"Container Filling: {container.get_filling_rate()*100:.2f}% "
              f"({len(layers)} Layers)")
    plt.xlabel("Total Length (X)")
    plt.ylabel("Width (Y)")
    plt.show()