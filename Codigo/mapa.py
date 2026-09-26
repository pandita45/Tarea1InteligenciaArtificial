from pathlib import Path

import numpy as np
from nodos import ESTADO, Nodo
from random import randint

def distancia_manhattan(nodo1, nodo2):
    return abs(nodo1.x - nodo2.x) + abs(nodo1.y - nodo2.y)
class Mapa:
    def __init__(self, opcion):
        self.salida = None
        self.spawn = None
        self.grilla = self.cargar_mapa(opcion)
        self.filas, self.columnas = self.grilla.shape

    def cargar_mapa(self, opcion):
        if opcion == 1:
            nombre_mapa = "cuelloBotella.txt"
        elif opcion == 2:
            nombre_mapa = "dispersionAbierta.txt"
        elif opcion == 3:
            nombre_mapa = "laberintoCorporativo.txt"
        else:
            raise ValueError("Opción de mapa no válida. Debe ser 1, 2 o 3.")

        ruta = Path(__file__).parent / "Mapas" / nombre_mapa
        with open(ruta, 'r', encoding='utf-8') as f:
            lineas = [linea.strip() for linea in f.readlines() if linea.strip()]

        filas = len(lineas)
        columnas = len(lineas[0].strip())
        grilla = np.empty((filas, columnas), dtype=object)

        for i, linea in enumerate(lineas):
            for j, char in enumerate(linea):
                if char == '.':
                    grilla[i, j] = Nodo(ESTADO.transitable, i, j)
                elif char == '#':
                    grilla[i, j] = Nodo(ESTADO.muro, i, j)
                elif char == 'S':
                    grilla[i, j] = Nodo(ESTADO.salida, i, j)
                    self.salida = grilla[i, j]
                elif char == 'A':
                    grilla[i, j] = Nodo(ESTADO.transitable, i, j)
                    self.spawn = grilla[i, j]
                  

        random_x = 0
        random_y = 0
        #El fuego no puede estar a menos de 5 nodos de la salida ni a menos de 3 nodos del spawn
        while grilla[random_x, random_y].estado != ESTADO.transitable or distancia_manhattan(grilla[random_x, random_y], self.salida) < 5 or distancia_manhattan(grilla[random_x, random_y], self.spawn) < 3:
            random_x = randint(0, filas - 1)
            random_y = randint(0, columnas - 1)

        grilla[random_x, random_y] = Nodo(ESTADO.quemado, random_x, random_y)
        return grilla

    def obtener_salida(self):
        return self.salida

    def obtener_spawn(self):
        return self.spawn
        
