from os import name
from django.urls import include, path
from . import views_chatgpt
from .views_chatgpt import NextQuestionView
from . import views




app_name = 'learning_app'

urlpatterns = [
    path('start-test/<int:category_id>/', views.start_test, name='startTest'),
    path('next-question/<int:category_id>/<int:question_number>/', views.next_question, name='next_question'),
    path('submit-answer/<int:category_id>/<int:question_number>/', views.submit_answer, name='submit_answer'),
]