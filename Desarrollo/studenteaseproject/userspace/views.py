from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from accounting.models import Estudiante
from .models import Semestre
from .forms import SemestreForm

@login_required
def home(request):
    # Verificar si el usuario tiene información de semestre creada

    estudiante = Estudiante.objects.filter(user=request.user).first()

    semestre_creado = Semestre.objects.filter(estudiante=estudiante).exists()

    context = {
        'semestre_creado': semestre_creado,
        'user_name': request.user.username,
        'nombre': estudiante.nombre,
    }
    
    return render(request, 'home.html', context)

@login_required
def crear_semestre(request):
    estudiante = Estudiante.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        form = SemestreForm(request.POST)
        if form.is_valid():
            semestre = form.save(commit=False)
            semestre.estudiante = estudiante
            semestre.save()
            return redirect('home')  # Redirigir a la página principal o donde prefieras
    else:
        form = SemestreForm()
    
    return render(request, 'crear_semestre.html', {'form': form})