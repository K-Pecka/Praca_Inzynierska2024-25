from drf_spectacular.utils import extend_schema
from django.db.models import Count

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated\

from django_filters.rest_framework import DjangoFilterBackend

from server.permissions import IsTripParticipant, IsTripCreator
from trips.filters import TripFilter
from trips.models import Trip
from trips.serializers.trip_serializers import TripListSerializer, TripRetrieveSerializer, TripCreateSerializer, \
    TripUpdateSerializer, TripDestroySerializer


@extend_schema(tags=['trip'])
class TripViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = TripFilter

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsTripParticipant()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsTripCreator()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.action == 'list':
            return (
                Trip.objects
                .by_user_profile(self.request.user.get_default_profile())
                .select_related('creator')
                .prefetch_related('members')
            ).order_by('-created_at')
        return Trip.objects.all()

    def get_object(self):
        trip_id = self.kwargs.get('pk')
        return Trip.objects.annotate(
            activity_count=Count('itineraries__activities')
        ).get(pk=trip_id)

    def get_serializer_class(self):
        if self.action == 'create':
            return TripCreateSerializer
        elif self.action == 'retrieve':
            return TripRetrieveSerializer
        elif self.action == 'list':
            return TripListSerializer
        elif self.action in ['update', 'partial_update']:
            return TripUpdateSerializer
        elif self.action == 'destroy':
            return TripDestroySerializer
        return TripRetrieveSerializer
