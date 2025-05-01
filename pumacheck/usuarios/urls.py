from django.urls import path
from .views import inicioSistemaIH, inicioAdministradorIH, inicioTrabajadorIH, crearCuentaIH, errorConexionIH, errorCerrarIH, login_view, crear_trabajador, logout_view

urlpatterns = [
    path('inicioSistema/', inicioSistemaIH, name='inicioSistema'),
    path('inicioAdministrador/', inicioAdministradorIH, name='inicioAdministrador'),
    path('inicioTrabajador/', inicioTrabajadorIH, name='inicioTrabajador'),
    path('crearCuenta/', crearCuentaIH, name='crearCuenta'),
    path('errorConexion/', errorConexionIH, name='errorConexion'),
    path('errorCerrar/', errorCerrarIH, name='errorCerrar'),
    path('login/', login_view, name='login'),
    path('crear-trabajador/',crear_trabajador, name='crear_trabajador'),
    path('logout/', logout_view, name='logout')
]