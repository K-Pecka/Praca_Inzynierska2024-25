from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from chats.serializers.chatroom_serializers import ChatroomCreateSerializer, ChatroomRetrieveSerializer, \
    ChatroomListSerializer, ChatroomUpdateSerializer

from chats.models import Chatroom
from server.permissions import IsTripParticipant, IsParticipantForChatroom, IsCreatorForChatroom


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
