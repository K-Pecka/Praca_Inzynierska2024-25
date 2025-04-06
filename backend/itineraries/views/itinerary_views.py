from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from itineraries.serializers.itinerary_serializers import ItineraryCreateSerializer, ItineraryRetrieveSerializer, \
    ItineraryUpdateSerializer, ItineraryDeleteSerializer

from itineraries.models import Itinerary
from server.permissions import IsTripCreator, IsTripParticipant


@extend_schema(tags=['itinerary'])
class ItineraryCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = ItineraryCreateSerializer


@extend_schema(tags=['itinerary'])
class ItineraryRetrieveAPIView(RetrieveAPIView):
    queryset = Itinerary.objects.all()
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ItineraryRetrieveSerializer


@extend_schema(tags=['itinerary'])
class ItineraryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ItineraryRetrieveSerializer

    def get_queryset(self):
        return Itinerary.objects.filter(trip=self.kwargs['trip_pk'])


@extend_schema(tags=['itinerary'])
class ItineraryUpdateAPIView(UpdateAPIView):
    queryset = Itinerary.objects.all()
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = ItineraryUpdateSerializer


@extend_schema(tags=['itinerary'])
class ItineraryDestroyAPIView(DestroyAPIView):
    queryset = Itinerary.objects.all()
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = ItineraryDeleteSerializer
