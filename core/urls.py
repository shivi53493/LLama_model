# core/urls.py

from django.urls import path
from .views import chat_view, upload_file,test_view,stream_question

urlpatterns = [
    path('', chat_view, name='chat'),
    path('upload/', upload_file, name='upload_file'),
    path('test/', test_view, name='test'),
    path("stream/", stream_question,name="stream-question"),
]
