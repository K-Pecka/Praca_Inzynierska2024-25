from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from itineraries.serializers.itinerary_activity_serializers import ItineraryActivityCreateSerializer, \
    ItineraryActivityUpdateSerializer, ItineraryActivityDeleteSerializer, ItineraryActivityRetrieveSerializer, \
    ItineraryActivityListSerializer

from itineraries.models import ItineraryActivity, Itinerary
from server.permissions import IsTripCreator, IsTripParticipant


@extend_schema(tags=["itinerary activity"])
class ItineraryActivityViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsTripCreator()]
        return [IsAuthenticated(), IsTripParticipant()]

    def get_queryset(self):
        return ItineraryActivity.objects.by_itinerary(self.kwargs['itinerary_pk'])

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), pk=self.kwargs['pk']
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return ItineraryActivityCreateSerializer
        elif self.action == 'retrieve':
            return ItineraryActivityRetrieveSerializer
        elif self.action == 'list':
            return ItineraryActivityListSerializer
        elif self.action in ['update', 'partial_update']:
            return ItineraryActivityUpdateSerializer
        elif self.action == 'destroy':
            return ItineraryActivityDeleteSerializer
        return ItineraryActivityRetrieveSerializer
