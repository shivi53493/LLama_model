# core/urls.py

from django.urls import path
from .views import chat_view, upload_file, ask_question,test_view

urlpatterns = [
    path('', chat_view, name='chat'),
    path('upload/', upload_file, name='upload_file'),
    path('chat/', ask_question, name='ask_question'),
    path('test/', test_view, name='test'),
]
