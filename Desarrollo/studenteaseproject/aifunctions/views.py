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



import os
import json
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Evento
from accounting.models import Estudiante
from userspace.models import Semestre, Materia
from .forms import EventoForm
import openai
from dotenv import load_dotenv
from django.contrib import messages

# Cargar variables de entorno
load_dotenv('openAI.env')
openai.api_key = os.getenv('OPENAI_API_KEY')

@login_required
def calendario(request):
    # Obtener el estudiante actual
    estudiante = Estudiante.objects.get(user=request.user)
    
    # Formulario para crear nuevo evento
    form = EventoForm()
    
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            nuevo_evento = form.save(commit=False)
            nuevo_evento.estudiante = estudiante
            nuevo_evento.save()
            messages.success(request, "Evento agregado correctamente")
            return redirect('calendario')
        else:
            messages.error(request, "Error al agregar el evento. Por favor verifica los datos.")
    
    # Obtener todos los eventos del estudiante
    eventos = Evento.objects.filter(estudiante=estudiante)
    
    # Obtener recomendaciones de IA
    recomendaciones = obtener_recomendaciones_ia(estudiante)
    
    context = {
        'eventos': eventos,  # Pasamos los eventos directamente, no como JSON
        'form': form,
        'recomendaciones': recomendaciones,
        'user_name': request.user.username,
        'nombre': estudiante.nombre
    }
    
    return render(request, 'calendario.html', context)

@login_required
def eliminar_evento(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    if evento.estudiante.user == request.user:
        evento.delete()
        messages.success(request, "Evento eliminado correctamente")
    return redirect('calendario')

def obtener_recomendaciones_ia(estudiante):
    try:
        # Obtener información relevante del estudiante
        semestre_actual = Semestre.objects.filter(estudiante=estudiante).last()
        materias = []
        if semestre_actual:
            materias = Materia.objects.filter(semestre=semestre_actual)
        
        # Construir el contexto para la IA
        contexto = {
            "tipo_aprendizaje": estudiante.tipo_aprendizaje,
            "programa": estudiante.programa,
            "condicion": estudiante.condicion,
            "semestre": semestre_actual.numero_semestre if semestre_actual else "No disponible",
            "creditos_totales": semestre_actual.numero_creditos if semestre_actual else 0,
            "horas_libres": semestre_actual.horas_libres if semestre_actual else 0,
            "materias": [{"nombre": m.nombre, "creditos": m.creditos, "nota": m.nota, 
                          "porcentaje_evaluado": m.porcentaje_evaluado} for m in materias]
        }
        
        # Eventos próximos
        eventos_proximos = Evento.objects.filter(
            estudiante=estudiante, 
            fecha__gte=datetime.now().date(),
            fecha__lte=datetime.now().date() + timedelta(days=14)
        ).order_by('fecha')
        
        eventos_texto = []
        for evento in eventos_proximos:
            eventos_texto.append(f"- {evento.nombre} ({evento.fecha.strftime('%Y-%m-%d')}): {evento.descripcion}")
        
        # Crear prompt para OpenAI
        prompt = f"""
        Eres un asistente académico para un estudiante universitario. Basado en la siguiente información, 
        proporciona 3-5 recomendaciones específicas sobre cómo organizar mejor su tiempo y reducir el estrés académico.
        
        INFORMACIÓN DEL ESTUDIANTE:
        - Tipo de aprendizaje: {contexto['tipo_aprendizaje']}
        - Programa académico: {contexto['programa']}
        - Condición especial: {contexto['condicion']}
        - Semestre actual: {contexto['semestre']}
        - Créditos totales: {contexto['creditos_totales']}
        - Horas libres semanales: {contexto['horas_libres']}
        
        MATERIAS ACTUALES:
        {json.dumps(contexto['materias'], indent=2, ensure_ascii=False)}
        
        EVENTOS PRÓXIMOS (14 DÍAS):
        {chr(10).join(eventos_texto) if eventos_texto else "No hay eventos próximos"}
        
        Proporciona recomendaciones personalizadas considerando:
        1. Su estilo de aprendizaje
        2. La carga académica actual
        3. Los eventos próximos
        4. Técnicas de gestión del tiempo y reducción de estrés
        
        Responde en español, con un tono amigable y motivador. Limita tu respuesta a 5 recomendaciones concretas.
        """
        
        # Llamada a la API de OpenAI
        model="gpt-4o-mini"

        messages = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature = 0,
            max_tokens = 1000,
        )
        
        # Extraer y devolver las recomendaciones
        recomendaciones = response.choices[0].message.content.strip()
        return recomendaciones
        
    except Exception as e:
        print(f"Error al obtener recomendaciones: {e}")
        return "No se pudieron generar recomendaciones en este momento. Por favor, intenta más tarde."
