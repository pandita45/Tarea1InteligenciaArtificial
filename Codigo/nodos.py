
from enum import Enum

class ESTADO(Enum):
    transitable = 0
    muro = 1
    quemado = 2
    salida = 3
    
class Nodo: 
    def __init__(self, estado : ESTADO, x : int, y : int):
        self.estado = estado

        self.costo = self.funcionCosto(0) # Inicializa el costo del nodo según la función f con 0 personas
        self.personas = 0
        self.capacidad = 20 # Capacidad máxima de personas en el nodo
        self.x = x
        self.y = y
        
    def funcionCosto(self, personas):
        if self.estado in [ESTADO.muro, ESTADO.quemado]:
            return float('inf') # Costo infinito para nodos que son muros o quemados
        return 1 + personas * 2 # Función de costo: f(x) = 1 + 2 * x, donde x es el número de personas en el nodo
    
    def actualizar_costo(self, accion): # Toma 1 si 1 persona entró al nodo y -1 si salió
        if accion == -1 and self.personas == 0:
            return False # No se puede quitar personas si no hay ninguna en el nodo
        if accion == 1 and self.personas == self.capacidad:
            return False # No se puede agregar más personas si se alcanza la capacidad máxima
        
        self.personas += accion # Actualiza el número de personas en el nodo
        self.costo = self.funcionCosto(self.personas) # Actualiza el costo del nodo según la función f
        return True # Retorna True si la actualización fue exitosa

    def __lt__(self, otro):
        return False

    def lleno(self):
        return self.personas == self.capacidad
