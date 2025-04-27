from django import forms
from .models import Semestre, Materia

class SemestreForm(forms.ModelForm):
    class Meta:
        model = Semestre
        exclude = ['estudiante']
        labels = {
            'numero_semestre': 'Número de Semestre',
            'numero_creditos': 'Número de Créditos',
            'horas_libres': 'Horas Libres a la semana',
        }

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        exclude = ['semestre']
        labels = {
            'nombre': 'Nombre de la materia',
            'creditos': 'Número de Créditos',
            'nota': 'Nota actual en la materia',
            'porcentaje_evaluado': 'Porcentaje evaluado hasta el momento',
        }