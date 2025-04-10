from django.shortcuts import render, redirect


def inicioSistemaIH(request):
    return render(request, 'usuarios/inicioSistema.html')

def inicioAdministradorIH(request):
    return render(request, 'usuarios/inicioAdministrador.html')

def inicioTrabajadorIH(request):
    return render(request, 'usuarios/inicioTrabajador.html')

def crearCuentaIH(request):
    return render(request, 'usuarios/crearCuenta.html')

# Create your views here.
