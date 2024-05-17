//Función para verificar si existe el token de inicio de sesión
document.addEventListener("DOMContentLoaded", function() {
    const token = localStorage.getItem('token');
    if (!token && window.location.pathname !== '/') {
        window.location.href = "/";
    }
});

//Función para cerrar sesió y borrar el token de inicio de sesión
document.addEventListener("DOMContentLoaded", function() {
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', function(event) {
            event.preventDefault();
            localStorage.removeItem('token');
            window.location.reload();
            window.location.href = '/';
            window.location.reload();
        });
    }
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

