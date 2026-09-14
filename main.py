import numpy as np
from mapa import Mapa
from nodos import ESTADO

def propagarFuego(mapa):
    lista_quemados = []
    for x in range(mapa.filas):
        for y in range(mapa.columnas):
            if mapa.grilla[x,y].estado == ESTADO.quemado and (x, y) not in lista_quemados:
                for i in [(-1,0), (1,0), (0,-1), (0,1)]:  # Vecinos arriba, abajo, izquierda, derecha
                    nx, ny = x + i[0], y + i[1]
                    if 0 <= nx < mapa.filas and 0 <= ny < mapa.columnas:
                        vecino = mapa.grilla[nx, ny]
                        if vecino.estado == ESTADO.transitable: # no propagar el fuego a muros, quemados o salida
                            vecino.estado = ESTADO.quemado
                            vecino.costo = vecino.actualizar_costo(0)  # Actualiza el costo del nodo quemado
                            lista_quemados.append((nx, ny))

    
            

mapa = Mapa(1)  # Cargar el mapa de cuello de botella

mapa.grilla[0, mapa.columnas//2].estado = ESTADO.quemado  # Iniciar el fuego en el centro de la primera columna
for i in range(mapa.filas):
    for j in range(mapa.columnas):
        nodo = mapa.grilla[i, j]
        if nodo is not None:
            print(f"({i}, {j}): Estado={nodo.estado.name}, Costo={nodo.costo}, Personas={nodo.personas}")
        else:
            print(f"({i}, {j}): Nodo no definido")
