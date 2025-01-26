from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
)
from rest_framework.permissions import IsAuthenticated
from .models import Chatroom, ChatMessage
from .serializers import (
ChatroomCreateSerializer, ChatroomUpdateSerializer, ChatMessageCreateSerializer, ChatroomSerializer,
ChatMessageSerializer
)


# Chatroom Views
class ChatroomCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatroomCreateSerializer


class ChatroomRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatroomSerializer

    def get_object(self):
        return Chatroom.objects.get(pk=self.kwargs['pk'])


class ChatroomUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatroomUpdateSerializer

    def get_object(self):
        return Chatroom.objects.get(pk=self.kwargs['pk'])


class ChatroomDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatroomSerializer

    def get_object(self):
        return Chatroom.objects.get(pk=self.kwargs['pk'])


class ChatroomListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatroomSerializer

    def get_queryset(self):
        return Chatroom.objects.all()

# ChatMessage Views
class ChatMessageCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageCreateSerializer


class ChatMessageRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer

    def get_object(self):
        return ChatMessage.objects.get(pk=self.kwargs['pk'])


class ChatMessageUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer

    def get_object(self):
        return ChatMessage.objects.get(pk=self.kwargs['pk'])


class ChatMessageDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer

    def get_object(self):
        return ChatMessage.objects.get(pk=self.kwargs['pk'])


class ChatMessageListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        return ChatMessage.objects.all()
