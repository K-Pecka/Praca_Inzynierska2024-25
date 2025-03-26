from django.urls import path

from chats.views.chat_message_views import ChatMessageCreateAPIView, ChatMessageRetrieveAPIView, ChatMessageListAPIView, \
    ChatMessageUpdateAPIView, ChatMessageDestroyAPIView
from chats.views.chatroom_views import ChatroomCreateAPIView, ChatroomRetrieveAPIView, ChatroomListAPIView, \
    ChatroomUpdateAPIView, ChatroomDestroyAPIView

urlpatterns = [
    # Chatroom URLs
    # path('create/', ChatroomCreateAPIView.as_view(), name='chatroom-create'),
    path('<int:pk>/', ChatroomRetrieveAPIView.as_view(), name='chatroom-retrieve'),
    path('all/', ChatroomListAPIView.as_view(), name='chatroom-list'),
    path('<int:pk>/update/', ChatroomUpdateAPIView.as_view(), name='chatroom-update'),
    path('<int:pk>/delete/', ChatroomDestroyAPIView.as_view(), name='chatroom-delete'),

    # ChatMessage URLs
    path('<int:room_pk>/chat-message/create/', ChatMessageCreateAPIView.as_view(), name='chat-message-create'),
    path('<int:room_pk>/chat-message/<int:pk>/', ChatMessageRetrieveAPIView.as_view(), name='chat-message-retrieve'),
    path('<int:room_pk>/chat-message/all/', ChatMessageListAPIView.as_view(), name='chat-message-list'),
    path('<int:room_pk>/chat-message/<int:pk>/update/', ChatMessageUpdateAPIView.as_view(), name='chat-message-update'),
    path('<int:room_pk>/chat-message/<int:pk>/delete/', ChatMessageDestroyAPIView.as_view(), name='chat-message-delete'),
]
