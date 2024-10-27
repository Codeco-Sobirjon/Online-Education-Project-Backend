from django.urls import path

from apps.chat.views import ChatView, ChatDetailView

urlpatterns = [
    path('chats/', ChatView.as_view(), name='chat-list'),
    path('chats/<str:chat_id>/', ChatDetailView.as_view(), name='chat-detail'),
]
