from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from itineraries.serializers.itinerary_serializers import ItineraryCreateSerializer, ItinerarySerializer, \
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
    serializer_class = ItinerarySerializer


@extend_schema(tags=['itinerary'])
class ItineraryListAPIView(ListAPIView):
    queryset = Itinerary.objects.all()
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ItinerarySerializer


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
