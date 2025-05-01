from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

#Creación de Administradores
class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError("El correo es obligatorio")
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        usuario = self.model(
            correo=self.normalize_email(correo),
            **extra_fields
        )
        usuario.set_password(password)
        usuario.save(using=self._db) 
        return usuario

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('es_admin', False)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(correo, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre_completo = models.CharField(max_length=40)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=10)
    es_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    campus = models.ForeignKey('Campus', on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre_completo']

    objects = UsuarioManager()

    def __str__(self): 
        return self.correo
        
    def registrarEntrada(self, visitante, horaEntrada):
        visitante.horaEntrada = horaEntrada
        visitante.save()

    def registrarSalida(self, visitante, horaSalida):
        visitante.horaSalida = horaSalida
        visitante.save()

            
#Modelo Campus que se relaciona con Trabajador
class Campus(models.Model):
    nombreCampus = models.CharField(max_length=30)
    direccion = models.CharField(max_length=80)
    director = models.CharField(max_length=30)
    telefono = models.CharField(max_length=10)
    correo = models.EmailField(unique=True)