from django.urls import path

from chats.views.message_views import MessageCreateAPIView, MessageRetrieveAPIView, MessageListAPIView, \
    MessageUpdateAPIView, MessageDestroyAPIView
from chats.views.chatroom_views import ChatroomCreateAPIView, ChatroomRetrieveAPIView, ChatroomListAPIView, \
    ChatroomUpdateAPIView, ChatroomDestroyAPIView

urlpatterns = [
    # Chatroom URLs
    path('create/', ChatroomCreateAPIView.as_view(), name='chatroom-create'),
    path('<int:pk>/', ChatroomRetrieveAPIView.as_view(), name='chatroom-retrieve'),
    path('all/', ChatroomListAPIView.as_view(), name='chatroom-list'),
    path('update/', ChatroomUpdateAPIView.as_view(), name='chatroom-update'),
    path('delete/', ChatroomDestroyAPIView.as_view(), name='chatroom-delete'),

    # Message URLs
    path('<int:room_pk>/chat-message/create/', MessageCreateAPIView.as_view(), name='chat-message-create'),
    path('<int:room_pk>/chat-message/<int:pk>/', MessageRetrieveAPIView.as_view(), name='chat-message-retrieve'),
    path('<int:room_pk>/chat-message/all/', MessageListAPIView.as_view(), name='chat-message-list'),
    path('<int:room_pk>/chat-message/<int:pk>/update/', MessageUpdateAPIView.as_view(), name='chat-message-update'),
    path('<int:room_pk>/chat-message/<int:pk>/delete/', MessageDestroyAPIView.as_view(), name='chat-message-delete'),
]
