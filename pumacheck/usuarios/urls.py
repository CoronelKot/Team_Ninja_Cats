from django.urls import path
from .views import opcionesRegistroIH, registroEstudianteIH, registroVisitanteIH, registrosSalidasIH,informacionDelCampusIH,seleccionDeCampusIH

urlpatterns = [
    path('opcionesRegistro/', opcionesRegistroIH, name='opcionesRegistro'),
    path('registroEstudiante/', registroEstudianteIH, name='registroEstudiante'),
    path('registrosSalidas/', registrosSalidasIH, name='registrosSalidas'),
    path('registroVisitante/', registroVisitanteIH, name='registroVisitante'),
    path('seleccionDeCampus/', seleccionDeCampusIH, name='seleccionDeCampus'),
    path('informacionDelCampus/<int:campus_id>/', informacionDelCampusIH, name='informacionDelCampus'),
]