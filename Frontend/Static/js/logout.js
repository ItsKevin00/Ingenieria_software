// Función para cerrar sesión
function logout() {
    // Después de cerrar sesión, redireccionamos a la página de inicio de sesión
    window.location.href = "/?logged_out=true";
    console.log("Sesión cerrada!!");
}

// Verificar si el usuario ha cerrado sesión
const urlParams = new URLSearchParams(window.location.search);
const loggedOut = urlParams.get('logged_out');

// Si el usuario ha cerrado sesión, redirigir a la página de inicio de sesión
if (loggedOut === 'true') {
    // Establecer una cookie para marcar que el usuario ha cerrado sesión
    document.cookie = "logged_out=true; path=/";
    window.location.href = "/";
}

// Agregar el event listener para cerrar sesión
document.getElementById("logoutButton").addEventListener("click", logout);

// Impedir que el usuario retroceda a esta página después de cerrar sesión
window.addEventListener('popstate', function (event) {
    window.location.href = "/";
});
