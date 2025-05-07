from drf_spectacular.utils import extend_schema
from django.db.models import Count

from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated\

from server.permissions import IsTripParticipant, IsTripCreator
from trips.models import Trip
from trips.serializers.trip_serializers import TripListSerializer, TripRetrieveSerializer, TripCreateSerializer, \
    TripUpdateSerializer, TripDestroySerializer


@extend_schema(tags=['trip'])
class TripCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TripCreateSerializer


@extend_schema(tags=['trip'])
class TripRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TripRetrieveSerializer

    def get_queryset(self):
        return Trip.objects.annotate(
            activity_count=Count('itineraries__activities')
        )


@extend_schema(tags=['trip'])
class TripListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = TripListSerializer

    def get_queryset(self):
        return (Trip.objects
            .by_user_profile(self.request.user.get_default_profile())
            .select_related('creator')
            .prefetch_related('members')
        )

@extend_schema(tags=['trip'])
class TripUpdateAPIView(UpdateAPIView):
    queryset = Trip.objects.all()
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = TripUpdateSerializer


@extend_schema(tags=['trip'])
class TripDestroyAPIView(DestroyAPIView):
    queryset = Trip.objects.all()
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = TripDestroySerializer

