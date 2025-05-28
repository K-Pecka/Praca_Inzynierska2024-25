from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

from server.permissions import IsTripParticipant, IsTicketOwner, IsTripCreator
from trips.models import Ticket
from trips.serializers.ticket_serializers import TicketCreateSerializer, TicketRetrieveSerializer, TicketListSerializer, \
    TicketUpdateSerializer, TicketDestroySerializer


@extend_schema(tags=['ticket'])
class TicketViewSet(ModelViewSet):
    parser_classes = (MultiPartParser,)

    def get_permissions(self):
        base = [IsAuthenticated(), IsTripParticipant()]
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            base.append(IsTicketOwner())
        elif self.action == 'list_all_for_trip':
            base.append(IsTripCreator())
        return base

    def get_queryset(self):
        trip_id = self.kwargs['trip_pk']
        profile = self.request.user.get_default_profile()
        return (
            Ticket.objects
            .by_trip_and_profile(trip_id, profile)
            .select_related('owner', 'trip')
        ).order_by('-created_at')

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.action == 'create':
            return TicketCreateSerializer
        elif self.action == 'retrieve':
            return TicketRetrieveSerializer
        elif self.action == 'list':
            return TicketListSerializer
        elif self.action in ['update', 'partial_update']:
            return TicketUpdateSerializer
        elif self.action == 'destroy':
            return TicketDestroySerializer
        return TicketRetrieveSerializer

    @action(detail=False, methods=['get'], url_path='all')
    def by_trip(self, request, trip_pk=None):
        tickets = Ticket.objects.filter(trip_id=trip_pk).select_related('owner', 'trip')
        serializer = TicketListSerializer(tickets, many=True)
        return Response(serializer.data)