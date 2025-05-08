document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-registro');
    const mensaje = document.getElementById('mensaje');

    // Agregar mensajes personalizados a campos requeridos
    const campos = ['nombre', 'apellidos', 'identificador'];
    campos.forEach(id => {
        const campo = document.getElementById(id);

        campo.addEventListener('invalid', () => {
            if (!campo.value.trim()) {
                campo.setCustomValidity("Completa este campo");
            }
        });

        campo.addEventListener('input', () => {
            campo.setCustomValidity("");
        });

        campo.addEventListener('invalid', () => {
            if (!campo.value.trim()) {
                campo.setCustomValidity("Completa este campo");
                campo.reportValidity();
            }
        });
        

    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Esto activa los estilos de Bootstrap y muestra mensajes de validación
        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            return;
        }

        const formData = new FormData(form);
        const url = form.dataset.url;

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                }
            });

            const data = await response.json();

            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: 'Registro exitoso',
                    text: data.mensaje,
                    confirmButtonText: 'Aceptar'
                });
                mensaje.textContent = '';
                mensaje.className = '';
                form.reset();
                form.classList.remove('was-validated');
            } else {
                mensaje.textContent = data.mensaje || 'Error en el registro';
                mensaje.className = 'text-danger';
            }
        } catch (error) {
            mensaje.textContent = 'Error de conexión con el servidor.';
            mensaje.className = 'text-danger';
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const horaEntrada = document.getElementById('horaEntrada');

    function pad(n) {
        return n.toString().padStart(2, '0');
    }

    function actualizarHora() {
        const ahora = new Date();
        const año = ahora.getFullYear();
        const mes = pad(ahora.getMonth() + 1);
        const dia = pad(ahora.getDate());
        const horas = pad(ahora.getHours());
        const minutos = pad(ahora.getMinutes());

        // formato requerido por datetime-local: YYYY-MM-DDTHH:MM
        horaEntrada.value = `${año}-${mes}-${dia}T${horas}:${minutos}`;
    }

    actualizarHora(); // ponerla al cargar

    // Opcional: actualiza cada minuto
    setInterval(actualizarHora, 1000);
});

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form-registro');
    const numCuentaInput = document.getElementById('identificador');
    const mensajeDiv = document.getElementById('mensaje');

    form.addEventListener('submit', function (event) {
        const numCuenta = numCuentaInput.value.trim();

        // Verificar que el número de cuenta tenga exactamente 9 dígitos numéricos
        const esValido = /^\d{9}$/.test(numCuenta);

        if (!esValido) {
            event.preventDefault(); // Detener el envío
            mensajeDiv.innerHTML = '<div class="alert alert-danger">El identificador cuenta debe tener exactamente 9 dígitos.</div>';
            numCuentaInput.classList.add('is-invalid');
        } else {
            mensajeDiv.innerHTML = '';
            numCuentaInput.classList.remove('is-invalid');
        }
    });
});




