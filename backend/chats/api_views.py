from django.db.models import Q
from rest_framework.exceptions import NotFound

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, get_object_or_404
)

from .models import Chatroom, ChatMessage
from .permissions import IsCreatorForChatroom, IsParticipantForChatroom, IsCreatorForChatMessage
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
        try:
            return Chatroom.objects.get(pk=self.kwargs['pk'])
        except Chatroom.DoesNotExist:
            raise NotFound(detail="Nie znaleziono czatu o podanym ID")


class ChatroomListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatroomSerializer

    def get_queryset(self):
        profile = self.request.user.profiles.filter(is_active=True)
        return Chatroom.objects.filter(Q(creator=profile) | Q(members=profile)).distinct()


class ChatroomUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsCreatorForChatroom]
    serializer_class = ChatroomUpdateSerializer

    def get_object(self):
        try:
            return Chatroom.objects.get(pk=self.kwargs['pk'])
        except Chatroom.DoesNotExist:
            raise NotFound(detail="Nie znaleziono czatu o podanym ID")


class ChatroomDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsCreatorForChatroom]
    serializer_class = ChatroomSerializer

    def get_object(self):
        try:
            return Chatroom.objects.get(pk=self.kwargs['pk'])
        except Chatroom.DoesNotExist:
            raise NotFound(detail="Nie znaleziono czatu o podanym ID")


# ChatMessage Views
class ChatMessageCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsParticipantForChatroom]
    serializer_class = ChatMessageCreateSerializer


class ChatMessageRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsParticipantForChatroom]
    serializer_class = ChatMessageSerializer

    def get_object(self):
        try:
            return ChatMessage.objects.get(chatroom=self.kwargs['room_pk'], pk=self.kwargs['pk'])
        except ChatMessage.DoesNotExist:
            raise NotFound("Nie znaleziono wiadomości o podanym ID")


class ChatMessageListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        return ChatMessage.objects.filter(chatroom=self.kwargs['room_pk'], profile=self.request.user.get_default_profile())


class ChatMessageUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsCreatorForChatMessage]
    serializer_class = ChatMessageUpdateSerializer

    def get_object(self):
        try:
            return ChatMessage.objects.get(chatroom=self.kwargs['room_pk'], pk=self.kwargs['pk'])
        except ChatMessage.DoesNotExist:
            raise NotFound("Nie znaleziono wiadomości o podanym ID")


class ChatMessageDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsCreatorForChatMessage]
    serializer_class = ChatMessageSerializer

    def get_object(self):
        try:
            return ChatMessage.objects.get(chatroom=self.kwargs['room_pk'], pk=self.kwargs['pk'])
        except ChatMessage.DoesNotExist:
            raise NotFound("Nie znaleziono wiadomości o podanym ID")
