from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        exclude = ['estudiante']
        labels = {
            'nombre': 'Nombre del evento',
            'fecha': 'Fecha del evento',
            'descripcion': 'Descripción del evento',
        }

    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'})
    )