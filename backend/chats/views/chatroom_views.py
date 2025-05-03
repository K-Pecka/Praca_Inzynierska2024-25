from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from chats.choices import ChatroomType
from chats.serializers.chatroom_serializers import ChatroomCreateSerializer, ChatroomRetrieveSerializer, \
    ChatroomListSerializer, ChatroomUpdateSerializer
from chats.models import Chatroom
from server.permissions import IsTripParticipant, IsParticipantForChatroom, IsCreatorForChatroom


@extend_schema(tags=['chat_room'])
class ChatroomCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ChatroomCreateSerializer


@extend_schema(tags=['chat_room'])
class ChatroomRetrieveAPIView(RetrieveAPIView):
    queryset = Chatroom.objects.all()
    permission_classes = [IsAuthenticated, IsTripParticipant, IsParticipantForChatroom]
    serializer_class = ChatroomRetrieveSerializer


@extend_schema(tags=['chat_room'])
class ChatroomListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ChatroomListSerializer

    def get_queryset(self):
        trip_id = self.kwargs.get("trip_pk")
        return (
            Chatroom.objects
            .by_user(self.request.user.get_default_profile())
            .filter(trip_id=trip_id)
            .select_related('creator')
            .prefetch_related('members')
        )


@extend_schema(tags=['chat_room'])
class ChatroomUpdateAPIView(UpdateAPIView):
    queryset = Chatroom.objects.all()
    permission_classes = [IsAuthenticated, IsTripParticipant, IsCreatorForChatroom]
    serializer_class = ChatroomUpdateSerializer


@extend_schema(tags=['chat_room'])
class ChatroomDestroyAPIView(DestroyAPIView):
    queryset = Chatroom.objects.all()
    permission_classes = [IsAuthenticated, IsTripParticipant, IsCreatorForChatroom]
