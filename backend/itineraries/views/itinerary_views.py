from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from itineraries.serializers.itinerary_serializers import ItineraryCreateSerializer, ItineraryRetrieveSerializer, \
    ItineraryUpdateSerializer, ItineraryDeleteSerializer

from itineraries.models import Itinerary
from server.permissions import IsTripCreator, IsTripParticipant


@extend_schema(tags=["itinerary"])
class ItineraryViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsTripCreator()]
        return [IsAuthenticated(), IsTripParticipant()]

    def get_queryset(self):
        return Itinerary.objects.filter(trip_id=self.kwargs['trip_pk'])

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.action == 'create':
            return ItineraryCreateSerializer
        elif self.action == 'retrieve':
            return ItineraryRetrieveSerializer
        elif self.action == 'list':
            return ItineraryRetrieveSerializer
        elif self.action in ['update', 'partial_update']:
            return ItineraryUpdateSerializer
        elif self.action == 'destroy':
            return ItineraryDeleteSerializer
        return ItineraryRetrieveSerializer
