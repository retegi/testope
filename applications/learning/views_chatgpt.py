from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.views import View
import json
from .models import Category, Test, UserAnswer


class NextQuestionView(View):
    def get(self, request, category_id):
        user = request.user
        category = get_object_or_404(Category, id=category_id)

        # Obtener la primera pregunta o la siguiente pregunta según el estado del usuario
        next_question, _ = get_next_question(user, category.name)

        if next_question:
            return render(request, 'home/preguntas.html', {
                'category': category,
                'question': next_question,
            })

        # Si no hay preguntas disponibles, renderizar con un mensaje
        return render(request, 'home/preguntas.html', {
            'category': category,
            'message': 'No hay más preguntas disponibles.',
        })

def get_next_question(user, category_name):
    category = get_object_or_404(Category, name=category_name)

    # Obtener respuestas del usuario en la categoría
    user_answers = UserAnswer.objects.filter(user=user, category=category_name).order_by('lastAnsweredQuestion')

    # Si es la primera vez en esta categoría
    if not user_answers.exists():
        first_question = Test.objects.filter(category=category).order_by('number').first()
        if first_question:
            # Crear registro inicial para el usuario
            UserAnswer.objects.create(
                user=user,
                number=first_question.number,
                category=category_name,
                answerProgresionCorrect=0,
                correctAnswerCounter=0,
                incorrectAnswerCounter=0,
                questionCircleCounter=0,
                lastAnsweredQuestion=first_question.number,
            )
            return first_question, None

    # Obtener ciclo actual de 10 preguntas
    current_cycle_questions = user_answers.filter(questionCircleCounter__lt=4).order_by('number')[:10]

    # Si hay menos de 10 preguntas activas, agregar nuevas preguntas
    if len(current_cycle_questions) < 10:
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

    return None, None
