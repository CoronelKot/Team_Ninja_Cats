document.addEventListener('DOMContentLoaded', () => {
    const modalElement = document.getElementById('editarModal');
    const modal = new bootstrap.Modal(modalElement);
    const editarBtns = document.querySelectorAll('.editar-btn');

    editarBtns.forEach(button => {
        button.addEventListener('click', () => {
            const visitaId = button.dataset.id;

            fetch(`/usuarios/get_visita_data/${visitaId}/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('visitaId').value = data.id;
                    document.getElementById('nombre').value = data.nombre;
                    document.getElementById('identificador').value = data.identificador;
                    document.getElementById('tipo').value = data.tipo;
                    document.getElementById('vehiculo').value = data.vehiculo;
                    document.getElementById('equipo').value = data.equipo;

                    const form = document.getElementById('formEditarVisita');
                    form.action = `/usuarios/visita/${visitaId}/actualizar/`;

                    modal.show();
                })
                .catch(error => {
                    console.error('Error al cargar datos:', error);
                    Swal.fire('Error', 'No se pudieron cargar los datos de la visita.', 'error');
                });
        });
    });

    const form = document.getElementById('formEditarVisita');
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // --- VALIDACIONES ---
        const nombre = document.getElementById('nombre').value.trim();
        const identificador = document.getElementById('identificador').value.trim();
        const tipo = document.getElementById('tipo').value;
        let vehiculo = document.getElementById('vehiculo').value.trim();
        let equipo = document.getElementById('equipo').value.trim();


        if (vehiculo === '') vehiculo = 'No hay';
        if (equipo === '') equipo = 'No hay';

        if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/.test(nombre)) {
            console.log('Nombre inválido');
            Swal.fire('Error', 'El nombre solo puede contener letras y espacios.', 'error');
            return;
        }
        if (nombre.replace(/\s/g, '').length < 6) {
            Swal.fire('Error', 'El nombre debe tener al menos 6 letras.', 'error');
            return;
        }

        if (tipo === 'Estudiante') {
            if (!/^\d{9}$/.test(identificador)) {
                Swal.fire('Error', 'El identificador para estudiante debe ser exactamente 9 dígitos numéricos.', 'error');
                return;
            }
        } else if (tipo === 'Visitante') {
            if (!/^[A-Za-z0-9]{16}$/.test(identificador)) {
                Swal.fire('Error', 'El identificador para visitante debe ser exactamente 16 caracteres alfanuméricos.', 'error');
                return;
            }
        } else {
            Swal.fire('Error', 'Tipo inválido.', 'error');
            return;
        }

        if (vehiculo !== 'No hay' && !/^[A-Za-z0-9\-]{6,8}$/.test(vehiculo)) {
            Swal.fire('Error', 'La placa debe tener entre 6 y 8 caracteres, solo letras, números y guiones, o la frase "No hay".', 'error');
            return;
        }

        if (!nombre || !identificador || !tipo || !vehiculo || !equipo) {
            Swal.fire('Error', 'Ningún campo puede estar vacío.', 'error');
            return;
        }

        // Actualizamos los campos vehiculo y equipo para enviar bien
        document.getElementById('vehiculo').value = vehiculo;
        document.getElementById('equipo').value = equipo;

        // --- ENVÍO AJAX ---
        const url = form.action;
        const formData = new FormData(form);

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                modal.hide();
                Swal.fire({
                    icon: 'success',
                    title: 'Actualizado',
                    text: '¡Visita actualizada correctamente!',
                    timer: 2000,
                    showConfirmButton: false
                });
                // Aquí actualizar tabla o lo que quieras
            } else {
                Swal.fire('Error', data.error || 'No se pudo actualizar.', 'error');
            }
        })
        .catch(error => {
            console.error('Error al actualizar:', error);
            Swal.fire('Error', 'Ocurrió un error inesperado.', 'error');
        });

    });
});


