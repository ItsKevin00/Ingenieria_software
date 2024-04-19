document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();
  
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
  
    // Realizar la solicitud POST a la API utilizando Axios
    axios.post("/api/login", { username, password })
      .then(response => {
        if (response.status === 200) {
            alert("Credenciales válidas!!!!");
        } else {
          alert("Credenciales inválidas");
        }
      })
      .catch(error => {
        console.error("Error al realizar la solicitud:", error);
      });
  });
  
  