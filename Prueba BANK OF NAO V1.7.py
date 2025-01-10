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

# Funciones de backend

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
        contenido = json.dumps(datos, indent=5)
        contenido_encoded = b64encode(contenido.encode()).decode()

        response = requests.get(GITHUB_API_BASE, headers={"Authorization": f"token {GITHUB_TOKEN}"})
        sha_actual = response.json()["sha"] if response.status_code == 200 else None

        payload = {
            "message": "Actualización de la base de datos del BANK OF NAO.",
            "content": contenido_encoded,
            "branch": BRANCH
        }
        if sha_actual:
            payload["sha"] = sha_actual

        response = requests.put(GITHUB_API_BASE, headers={"Authorization": f"token {GITHUB_TOKEN}"}, json=payload)

        if response.status_code not in [200, 201]:
            messagebox.showerror("Error", f"Error al subir datos a GitHub: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar datos en GitHub: {e}")

def buscar_usuario_por_credenciales(usuario_banco, clave_usuario_banco, datos):
    for usuario in datos['usuarios']:
        if usuario['usuario_banco'] == usuario_banco and usuario['clave_usuario_banco'] == clave_usuario_banco:
            return usuario
    return None

def crear_usuario(datos):
    nombre_completo = simpledialog.askstring("Crear Usuario", "Ingrese el nombre completo:")
    cedula = simpledialog.askstring("Crear Usuario", "Ingrese la cédula:")
    usuario_banco = simpledialog.askstring("Crear Usuario", "Ingrese el nombre de usuario para el banco:")
    clave_usuario_banco = simpledialog.askinteger("Crear Usuario", "Ingrese la clave de usuario:")
    saldo_Bs = simpledialog.askfloat("Crear Usuario", "Ingrese el saldo inicial en Bs:")
    tipo_de_cuenta = simpledialog.askstring("Crear Usuario", "Ingrese el tipo de cuenta (ahorro/corriente):")

    nuevo_usuario = {
        "nombre_completo": nombre_completo,
        "cedula": cedula,
        "usuario_banco": usuario_banco,
        "clave_usuario_banco": clave_usuario_banco,
        "saldo_Bs": saldo_Bs,
        "tipo_de_cuenta": tipo_de_cuenta
    }

    datos['usuarios'].append(nuevo_usuario)
    guardar_datos_en_github(datos)
    messagebox.showinfo("Éxito", f"Usuario {nombre_completo} creado exitosamente.")

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

# Interfaz gráfica
class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BANK OF NAO")
        self.root.geometry("400x300")

        self.datos = cargar_datos_desde_github()
        self.usuario_actual = None

        # Elementos de la interfaz principal
        self.label_titulo = tk.Label(root, text="BANK OF NAO", font=("Arial", 18))
        self.label_titulo.pack(pady=10)

        self.btn_login = tk.Button(root, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.btn_login.pack(pady=5)

        self.btn_registro = tk.Button(root, text="Crear Usuario", command=self.crear_usuario_gui)
        self.btn_registro.pack(pady=5)

    def iniciar_sesion(self):
        usuario_banco = simpledialog.askstring("Iniciar Sesión", "Ingrese su nombre de usuario:")
        clave_usuario_banco = simpledialog.askinteger("Iniciar Sesión", "Ingrese su clave de usuario:")

        self.usuario_actual = buscar_usuario_por_credenciales(usuario_banco, clave_usuario_banco, self.datos)

        if self.usuario_actual:
            messagebox.showinfo("Bienvenido", f"Bienvenido, {self.usuario_actual['nombre_completo']}!")
            self.menu_usuario()
        else:
            messagebox.showerror("Error", "Usuario o clave incorrecta.")

    def crear_usuario_gui(self):
        crear_usuario(self.datos)

    def menu_usuario(self):
        menu = tk.Toplevel(self.root)
        menu.title("Menú del Usuario")

        if self.usuario_actual:
            tk.Label(menu, text=f"Bienvenido, {self.usuario_actual['nombre_completo']}", font=("Arial", 14)).pack(pady=10)

            tk.Button(menu, text="Estado de Cuenta", command=lambda: self.ver_estado_cuenta(menu)).pack(pady=5)
            tk.Button(menu, text="Depósito", command=lambda: self.realizar_deposito(menu)).pack(pady=5)
            tk.Button(menu, text="Retiro", command=lambda: self.realizar_retiro(menu)).pack(pady=5)
        else:
            messagebox.showerror("Error", "No se pudo cargar el menú del usuario.")

    def ver_estado_cuenta(self, menu):
        saldo = estado_cuenta(self.usuario_actual)
        messagebox.showinfo("Estado de Cuenta", f"Su saldo actual es: {saldo} Bs.")

    def realizar_deposito(self, menu):
        monto = simpledialog.askfloat("Depósito", "Ingrese el monto a depositar:")
        if monto:
            nuevo_saldo = deposito(self.usuario_actual, monto)
            guardar_datos_en_github(self.datos)
            messagebox.showinfo("Depósito", f"Depósito realizado. Nuevo saldo: {nuevo_saldo} Bs.")

    def realizar_retiro(self, menu):
        monto = simpledialog.askfloat("Retiro", "Ingrese el monto a retirar:")
        if monto:
            resultado = retiro(self.usuario_actual, monto)
            if isinstance(resultado, str):
                messagebox.showerror("Error", resultado)
            else:
                guardar_datos_en_github(self.datos)
                messagebox.showinfo("Retiro", f"Retiro realizado. Nuevo saldo: {resultado} Bs.")

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()