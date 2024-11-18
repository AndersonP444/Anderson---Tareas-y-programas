class Deque:
    def __init__(self):
        self.__deque = [] # inicializa una lista vacia para simular el deque
    
    def agg_primero(self, item):
        """Agregar un elemento a la parte inicial del deque."""
        self.__deque.insert(0, item) # insertar el elemento al inicio de la lista
    
    def remove_primero(self):
        """Remover y retornar un elemonto a la parte inicial del deque: """
        if not self.esta_vacio():
            return self.__deque.pop(0) # remover y retornar el primer elemento
        else:
            raise IndexError("Deque vacio, no se puede remover el primer elemento. ")
    
    def agg_ultimo(self, item):
        """agregar un elemento a la parte final del deque: """
        self.__deque.append(item) # agregar el ultimo al final de la lista

    def remove_ultimo(self):
        """remover y retornar un elemento a la parte final del deque: """
        if not self.esta_vacio():
            return self.__deque.pop() # remueve y retorna el ultimo elemento
        else:
            raise IndexError("Deque vacio, no se puede remover el ultimo elemento. ")
    
    def esta_vacio(self):
        """Retornar True si el deque esta vacio, de lo contrario False. """
        return len(self.__deque) == 0
    
    def tamano(self):
        """Retorna el numero de elementos del deque. """
        return len(self.__deque)
    
    def __str__(self):
        """Devuelve una representacion en string del deque. """
        return str(self.__deque)
    
deque = Deque()

# agregar elementos al inicio y final
ro = int(input("Ingrese el primer numero: "))
do = int(input("Ingrese el segundo numero: "))
roo = int(input("Ingrese el tercer numero: "))
deque.agg_primero(ro)     
deque.agg_ultimo(do)
deque.agg_primero(roo)

print(f"deque actual (elementos añadidos): {deque} ") # muestra el deque actual

# remover elementos del inicio y del final
primer_elemento = deque.remove_primero()
ultimo_elemento = deque.remove_ultimo()

print(f"primer elemento removido: {primer_elemento}")
print(f"ultimo elemento removido: {ultimo_elemento}")

print(f"""(elementos removidos, completado) 
Deque actual: {deque} """) # deque actual despues de las remociones