from django.urls import path
from . import views


urlpatterns = [
    path('chat/', views.chat_view, name='chat_view'),
    path('api/get_response/', views.get_bot_response, name='get_bot_response'),
    path('end_conversation/', views.end_conversation, name='end_conversation'),
]