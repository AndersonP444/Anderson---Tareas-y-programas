import os
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'encuesta.db')

def inicializar_db():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    # Creamos la tabla con las 13 preguntas + el comentario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS respuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            p1 TEXT, p2 TEXT, p3 TEXT, p4 TEXT, p5 TEXT,
            p6 TEXT, p7 TEXT, p8 TEXT, p9 TEXT, p10 TEXT,
            p11 TEXT, p12 TEXT, p13 TEXT,
            comentario TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

# Ejecutar la creación de la tabla al iniciar
inicializar_db()

@app.route('/')
def home():
    return render_template('encuesta.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    # Recolectamos las 13 respuestas
    respuestas = [request.form.get(f'p{i}') for i in range(1, 14)]
    # Recolectamos el comentario
    comentario = request.form.get('comentario', '')
    
    # --- ESTILO PARA LOS MENSAJES (Tarjeta Cinex) ---
    estilo_respuesta = """
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f4f4f4; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; text-align: center; }
        .card { background: white; padding: 40px; border-radius: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); max-width: 450px; margin: 20px; }
        h1 { color: #e02424; font-size: 2rem; margin-bottom: 15px; }
        p { color: #444; font-size: 1.2rem; line-height: 1.5; margin-bottom: 25px; }
        .btn { background: #e02424; color: white; text-decoration: none; padding: 12px 30px; border-radius: 50px; font-weight: bold; display: inline-block; transition: 0.3s; }
        .btn:hover { background: #b01d1d; }
    </style>
    """

    # 1. VALIDACIÓN DE ERROR
    if None in respuestas:
        return f"""
        {estilo_respuesta}
        <div class="card">
            <h1>¡Atención!</h1>
            <p>Por favor, asegúrate de responder todas las preguntas para que podamos procesar tu opinión.</p>
            <a href="/" class="btn">Volver a intentar</a>
        </div>
        """, 400

    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        
        # Unimos las respuestas con el comentario (14 datos en total)
        datos_a_guardar = respuestas + [comentario]
        
        # Consulta SQL con 14 columnas y 14 signos "?"
        query = """INSERT INTO respuestas (p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, comentario) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        
        cursor.execute(query, datos_a_guardar)
        conexion.commit()
        conexion.close()

        # MENSAJE DE ÉXITO
# REDIRECCIÓN DIRECTA AL INICIO
        # Esto evita que aparezca la ventana intermedia y permite que 
        # el siguiente cliente vea la encuesta desde cero inmediatamente.
        from flask import redirect, url_for
        return redirect(url_for('home'))
    
    except Exception as e:
        return f"<p>Error al guardar: {e}</p>", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)