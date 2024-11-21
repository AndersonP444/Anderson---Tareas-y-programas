import streamlit as st
import json
import requests
from base64 import b64encode, b64decode

# Configuración de GitHub
GITHUB_TOKEN = "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"  # Reemplaza con tu token de acceso personal
GITHUB_USERNAME = "AndersonP444"
REPO_NAME = "Anderson---Tareas-y-programas"
FILE_PATH = "Base de datos del BANK OF NAO.json"
BRANCH = "main"

GITHUB_API_BASE = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{FILE_PATH}"

# Cargar datos desde GitHub
def cargar_datos_desde_github():
    try:
        response = requests.get(GITHUB_API_BASE)
        if response.status_code == 200:
            content = response.json()
            decoded_content = b64decode(content["content"]).decode()
            return json.loads(decoded_content)
        elif response.status_code == 404:
            return {"usuarios": []}
        else:
            st.error(f"Error al cargar datos desde GitHub: {response.status_code}")
            return {"usuarios": []}
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return {"usuarios": []}

# Guardar datos en GitHub
def guardar_datos_en_github(datos):
    try:
        contenido = json.dumps(datos, indent=5)
        contenido_encoded = b64encode(contenido.encode()).decode()
        response = requests.get(GITHUB_API_BASE, headers={"Authorization": f"token {GITHUB_TOKEN}"})
        sha_actual = response.json()["sha"] if response.status_code == 200 else None
        payload = {"message": "Actualización de la base de datos", "content": contenido_encoded, "branch": BRANCH}
        if sha_actual:
            payload["sha"] = sha_actual
        response = requests.put(GITHUB_API_BASE, headers={"Authorization": f"token {GITHUB_TOKEN}"}, json=payload)
        if response.status_code not in [200, 201]:
            st.error(f"Error al guardar datos en GitHub: {response.status_code}")
    except Exception as e:
        st.error(f"Error al guardar datos en GitHub: {e}")

# Funciones del sistema bancario
def crear_usuario(datos):
    st.title("Crear un nuevo usuario")
    nombre = st.text_input("Nombre completo")
    cedula = st.text_input("Cédula")
    usuario_banco = st.text_input("Usuario del banco")
    clave = st.text_input("Clave de usuario", type="password")
    saldo = st.number_input("Saldo inicial (Bs)", min_value=0.0, step=0.01)
    tipo_cuenta = st.selectbox("Tipo de cuenta", ["ahorro", "corriente"])

    if st.button("Crear usuario"):
        nuevo_usuario = {"nombre_completo": nombre, "cedula": cedula, "usuario_banco": usuario_banco,
                         "clave_usuario_banco": clave, "saldo_Bs": saldo, "tipo_de_cuenta": tipo_cuenta}
        datos["usuarios"].append(nuevo_usuario)
        guardar_datos_en_github(datos)
        st.success(f"Usuario {nombre} creado exitosamente")

def mostrar_estado(usuario):
    st.write(f"Estado de cuenta de {usuario['nombre_completo']}: {usuario['saldo_Bs']} Bs")

def realizar_deposito(usuario, datos):
    monto = st.number_input("Monto a depositar", min_value=0.0, step=0.01)
    if st.button("Realizar depósito"):
        usuario["saldo_Bs"] += monto
        guardar_datos_en_github(datos)
        st.success(f"Depósito realizado. Nuevo saldo: {usuario['saldo_Bs']} Bs")

def realizar_retiro(usuario, datos):
    monto = st.number_input("Monto a retirar", min_value=0.0, step=0.01)
    if st.button("Realizar retiro"):
        if monto > usuario["saldo_Bs"]:
            st.error("Fondos insuficientes")
        else:
            usuario["saldo_Bs"] -= monto
            guardar_datos_en_github(datos)
            st.success(f"Retiro realizado. Nuevo saldo: {usuario['saldo_Bs']} Bs")

def realizar_transferencia(usuario, datos):
    cedula_destino = st.text_input("Cédula del destinatario")
    monto = st.number_input("Monto a transferir", min_value=0.0, step=0.01)

    if st.button("Realizar transferencia"):
        usuario_destino = next((u for u in datos["usuarios"] if u["cedula"] == cedula_destino), None)
        if not usuario_destino:
            st.error("Usuario destino no encontrado")
        elif monto > usuario["saldo_Bs"]:
            st.error("Fondos insuficientes")
        else:
            usuario["saldo_Bs"] -= monto
            usuario_destino["saldo_Bs"] += monto
            guardar_datos_en_github(datos)
            st.success(f"Transferencia realizada. Nuevo saldo: {usuario['saldo_Bs']} Bs")

# Interfaz principal
def main():
    datos = cargar_datos_desde_github()

    st.sidebar.title("Sistema Bancario - BANK OF NAO")
    opcion = st.sidebar.selectbox("Seleccione una opción", ["Iniciar sesión", "Crear usuario"])

    if opcion == "Crear usuario":
        crear_usuario(datos)
    elif opcion == "Iniciar sesión":
        usuario_banco = st.sidebar.text_input("Usuario del banco")
        clave = st.sidebar.text_input("Clave", type="password")

        if st.sidebar.button("Iniciar sesión"):
            usuario = next((u for u in datos["usuarios"] if u["usuario_banco"] == usuario_banco and str(u["clave_usuario_banco"]) == clave), None)
            if usuario:
                st.success(f"Bienvenido {usuario['nombre_completo']}")
                accion = st.selectbox("Seleccione una acción", ["Estado de cuenta", "Depósito", "Retiro", "Transferencia"])
                if accion == "Estado de cuenta":
                    mostrar_estado(usuario)
                elif accion == "Depósito":
                    realizar_deposito(usuario, datos)
                elif accion == "Retiro":
                    realizar_retiro(usuario, datos)
                elif accion == "Transferencia":
                    realizar_transferencia(usuario, datos)
            else:
                st.error("Usuario o clave incorrecta")

if __name__ == "__main__":
    main()
