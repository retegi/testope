from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Test, Ope, UserAnswer,  MyLearning, Topic
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, ListView

from django.utils import timezone


class StartTestView(LoginRequiredMixin, View):
    def get(self, request, ope_id, topic_id):
        user = request.user
        ope = get_object_or_404(Ope, id=ope_id)
        topic = get_object_or_404(Topic, id=topic_id, ope=ope)

        all_questions = Test.objects.filter(topic=topic).order_by('number')
        total_questions = all_questions.count()
        all_numbers = list(all_questions.values_list('number', flat=True))

        if total_questions == 0:
            return render(request, 'home/no_questions.html', {'ope': ope, 'topic': topic})

        progreso_usuario = UserAnswer.objects.filter(user=user, ope=ope, number__in=all_numbers).order_by('number')
        learned_numbers = set(
            progreso_usuario.filter(answerProgresionCorrect__gte=4).values_list('number', flat=True)
        )

        # Preguntas no aprendidas
        unlearned_questions = [q for q in all_questions if q.number not in learned_numbers]

        if not unlearned_questions:
            return render(request, 'home/test_completed.html', {'ope': ope, 'topic': topic})

        # Obtener ciclo actual desde sesión
        session_key = f'cycle_{ope_id}_{topic_id}'
        current_cycle_numbers = request.session.get(session_key)

        # Asegurar que sea una lista válida
        if not isinstance(current_cycle_numbers, list):
            current_cycle_numbers = []

        # Eliminar del ciclo las ya aprendidas
        current_cycle_numbers = [n for n in current_cycle_numbers if n not in learned_numbers]

        # Rellenar ciclo con nuevas preguntas no aprendidas
        next_candidates = [q for q in unlearned_questions if q.number not in current_cycle_numbers]
        while len(current_cycle_numbers) < 10 and next_candidates:
            current_cycle_numbers.append(next_candidates.pop(0).number)

        # Si el ciclo está vacío (puede pasar si todas han sido aprendidas justo ahora)
        if not current_cycle_numbers:
            return render(request, 'home/test_completed.html', {'ope': ope, 'topic': topic})

        # Guardar el ciclo actualizado
        request.session[session_key] = current_cycle_numbers
        request.session.modified = True

        # Cargar objetos Test del ciclo
        cycle_questions = Test.objects.filter(topic=topic, number__in=current_cycle_numbers).order_by('number')

        # Última pregunta respondida en el ciclo
        last_answer = progreso_usuario.filter(number__in=current_cycle_numbers).order_by('-datetime').first()
        last_number = last_answer.lastAnsweredQuestion if last_answer else -1

        # Ordenar el ciclo y seleccionar la siguiente pregunta
        sorted_cycle = list(cycle_questions.order_by('number'))

        # Si el ciclo quedó vacío por alguna razón, evitar error
        if not sorted_cycle:
            return render(request, 'home/test_completed.html', {'ope': ope, 'topic': topic})

        next_question = None
        for q in sorted_cycle:
            if q.number > last_number:
                next_question = q
                break

        if not next_question:
            next_question = sorted_cycle[0]  # reiniciar el ciclo si ya se llegó al final

        return render(request, 'home/preguntas.html', {
            'test': next_question,
            'currentQuestion': next_question.number,
            'totalQuestions': total_questions,
            'ope': ope,
            'topic': topic,
            'learned_question_numbers': learned_numbers,
            'questionList': progreso_usuario,
        })



class SubmitAnswerView(LoginRequiredMixin, View):
    def post(self, request, ope_id, topic_id, test_id):
        user = request.user
        ope = get_object_or_404(Ope, id=ope_id)
        topic = get_object_or_404(Topic, id=topic_id, ope=ope)
        test = get_object_or_404(Test, id=test_id, ope=ope, topic=topic)

        user_answer_value = request.POST.get("respuesta")  # debe ser name="respuesta" en el form
        is_correct = (user_answer_value == test.correctAnswer)

        # Obtener o crear UserAnswer para este número de pregunta
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

        # Actualizar progreso
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

        # Redirigir a la siguiente pregunta
        return redirect('learning_app:start_test', ope_id=ope.id, topic_id=topic.id)





"""class StartTestView(LoginRequiredMixin, View):
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
        })"""




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
    
class TopicProgressView(LoginRequiredMixin, ListView):
    model = Topic
    template_name = 'home/my_ope_topics_progress.html'
    context_object_name = 'temas'

    def get_queryset(self):
        ope_id = self.kwargs['ope_id']
        return Topic.objects.filter(ope_id=ope_id).order_by('number')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        temas = context['temas']
        progresos = []

        for tema in temas:
            preguntas = Test.objects.filter(topic=tema)
            total = preguntas.count()
            pregunta_ids = preguntas.values_list('id', flat=True)

            respuestas_usuario = UserAnswer.objects.filter(
                user=user,
                number__in=pregunta_ids,
                ope=tema.ope
            )

            aprendidas = respuestas_usuario.filter(answerProgresionCorrect__gte=4).count()

            progresos.append({
                'tema': tema,
                'total': total,
                'aprendidas': aprendidas,
                'porcentaje': round((aprendidas / total) * 100) if total > 0 else 0,
                'detalles': respuestas_usuario.order_by('number')  # para mostrar progreso visual
            })


        context['progresos'] = progresos
        context['ope'] = Ope.objects.get(id=self.kwargs['ope_id'])
        return context