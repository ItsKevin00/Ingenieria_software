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

# Ruta para la página de inicio
@app.route("/index")
def inicio():
    return render_template("index.html")


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

@app.route('/api/registro', methods=['POST'])
def registro():
    #Obtener los datos para el registro del usuario
    data = request.get_json()
    primer_nombre = data.get('nombre1', False)
    segundo_nombre = data.get('nombre2', False)
    primer_apellido = data.get('apellido1', False)
    segundo_apellido = data.get('apellido2', False)
    direccion = data.get('direccion', False)
    telefono = data.get('telefono', False)
    email = data.get('email', False)
    password = data.get('password', False)
    puesto = 'Usuario'

    if primer_nombre == False or email == False or password == False:
        # Datos insuficientes
        return jsonify({'message': 'Datos inválidos'}), 401

    # Conectar a la base de datos
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    # Verificar si el usuario ya existe en la base de datos
    query = f"SELECT * FROM C##USER_DBA.Usuario WHERE CorreoElectronico = '{email}'"
    cursor.execute(query)
    usuario = cursor.fetchone()

    if usuario:
        return jsonify({'message': 'El usuario ya existe.'}), 401
    
    else:
        # Consulta para crear el nuevo usuario en la base de datos
        registro_query = """INSERT INTO C##USER_DBA.Usuario
                          (Puesto, Nombre1, Nombre2, Apellido1, Apellido2, Direccion, Telefono, CorreoElectronico, Contraseña)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(registro_query, (puesto, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, direccion, telefono, email, password))
        # Realizar el commitn para guardar los datos en la bd y cerrar la conexión
        connection.commit()

        # Consulta para verificar si el usuario se creó correctamente
        query = f"SELECT * FROM C##USER_DBA.Usuario WHERE CorreoElectronico = '{email}' AND Contraseña = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()

        # Cerrar la conexión
        cursor.close()
        connection.close()

        if user:
            # Creación exitosa
            return jsonify({'message': 'Creación exitosa'}), 200
        else:
            # No se pudo crear el usuario
            return jsonify({'message': 'No se pudo crear el usuario'}), 401





if __name__ == '__main__':
    app.run(debug=True)