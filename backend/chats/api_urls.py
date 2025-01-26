from django.urls import path
from .api_views import (
    ChatroomListAPIView, ChatroomCreateAPIView, ChatroomRetrieveAPIView, ChatroomUpdateAPIView, ChatroomDestroyAPIView,
    ChatMessageListAPIView, ChatMessageCreateAPIView, ChatMessageRetrieveAPIView, ChatMessageUpdateAPIView,
    ChatMessageDestroyAPIView
)

urlpatterns = [
    # Chatroom URLs
    path('chatroom/', ChatroomListAPIView.as_view(), name='chatroom-list'),
    path('chatroom/create/', ChatroomCreateAPIView.as_view(), name='chatroom-create'),
    path('chatroom/<int:pk>/', ChatroomRetrieveAPIView.as_view(), name='chatroom-retrieve'),
    path('chatroom/<int:pk>/update/', ChatroomUpdateAPIView.as_view(), name='chatroom-update'),
    path('chatroom/<int:pk>/delete/', ChatroomDestroyAPIView.as_view(), name='chatroom-delete'),

    # ChatMessage URLs
    path('chat-message/', ChatMessageListAPIView.as_view(), name='chat-message-list'),
    path('chat-message/create/', ChatMessageCreateAPIView.as_view(), name='chat-message-create'),
    path('chat-message/<int:pk>/', ChatMessageRetrieveAPIView.as_view(), name='chat-message-retrieve'),
    path('chat-message/<int:pk>/update/', ChatMessageUpdateAPIView.as_view(), name='chat-message-update'),
    path('chat-message/<int:pk>/delete/', ChatMessageDestroyAPIView.as_view(), name='chat-message-delete'),
]
