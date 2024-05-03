const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});
document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();
  
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch("/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => {
        if (response.ok) {

            // Obtener la URL actual
            // const currentUrl = window.location.href;
            // console.log("URL actual:", currentUrl);

            window.location.href = "/index";
            return response.json();
        }
        throw new Error("Network response was not ok.");
    })
    .then(data => {
        // Manejar la respuesta de la API
        console.log(data);
    })
    .catch(error => {
        console.error("Error al realizar la solicitud:", error);
    });
});
