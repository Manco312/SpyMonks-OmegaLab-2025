from django.db import models
from accounting.models import Estudiante

# Create your models here.

class Evento(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    