from django.urls import path
from . import views

urlpatterns = [
    path('chatbot/', views.chatbot_page, name='chatbot'),
    path('chatbot/response/', views.chat_response, name='chat_response'),
]





