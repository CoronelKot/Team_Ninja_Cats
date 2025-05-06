from django.test import TestCase

# Create your tests here.
import pytest
from django.urls import reverse
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

