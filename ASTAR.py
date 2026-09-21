import heapq
from nodos import Nodo, ESTADO




def funcion_Manhattan(a,b):
    return abs(a.x - b.x) + abs(a.y - b.y)



def astar(mapa, inicio, nodo_meta):
    # funcion heuristica = g(nodo) + h(nodo), g(nodo) = costo acumulado, h funcion manhattan
    g = {inicio: 0}  # Costo acumulado desde el nodo inicial hasta el nodo actual
    padres = {inicio: None}  # Diccionario para rastrear los padres de cada nodo


    f_inicial = funcion_Manhattan(inicio, nodo_meta)
    f = {inicio: f_inicial}  # Costo total estimado (g + h) para cada nodo

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


        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)

        for dx, dy in [(-1,0), (1,0), (0, -1), (0,1)]:
            nx, ny = nodo_actual.x + dx, nodo_actual.y + dy
            if 0 <= nx < mapa.filas and 0 <= ny < mapa.columnas:
                vecino = mapa.grilla[nx, ny]
                if vecino.estado in (ESTADO.transitable, ESTADO.salida) and not vecino.lleno():
                    g_nuevo = g[nodo_actual] + vecino.costo  # Costo acumulado desde el nodo inicial hasta el vecino
                    f_nuevo = g_nuevo + funcion_Manhattan(vecino, nodo_meta)  # Costo total estimado para el vecino

                    print(f"Evaluando vecino: {vecino.x}, {vecino.y}, g_nuevo: {g_nuevo}, f_nuevo: {f_nuevo}")
                    if vecino not in g or g_nuevo < g[vecino]:
                        print(f"Actualizando vecino: {vecino.x}, {vecino.y}, g: {g_nuevo}, f: {f_nuevo}")
                        g[vecino] = g_nuevo
                        f[vecino] = f_nuevo
                        padres[vecino] = nodo_actual  # Registrar el padre del vecino
                        heapq.heappush(frontera, (f_nuevo, vecino))  # Agregar el vecino a la frontera

    return None  # Si no se encuentra un camino a la salida