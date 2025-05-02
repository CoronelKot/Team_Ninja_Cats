from django.shortcuts import render, redirect
from .models import Visita,Vehiculo,Equipo,Campus

def opcionesRegistroIH(request):
    return render(request, 'usuarios/opcionesRegistro.html')

def registroEstudianteIH(request):
    return render(request, 'usuarios/registroEstudiante.html')

def registrosSalidasIH(request):
    return render(request, 'usuarios/registrosSalidas.html')

def registroVisitanteIH(request):
    return render(request, 'usuarios/registroVisitante.html')

def informacionDelCampusIH(request, campus_id):
    campus = Campus.objects.get(pk=campus_id)
    visitas = Visita.objects.filter(equipo__visita__campus=campus).distinct()
    vehiculos = Vehiculo.objects.filter(visita__in=visitas)
    equipos = Equipo.objects.filter(visita__in=visitas)

    contexto = {
        'campus': campus,
        'visitas': visitas,
        'vehiculos': vehiculos,
        'equipos': equipos,
    }
    return render(request, 'usuarios/informacionDelCampus.html', contexto)
   
def seleccionDeCampusIH(request):
    campus = Campus.objects.all()

    contexto2 = {
        'campus': campus
    }
    return render(request, 'usuarios/seleccionDeCampus.html',contexto2)

# Create your views here.
