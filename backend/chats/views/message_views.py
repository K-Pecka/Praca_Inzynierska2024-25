from drf_spectacular.utils import extend_schema

from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from chats.serializers.message_serializers import MessageCreateSerializer, MessageRetrieveSerializer, \
    MessageListSerializer, MessageUpdateSerializer

from chats.models import Message
from server.permissions import IsTripParticipant, IsParticipantForChatroom, IsCreatorForMessage


@extend_schema(tags=['message'])
class MessageCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom]
    serializer_class = MessageCreateSerializer


@extend_schema(tags=['message'])
class MessageRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom]
    serializer_class = MessageRetrieveSerializer

    def get_object(self):
        return Message.objects.by_chatroom_pk(self.kwargs['room_pk'])


@extend_schema(tags=['message'])
class MessageListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom]
    serializer_class = MessageListSerializer

    def get_queryset(self):
        return (Message.objects
            .by_user_and_chatroom(self.request.user.get_default_profile(), self.kwargs['room_pk'])
            .select_related('profile', 'chatroom')
            .prefetch_related('chatroom__members',)
        )


@extend_schema(tags=['message'])
class MessageUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom, IsCreatorForMessage]
    serializer_class = MessageUpdateSerializer

    def get_object(self):
        return Message.objects.by_chatroom_pk(self.kwargs['room_pk'])


@extend_schema(tags=['message'])
class MessageDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom, IsCreatorForMessage]

    def get_object(self):
        return Message.objects.by_chatroom_pk(self.kwargs['room_pk'])

