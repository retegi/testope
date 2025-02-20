from django.shortcuts import render
from django.views.generic import TemplateView, ListView, FormView
from applications.learning.models import Test, UserAnswer
from django.http import HttpResponse
from django.template import Template
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from applications.social.models import TestChat
from django.contrib.auth.models import User
from applications.learning.models import Category
from django.db.models import Q
from .models import Test
# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Category, Test, UserAnswer
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now


def get_next_question(user, category_name):
    # Obtener la categoría
    category = get_object_or_404(Category, name=category_name)

    # Obtener las respuestas del usuario para la categoría
    user_answers = UserAnswer.objects.filter(user=user, category=category_name).order_by('lastAnsweredQuestion')

    # Si es la primera vez en esta categoría
    if not user_answers.exists():
        first_question = Test.objects.filter(category=category).order_by('number').first()
        if first_question:
            return first_question, None
        else:
            return None, None  # No hay preguntas disponibles

    # Obtener las preguntas en el ciclo actual (10 preguntas)
    current_cycle_questions = user_answers.filter(questionCircleCounter__lt=4).order_by('number')[:10]

    if len(current_cycle_questions) < 10:
        # Agregar nuevas preguntas si hay menos de 10 preguntas activas
        available_questions = Test.objects.filter(category=category).exclude(
            number__in=user_answers.values_list('number', flat=True)
        ).order_by('number')

        for question in available_questions:
            if len(current_cycle_questions) >= 10:
                break

            UserAnswer.objects.create(
                user=user,
                number=question.number,
                category=category_name,
                answerProgresionCorrect=0,
                correctAnswerCounter=0,
                incorrectAnswerCounter=0,
                questionCircleCounter=0,
                lastAnsweredQuestion=question.number,
            )

            current_cycle_questions = user_answers.filter(questionCircleCounter__lt=4).order_by('number')[:10]

    # Seleccionar la siguiente pregunta
    if current_cycle_questions.exists():
        next_question = current_cycle_questions.first()
        return Test.objects.get(category=category, number=next_question.number), next_question

    return None, None  # No hay más preguntas activas

@login_required
def next_question_view(request, category_name):
    if request.method == "POST":
        user = request.user
        user_response = request.POST.get("response")
        question_number = request.POST.get("question_number")

        if not question_number:
            return JsonResponse({"error": "Número de pregunta no proporcionado."}, status=400)

        question_number = int(question_number)

        try:
            # Guardar la respuesta del usuario
            user_answer = UserAnswer.objects.get(user=user, category=category_name, number=question_number)
            test_question = Test.objects.get(category__name=category_name, number=question_number)

            if user_response == test_question.correctAnswer:
                user_answer.correctAnswerCounter += 1
                user_answer.incorrectAnswerCounter = 0
                if user_answer.correctAnswerCounter >= 4:
                    user_answer.questionCircleCounter += 1
                    user_answer.correctAnswerCounter = 0  # Reiniciar el contador para la pregunta
            else:
                user_answer.incorrectAnswerCounter += 1
                user_answer.correctAnswerCounter = 0

            user_answer.lastAnsweredQuestion = question_number
            user_answer.datetime = now()
            user_answer.save()

            # Obtener la siguiente pregunta
            next_question, _ = get_next_question(user, category_name)

            if next_question:
                return JsonResponse({
                    "question": next_question.question,
                    "aAnswer": next_question.aAnswer,
                    "bAnswer": next_question.bAnswer,
                    "cAnswer": next_question.cAnswer,
                    "dAnswer": next_question.dAnswer,
                    "number": next_question.number,
                })

            return JsonResponse({"message": "Has completado todas las preguntas de esta categoría."})

        except UserAnswer.DoesNotExist:
            return JsonResponse({"error": "La respuesta del usuario no existe."}, status=404)
        except Test.DoesNotExist:
            return JsonResponse({"error": "La pregunta no existe."}, status=404)

    return JsonResponse({"error": "Método no permitido"}, status=405)
