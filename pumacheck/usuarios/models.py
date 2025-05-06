from django.db import models

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