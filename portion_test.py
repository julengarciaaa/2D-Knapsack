import portion as P

# 1. Definimos tus bordes con el hueco que mencionas (de 4 a 5 no hay nada)
# horizontal_edges[2] tiene [2, 4) y [5, 6)
horizontal_edges_2 = P.closedopen(2, 4) | P.closedopen(5, 6)

# 2. Tu nuevo intervalo (Nota: he usado closedopen para ser consistente)
# Queremos ver cuánto toca de 3 a 6
intervalo_nuevo = P.closedopen(3, 6)

# 3. Calculamos la INTERSECCIÓN
# Esto nos da los trozos donde REALMENTE se tocan
contacto = intervalo_nuevo & horizontal_edges_2

# 4. Sumamos las longitudes
# contacto será: [3, 4) | [5, 6)
touching_points = 0
for interval in contacto:
    print(interval)
    touching_points += (interval.upper - interval.lower)

print(f"Segmentos de contacto: {contacto}")
print(f"Unidades de Touching Point: {touching_points}") 
# Resultado: (4-3) + (6-5) = 2 unidades