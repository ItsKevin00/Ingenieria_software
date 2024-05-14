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
            window.location.href = '/';
            window.location.reload();
        });
    }
});