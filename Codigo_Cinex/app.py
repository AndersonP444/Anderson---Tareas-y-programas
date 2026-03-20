import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'encuesta.db')

def obtener_hora_venezuela():
    return datetime.utcnow() - timedelta(hours=4)

def inicializar_db():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    # Creamos la tabla con espacio para 17 preguntas (p1 a p17)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS respuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT, email TEXT, complejo TEXT,
            p1 TEXT, p2 TEXT, p3 TEXT, p4 TEXT, p5 TEXT,
            p6 TEXT, p7 TEXT, p8 TEXT, p9 TEXT, p10 TEXT,
            p11 TEXT, p12 TEXT, p13 TEXT, p14 TEXT, p15 TEXT, p16 TEXT, p17 TEXT,
            comentario TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

inicializar_db()

@app.route('/')
def home():
    return render_template('encuesta.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    try:
        email = request.form.get('email')
        complejo = request.form.get('complejo')
        # Capturamos p1 hasta p17
        respuestas = [request.form.get(f'p{i}') for i in range(1, 18)]
        comentario = request.form.get('comentario', '')

        if None in respuestas or not email or not complejo:
            return "<h3>Error: Faltan respuestas.</h3><a href='/'>Volver</a>", 400

        fecha_ve = obtener_hora_venezuela().strftime('%Y-%m-%d %H:%M:%S')

        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        # Datos para insertar: fecha, email, complejo, 17 preguntas y comentario (Total 21 campos)
        # Pero el ID es NULL, así que ponemos NULL y luego 20 valores con "?"
        datos = [fecha_ve, email, complejo] + respuestas + [comentario]

        query = "INSERT INTO respuestas VALUES (NULL, " + ",".join(["?"]*21) + ")"

        cursor.execute(query, datos)
        conexion.commit()
        conexion.close()
        return redirect(url_for('home'))
    except Exception as e:
        return f"<h3>Error: {e}</h3><a href='/'>Volver</a>", 500

if __name__ == '__main__':
    app.run(debug=True)