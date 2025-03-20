from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('sessions/create/', views.create_chat_session, name='create_session'),
    path('sessions/<int:session_id>/messages/', views.send_message, name='send_message'),
    path('sessions/<int:session_id>/history/', views.get_chat_history, name='chat_history'),
    path('stats/', views.get_user_stats, name='user_stats'),
] 