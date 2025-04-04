from django.shortcuts import render, redirect

def opcionesRegistroIH(request):
    return render(request, 'usuarios/opcionesRegistro.html')

def registroEstudianteIH(request):
    return render(request, 'usuarios/registroEstudiante.html')

def registrosSalidasIH(request):
    return render(request, 'usuarios/registrosSalidas.html')

def registroVisitanteIH(request):
    return render(request, 'usuarios/registroVisitante.html')

# Create your views here.
