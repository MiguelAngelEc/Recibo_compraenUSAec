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

});
