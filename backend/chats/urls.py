from django.urls import path, include

from rest_framework.routers import DefaultRouter

from chats.views.chatroom_views import ChatroomViewSet
from chats.views.message_views import MessageViewSet

router = DefaultRouter()
router.register(r'', ChatroomViewSet, basename='chatroom')

urlpatterns = [
    path('', include(router.urls)),

    # Message URLs
    path('<int:room_pk>/chat-message/', MessageViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='chat-message-list-create'),

    # retrieve, update, partial_update, destroy
    path('<int:room_pk>/chat-message/<int:pk>/', MessageViewSet.as_view({
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='chat-message-detail'),
]
