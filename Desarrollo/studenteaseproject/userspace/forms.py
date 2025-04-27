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