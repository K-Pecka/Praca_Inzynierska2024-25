from drf_spectacular.utils import extend_schema

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from chats.serializers.chatroom_serializers import ChatroomCreateSerializer, ChatroomRetrieveSerializer, \
    ChatroomListSerializer, ChatroomUpdateSerializer
from chats.models import Chatroom
from server.permissions import IsTripParticipant, IsParticipantForChatroom, IsCreatorForChatroom


@extend_schema(tags=['chat_room'])
class ChatroomViewSet(ModelViewSet):
    """
    ViewSet do obsługi tworzenia, listowania, pobierania,
    aktualizacji i usuwania pokojów czatowych (chatroomów).
    """
    def get_permissions(self):
        base = [IsAuthenticated(), IsTripParticipant()]
        if self.action in ['retrieve']:
            base.append(IsParticipantForChatroom())
        elif self.action in ['update', 'partial_update', 'destroy']:
            base.append(IsCreatorForChatroom())
        return base

    def get_queryset(self):
        if self.action == 'list':
            trip_id = self.kwargs.get("trip_pk")
            return (
                Chatroom.objects
                .by_user(self.request.user.get_default_profile())
                .filter(trip_id=trip_id)
                .select_related('creator')
                .prefetch_related('members')
            ).order_by('-created_at')
        return Chatroom.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ChatroomCreateSerializer
        elif self.action == 'retrieve':
            return ChatroomRetrieveSerializer
        elif self.action == 'list':
            return ChatroomListSerializer
        elif self.action in ['update', 'partial_update']:
            return ChatroomUpdateSerializer
        elif self.action == 'destroy':
            return ChatroomRetrieveSerializer  # lub osobny serializer jeśli masz
        return ChatroomRetrieveSerializer
