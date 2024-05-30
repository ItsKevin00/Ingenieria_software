//Función para verificar si existe el token de inicio de sesión
document.addEventListener("DOMContentLoaded", function() {
    const token = localStorage.getItem('token');
    if (!token && window.location.pathname !== '/') {
        window.location.href = "/";
    }
});
function redirigirCrear(tipo) {
    window.location.href = '/crear?tipo=' + tipo;
}

document.addEventListener("DOMContentLoaded", function() {
    const rol = localStorage.getItem('rol');
    if (rol === "Administrador") {
        const navbarAdmin = document.getElementById("navbarAdmin");
        navbarAdmin.innerHTML = `
            <ul class="navbar-nav ml-auto">
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="Administrar-menu" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Administrar
                    </a>
                    <div class="dropdown-menu" aria-labelledby="Administrar-menu">
                        <a class="dropdown-item" href="/animales">Animales</a>
                        <a class="dropdown-item" href="/usuarios">Usuarios</a>
                        <a class="dropdown-item" href="/veterinarios">Veterinarios</a>
                        <a class="dropdown-item" href="/refugios">Refugios</a>
                    </div>
                </li>
            </ul>
        `;
    }
});

function openEditModal(type, ...args) {
    if (type === "usuarios") {
        document.getElementById('edit_usuario_id').value = args[0] || '';
        document.getElementById('edit_puesto_usuario').value = args[1] || '';
        document.getElementById('edit_nombre1_usuario').value = args[2] || '';
        document.getElementById('edit_nombre2_usuario').value = args[3] || '';
        document.getElementById('edit_apellido1_usuario').value = args[4] || '';
        document.getElementById('edit_apellido2_usuario').value = args[5] || '';
        document.getElementById('edit_direccion_usuario').value = args[6] || '';
        document.getElementById('edit_telefono_usuario').value = args[7] || '';
        document.getElementById('edit_correo_electronico_usuario').value = args[8] || '';
        $('#editUsuarioModal').modal('show');
    } else if (type === "refugios") {
        document.getElementById('edit_refugio_id').value = args[0] || '';
        document.getElementById('edit_nombre_refugio').value = args[1] || '';
        document.getElementById('edit_direccion_refugio').value = args[2] || '';
        document.getElementById('edit_ciudad_refugio').value = args[3] || '';
        document.getElementById('edit_pais_refugio').value = args[4] || '';
        document.getElementById('edit_codigo_postal_refugio').value = args[5] || '';
        document.getElementById('edit_correo_electronico_refugio').value = args[6] || '';
        document.getElementById('edit_telefono_refugio').value = args[7] || '';
        $('#editRefugioModal').modal('show');
    } else if (type === "animales") {
        document.getElementById('edit_animal_id').value = args[0] || '';
        document.getElementById('edit_nombre_animal').value = args[1] || '';
        document.getElementById('edit_especie_animal').value = args[2] || '';
        document.getElementById('edit_raza_animal').value = args[3] || '';
        document.getElementById('edit_genero_animal').value = args[4] || '';
        document.getElementById('edit_esterilizado_animal').value = args[5] || '';
        document.getElementById('edit_ubicacion_actual_animal').value = args[6] || '';
        document.getElementById('edit_propietario_id_animal').value = args[7] || '';
        document.getElementById('edit_refugio_id_animal').value = args[8] || '';
        document.getElementById('edit_publicado_animal').value = args[9] || '';
        $('#editAnimalModal').modal('show');
    } else if (type === "veterinarios") {
        document.getElementById('edit_veterinario_id').value = args[0] || '';
        document.getElementById('edit_nombre').value = args[1] || '';
        document.getElementById('edit_especialidad').value = args[2] || '';
        document.getElementById('edit_telefono').value = args[3] || '';
        document.getElementById('edit_correo_electronico').value = args[4] || '';
        document.getElementById('edit_direccion').value = args[5] || '';
        $('#editVeterinarioModal').modal('show');
    }
}

var deleteParams = {};

function deleteRecord(tableType, id) {
    deleteParams = { tableType, id };
    showModal();
}

function showModal() {
    document.getElementById('deleteModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('deleteModal').style.display = 'none';
}

function confirmDelete() {
    var apiUrl = '/api/eliminar/' + deleteParams.tableType + '/' + deleteParams.id;

    fetch(apiUrl, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            return response.json().then(errorData => {
                throw new Error(errorData.message || 'Error en la solicitud.');
            });
        }
    })
    .then(data => {
        console.log(data);
        // alert(data.message);
        window.location.reload();
    })
    .catch(error => {
        console.error('Error al realizar la solicitud:', error);
        alert('Error al realizar la solicitud: ' + error.message);
    });

    closeModal();
}