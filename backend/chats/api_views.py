from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
)

from .models import Chatroom, ChatMessage
from server.permissions import IsCreatorForChatroom, IsParticipantForChatroom, IsCreatorForChatMessage, \
    IsTripParticipant, IsTripCreator
from .serializers import (
    ChatroomCreateSerializer, ChatroomUpdateSerializer, ChatMessageCreateSerializer, ChatroomSerializer,
    ChatMessageSerializer, ChatMessageUpdateSerializer
)


#####################################################################
# Chatroom Views
#####################################################################
class ChatroomCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ChatroomCreateSerializer


class ChatroomRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom]
    serializer_class = ChatroomSerializer

    def get_object(self):
        return Chatroom.objects.by_id(self.kwargs['pk']).select_related('creator').prefetch_related('members')

class ChatroomListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ChatroomSerializer

    def get_queryset(self):
        profile = self.request.user.get_default_profile()

        return Chatroom.objects.for_user(profile).select_related('creator').prefetch_related('members')


class ChatroomUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsCreatorForChatroom]
    serializer_class = ChatroomUpdateSerializer

    def get_object(self):
        return Chatroom.objects.by_id(self.kwargs['pk']).select_related('creator').prefetch_related('members')


class ChatroomDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsCreatorForChatroom]
    serializer_class = ChatroomSerializer

    def get_object(self):
        return Chatroom.objects.by_id(self.kwargs['pk']).select_related('creator').prefetch_related('members')


#####################################################################
# ChatMessage Views
#####################################################################
class ChatMessageCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom]
    serializer_class = ChatMessageCreateSerializer


class ChatMessageRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom]
    serializer_class = ChatMessageSerializer

    def get_object(self):
        return ChatMessage.objects.by_room_and_id(
            self.kwargs['pk'], self.kwargs['room_pk']
        ).select_related('profile', 'chatroom').prefetch_related('chatroom__members',)


class ChatMessageListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        profile = self.request.user.get_user_permissions()

        return ChatMessage.objects.for_user_and_chatroom(
            profile, self.kwargs['room_pk']
        ).select_related('profile', 'chatroom').prefetch_related('chatroom__members',)


class ChatMessageUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsCreatorForChatMessage]
    serializer_class = ChatMessageUpdateSerializer

    def get_object(self):
        return ChatMessage.objects.by_room_and_id(
            self.kwargs['pk'], self.kwargs['room_pk']
        ).select_related('profile', 'chatroom').prefetch_related('chatroom__members',)


class ChatMessageDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsCreatorForChatMessage]
    serializer_class = ChatMessageSerializer

    def get_object(self):
        return ChatMessage.objects.by_room_and_id(
            self.kwargs['pk'], self.kwargs['room_pk']
        ).select_related('profile', 'chatroom').prefetch_related('chatroom__members',)
