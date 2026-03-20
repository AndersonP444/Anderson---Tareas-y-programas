import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'encuesta.db')

if not os.path.exists(DB_PATH):
    print("La base de datos aún no existe. Llena la encuesta primero.")
else:
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM respuestas")
    filas = cursor.fetchall()
    
    print(f"\nSe han encontrado {len(filas)} encuestas guardadas.\n")
    for f in filas:
        print(f"ID: {f[0]} | Email: {f[2]} | Gasto (P15): {f[17]} | Sugerencia: {f[21]}")
    
    conexion.close()