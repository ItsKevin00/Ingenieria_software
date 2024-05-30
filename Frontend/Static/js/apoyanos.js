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
function simulateDonation() {
    const amount = document.getElementById('donationAmount').value;
    const name = document.getElementById('donorName').value;
    const email = document.getElementById('donorEmail').value;
    const cardNumber = document.getElementById('cardNumber').value;
    const expiryDate = document.getElementById('expiryDate').value;
    const cvv = document.getElementById('cvv').value;

    if (amount && name && email && cardNumber && expiryDate && cvv) {
        alert('Donación simulada exitosamente. ¡Gracias por tu apoyo!');
        $('#donarDineroModal').modal('hide');
    } else {
        alert('Por favor, complete todos los campos requeridos.');
    }
}
function submitVolunteerForm() {
    const name = document.getElementById('volunteerName').value;
    const email = document.getElementById('volunteerEmail').value;
    const phone = document.getElementById('volunteerPhone').value;
    const availability = document.getElementById('volunteerAvailability').value;
    const skills = document.getElementById('volunteerSkills').value;

    if (name && email && phone && availability) {
        alert('Formulario de voluntariado enviado exitosamente. ¡Gracias por tu interés en ayudar!');
        $('#voluntarioModal').modal('hide');
    } else {
        alert('Por favor, complete todos los campos requeridos.');
    }
}
function submitSupplyDonationForm() {
    const name = document.getElementById('donorName').value;
    const email = document.getElementById('donorEmail').value;
    const supplyType = document.getElementById('supplyType').value;
    const supplyQuantity = document.getElementById('supplyQuantity').value;
    const notes = document.getElementById('additionalNotes').value;

    if (name && email && supplyType && supplyQuantity) {
        alert('Formulario de donación de suministros enviado exitosamente. ¡Gracias por tu aporte!');
        $('#donarSuministrosModal').modal('hide');
    } else {
        alert('Por favor, complete todos los campos requeridos.');
    }
}
function shareOnPlatform(platform) {
    const message = document.getElementById('shareMessage').value;

    if (message) {
        alert('Gracias por compartir nuestra misión en ' + platform + '!');
        $('#compartirModal').modal('hide');
    } else {
        alert('Por favor, escribe un mensaje para compartir.');
    }
}