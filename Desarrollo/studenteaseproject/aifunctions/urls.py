from django.urls import path
from . import views

urlpatterns = [
    path('chatbot/', views.chatbot_page, name='chatbot'),
    path('chatbot/response/', views.chat_response, name='chat_response'),
    path('calendario/', views.calendario, name='calendario'),
    path('calendario/eliminar/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),
]





