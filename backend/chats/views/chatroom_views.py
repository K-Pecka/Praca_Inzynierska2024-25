from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from chats.choices import ChatroomType
from chats.serializers.chatroom_serializers import ChatroomCreateSerializer, ChatroomRetrieveSerializer, \
    ChatroomListSerializer, ChatroomUpdateSerializer
from chats.models import Chatroom
from server.permissions import IsTripParticipant, IsParticipantForChatroom, IsCreatorForChatroom
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from users.models import UserProfile
from trips.models import Trip
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


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
        return (
            Chatroom.objects
            .by_user(self.request.user.get_default_profile())
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


@extend_schema(tags=['chat_room'])
class ChatroomCreateOrGetAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        trip_id = request.data.get("trip_id")
        receiver_id = request.data.get("receiver_id")

        if not all([trip_id, receiver_id]):
            return Response(
                {"detail": "trip_id i receiver_id są wymagane."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            trip = Trip.objects.get(pk=trip_id)
            receiver = UserProfile.objects.get(pk=receiver_id)
        except (Trip.DoesNotExist, UserProfile.DoesNotExist):
            return Response(
                {"detail": "Nieprawidłowy trip_id lub receiver_id"},
                status=status.HTTP_404_NOT_FOUND
            )

        creator = request.user.get_default_profile()

        chatroom = Chatroom.objects.filter(
            type=ChatroomType.PRIVATE,
            trip=trip,
            members=creator,
        ).filter(members=receiver).first()

        if chatroom:
            serializer = ChatroomRetrieveSerializer(chatroom)
            return Response(serializer.data, status=status.HTTP_200_OK)

        chatroom = Chatroom.objects.create(
            name=f"Czat: {creator.user.first_name} & {receiver.user.first_name}",
            type=ChatroomType.PRIVATE,
            trip=trip,
            creator=creator,
        )
        chatroom.members.add(creator, receiver)
        serializer = ChatroomRetrieveSerializer(chatroom)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
