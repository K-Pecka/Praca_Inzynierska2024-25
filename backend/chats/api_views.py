from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
)
from rest_framework.permissions import IsAuthenticated

from users.models import UserProfile
from .models import Chatroom, ChatMessage
from .permissions import IsCreatorForChatroom, IsParticipantForChatroom, CanSendMessageInChatroom, IsCreatorForChatMessage
from .serializers import (
    ChatroomCreateSerializer, ChatroomUpdateSerializer, ChatMessageCreateSerializer, ChatroomSerializer,
    ChatMessageSerializer, ChatMessageUpdateSerializer
)


# Chatroom Views
class ChatroomCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatroomCreateSerializer


class ChatroomRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsParticipantForChatroom]
    serializer_class = ChatroomSerializer

    def get_object(self):
        return Chatroom.objects.get(pk=self.kwargs['pk'])


class ChatroomUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsCreatorForChatroom]
    serializer_class = ChatroomUpdateSerializer

    def get_object(self):
        return Chatroom.objects.get(pk=self.kwargs['pk'])


class ChatroomDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsCreatorForChatroom]
    serializer_class = ChatroomSerializer

    def get_object(self):
        return Chatroom.objects.get(pk=self.kwargs['pk'])


class ChatroomListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatroomSerializer

    def get_queryset(self):
        profile = self.request.user_profile
        return Chatroom.objects.filter(Q(creator=profile) | Q(members=profile)).distinct()


# ChatMessage Views
class ChatMessageCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, CanSendMessageInChatroom]
    serializer_class = ChatMessageCreateSerializer


class ChatMessageRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer

    def get_object(self):
        return ChatMessage.objects.get(chatroom=self.kwargs['room_pk'], pk=self.kwargs['pk'])


class ChatMessageUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsCreatorForChatMessage]
    serializer_class = ChatMessageUpdateSerializer

    def get_object(self):
        return ChatMessage.objects.get(chatroom=self.kwargs['room_pk'], pk=self.kwargs['pk'])


class ChatMessageDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsCreatorForChatMessage]
    serializer_class = ChatMessageSerializer

    def get_object(self):
        return ChatMessage.objects.get(chatroom=self.kwargs['room_pk'], pk=self.kwargs['pk'])


class ChatMessageListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        profile = self.request.user_profile
        return ChatMessage.objects.filter(chatroom=self.kwargs['room_pk'], profile=profile)
