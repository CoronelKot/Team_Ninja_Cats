from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
#Clase abstracta del modelo Usuaurio y de la que no se hara una tabla
class Usuario(models.Model):
    nombre_completo = models.CharField(max_length=40)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=10)
    tipoUsuario = models.BooleanField()

    class Meta:
        abstract = True

    def iniciarSesion():
        return None
    
    def cerrarSesion():
        return None

#Modelo administrador que herada de usuario
class Administrador(Usuario):
    
    def accederInfoCampus():
        return None
    
    def crearCuenta():
        return None

#Modelo trabajador que hereda de usuario
class Trabajador(Usuario):
    campus = models.ForeignKey('Campus', on_delete=models.CASCADE)

    def registrarEntrada(self, visitante, horaEntrada):
        visitante.horaEntrada = horaEntrada
        visitante.save()

    def registrarSalida(self, visitante, horaSalida):
        visitante.horaSalida = horaSalida
        visitante.save()

#Modelo Visita que puede ser estudiante o visitante
class Visita(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    identificador = models.CharField(max_length=15)
    tipo = models.CharField(max_length=10)
    horaEntrada = models.DateTimeField()
    horaSalida = models.DateTimeField(null=True, blank=True)

#Modelo Vehiculo que se relaciona con Visita
class Vehiculo(models.Model):
    numPlaca = models.CharField(max_length=10)
    registradoPor = models.CharField(max_length=30)
    visita = models.ForeignKey(Visita, on_delete=models.CASCADE)
    horaEntrada = models.DateField()
    horaSalida = models.DateField(null=True,blank=True)

    @property
    def horaEntradaSincrona(self):
        if self .horaEntrada:
            return self.horaEntrada
        elif self.visita and self.visita.horaEntrada:
            return self.visita.horaEntrada
        else:
            return None
        
    @property
    def horaSalidaSincrona(self):
        if self.horaSalida:
            return self.horaSalida
        elif self.visita and self.visita.horaSalida:
            return self.visita.horaSalida
        else:
            return None
        

#Modelo Equipo que se relaciona con Visita
class Equipo(models.Model):
    descripcion = models.CharField(max_length=100)
    registradoPor = models.CharField(max_length=30)
    horaEntrada = models.DateField()
    horaSalida = models.DateField(null=True,blank=True)
    visita = models.ForeignKey(Visita, on_delete=models.CASCADE)

    @property
    def horaEntradaSincrona(self):
        if self .horaEntrada:
            return self.horaEntrada
        elif self.visita and self.visita.horaEntrada:
            return self.visita.horaEntrada
        else:
            return None
        
    @property
    def horaSalidaSincrona(self):
        if self.horaSalida:
            return self.horaSalida
        elif self.visita and self.visita.horaSalida:
            return self.visita.horaSalida
        else:
            return None
        
#Modelo Campus que se relaciona con Trabajador
class Campus(models.Model):
    nombreCampus = models.CharField(max_length=30)
    direccion = models.CharField()
    director = models.CharField(max_length=30)
    telefono = models.CharField(max_length=10)
    correo = models.EmailField(unique=True)
