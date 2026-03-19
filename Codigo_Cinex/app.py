import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'encuesta.db')

def inicializar_db():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    # Ahora tenemos p1 hasta p16 + email, complejo y comentario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS respuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
    # Recolectamos las 16 respuestas
    respuestas = [request.form.get(f'p{i}') for i in range(1, 17)]
    comentario = request.form.get('comentario', '')
    
    if None in respuestas or not email or not complejo:
        return "<h3>Error: Datos incompletos.</h3><a href='/'>Volver</a>", 400

    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        
        # 19 campos en total
        datos = [email, complejo] + respuestas + [comentario]
        query = "INSERT INTO respuestas (email, complejo, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, comentario) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        
        cursor.execute(query, datos)
        conexion.commit()
        conexion.close()
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)