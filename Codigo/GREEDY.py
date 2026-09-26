
import heapq

from nodos import ESTADO


def distancia_manhattan(a,b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def greedy(mapa, inicio, nodo_meta):

    padres = {inicio: None}  # Diccionario para rastrear los padres de cada nodo
    f_inicial = distancia_manhattan(inicio, nodo_meta) # f = h(nodo)
    visitados = set()  # Conjunto para rastrear los nodos visitados
    frontera = [(f_inicial, inicio)]  # Cola de prioridad para los nodos a explorar
    while frontera:
        f_actual, nodo_actual = heapq.heappop(frontera)  # Extrae el nodo con el menor costo total estimado


        if nodo_actual == nodo_meta:
            camino = [] 
            while nodo_actual is not None:
                    camino.append(nodo_actual)
                    nodo_actual = padres[nodo_actual]
            return camino[::-1]  # Devolver el camino en orden desde inicio hasta salida
        # Evitar reexplorar nodos y ciclos infinitos
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # Explorar los vecinos del nodo actual
            nx, ny = nodo_actual.x + dx, nodo_actual.y + dy
            if 0 <= nx < mapa.filas and 0 <= ny < mapa.columnas:
                vecino = mapa.grilla[nx, ny]
                if vecino.estado in (ESTADO.transitable, ESTADO.salida) and not vecino.lleno(): # Si el vecino es transitable o es la salida y no está lleno, se considera para la exploración
                    if vecino not in visitados and vecino not in padres:  # Evitar reexplorar nodos y ciclos infinitos
                        padres[vecino] = nodo_actual
                        f_nuevo = distancia_manhattan(vecino, nodo_meta)
                        heapq.heappush(frontera, (f_nuevo, vecino))

    return None  # Si no se encuentra un camino a la salida