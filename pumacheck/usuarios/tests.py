import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from usuarios.models import Visita, Vehiculo, Equipo

@pytest.mark.django_db
def test_registro_visita(client):
    data = {
        'nombre': 'Juan',
        'apellidos': 'Pérez',
        'numCuenta': '12345678'
    }
    response = client.post(reverse('registrar_visita'), data)
    assert response.status_code == 200
    assert Visita.objects.filter(identificador='12345678').exists()

@pytest.mark.django_db
def test_registrar_visita_sin_datos(client):
    response = client.post(reverse('registrar_visita'), {})
    assert response.status_code == 400


def test_url_invalida(client):
    response = client.get('/usuarios/nohay/')
    assert response.status_code == 404

@pytest.mark.django_db
def test_registrar_visita_con_equipo(client):
    data = {
        'nombre': 'Luis',
        'apellidos': 'Lopez',
        'numCuenta': '11223344',
        'equipo': 'Laptop ASUS'
    }
    response = client.post(reverse('registrar_visita'), data)
    assert response.status_code == 200
    assert Equipo.objects.count() == 1

@pytest.mark.django_db
def test_registrar_visita_con_vehiculo(client):
    data = {
        'nombre': 'Ana',
        'apellidos': 'Casballido',
        'numCuenta': '87654321',
        'placa': 'ABC1234'
    }
    response = client.post(reverse('registrar_visita'), data)
    assert response.status_code == 200
    assert Visita.objects.count() == 1
    assert Vehiculo.objects.count() == 1

@pytest.mark.django_db
def test_registrar_visita_sin_vehiculo_ni_equipo(client):
    data = {
        'nombre': 'Juan',
        'apellidos': 'Pérez',
        'numCuenta': '12345678'
    }
    response = client.post(reverse('registrar_visita'), data)
    assert response.status_code == 200
    assert Visita.objects.count() == 1
    assert Vehiculo.objects.count() == 0
    assert Equipo.objects.count() == 0

@pytest.mark.django_db
def test_pagina_registro_estudiante_carga(client):
    response = client.get(reverse('registroEstudiante'))
    assert response.status_code == 200
    assert 'Registro de Estudiante' in response.content.decode()

@pytest.mark.django_db
def test_pagina_registro_visitante_carga(client):
    response = client.get(reverse('registroVisitante'))
    assert response.status_code == 200
    assert 'Registro de Visitantes' in response.content.decode()

@pytest.mark.django_db
def test_pagina_opciones_registro_carga(client):
    response = client.get(reverse('opcionesRegistro'))
    assert response.status_code == 200
    assert 'Registro de entradas' in response.content.decode()

@pytest.mark.django_db
def test_pagina_registro_salidas_carga(client):
    response = client.get(reverse('registrosSalidas'))
    assert response.status_code == 200
    assert 'Registro de Salidas' in response.content.decode()

@pytest.mark.django_db
def test_login_view_trabajador(client):
    User = get_user_model()
    user = User.objects.create_user(
        correo='trabajador@gmail.com',
        password='trabajador12345.',
        es_admin=False,
        telefono='5518872344',
        nombre_completo='Trabajador Uno',
        campus=None,
    )
    response = client.post(reverse('login'), {
        'correo': 'trabajador@gmail.com',
        'password': 'trabajador12345.'
    })

    assert response.status_code == 302
    assert response['Location'] == reverse('inicioTrabajador')


@pytest.mark.django_db
def test_login_view_administrador(client):
    User = get_user_model()
    user = User.objects.create_user(
        correo='admin@gmail.com',
        password='admin12345.',
        es_admin=True,
        telefono='5518872343',
        nombre_completo='Administrador Uno',
        campus=None,
    )
    response = client.post(reverse('login'), {
        'correo': 'admin@gmail.com',
        'password': 'admin12345.'
    })

    assert response.status_code == 302
    assert response['Location'] == reverse('inicioAdministrador')


@pytest.mark.django_db
def test_login_view_falla(client):
    User = get_user_model()
    User.objects.create_user(
        correo='usuario@ejemplo.com',
        password='contrasenaSegura123.',
        es_admin=False,
        telefono='5500000000',
        nombre_completo='Usuario Prueba',
        campus=None,
    )
    # Intentar iniciar sesión con credenciales incorrectas
    response = client.post(reverse('login'), {
        'correo': 'usuario@ejemplo.com',
        'password': 'incorrecta'
    })

    #Debe quedarse en la página de login
    assert response.status_code == 200
    assert "Correo o contraseña incorrectos." in response.content.decode()


@pytest.mark.django_db
def test_logout_view_post(client):
    User = get_user_model()
    user = User.objects.create_user(
        correo='logoutpost@gmail.com',
        password='logoutpass123.',
        es_admin=False,
        telefono='5518871234',
        nombre_completo='Logout Post Tester',
        campus=None,
    )

    #Autenticar al usuario
    client.login(username='logoutpost@gmail.com', password='logoutpass123.')

    # Hacer POST a la vista de logout
    response = client.post(reverse('logout'))

    #Redirigir al inicio del sistema
    assert response.status_code == 302
    assert response['Location'] == reverse('inicioSistema')

    #Intentar acceder a una vista protegida después del logout
    response_protegido = client.get(reverse('inicioAdministrador'))
    assert response_protegido.status_code == 302 


@pytest.mark.django_db
def test_crear_trabajador_exitoso(client):
    #Crear un administrador autenticado
    User = get_user_model()
    admin = User.objects.create_user(
        correo='admin@gmail.com',
        password='AdminSegura123.',
        es_admin=True,
        is_staff=True,
        nombre_completo='Admin Prueba',
        telefono='5512345678',
        campus=None
    )
    client.login(username='admin@gmail.com', password='AdminSegura123.')

    # Datos para el nuevo trabajador a registrar
    data = {
        'nombre': 'Juan',
        'apellidos': 'Pérez',
        'telefono': '5599999999',
        'correo': 'juan_perez@gmail.com',
        'contrasena': 'Contrasena123.',
        'confirmar_contrasena': 'Contrasena123.',
    }

    response = client.post(reverse('crear_trabajador'), data)

    # Verificamos que el trabajador fue creado y se redirige correctamente
    User = get_user_model()
    assert User.objects.filter(correo='juan_perez@gmail.com').exists()
    assert response.status_code == 302
    assert response.url == reverse('crearCuenta')

