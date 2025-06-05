document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('formEditarVisita');
  
    form.addEventListener('submit', (e) => {
      e.preventDefault();
  
      const nombre = document.getElementById('nombre').value.trim();
      const identificador = document.getElementById('identificador').value.trim();
      const tipo = document.getElementById('tipo').value;
      let vehiculo = document.getElementById('vehiculo').value.trim();
      let equipo = document.getElementById('equipo').value.trim();
  
      // Si vehiculo o equipo están vacíos, poner "No hay"
      if (vehiculo === '') vehiculo = 'No hay';
      if (equipo === '') equipo = 'No hay';
  
      // Validaciones
  
      // Nombre: solo letras y espacios, mínimo 6 letras (excluyendo espacios)
      if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/.test(nombre)) {
        Swal.fire('Error', 'El nombre solo puede contener letras y espacios.', 'error');
        return;
      }
      if (nombre.replace(/\s/g, '').length < 6) {
        Swal.fire('Error', 'El nombre debe tener al menos 6 letras.', 'error');
        return;
      }
  
      // Identificador según tipo
      if (tipo === 'estudiante') {
        if (!/^\d{9}$/.test(identificador)) {
          Swal.fire('Error', 'El identificador para estudiante debe ser exactamente 9 dígitos numéricos.', 'error');
          return;
        }
      } else if (tipo === 'visitante') {
        if (!/^[A-Za-z0-9]{16}$/.test(identificador)) {
          Swal.fire('Error', 'El identificador para visitante debe ser exactamente 16 caracteres alfanuméricos.', 'error');
          return;
        }
      } else {
        Swal.fire('Error', 'Tipo inválido.', 'error');
        return;
      }
  
      // Vehículo: 6 a 8 caracteres letras, números o guiones o "No hay"
      if (vehiculo !== 'No hay' && !/^[A-Za-z0-9\-]{6,8}$/.test(vehiculo)) {
        Swal.fire('Error', 'La placa debe tener entre 6 y 8 caracteres, solo letras, números y guiones, o la frase "No hay".', 'error');
        return;
      }
  
      // Validar que ningún campo esté vacío (nombre, identificador, tipo ya validados, pero revisamos vehículo y equipo)
      if (!nombre || !identificador || !tipo || !vehiculo || !equipo) {
        Swal.fire('Error', 'Ningún campo puede estar vacío.', 'error');
        return;
      }
  
      // Actualizar los campos vehiculo y equipo con "No hay" si es necesario
      document.getElementById('vehiculo').value = vehiculo;
      document.getElementById('equipo').value = equipo;
  
      // Si pasa todas las validaciones, enviar el formulario
      form.submit();
    });
  });
  