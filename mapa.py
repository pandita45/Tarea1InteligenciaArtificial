from pathlib import Path

import numpy as np
from nodos import ESTADO, Nodo


class Mapa:
    def __init__(self, opcion):
        self.salida = None
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
                elif char == 'F':
                    grilla[i, j] = Nodo(ESTADO.quemado, i, j)

        return grilla

    def obtener_salida(self):
        return self.salida
        
