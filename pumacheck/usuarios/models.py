from django.db import models

""" Modelo de ejemplo.
class Entrada(models.Model):
    
    nombre = models.CharField(max_length=100)
    identificacion = models.TextField(max_length=10)
    placa = models.TextField(max_length=8)
    tipo = models.CharField(max_length=100)
    fechaEntrada = models.TimeField()
    fechaSalida = models.TimeField()
    equipo = models.CharField(max_length=100)
    #def __str__(self):
    #    return 'Entrada: ' + self.nombre + ' identificación ' + self.identificacion +' placa: ' + self.placa + ' Entrada: ' + self.fechaEntrada.strftime("%H/%M") +' Salida: ' + self.fechaSalida.strftime("%H/%M")+ ' id: ' + self.aidi
    
#Modelo Campus que se relaciona con Trabajador
class Campus(models.Model):
    nombreCampus = models.CharField(max_length=30)
    direccion = models.CharField()
    director = models.CharField(max_length=30)
    telefono = models.CharField(max_length=10)
    correo = models.EmailField(unique=True)"""