from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Usuario

def inicioSistemaIH(request):
    return render(request, 'usuarios/inicioSistema.html')

@login_required
def inicioAdministradorIH(request):
    return render(request, 'usuarios/inicioAdministrador.html')

@login_required
def inicioTrabajadorIH(request):
    return render(request, 'usuarios/inicioTrabajador.html')

@login_required
def crearCuentaIH(request):
    return render(request, 'usuarios/crearCuenta.html')

@login_required
def errorConexionIH(request):
    return render(request, 'usuarios/errorConexion.html')

@login_required
def errorCerrarIH(request):
    return render(request, 'usuarios/errorCerrar.html')

def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        usuario = authenticate(request, username=correo, password=password)
        print("usuario:", usuario)
        if usuario is not None:
            login(request, usuario)
            if usuario.es_admin:
                return redirect('inicioAdministrador')
            return redirect('inicioTrabajador')
        else:
            messages.error(request, 'Correo o contraseña incorrectos.')
            return render(request, 'usuarios/inicioSistema.html', {'messages': messages.get_messages(request)})
    else:
        return render(request, 'usuarios/inicioSistema.html')

@login_required
def logout_view(request):
    logout(request)
    if request.method == 'POST':
        logout(request)
    return redirect('inicioSistema')

@login_required
def crear_trabajador(request):
    if request.method == 'POST':
        print("Formulario recibido")
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        password = request.POST.get('contrasena')
        confirmar = request.POST.get('confirmar_contrasena')

        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "El correo ya está registrado.")
            return redirect('crear_trabajador')
        
        if password != confirmar:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('crearCuenta')
        
        nombre_completo = f"{nombre} {apellidos}"

        Usuario.objects.create_user(
            correo=correo,
            password=password,
            nombre_completo=nombre_completo,
            telefono=telefono,
            es_admin=False,
            is_staff=False,
            is_superuser=False,
        )
        messages.success(request, "Registro exitoso.")
        return redirect('crearCuenta') 

    return redirect('inicioAdministrador')
    
# Solo permite acceso si el usuario actual es superusuario de Django
@user_passes_test(lambda u: u.is_superuser)
def crear_administrador(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        usuario = Usuario.objects.create_user(
            correo=correo,
            password=password,
            nombre_completo=request.POST.get('nombre'),
            telefono=request.POST.get('telefono'),
            es_admin=True,
            is_staff=True,
            campus = request.POST.get('campus')
        )
    return render(request, 'inicioAdministrador.html')


# Create your views here.
