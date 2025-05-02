import pytest
from django.urls import path
from datetime import date
from .models import Entrada,Campus
# Create your tests here.
@pytest.mark.django_db
def test_creacion_campus():
    campus = Campus.objects.create(
        nombreCampus="CU",
        direccion="Av. Universidad 3000",
        director="Dra. María Pérez",
        telefono="5555555555",
        correo="cu@unam.mx"
    )
    assert campus.nombreCampus == "CU"
    assert campus.id is not None
    
@pytest.mark.django_db
def create_test_data():
    """
    Crea una información de un  campus .
    """
    ##publisher = Publisher.objects.create(name="Test Publisher")
    prueba = Campus.objects.create(
        nombreCampus2 = "Facultad de estudios superiores Zaragoza",
        direccion = "Enrique segobiano",
        director = "Ronaldo Cisneros Huerta",
        telefono = "1234567890",
        correo = "pumitapuma@ciencias.unam.mx",
    )
    return prueba