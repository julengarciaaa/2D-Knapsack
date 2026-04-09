import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_layer_state(state):
    """Dibuja el contenedor y las piezas colocadas usando Matplotlib."""
    layer = state.get_layer()
    layer_l = layer.get_length()
    layer_w = layer.get_width()

    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Configurar los límites del contenedor
    ax.set_xlim(0, layer_l)
    ax.set_ylim(0, layer_w)
    
    # Dibujar una cuadrícula para ver mejor las coordenadas
    ax.set_xticks(range(layer_l + 1))
    ax.set_yticks(range(layer_w + 1))
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Asegurar que los ejes tengan la misma proporción (1x1 se vea cuadrado)
    ax.set_aspect('equal')

    # Generar colores distintos para las piezas
    colores = plt.cm.get_cmap('Pastel1', len(state.get_placements()))

    for i, placement in enumerate(state.get_placements()):
        x, y = placement.get_p_point()
        piece = placement.get_piece()
        p_l = placement.get_length()
        p_w = placement.get_width()
        
        # Crear el rectángulo
        rect = patches.Rectangle((x, y), p_l, p_w, linewidth=1.5,
                                 edgecolor='black', facecolor=colores(i))
        ax.add_patch(rect)
        
        # Poner un texto en el centro de la pieza (Orden y dimensiones)
        cx = x + p_l / 2
        cy = y + p_w / 2
        rot = " (R)" if placement.is_rotated else ""
        ax.text(cx, cy, f"#{i+1}\n{p_l}x{p_w}{rot}", 
                color='black', weight='bold', fontsize=9,
                ha='center', va='center')

    plt.title(f"Covered area: {state.get_packed_value()} / {layer_l * layer_w}")
    plt.xlabel("Length (X)")
    plt.ylabel("Width (Y)")
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