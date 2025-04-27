from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_estudiante = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=50)
    tipo_aprendizaje = models.CharField(max_length=50)
    programa = models.CharField(max_length=50)
    apoyo_financiero = models.BooleanField(default=False)
    condicion = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
    
class Semestre(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    numero_semestre = models.IntegerField()
    numero_creditos = models.IntegerField()
    horas_libres = models.IntegerField()
    
    def __str__(self):
        return self.nombre
    
class Materia(models.Model):
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    nota = models.FloatField()
    porcentaje_evaluado = models.IntegerField()

    def __str__(self):
        return self.nombre