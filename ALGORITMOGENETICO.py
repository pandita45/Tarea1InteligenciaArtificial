from nodos import Nodo, ESTADO
import random


MOVIMIENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class cromosoma:
    def __init__(self, genes):
        self.genes = genes #lista de tuplas que representan los movimientos [(-1,0), (-1,0), (0,1), ...])
        self.camino = [] #lista de nodos que representan el camino que se recorre con los genes
        self.fitness = 0.0 
        self.costo_total = 0.0 
        self.nodo_final = None #nodo final al que se llega con el camino
        self.penalizacion = 0.0 #penalización por llegar a un nodo quemado o lleno, a mayor penalización, peor es el camino
        self.llego_a_meta = False 


def distancia_manhattan(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)
                                
def evaluar_fitness(cromosoma, mapa, inicio, nodo_meta):
    nodo_actual = inicio
    camino = [inicio]
    costo_acumulado = 0
    penalizaciones = 0
    llego = False

    for dx, dy in cromosoma.genes:
        nx = nodo_actual.x + dx
        ny = nodo_actual.y + dy

        #se penaliza si se sale del mapa o si se entra a un nodo quemado o lleno
        if not (0 <= nx < mapa.filas and 0 <= ny < mapa.columnas):
            penalizaciones += 15
            continue

        vecino = mapa.grilla[nx, ny]

        if vecino.estado not in (ESTADO.transitable, ESTADO.salida):
            penalizaciones += 30
            continue

        if vecino.lleno():
            penalizaciones += 15
            continue

        nodo_actual = vecino
        costo_acumulado += vecino.costo
        camino.append(nodo_actual)

        if nodo_actual == nodo_meta:
            llego = True
            break

    cromosoma.camino = camino
    cromosoma.nodo_final = nodo_actual
    cromosoma.costo_total = costo_acumulado
    cromosoma.penalizacion = penalizaciones
    cromosoma.llego_a_meta = llego


    dist = distancia_manhattan(nodo_actual, nodo_meta)
    fitness = 1000 / (dist + 1)

    if llego:
        pasos_dados = len(camino)
        fitness += 5000 + (500 / pasos_dados)

    fitness -= (costo_acumulado * 1.5) + penalizaciones
    cromosoma.fitness = fitness
    return cromosoma.fitness

def seleccion_torneo(poblacion, k=3):
    aspirantes = random.sample(poblacion, k)
    #retorna el individuo con mayor fitness
    return max(aspirantes, key=lambda ind: ind.fitness)





def algoritmo_genetico(mapa, inicio, nodo_meta, tam_poblacion=30, generaciones=50, tasa_mutacion=0.15):
    
    dist_base = distancia_manhattan(inicio, nodo_meta)
    longitud_genes = max(15, int(dist_base * 2.0))

    # población inicial
    poblacion = [
        cromosoma([random.choice(MOVIMIENTOS) for _ in range(longitud_genes)])
        for _ in range(tam_poblacion)
    ]

    mejor_historico = None


    for _ in range(generaciones):
        # Evaluar fitness de cada individuo en la población
        for ind in poblacion:
            evaluar_fitness(ind, mapa, inicio, nodo_meta)

        # Ordenar de mejor a peor fitness
        poblacion.sort(key=lambda ind: ind.fitness, reverse=True)

        # Guardar el mejor individuo de la generación actual
        if mejor_historico is None or poblacion[0].fitness > mejor_historico.fitness:
            mejor_historico = poblacion[0]

        # Si el mejor de esta generación ya llegó a la meta, se devuelve la ruta
        if poblacion[0].llego_a_meta:
            return poblacion[0].camino

        # Se conservan los dos mejores individuos para la siguiente generación
        nueva_poblacion = [
            cromosoma(poblacion[0].genes[:]),
            cromosoma(poblacion[1].genes[:])
        ]

        # Reproducción (Torneo + Cruce + Mutación)
        while len(nueva_poblacion) < tam_poblacion:
            padre_a = seleccion_torneo(poblacion)
            padre_b = seleccion_torneo(poblacion)

            # Cruce de genes con un punto aleatorio 
            punto = random.randint(1, longitud_genes - 1)
            genes_hijo = padre_a.genes[:punto] + padre_b.genes[punto:]

            # Mutación genética, cada gen tiene una probabilidad de mutar a un movimiento aleatorio
            for i in range(longitud_genes):
                if random.random() < tasa_mutacion:
                    genes_hijo[i] = random.choice(MOVIMIENTOS)

            # Crear un nuevo cromosoma con los genes del hijo y agregarlo a la nueva población
            nueva_poblacion.append(cromosoma(genes_hijo))

        # Actualizar la población para la siguiente generación
        poblacion = nueva_poblacion

    # Si se agotan las generaciones, retorna el mejor camino alcanzado
    return mejor_historico.camino if mejor_historico else []