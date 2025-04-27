from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('crear_semestre/', views.crear_semestre, name='crear_semestre'),
]