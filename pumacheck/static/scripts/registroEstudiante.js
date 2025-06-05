document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-registro');
    const mensaje = document.getElementById('mensaje');
    const horaEntrada = document.getElementById('horaEntrada');
    const numCuentaInput = document.getElementById('numCuenta');
    const placasInput = document.getElementById('placas');

    // --- Establecer hora actual en horaEntrada ---
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

    actualizarHora(); // Al cargar
    setInterval(actualizarHora, 1000); // Opcional: actualizar cada segundo

    // --- Mensajes personalizados para campos requeridos ---
    const campos = ['nombre', 'apellidos', 'numCuenta'];
    campos.forEach(id => {
        const campo = document.getElementById(id);

        campo.addEventListener('invalid', () => {
            if (!campo.value.trim()) {
                campo.setCustomValidity("Completa este campo");
                campo.reportValidity();
            }
        });

        campo.addEventListener('input', () => {
            campo.setCustomValidity("");
        });
    });

    // --- Validación completa y envío del formulario ---
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        mensaje.innerHTML = '';
        mensaje.className = '';
        let errores = [];

        // Validar número de cuenta
        const numCuenta = numCuentaInput.value.trim();
        if (!/^\d{9}$/.test(numCuenta)) {
            errores.push("El número de cuenta debe tener exactamente 9 dígitos.");
            numCuentaInput.classList.add('is-invalid');
        } else {
            numCuentaInput.classList.remove('is-invalid');
        }

        // Validar placas si no están vacías
        const placas = placasInput.value.trim();
        if (placas !== '') {
            if (!/^[A-Z0-9-]{6,8}$/i.test(placas)) {
                errores.push("Las placas deben tener entre 6 y 8 caracteres alfanuméricos o guiones.");
                placasInput.classList.add('is-invalid');
            } else {
                placasInput.classList.remove('is-invalid');
            }
        } else {
            placasInput.classList.remove('is-invalid');
        }

        // Validación HTML5 adicional
        if (!form.checkValidity()) {
            form.classList.add('was-validated');
        }

        // Mostrar errores y no enviar si hay alguno
        if (errores.length > 0) {
            mensaje.innerHTML = `<div class="alert alert-danger">${errores.join('<br>')}</div>`;
            return;
        }

        // Enviar con fetch
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
                form.reset();
                form.classList.remove('was-validated');
            } else {
                mensaje.innerHTML = `<div class="alert alert-danger">${data.mensaje || 'Error en el registro.'}</div>`;
            }
        } catch (error) {
            mensaje.innerHTML = `<div class="alert alert-danger">Error de conexión con el servidor.</div>`;
        }
    });
});


