from nodos import ESTADO, Nodo
from collections import deque

def dfs(mapa, inicio, meta_nodo = None): #Para hacer mas universal el algoritmo, no tiene ninguna función meta_nodo
    #iniciar la pila con el nodo inicial
    pila = deque([inicio])
    visitados = set()
    padres = {inicio: None}  # Diccionario para rastrear los padres de cada nodo
    while pila:
        nodo_actual = pila.pop()
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)
        
        if nodo_actual.estado == ESTADO.salida:
            # Reconstruir el camino desde el nodo de salida hasta el nodo inicial
            camino = []
            while nodo_actual is not None:
                camino.append(nodo_actual)
                nodo_actual = padres[nodo_actual]
            return camino[::-1]  # Devolver el camino en orden desde inicio hasta salida
        else:
            #explorar los vecinos del nodo actual y apilar los que no han sido visitados
            for dx, dy in [(-1,0), (1,0), (0, -1), (0,1)]:
                nx, ny = nodo_actual.x + dx, nodo_actual.y + dy
                if 0 <= nx < mapa.filas and 0 <= ny < mapa.columnas:
                    vecino = mapa.grilla[nx, ny]
                    if vecino.estado in (ESTADO.transitable, ESTADO.salida) and vecino not in visitados:
                        visitados.add(vecino)
                        padres[vecino] = nodo_actual  # Registrar el padre del vecino
                        pila.append(vecino)

    return None  # Si no se encuentra un camino a la salida