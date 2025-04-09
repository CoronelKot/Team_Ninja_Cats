from django.urls import path
from .views import inicioSistemaIH, inicioAdministradorIH, inicioTrabajadorIH, crearCuentaIH

urlpatterns = [
    path('inicioSistema/', inicioSistemaIH, name='inicioSistema'),
    path('inicioAdministrador/', inicioAdministradorIH, name='inicioAdministrador'),
    path('inicioTrabajador/', inicioTrabajadorIH, name='inicioTrabajador'),
    path('crearCuenta/', crearCuentaIH, name='crearCuenta'),
]