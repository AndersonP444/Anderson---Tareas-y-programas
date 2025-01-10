import json
import os
import requests
from base64 import b64encode, b64decode
import tkinter as tk
from tkinter import messagebox, simpledialog

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

# Funciones de sincronización con GitHub
def cargar_datos_desde_github():
    try:
        response = requests.get(GITHUB_API_BASE)
        if response.status_code == 200:
            content = response.json()
            decoded_content = b64decode(content["content"]).decode()
            return json.loads(decoded_content)
        elif response.status_code == 404:
            return base_de_datos_BANK_OF_NAO
        else:
            return base_de_datos_BANK_OF_NAO
    except Exception as e:
        return base_de_datos_BANK_OF_NAO

def guardar_datos_en_github(datos):
    try:
        contenido = json.dumps(datos, indent=4)
        contenido_encoded = b64encode(contenido.encode()).decode()

        response = requests.get(GITHUB_API_BASE, headers={
            "Authorization": f"token {GITHUB_TOKEN}"
        })
        sha_actual = response.json()["sha"] if response.status_code == 200 else None

        payload = {
            "message": "Actualización de la base de datos del BANK OF NAO.",
            "content": contenido_encoded,
            "branch": BRANCH
        }
        if sha_actual:
            payload["sha"] = sha_actual

        response = requests.put(GITHUB_API_BASE, headers={
            "Authorization": f"token {GITHUB_TOKEN}"
        }, json=payload)

        if response.status_code not in [200, 201]:
            raise Exception(f"Error al subir datos: {response.status_code}")
    except Exception as e:
        print(f"Error al guardar datos en GitHub: {e}")

# Base de datos cargada desde GitHub
data = cargar_datos_desde_github()

# Funciones bancarias
def crear_usuario():
    nombre_completo = simpledialog.askstring("Nuevo Usuario", "Ingrese el nombre completo:")
    cedula = simpledialog.askstring("Nuevo Usuario", "Ingrese la cédula:")
    usuario_banco = simpledialog.askstring("Nuevo Usuario", "Ingrese el nombre de usuario:")
    clave_usuario_banco = simpledialog.askinteger("Nuevo Usuario", "Ingrese la clave de usuario:")
    saldo_Bs = simpledialog.askfloat("Nuevo Usuario", "Ingrese el saldo inicial en Bs:")
    tipo_de_cuenta = simpledialog.askstring("Nuevo Usuario", "Ingrese el tipo de cuenta (ahorro/corriente):")
    if tipo_de_cuenta:
        tipo_de_cuenta = tipo_de_cuenta.lower()

    nuevo_usuario = {
        "nombre_completo": nombre_completo,
        "cedula": cedula,
        "usuario_banco": usuario_banco,
        "clave_usuario_banco": clave_usuario_banco,
        "saldo_Bs": saldo_Bs,
        "tipo_de_cuenta": tipo_de_cuenta
    }

    data['usuarios'].append(nuevo_usuario)
    guardar_datos_en_github(data)
    messagebox.showinfo("Usuario Creado", f"El usuario {nombre_completo} ha sido creado exitosamente.")

def buscar_usuario(usuario_banco, clave_usuario_banco):
    for usuario in data['usuarios']:
        if usuario['usuario_banco'] == usuario_banco and usuario['clave_usuario_banco'] == clave_usuario_banco:
            return usuario
    return None

def estado_cuenta(usuario):
    messagebox.showinfo("Estado de Cuenta", f"Saldo actual: {usuario['saldo_Bs']} Bs")

def deposito(usuario):
    monto = simpledialog.askfloat("Depósito", "Ingrese el monto a depositar:")
    if monto:
        usuario['saldo_Bs'] += monto
        guardar_datos_en_github(data)
        messagebox.showinfo("Depósito", f"Depósito exitoso. Nuevo saldo: {usuario['saldo_Bs']} Bs")

def retiro(usuario):
    monto = simpledialog.askfloat("Retiro", "Ingrese el monto a retirar:")
    if monto:
        if monto > usuario['saldo_Bs']:
            messagebox.showerror("Error", "Fondos insuficientes.")
        else:
            usuario['saldo_Bs'] -= monto
            guardar_datos_en_github(data)
            messagebox.showinfo("Retiro", f"Retiro exitoso. Nuevo saldo: {usuario['saldo_Bs']} Bs")

def transferencia(usuario):
    cedula_destino = simpledialog.askstring("Transferencia", "Ingrese la cédula del destinatario:")
    monto = simpledialog.askfloat("Transferencia", "Ingrese el monto a transferir:")

    if cedula_destino and monto:
        usuario_destino = next((u for u in data['usuarios'] if u['cedula'] == cedula_destino), None)
        if usuario_destino:
            if monto > usuario['saldo_Bs']:
                messagebox.showerror("Error", "Fondos insuficientes.")
            else:
                usuario['saldo_Bs'] -= monto
                usuario_destino['saldo_Bs'] += monto
                guardar_datos_en_github(data)
                messagebox.showinfo("Transferencia", f"Transferencia exitosa. Nuevo saldo: {usuario['saldo_Bs']} Bs")
        else:
            messagebox.showerror("Error", "Usuario destinatario no encontrado.")

def iniciar_sesion():
    usuario_banco = simpledialog.askstring("Iniciar Sesión", "Ingrese su nombre de usuario:")
    clave_usuario_banco = simpledialog.askinteger("Iniciar Sesión", "Ingrese su clave:")

    usuario_actual = buscar_usuario(usuario_banco, clave_usuario_banco)

    if usuario_actual:
        messagebox.showinfo("Bienvenido", f"Bienvenido, {usuario_actual['nombre_completo']}")

        while True:
            opcion = simpledialog.askstring("Operaciones", "1. Estado de cuenta\n2. Depósito\n3. Retiro\n4. Transferencia\n5. Salir")

            if opcion == "1":
                estado_cuenta(usuario_actual)
            elif opcion == "2":
                deposito(usuario_actual)
            elif opcion == "3":
                retiro(usuario_actual)
            elif opcion == "4":
                transferencia(usuario_actual)
            elif opcion == "5":
                break
            else:
                messagebox.showerror("Error", "Opción no válida.")
    else:
        messagebox.showerror("Error", "Credenciales incorrectas.")

# Configurar la ventana principal
root = tk.Tk()
root.title("BANK OF NAO")

frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

btn_login = tk.Button(frame, text="Iniciar Sesión", command=iniciar_sesion)
btn_login.pack(pady=5)

btn_new_user = tk.Button(frame, text="Crear Usuario", command=crear_usuario)
btn_new_user.pack(pady=5)

root.mainloop()


