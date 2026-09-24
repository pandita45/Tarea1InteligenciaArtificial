import random
from statistics import mean, stdev

from BFS import bfs
from agente import Agente
from mapa import Mapa
from nodos import ESTADO
from ASTAR import astar
from GREEDY import greedy
from DFS import dfs
from ALGORITMOGENETICO import algoritmo_genetico
import time
import numpy as np

# Mapas y algoritmos a evaluar[cite: 2]
MAPAS = ["1", "2", "3"] # 1 cuello de botella, 2 dispersion abierta, 3 laberinto corporativo
ALGORITMOS = {
    "BFS": bfs,
    "DFS": dfs,
    "Greedy": greedy,
    "A_Star": astar,
    "Genetico": algoritmo_genetico
}

NUM_AGENTES = 30
ITERACIONES = 200  
ARCHIVO_SALIDA = "resultados_benchmark.txt"

def obtener_inicio(mapa):
    # Se obtiene un nodo de inicio aleatorio que no sea una muralla o muy cerca de la salida
    lim_superior = (mapa.filas - 1) // 2 # Limite superior para evitar que el nodo de inicio esté demasiado cerca de la salida

    while True:
        x = random.randint(0, lim_superior)
        y = random.randint(0, mapa.columnas - 1)
        nodo = mapa.grilla[x, y]

        if nodo.estado == ESTADO.transitable and not nodo.lleno():  # Verifica que el nodo sea transitable y no esté lleno
            #se actualiza su capacidad
            nodo.actualizar_costo(1) 
            return nodo


def propagacion_fuego(k, mapa):
    nuevos_quemados = set()
    
    for i in range(mapa.filas):
        for j in range(mapa.columnas):
            nodo = mapa.grilla[i, j]
            if nodo.estado == ESTADO.quemado:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = i + dx, j + dy
                    if 0 <= nx < mapa.filas and 0 <= ny < mapa.columnas:
                        vecino = mapa.grilla[nx, ny]
                        if vecino.estado == ESTADO.transitable:
                            nuevos_quemados.add(vecino)

    for vecino in nuevos_quemados:
        vecino.estado = ESTADO.quemado
        vecino.actualizar_costo(1)
        
def ejecutar_benchmark():

    for algoritmo in ALGORITMOS:
        for mapa in MAPAS:
            
            for iteracion in range(ITERACIONES):
                id_agente = 0

                agentes = [Agente(id_agente:=id_agente+1, obtener_inicio(mapa), ALGORITMOS[algoritmo], mapa.obtener_salida()) for i in range(NUM_AGENTES)]