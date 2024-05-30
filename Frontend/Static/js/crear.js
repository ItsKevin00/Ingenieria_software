document.addEventListener("DOMContentLoaded", function() {
    // Poblar el selector de refugios
    fetch('/api/refugios')
        .then(response => response.json())
        .then(data => {
            const refugioSelect = document.getElementById('refugio_id_animal');
            data.forEach(refugio => {
                const option = document.createElement('option');
                option.value = refugio.id;
                option.text = refugio.nombre;
                refugioSelect.appendChild(option);
            });
            // Inicializar Select2 después de poblar las opciones
            $('#refugio_id_animal').select2();
        })
        .catch(error => console.error('Error al cargar los refugios:', error));

    // Poblar el selector de propietarios
    fetch('/api/propietarios')
        .then(response => response.json())
        .then(data => {
            const propietarioSelect = document.getElementById('propietario_id_animal');
            data.forEach(propietario => {
                const option = document.createElement('option');
                option.value = propietario.id;
                option.text = propietario.nombre;
                propietarioSelect.appendChild(option);
            });
            // Inicializar Select2 después de poblar las opciones
            $('#propietario_id_animal').select2();
        })
        .catch(error => console.error('Error al cargar los propietarios:', error));
});

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


function subirDatos(tipo) {
    var form = document.getElementById('formulario-' + tipo);
    var formData = new FormData(form);
    var apiUrl;

    // Ajustar la URL de la API y manipular los datos según el tipo
    switch (tipo) {
        case 'animal':
            formData.append('publicado', document.getElementById('publicado_animal').checked ? 'Y' : 'N');
            apiUrl = '/api/animales';
            break;
        case 'usuario':
            apiUrl = '/api/usuarios';
            break;
        case 'refugio':
            apiUrl = '/api/refugios';
            break;
        case 'veterinario':
            apiUrl = '/api/veterinarios';
            break;
        default:
            console.error('Tipo de entidad no reconocido.');
            return;
    }

    fetch(apiUrl, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            if (tipo === 'animal') {
                var archivo = document.getElementById('archivo_animal').files[0];
                if (archivo) {
                    document.getElementById('imagen').src = URL.createObjectURL(archivo);
                }
                window.location.reload();
            }
            return response.json();
        } else {
            throw new Error('Error en la solicitud.');
        }
    })
    .then(data => {
        console.log(data);
        window.location.reload();
    })
    .catch(error => {
        console.error('Error al realizar la solicitud:', error);
    });
}
