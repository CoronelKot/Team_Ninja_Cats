from django.db import models

# Create your models here.
class Entrada(models.Model):
    
    nombre = models.CharField(max_length=100)
    identificacion = models.TextField(max_length=10)
    placa = models.TextField(max_length=8)
    tipo = models.CharField(max_length=100)
    fechaEntrada = models.TimeField()
    fechaSalida = models.TimeField()
    equipo = models.CharField(max_length=100)
    def __str__(self):
        return 'Entrada: ' + self.nombre + ' identificación ' + self.identificacion +' placa: ' + self.placa + ' Entrada: ' + self.fechaEntrada.strftime("%H/%M") +' Salida: ' + self.fechaSalida.strftime("%H/%M")+ ' id: ' + self.aidi