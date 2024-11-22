import json
import os
import requests
from base64 import b64encode, b64decode

# Configuración de GitHub
GITHUB_TOKEN = "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"  # Reemplaza con tu token de acceso personal
GITHUB_USERNAME = "AndersonP444"
REPO_NAME = "Anderson---Tareas-y-programas"
FILE_PATH = "Base de datos del BANK OF NAO.json"
BRANCH = "main"

# URL base para la API de GitHub
GITHUB_API_BASE = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{FILE_PATH}"

# Diccionario de la base de datos del banco (inicialmente vacío)
base_de_datos_BANK_OF_NAO = {
    "usuarios": []
}

# Función para cargar los datos desde GitHub
def cargar_datos_desde_github():
    try:
        response = requests.get(GITHUB_API_BASE)
        if response.status_code == 200:
            print("Datos cargados exitosamente desde GitHub.")
            content = response.json()
            decoded_content = b64decode(content["content"]).decode()
            return json.loads(decoded_content)
        elif response.status_code == 404:
            print("Archivo no encontrado en GitHub. Usando base de datos local.")
            return base_de_datos_BANK_OF_NAO
        else:
            print(f"Error al acceder al archivo en GitHub. Código: {response.status_code}")
            return base_de_datos_BANK_OF_NAO
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return base_de_datos_BANK_OF_NAO

# Función para guardar datos localmente y en GitHub
def guardar_datos_en_github(datos):
    try:
        # Convertir los datos a base64
        contenido = json.dumps(datos, indent=5)
        contenido_encoded = b64encode(contenido.encode()).decode()

        # Obtener el SHA del archivo actual en GitHub
        response = requests.get(GITHUB_API_BASE, headers={
            "Authorization": f"token {GITHUB_TOKEN}"
        })
        if response.status_code == 200:
            sha_actual = response.json()["sha"]
        else:
            sha_actual = None

        # Preparar payload para la actualización
        payload = {
            "message": "Actualización de la base de datos del BANK OF NAO.",
            "content": contenido_encoded,
            "branch": BRANCH
        }
        if sha_actual:
            payload["sha"] = sha_actual

        # Subir el archivo actualizado
        response = requests.put(GITHUB_API_BASE, headers={
            "Authorization": f"token {GITHUB_TOKEN}"
        }, json=payload)

        if response.status_code in [200, 201]:
            print("Datos guardados y subidos a GitHub exitosamente.")
        else:
            print(f"Error al subir datos a GitHub: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error al guardar datos en GitHub: {e}")

# Función para crear un nuevo usuario
def crear_usuario(datos):
    print("Creando un nuevo usuario...")
    nombre_completo = input("Ingrese el nombre completo: ")
    cedula = input("Ingrese la cédula: ")
    usuario_banco = input("Ingrese el nombre de usuario para el banco: ")
    clave_usuario_banco = int(input("Ingrese la clave de usuario: "))
    saldo_Bs = float(input("Ingrese el saldo inicial en Bs: "))
    tipo_de_cuenta = input("Ingrese el tipo de cuenta (ahorro/corriente): ").lower()

    # Crear el nuevo usuario
    nuevo_usuario = {
        "nombre_completo": nombre_completo,
        "cedula": cedula,
        "usuario_banco": usuario_banco,
        "clave_usuario_banco": clave_usuario_banco,
        "saldo_Bs": saldo_Bs,
        "tipo_de_cuenta": tipo_de_cuenta
    }

    # Agregar el nuevo usuario a la lista de usuarios
    datos['usuarios'].append(nuevo_usuario)
    
    # Guardar los datos actualizados en GitHub
    guardar_datos_en_github(datos)

    print(f"Usuario {nombre_completo} creado exitosamente.")

# Funciones para realizar las operaciones bancarias
def estado_cuenta(usuario):
    return usuario['saldo_Bs']

def deposito(usuario, monto):
    usuario['saldo_Bs'] += monto
    return usuario['saldo_Bs']

def retiro(usuario, monto):
    if monto > usuario['saldo_Bs']:
        return "Fondos insuficientes"
    else:
        usuario['saldo_Bs'] -= monto
        return usuario['saldo_Bs']

def transferencia(usuario, monto, usuario_destino, datos):
    if monto > usuario['saldo_Bs']:
        return "Fondos insuficientes"
    else:
        usuario['saldo_Bs'] -= monto
        usuario_destino['saldo_Bs'] += monto
        # Guardar los datos actualizados en GitHub
        guardar_datos_en_github(datos)
        return usuario['saldo_Bs'], usuario_destino['saldo_Bs']

# Menú de opciones
def menu():
    print("¿Qué operación desea realizar?")
    print("1. Estado de cuenta")
    print("2. Depósito")
    print("3. Retiro")
    print("4. Transferencia")
    print("5. Salir")
    return int(input("Ingrese una opción: "))

# Función para buscar usuario por credenciales (usuario_banco y clave_usuario_banco)
def buscar_usuario_por_credenciales(usuario_banco, clave_usuario_banco, datos):
    for usuario in datos['usuarios']:
        if usuario['usuario_banco'] == usuario_banco and usuario['clave_usuario_banco'] == clave_usuario_banco:
            return usuario
    return None

# Nueva función: Buscar usuario por cédula
def buscar_usuario_por_cedula(cedula, datos):
    for usuario in datos['usuarios']:
        if usuario['cedula'] == cedula:
            return usuario
    return None

# Nueva funcion: Buscar usuario por nombre completo
def buscar_usuario_por_nombre_completo(nombre_completo, datos):
    for usuario in datos['usuarios']:
        if usuario['nombre_completo'] == nombre_completo:
            return usuario
    return None

# Nueva funcion: Buscar usuario por tipo de cuenta
def buscar_usuario_por_tipo_de_cuenta(tipo_de_cuenta, datos):
    for usuario in datos['usuarios']:
        if usuario['tipo_de_cuenta'] == tipo_de_cuenta:
            return usuario
    return None


# Función principal
def main():
    datos = cargar_datos_desde_github()  # Cargar los datos desde GitHub al inicio

    while True:
        print("1. Iniciar sesión")
        print("2. Crear un nuevo usuario")
        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:  # Iniciar sesión
            usuario_banco = input("Ingrese su nombre de usuario: ")
            clave_usuario_banco = int(input("Ingrese su clave de usuario: "))

            usuario_actual = buscar_usuario_por_credenciales(usuario_banco, clave_usuario_banco, datos)

            if usuario_actual:
                print(f"Bienvenido, {usuario_actual['nombre_completo']}")

                while True:
                    opcion = menu()

                    if opcion == 1:  # Estado de cuenta
                        print(f"Estado de cuenta: {estado_cuenta(usuario_actual)}")
                    elif opcion == 2:  # Depósito
                        monto = int(input("Ingrese el monto a depositar: "))
                        print(f"Nuevo saldo: {deposito(usuario_actual, monto)}")
                        guardar_datos_en_github(datos)  # Guardar cambios en GitHub
                    elif opcion == 3:  # Retiro
                        monto = int(input("Ingrese el monto a retirar: "))
                        resultado = retiro(usuario_actual, monto)
                        print(resultado if isinstance(resultado, str) else f"Nuevo saldo: {resultado}")
                        guardar_datos_en_github(datos)  # Guardar cambios en GitHub
                    elif opcion == 4:  # Transferencia
                        monto = int(input("Ingrese el monto a transferir: "))
                        cedula_destino = input("Ingrese la cédula del usuario de destino: ")
                        nombre_destino = input("Ingrese el nombre completo del usuario de destino: ")
                        cuenta_destino = input("Ingrese el tipo de cuenta del usuario de destino: ")


                        # Buscar el usuario de destino por cédula, nombre y tipo de cuenta
                        usuario_destino = buscar_usuario_por_cedula(cedula_destino, datos)
                        usuario_destino1 = buscar_usuario_por_nombre_completo(nombre_destino, datos)
                        usuario_destino2 = buscar_usuario_por_tipo_de_cuenta(cuenta_destino, datos)


                        if usuario_destino:
                            resultado = transferencia(usuario_actual, monto, usuario_destino, datos)
                            print(resultado if isinstance(resultado, str) else f"Transferencia exitosa. Nuevo saldo: {resultado[0]}")
                        else:
                            print("Usuario de destino no encontrado.")
                    elif opcion == 5:  # Salir
                        print("Gracias por usar el sistema bancario del BANK OF NAO.")
                        break
                    else:
                        print("Opción no válida, intenta nuevamente.")

                    # Preguntar si desea realizar otra operación
                    continuar = input("¿Quieres realizar otra operación en tu cuenta? (si/no): ").lower()
                    if continuar != "si":
                        break
            else:
                print("Usuario o clave incorrecta, intenta nuevamente.")
        elif opcion == 2:  # Crear un nuevo usuario
            crear_usuario(datos)  # Llamar a la función para crear un nuevo usuario
        else:
            print("Opción no válida, intenta nuevamente.")

        # Preguntar si desea realizar otra operación bancaria
        continuar = input("¿Quieres realizar otra operación bancaria? (si/no): ").lower()
        if continuar != "si":
            break
# Ejecutar el programa
if __name__ == "__main__":
    main()
