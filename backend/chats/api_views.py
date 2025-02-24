from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
)

from .models import Chatroom, ChatMessage
from server.permissions import IsCreatorForChatroom, IsParticipantForChatroom, IsCreatorForChatMessage, \
    IsTripParticipant
from .serializers import (
    ChatroomCreateSerializer, ChatroomUpdateSerializer, ChatMessageCreateSerializer,
    ChatMessageUpdateSerializer, ChatroomRetrieveSerializer, ChatroomListSerializer,
    ChatroomDestroySerializer, ChatMessageRetrieveSerializer, ChatMessageListSerializer, ChatMessageDestroySerializer
)


#####################################################################
# Chatroom Views
#####################################################################
class ChatroomCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ChatroomCreateSerializer


class ChatroomRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom]
    serializer_class = ChatroomRetrieveSerializer

    def get_object(self):
        id = self.kwargs['pk']
        return Chatroom.objects.by_id(id)


class ChatroomListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ChatroomListSerializer

    def get_queryset(self):
        user = self.request.user.get_default_profile()
        return Chatroom.objects.by_user(user).select_related('creator').prefetch_related('members')


class ChatroomUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsCreatorForChatroom]
    serializer_class = ChatroomUpdateSerializer

    def get_object(self):
        id = self.kwargs['pk']
        return Chatroom.objects.by_id(id)


class ChatroomDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsCreatorForChatroom]
    serializer_class = ChatroomDestroySerializer

    def get_object(self):
        id = self.kwargs['pk']
        return Chatroom.objects.by_id(id)


#####################################################################
# ChatMessage Views
#####################################################################
class ChatMessageCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom]
    serializer_class = ChatMessageCreateSerializer


class ChatMessageRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom]
    serializer_class = ChatMessageRetrieveSerializer

    def get_object(self):
        id = self.kwargs['pk']
        room_id = self.kwargs['room_pk']
        return ChatMessage.objects.by_room_and_id(room_id, id)


class ChatMessageListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom]
    serializer_class = ChatMessageListSerializer

    def get_queryset(self):
        profile = self.request.user.get_default_profile()
        room_pk = self.kwargs['room_pk']

        return ChatMessage.objects.by_user_and_chatroom(
            profile, room_pk
        ).select_related('profile', 'chatroom').prefetch_related('chatroom__members',)


class ChatMessageUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom, IsCreatorForChatMessage]
    serializer_class = ChatMessageUpdateSerializer

    def get_object(self):
        id = self.kwargs['pk']
        room_id = self.kwargs['room_pk']
        return ChatMessage.objects.by_room_and_id(room_id, id)


class ChatMessageDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom, IsCreatorForChatMessage]
    serializer_class = ChatMessageDestroySerializer

    def get_object(self):
        id = self.kwargs['pk']
        room_id = self.kwargs['room_pk']
        return ChatMessage.objects.by_room_and_id(room_id, id)
