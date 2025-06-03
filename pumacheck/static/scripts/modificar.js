document.addEventListener('DOMContentLoaded', () => {
    const editarBtns = document.querySelectorAll('.editar-btn');
    const form = document.getElementById('formEditarVisita');

    // Cargar datos en el modal
    editarBtns.forEach(button => {
        button.addEventListener('click', () => {
            document.getElementById('visitaId').value = button.dataset.id;
            document.getElementById('nombre').value = button.dataset.nombre;
            document.getElementById('identificador').value = button.dataset.identificador;
            document.getElementById('tipo').value = button.dataset.tipo;
            document.getElementById('vehiculo').value = button.dataset.vehiculo;
            document.getElementById('equipo').value = button.dataset.equipo;
        });
    });

    // Enviar cambios por AJAX
    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    icon: 'success',
                    title: '¡Actualizado!',
                    text: data.mensaje,
                    timer: 2000,
                    showConfirmButton: false
                });

                // Cerrar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('editarModal'));
                modal.hide();

                // Opcional: actualizar la fila correspondiente en la tabla (puedes hacerlo con id)
                const row = document.querySelector(`button[data-id='${formData.get('visita_id')}']`).closest('tr');
                if (row) {
                    row.querySelector('.col-nombre').textContent = formData.get('nombre');
                    row.querySelector('.col-identificador').textContent = formData.get('identificador');
                    row.querySelector('.col-tipo').textContent = formData.get('tipo');

                    // También actualiza los data-* para futuras ediciones
                    const btn = row.querySelector('.editar-btn');
                    btn.dataset.nombre = formData.get('nombre');
                    btn.dataset.identificador = formData.get('identificador');
                    btn.dataset.tipo = formData.get('tipo');
                    btn.dataset.vehiculo = formData.get('vehiculo');
                    btn.dataset.equipo = formData.get('equipo');
                }
            } else {
                Swal.fire('Error', data.mensaje, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire('Error', 'Ocurrió un error al actualizar la visita.', 'error');
        });
    });
});
