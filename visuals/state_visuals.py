import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_state(state):
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
        p_l = piece.get_length()
        p_w = piece.get_width()
        
        # Crear el rectángulo
        rect = patches.Rectangle((x, y), p_l, p_w, linewidth=1.5,
                                 edgecolor='black', facecolor=colores(i))
        ax.add_patch(rect)
        
        # Poner un texto en el centro de la pieza (Orden y dimensiones)
        cx = x + p_l / 2
        cy = y + p_w / 2
        rot = " (R)" if piece.ov else ""
        ax.text(cx, cy, f"#{i+1}\n{p_l}x{p_w}{rot}", 
                color='black', weight='bold', fontsize=9,
                ha='center', va='center')

    plt.title(f"Empaquetado - Área cubierta: {state.get_packed_value()} / {layer_l * layer_w}")
    plt.xlabel("Largo (X)")
    plt.ylabel("Ancho (Y)")
    plt.show()