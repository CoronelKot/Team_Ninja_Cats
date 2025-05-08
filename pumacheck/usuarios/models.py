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
    
#Modelo Visita que puede ser estudiante o visitante
class Visita(models.Model):
    nombre = models.CharField(max_length=50)
    identificador = models.CharField(max_length=15)
    tipo = models.CharField(max_length=10)
    horaEntrada = models.DateTimeField()
    horaSalida = models.DateTimeField(null=True, blank=True)
    campus = models.ForeignKey('Campus', on_delete=models.CASCADE, null=True)

#Modelo Vehiculo que se relaciona con Visita
class Vehiculo(models.Model):
    numPlaca = models.CharField(max_length=10)
    visita = models.ForeignKey(Visita, on_delete=models.CASCADE)
    horaEntrada = models.DateTimeField()
    horaSalida = models.DateTimeField(null=True,blank=True)
        

#Modelo Equipo que se relaciona con Visita
class Equipo(models.Model):
    descripcion = models.CharField(max_length=100)
    horaEntrada = models.DateTimeField()
    horaSalida = models.DateTimeField(null=True,blank=True)
    visita = models.ForeignKey(Visita, on_delete=models.CASCADE)
        
#Modelo Campus que se relaciona con Trabajador
class Campus(models.Model):
    nombreCampus = models.CharField(max_length=30)
    direccion = models.CharField(max_length=80)
    director = models.CharField(max_length=30)
    telefono = models.CharField(max_length=10)
    correo = models.EmailField(unique=True)
