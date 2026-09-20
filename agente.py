
from BFS import bfs
from nodos import ESTADO

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

        if not inicio_nodo.actualizar_costo(1):
            raise ValueError("El nodo inicial del agente está lleno o no admite personas")

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

        if self.indice_paso + 1 >= len(self.camino):
            self.calcular_ruta(mapa)
            if len(self.camino) <= 1:
                return

        siguiente_mov = self.camino[self.indice_paso + 1]
        # No se puede entrar a una casilla quemada o que ya alcanzó su capacidad.
        if siguiente_mov.estado == ESTADO.quemado or siguiente_mov.lleno():
            self.calcular_ruta(mapa)
            if len(self.camino) <= 1:
                return
            siguiente_mov = self.camino[self.indice_paso + 1]

        if siguiente_mov.estado == ESTADO.quemado or siguiente_mov.lleno():
            return
    

        #si la siguiente celda tiene alguna persona o aglomeración, se recalcula la ruta, para confirmar si sigue siendo la mejor opción

        if siguiente_mov.costo > 1.0 and self.tiene_alternativas(mapa):
            self.calcular_ruta(mapa)
            siguiente_mov = self.camino[self.indice_paso + 1]


        if not siguiente_mov.actualizar_costo(1):
            return

        self.nodo_actual.actualizar_costo(-1)
        self.nodo_actual = siguiente_mov
        self.indice_paso += 1

        if self.nodo_actual.estado == ESTADO.salida:
            self.evacuado = True
            self.nodo_actual.actualizar_costo(-1)  # Liberar el nodo de salida al evacuar
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

            

        