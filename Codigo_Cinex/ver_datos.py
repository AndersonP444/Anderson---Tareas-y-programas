# ver_datos.py actualizado
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'encuesta.db')

conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

try:
    cursor.execute("SELECT * FROM respuestas")
    filas = cursor.fetchall()
    print(f"\n--- TOTAL DE ENCUESTAS: {len(filas)} ---\n")
    
    for fila in filas:
        # fila[0]=ID, fila[1]=Fecha, del [2] al [14] son p1 a p13
        fecha = fila[1]
        p_satisfaccion_final = fila[14] 
        print(f"ID: {fila[0]} | Fecha: {fecha} | Satisfacción Final: {p_satisfaccion_final}")
        # Opcional: imprimir todas las respuestas en una línea
        print(f"   Detalle p1-p13: {fila[2:15]}")
        print("-" * 50)
        
except sqlite3.OperationalError:
    print("Error: La tabla aún no existe o la ruta es incorrecta.")

conexion.close()