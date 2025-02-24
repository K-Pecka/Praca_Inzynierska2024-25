from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from server.permissions import IsTripCreator, IsTripParticipant
from .models import Itinerary, ItineraryActivity
from .serializers import ItinerarySerializer, ItineraryActivitySerializer, ItineraryCreateSerializer, \
    ItineraryUpdateSerializer, ItineraryDeleteSerializer, ItineraryActivityCreateSerializer, \
    ItineraryActivityUpdateSerializer, ItineraryActivityDeleteSerializer


class ItineraryCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = ItineraryCreateSerializer


class ItineraryRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ItinerarySerializer

    def get_object(self):
        return Itinerary.objects.by_id(self.kwargs['pk'])


class ItineraryUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = ItineraryUpdateSerializer

    def get_object(self):
        return Itinerary.objects.by_id(self.kwargs['pk'])


class ItineraryDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = ItineraryDeleteSerializer

    def get_object(self):
        return Itinerary.objects.by_id(self.kwargs['pk'])


class ItineraryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ItinerarySerializer

    def get_queryset(self):
        return Itinerary.objects.by_trip(self.kwargs['trip_pk'])


class ItineraryActivityCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItineraryActivityCreateSerializer

class ItineraryActivityRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ItineraryActivitySerializer

    def get_object(self):
        return ItineraryActivity.objects.by_id(self.kwargs['pk'])


class ItineraryActivityUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = ItineraryActivityUpdateSerializer

    def get_object(self):
        return ItineraryActivity.objects.by_id(self.kwargs['pk'])


class ItineraryActivityDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTripCreator]
    serializer_class = ItineraryActivityDeleteSerializer

    def get_object(self):
        return ItineraryActivity.objects.by_id(self.kwargs['pk'])


class ItineraryActivityListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsTripParticipant]
    serializer_class = ItineraryActivitySerializer
    lookup_url_kwarg = "itinerary_pk"
    def get_queryset(self):
        return ItineraryActivity.objects.by_itinerary(self.kwargs[self.lookup_url_kwarg])
