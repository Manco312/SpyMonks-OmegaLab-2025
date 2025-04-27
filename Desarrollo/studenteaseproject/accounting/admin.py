from django.contrib import admin
from .models import Estudiante, Semestre, Materia

# Register your models here.

admin.site.register(Estudiante)
admin.site.register(Semestre)
admin.site.register(Materia)