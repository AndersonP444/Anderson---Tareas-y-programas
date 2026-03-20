import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'encuesta.db')

def obtener_hora_venezuela():
    # UTC - 4 horas (GMT-4 La Guaira/Venezuela)
    return datetime.utcnow() - timedelta(hours=4)

def inicializar_db():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    # Definimos p1 hasta p16 + email, complejo, comentario y fecha
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS respuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            email TEXT,
            complejo TEXT,
            p1 TEXT, p2 TEXT, p3 TEXT, p4 TEXT, p5 TEXT,
            p6 TEXT, p7 TEXT, p8 TEXT, p9 TEXT, p10 TEXT,
            p11 TEXT, p12 TEXT, p13 TEXT, p14 TEXT, p15 TEXT, p16 TEXT,
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
    email = request.form.get('email')
    complejo = request.form.get('complejo')
    # Recolectamos p1 hasta p16 (16 preguntas en total)
    respuestas = [request.form.get(f'p{i}') for i in range(1, 17)]
    comentario = request.form.get('comentario', '')
    
    if None in respuestas or not email or not complejo:
        return "<h3>Error: Datos incompletos.</h3><a href='/'>Volver</a>", 400

    # Generamos la hora de Venezuela
    fecha_ve = obtener_hora_venezuela().strftime('%Y-%m-%d %H:%M:%S')

    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        
        # Datos para el INSERT (20 valores en total)
        datos = [fecha_ve, email, complejo] + respuestas + [comentario]
        
        query = """INSERT INTO respuestas 
                   (fecha, email, complejo, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, comentario) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        
        cursor.execute(query, datos)
        conexion.commit()
        conexion.close()
        
        # REDIRECCIÓN DIRECTA AL INICIO
        return redirect(url_for('home'))
        
    except Exception as e:
        return f"<h3>Error al guardar en la base de datos: {e}</h3>", 500

if __name__ == '__main__':
    app.run(debug=True)