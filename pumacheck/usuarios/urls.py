from django.urls import path
from .views import opcionesRegistroIH, registroEstudianteIH, registroVisitanteIH, registrosSalidasIH, registrar_visita, buscar_visita, registrar_salida_visita, registrar_visita_visitante

urlpatterns = [
    path('opcionesRegistro/', opcionesRegistroIH, name='opcionesRegistro'),
    path('registroEstudiante/', registroEstudianteIH, name='registroEstudiante'),
    path('registrosSalidas/', registrosSalidasIH, name='registrosSalidas'),
    path('registroVisitante/', registroVisitanteIH, name='registroVisitante'),
    path('registrar-visita/', registrar_visita, name='registrar_visita'),
    path('registro-salidas/', buscar_visita, name='buscar_visita'),
    path('registrar-salida/', registrar_salida_visita, name='registrar_salida_visita'),
    path('registrarVisita/', registrar_visita_visitante, name='registrar_visita_visitante'),
]