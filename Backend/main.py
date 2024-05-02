from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, send_file, make_response
import pyodbc
import datetime
from flask_cors import CORS
from flask import send_file
from oracle import connection_string

app = Flask(__name__, template_folder="C:/Users/baril/Documents/9no Semestre Sistemas/Ingeniería de Software/Ingenieria_software-1/Frontend/templates", static_folder='C:/Users/baril/Documents/9no Semestre Sistemas/Ingeniería de Software/Ingenieria_software-1/Frontend/static')
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080", "supports_credentials": True}})


@app.route("/")
def index():
    return render_template("Login.html")


@app.route('/api/login', methods=['POST'])
def login():
    # Obtener las credenciales de la solicitud
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Conectar a la base de datos
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    # Consulta para verificar las credenciales
    query = f"SELECT * FROM C##USER_DBA.Usuario WHERE CorreoElectronico = '{username}' AND Contraseña = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()

    # Cerrar la conexión
    cursor.close()
    connection.close()

    if user:
        # Credenciales correctas
        return jsonify({'message': 'Inicio de sesión exitoso'}), 200
    else:
        # Credenciales incorrectas
        return jsonify({'message': 'Datos inválidos'}), 401

if __name__ == '__main__':
    app.run(debug=True)