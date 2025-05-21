from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# --------------------------------------------------------
# Modelo de gestor personalizado de usuarios (administradores y trabajadores)
# --------------------------------------------------------

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
        extra_fields.setdefault('es_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(correo, password, **extra_fields)
    

# --------------------------------------------------------
# Modelo de Usuario (trabajadores y administradores)
# --------------------------------------------------------

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
    
    def __str__(self): 
        # Si el usuario tiene un campus asignado, muestra el nombre del campus
        if self.campus:
            return f"{self.nombre_completo} - {self.campus.nombreCampus}"
        # Si no tiene un campus asignado, muestra solo el nombre completo
        return self.nombre_completo
    
# --------------------------------------------------------
# Modelo de Visita (estudiantes y visitantes externos)
# --------------------------------------------------------

class Visita(models.Model):
    nombre = models.CharField(max_length=50)
    identificador = models.CharField(max_length=15)
    tipo = models.CharField(max_length=10)
    horaEntrada = models.DateTimeField()
    horaSalida = models.DateTimeField(null=True, blank=True)
    campus = models.ForeignKey('Campus', on_delete=models.CASCADE, null=True)

# --------------------------------------------------------
# Modelo de Vehículo asociado a una visita
# --------------------------------------------------------

class Vehiculo(models.Model):
    numPlaca = models.CharField(max_length=10)
    visita = models.ForeignKey(Visita, on_delete=models.CASCADE)
    horaEntrada = models.DateTimeField()
    horaSalida = models.DateTimeField(null=True,blank=True)
        

# --------------------------------------------------------
# Modelo de Equipo electrónico asociado a una visita
# --------------------------------------------------------

class Equipo(models.Model):
    descripcion = models.CharField(max_length=100)
    horaEntrada = models.DateTimeField()
    horaSalida = models.DateTimeField(null=True,blank=True)
    visita = models.ForeignKey(Visita, on_delete=models.CASCADE)
        
# --------------------------------------------------------
# Modelo de Campus
# --------------------------------------------------------

class Campus(models.Model):
    nombreCampus = models.CharField(max_length=30)
    direccion = models.CharField(max_length=80)
    director = models.CharField(max_length=30)
    telefono = models.CharField(max_length=10)
    correo = models.EmailField(unique=True)

# --------------------------------------------------------
# Modelo de Ticket
# --------------------------------------------------------

class Ticket(models.Model):
    identificador = models.CharField(max_length=12)
    cambio = models.CharField(max_length=20)
    actualizacion = models.CharField(max_length=20)
    corregido = models.BooleanField(default=False)
