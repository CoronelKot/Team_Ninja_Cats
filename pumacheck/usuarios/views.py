from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Visita, Vehiculo, Equipo, Usuario,Campus, Ticket
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import CrearCuentaForm
from django.contrib.auth import update_session_auth_hash
from .forms_modificar_perfil import ModificarPerfilForm
from django.shortcuts import get_object_or_404


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
        form = CrearCuentaForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellidos = form.cleaned_data['apellidos']
            telefono = form.cleaned_data['telefono']
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
            campus_id = form.cleaned_data['campus']

            if Usuario.objects.filter(correo=correo).exists():
                messages.error(request, "El correo ya está registrado.")
                return redirect('crear_trabajador')

            nombre_completo = f"{nombre} {apellidos}"
            campus = Campus.objects.get(id=campus_id) if campus_id else None

            Usuario.objects.create_user(
                correo=correo,
                password=contrasena,
                nombre_completo=nombre_completo,
                telefono=telefono,
                es_admin=False,
                is_staff=False,
                is_superuser=False,
                campus=campus
            )
            messages.success(request, "Registro exitoso.")
            return redirect('crearCuenta')
        else:
            campus_disponibles = Campus.objects.all()
            return render(request, 'usuarios/crearCuenta.html', {'form': form})
    else:
        form = CrearCuentaForm()
        campus_disponibles = Campus.objects.all()
        return render(request, 'usuarios/crearCuenta.html', {'form': form})


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
        
        visita_activa = Visita.objects.filter(identificador=identificador, horaSalida__isnull=True).first()
        if visita_activa:
            return JsonResponse({
                'mensaje': f'Ya existe una visita activa con el identificador {identificador}. No se puede registrar una nueva hasta que finalice la anterior.'
            }, status=400)

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

        # Verifica si ya hay una visita activa (sin hora de salida) con ese identificador
        visita_activa = Visita.objects.filter(identificador=identificador, horaSalida__isnull=True).first()
        if visita_activa:
            return JsonResponse({
                'mensaje': f'Ya existe una visita activa con el identificador {identificador}. No se puede registrar una nueva hasta que finalice la anterior.'
            }, status=400)

        campus = request.user.campus

        visita = Visita.objects.create(
            nombre=f"{nombre} {apellidos}",
            identificador=identificador,
            tipo=tipo,
            horaEntrada=horaEntrada,
            campus=campus
        )
        
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

        return JsonResponse({'mensaje': 'Registro exitoso'})

    return JsonResponse({'mensaje': 'Método no permitido'}, status=405)

# ============================
# Registro de salida
# ============================

#Busca una visita que no tenga la salida registrada
@login_required
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


#Vista para mostrar la informaciónDelCampusIH.
@login_required
def informacionDelCampusIH(request, campus_id):
    campus = Campus.objects.get(pk=campus_id)
    visitas = Visita.objects.filter(campus=campus)
    vehiculos = Vehiculo.objects.filter(visita__in=visitas)
    equipos = Equipo.objects.filter(visita__in=visitas)
    es_trabajador = not request.user.es_admin


    contexto = {
        'campus': campus,
        'visitas': visitas,
        'vehiculos': vehiculos,
        'equipos': equipos,
        'es_trabajador': es_trabajador,
    }
    return render(request, 'usuarios/informacionDelCampus.html', contexto)

#Vista para seleccionar un campusIH.
@login_required
def seleccionDeCampusIH(request):
    campus = Campus.objects.all()

    contexto2 = {
        'campus': campus
    }
    return render(request, 'usuarios/seleccionDeCampus.html',contexto2)
#Vista para ver los tickets.
@login_required
def verTicketIH(request):
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.corregido = True
        ticket.save()
        return redirect('verTicketIH')  # Redirige a sí misma

    tickets = Ticket.objects.filter(corregido=False)
    contexto = {
        'tickets': tickets,
    }
    return render(request, 'usuarios/verTicket.html', contexto)
    
#Vista para la generación de tickets.
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from usuarios.models import Visita, Vehiculo, Equipo, Ticket

@login_required
def crearTicketIH(request, tipo, identificador):
    campus_id = request.GET.get('campus_id') or request.POST.get('campus_id')
    nombre = '' 

    if tipo == 'visita':
        visita = Visita.objects.filter(identificador=identificador).first()
        nombre = visita.nombre if visita else ''
    elif tipo == 'vehiculo':
        vehiculo = Vehiculo.objects.filter(numPlaca=identificador).select_related('visita').first()
        nombre = vehiculo.visita.nombre if vehiculo else ''
    elif tipo == 'equipo':
        equipo = Equipo.objects.filter(descripcion=identificador).select_related('visita').first()
        nombre = equipo.visita.nombre if equipo else ''

    if request.method == 'POST':
        cambio = request.POST.get('cambio') if tipo == 'visita' else 'identificador'
        actualizacion = request.POST.get('actualizacion')

        Ticket.objects.create(
            identificador=identificador,
            cambio=cambio,
            actualizacion=actualizacion
        )
        return redirect('informacionDelCampus', campus_id=campus_id)

    contexto = {
        'tipo': tipo,
        'identificador': identificador,
        'nombre': nombre,
        'campus_id': campus_id,
    }
    return render(request, 'usuarios/crearTicket.html', contexto)

@login_required
def verPerfilIH(request):
    usuario = request.user  # Obtén el usuario logueado para cuando se hace la modificación de la ocntraseña
    return render(request, 'usuarios/verPerfil.html', {'usuario': usuario})

@login_required
def modificarPerfilIH(request):
    usuario = request.user
    campus_disponibles = Campus.objects.all()

    if request.method == 'POST':
        form = ModificarPerfilForm(request.POST, usuario_actual=usuario)
        if form.is_valid():
            nombre = form.cleaned_data.get('nombre', usuario.nombre_completo.split()[0])
            apellidos = form.cleaned_data.get('apellidos', ' '.join(usuario.nombre_completo.split()[1:]))
            telefono = form.cleaned_data.get('telefono', usuario.telefono)
            campus_id = form.cleaned_data.get('campus')
            correo = form.cleaned_data.get('correo', usuario.correo)

            usuario.nombre_completo = f"{nombre} {apellidos}"
            usuario.telefono = telefono or usuario.telefono
            usuario.correo = correo or usuario.correo

            # Obtener la instancia del campus si se proporciona un ID
            if campus_id:
                usuario.campus = Campus.objects.get(id=campus_id)

            usuario.save()

            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('verPerfil')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = ModificarPerfilForm(initial={
            'nombre': usuario.nombre_completo.split()[0],
            'apellidos': ' '.join(usuario.nombre_completo.split()[1:]),
            'telefono': usuario.telefono,
            'correo': usuario.correo,
            'campus': usuario.campus.id if usuario.campus else None,
        }, usuario_actual=usuario)

    return render(request, 'usuarios/modificarPerfil.html', {
        'usuario': usuario,
        'campus_disponibles': campus_disponibles,
        'form': form,
    })

@login_required
def modificar_contraseña(request):
    if request.method == 'POST':
        usuario = request.user
        contraseña_actual = request.POST.get('contraseña_actual')
        nueva_contraseña = request.POST.get('nueva_contraseña')
        confirmar_contraseña = request.POST.get('confirmar_contraseña')

        # Verificar la contraseña actual
        if not usuario.check_password(contraseña_actual):
            messages.error(request, "La contraseña actual es incorrecta.")
            return redirect('modificarPerfil')

        # Verificar que las nuevas contraseñas coincidan
        if nueva_contraseña != confirmar_contraseña:
            messages.error(request, "Las nuevas contraseñas no coinciden.")
            return redirect('modificarPerfil')

        # Cambiar la contraseña
        usuario.set_password(nueva_contraseña)
        usuario.save()

        # Actualizar la sesión para evitar logout
        update_session_auth_hash(request, usuario)

        messages.success(request, "La contraseña ha sido cambiada exitosamente.")
        return redirect('modificarPerfil')

@login_required
def guardar_cambios_perfil(request):
    if request.method == 'POST':
        form = ModificarPerfilForm(request.POST, usuario_actual=request.user)
        if form.is_valid():
            usuario = request.user
            nombre = form.cleaned_data.get('nombre', usuario.nombre_completo.split()[0])
            apellidos = form.cleaned_data.get('apellidos', ' '.join(usuario.nombre_completo.split()[1:]))
            telefono = form.cleaned_data.get('telefono', usuario.telefono)
            campus_id = form.cleaned_data.get('campus')
            correo = form.cleaned_data.get('correo', usuario.correo)

            usuario.nombre_completo = f"{nombre} {apellidos}"
            usuario.telefono = telefono or usuario.telefono
            usuario.correo = correo or usuario.correo

            # Obtener la instancia del campus si se proporciona un ID
            if campus_id:
                usuario.campus = Campus.objects.get(id=campus_id)

            usuario.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('verPerfil')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
            return render(request, 'usuarios/modificarPerfil.html', {
                'form': form,
                'usuario': request.user,
                'campus_disponibles': Campus.objects.all(),
            })
    return redirect('modificarPerfil')

@login_required
def listaCampusIH(request):
    campus_list = Campus.objects.all()
    return render(request, 'usuarios/listaCampus.html', {
        'campus_list': campus_list
    })


@login_required
def visitas_por_campus(request, campus_id):
    campus = get_object_or_404(Campus, id=campus_id)
    datos_visitas = Visita.objects.filter(campus=campus)
    return render(request, 'usuarios/visitasCampus.html', {
        'campus': campus,
        'datos_visitas': datos_visitas
    })



def editar_visita(request, visita_id):
    if request.method == "GET":
        try:
            visita = Visita.objects.get(id=visita_id)
            vehiculo = Vehiculo.objects.filter(visita=visita).first()
            equipo = Equipo.objects.filter(visita=visita).first()

            return JsonResponse({
                'success': True,
                'visita': {
                    'id': visita.id,
                    'nombre': visita.nombre,
                    'identificador': visita.identificador,
                    'tipo': visita.tipo,
                    'vehiculo': vehiculo.numPlaca if vehiculo else '',
                    'equipo': equipo.descripcion if equipo else '',
                }
            })
        except Visita.DoesNotExist:
            return JsonResponse({'success': False, 'mensaje': 'Visita no encontrada'})

    elif request.method == "POST":
        visita_id = request.POST.get('visita_id')
        nombre = request.POST.get('nombre')
        identificador = request.POST.get('identificador')
        tipo = request.POST.get('tipo')
        vehiculo_input = request.POST.get('vehiculo')
        equipo_input = request.POST.get('equipo')

        try:
            visita = Visita.objects.get(id=visita_id)
            visita.nombre = nombre
            visita.identificador = identificador
            visita.tipo = tipo
            visita.save()

            # Vehículo
            if vehiculo_input != 'No hay':
                vehiculo, created = Vehiculo.objects.get_or_create(
                    visita=visita,
                    defaults={
                        'horaEntrada': visita.horaEntrada,
                        'numPlaca': vehiculo_input
                            }
                    )
                vehiculo.save()
            else:
                Vehiculo.objects.filter(visita=visita).delete()

            # Equipo
            if equipo_input != 'No hay':
                equipo, created = Equipo.objects.get_or_create(
                    visita=visita,
                    defaults={
                        'horaEntrada': visita.horaEntrada,
                        'descripcion': equipo_input
                            }
                    )
                equipo.save()
            else:
                Equipo.objects.filter(visita=visita).delete()

            return JsonResponse({'success': True, 'mensaje': 'Visita actualizada correctamente'})

        except Visita.DoesNotExist:
            return JsonResponse({'success': False, 'mensaje': 'Visita no encontrada'})

    return JsonResponse({'success': False, 'mensaje': 'Solicitud no válida'})

def get_visita_data(request, visita_id):
    try:
        visita = Visita.objects.get(id=visita_id)
        vehiculo = Vehiculo.objects.filter(visita=visita).first()
        equipo = Equipo.objects.filter(visita=visita).first()

        data = {
            'id': visita.id,
            'nombre': visita.nombre,
            'identificador': visita.identificador,
            'tipo': visita.tipo,
            'vehiculo': vehiculo.numPlaca if vehiculo else 'No hay',
            'equipo': equipo.descripcion if equipo else 'No hay',
        }
        return JsonResponse(data)
    except Visita.DoesNotExist:
        return JsonResponse({'error': 'Visita no encontrada'}, status=404)


