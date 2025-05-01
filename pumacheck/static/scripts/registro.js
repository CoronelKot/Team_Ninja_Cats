document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form-registro');

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            Swal.fire({
                title: '¡Registro exitoso!',
                text: data.mensaje,
                icon: 'success',
                confirmButtonText: 'Aceptar'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/usuarios/opcionesRegistro/';
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                title: '¡Error!',
                text: 'Ocurrió un problema al registrar. Intenta de nuevo.',
                icon: 'error',
                confirmButtonText: 'Aceptar'
            });
        });
    });
});


