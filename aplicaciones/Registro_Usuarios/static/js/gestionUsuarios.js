// Función autoejecutable para manejar la confirmación de eliminación
(function() {
    // Selecciona todos los botones con la clase "btnEliminacion" solo si existen
    const btnEliminacion = document.querySelectorAll(".btnEliminacion");

    if (btnEliminacion.length > 0) {
        btnEliminacion.forEach(btn => {
            btn.addEventListener('click', (e) => {
                // Confirmación de eliminación
                if (!confirm('¿Seguro de eliminar el curso?')) {
                    e.preventDefault(); // Previene la acción si se cancela
                }
            });
        });
    }
})();

// Espera a que el DOM esté completamente cargado para las alertas y otros eventos
document.addEventListener('DOMContentLoaded', function () {
    // Selecciona todas las alertas con la clase "alert" y configura su cierre automático
    const alerts = document.querySelectorAll('.alert');

    if (alerts.length > 0) {
        alerts.forEach(alert => {
            setTimeout(() => {
                const alertInstance = new bootstrap.Alert(alert);
                alertInstance.close();
            }, 2000); // Cierra la alerta después de 2 segundos
        });
    }

    // Selecciona el campo de entrada y el formulario solo si existen
    const inputField = document.getElementById('txtTienda');
    const form = document.getElementById('tiendaForm');

    if (inputField && form) {
        // Añade un evento al presionar "Enter" en el campo de entrada
        inputField.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault(); // Evita el comportamiento predeterminado
                form.submit(); // Envía el formulario
            }
        });
    }

    // Manejo de la búsqueda de usuarios por cédula usando AJAX
    const buscarUsuarioForm = document.getElementById('buscar-usuario-form');

    if (buscarUsuarioForm) {
        buscarUsuarioForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Evita la recarga de la página

            const cedulaValue = document.getElementById('txtCedula').value;
            const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

            // Verifica que haya una cédula antes de realizar la búsqueda
            if (cedulaValue) {
                $.ajax({
                    url: "{% url 'buscar_usuarios' %}",  // Asegúrate de que este URL sea correcto en Django
                    type: "POST",
                    data: {
                        txtCedula: cedulaValue,  // Valor del campo txtCedula
                        csrfmiddlewaretoken: csrfToken,  // Token CSRF para seguridad en Django
                    },
                    success: function(response) {
                        // Actualiza el área de resultado con la respuesta del servidor
                        document.getElementById('resultado-usuario').innerHTML = response;
                    },
                    error: function() {
                        // Muestra un mensaje de error en caso de fallo
                        document.getElementById('resultado-usuario').innerHTML = '<p style="color:red;">Error al buscar el usuario.</p>';
                    }
                });
            } else {
                // Si no hay cédula ingresada, muestra un mensaje de error
                document.getElementById('resultado-usuario').innerHTML = '<p style="color:red;">Por favor, ingrese un número de cédula.</p>';
            }
        });
    }
});
