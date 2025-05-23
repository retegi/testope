from os import name
from django.urls import include, path
from . import views
from .views import AddToMyLearningView, TestCompletedView, SubmitAnswerView, StartTestView, ResetOpeProgressView, TopicProgressView


app_name = 'learning_app'

urlpatterns = [
    # Página de selección de temas de una OPE
    path('ope/<int:ope_id>/temas/', TopicProgressView.as_view(), name='my_ope_topics'),

    # Comenzar test para un topic concreto de una OPE
    path('ope/<int:ope_id>/topic/<int:topic_id>/comenzar/', StartTestView.as_view(), name='start_test'),

    # Enviar respuesta para una pregunta de un test
    #path('ope/<int:ope_id>/topic/<int:topic_id>/respuesta/<int:test_id>/', SubmitAnswerView.as_view(), name='submit_answer'),
    path('ope/<int:ope_id>/topic/<int:topic_id>/respuesta/numero/<int:number>/', SubmitAnswerView.as_view(), name='submit_answer'),


    # Finalización del test en un topic concreto
    path('ope/<int:ope_id>/topic/<int:topic_id>/completado/', TestCompletedView.as_view(), name='test_completed'),

    # Añadir a mi aprendizaje una OPE
    path('anadir-aprendizaje/<int:ope_id>/', AddToMyLearningView.as_view(), name='add_to_my_learning'),

    # Reiniciar el progreso en una OPE
    path('reset/<int:ope_id>/', ResetOpeProgressView.as_view(), name='reset_progress'),
]
