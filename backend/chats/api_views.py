from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
)

from .models import Chatroom, ChatMessage
from server.permissions import (
    IsCreatorForChatroom, IsParticipantForChatroom, IsCreatorForChatMessage, IsTripParticipant
)

from .serializers import (
    ChatroomCreateSerializer, ChatroomUpdateSerializer, ChatMessageCreateSerializer,
    ChatMessageUpdateSerializer, ChatroomRetrieveSerializer, ChatroomListSerializer,
    ChatMessageRetrieveSerializer, ChatMessageListSerializer
)


#####################################################################
# Chatroom Views
#####################################################################
class ChatroomCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ChatroomCreateSerializer


class ChatroomRetrieveAPIView(RetrieveAPIView):
    queryset = Chatroom.objects.all()
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom]
    serializer_class = ChatroomRetrieveSerializer


class ChatroomListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ChatroomListSerializer

    def get_queryset(self):
        return (
            Chatroom.objects
            .by_user(self.request.user.get_default_profile())
            .select_related('creator')
            .prefetch_related('members')
        )


class ChatroomUpdateAPIView(UpdateAPIView):
    queryset = Chatroom.objects.all()
    permission_classes = [IsAuthenticated, IsTripParticipant, IsCreatorForChatroom]
    serializer_class = ChatroomUpdateSerializer


class ChatroomDestroyAPIView(DestroyAPIView):
    queryset = Chatroom.objects.all()
    permission_classes = [IsAuthenticated, IsTripParticipant, IsCreatorForChatroom]


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
        return ChatMessage.objects.by_chatroom_pk(self.kwargs['room_pk'])


class ChatMessageListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom]
    serializer_class = ChatMessageListSerializer

    def get_queryset(self):
        return (ChatMessage.objects
            .by_user_and_chatroom(self.request.user.get_default_profile(), self.kwargs['room_pk'])
            .select_related('profile', 'chatroom')
            .prefetch_related('chatroom__members',)
        )


class ChatMessageUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom, IsCreatorForChatMessage]
    serializer_class = ChatMessageUpdateSerializer

    def get_object(self):
        return ChatMessage.objects.by_chatroom_pk(self.kwargs['room_pk'])


class ChatMessageDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom, IsCreatorForChatMessage]

    def get_object(self):
        return ChatMessage.objects.by_chatroom_pk(self.kwargs['room_pk'])
