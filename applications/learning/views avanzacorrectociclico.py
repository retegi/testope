from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, Category

from django.shortcuts import redirect

def start_test(request, category_id):
    """
    Inicia el test con la primera pregunta.
    """
    category = get_object_or_404(Category, id=category_id)
    first_question = Test.objects.filter(category=category).order_by('number').first()

    if not first_question:
        return render(request, 'error.html', {'message': 'No hay preguntas disponibles en esta categoría'})

    # Redirige a la primera pregunta
    return redirect('learning_app:next_question', category_id=category_id, question_number=1)

def next_question(request, category_id, question_number):
    """
    Muestra la pregunta actual y prepara la siguiente en función del progreso.
    """
    category = get_object_or_404(Category, id=category_id)
    questions = Test.objects.filter(category=category).order_by('number')[:10]  # Limita a 10 preguntas
    total_questions = questions.count()

    if total_questions == 0:
        return render(request, 'error.html', {'message': 'No hay preguntas disponibles en esta categoría'})

    # Ajusta el índice de la pregunta actual dentro del rango válido
    adjusted_question_number = (question_number - 1) % total_questions
    question = questions[adjusted_question_number]

    # Calcula el próximo número de pregunta para el ciclo
    next_question_number = (adjusted_question_number + 1) % total_questions + 1  # Corrección aquí

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
    Procesa la respuesta del usuario y avanza a la siguiente pregunta.
    """
    if request.method == 'POST':
        user_answer = request.POST.get('answer')
        category = get_object_or_404(Category, id=category_id)
        questions = Test.objects.filter(category=category).order_by('number')[:10]
        total_questions = questions.count()

        if total_questions == 0:
            return render(request, 'error.html', {'message': 'No hay preguntas disponibles en esta categoría'})

        # Ajustar índice de pregunta al rango válido
        adjusted_question_number = (question_number - 1) % total_questions
        question = questions[adjusted_question_number]

        # Determinar la siguiente pregunta
        next_question_number = (adjusted_question_number + 1) % total_questions + 1

        # Redirigir a la siguiente pregunta
        return redirect('learning_app:next_question', category_id=category_id, question_number=next_question_number)

    return redirect('learning_app:next_question', category_id=category_id, question_number=question_number)
