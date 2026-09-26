from collections import deque
from nodos import ESTADO

def bfs(mapa, inicio, meta_nodo = None): #Para hacer mas universal el algoritmo, no tiene ninguna función meta_nodo
    #iniciar la cola con el nodo inicial
    cola = deque([inicio])
    visitados = set()
    visitados.add(inicio)
    padres = {inicio: None}  # Diccionario para rastrear los padres de cada nodo
    while cola:
        nodo_actual = cola.popleft()
        if nodo_actual.estado == ESTADO.salida:
            # Reconstruir el camino desde el nodo de salida hasta el nodo inicial
            camino = []

            while nodo_actual is not None:
                camino.append(nodo_actual)
                nodo_actual = padres[nodo_actual]
            return camino[::-1]  # Devolver el camino en orden desde inicio hasta salida
        else:
            #explorar los vecinos del nodo actual y encolar los que no han sido visitados
            for dx, dy in [(-1,0), (1,0), (0, -1), (0,1)]:
                nx, ny = nodo_actual.x + dx, nodo_actual.y + dy
                if 0 <= nx < mapa.filas and 0 <= ny < mapa.columnas:
                    vecino = mapa.grilla[nx, ny]
                    if vecino.estado in (ESTADO.transitable, ESTADO.salida) and vecino not in visitados:
                        visitados.add(vecino)
                        padres[vecino] = nodo_actual  # Registrar el padre del vecino
                        cola.append(vecino)


    return None  # Si no se encuentra un camino a la salida
