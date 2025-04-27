from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('crear_semestre/', views.crear_semestre, name='crear_semestre'),
    path('registrar_materias/', views.registrar_materias, name='registrar_materias'),
    path('eliminar-materia/<int:materia_id>/', views.eliminar_materia, name='eliminar_materia'),
]