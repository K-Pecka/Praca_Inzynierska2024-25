from django.urls import path
from .api_views import (
    ChatroomListAPIView, ChatroomCreateAPIView, ChatroomRetrieveAPIView, ChatroomUpdateAPIView, ChatroomDestroyAPIView,
    ChatMessageListAPIView, ChatMessageCreateAPIView, ChatMessageRetrieveAPIView, ChatMessageUpdateAPIView,
    ChatMessageDestroyAPIView
)

urlpatterns = [
    # Chatroom URLs
    path('', ChatroomCreateAPIView.as_view(), name='chatroom-create'),
    path('all/', ChatroomListAPIView.as_view(), name='chatroom-list'),
    path('<int:pk>/', ChatroomRetrieveAPIView.as_view(), name='chatroom-retrieve'),
    path('<int:pk>/update/', ChatroomUpdateAPIView.as_view(), name='chatroom-update'),
    path('<int:pk>/delete/', ChatroomDestroyAPIView.as_view(), name='chatroom-delete'),

    # ChatMessage URLs
    path('chat-message/', ChatMessageCreateAPIView.as_view(), name='chat-message-create'),
    path('<int:room_pk>/chat-message/all/', ChatMessageListAPIView.as_view(), name='chat-message-list'),
    path('<int:room_pk>/chat-message/<int:pk>/', ChatMessageRetrieveAPIView.as_view(), name='chat-message-retrieve'),
    path('<int:room_pk>/chat-message/<int:pk>/update/', ChatMessageUpdateAPIView.as_view(), name='chat-message-update'),
    path('<int:room_pk>/chat-message/<int:pk>/delete/', ChatMessageDestroyAPIView.as_view(), name='chat-message-delete'),
]
