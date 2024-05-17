const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

//Función para verificar si existe el token de inicio de sesión
document.addEventListener("DOMContentLoaded", function() {
    const token = localStorage.getItem('token');
    if (!token && window.location.pathname !== '/') {
        window.location.href = "/";
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var donateBtn = document.getElementById('donate-btn');
    if (donateBtn) {
        donateBtn.addEventListener('click', function() {
            alert('¡Gracias por la donación!');
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var donateBtn = document.getElementById('donate-btn');
    var registerBtn = document.getElementById('register');
    var container = document.querySelector('.container');

    if (donateBtn) {
        donateBtn.addEventListener('click', function() {
            alert('¡Gracias por la donación!');
        });
    }

    if (registerBtn) {
        registerBtn.addEventListener('click', function() {
            if (container) {
                container.classList.add('active');
            }
        });
    }
});


loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

//Función para verificar si existe el token de inicio de sesión
document.addEventListener("DOMContentLoaded", function() {
    const token = localStorage.getItem('token');
    if (!token && window.location.pathname !== '/') {
        window.location.href = "/";
    }
});

//Función para obtener los datos de inicio de sesión
document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    console.log("Enviando datos a la API de inicio de sesión.");
    fetch("/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("Error al iniciar sesión");
        }
    })
    .then(data => {
        localStorage.setItem('token', data.token);
        localStorage.setItem('rol', data.rol);
        // if (data.rol === "Administrador") {
        //     const navbarAdmin = document.getElementById("navbarAdmin");
        //     navbarAdmin.innerHTML = `
        //         <ul class="navbar-nav ml-auto">
        //             <li class="nav-item">
        //                 <a class="nav-link" href="/administrar">Administrar</a>
        //             </li>
        //         </ul>
        //     `;
        // }
        window.location.href = "/index";  // Redirigir a la página de inicio si existe el token
    })
    .catch(error => {
        console.error("Error al iniciar sesión:", error);
        const errorElement = document.getElementById('passError');
        errorElement.textContent = "Error al iniciar sesión. Verifica tus credenciales e intenta nuevamente.";
    });
});

function fetchProtectedRoute() {
    fetch("/protected_route", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem('token')}`
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("Acceso denegado");
        }
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error("Error:", error);
        window.location.href = "/login";
    });
}



document.getElementById('sing-up form').addEventListener("submit", function(event) {
    event.preventDefault();

    const nombre1 = document.getElementById('nombre1').value;
    const nombre2 = document.getElementById('nombre2').value;
    const apellido1 = document.getElementById('apellido1').value;
    const apellido2 = document.getElementById('apellido2').value;
    const direccion = document.getElementById('direccion').value;
    const telefono = document.getElementById('telefono').value;
    const email = document.getElementById('email_new').value;
    const password = document.getElementById('password_new').value;

    fetch("/api/registro", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ nombre1, nombre2, apellido1, apellido2, direccion, telefono, email, password })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else if (response.status === 401) {
            return response.json().then(data => {
                if (data.message === "El usuario ya existe.") {
                    alert("El usuario ya existe!");
                    window.location.reload(); 
                    throw new Error('El usuario ya existe.');
                } else {
                    throw new Error('Error en la solicitud.');
                }
            });
        } else {
            throw new Error('Error en la solicitud.');
        }
    })
    .then(data => {
        // Manejar la respuesta de la API
        alert('¡Usuario creado con éxito!');
        console.log(data);
        window.location.reload(); 
    })
    .catch(error => {
        console.error("Error al realizar la solicitud:", error);
    });

});

// Función para eliminar el mensaje de error al borrar la contraseña
function passError(pass){
    var error = document.getElementById('passError');
    if (pass.length === 0) {
        error.textContent = "";
        return;
    }
}

// Esta función verifica en tiempo real si la contaraseña cumple con ciertos criterios de seguridad
function validatePassword(password) {
    var passwordError = document.getElementById("passwordError");
    var signUpButton = document.getElementById("sign-up");
    var criteria = [];

    if (password.length === 0) {
        passwordError.textContent = "";
        passwordMessage.textContent = "";
        return;
    }
    if (password.length < 8) {
        criteria.push("al menos 8 caracteres");
    }
    
    if (!/[A-Z]/.test(password)) {
        criteria.push("una letra mayúscula");
    }

    if (!/[0-9]/.test(password)) {
        criteria.push("un número");
    }

    if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/.test(password)) {
        criteria.push("un carácter especial");
    }
    
    if (/[./]/.test(password)) {
        criteria.push("no puede contener los caracteres '.' '/'");
    } 
    
    if (criteria.length > 0) {
        passwordError.textContent = "La contraseña debe contener " + criteria.join(", ") + ".";
        passwordMessage.textContent = "";
        signUpButton.disabled = true; 
    } else {
        passwordError.textContent = "";
        passwordMessage.textContent = "Contraseña segura.";
        signUpButton.disabled = false;
    }
}


//Función de olvido de contraseña
document.addEventListener("DOMContentLoaded", function() {
    const forgotPasswordLink = document.getElementById('forgotPasswordLink');
    const backToLogin = document.getElementById('backToLogin');
    const signInContainer = document.querySelector('.sign-in');
    const popupContainer = document.getElementById('popupContainer');

    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener('click', function(event) {
            event.preventDefault();
            signInContainer.style.display = 'none';
            popupContainer.style.display = 'block';
            document.querySelector('.forgot-password').style.display = 'flex';
        });
    }

    if (backToLogin) {
        backToLogin.addEventListener('click', function(event) {
            event.preventDefault();
            signInContainer.style.display = 'flex';
            popupContainer.style.display = 'none';
        });
    }

    const forgotPasswordForm = document.getElementById('forgotPasswordForm');
    if (forgotPasswordForm) {
        forgotPasswordForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const email = document.getElementById('forgotEmail').value;

            fetch('/api/forgot-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: email })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Se ha enviado un token de verificación a tu correo.');
                    forgotPasswordContainer.style.display = 'none';
                    resetPasswordContainer.style.display = 'flex';
                } else {
                    alert('No se pudo enviar el token. Verifica tu correo e intenta nuevamente.');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    const resetPasswordForm = document.getElementById('resetPasswordForm');
    if (resetPasswordForm) {
        resetPasswordForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const token = document.getElementById('resetToken').value;
            const newPassword = document.getElementById('newPassword').value;

            fetch('/api/reset-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ token: token, newPassword: newPassword })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Tu contraseña ha sido restablecida con éxito.');
                    window.location.href = '/login';
                } else {
                    alert('Token inválido o expirado. Intenta nuevamente.');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});
