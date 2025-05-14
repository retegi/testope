from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Test, Ope, UserAnswer,  MyLearning
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView

from django.utils import timezone


class StartTestView(LoginRequiredMixin, View):
    def get(self, request, ope_id):
        user = request.user
        ope = get_object_or_404(Ope, id=ope_id)

        # Todas las preguntas ordenadas por número
        all_questions = Test.objects.filter(ope=ope).order_by('number')
        total_questions = all_questions.count()

        if total_questions == 0:
            return render(request, 'home/no_questions.html', {'ope': ope})

        # Números de preguntas aprendidas (progresión >= 4)
        learned_numbers = UserAnswer.objects.filter(
            user=user, ope=ope, answerProgresionCorrect__gte=4
        ).values_list('number', flat=True)

        # Filtrar las preguntas no aprendidas
        unlearned_questions = [q for q in all_questions if q.number not in learned_numbers]

        if not unlearned_questions:
            return render(request, 'home/test_completed.html', {'ope': ope})

        # Obtener la última pregunta respondida (puede ser aprendida o no)
        last_answer = UserAnswer.objects.filter(user=user, ope=ope).order_by('-datetime').first()
        last_number = last_answer.lastAnsweredQuestion if last_answer else 0

        # Generar el ciclo de 10 preguntas activas, saltando las aprendidas
        cycle_questions = []
        seen = set()
        for q in unlearned_questions:
            if q.number > last_number and q.number not in seen:
                cycle_questions.append(q)
                seen.add(q.number)
                if len(cycle_questions) == 10:
                    break
        for q in unlearned_questions:
            if q.number not in seen:
                cycle_questions.append(q)
                seen.add(q.number)
                if len(cycle_questions) == 10:
                    break

        if not cycle_questions:
            return render(request, 'home/test_completed.html', {'ope': ope})

        # Determinar la siguiente pregunta
        next_question = None
        for q in cycle_questions:
            if q.number > last_number:
                next_question = q
                break
        if not next_question:
            next_question = cycle_questions[0]  # Si no hay mayor, volver al inicio del ciclo

        return render(request, 'home/preguntas.html', {
            'test': next_question,
            'currentQuestion': next_question.number,
            'totalQuestions': total_questions,
            'ope': ope,
            'learned_question_numbers': learned_numbers,
            'progresion_questions': UserAnswer.objects.filter(user=user, ope=ope)
        })


class SubmitAnswerView(LoginRequiredMixin, View):
    def post(self, request, ope_id, test_number):
        user = request.user
        ope = get_object_or_404(Ope, id=ope_id)
        test = get_object_or_404(Test, ope=ope, number=test_number)

        user_answer_value = request.POST.get("answer")
        is_correct = (user_answer_value == test.correctAnswer)

        # Obtener o crear UserAnswer para esta pregunta
        user_answer, created = UserAnswer.objects.get_or_create(
            user=user,
            ope=ope,
            number=test.number,
            defaults={
                'answerProgresionCorrect': 0,
                'correctAnswerCounterTotal': 0,
                'incorrectAnswerCounterTotal': 0,
                'questionCircleCounter': 0,
                'lastAnsweredQuestion': test.number,
                'datetime': timezone.now()
            }
        )

        # Actualizar datos
        user_answer.lastAnsweredQuestion = test.number
        user_answer.datetime = timezone.now()
        user_answer.questionCircleCounter = (user_answer.questionCircleCounter or 0) + 1

        if is_correct:
            user_answer.answerProgresionCorrect = (user_answer.answerProgresionCorrect or 0) + 1
            user_answer.correctAnswerCounterTotal = (user_answer.correctAnswerCounterTotal or 0) + 1
        else:
            user_answer.answerProgresionCorrect = 0
            user_answer.incorrectAnswerCounterTotal = (user_answer.incorrectAnswerCounterTotal or 0) + 1

        user_answer.save()

        # Redirigir al ciclo de 10 activas, omitiendo las aprendidas
        return redirect('learning_app:start_test', ope_id=ope.id)



class StartTestView(LoginRequiredMixin, View):
    def get(self, request, ope_id):
        user = request.user
        ope = get_object_or_404(Ope, id=ope_id)

        # Todas las preguntas de esta OPE
        all_questions = Test.objects.filter(ope=ope).order_by('number')
        total_questions = all_questions.count()

        # IDs de preguntas que el usuario ya ha aprendido (progress == 4)
        learned_numbers = UserAnswer.objects.filter(user=user, ope=ope, answerProgresionCorrect=4).values_list('number', flat=True)

        # Lista de preguntas no aprendidas
        unlearned_questions = [q for q in all_questions if q.number not in learned_numbers]

        # Última pregunta que respondió (cualquiera, aprendida o no)
        last_answer = UserAnswer.objects.filter(user=user, ope=ope).order_by('-datetime').first()
        last_number = last_answer.lastAnsweredQuestion if last_answer else 0

        # Crear el ciclo de 10 preguntas activas, ignorando aprendidas
        cycle_questions = []
        for q in unlearned_questions:
            if len(cycle_questions) < 10:
                if q.number > last_number or last_number == 0:
                    cycle_questions.append(q)
        # Si no hay suficientes tras el número actual, completamos desde el inicio
        for q in unlearned_questions:
            if len(cycle_questions) < 10 and q not in cycle_questions:
                cycle_questions.append(q)

        # Si no quedan preguntas nuevas sin aprender
        if not cycle_questions:
            return render(request, 'home/test_completed.html', {'ope': ope})

        # Buscar la siguiente pregunta en el ciclo (siguiendo orden tras la última)
        next_question = None
        for q in cycle_questions:
            if q.number > last_number:
                next_question = q
                break
        if not next_question:
            # Si no hay ninguna con número mayor, volver al inicio del ciclo
            next_question = cycle_questions[0]

        return render(request, 'home/preguntas.html', {
            'test': next_question,
            'currentQuestion': next_question.number,
            'totalQuestions': total_questions,
            'ope': ope,
            'learned_question_numbers': learned_numbers,
            'questionList': UserAnswer.objects.filter(user=user, ope=ope).order_by('number'),
        })




class AddToMyLearningView(LoginRequiredMixin, View):
    def post(self, request, ope_id):
        ope = get_object_or_404(Ope, id=ope_id)
        MyLearning.objects.get_or_create(user=request.user, ope=ope)
        return redirect('home_app:home')  # o la vista que tú quieras redirigir


class TestCompletedView(LoginRequiredMixin, TemplateView):
    template_name = 'home/test_completed.html'

class ResetOpeProgressView(LoginRequiredMixin, View):
    def post(self, request, ope_id):
        ope = get_object_or_404(Ope, id=ope_id)
        UserAnswer.objects.filter(user=request.user, ope=ope).delete()
        return redirect('learning_app:start_test', ope_id=ope.id)