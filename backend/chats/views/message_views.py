from drf_spectacular.utils import extend_schema

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from chats.serializers.message_serializers import MessageCreateSerializer, MessageRetrieveSerializer, \
    MessageListSerializer, MessageUpdateSerializer

from chats.models import Message
from server.permissions import IsTripParticipant, IsParticipantForChatroom, IsCreatorForMessage


@extend_schema(tags=['message'])
class MessageViewSet(ModelViewSet):
    """
    ViewSet obsługujący tworzenie, pobieranie, listowanie, aktualizację
    i usuwanie wiadomości w obrębie czatu.
    """
    queryset = Message.objects.all()  # nie używane bezpośrednio – nadpisujemy `get_queryset`

    def get_permissions(self):
        base = [IsAuthenticated(), IsTripParticipant(), IsParticipantForChatroom()]
        if self.action in ['update', 'partial_update', 'destroy']:
            base.append(IsCreatorForMessage())
        return base

    def get_queryset(self):
        return (
            Message.objects
            .filter(chatroom_id=self.kwargs['room_pk'])
            .select_related('profile', 'chatroom')
            .prefetch_related('chatroom__members')
        )

    def get_object(self):
        return Message.objects.by_chatroom_pk(self.kwargs['room_pk'])

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        elif self.action == 'retrieve':
            return MessageRetrieveSerializer
        elif self.action == 'list':
            return MessageListSerializer
        elif self.action in ['update', 'partial_update']:
            return MessageUpdateSerializer
        elif self.action == 'destroy':
            return MessageRetrieveSerializer
        return MessageRetrieveSerializer
