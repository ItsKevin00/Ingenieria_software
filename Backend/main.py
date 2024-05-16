from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, send_file, make_response
import pyodbc
import datetime
from flask_cors import CORS
from flask import send_file
from oracle import connection_string
from werkzeug.utils import secure_filename
from io import BytesIO
import jwt
import secrets
from functools import wraps


app = Flask(__name__, template_folder="C:/Users/baril/Documents/9no Semestre Sistemas/Ingeniería de Software/Desarrollo/Ingenieria_software/Frontend/templates", static_folder='C:/Users/baril/Documents/9no Semestre Sistemas/Ingeniería de Software/Desarrollo/Ingenieria_software/Frontend/static')
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080", "supports_credentials": True}})


@app.route("/")
def index():
    return render_template("Login.html")

# Ruta para la página de inicio
@app.route("/index")
def inicio():
    return render_template("index.html")

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/apoyanos")
def apoyanos():
    return render_template("About.html")

@app.route("/adopta")
def adopta():
    dogs = [
        [1, "Firulais", "Grande", "2 años", "/static/img/perro1.jpg"],
        [2, "Bobby", "Mediano", "3 años", "/static/img/perro2.jpg"],
        [3, "Max", "Pequeño", "1 año", "/static/img/perro3.jpg"]
    ]
    return render_template("Adopta.html", dogs = dogs)


# Generar token JWT
def generate_token(user_id):
    payload = {'user_id': user_id}
    token = jwt.encode(payload, 'secret_key', algorithm='HS256')
    return token

# Verificar token JWT
def verify_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return False, 'Missing token'
    
    token = auth_header.split(" ")[1]
    
    try:
        payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        return True, payload['user_id']
    except jwt.ExpiredSignatureError:
        return False, 'Expired token'
    except jwt.InvalidTokenError:
        return False, 'Invalid token'

# Decorador para rutas protegidas
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        is_valid, user_id = verify_token()
        if not is_valid:
            return jsonify({'message': 'Token is missing or invalid!'}), 401
        return f(user_id, *args, **kwargs)
    return decorated

@app.route('/protected_route')
@token_required
def protected_route(user_id):
    return jsonify({'message': 'Acceso permitido', 'user_id': user_id})

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
    query = "SELECT * FROM C##USER_DBA.Usuario WHERE CorreoElectronico = ? AND Contraseña = ?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    # Cerrar la conexión
    cursor.close()
    connection.close()

    if user:
         # Credenciales correctas
        longitud = secrets.randbelow(11) + 10  # Genera una longitud aleatoria entre 10 y 20 caracteres
        cadena_aleatoria = secrets.token_hex(longitud)
        cadena = str(cadena_aleatoria)
        token = generate_token(cadena_aleatoria)
        print("Datos correctos en el inicio de sesión")
        return jsonify({'token': token}), 200
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


# @app.route('/api/animales', methods=['POST'])
# def animales():
#     if 'imagen' not in request.files:
#         return jsonify({'message': 'No se proporcionó ninguna imagen'}), 400

#     imagen = request.files['imagen']
    
#     # Verificar si se proporcionó una imagen válida
#     if imagen.filename == '':
#         return jsonify({'message': 'No se seleccionó ningún archivo'}), 400

#     # Conectar a la base de datos
#     connection = pyodbc.connect(connection_string)
#     cursor = connection.cursor()

#     # Consulta para insertar el registro del animal
#     registro_animales = """INSERT INTO C##USER_DBA.Animales
#                           (animal_id, nombre, imagen)
#                           VALUES (1, 'test', ?)"""
#     cursor.execute(registro_animales, (imagen.read(),))

#     # Guardar cambios en la base de datos
#     connection.commit()

#     # Cerrar la conexión
#     cursor.close()
#     connection.close()

#     # Creación exitosa
#     return jsonify({'message': 'Creación exitosa'}), 201

@app.route('/api/animales', methods=['POST'])
def animales():
    if 'imagen' not in request.files:
        return jsonify({'message': 'No se proporcionó ninguna imagen'}), 400

    imagen = request.files['imagen']
    
    # Verificar si se proporcionó una imagen válida
    if imagen.filename == '':
        return jsonify({'message': 'No se seleccionó ningún archivo'}), 400

    # Conectar a la base de datos
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    # Consulta para insertar el registro del animal
    cursor.execute("SELECT MAX(animal_id) FROM C##USER_DBA.Animales")
    max_animal_id = cursor.fetchone()[0]
    new_animal_id = max_animal_id + 1 if max_animal_id else 1

    registro_animales = """INSERT INTO C##USER_DBA.Animales
                          (animal_id, nombre, imagen)
                          VALUES (?, 'test', ?)"""
    cursor.execute(registro_animales, (new_animal_id, imagen.read(),))

    # Guardar cambios en la base de datos
    connection.commit()

    # Cerrar la conexión
    cursor.close()
    connection.close()

    # Creación exitosa, devolver la imagen en la respuesta
    return send_file(BytesIO(imagen.read()), mimetype='image/jpeg', as_attachment=True, attachment_filename=f'animal_{new_animal_id}.jpg')


if __name__ == '__main__':
    app.run(debug=True)