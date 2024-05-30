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
import os


app = Flask(__name__, template_folder="C:/Users/baril/Documents/9no Semestre Sistemas/Ingeniería de Software/Ingenieria_software-1/Frontend/templates", static_folder='C:/Users/baril/Documents/9no Semestre Sistemas/Ingeniería de Software/Ingenieria_software-1/Frontend/static')
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080", "supports_credentials": True}})

IMAGES_DIR = os.path.join(app.static_folder, 'img')

@app.route("/")
def index():
    return render_template("Login.html")

# RUTAS DE LA PÁGINAS
@app.route("/index")
def inicio():
    return render_template("index.html")

@app.route("/crear")
def test():
    tipo = request.args.get('tipo')
    return render_template('test.html', tipo=tipo)

@app.route("/apoyanos")
def apoyanos():
    return render_template("About.html")

@app.route("/tablas")
def tablas():
    titulo = "Administrar Tablas"
    return render_template('tablas.html', titulo=titulo)

# Función que recibe una consulta, la ejecuta y devuelve el resultado
def get_results(query):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    connection.close()
    return resultados


# ADMINISTRACIÓN DE REGISTROS
@app.route("/animales")
def animales_tabla():
    titulo = "Administrar Animales"
    query = """
        SELECT 
            a.animal_id, 
            a.nombre, 
            a.especie, 
            a.raza, 
            a.genero, 
            a.esterilizado, 
            a.ubicacion_actual, 
            p.nombre AS propietario_nombre, 
            r.nombre AS refugio_nombre, 
            a.publicado
        FROM 
            C##USER_DBA.Animales a
        LEFT JOIN 
            C##USER_DBA.Propietarios p ON a.propietario_id = p.propietario_id
        LEFT JOIN 
            C##USER_DBA.Refugios r ON a.refugio_id = r.refugio_id;
    """
    resultados = get_results(query)
    # Construir la tabla HTML
    headers = ["ID", "Nombre", "Especie", "Raza", "Género", "Esterilizado", "Ubicación", "Propietario", "Refugio", "Publicado"]
    tipo = "animales"
    html_table = build_html_table(resultados, headers, "animales")
    return render_template('tablas.html', titulo=titulo, html_table=html_table, tipo=tipo)

# Ruta para administrar usuarios
@app.route("/usuarios")
def usuarios():
    titulo = "Administrar Usuarios"
    query = """
        SELECT Usuario_id, Puesto, Nombre1, Nombre2, Apellido1, Apellido2, Direccion, Telefono, CorreoElectronico
        FROM C##USER_DBA.Usuario;
    """
    resultados = get_results(query)
    # Construir la tabla HTML
    headers = ["ID", "Puesto", "Nombre1", "Nombre2", "Apellido1", "Apellido2", "Dirección", "Teléfono", "Correo Electrónico"]
    tipo = "usuarios"
    html_table = build_html_table(resultados, headers, "usuarios")
    return render_template('tablas.html', titulo=titulo, html_table=html_table, tipo=tipo)


# Ruta para administrar refugios
@app.route("/refugios")
def refugios():
    titulo = "Administrar Refugios"
    query = """
        SELECT refugio_id, nombre, direccion, ciudad, pais, codigo_postal, correo_electronico, telefono
        FROM C##USER_DBA.Refugios;
    """
    resultados = get_results(query)
    # Construir la tabla HTML
    headers = ["ID", "Nombre", "Dirección", "Ciudad", "País", "Código Postal", "Correo Electrónico", "Teléfono"]
    tipo = "refugios"
    html_table = build_html_table(resultados, headers, "refugios")
    return render_template('tablas.html', titulo=titulo, html_table=html_table, tipo=tipo)

# Ruta para administrar veterinarios
@app.route("/veterinarios")
def veterinarios():
    titulo = "Administrar Veterinarios"
    query = """
        SELECT veterinario_id, 
        TRIM(Nombre || ' ' || Apellido) AS Nombre,
        telefono, email
        FROM C##USER_DBA.Veterinarios;
    """
    resultados = get_results(query)
    # Construir la tabla HTML
    headers = ["ID", "Nombre", "Teléfono", "Email"]
    tipo= "veterinarios"
    html_table = build_html_table(resultados, headers, "veterinarios")
    return render_template('tablas.html', titulo=titulo, html_table=html_table, tipo=tipo)


###############################################
#                                             #
#              OPERACIONES CRUD               #
#                                             #
###############################################

# UPDATE REGISTROS     
@app.route("/update_usuario", methods=["POST"])
def update_usuario():
    usuario_id = request.form["id"]
    puesto = request.form["puesto"]
    nombre1 = request.form["nombre1"]
    nombre2 = request.form["nombre2"]
    apellido1 = request.form["apellido1"]
    apellido2 = request.form["apellido2"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]
    correo_electronico = request.form["correo_electronico"]

    query = """
        UPDATE C##USER_DBA.Usuario
        SET Puesto = ?, Nombre1 = ?, Nombre2 = ?, Apellido1 = ?, Apellido2 = ?, Direccion = ?, Telefono = ?, CorreoElectronico = ?
        WHERE Usuario_id = ?
    """
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    cursor.execute(query, (puesto, nombre1, nombre2, apellido1, apellido2, direccion, telefono, correo_electronico, usuario_id))
    connection.commit()
    
    return redirect("/usuarios")

@app.route('/update_refugio', methods=['POST'])
def update_refugio():
    
    refugio_id = request.form.get('refugio_id')
    print("Este es el id: "+str(refugio_id))
    refugio_id = int(float(refugio_id))
    
    nombre = request.form.get('nombre', '').encode('utf-8').decode('utf-8')
    direccion = request.form.get('direccion', '').encode('utf-8').decode('utf-8')
    ciudad = request.form.get('ciudad', '').encode('utf-8').decode('utf-8')
    pais = request.form.get('pais', '').encode('utf-8').decode('utf-8')
    codigo_postal = request.form.get('codigo_postal', '').encode('utf-8').decode('utf-8')
    correo_electronico = request.form.get('correo_electronico', '').encode('utf-8').decode('utf-8')
    telefono = request.form.get('telefono', '').encode('utf-8').decode('utf-8')

    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = """
    UPDATE C##USER_DBA.Refugios
    SET nombre = ?, direccion = ?, ciudad = ?, pais = ?, codigo_postal = ?, correo_electronico = ?, telefono = ?
    WHERE refugio_id = ?
    """
    cursor.execute(query, (nombre, direccion, ciudad, pais, codigo_postal, correo_electronico, telefono, refugio_id))
    connection.commit()
    cursor.close()
    connection.close()
    
    return redirect('/refugios')

@app.route('/update_animal', methods=['POST'])
def update_animal():
    try:
        animal_id = request.form.get('animal_id')
        animal_id = int(float(animal_id))
        
        nombre = request.form.get('nombre', '').encode('utf-8').decode('utf-8')
        especie = request.form.get('especie', '').encode('utf-8').decode('utf-8')
        raza = request.form.get('raza', '').encode('utf-8').decode('utf-8')
        genero = request.form.get('genero', '').encode('utf-8').decode('utf-8')
        esterilizado = request.form.get('esterilizado', '').encode('utf-8').decode('utf-8')
        ubicacion_actual = request.form.get('ubicacion_actual', '').encode('utf-8').decode('utf-8')
        propietario_id = request.form.get('propietario_id')
        propietario_id = int(float(propietario_id))
        refugio_id = request.form.get('refugio_id')
        refugio_id = int(float(refugio_id))
        publicado = request.form.get('edit_publicado', False)
        publicado = int(publicado)
        if publicado == 1:
            publicado = True
        elif publicado == 0:
            publicado = False
        else:
            publicado = False
        
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        query = """
        UPDATE C##USER_DBA.Animales
        SET nombre = ?, especie = ?, raza = ?, genero = ?, esterilizado = ?, ubicacion_actual = ?, propietario_id = ?, refugio_id = ?, publicado = ?
        WHERE animal_id = ?
        """
        cursor.execute(query, (nombre, especie, raza, genero, esterilizado, ubicacion_actual, propietario_id, refugio_id, publicado, animal_id))
        connection.commit()
        cursor.close()
        connection.close()
        
        return redirect('/animales')
    except Exception as e:
        print(f"Error: {str(e).encode('utf-8', 'replace').decode('utf-8')}")
        return str(e), 500


@app.route('/update_veterinario', methods=['POST'])
def update_veterinario():
    try:
        veterinario_id = request.form.get('veterinario_id')
        veterinario_id = int(float(veterinario_id))
        
        nombre = request.form.get('nombre', '').encode('utf-8').decode('utf-8')
        especialidad = request.form.get('especialidad', '').encode('utf-8').decode('utf-8')
        telefono = request.form.get('telefono', '').encode('utf-8').decode('utf-8')
        email = request.form.get('email', '').encode('utf-8').decode('utf-8')

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        query = """
        UPDATE C##USER_DBA.Veterinarios
        SET nombre = ?, especialidad = ?, telefono = ?, email = ?
        WHERE veterinario_id = ?
        """
        cursor.execute(query, (nombre, especialidad, telefono, email, veterinario_id))
        connection.commit()
        cursor.close()
        connection.close()
        
        return redirect('/veterinarios')
    except Exception as e:
        print(f"Error: {e}")
        return str(e), 500

# READ REGISTROS
def build_html_table(data, headers, table_type):
    html_table = "<table  class='dynamic-table'>"
    html_table += "<thead class='thead-light'><tr>"
    for header in headers:
        html_table += f"<th>{header}</th>"
    html_table += "<th>Acciones</th></tr></thead>"
    html_table += "<tbody>"
    for row in data:
        html_table += "<tr>"
        for i in range(len(headers)):
            value = row[i] if i < len(row) and row[i] is not None else ''
            html_table += f"<td>{value}</td>"
        row_data = [str(cell) if cell is not None else '' for cell in row]
        js_row_data = ', '.join([f'"{cell}"' for cell in row_data])
        html_table += f"""
            <td>
                <button class='btn-edit' type='button' onclick='openEditModal("{table_type}", {js_row_data})'>Editar</button>
                <form action='/Eliminar' method='POST' style='display:inline;'>
                    <button class='btn-delete' type='button' onclick='deleteRecord("{table_type}", {row[0]})'>Eliminar</button>
                </form>
            </td>
        """
        html_table += "</tr>"
    html_table += "</tbody></table>"
    return html_table


@app.route("/adopta")
def adopta():
    # Conectar a la base de datos
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    # Recuperar los animales de la base de datos
    query = "SELECT animal_id, nombre, tamanio, edad, imagen FROM C##USER_DBA.Animales WHERE publicado = 1;"
    cursor.execute(query)
    animales = cursor.fetchall()

    dogs = []

    if animales:
        for animal in animales:
            animal_id = animal[0]
            nombre = animal[1]
            tamaño = animal[2].capitalize()
            edad = str(int(animal[3])) + ' año' if animal[3] == 1.0 else str(int(animal[3])) + ' años'
            imagen_blob = animal[4]

            # Guardar la imagen en un archivo
            imagen_filename = f"{animal_id}.jpg"
            imagen_path = os.path.join(IMAGES_DIR, imagen_filename)
            with open(imagen_path, 'wb') as f:
                f.write(imagen_blob)

            # Agregar el animal a la lista con la ruta de la imagen
            dogs.append([animal_id, nombre, tamaño, edad, f"/static/img/{imagen_filename}"])

    return render_template("Adopta.html", dogs=dogs)

@app.route('/static/img/<filename>')
def get_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

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

# CREATE REGISTROS
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
        return jsonify({'token': token, 'rol': user[1]}), 200
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


@app.route('/api/animales', methods=['POST'])
def animales():
    # Verificar si la imagen está en la solicitud
    if 'archivo' not in request.files:
        return jsonify({'message': 'No se proporcionó ninguna imagen'}), 400

    # Obtener la imagen
    imagen = request.files['archivo']

    # Verificar si se proporcionó una imagen válida
    if imagen.filename == '':
        return jsonify({'message': 'No se seleccionó ningún archivo'}), 400

    # Leer el contenido de la imagen
    imagen_bytes = imagen.read()

    # Conectar a la base de datos
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    # Obtener otros campos del formulario
    # Consulta para obtener el ID máximo y calcular el nuevo ID
    cursor.execute("SELECT MAX(animal_id) FROM C##USER_DBA.Animales")
    max_animal_id = cursor.fetchone()[0]
    animal_id = max_animal_id + 1 if max_animal_id else 1
    nombre = request.form.get('nombre')
    especie = request.form.get('especie')
    raza = request.form.get('raza')
    genero = request.form.get('genero')
    esterilizado = request.form.get('esterilizado')
    ubicacion_actual = request.form.get('ubicacion_actual')
    propietario_id = request.form.get('propietario_id')
    refugio_id = request.form.get('refugio_id')
    edad = request.form.get('edad')
    tamanio = request.form.get('tamanio')
    publicado_json = request.form.get('publicado')
    if str(publicado_json) == 'on':
        publicado = True
    else:
        publicado = False
    print("Este es el valor de publicado: " + str(publicado))

    # Insertar el registro del animal
    registro_animales = """INSERT INTO C##USER_DBA.Animales
                           (animal_id, nombre, especie, raza, genero, esterilizado, ubicacion_actual, propietario_id, refugio_id, imagen, edad, tamanio,publicado)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(registro_animales, (animal_id, nombre, especie, raza, genero, esterilizado, ubicacion_actual, propietario_id, refugio_id, pyodbc.Binary(imagen_bytes), edad, tamanio, publicado))

    # Guardar cambios en la base de datos
    connection.commit()

    # Cerrar la conexión
    cursor.close()
    connection.close()

    # Creación exitosa, devolver la imagen en la respuesta
    return send_file(BytesIO(imagen_bytes), mimetype='image/jpeg', as_attachment=True, download_name=f'animal_{animal_id}.jpg')

@app.route('/api/usuarios', methods=['POST'])
def registrar_usuario():
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Obtener los datos del formulario
        puesto = request.form.get('puesto')
        primer_nombre = request.form.get('nombre1')
        segundo_nombre = request.form.get('nombre2')
        primer_apellido = request.form.get('apellido1')
        segundo_apellido = request.form.get('apellido2')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        email = request.form.get('email')
        password = request.form.get('contraseña_usuario')

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

    except pyodbc.Error as e:
        print("Error en la base de datos:", e)
        return jsonify({'message': 'Error en la base de datos', 'details': str(e)}), 500
    except Exception as e:
        print("Error en el servidor:", e)
        return jsonify({'message': 'Error en el servidor', 'details': str(e)}), 500

@app.route('/api/refugios', methods=['POST'])
def registrar_refugio():
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Obtener el ID máximo y calcular el nuevo ID
        cursor.execute("SELECT MAX(refugio_id) FROM C##USER_DBA.Refugios")
        max_refugio_id = cursor.fetchone()[0]
        refugio_id = max_refugio_id + 1 if max_refugio_id else 1

        # Obtener los datos del formulario
        nombre = request.form.get('nombre')
        direccion = request.form.get('direccion')
        ciudad = request.form.get('ciudad_refugio')
        pais = request.form.get('pais_refugio')
        codigo_postal = request.form.get('postal_refugio')
        correo_electronico = request.form.get('email_refugio')
        telefono = request.form.get('telefono')

        # Insertar el registro del refugio
        registro_refugios = """INSERT INTO C##USER_DBA.Refugios
                               (refugio_id, nombre, direccion, ciudad, pais, codigo_postal, correo_electronico, telefono)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(registro_refugios, (refugio_id, nombre, direccion, ciudad, pais, codigo_postal, correo_electronico, telefono))

        # Guardar cambios en la base de datos
        connection.commit()

        # Cerrar la conexión
        cursor.close()
        connection.close()

        return jsonify({'message': 'Refugio registrado con éxito', 'refugio_id': refugio_id}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/veterinarios', methods=['POST'])
def registrar_veterinario():
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Obtener el ID máximo y calcular el nuevo ID
        cursor.execute("SELECT MAX(veterinario_id) FROM C##USER_DBA.Veterinarios")
        max_veterinario_id = cursor.fetchone()[0]
        veterinario_id = max_veterinario_id + 1 if max_veterinario_id else 1

        # Obtener los datos del formulario
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        direccion = request.form.get('direccion')
        email = request.form.get('email')
        telefono = request.form.get('telefono')

        # Insertar el registro del veterinario
        registro_veterinarios = """INSERT INTO C##USER_DBA.Veterinarios
                                   (veterinario_id, nombre, apellido, direccion, email, telefono)
                                   VALUES (?, ?, ?, ?, ?, ?)"""
        cursor.execute(registro_veterinarios, (veterinario_id, nombre, apellido, direccion, email, telefono))

        # Guardar cambios en la base de datos
        connection.commit()

        # Cerrar la conexión
        cursor.close()
        connection.close()

        return jsonify({'message': 'Veterinario registrado con éxito', 'veterinario_id': veterinario_id}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# ELIMINAR REGISTROS
@app.route('/api/eliminar/<string:table_type>/<int:id>', methods=['DELETE'])
def eliminar_registro(table_type, id):
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Determinar la tabla y la columna de ID basándose en el tipo
        if table_type == 'usuarios':
            table_name = 'C##USER_DBA.Usuario'
            id_column = 'Usuario_id'
        elif table_type == 'animales':
            table_name = 'C##USER_DBA.Animales'
            id_column = 'animal_id'
        elif table_type == 'refugios':
            table_name = 'C##USER_DBA.Refugios'
            id_column = 'refugio_id'
        elif table_type == 'veterinarios':
            table_name = 'C##USER_DBA.Veterinarios'
            id_column = 'veterinario_id'
        else:
            return jsonify({'message': 'Tipo de entidad no reconocido'}), 400

        # Eliminar el registro
        cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = ?", id)
        
        if cursor.rowcount == 0:
            return jsonify({'message': f'No se encontró el registro con ID {id} en {table_type}'}), 404

        # Guardar cambios en la base de datos
        connection.commit()

        # Cerrar la conexión
        cursor.close()
        connection.close()

        return jsonify({'message': f'{table_type.capitalize()} eliminado con éxito'}), 200
    except pyodbc.Error as e:
        print("Error en la base de datos:", e)
        return jsonify({'message': 'Error en la base de datos', 'details': str(e)}), 500
    except Exception as e:
        print("Error en el servidor:", e)
        return jsonify({'message': 'Error en el servidor', 'details': str(e)}), 500

# OBTENER DATOS
@app.route('/api/refugios', methods=['GET'])
def get_refugios():
    search_query = request.args.get('search', '')
    if search_query:
        search_query = search_query.upper()
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = """
        SELECT refugio_id, nombre
        FROM C##USER_DBA.Refugios
        WHERE upper(nombre) like ?
        AND ROWNUM <= 10
    """
    cursor.execute(query, ('%' + search_query + '%',))
    refugios = [{'id': row[0], 'nombre': row[1]} for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return jsonify(refugios)

@app.route('/api/propietarios', methods=['GET'])
def get_propietarios():
    search_query = request.args.get('search', '')
    if search_query:
        search_query = search_query.upper()
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = """
        SELECT propietario_id, nombre, apellido
        FROM C##USER_DBA.Propietarios
        WHERE upper(nombre) like ? OR upper(apellido) like ?
        AND ROWNUM <= 10
    """
    cursor.execute(query, ('%' + search_query + '%', '%' + search_query + '%'))
    propietarios = [{'id': row[0], 'nombre': f"{row[1]} {row[2]}"} for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return jsonify(propietarios)




if __name__ == '__main__':
    app.run(debug=True)