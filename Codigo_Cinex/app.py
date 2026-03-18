import os
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'encuesta.db')

def inicializar_db():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    # Usamos nombres cortos p1, p2... p13 para que SQL no de errores de sintaxis
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS respuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            p1 TEXT, p2 TEXT, p3 TEXT, p4 TEXT, p5 TEXT,
            p6 TEXT, p7 TEXT, p8 TEXT, p9 TEXT, p10 TEXT,
            p11 TEXT, p12 TEXT, p13 TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

# Inicializamos la base de datos
inicializar_db()

@app.route('/')
def home():
    return render_template('encuesta.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    # Recolectamos las 13 respuestas p1 a p13 que vienen del HTML
    respuestas = [request.form.get(f'p{i}') for i in range(1, 14)]
    
    # Si falta alguna respuesta, detenemos el proceso
    if None in respuestas:
        return "<h3>Error: Por favor responde todas las preguntas.</h3><a href='/'>Volver</a>", 400

    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        
        # Hay exactamente 13 nombres de columnas y 13 signos de "?"
        query = """INSERT INTO respuestas (p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        
        cursor.execute(query, respuestas)
        conexion.commit()
        conexion.close()
        return "<h1>¡Gracias!</h1><p>Tu opinión ha sido registrada con éxito.</p><a href='/'>Volver</a>"
    
    except Exception as e:
        return f"Ocurrió un error al guardar: {e}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)