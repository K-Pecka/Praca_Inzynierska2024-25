from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from itineraries.serializers.itinerary_activity_serializers import ItineraryActivityCreateSerializer, \
    ItineraryActivitySerializer, ItineraryActivityUpdateSerializer, ItineraryActivityDeleteSerializer

from itineraries.models import ItineraryActivity, Itinerary
from server.permissions import IsTripCreator, IsTripParticipant


@extend_schema(tags=['itinerary activity'])
class ItineraryActivityCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = ItineraryActivityCreateSerializer


@extend_schema(tags=['itinerary activity'])
class ItineraryActivityRetrieveAPIView(RetrieveAPIView):
    queryset = ItineraryActivity.objects.all()
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ItineraryActivitySerializer


@extend_schema(tags=['itinerary activity'])
class ItineraryActivityListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ItineraryActivitySerializer
    lookup_url_kwarg = "itinerary_pk"

    def get_queryset(self):
        return ItineraryActivity.objects.by_itinerary(self.kwargs[self.lookup_url_kwarg])


@extend_schema(tags=['itinerary activity'])
class ItineraryActivityUpdateAPIView(UpdateAPIView):
    queryset = ItineraryActivity.objects.all()
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = ItineraryActivityUpdateSerializer


@extend_schema(tags=['itinerary activity'])
class ItineraryActivityDestroyAPIView(DestroyAPIView):
    queryset = ItineraryActivity.objects.all()
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = ItineraryActivityDeleteSerializer
