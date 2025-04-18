from drf_spectacular.utils import extend_schema

from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from chats.serializers.chat_message_serializers import ChatMessageCreateSerializer, ChatMessageRetrieveSerializer, \
    ChatMessageListSerializer, ChatMessageUpdateSerializer

from chats.models import ChatMessage
from server.permissions import IsTripParticipant, IsParticipantForChatroom, IsCreatorForChatMessage


@extend_schema(tags=['chat_message'])
class ChatMessageCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom]
    serializer_class = ChatMessageCreateSerializer


@extend_schema(tags=['chat_message'])
class ChatMessageRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom]
    serializer_class = ChatMessageRetrieveSerializer

    def get_object(self):
        return ChatMessage.objects.by_chatroom_pk(self.kwargs['room_pk'])


@extend_schema(tags=['chat_message'])
class ChatMessageListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom]
    serializer_class = ChatMessageListSerializer

    def get_queryset(self):
        return (ChatMessage.objects
            .by_user_and_chatroom(self.request.user.get_default_profile(), self.kwargs['room_pk'])
            .select_related('profile', 'chatroom')
            .prefetch_related('chatroom__members',)
        )


@extend_schema(tags=['chat_message'])
class ChatMessageUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom, IsCreatorForChatMessage]
    serializer_class = ChatMessageUpdateSerializer

    def get_object(self):
        return ChatMessage.objects.by_chatroom_pk(self.kwargs['room_pk'])


@extend_schema(tags=['chat_message'])
class ChatMessageDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom, IsCreatorForChatMessage]

    def get_object(self):
        return ChatMessage.objects.by_chatroom_pk(self.kwargs['room_pk'])

