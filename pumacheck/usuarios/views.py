from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Visita, Vehiculo, Equipo, Usuario,Campus
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
#from usuarios.models import Campus

# ============================
# Vistas públicas (login/logout)
# ============================

# Página de inicio del sistema con el formulario de login.

def inicioSistemaIH(request):
    return render(request, 'usuarios/inicioSistema.html')

# Autenticación de usuario y redirección según su rol.

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
            return render(request, 'usuarios/inicioSistema.html',{
                'abrir_modal': True
            })
    else:
        return render(request, 'usuarios/inicioSistema.html')


#Cierra la sesión del usuario.
@login_required
def logout_view(request):
    logout(request)
    if request.method == 'POST':
        logout(request)
    return redirect('inicioSistema')


# ============================
# Vistas de inicio según rol
# ============================


#Pantalla de inicio para usuarios administradores.
@login_required
def inicioAdministradorIH(request):
    return render(request, 'usuarios/inicioAdministrador.html')

#Pantalla de inicio para usuarios trabajadores, muestra el campus al que pertenecen
@login_required
def inicioTrabajadorIH(request):
    usuario = request.user  #Usuario actual
    campus = usuario.campus  #Campus del usuario

    contexto = {
        'campus': campus
    }
    return render(request, 'usuarios/inicioTrabajador.html', contexto)


# ============================
# Registro de usuarios
# ============================

#Formulario para creación de cuenta de trabajador (solo visible para administradores).
@login_required
def crearCuentaIH(request):
    campus_disponibles = Campus.objects.all()

    contexto = {
        'campus_disponibles': campus_disponibles
    }
    return render(request, 'usuarios/crearCuenta.html', contexto)


#Registra un nuevo trabajador asociado a un campus.
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
        campus_id = request.POST.get('campus')

        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "El correo ya está registrado.")
            return redirect('crear_trabajador')
        
        if password != confirmar:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('crearCuenta')
        
        nombre_completo = f"{nombre} {apellidos}"

        campus = Campus.objects.get(id=campus_id) if campus_id else None

        Usuario.objects.create_user(
            correo=correo,
            password=password,
            nombre_completo=nombre_completo,
            telefono=telefono,
            es_admin=False,
            is_staff=False,
            is_superuser=False,
            campus=campus
        )
        messages.success(request, "Registro exitoso.")
        return redirect('crearCuenta') 

    return redirect('inicioAdministrador')


# Solo permite acceso si el usuario actual es superusuario de Django
#Crea un administrador (solo accesible por superusuarios de Django).
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


# ============================
# Registro de visitas
# ============================

#Registra una visita de tipo Estudiante y opciona vehículo/equipo.
@login_required
def registrar_visita(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        identificador = request.POST.get('numCuenta')
        tipo = 'Estudiante'
        horaEntrada = timezone.now()

        if not nombre or not apellidos or not identificador:
            return JsonResponse({'mensaje': 'Faltan campos'}, status=400)
        
        # Validación de número de cuenta: exactamente 9 dígitos numéricos
        if not identificador.isdigit() or len(identificador) != 9:
            return JsonResponse({'mensaje': 'El número de cuenta debe tener exactamente 9 dígitos.'}, status=400)
        
        campus = request.user.campus

        visita = Visita.objects.create(
            nombre=f"{nombre} {apellidos}",
            identificador=identificador,
            tipo=tipo, horaEntrada=horaEntrada,
            campus=campus)
        
        
        # Si registró vehículo
        num_placa = request.POST.get('placa')
        if num_placa:
            Vehiculo.objects.create(
                numPlaca=num_placa,
                visita=visita,
                horaEntrada=horaEntrada
            )

        # Si registró equipo
        descripcion_equipo = request.POST.get('equipo')
        if descripcion_equipo:
            Equipo.objects.create(
                descripcion=descripcion_equipo,
                visita=visita,
                horaEntrada=horaEntrada
            )

        # Devolver una respuesta JSON para que el fetch() sepa que fue exitoso
        return JsonResponse({'mensaje': 'Registro exitoso'})

    return JsonResponse({'mensaje': 'Método no permitido'}, status=405)

#Registra una visita de tipo Visitante que requiere del CURP de 16 caracteres.
@login_required
def registrar_visita_visitante(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        identificador = request.POST.get('identificador')
        tipo = 'Visitante'
        horaEntrada = timezone.now()

        if not nombre or not apellidos or not identificador:
            return JsonResponse({'mensaje': 'Faltan campos'}, status=400)
        
        if len(identificador) != 16:
            return JsonResponse({'mensaje': 'El código de CURP debe tener exactamente 16 caracteres.'}, status=400)
        
        campus = request.user.campus

        visita = Visita.objects.create(
            nombre=f"{nombre} {apellidos}",
            identificador=identificador,
            tipo=tipo, horaEntrada=horaEntrada,
            campus=campus)
        
        # Si registró vehículo
        num_placa = request.POST.get('placa')
        if num_placa:
            Vehiculo.objects.create(
                numPlaca=num_placa,
                visita=visita,
                horaEntrada=horaEntrada
            )

        # Si registró equipo
        descripcion_equipo = request.POST.get('equipo')
        if descripcion_equipo:
            Equipo.objects.create(
                descripcion=descripcion_equipo,
                visita=visita,
                horaEntrada=horaEntrada
            )

        # Devolver una respuesta JSON para que el fetch() sepa que fue exitoso
        return JsonResponse({'mensaje': 'Registro exitoso'})

    return JsonResponse({'mensaje': 'Método no permitido'}, status=405)

# ============================
# Registro de salida
# ============================

#Busca una visita que no tenga la salida registrada
def buscar_visita(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        identificador = request.POST.get('identificador')
        campus = request.user.campus

        try:
            visita = Visita.objects.get(identificador=identificador,horaSalida__isnull=True,campus=campus)
            return render(request, 'usuarios/registrosSalidas.html', {'visita': visita})
        except Visita.DoesNotExist:
            return render(request, 'usuarios/registrosSalidas.html', {'error': 'No se encontró la visita o ya registró su salida.'})

    return render(request, 'usuarios/registroSalida.html')

#Registra la hora de salida de una visita y su vehiculo y/o equipos asociados
@login_required
def registrar_salida_visita(request):
    if request.method == 'POST':
        visita_id = request.POST.get('visita_id')

        try:
            visita = Visita.objects.get(id=visita_id)
            ahora = timezone.now()
            visita.horaSalida = ahora
            visita.save()

             # Registrar salida del vehículo si existe
            vehiculo = Vehiculo.objects.filter(visita=visita, horaSalida__isnull=True).first()
            if vehiculo:
                vehiculo.horaSalida = ahora
                vehiculo.save()

            # Registrar salida del equipo si existe
            equipo = Equipo.objects.filter(visita=visita, horaSalida__isnull=True).first()
            if equipo:
                equipo.horaSalida = ahora
                equipo.save()

            return render(request, 'usuarios/registrosSalidas.html', {'mensaje': 'Salida registrada exitosamente.'})
        
        except Visita.DoesNotExist:
            return render(request, 'usuarios/registrosSalidas.html', {'error': 'No se pudo registrar la salida.'})

    return redirect('buscar_visita')


# ============================
# Vistas de error
# ============================

#Vista para mostrar error de conexión.
@login_required
def errorConexionIH(request):
    return render(request, 'usuarios/errorConexion.html')


#Vista para mostrar error al cerrar sesión.
@login_required
def errorCerrarIH(request):
    return render(request, 'usuarios/errorCerrar.html')


# ============================
# Vistas a templates
# ============================

@login_required
def opcionesRegistroIH(request):
    return render(request, 'usuarios/opcionesRegistro.html')

@login_required
def registroEstudianteIH(request):
    return render(request, 'usuarios/registroEstudiante.html')

@login_required
def registrosSalidasIH(request):
    return render(request, 'usuarios/registrosSalidas.html')

@login_required
def registroVisitanteIH(request):
    return render(request, 'usuarios/registroVisitante.html')



@login_required
def informacionDelCampusIH(request, campus_id):
    campus = Campus.objects.get(pk=campus_id)
    visitas = Visita.objects.filter(campus=campus)
    vehiculos = Vehiculo.objects.filter(visita__in=visitas)
    equipos = Equipo.objects.filter(visita__in=visitas)

    contexto = {
        'campus': campus,
        'visitas': visitas,
        'vehiculos': vehiculos,
        'equipos': equipos,
    }
    return render(request, 'usuarios/informacionDelCampus.html', contexto)
@login_required
def seleccionDeCampusIH(request):
    campus = Campus.objects.all()

    contexto2 = {
        'campus': campus
    }
    return render(request, 'usuarios/seleccionDeCampus.html',contexto2)


@login_required
def listaCampusIH(request):
    campus_list = Campus.objects.all()
    return render(request, 'usuarios/listaCampus.html', {
        'campus_list': campus_list
    })


@login_required
def visitas_por_campus(request, campus_id):
    campus = get_object_or_404(Campus, id=campus_id)
    visitas = Visita.objects.filter(campus=campus)
    return render(request, 'usuarios/visitasCampus.html', {
        'campus': campus,
        'visitas': visitas
    })


def editar_visita(request):
    if request.method == "POST":
        visita_id = request.POST.get('visita_id')
        nombre = request.POST.get('nombre')
        identificador = request.POST.get('identificador')
        tipo = request.POST.get('tipo')
        vehiculo_desc = request.POST.get('vehiculo')
        equipo_desc = request.POST.get('equipo')

        try:
            visita = Visita.objects.get(id=visita_id)
            visita.nombre = nombre
            visita.identificador = identificador
            visita.tipo = tipo

            # Actualizar o crear Vehiculo
            if vehiculo_desc:
                vehiculo, _ = Vehiculo.objects.get_or_create(visita=visita)
                vehiculo.descripcion = vehiculo_desc
                vehiculo.save()
            else:
                Vehiculo.objects.filter(visita=visita).delete()

            # Actualizar o crear Equipo
            if equipo_desc:
                equipo, _ = Equipo.objects.get_or_create(visita=visita)
                equipo.descripcion = equipo_desc
                equipo.save()
            else:
                Equipo.objects.filter(visita=visita).delete()

            visita.save()
            return JsonResponse({'success': True, 'mensaje': 'Visita actualizada correctamente'})
        except Visita.DoesNotExist:
            return JsonResponse({'success': False, 'mensaje': 'Visita no encontrada'})
    return JsonResponse({'success': False, 'mensaje': 'Solicitud no válida'})


# Create your views here.
