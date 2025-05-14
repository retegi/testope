from os import name
from django.urls import include, path
from . import views
from .views import AddToMyLearningView, TestCompletedView, SubmitAnswerView, StartTestView, ResetOpeProgressView

app_name = 'learning_app'

urlpatterns = [
    #path('start-test/<int:ope_id>/', views.start_test, name='startTest'),
    #path('next-question/<int:ope_id>/<int:question_number>/<int:total_questions>/', views.next_question, name='next_question'),
    #path('submit-answer/<int:ope_id>/<int:question_number>/', views.submit_answer, name='submit_answer'),
    #path('add-to-my-learning/<int:ope_id>/', AddToMyLearningView.as_view(), name='add_to_my_learning'),

    path('comenzar/<int:ope_id>/', StartTestView.as_view(), name='start_test'),
    path('respuesta/<int:ope_id>/<int:test_number>/', SubmitAnswerView.as_view(), name='submit_answer'),

    path('completado/<int:ope_id>/', TestCompletedView.as_view(), name='test_completed'),


    path('anadir-aprendizaje/<int:ope_id>/', AddToMyLearningView.as_view(), name='add_to_my_learning'),
    path('reset/<int:ope_id>/', ResetOpeProgressView.as_view(), name='reset_progress'),
]
