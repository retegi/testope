from django.shortcuts import render
from django.http import JsonResponse
import openai
from django.conf import settings
import os



MAX_HISTORY = 20  # Mantén los últimos 10 mensajes


def chat_view(request):
    return render(request, 'home/chat.html')

def load_instructions():
    instructions_path = os.path.join(settings.BASE_DIR, 'indications', 'instructions.txt')
    try:
        with open(instructions_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "Eres un asistente virtual amigable y útil."

def get_bot_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        openai.api_key = settings.OPENAI_API_KEY

        # Carga las instrucciones desde el archivo
        instructions = load_instructions()
        print("Instrucciones enviadas al modelo:", instructions)

        try:
            # Enviar las instrucciones junto con el mensaje del usuario
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": instructions},  # Instrucciones
                    {"role": "user", "content": user_message}  # Mensaje del usuario
                ]
            )

            bot_reply = response['choices'][0]['message']['content']
            return JsonResponse({'reply': bot_reply})
        except Exception as e:
            print(f"Error con OpenAI: {e}")  # Depuración
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request'})



def end_conversation(request):
    if 'conversation_history' in request.session:
        del request.session['conversation_history']
    return JsonResponse({'status': 'Conversación finalizada'})


