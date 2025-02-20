from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, Category, UserAnswer  # Asegúrate de importar UserAnswer
from django.utils.timezone import now
from django.http import JsonResponse


def start_test(request, category_id):
    """
    Inicia el test con la primera pregunta.
    """
    # Obtén la categoría seleccionada
    category = get_object_or_404(Category, id=category_id)

    # Obtén el usuario actual
    user = request.user

    # Filtrar las preguntas aprendidas por el usuario
    learned_question_numbers = UserAnswer.objects.filter(
        user=user,
        category=category.name,  # Asumiendo que el nombre de la categoría se usa para identificar
        correctAnswerCounterTotal__gte=4
    ).values_list('number', flat=True)

    # Selecciona la primera pregunta que no esté en las aprendidas
    first_question = Test.objects.filter(
        category=category
    ).exclude(number__in=learned_question_numbers).order_by('number').first()

    if not first_question:
        return render(request, 'error.html', {'message': 'No hay preguntas disponibles en esta categoría'})

    # Redirige a la primera pregunta válida
    return redirect('learning_app:next_question', category_id=category_id, question_number=first_question.number)



def next_question(request, category_id, question_number):
    """
    Muestra la pregunta actual y prepara la siguiente en función del progreso.
    """
    # Obtén la categoría seleccionada
    category = get_object_or_404(Category, id=category_id)

    # Obtén el usuario actual
    user = request.user

    # Filtrar las preguntas aprendidas por el usuario
    learned_question_numbers = UserAnswer.objects.filter(
        user=user,
        category=category.name,  # Asumiendo que el nombre de la categoría se usa para identificar
        correctAnswerCounterTotal__gte=4
    ).values_list('number', flat=True)

    # Filtrar las preguntas no aprendidas y ordenar por número
    questions = Test.objects.filter(
        category=category
    ).exclude(number__in=learned_question_numbers).order_by('number')[:10]  # Limita a 10 preguntas

    total_questions = questions.count()

    if total_questions == 0:
        return render(request, 'error.html', {'message': 'No hay más preguntas disponibles en esta categoría'})

    # Ajusta el índice de la pregunta actual dentro del rango válido
    adjusted_question_number = (question_number - 1) % total_questions
    question = questions[adjusted_question_number]

    # Genera un rango para el progreso en la plantilla
    progress_range = range(1, total_questions + 1)

    context = {
        'test': question,
        'category': category,
        'totalQuestions': total_questions,
        'currentQuestion': adjusted_question_number + 1,
        'progressRange': progress_range,  # Agrega el rango al contexto
    }

    return render(request, 'home/preguntas.html', context)
def submit_answer(request, category_id, question_number):
    """
    Procesa la respuesta del usuario, guarda la respuesta en la tabla UserAnswer,
    y redirige a la siguiente pregunta mostrando si fue correcta o no.
    """
    if request.method == 'POST':
        user = request.user  # Usuario actual
        user_answer = request.POST.get('answer')  # Respuesta del usuario
        category = get_object_or_404(Category, id=category_id)

        # Obtener la pregunta actual
        question = get_object_or_404(Test, category=category, number=question_number)

        # Validar la respuesta del usuario
        is_correct = user_answer == question.correctAnswer

        # Guarda la respuesta en UserAnswer
        user_answer_entry, created = UserAnswer.objects.get_or_create(
            user=user,
            number=question.number,
            category=category.name,
            defaults={
                'answerProgresionCorrect': 0,
                'correctAnswerCounterTotal': 0,
                'incorrectAnswerCounterTotal': 0,
                'questionCircleCounter': 1,
                'lastAnsweredQuestion': question.number,
                'datetime': now(),
            }
        )

        if is_correct:
            user_answer_entry.answerProgresionCorrect += 1
            user_answer_entry.correctAnswerCounterTotal += 1
        else:
            user_answer_entry.answerProgresionCorrect = 0
            user_answer_entry.incorrectAnswerCounterTotal += 1

        user_answer_entry.lastAnsweredQuestion = question.number
        user_answer_entry.datetime = now()
        user_answer_entry.save()

        # Determinar la siguiente pregunta
        learned_question_numbers = UserAnswer.objects.filter(
            user=user,
            category=category.name,
            correctAnswerCounterTotal__gte=4
        ).values_list('number', flat=True)

        next_question = Test.objects.filter(
            category=category
        ).exclude(number__in=learned_question_numbers).filter(number__gt=question.number).order_by('number').first()

        if next_question:
            # Mostrar si fue correcta o no en la siguiente pregunta
            return render(request, 'home/preguntas.html', {
                'test': next_question,
                'category': category,
                'is_correct': is_correct,
                'correct_answer': question.correctAnswer,
                'user_answer': user_answer,
                'currentQuestion': next_question.number
            })

        # Si no hay más preguntas, mostrar un mensaje de finalización
        return render(request, 'home/test_completed.html', {
            'message': '¡Test completado!',
            'is_correct': is_correct,
            'correct_answer': question.correctAnswer,
            'user_answer': user_answer
        })

    return JsonResponse({'error': 'Método no permitido'}, status=405)
