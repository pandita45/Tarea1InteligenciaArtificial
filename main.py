import numpy as np
from BFS import bfs
from agente import Agente
from mapa import Mapa
from nodos import ESTADO
from ASTAR import astar
from GREEDY import greedy
from ALGORITMOGENETICO import algoritmo_genetico

def buscar_nodo_salida(grilla):
    for i in range(grilla.shape[0]):
        for j in range(grilla.shape[1]):
            if grilla[i, j].estado == ESTADO.salida:
                return (i, j)
    return None


mapa = Mapa(3)  # Cargar el mapa de cuello de botella
x,y = buscar_nodo_salida(mapa.grilla)

agente1 = Agente(1, mapa.grilla[1, 2], bfs, mapa.grilla[x, y])  # Crear un agente en la posición (0, 0) usando BFS
print(f"Agente en posición: ({agente1.nodo_actual.x}, {agente1.nodo_actual.y})")
# Simulación de movimiento del agente
for _ in range(30):
    agente1.mover(mapa)
    print(f"Agente en posición: ({agente1.nodo_actual.x}, {agente1.nodo_actual.y})")
    if agente1.evacuado:
        print("El agente ha evacuado con éxito.")
        break
    elif agente1.atrapado:
        print("El agente ha quedado atrapado.")
        break



mapa2 = Mapa(3)
print("ALO KIKE")
agente2 = Agente(2, mapa2.grilla[1, 2], bfs, mapa2.grilla[x, y])  # Crear un agente en la posición (0, 0) usando BFS
print(f"Agente en posición: ({agente2.nodo_actual.x}, {agente2.nodo_actual.y})")
# Simulación de movimiento del agente
for _ in range(30):
    agente2.mover(mapa2)
    print(f"Agente en posición: ({agente2.nodo_actual.x}, {agente2.nodo_actual.y})")
    if agente2.evacuado:
        print("El agente ha evacuado con éxito.")
        break
    elif agente2.atrapado:
        print("El agente ha quedado atrapado.")
        break


mapa3 = Mapa(3)
agente3 = Agente(3, mapa3.grilla[1, 2], astar, mapa3.grilla[x, y])  # Crear un agente en la posición (0, 0) usando A*
print(f"Agente en posición: ({agente3.nodo_actual.x}, {agente3.nodo_actual.y})")
# Simulación de movimiento del agente
for _ in range(40):
    agente3.mover(mapa3)
    print(f"Agente en posición: ({agente3.nodo_actual.x}, {agente3.nodo_actual.y})")
    if agente3.evacuado:
        print("El agente ha evacuado con éxito.")
        break
    elif agente3.atrapado:
        print("El agente ha quedado atrapado.")
        break