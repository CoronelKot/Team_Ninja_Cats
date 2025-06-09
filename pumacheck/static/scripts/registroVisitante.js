document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-registro');
    const mensaje = document.getElementById('mensaje');
    const horaEntrada = document.getElementById('horaEntrada');
    const identificadorInput = document.getElementById('identificador');
    const placasInput = document.getElementById('placas');
    const nombreInput = document.getElementById('nombre');
    const apellidosInput = document.getElementById('apellidos');

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

        horaEntrada.value = `${año}-${mes}-${dia}T${horas}:${minutos}`;
    }

    actualizarHora();
    setInterval(actualizarHora, 1000);

    // --- Mensajes personalizados para campos requeridos ---
    const campos = ['nombre', 'apellidos', 'identificador'];
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

    // --- Validación en tiempo real de nombre y apellidos ---
    function validarTexto(input) {
        const valor = input.value.trim();
        const esValido = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/.test(valor);
        if (valor === '') {
            input.classList.remove('is-invalid', 'is-valid');
        } else if (esValido) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        } else {
            input.classList.add('is-invalid');
            input.classList.remove('is-valid');
        }
    }

    nombreInput.addEventListener('input', () => validarTexto(nombreInput));
    apellidosInput.addEventListener('input', () => validarTexto(apellidosInput));

    // --- Validación completa y envío del formulario ---
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        mensaje.innerHTML = '';
        mensaje.className = '';
        let errores = [];

        // Validar nombre
        const nombre = nombreInput.value.trim();
        if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/.test(nombre)) {
            errores.push("El nombre solo puede contener letras y espacios.");
            nombreInput.classList.add('is-invalid');
            nombreInput.classList.remove('is-valid');
        }

        // Validar apellidos
        const apellidos = apellidosInput.value.trim();
        if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/.test(apellidos)) {
            errores.push("Los apellidos solo pueden contener letras y espacios.");
            apellidosInput.classList.add('is-invalid');
            apellidosInput.classList.remove('is-valid');
        }

        // Validar número de cuenta
        const identificador = identificadorInput.value.trim();
        if (!/^[A-Z0-9]{16}$/i.test(identificador)) {
            errores.push("El número CURP debe tener exactamente 16 cáracteres alfanuméricos.");
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

        // Mostrar errores y detener envío
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

                // Limpiar clases de validación visual
                [nombreInput, apellidosInput, identificadorInput, placasInput].forEach(input => {
                    input.classList.remove('is-invalid', 'is-valid');
                });

            } else {
                mensaje.innerHTML = `<div class="alert alert-danger">${data.mensaje || 'Error en el registro.'}</div>`;
            }
        } catch (error) {
            mensaje.innerHTML = `<div class="alert alert-danger">Error de conexión con el servidor.</div>`;
        }
    });
});




