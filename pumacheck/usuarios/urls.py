from django.urls import path
from .views import opcionesRegistroIH, registroEstudianteIH, registroVisitanteIH, registrosSalidasIH, registrar_visita, buscar_visita, registrar_salida_visita, registrar_visita_visitante, inicioSistemaIH, inicioAdministradorIH, inicioTrabajadorIH, crearCuentaIH, errorConexionIH, errorCerrarIH, login_view, crear_trabajador, logout_view,informacionDelCampusIH,seleccionDeCampusIH, verPerfilIH, modificarPerfilIH, guardar_cambios_perfil, modificar_contraseña, listaCampusIH, visitas_por_campus, editar_visita, get_visita_data

urlpatterns = [
    path('opcionesRegistro/', opcionesRegistroIH, name='opcionesRegistro'),
    path('registroEstudiante/', registroEstudianteIH, name='registroEstudiante'),
    path('registrosSalidas/', registrosSalidasIH, name='registrosSalidas'),
    path('registroVisitante/', registroVisitanteIH, name='registroVisitante'),
    path('registrar-visita/', registrar_visita, name='registrar_visita'),
    path('registro-salidas/', buscar_visita, name='buscar_visita'),
    path('registrar-salida/', registrar_salida_visita, name='registrar_salida_visita'),
    path('registrarVisita/', registrar_visita_visitante, name='registrar_visita_visitante'),
    path('inicioSistema/', inicioSistemaIH, name='inicioSistema'),
    path('inicioAdministrador/', inicioAdministradorIH, name='inicioAdministrador'),
    path('inicioTrabajador/', inicioTrabajadorIH, name='inicioTrabajador'),
    path('crearCuenta/', crearCuentaIH, name='crearCuenta'),
    path('errorConexion/', errorConexionIH, name='errorConexion'),
    path('errorCerrar/', errorCerrarIH, name='errorCerrar'),
    path('login/', login_view, name='login'),
    path('crear-trabajador/',crear_trabajador, name='crear_trabajador'),
    path('logout/', logout_view, name='logout'),
    path('seleccionDeCampus/', seleccionDeCampusIH, name='seleccionDeCampus'),
    path('informacionDelCampus/<int:campus_id>/', informacionDelCampusIH, name='informacionDelCampus'),
    path('verPerfil/', verPerfilIH, name='verPerfil'),
    path('modificarPerfil/', modificarPerfilIH, name='modificarPerfil'),
    path('guardar_cambios_perfil/', guardar_cambios_perfil, name='guardar_cambios_perfil'),
    path('modificar_contraseña/', modificar_contraseña, name='modificar_contraseña'),
    path('listaCampus/', listaCampusIH, name='listaCampus'),
    path('campus/<int:campus_id>/visitas/', visitas_por_campus, name='visitas_por_campus'),
    path('visita/<int:visita_id>/actualizar/', editar_visita, name='editar_visita'),
    path('get_visita_data/<int:visita_id>/', get_visita_data, name='get_visita_data'),

]