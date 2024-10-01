
// Selecciona el campo de entrada
const inputField = document.getElementById('txtTienda');
// Selecciona el formulario
const form = document.getElementById('tiendaForm');

// Añade un evento keydown al campo de entrada
inputField.addEventListener('keydown', function(event) {
    // Comprueba si la tecla presionada es Enter
    if (event.key === 'Enter') {
        // Previene el comportamiento predeterminado (si es necesario)
        event.preventDefault();
        // Envía el formulario
        form.submit();
    }
});
