
        document.addEventListener('DOMContentLoaded', () => {
            const form = document.getElementById('form-registro');
            const mensaje = document.getElementById('mensaje');

            form.addEventListener('submit', async (e) => {
                e.preventDefault();

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
                        mensaje.textContent = data.mensaje;
                        mensaje.className = 'text-success';
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




