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

@pytest.mark.django_db
def test_pagina_registro_estudiante_carga(client):
    response = client.get(reverse('usuarios:registro_estudiante'))
    assert response.status_code == 200
    assert 'Registro de Estudiante' in response.content.decode()



