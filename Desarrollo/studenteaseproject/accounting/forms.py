from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Estudiante

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
        }

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        exclude = ['user']
        labels = {
            'id_estudiante': 'ID Estudiante',
            'nombre': 'Nombre Completo',
            'tipo_aprendizaje': 'Tipo de Aprendizaje',
            'programa': 'Programa',
            'apoyo_financiero': 'Apoyo Financiero',
            'condicion': 'Condición',
        }