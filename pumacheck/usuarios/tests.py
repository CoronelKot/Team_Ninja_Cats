import pytest
from django.urls import reverse
from usuarios.models import Campus,Visita,Vehiculo,Equipo
from django.utils import timezone
# Create your tests here.

@pytest.mark.django_db
def test_informacion_del_campus_context(client):
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
