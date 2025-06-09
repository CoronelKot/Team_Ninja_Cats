import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from usuarios.models import Visita, Vehiculo, Equipo, Campus

@pytest.fixture
def crear_usuario_y_login(client):
    User = get_user_model()
    
    user = User.objects.create_user(
        correo='usuario@ejemplo.com',
        password='contrasenaSegura123.',
        es_admin=False,
        telefono='5512345678',
        nombre_completo='Luis Lopez',
        campus=None
    )
    client.login(username='usuario@ejemplo.com', password='contrasenaSegura123.')
    return user


@pytest.mark.django_db
def test_registro_visita(client):
    # Obtén el modelo de usuario
    User = get_user_model()

    user = User.objects.create_user(
        correo='usuario@ejemplo.com',
        password='contrasenaSegura123.',
        es_admin=False,
        telefono='5512345678',
        nombre_completo='Juan Pérez',
        campus=None  
    )

    client.force_login(user)

    data = {
        'nombre': 'Juan',
        'apellidos': 'Pérez',
        'numCuenta': '123456789',
        'tipo': 'Estudiante',
        'horaEntrada': '2025-05-14 8:59:00',
        'campus': 'None'
    }

    
    response = client.post(reverse('registrar_visita'), data)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.content)

    assert response.status_code == 200
    assert 'Registro exitoso' in response.json().get('mensaje')

    assert Visita.objects.filter(identificador='123456789').exists()
    



@pytest.mark.django_db
def test_registrar_visita_sin_datos(client):
    # Crear un usuario de prueba
    User = get_user_model()
    user = User.objects.create_user(
        correo='usuario@ejemplo.com',
        password='contrasenaSegura123.',
        es_admin=False,
        telefono='5512345678',
        nombre_completo='Juan Pérez',
        campus=None
    )

    client.login(correo='usuario@ejemplo.com', password='contrasenaSegura123.')

    response = client.post(reverse('registrar_visita'), {})

    assert response.status_code == 400
    assert 'Faltan campos' in response.json().get('mensaje')

@pytest.mark.django_db
def test_registrar_visita_con_vehiculo(client, crear_usuario_y_login):
    data = {
        'nombre': 'Ana',
        'apellidos': 'Martínez',
        'numCuenta': '987654321',
        'placa': 'ABC1234'
    }
    response = client.post(reverse('registrar_visita'), data)
    assert response.status_code == 200
    assert Vehiculo.objects.count() == 1

@pytest.mark.django_db
def test_registrar_visita_faltan_campos(client, crear_usuario_y_login):
    data = {
        'nombre': 'Erika'
        # Faltan 'apellidos' e 'identificador'
    }
    response = client.post(reverse('registrar_visita'), data)
    assert response.status_code == 400
    assert b'Faltan campos' in response.content


@pytest.mark.django_db
def test_registro_falla_identificador_invalido(client):
    User = get_user_model()
    user = User.objects.create_user(
        correo='usuario@ejemplo.com',
        password='contrasenaSegura123.',
        es_admin=False,
        telefono='5512345678',
        nombre_completo='Carlos Sánchez',
        campus=None  # o asigna un campus si es requerido
    )

    client.login(username='usuario@ejemplo.com', password='contrasenaSegura123.')

    # Probar con identificadores inválidos
    identificadores_invalidos = ['12345678', '1234567890', 'abcdefghi', '12345abcd']

    for identificador in identificadores_invalidos:
        data = {
            'nombre': 'Carlos',
            'apellidos': 'Sánchez',
            'numCuenta': identificador
        }
        response = client.post(reverse('registrar_visita'), data)
        assert response.status_code == 400
        assert 'El número de cuenta debe tener exactamente 9 dígitos' in response.json()['mensaje']

@pytest.mark.django_db
def test_registro_con_campos_minimos_validos(client):
    # Obtener el modelo de usuario
    User = get_user_model()

    user = User.objects.create_user(
        correo='minimo@ejemplo.com',
        password='seguro123',
        es_admin=False,
        telefono='5544332211',
        nombre_completo='Usuario Mínimo',
        campus=None 
    )

    client.login(username='minimo@ejemplo.com', password='seguro123')

    data = {
        'nombre': 'Mario',
        'apellidos': 'Gómez',
        'numCuenta': '123456789',
    }

    response = client.post(reverse('registrar_visita'), data)

    assert response.status_code == 200
    assert response.json()['mensaje'] == 'Registro exitoso'

    # Verificar que la visita se guardó correctamente
    visitas = Visita.objects.filter(identificador='123456789')
    assert visitas.exists()
    assert visitas.first().nombre == 'Mario Gómez'


@pytest.mark.django_db
def test_registro_falla_numero_cuenta_invalido(client):
    User = get_user_model()

    user = User.objects.create_user(
        correo='error@ejemplo.com',
        password='claveSegura321',
        es_admin=False,
        telefono='5550001111',
        nombre_completo='Error Usuario',
        campus=None
    )

    client.login(username='error@ejemplo.com', password='claveSegura321')

    # Número de cuenta inválido: solo 8 dígitos
    data = {
        'nombre': 'Laura',
        'apellidos': 'Cruz',
        'numCuenta': '12345678'
    }

    response = client.post(reverse('registrar_visita'), data)

    assert response.status_code == 400
    assert 'El número de cuenta' in response.json()['mensaje']

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

@pytest.mark.django_db
def test_informacion_del_campus_context(client):
    User = get_user_model()
    
    user = User.objects.create_user(
        correo='usuario@ejemplo.com',
        password='contrasenaSegura123.',
        es_admin=False,
        telefono='5512345678',
        nombre_completo='Luis Lopez',
        campus=None
    )
    client.force_login(user)
    campus = Campus.objects.create(
        nombreCampus="FES Iztacala",
        direccion="Calle Salud 22",
        director="Luis Montaño",
        telefono="1234567890",
        correo="izta@unam.mx"
    )

    visita = Visita.objects.create(
        nombre="Carla",
        identificador="8888",
        tipo="profesor",
        horaEntrada=timezone.now(),
        campus=campus
    )

    vehiculo = Vehiculo.objects.create(
        numPlaca="XYZ987",
        visita=visita,
        horaEntrada=timezone.now()
    )

    equipo = Equipo.objects.create(
        descripcion="Proyector",
        horaEntrada=timezone.now(),
        visita=visita
    )

    url = reverse('informacionDelCampus', args=[campus.id])
    response = client.get(url)

    assert response.status_code == 200
    assert 'visitas' in response.context
    assert 'vehiculos' in response.context
    assert 'equipos' in response.context

    assert list(response.context['visitas']) == [visita]
    assert list(response.context['vehiculos']) == [vehiculo]
    assert list(response.context['equipos']) == [equipo]
@pytest.mark.django_db
def test_seleccion_de_campus_context(client):
    User = get_user_model()
    
    user = User.objects.create_user(
        correo='usuario@ejemplo.com',
        password='contrasenaSegura123.',
        es_admin=False,
        telefono='5512345678',
        nombre_completo='Luis Lopez',
        campus=None
    )
    client.force_login(user)
    # Crea un dato de ejemplo en Campus
    campus = Campus.objects.create(
        nombreCampus="FES Zaragoza",
        direccion="Enrique Segoviano 123",
        director="Ronaldo Cisneros",
        telefono="5551234567",
        correo="zaragoza@unam.mx"
    )
    url = reverse('seleccionDeCampus')
    response = client.get(url)

    assert response.status_code == 200
    assert 'campus' in response.context
    assert list(response.context['campus']) == [campus]
