import os
from dotenv import load_dotenv
import openai
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from accounting.models import Estudiante
from userspace.models import Semestre, Materia

from django.views.decorators.csrf import csrf_exempt

_ = load_dotenv('openAI.env')
# Configura tu clave API en settings.py como OPENAI_API_KEY
client = openai.OpenAI(
                # This is the default and can be omitted
                api_key=os.environ.get('openAI_api_key'),
            )   

@login_required
def chatbot_page(request):
    estudiante = Estudiante.objects.get(user=request.user)
    context = {
        'user_name': request.user.username,
        'nombre': estudiante.nombre,
    }
    return render(request, 'chatbot.html', context)


@login_required
@csrf_exempt
def chat_response(request):
    estudiante = Estudiante.objects.get(user=request.user)
    semestre = Semestre.objects.filter(estudiante=estudiante).last()
    materias_lista = Materia.objects.filter(semestre=semestre)

    materias = ""
    for materia in materias_lista:
        materias += f"\nNombre de la materia: {materia.nombre}, Créditos: {materia.creditos}, Nota: {materia.nota}, Porcentaje evaluado: {materia.porcentaje_evaluado}\n"

    # Definir el system_prompt siempre
    system_prompt = f"""
    Eres un mentor académico en español llamado "StudentEaseBot". Tu objetivo es ayudar al estudiante llamado {estudiante.nombre}, que estudia {estudiante.programa}.
    Su tipo de aprendizaje es {estudiante.tipo_aprendizaje}, y tiene { 'apoyo financiero' if estudiante.apoyo_financiero else 'no apoyo financiero' }.
    Está actualmente en el semestre {estudiante.semestre_set.last().numero_semestre}.

    Semestre actual: {semestre.numero_semestre}, Créditos: {semestre.numero_creditos}, Horas libres: {semestre.horas_libres}.

    Materias cursadas:
    {materias}

    Habla de forma positiva, relajante, motivadora, sencilla y cercana. Haz preguntas pequeñas para mantener la conversación activa, enfócate en bajar su estrés y organizar sus actividades académicas.
    """

    # Inicializar historial si no existe
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    if request.method == 'POST':
        user_message = request.POST.get('message')

        # Cargar historial
        chat_history = request.session['chat_history']
        chat_history.append({"role": "user", "content": user_message})

        # Preparar mensajes para enviar: primero system, luego historial
        messages_to_send = [{"role": "system", "content": system_prompt}] + chat_history

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages_to_send,
                temperature=0.3,
                max_tokens=1000,
            )

            bot_message = response.choices[0].message.content.strip()

            # Guardar respuesta en el historial
            chat_history.append({"role": "assistant", "content": bot_message})

            # Actualizar historial en la sesión
            request.session['chat_history'] = chat_history

            return JsonResponse({'response': bot_message})

        except Exception as e:
            print(f"Error llamando a OpenAI: {e}")
            return JsonResponse({'response': 'Hubo un error al procesar tu mensaje.'})
