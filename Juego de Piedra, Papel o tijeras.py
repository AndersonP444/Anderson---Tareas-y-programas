import random

def jugar_piedra_papel_tijeras():
    opciones = ['piedra', 'papel', 'tijeras']
    
    print("Bienvenido al juego de Piedra, Papel o Tijeras.")
    print("Selecciona una opción: ")
    print("1. Piedra")
    print("2. Papel")
    print("3. Tijeras")
    
    # Entrada del jugador
    eleccion_jugador = int(input("Escribe el número de tu elección (1, 2 o 3): "))
    if eleccion_jugador < 1 or eleccion_jugador > 3:
        print("Elección inválida. Intenta nuevamente.")
        return

    # Traducir elección a piedra, papel o tijeras
    eleccion_jugador = opciones[eleccion_jugador - 1]
    print(f"Has elegido: {eleccion_jugador}")
    
    # Elección de la computadora
    eleccion_computadora = random.choice(opciones)
    print(f"La computadora ha elegido: {eleccion_computadora}")
    
    # Determinar el ganador
    if eleccion_jugador == eleccion_computadora:
        print("Es un empate!")
    elif (eleccion_jugador == 'piedra' and eleccion_computadora == 'tijeras') or \
         (eleccion_jugador == 'papel' and eleccion_computadora == 'piedra') or \
         (eleccion_jugador == 'tijeras' and eleccion_computadora == 'papel'):
        print("¡Has ganado!")
    else:
        print("Has perdido. La computadora ha ganado.")

# Llamada a la función para jugar
jugar_piedra_papel_tijeras()
