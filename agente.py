
from nodos import ESTADO, Nodo

class Agente:
    def __init__(self, id_agente, inicio_nodo, algoritmo, nodo_meta):
        self.id = id_agente
        self.nodo_actual = inicio_nodo
        self.camino = [] #lista de nodos a recorrer dado por los algoritmos
        self.algoritmo = algoritmo #El algoritmo que ejecutara el agente para encontrar el mejor camino
        self.indice_paso = 0 #Para saber en que parte de la ruta se encuentra el agente
        self.atrapado = False
        self.evacuado = False
        self.nodo_meta = nodo_meta

    def calcular_ruta(self, mapa):
        ruta = self.algoritmo(mapa, self.nodo_actual, self.nodo_meta)
        if ruta and len(ruta) > 1: #por si el agente queda acorralado en fuegos o no encuentra camino
            self.camino = ruta
            self.indice_paso = 0
        else:
            self.camino = [] #no se encontró camino

        
    def mover(self, mapa):
        if self.evacuado or self.atrapado:
            return #si ya murió o evacuó no se mueve

        #se comprueba que no le alcanzo el fuego
        if self.nodo_actual.estado == ESTADO.quemado:
            self.atrapado = True
            return

        #si no tiene ruta, calcula 1, ideal en la primera iteración
        if len(self.camino) == 0:
            self.calcular_ruta(mapa)
            if len(self.camino) == 0: #si no encuentra ruta, se queda en su lugar
                return

        siguiente_mov = self.camino[self.indice_paso + 1]
        #si su siguiente movimiento es en una casilla quemada, se recalcula ruta
        if siguiente_mov.estado == ESTADO.quemado:
            self.calcular_ruta(mapa)
    

        #si la siguiente celda tiene alguna persona o aglomeración, se recalcula la ruta, para confirmar si sigue siendo la mejor opción
        if siguiente_mov.costo > 1.0 and self.tiene_alternativas(mapa):
            self.calcular_ruta(mapa)
    

        self.nodo_actual.personas = self.nodo_actual.personas - 1
        self.nodo_actual = siguiente_mov
        self.nodo_actual.personas = self.nodo_actual.personas + 1
        self.indice_paso += 1

        if self.nodo_actual.estado == ESTADO.salida:
            self.evacuado = True
            return

            #determina si puede encontrar otra solución o esta obligado a irse al siguiente nodo
    def tiene_alternativas(self, mapa):
        #como si o si tendrá 2 alternativas, si encuentra otro nodo libre, puede haber otra solución al camino
        cont = 0
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = self.nodo_actual.x + dx, self.nodo_actual.y + dy
            if 0 <= nx < mapa.filas and 0 <= ny < mapa.columnas:
                vecino = mapa.grilla[nx,ny]
                if vecino.estado in [ESTADO.transitable, ESTADO.salida]:
                    cont += 1
                
        return cont > 2

            

        