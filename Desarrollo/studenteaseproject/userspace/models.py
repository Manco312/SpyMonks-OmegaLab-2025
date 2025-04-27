from django.db import models
from accounting.models import Estudiante

# Create your models here.

class Semestre(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    numero_semestre = models.IntegerField()
    numero_creditos = models.IntegerField()
    horas_libres = models.IntegerField()
    
    def __str__(self):
        return self.nombre
    
class Materia(models.Model):
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    creditos = models.IntegerField()
    nombre = models.CharField(max_length=50)
    nota = models.FloatField()
    porcentaje_evaluado = models.IntegerField()

    def __str__(self):
        return self.nombre