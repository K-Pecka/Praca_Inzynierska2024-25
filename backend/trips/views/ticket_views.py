from drf_spectacular.utils import extend_schema
from rest_framework.generics import UpdateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser

from server.permissions import IsTripParticipant, IsTicketOwner
from trips.models import Ticket
from trips.serializers.ticket_serializers import TicketCreateSerializer, TicketRetrieveSerializer, TicketListSerializer, \
    TicketUpdateSerializer, TicketDestroySerializer


@extend_schema(tags=['ticket'])
class TicketCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TicketCreateSerializer
    parser_classes = (MultiPartParser,)


@extend_schema(tags=['ticket'])
class TicketRetrieveAPIView(RetrieveAPIView):
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated, IsTripParticipant, IsTicketOwner]
    serializer_class = TicketRetrieveSerializer

@extend_schema(tags=['ticket'])
class TicketListByTripAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TicketListSerializer

    def get_queryset(self):
        trip_id = self.kwargs['trip_pk']
        profile = self.request.user.get_default_profile()
        return (
            Ticket.objects
            .by_trip_and_profile(trip_id, profile)
            .select_related('owner', 'trip')
        )


@extend_schema(tags=['ticket'])
class TicketListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TicketListSerializer

    def get_queryset(self):
        return (Ticket.objects
            .by_user(self.request.user.get_default_profile())
            .select_related('profile', 'trip')
        )


@extend_schema(tags=['ticket'])
class TicketUpdateAPIView(UpdateAPIView):
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated, IsTripParticipant, IsTicketOwner]
    serializer_class = TicketUpdateSerializer
    parser_classes = (MultiPartParser,)


@extend_schema(tags=['ticket'])
class TicketDestroyAPIView(DestroyAPIView):
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated, IsTripParticipant, IsTicketOwner]
    serializer_class = TicketDestroySerializer
