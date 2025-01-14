from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Itinerary
from .serializers import ItinerarySerializer


class ItineraryCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItinerarySerializer


class ItineraryRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItinerarySerializer

    def get_object(self):
        return Itinerary.objects.get(pk=self.kwargs['pk'])


class ItineraryUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItinerarySerializer

    def get_object(self):
        return Itinerary.objects.get(pk=self.kwargs['pk'])


class ItineraryDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItinerarySerializer

    def get_object(self):
        return Itinerary.objects.get(pk=self.kwargs['pk'])


class ItineraryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer
