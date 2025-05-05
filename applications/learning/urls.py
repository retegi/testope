from os import name
from django.urls import include, path
from . import views
from .views import AddToMyLearningView

app_name = 'learning_app'

urlpatterns = [
    path('start-test/<int:ope_id>/', views.start_test, name='startTest'),
    path('next-question/<int:ope_id>/<int:question_number>/<int:total_questions>/', views.next_question, name='next_question'),
    path('submit-answer/<int:ope_id>/<int:question_number>/', views.submit_answer, name='submit_answer'),
    path('add-to-my-learning/<int:ope_id>/', AddToMyLearningView.as_view(), name='add_to_my_learning'),
]