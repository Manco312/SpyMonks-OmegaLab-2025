
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounting.models import Estudiante
from .models import Materia, Semestre
from .forms import MateriaForm, SemestreForm

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


@login_required
def registrar_materias(request):
    # Obtener el estudiante asociado al usuario actual
    try:
        estudiante = Estudiante.objects.get(user=request.user)
    except Estudiante.DoesNotExist:
        messages.error(request, "No se encontró un perfil de estudiante asociado a tu cuenta.")
        return redirect('home')
    
    # Obtener el semestre del estudiante (asumiendo que solo hay uno)
    try:
        semestre = Semestre.objects.get(estudiante=estudiante)
    except Semestre.DoesNotExist:
        messages.error(request, "Primero debes crear un semestre.")
        return redirect('crear_semestre')
    
    # Obtener las materias ya registradas para este semestre
    materias = Materia.objects.filter(semestre=semestre).order_by('nombre')
    
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.semestre = semestre
            materia.save()
            messages.success(request, f"¡La materia '{materia.nombre}' ha sido registrada exitosamente!")
            return redirect('registrar_materias')  # Redirigir a la misma página para añadir más materias
    else:
        form = MateriaForm()
    
    return render(request, 'registrar_materias.html', {
        'form': form,
        'estudiante': estudiante,
        'semestre': semestre,
        'materias': materias,
        'user_name': request.user.username,  # Para mostrar en la navbar
    })

@login_required
def eliminar_materia(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id)
    
    # Verificar que la materia pertenezca al semestre del estudiante actual
    if materia.semestre.estudiante.user != request.user:
        messages.error(request, "No tienes permiso para eliminar esta materia.")
        return redirect('registrar_materias')
    
    nombre_materia = materia.nombre
    materia.delete()
    messages.success(request, f"La materia '{nombre_materia}' ha sido eliminada.")
    return redirect('registrar_materias')