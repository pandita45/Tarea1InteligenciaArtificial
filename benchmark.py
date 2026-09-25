
import random
import time
from statistics import mean, stdev

import numpy as np

from BFS import bfs
from DFS import dfs
from GREEDY import greedy
from ASTAR import astar
from ALGORITMOGENETICO import algoritmo_genetico

from agente import Agente
from mapa import Mapa
from nodos import ESTADO

MAPAS = ["1", "2", "3"]
ALGORITMOS = {
    "BFS": bfs,
    "DFS": dfs,
    "Greedy": greedy,
    "A_Star": astar,
    "Genetico": algoritmo_genetico,
}

NUM_AGENTES = 80
ITERACIONES = 200
K_FUEGO = 3
MAX_TURNOS = 100
ARCHIVO_SALIDA = "resultados_benchmark.txt"


def obtener_inicio(mapa):
    lim_superior = (mapa.filas - 1) // 2
    while True:
        x = random.randint(0, lim_superior)
        y = random.randint(0, mapa.columnas - 1)
        nodo = mapa.grilla[x, y]

        if nodo.estado == ESTADO.transitable and not nodo.lleno():
            nodo.actualizar_costo(1)
            return nodo


def propagacion_fuego(mapa):
    nuevos_quemados = set()  # Se inicializa el conjunto de los que se quemarán en esta iteración

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
    tiempo_inicio_total = time.time()

    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.write("=" * 85 + "\n")
        f.write("               REPORTE DE BENCHMARKING\n")
        f.write("=" * 85 + "\n")
        f.write(f"Configuracion: {NUM_AGENTES} agentes | {ITERACIONES} iteraciones | k_fuego={K_FUEGO}\n")
        f.write("-" * 85 + "\n")
        f.write(f"{'Mapa':<12} | {'Algoritmo':<10} | {'Superv.(%)':<10} | {'Media':<7} | {'Std':<7} | {'Min':<5} | {'Max':<5}\n")
        f.write("-" * 85 + "\n")
        f.flush()

        for id_mapa in MAPAS:
            for nombre_alg, func_alg in ALGORITMOS.items():
                print(f"Ejecutando {nombre_alg} en Mapa {id_mapa}...")

                tasas_supervivencia = []
                turnos_despeje = []

                for iteracion in range(ITERACIONES):
                    # Crear el mapa
                    mapa_actual = Mapa(int(id_mapa))
                    nodo_salida = mapa_actual.obtener_salida()

                    # Asignar posiciones iniciales, y crear, a los agentes
                    id_agente = 0
                    agentes = [
                        Agente(
                            id_agente := id_agente + 1,
                            mapa_actual.obtener_spawn(),
                            func_alg,
                            nodo_salida,
                        )
                        for _ in range(NUM_AGENTES)
                    ]

                    turnos_evacuacion = {}

                    # Bucle de turnos de la simulación
                    for turno in range(1, MAX_TURNOS + 1):
                        # Mover a cada agente activo
                        for agente in agentes:
                            if not agente.evacuado and not agente.atrapado:
                                agente.mover(mapa_actual)
                                if agente.evacuado:
                                    turnos_evacuacion[agente.id] = turno

                        # Propagación del fuego cada K_FUEGO turnos
                        if turno % K_FUEGO == 0:
                            propagacion_fuego(mapa_actual)

                            # Verificar si las llamas atraparon agentes
                            for agente in agentes:
                                if not agente.evacuado and not agente.atrapado:
                                    if agente.nodo_actual.estado == ESTADO.quemado:
                                        agente.atrapado = True

                        # Terminar la iteración si ya no hay agentes activos
                        if all(agente.evacuado or agente.atrapado for agente in agentes):
                            break

                    # Ver cuantos agentes lograron evacuar
                    evacuados = 0
                    for a in agentes:
                        if a.evacuado:
                            evacuados += 1

                    # Calcular la tasa de supervivencia
                    tasas_supervivencia.append((evacuados / NUM_AGENTES) * 100.0)

                    if turnos_evacuacion:
                        turnos_despeje.append(max(turnos_evacuacion.values()))

                # Estadísticas de las 200 iteraciones
                sup_media = mean(tasas_supervivencia)

                #en caso de que no haya agentes que hayan logrado evacuar, se evita calcular
                if turnos_despeje:
                    turnos_media = mean(turnos_despeje)
                    turnos_min = min(turnos_despeje)
                    turnos_max = max(turnos_despeje)

                    if len(turnos_despeje) > 1:
                        turnos_std = stdev(turnos_despeje)
                    else:
                        turnos_std = 0.0
                else:
                    turnos_media = 0.0
                    turnos_std = 0.0
                    turnos_min = 0
                    turnos_max = 0

                linea = (
                    f"Mapa {id_mapa:<7} | "
                    f"{nombre_alg:<10} | "
                    f"{sup_media:>9.2f}% | "
                    f"{turnos_media:>7.2f} | "
                    f"{turnos_std:>7.2f} | "
                    f"{turnos_min:>5} | "
                    f"{turnos_max:>5}\n"
                )
                f.write(linea)
                f.flush()
                print(f" -> Finalizado: {linea.strip()}")

        duracion_min = (time.time() - tiempo_inicio_total) / 60
        f.write("=" * 85 + "\n")
        f.write(f"Tiempo total: {duracion_min:.2f} minutos\n")

    print(f"\nBenchmark completo guardado en {ARCHIVO_SALIDA}")


if __name__ == "__main__":
    ejecutar_benchmark()