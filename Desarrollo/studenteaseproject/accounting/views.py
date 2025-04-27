from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import UserForm, EstudianteForm

# Create your views here.

def landing(request):
    return render(request, 'landing.html')


def sign_up(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        estudiante_form = EstudianteForm(request.POST)
        if user_form.is_valid() and estudiante_form.is_valid():
            if request.POST['password1'] == request.POST['password2']:
                user = user_form.save()

                estudiante = estudiante_form.save(commit=False)
                estudiante.user = user
                estudiante.save()
                messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
                return redirect('login')
    else:
        user_form = UserForm()
        estudiante_form = EstudianteForm()

    return render(request, 'signup.html', {'user_form': user_form, 'estudiante_form': estudiante_form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, '¡Has iniciado sesión correctamente!')
            return redirect('home')  # Redirigir al home
        else:
            messages.error(request, 'Error en el nombre de usuario o la contraseña.')

    return render(request, 'login.html')
