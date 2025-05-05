from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, Topic, UserAnswer  # Asegúrate de importar UserAnswer
from django.utils.timezone import now
from django.http import JsonResponse

from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Test, UserAnswer, MyLearning, Ope
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin


def start_test(request, ope_id):
    """
    Inicia el test desde la primera pregunta no aprendida o desde donde el usuario lo dejó.
    Si ya se han respondido todas las preguntas, reinicia desde la primera disponible.
    """
    ope = get_object_or_404(Ope, id=ope_id)
    user = request.user
    print("Usuario actual:", user)
    print("Ope actual es:", ope_id)

    # Obtener el número total de preguntas de la categoría (ope)
    total_questions = Test.objects.filter(ope=ope).count()
    print("Total de preguntas: ", total_questions)

    # Obtener la última pregunta respondida por el usuario en esta categoría
    last_answered_question = (
        UserAnswer.objects.filter(user=user, ope=ope_id)
        .order_by('-lastAnsweredQuestion')
        .values_list('lastAnsweredQuestion', flat=True)
        .first()
    ) or 0  # Si no hay preguntas respondidas, empezamos desde la 1

    # Obtener preguntas ya aprendidas
    learned_question_numbers = list(
        UserAnswer.objects.filter(user=user, ope=ope, correctAnswerCounterTotal__gte=4)
        .values_list('number', flat=True)
    )

    # Si la última respondida es la última del total, reiniciar desde la primera
    if last_answered_question >= total_questions:
        last_answered_question = 0  # Reinicia el test

    # Intentar seleccionar la siguiente pregunta exacta
    first_question = (
        Test.objects.filter(ope=ope)
        .exclude(number__in=learned_question_numbers)
        .filter(number=last_answered_question + 1)
        .first()
    )

    # Si no existe la pregunta exacta, buscar la más cercana superior
    if not first_question:
        first_question = (
            Test.objects.filter(ope=ope)
            .exclude(number__in=learned_question_numbers)
            .filter(number__gt=last_answered_question)
            .order_by('number')
            .first()
        )

    if not first_question:
        return render(request, 'error.html', {
            'message': 'No hay preguntas disponibles en esta categoría',
            'totalQuestions': total_questions
        })

    return redirect('learning_app:next_question', ope_id=ope_id, question_number=first_question.number, total_questions=total_questions)



def next_question(request, ope_id, question_number, total_questions):
    """
    Selecciona la siguiente pregunta en orden, evitando preguntas ya aprendidas.
    Si se alcanza la última pregunta, vuelve a la primera.
    """
    ope = get_object_or_404(Ope, id=ope_id)
    user = request.user

    # Obtener preguntas aprendidas
    learned_question_numbers = UserAnswer.objects.filter(
        user=user, ope=ope, correctAnswerCounterTotal__gte=4
    ).values_list('number', flat=True)

    # Si la pregunta actual es la última, reiniciar desde la primera pregunta disponible
    if question_number > total_questions:
        question_number = 0  # Reinicia el test desde la primera

    # Intentar seleccionar la siguiente pregunta exacta
    next_question = (
        Test.objects.filter(ope=ope)
        .exclude(number__in=learned_question_numbers)
        .filter(number=question_number)
        .first()
    )

    # Si no existe la pregunta exacta, buscar la más cercana superior
    if not next_question:
        next_question = (
            Test.objects.filter(ope=ope)
            .exclude(number__in=learned_question_numbers)
            .filter(number__gt=question_number)
            .order_by('number')
            .first()
        )

    if not next_question:
        return render(request, 'error.html', {'message': 'No hay más preguntas disponibles en esta categoría'})

    context = {
        'test': next_question,
        'ope': ope,
        'currentQuestion': next_question.number,
        'totalQuestions': total_questions,
    }

    return render(request, 'home/preguntas.html', context)


def submit_answer(request, ope_id, question_number):
    if request.method == 'POST':
        user = request.user
        user_answer = request.POST.get('answer', '').strip()
        ope = get_object_or_404(Ope, id=ope_id)
        question = get_object_or_404(Test, ope=ope, number=question_number)

        if not user_answer:
            return JsonResponse({'error': 'No se recibió respuesta'}, status=400)

        is_correct = user_answer.lower() == question.correctAnswer.strip().lower()

        # Obtener o crear UserAnswer
        user_answer_entry, created = UserAnswer.objects.get_or_create(
            user=user,
            number=question.number,
            ope=ope,
            defaults={
                'answerProgresionCorrect': 0,
                'correctAnswerCounterTotal': 0,
                'incorrectAnswerCounterTotal': 0,
                'questionCircleCounter': 1,
                'lastAnsweredQuestion': question.number,
                'datetime': now(),
            }
        )

        # Actualizar datos del usuario según si la respuesta es correcta
        if is_correct:
            user_answer_entry.answerProgresionCorrect += 1
            user_answer_entry.correctAnswerCounterTotal += 1
        else:
            user_answer_entry.answerProgresionCorrect = 0
            user_answer_entry.incorrectAnswerCounterTotal += 1

        user_answer_entry.lastAnsweredQuestion = question.number
        user_answer_entry.datetime = now()
        user_answer_entry.save()

        # Buscar la siguiente pregunta
        learned_question_numbers = UserAnswer.objects.filter(
            user=user, ope=ope, correctAnswerCounterTotal__gte=4
        ).values_list('number', flat=True)

        next_question = (
            Test.objects.filter(ope=ope)
            .exclude(number__in=learned_question_numbers)
            .filter(number__gt=question.number)
            .order_by('number')
            .first()
        )

        if next_question:
            return redirect('learning_app:next_question', ope_id=ope_id, question_number=next_question.number, total_questions=Test.objects.filter(ope=ope).count())

        return render(request, 'home/test_completed.html', {
            'message': '¡Test completado!',
            'is_correct': is_correct,
            'correct_answer': question.correctAnswer,
            'user_answer': user_answer
        })

    return JsonResponse({'error': 'Método no permitido'}, status=405)
    if request.method == 'POST':
        user = request.user
        print("post user:",user)
        user_answer = request.POST.get('answer', '').strip()
        print("post user_answer",user_answer)
        ope = get_object_or_404(Ope, id=ope_id)
        print("post ope:",ope)
        question = get_object_or_404(Test, ope=ope, number=question_number)
        print("post question:",question)

        is_correct = user_answer.lower() == question.correctAnswer.strip().lower()

        # Obtener o crear UserAnswer
        user_answer_entry, created = UserAnswer.objects.get_or_create(
            user=user,
            number=question.number,
            ope=ope,
            defaults={
                'answerProgresionCorrect': 0,
                'correctAnswerCounterTotal': 0,
                'incorrectAnswerCounterTotal': 0,
                'questionCircleCounter': 1,
                'lastAnsweredQuestion': question.number,
                'datetime': now(),
            }
        )

        # Actualizar datos del usuario según si la respuesta es correcta
        if is_correct:
            user_answer_entry.answerProgresionCorrect += 1
            user_answer_entry.correctAnswerCounterTotal += 1
        else:
            user_answer_entry.answerProgresionCorrect = 0
            user_answer_entry.incorrectAnswerCounterTotal += 1

        user_answer_entry.lastAnsweredQuestion = question.number
        user_answer_entry.datetime = now()
        user_answer_entry.save()

        # Buscar la siguiente pregunta
        learned_question_numbers = UserAnswer.objects.filter(
            user=user, ope=ope, correctAnswerCounterTotal__gte=4
        ).values_list('number', flat=True)

        next_question = (
            Test.objects.filter(ope=ope)
            .exclude(number__in=learned_question_numbers)
            .filter(number__gt=question.number)
            .order_by('number')
            .first()
        )

        if next_question:
            return render(request, 'home/preguntas.html', {
                'test': next_question,
                'ope': ope,
                'is_correct': is_correct,
                'correct_answer': question.correctAnswer,
                'user_answer': user_answer,
                'currentQuestion': next_question.number
            })

        return render(request, 'home/test_completed.html', {
            'message': '¡Test completado!',
            'is_correct': is_correct,
            'correct_answer': question.correctAnswer,
            'user_answer': user_answer
        })

    return JsonResponse({'error': 'Método no permitido'}, status=405)


class AddToMyLearningView(LoginRequiredMixin, CreateView):
    model = MyLearning
    fields = []  # No usamos un formulario, solo procesamos la solicitud

    def post(self, request, *args, **kwargs):
        ope_id = self.kwargs.get("ope_id")
        ope = get_object_or_404(Ope, id=ope_id)

        # Verificar si ya existe en MyLearning para el usuario actual
        my_learning, created = MyLearning.objects.get_or_create(user=request.user, ope=ope)

        return redirect("home_app:home")  # Redirige a la lista de aprendizajes del usuario


