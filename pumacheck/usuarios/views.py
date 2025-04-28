from django.shortcuts import render, redirect
from .models import Entrada,Campus

def opcionesRegistroIH(request):
    return render(request, 'usuarios/opcionesRegistro.html')

def registroEstudianteIH(request):
    return render(request, 'usuarios/registroEstudiante.html')

def registrosSalidasIH(request):
    return render(request, 'usuarios/registrosSalidas.html')

def registroVisitanteIH(request):
    return render(request, 'usuarios/registroVisitante.html')

def informacionDelCampusIH(request):
    ## entradas_Hoy = [
    ##    {'nombre':'Cosme fulanito1','identificacion':'xyx','placa':'xyz','tipo':'Alumno','fechaEntrada':'11:50','fechaSalida':'12:50','equipo':'asus'},
    ##    {'nombre':'Cosme fulanito1','identificacion':'xyx','placa':'xyz','tipo':'Alumno','fechaEntrada':'11:50','fechaSalida':'12:50','equipo':'asus'},
    ##    {'nombre':'Cosme fulanito1','identificacion':'xyx','placa':'xyz','tipo':'Alumno','fechaEntrada':'11:50','fechaSalida':'12:50','equipo':'asus'},
    ##    {'nombre':'Cosme fulanito1','identificacion':'xyx','placa':'xyz','tipo':'Visitante','fechaEntrada':'11:50','fechaSalida':'12:50','equipo':'asus'},
    ##]
    entradas_Hoy = Entrada.objects.all()

    contexto = {
        'entradas_Hoy': entradas_Hoy
    }
    return render(request, 'usuarios/informacionDelCampus.html',contexto)
def seleccionDeCampusIH(request):
    campusPrueba = Campus.objects.all()

    contexto2 = {
        'campusPrueba': campusPrueba
    }
    return render(request, 'usuarios/seleccionDeCampus.html',contexto2)

# Create your views here.
